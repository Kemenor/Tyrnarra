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
    from PIL import Image, ImageChops, ImageDraw, ImageFilter
except ImportError:
    sys.exit("Missing dep. Run: pip install pillow numpy")


def _crop_square(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def _circle_mask(size, feather, radius_frac=0.995, cy_frac=0.5):
    m = Image.new("L", (size, size), 0)
    c, r = size / 2, size / 2 * radius_frac
    cy = size * cy_frac
    ImageDraw.Draw(m).ellipse((c - r, cy - r, c + r, cy + r), fill=255)
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


def _framed(path, size, zoom=1.0, dy=0.0):
    """The image square-cropped to the token, zoomed about its centre and moved
    down by dy (a fraction of the token; negative moves it up)."""
    im = _crop_square(Image.open(path).convert("RGBA"))
    big = round(size * zoom)
    im = im.resize((big, big), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    off = (size - big) // 2
    out.paste(im, (off, off + round(dy * size)))
    return out


def bake(portrait, frame, out, size=512, inner=0.84, feather=1.0, frame_mode="auto",
         cutout=None, pop=(), zoom=1.0, dy=0.0, ring=0.995, ring_dy=0.0):
    """Circle-crop portrait; layer frame (transparent -> exact; opaque -> annulus).

    Pop-out: `cutout` is the same portrait with its background removed (same
    size and framing, e.g. from rembg); every `pop` box (x0, y0, x1, y1 as
    fractions of the token) lays the cut-out's figure back OVER the frame
    there, so a head or an arm breaks the border."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    p = _framed(portrait, size, zoom, dy)
    # Portrait sits inside the ring (0.96 radius) so the band always overlaps its
    # rim and the art never spills past the frame. A frame with ornaments above or
    # below the ring (a badge on top, drips under it) is taller than it is wide;
    # the auto-fit then shrinks the ring, so the portrait shrinks with the ring's
    # WIDTH, which is the ring itself.
    radius = 0.96
    if frame:
        f0 = Image.open(frame).convert("RGBA").resize((size, size), Image.LANCZOS)
        if frame_mode == "alpha" or (frame_mode == "auto" and _has_alpha(f0)):
            bb = f0.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox()
            if bb and (bb[3] - bb[1]) > (bb[2] - bb[0]):
                radius = 0.96 * (bb[2] - bb[0]) / (bb[3] - bb[1])
    # ring < 0.995 draws the frame smaller than the token and ring_dy moves it down,
    # leaving room above it for a pop-out head; the portrait circle follows the ring.
    canvas.paste(p, (0, 0), _circle_mask(size, feather, radius * ring / 0.995, 0.5 + ring_dy))
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
                scale = (size * ring) / max(bw, bh)
                rimg = f.crop(bbox).resize((max(1, round(bw * scale)), max(1, round(bh * scale))), Image.LANCZOS)
                f = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                f.paste(rimg, ((size - rimg.width) // 2, (size - rimg.height) // 2 + round(ring_dy * size)), rimg)
            canvas = Image.alpha_composite(canvas, f)        # exact: frame's own alpha
        else:
            ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            ring.paste(f, (0, 0), _annulus_mask(size, inner, feather))
            canvas = Image.alpha_composite(canvas, ring)
    if cutout and pop:
        c = _framed(cutout, size, zoom, dy)
        box = Image.new("L", (size, size), 0)
        d = ImageDraw.Draw(box)
        for x0, y0, x1, y1 in pop:
            d.rectangle([x0 * size, y0 * size, x1 * size, y1 * size], fill=255)
        box = box.filter(ImageFilter.GaussianBlur(size / 128))     # soft edge where the pop starts
        alpha = ImageChops.multiply(c.split()[3], box)
        c.putalpha(alpha)
        canvas = Image.alpha_composite(canvas, c)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    canvas.save(out)
    return out


def head_pop(portrait, frame, cutout, out, size=512, ring=0.9, ring_dy=0.06, head_top=0.015, zoom=1.0):
    """Bake with the head lifted over the frame, worked out from the cut-out.

    The figure is moved so the top of its head sits head_top below the token's
    top edge; the frame is drawn at `ring` of the token, moved down by ring_dy,
    so the head clears its top band; the pop box covers the head's width from
    the top edge down past the band. A head already cut off at the top of the
    source art is left inside the ring (a flat-topped pop-out reads badly)."""
    c = _framed(cutout, size, zoom).split()[3].point(lambda v: 255 if v > 128 else 0)
    w = c.width
    rows = [sum(1 for x in range(0, w, 2) if c.getpixel((x, y))) for y in range(c.height)]
    top = next((y for y, n in enumerate(rows) if n > w * 0.01), 0)
    if top < size * 0.01:
        return bake(portrait, frame, out, size, cutout=None, zoom=zoom), "head cut off in the art: plain"
    dy = head_top - top / size
    xs = sorted({x for y in range(top, min(c.height, top + int(size * 0.12))) for x in range(0, w, 2) if c.getpixel((x, y))})
    # the head is the widest run of columns; a stray bit of the cut-out (a bird, a
    # lantern) near the top is its own run and stays inside the ring
    runs, start = [], xs[0]
    for a_, b_ in zip(xs, xs[1:] + [None]):
        if b_ is None or b_ - a_ > size * 0.04:
            runs.append((start, a_))
            start = b_
    hx0, hx1 = max(runs, key=lambda r: r[1] - r[0])
    x0, x1 = max(0.0, hx0 / size - 0.03), min(1.0, hx1 / size + 0.03)
    # where the frame's top band really sits once placed: a frame with spires or
    # lanterns round it is drawn smaller, so its band runs lower than ring_top
    f = Image.open(frame).convert("RGBA").resize((size, size), Image.LANCZOS)
    fa = f.split()[3].point(lambda v: 255 if v > 128 else 0)
    bb = fa.getbbox()
    sc = (size * ring) / max(bb[2] - bb[0], bb[3] - bb[1])
    placed = Image.new("L", (size, size), 0)
    rimg = fa.crop(bb).resize((max(1, round((bb[2] - bb[0]) * sc)), max(1, round((bb[3] - bb[1]) * sc))))
    placed.paste(rimg, ((size - rimg.width) // 2, (size - rimg.height) // 2 + round(ring_dy * size)))
    band_bottom = 0
    for x in range(int(x0 * size), int(x1 * size), 2):
        col = [y for y in range(size // 2) if placed.getpixel((x, y))]
        if col:
            # the band is the first run of opaque rows from the top; its bottom is where the run ends
            run_end = col[0]
            for y in col[1:]:
                if y - run_end > 2:
                    break
                run_end = y
            band_bottom = max(band_bottom, run_end)
    box = (x0, 0.0, x1, band_bottom / size + 0.02)
    bake(portrait, frame, out, size, cutout=cutout, pop=[box], zoom=zoom, dy=dy, ring=ring, ring_dy=ring_dy)
    return out, f"head popped (dy {dy:+.3f})"


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
    b.add_argument("--zoom", type=float, default=1.0, help="Zoom the portrait (and cut-out) about its centre.")
    b.add_argument("--dy", type=float, default=0.0, help="Move the portrait down by this fraction of the token (negative: up).")
    b.add_argument("--ring", type=float, default=0.995, help="The frame's size as a fraction of the token (smaller leaves room for a pop-out).")
    b.add_argument("--ring-dy", type=float, default=0.0, help="Move the frame (and the portrait circle) down by this fraction of the token.")
    b.add_argument("--cutout", help="The portrait with its background removed (same framing), for --pop.")
    b.add_argument("--pop", action="append", default=[], metavar="X0,Y0,X1,Y1",
                   help="A box (fractions of the token) where the cut-out figure is laid over the frame. Repeatable.")

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

    h = sub.add_parser("headpop", help="Bake tokens with the head lifted over the frame, from cut-outs.")
    h.add_argument("--portraits", required=True, help="Folder of <slug>.png portraits.")
    h.add_argument("--cutouts", required=True, help="Folder of the same portraits with the background removed (<slug>-cutout.png or <slug>.png).")
    h.add_argument("--frames", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "token-frames"))
    h.add_argument("--map", required=True, help='JSON {frame-stem: [portrait slugs]}.')
    h.add_argument("--out", required=True)
    h.add_argument("--size", type=int, default=512)

    a = ap.parse_args()
    if a.cmd == "headpop":
        groups = json.load(open(a.map, encoding="utf-8"))
        for fr, slugs in groups.items():
            frame = _resolve_frame(fr, a.frames)
            for slug in slugs:
                cut = next((os.path.join(a.cutouts, slug + e) for e in ("-cutout.png", ".png")
                            if os.path.exists(os.path.join(a.cutouts, slug + e))), None)
                if not cut:
                    print(f"{slug}: no cut-out, skipped")
                    continue
                _, msg = head_pop(os.path.join(a.portraits, slug + ".png"), frame, cut,
                                  os.path.join(a.out, slug + ".png"), a.size)
                print(f"{slug} [{fr}]: {msg}")
        return
    if a.cmd == "prep":
        _, used = prep(a.src, a.out, a.hue, a.hue_tol, a.sat_min, a.feather)
        print(f"{a.out}  (keyed hue {used:.0f})")
    elif a.cmd == "bake":
        pop = [tuple(float(v) for v in p.split(",")) for p in a.pop]
        print(bake(a.portrait, a.frame, a.out, a.size, a.inner, a.feather, a.frame_mode,
                   cutout=a.cutout, pop=pop, zoom=a.zoom, dy=a.dy, ring=a.ring, ring_dy=a.ring_dy))
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
