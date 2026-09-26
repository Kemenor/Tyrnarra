"""From generated images to Wonderdraft sprites.

cut()       the subject out of one image: BiRefNet mask -> largest object, ground patch trimmed
check()     reasons to reject a cut-out (extra objects, cropped, odd proportions, ...)
finish()    greyscale with the family's levels, resized to Wonderdraft's scale-1 size, outlined
install()   write a pack folder with the .wonderdraft_symbols file Wonderdraft reads
"""
import json
import os
import shutil

import numpy as np
from PIL import Image, ImageChops
from scipy import ndimage

import recipes

LUMA = np.array([0.2126, 0.7152, 0.0722])


def _disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def cut(rgb_path, mask_path):
    """(rgba array, reason) for one generated image; rgba is None when the image is unusable."""
    rgb = np.asarray(Image.open(rgb_path).convert("RGB")).astype(np.float32)
    mask = np.asarray(Image.open(mask_path).convert("L")).astype(np.float32) / 255
    solid = mask > 0.5
    lab, n = ndimage.label(solid, structure=np.ones((3, 3)))
    if n == 0:
        return None, "empty mask"
    sizes = ndimage.sum(solid, lab, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    main = lab == order[0] + 1
    if n > 1 and sizes[order[1]] > 0.06 * sizes[order[0]]:
        return None, "extra objects"
    H, W = main.shape
    rows = np.flatnonzero(main.any(1))
    cols = np.flatnonzero(main.any(0))
    if rows[0] <= 1 or cols[0] <= 1 or rows[-1] >= H - 2 or cols[-1] >= W - 2:
        return None, "touches the edge"
    # Ground patch: below the crown the width narrows to the trunk, then widens again where
    # grass, rocks or a shadow start; cut there. The ground is often wider than the crown, so
    # the crown width comes from the upper part only, and the trunk is the first run of narrow
    # rows below the middle of the subject.
    widths = main.sum(1)
    top, bottom = rows[0], rows[-1]
    span = bottom - top + 1
    crown_w = widths[top: top + int(span * 0.7)].max()
    narrow = [y for y in range(top + int(span * 0.4), bottom + 1) if 0 < widths[y] < 0.25 * crown_w]
    ground = None
    if narrow:
        trunk_top = narrow[0]
        run = [y for y in narrow if y - trunk_top < max(4, span * 0.05)]
        trunk_w = max(1.0, float(np.median(widths[run])))
        ground = next((y for y in range(trunk_top, bottom + 1)
                       if widths[y] > max(2.2 * trunk_w, trunk_w + 0.08 * crown_w)), None)
        if ground is not None:
            main[ground:] = False
            # Grass tufts beside the trunk were joined to the tree only through the ground.
            lab, n = ndimage.label(main, structure=np.ones((3, 3)))
            if n > 1:
                main = lab == 1 + int(np.argmax(ndimage.sum(main, lab, range(1, n + 1))))
    keep = ndimage.binary_dilation(main, iterations=3)
    if ground is not None:
        keep[ground:] = False
    alpha = mask * keep
    rows = np.flatnonzero(alpha.max(1) > 0.02)
    cols = np.flatnonzero(alpha.max(0) > 0.02)
    y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    rgba = np.dstack([rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1, None] * 255])
    return rgba, None


def check(rgba, fam):
    """Reason to reject a cut-out, or None."""
    a = rgba[..., 3] > 128
    h, w = a.shape
    lo, hi = fam["aspect"]
    if not lo <= h / w <= hi:
        return "proportions %.2f" % (h / w)
    th, _ = target_size(w, h, fam)
    if h < 0.8 * th:
        return "too small (%d px, would be enlarged)" % h
    widths = a.sum(1)
    crown = widths[: int(h * 0.85)].max()
    # The very base only: low branches and a root flare are part of the tree, a ground patch
    # the trim missed is about as wide as the crown.
    if widths[int(h * 0.96):].max() > 0.55 * crown:
        return "wide base (ground or bushes left)"
    fill = a.sum() / (h * w)
    if not 0.3 <= fill <= 0.8:
        return "fill %.2f" % fill
    return None


def target_size(w, h, fam):
    """(height, width) at Wonderdraft scale 1: the family's area, the cut-out's proportions."""
    fw, fh = fam["size"]
    th = (fw * fh * h / w) ** 0.5
    return round(th), round(th * w / h)


