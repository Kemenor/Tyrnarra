#!/usr/bin/env python3
r"""
tokenize.py - bake a circular VTT token from a portrait + a frame (Tokenizer-style).

The portrait is circle-masked (transparent corners); the frame is masked to a
clean circular annulus (its ornate band kept, center + corners discarded) and
laid over the rim. Output is one RGBA PNG ready to use as a token texture with
the Dynamic Token Ring turned OFF (the border is baked in).

Frames can be AI-generated ornate rings on any background: we impose the ring
geometry, so the model never has to produce real transparency.

Single:
  python tokenize.py bake --portrait portraits/sable-rei.webp --frame frames/bridge.webp \
      --out tokens/sable-rei.png

Batch (a JSON map of {portrait-stem: frame-path|frame-stem}, or a default frame):
  python tokenize.py batch --portraits portraits --frames frames --out tokens \
      --map faction_frames.json --default frames/generic.webp
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    sys.exit("Missing dep. Run: pip install pillow")


def _crop_square(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def _circle_mask(size, feather):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m


def _annulus_mask(size, inner_frac, feather):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((0, 0, size - 1, size - 1), fill=255)
    c = size / 2
    r = c * inner_frac
    d.ellipse((c - r, c - r, c + r, c + r), fill=0)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m


def bake(portrait, frame, out, size=512, inner=0.84, feather=1):
    """Circle-crop portrait, annulus-mask frame over the rim, save RGBA PNG."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    p = _crop_square(Image.open(portrait).convert("RGBA")).resize((size, size), Image.LANCZOS)
    canvas.paste(p, (0, 0), _circle_mask(size, feather))
    if frame:
        f = Image.open(frame).convert("RGBA").resize((size, size), Image.LANCZOS)
        ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        # combine the frame's own alpha (if any) with the imposed annulus
        band = _annulus_mask(size, inner, feather)
        fa = f.split()[3].point(lambda a: a)  # frame alpha
        band = Image.composite(band, Image.new("L", (size, size), 0), fa) if frame.lower().endswith(".png") else band
        ring.paste(f, (0, 0), band)
        canvas = Image.alpha_composite(canvas, ring)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    canvas.save(out)
    return out


def _resolve_frame(val, frames_dir):
    if not val:
        return None
    if os.path.sep in val or "/" in val or os.path.exists(val):
        return val
    for ext in (".webp", ".png", ".jpg", ".jpeg"):
        cand = os.path.join(frames_dir, val + ext)
        if os.path.exists(cand):
            return cand
    return val


def main():
    ap = argparse.ArgumentParser(description="Bake circular tokens from portraits + frames.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bake", help="One portrait + frame -> one token.")
    b.add_argument("--portrait", required=True)
    b.add_argument("--frame", help="Frame image (omit for a plain circle crop).")
    b.add_argument("--out", required=True)
    b.add_argument("--size", type=int, default=512)
    b.add_argument("--inner", type=float, default=0.84, help="Portrait circle as a fraction of radius (rest is frame band).")
    b.add_argument("--feather", type=float, default=1.0)

    z = sub.add_parser("batch", help="Bake a folder of portraits, choosing a frame per stem.")
    z.add_argument("--portraits", required=True, help="Directory of portrait images.")
    z.add_argument("--frames", default="", help="Directory frame stems resolve against.")
    z.add_argument("--out", required=True, help="Output directory for <stem>.png tokens.")
    z.add_argument("--map", help="JSON {portrait-stem: frame (path or stem)}.")
    z.add_argument("--default", help="Frame for stems not in the map.")
    z.add_argument("--size", type=int, default=512)
    z.add_argument("--inner", type=float, default=0.84)
    z.add_argument("--feather", type=float, default=1.0)

    a = ap.parse_args()
    if a.cmd == "bake":
        print(bake(a.portrait, a.frame, a.out, a.size, a.inner, a.feather))
        return

    fmap = json.load(open(a.map, encoding="utf-8-sig")) if a.map else {}
    exts = (".webp", ".png", ".jpg", ".jpeg")
    n = 0
    for f in sorted(os.listdir(a.portraits)):
        if not f.lower().endswith(exts):
            continue
        stem = os.path.splitext(f)[0]
        frame = _resolve_frame(fmap.get(stem, a.default), a.frames)
        out = os.path.join(a.out, stem + ".png")
        bake(os.path.join(a.portraits, f), frame, out, a.size, a.inner, a.feather)
        print(f"  {stem} + {os.path.basename(frame) if frame else 'no frame'} -> {out}")
        n += 1
    print(f"\nBaked {n} tokens -> {a.out}")


if __name__ == "__main__":
    main()
