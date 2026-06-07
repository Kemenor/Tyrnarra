#!/usr/bin/env python3
r"""
tokenize.py - bake a circular VTT token from a portrait + a frame (Tokenizer-style).

Two frame sources, both supported:
  - A *transparent* frame PNG (you cut it, or `prep` chroma-keyed it): the ring's
    own alpha is used, so the bake is exact - no gray edge.
  - A raw opaque frame (AI art on a flat field) with no usable alpha: falls back
    to masking a circular annulus (can leave a faint edge; prefer prep first).

Commands:
  prep   raw AI frame on a solid chroma field -> transparent ring PNG (key out
         the field colour; render the ring on e.g. solid magenta with a magenta
         centre so only the ring survives).
  bake   one portrait + frame -> one token PNG (transparent corners).
  batch  bake a folder of portraits, choosing a frame per stem.

Examples:
  python tokenize.py prep --in frames/bridge.webp --out frames/bridge.cut.png
  python tokenize.py bake --portrait portraits/sable-rei.webp --frame frames/bridge.cut.png --out tokens/sable-rei.png
  python tokenize.py batch --portraits portraits --frames frames --out tokens --map faction_frames.json --default frames/generic.cut.png
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    sys.exit("Missing dep. Run: pip install pillow numpy")


def _crop_square(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def _circle_mask(size, feather, radius_frac=0.995):
    m = Image.new("L", (size, size), 0)
    c, r = size / 2, size / 2 * radius_frac
    ImageDraw.Draw(m).ellipse((c - r, c - r, c + r, c + r), fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m


def _annulus_mask(size, inner_frac, feather):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((0, 0, size - 1, size - 1), fill=255)
    c, r = size / 2, size / 2 * inner_frac
    d.ellipse((c - r, c - r, c + r, c + r), fill=0)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m


def _has_alpha(img):
    if img.mode != "RGBA":
        return False
    a = img.split()[3]
    lo, hi = a.getextrema()
    return lo < 240  # has meaningful transparency


def prep(frame_in, out, hue=None, hue_tol=26, sat_min=55, feather=1.5, despill=True):
    """Key a magenta-field AI frame into a transparent ring PNG, by HUE.

    Hue keying (not brightness) removes the bright field AND the ring's darker
    drop-shadow (same magenta hue, lower value), which a distance key leaves as a
    magenta halo. A magenta despill then neutralises any residual edge fringe.
    """
    try:
        import numpy as np
    except ImportError:
        sys.exit("prep needs numpy. Run: pip install numpy")
    im = Image.open(frame_in).convert("RGB")
    rgb = np.asarray(im).astype(np.float32)
    hsv = np.asarray(im.convert("HSV")).astype(np.float32)
    H, S = hsv[:, :, 0], hsv[:, :, 1]                  # PIL HSV: 0-255 each
    if hue is None:                                    # key hue = median of the four corners
        h, w = H.shape
        hue = float(np.median([H[2, 2], H[2, w - 3], H[h - 3, 2], H[h - 3, w - 3]]))
    hue_dist = np.minimum(np.abs(H - hue), 255 - np.abs(H - hue))
    keyness = np.clip(1 - hue_dist / hue_tol, 0, 1) * np.clip((S - sat_min) / (sat_min * 0.5), 0, 1)
    alpha = (1 - keyness) * 255.0
    if despill:                                        # remove magenta excess = (R+B)/2 - G
        m = np.clip((rgb[:, :, 0] + rgb[:, :, 2]) / 2 - rgb[:, :, 1], 0, None)
        rgb[:, :, 0] -= m
        rgb[:, :, 2] -= m
    arr = np.dstack([rgb, alpha]).clip(0, 255).astype("uint8")
    cut = Image.fromarray(arr, "RGBA")
    if feather:
        cut.putalpha(cut.split()[3].filter(ImageFilter.GaussianBlur(feather)))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    cut.save(out)
    return out, hue


def bake(portrait, frame, out, size=512, inner=0.84, feather=1.0, frame_mode="auto"):
    """Circle-crop portrait; layer frame (transparent -> exact; opaque -> annulus)."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    p = _crop_square(Image.open(portrait).convert("RGBA")).resize((size, size), Image.LANCZOS)
    # Portrait sits inside the ring (0.96 radius) so the band always overlaps its
    # rim and the art never spills past the frame.
    canvas.paste(p, (0, 0), _circle_mask(size, feather, 0.96))
    if frame:
        f = Image.open(frame).convert("RGBA").resize((size, size), Image.LANCZOS)
        use_alpha = frame_mode == "alpha" or (frame_mode == "auto" and _has_alpha(f))
        if use_alpha:
            # Auto-fit: scale the ring so its opaque extent reaches the token edge,
            # regardless of how large the model drew it. Then composite its own alpha.
            # Threshold the alpha first so faint key remnants don't inflate the bbox.
            bbox = f.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox()
            if bbox:
                bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
                scale = (size * 0.995) / max(bw, bh)
                ring = f.crop(bbox).resize((max(1, round(bw * scale)), max(1, round(bh * scale))), Image.LANCZOS)
                f = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                f.paste(ring, ((size - ring.width) // 2, (size - ring.height) // 2), ring)
            canvas = Image.alpha_composite(canvas, f)        # exact: frame's own alpha
        else:
            ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            ring.paste(f, (0, 0), _annulus_mask(size, inner, feather))
            canvas = Image.alpha_composite(canvas, ring)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    canvas.save(out)
    return out


def _resolve_frame(val, frames_dir):
    if not val:
        return None
    if os.path.sep in val or "/" in val or os.path.exists(val):
        return val
    for ext in (".cut.png", ".png", ".webp", ".jpg", ".jpeg"):
        cand = os.path.join(frames_dir, val + ext)
        if os.path.exists(cand):
            return cand
    return val


def main():
    ap = argparse.ArgumentParser(description="Bake circular tokens from portraits + frames.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("prep", help="Chroma-key a flat-field AI frame into a transparent ring.")
    pr.add_argument("--in", dest="src", required=True)
    pr.add_argument("--out", required=True)
    pr.add_argument("--hue", type=float, help="Key hue 0-255 (PIL HSV); default = corner median (the field).")
    pr.add_argument("--hue-tol", type=float, default=26, help="Hue half-width keyed out.")
    pr.add_argument("--sat-min", type=float, default=55, help="Min saturation to count as the key (protects grey ring metal).")
    pr.add_argument("--feather", type=float, default=1.5)

    b = sub.add_parser("bake", help="One portrait + frame -> one token.")
    b.add_argument("--portrait", required=True)
    b.add_argument("--frame")
    b.add_argument("--out", required=True)
    b.add_argument("--size", type=int, default=512)
    b.add_argument("--inner", type=float, default=0.84, help="(annulus mode) portrait circle as fraction of radius.")
    b.add_argument("--feather", type=float, default=1.0)
    b.add_argument("--frame-mode", default="auto", choices=["auto", "alpha", "annulus"])

    z = sub.add_parser("batch", help="Bake a folder of portraits, a frame per stem.")
    z.add_argument("--portraits", required=True)
    z.add_argument("--frames", default="")
    z.add_argument("--out", required=True)
    z.add_argument("--map", help="JSON {portrait-stem: frame path or stem}.")
    z.add_argument("--default")
    z.add_argument("--size", type=int, default=512)
    z.add_argument("--inner", type=float, default=0.84)
    z.add_argument("--feather", type=float, default=1.0)
    z.add_argument("--frame-mode", default="auto", choices=["auto", "alpha", "annulus"])

    a = ap.parse_args()
    if a.cmd == "prep":
        _, used = prep(a.src, a.out, a.hue, a.hue_tol, a.sat_min, a.feather)
        print(f"{a.out}  (keyed hue {used:.0f})")
    elif a.cmd == "bake":
        print(bake(a.portrait, a.frame, a.out, a.size, a.inner, a.feather, a.frame_mode))
    else:
        fmap = json.load(open(a.map, encoding="utf-8-sig")) if a.map else {}
        exts = (".webp", ".png", ".jpg", ".jpeg")
        n = 0
        for f in sorted(os.listdir(a.portraits)):
            if not f.lower().endswith(exts):
                continue
            stem = os.path.splitext(f)[0]
            frame = _resolve_frame(fmap.get(stem, a.default), a.frames)
            out = os.path.join(a.out, stem + ".png")
            bake(os.path.join(a.portraits, f), frame, out, a.size, a.inner, a.feather, a.frame_mode)
            print(f"  {stem} + {os.path.basename(frame) if frame else 'no frame'} -> {out}")
            n += 1
        print(f"\nBaked {n} tokens -> {a.out}")


if __name__ == "__main__":
    main()