def levels(cutouts):
    """(lo, hi, gamma) mapping the family's luminance so the average grey lands on TARGET_MEAN."""
    lum = np.concatenate([(c[..., :3] @ LUMA)[c[..., 3] > 200] for c in cutouts])
    lo, hi = np.percentile(lum, 2), np.percentile(lum, 98)
    s = np.clip((lum - lo) / max(1.0, hi - lo), 0, 1)
    gamma = 1.0
    for _ in range(40):
        mean = 30 + 225 * (s ** gamma).mean()
        gamma *= (mean / recipes.TARGET_MEAN) ** 1.5
    return float(lo), float(hi), float(gamma)


def finish(rgba, fam, lv):
    """Greyscale sprite at Wonderdraft's scale-1 height, soft edge hidden under a solid outline."""
    lo, hi, gamma = lv
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA")
    th, tw = target_size(im.width, im.height, fam)
    im = im.resize((max(1, tw - 2 * recipes.OUTLINE), max(1, th - 2 * recipes.OUTLINE)), Image.LANCZOS)
    t = np.asarray(im).astype(np.float32)
    lum = t[..., :3] @ LUMA
    g = 30 + 225 * np.clip((lum - lo) / max(1.0, hi - lo), 0, 1) ** gamma
    pad = recipes.OUTLINE + 2
    a = np.pad(t[..., 3] / 255, pad)
    g = np.pad(g, pad)
    # The cut-out's outermost pixels still carry the white background; eat them and let the
    # outline cover the seam instead of showing a light halo.
    inner = ndimage.grey_erosion(a, footprint=_disk(recipes.DEFRINGE))
    outer = ndimage.grey_dilation(a, footprint=_disk(recipes.OUTLINE))
    grey = g * inner + recipes.OUTLINE_GREY * (1 - inner)
    out = np.dstack([grey, grey, grey, outer * 255]).clip(0, 255).astype(np.uint8)
    sprite = Image.fromarray(out, "RGBA")
    return sprite.crop(sprite.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def pack_dir(fam):
    return os.path.join(os.path.expanduser("~/.local/share/Wonderdraft/assets/Tyrnarra/sprites"), fam["kind"],
                        fam["pack_folder"])


def texture(fam, n):
    return "user://assets/Tyrnarra/sprites/%s/%s/%s" % (fam["kind"], fam["pack_folder"], fam["file"].format(n=n))


def install(sprites, fam):
    """Replace the pack folder's contents with `sprites`; returns the folder."""
    folder = pack_dir(fam)
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)
    for n, sp in enumerate(sprites, 1):
        sp.save(os.path.join(folder, fam["file"].format(n=n) + ".png"))
    meta = {"name": os.path.basename(folder).replace("_", " "), "radius": fam["radius"],
            "offset_x": 0, "offset_y": fam["offset_y"], "draw_mode": "sample_color"}
    with open(os.path.join(folder, ".wonderdraft_symbols"), "w") as f:
        json.dump(meta, f, indent=4)
    return folder


def contact_sheet(sprites, path, tint=(120, 170, 90), row_h=180, width=1600):
    """Sprites tinted like Wonderdraft would on grassland, in rows."""
    tiles = []
    for sp in sprites:
        sp = sp.resize((max(1, round(sp.width * row_h / sp.height)), row_h), Image.LANCZOS)
        rgb = ImageChops.multiply(sp.convert("RGB"), Image.new("RGB", sp.size, tint))
        tile = Image.new("RGB", sp.size, tint)
        tile.paste(rgb, (0, 0), sp.getchannel("A"))
        tiles.append(tile)
    rows, x, cur = [], 8, []
    for t in tiles:
        if x + t.width > width - 8 and cur:
            rows.append(cur)
            cur, x = [], 8
        cur.append(t)
        x += t.width + 6
    if cur:
        rows.append(cur)
    sheet = Image.new("RGB", (width, len(rows) * (row_h + 8) + 8), (236, 229, 214))
    for r, row in enumerate(rows):
        x = 8
        for t in row:
            sheet.paste(t, (x, 8 + r * (row_h + 8)))
            x += t.width + 6
    sheet.save(path, quality=88)
    return path
