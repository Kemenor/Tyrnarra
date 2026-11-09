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


def solidify(cut_path, out=None, floor=24, close=5):
    """Make a cut frame's ring solid: the magenta key leaves ring pixels whose
    colour sits near the key half-transparent, so a portrait shows through the
    band. Every pixel above `floor` alpha, with small gaps closed, becomes opaque."""
    im = Image.open(cut_path).convert("RGBA")
    m = im.split()[3].point(lambda v: 255 if v > floor else 0)
    m = m.filter(ImageFilter.MaxFilter(close)).filter(ImageFilter.MinFilter(close))   # close pinholes
    im.putalpha(m.filter(ImageFilter.GaussianBlur(0.6)))
    im.save(out or cut_path)
    return out or cut_path


def _ring_hole(frame_alpha):
    """(cx, cy, r) of the transparent hole inside a placed frame: the region
    round the canvas centre that the ring encloses. r reaches the hole's
    furthest edge, so the portrait meets the band with no gap and the band,
    being solid, hides the overlap."""
    size = frame_alpha.width
    m = frame_alpha.point(lambda v: 255 if v > 128 else 0)
    ImageDraw.floodfill(m, (size // 2, size // 2), 128)
    hole = m.point(lambda v: 255 if v == 128 else 0)
    bb = hole.getbbox()
    if not bb or (bb[2] - bb[0]) > size * 0.98:       # leaked: the ring is not closed
        return None
    return (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2, max(bb[2] - bb[0], bb[3] - bb[1]) / 2 + 2


def _ring_inside(alpha, cx, cy, rays=360):
    """The region inside a placed frame's band, as an L mask, or None.

    Along each ray from (cx, cy) the band is the longest run of opaque pixels;
    its start is the inside edge. The centre is first re-found from the band's
    top and bottom edges, since a frame with drips or a badge sits off its box."""
    import math
    size, height = alpha.size
    a = alpha.point(lambda v: 255 if v > 128 else 0).load()

    def edge(theta, cx, cy):
        best, start, run_start, run = (0, None), None, None, 0
        r = 0
        while True:
            x, y = int(cx + r * math.cos(theta)), int(cy + r * math.sin(theta))
            if not (0 <= x < size and 0 <= y < height):
                break
            if a[x, y]:
                if run_start is None:
                    run_start = r
                run += 1
            else:
                if run_start is not None and run > best[0]:
                    best = (run, run_start)
                run_start, run = None, 0
            r += 1
        if run_start is not None and run > best[0]:
            best = (run, run_start)
        return best[1]

    for _ in range(2):                                  # settle the centre on the band
        up, down = edge(-math.pi / 2, cx, cy), edge(math.pi / 2, cx, cy)
        left, right = edge(math.pi, cx, cy), edge(0, cx, cy)
        if None in (up, down, left, right):
            return None
        cy += (down - up) / 2
        cx += (right - left) / 2
    pts = []
    for k in range(rays):
        t = 2 * math.pi * k / rays
        r = edge(t, cx, cy)
        if r is None:
            return None
        pts.append((cx + (r + 3) * math.cos(t), cy + (r + 3) * math.sin(t)))
    m = Image.new("L", (size, height), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def ring_geometry(alpha, guess=None):
    """(cx, cy, outer diameter) in pixels of the ring in a frame's alpha: the
    centre of its hole, and the band's outer edge averaged over the four axes.
    Thin bits hanging off the band (lanterns, hooks) are opened away first."""
    w, h = alpha.size
    guess = guess or (w // 2, h // 2)
    inside = _ring_inside(alpha, guess[0], guess[1])
    if inside is None:
        return None
    hb = inside.getbbox()
    cx, cy = (hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2
    a = alpha.point(lambda v: 255 if v > 128 else 0)
    k = max(3, w // 64) | 1
    a = a.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    start = (hb[2] - hb[0]) / 2 - 4

    def out_edge(dx, dy):
        r, last = int(start), None
        while True:
            x, y = int(cx + dx * r), int(cy + dy * r)
            if not (0 <= x < w and 0 <= y < h):
                break
            if a.getpixel((x, y)):
                last = r
            elif last is not None and r - last > 3:
                break
            r += 1
        return last or r
    return cx, cy, (out_edge(1, 0) + out_edge(-1, 0) + out_edge(0, 1) + out_edge(0, -1)) / 2


def foundry_texture(token_png, ring_alpha, offset=(0, 0)):
    """{scale, anchorX, anchorY} for a token: the ring fills one grid square and
    sits on it, so a pop-out reaches past. ring_alpha is the ring as placed (the
    token's own frame layer), offset moves it into the token's canvas."""
    tw, th = Image.open(token_png).size
    g = ring_geometry(ring_alpha)
    if g is None:
        return None
    cx, cy, d = g
    k = tw / ring_alpha.width if ring_alpha.width == ring_alpha.height else 1.0
    cx, cy, d = (cx + offset[0]) * k, (cy + offset[1]) * k, d * k
    return {"scale": round(tw / d, 3), "anchorX": round(cx / tw, 3), "anchorY": round(cy / th, 3)}


def export_ora(ora, out, ring_layer="data/layer1.png", size=512, margin=8):
    """A hand-made token (a Pinta/Krita .ora) -> a square PNG centred on its ring,
    big enough that nothing that breaks out of the ring is clipped, and the
    Foundry texture {scale, anchorX, anchorY} for it (anchor is the centre, since
    the canvas is built round the ring). ring_layer is the layer holding the ring."""
    import zipfile, io
    z = zipfile.ZipFile(ora)
    merged = Image.open(io.BytesIO(z.read("mergedimage.png"))).convert("RGBA")
    ring_a = Image.open(io.BytesIO(z.read(ring_layer))).convert("RGBA").split()[3]
    bb = ring_a.point(lambda v: 255 if v > 128 else 0).getbbox()
    cx, cy, d = ring_geometry(ring_a, ((bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2))
    cb = merged.split()[3].point(lambda v: 255 if v > 16 else 0).getbbox()
    half = max(cx - cb[0], cb[2] - cx, cy - cb[1], cb[3] - cy) + margin
    side = int(round(2 * half))
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.alpha_composite(merged, (int(round(side / 2 - cx)), int(round(side / 2 - cy))))
    sq.resize((size, size), Image.LANCZOS).save(out)
    return {"scale": round(side / d, 3), "anchorX": 0.5, "anchorY": 0.5}


def placed_frame(frame, size=512, ring=0.995, ring_dy=0.0):
    """The frame's alpha as bake() draws it on a token of `size`."""
    f = Image.open(frame).convert("RGBA").resize((size, size), Image.LANCZOS)
    bb = f.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox()
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    sc = (size * ring) / max(bw, bh)
    r = f.crop(bb).resize((max(1, round(bw * sc)), max(1, round(bh * sc))), Image.LANCZOS)
    out = Image.new("L", (size, size), 0)
    out.paste(r.split()[3], ((size - r.width) // 2, (size - r.height) // 2 + round(ring_dy * size)))
    return out


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
    solidify(out)            # the key leaves near-key colours half-transparent; make the ring solid
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
    placed = None                                       # the frame as drawn on this token
    if frame:
        f = Image.open(frame).convert("RGBA").resize((size, size), Image.LANCZOS)
        if frame_mode == "alpha" or (frame_mode == "auto" and _has_alpha(f)):
            # Auto-fit: scale the ring so its opaque extent fills `ring` of the token
            # (ring < 0.995 leaves room above it for a pop-out head; ring_dy moves it down).
            bbox = f.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox()
            placed = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            if bbox:
                bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
                scale = (size * ring) / max(bw, bh)
                rimg = f.crop(bbox).resize((max(1, round(bw * scale)), max(1, round(bh * scale))), Image.LANCZOS)
                placed.paste(rimg, ((size - rimg.width) // 2, (size - rimg.height) // 2 + round(ring_dy * size)), rimg)
    # The portrait is cut to the inside of the ring, the way a magic wand on the
    # ring's hole would: flood-fill the hole, grow it a few pixels so it tucks
    # under the band, and keep only that. Nothing of the portrait reaches outside
    # the ring. Without a closed ring, a circle of `ring` size stands in.
    # The portrait is cut to the inside of the ring. Rays go out from the ring's
    # centre; along each, the band is the longest unbroken stretch of frame (a
    # thin rope line or a tiny airship inside the ring is a short one), and the
    # portrait reaches 3 px under the band's inner edge. Frame bits nearer the
    # centre than the band are erased, so nothing sits on the face.
    mask = None
    if placed is not None:
        inside = _ring_inside(placed.split()[3], size // 2, size * (0.5 + ring_dy))
        if inside is not None:
            mask = inside.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(feather))
            placed.putalpha(ImageChops.multiply(placed.split()[3], ImageChops.invert(inside.filter(ImageFilter.MinFilter(5)))))
    if mask is None:
        mask = _circle_mask(size, feather, 0.96 * ring / 0.995, 0.5 + ring_dy)
    canvas.paste(p, (0, 0), mask)
    if placed is not None:
        canvas = Image.alpha_composite(canvas, placed)
    elif frame:
        rg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        rg.paste(f, (0, 0), _annulus_mask(size, inner, feather))
        canvas = Image.alpha_composite(canvas, rg)
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


def head_pop(portrait, frame, cutout, out, size=512, ring=0.9, ring_dy=0.06, head_top=0.015, zoom=None):
    """Bake with the head over the frame. A head that sits low in its art cannot
    rise far at zoom 1 without the portrait leaving the ring's bottom bare, so
    zoom in a step at a time until the head clears the band."""
    ring_top = 0.5 + ring_dy - ring / 2
    steps = [zoom] if zoom else [1.0, 1.1, 1.2, 1.3]
    for z in steps:
        res = _head_pop(portrait, frame, cutout, out, size, ring, ring_dy, head_top, z)
        if res[2] < ring_top - 0.01 or z == steps[-1]:
            return res[0], res[1] + ("" if z == 1.0 else f", zoom {z}")


def _head_pop(portrait, frame, cutout, out, size, ring, ring_dy, head_top, zoom):
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
    clipped = top < size * 0.01
    # place by the head itself: its first row wider than a seventh of the token,
    # so a horn or an ear above it does not decide where the head goes
    wide = next((y for y, n in enumerate(rows) if n * 2 > w / 7 and y >= top), top)
    ring_top = 0.5 + ring_dy - ring / 2
    # the head's first wide row goes just above the band; a horn or ear above it
    # may run off the token's top. The portrait must still reach the ring's bottom.
    dy = 0.0 if clipped else ring_top - 0.05 - wide / size
    dy = max(dy, (0.5 + ring_dy + ring / 2 - 0.07) - (0.5 + zoom / 2))      # 0.07: the band's own depth
    # the head's width: the top 12% of the figure, or deeper while that is only a
    # horn or an ear (narrower than a sixth of the token)
    depth = 0.12
    while True:
        xs = sorted({x for y in range(top, min(c.height, top + int(size * depth))) for x in range(0, w, 2) if c.getpixel((x, y))})
        if depth >= 0.3 or (xs and xs[-1] - xs[0] > size / 6):
            break
        depth += 0.03
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
    return out, ("head cut off in the art: popped in place" if clipped else f"head popped (dy {dy:+.3f})"), wide / size + dy


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

    so = sub.add_parser("solidify", help="Make a cut frame's ring solid (no half-transparent band).")
    so.add_argument("frames", nargs="+")
    so.add_argument("--floor", type=int, default=24, help="Alpha above this becomes opaque (90 for a frame with a soft drop shadow).")

    h = sub.add_parser("headpop", help="Bake tokens with the head lifted over the frame, from cut-outs.")
    h.add_argument("--portraits", required=True, help="Folder of <slug>.png portraits.")
    h.add_argument("--cutouts", required=True, help="Folder of the same portraits with the background removed (<slug>-cutout.png or <slug>.png).")
    h.add_argument("--frames", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "token-frames"))
    h.add_argument("--map", required=True, help='JSON {frame-stem: [portrait slugs]}.')
    h.add_argument("--out", required=True)
    h.add_argument("--size", type=int, default=512)

    a = ap.parse_args()
    if a.cmd == "solidify":
        for f in a.frames:
            print(solidify(f, floor=a.floor))
        return
    if a.cmd == "headpop":
        groups = json.load(open(a.map, encoding="utf-8"))
        hand = groups.pop("_by_hand", {})
        for fr, slugs in groups.items():
            frame = _resolve_frame(fr, a.frames)
            for slug in slugs:
                cut = next((os.path.join(a.cutouts, slug + e) for e in ("-cutout.png", ".png")
                            if os.path.exists(os.path.join(a.cutouts, slug + e))), None)
                if not cut:
                    print(f"{slug}: no cut-out, skipped")
                    continue
                if slug in hand:                      # finished by hand: never overwritten
                    print(f"{slug} [{fr}]: by hand, left alone ({hand[slug]})")
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
