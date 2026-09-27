"""From generated images to Wonderdraft sprites.

cut()       the subject out of one image: BiRefNet mask (or a flood fill of a clean white
            background) -> largest object, a tree's ground patch trimmed
check()     reasons to reject a cut-out (extra objects, cropped, odd proportions, ...)
finish()    greyscale with the family's levels, resized to Wonderdraft's scale-1 size, outlined;
            custom-colour families get R/G/B colour masks instead (finish_cc)
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


def flood_mask(rgb):
    """Foreground mask of a drawing on a clean white background, without a model: the
    background is every near-white region that touches the image border. Enclosed white
    (a pale crown inside its outline) stays foreground. Soft over the 2 px of the edge."""
    border = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3),
                             rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
    diff = np.abs(rgb - np.median(border, axis=0)).max(2)
    lab, _ = ndimage.label(diff < 24)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    background = np.isin(lab, edge[edge > 0])
    fg = ~background
    soft = np.clip(diff / 60, 0, 1)
    band = ndimage.binary_dilation(fg, iterations=2) & ~ndimage.binary_erosion(fg, iterations=1)
    return np.where(band, np.maximum(soft, fg * 0.5), fg.astype(np.float32)).astype(np.float32)


def cut(rgb_path, mask_path, shape="tree", ink_alpha=False):
    """(rgba array, reason) for one generated image; rgba is None when the image is unusable.
    Without a mask file the mask comes from flood_mask. Only trees get the ground trim: a
    mountain's or a building's base is part of it. `ink_alpha` (bare trees): the paper between
    the strokes turns transparent too, where the mask would fill a crown's outline."""
    rgb = np.asarray(Image.open(rgb_path).convert("RGB")).astype(np.float32)
    if mask_path and os.path.exists(mask_path):
        mask = np.asarray(Image.open(mask_path).convert("L")).astype(np.float32) / 255
    else:
        mask = flood_mask(rgb)
    solid = mask > 0.5
    lab, n = ndimage.label(solid, structure=np.ones((3, 3)))
    if n == 0:
        return None, "empty mask"
    sizes = ndimage.sum(solid, lab, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    main = lab == order[0] + 1
    if shape == "clump":
        # A bamboo clump or a group of mushrooms is several pieces: keep every sizeable one.
        main = np.isin(lab, 1 + np.flatnonzero(sizes > 0.03 * sizes[order[0]]))
    elif n > 1 and sizes[order[1]] > 0.06 * sizes[order[0]]:
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
    if narrow and shape == "tree":
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
    # Semi-transparent edge pixels are the subject's colour mixed with the background (white or
    # parchment); take the background back out, so the edge shows no light halo on the map.
    border = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3),
                             rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    if ink_alpha:
        lum = rgb @ LUMA
        alpha = alpha * np.clip((bg @ LUMA - lum) / 90, 0, 1) ** 0.7
    a = alpha[..., None]
    rgb = np.where(a > 0.02, (rgb - (1 - a) * bg) / np.maximum(a, 0.02), rgb).clip(0, 255)
    rows = np.flatnonzero(alpha.max(1) > 0.02)
    cols = np.flatnonzero(alpha.max(0) > 0.02)
    y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    rgba = np.dstack([rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1, None] * 255])
    return rgba, None


def thin_ink(rgba, radius):
    """Greyscale with the dark lines made `radius` px narrower on each side (a max filter on
    luminance): the strokes stay black, a dense forest of them reads less dark. A negative
    radius makes them that much bolder (a min filter), so thin inner lines survive the
    downscale to map size."""
    lum = rgba[..., :3] @ LUMA
    if radius > 0:
        lum = ndimage.grey_dilation(lum, footprint=_disk(radius))
    elif radius < 0:
        lum = ndimage.grey_erosion(lum, footprint=_disk(-radius))
    out = rgba.copy()
    out[..., :3] = lum[..., None]
    return out


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
    if fam.get("shape", "tree") == "tree" and widths[int(h * 0.96):].max() > fam.get("base_max", 0.55) * crown:
        return "wide base (ground or bushes left)"
    fill = a.sum() / (h * w)
    lo, hi = fam.get("fill", (0.3, 0.8))
    if not lo <= fill <= hi:
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


def trim_skirts(rgba, keep):
    """A mountain without its long low flanks: only the columns at least `keep` of the tallest
    column's height stay, and the last 8% on each side fade out. Wide skirts of neighbouring
    mountains line up into horizontal stripes across a range."""
    a = rgba[..., 3] > 128
    heights = np.where(a.any(0), a.shape[0] - a.argmax(0), 0)
    cols = np.flatnonzero(heights >= keep * heights.max())
    x0, x1 = cols[0], cols[-1] + 1
    out = rgba[:, x0:x1].copy()
    w = x1 - x0
    edge = max(1, int(0.08 * w))
    ramp = np.ones(w)
    ramp[:edge] = np.linspace(0, 1, edge)
    ramp[-edge:] = np.linspace(1, 0, edge)
    out[..., 3] *= ramp[None, :]
    rows = np.flatnonzero(out[..., 3].max(1) > 2)
    return out[rows[0]:rows[-1] + 1]


def finish(rgba, fam, lv):
    """Greyscale sprite at Wonderdraft's scale-1 size, optionally with a solid outline ring."""
    if fam.get("draw") == "custom_colors":
        return finish_cc(rgba, fam)
    if recipes.SKIRT_TRIM:
        rgba = trim_skirts(rgba, recipes.SKIRT_TRIM)
    lo, hi, gamma = lv
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA")
    th, tw = target_size(im.width, im.height, fam)
    im = im.resize((max(1, tw - 2 * recipes.OUTLINE), max(1, th - 2 * recipes.OUTLINE)), Image.LANCZOS)
    t = np.asarray(im).astype(np.float32)
    lum = t[..., :3] @ LUMA
    g = 30 + 225 * np.clip((lum - lo) / max(1.0, hi - lo), 0, 1) ** gamma
    if recipes.INNER_LIGHTEN:
        # Bolder silhouette: strokes deep inside the shape fade toward white, the edge keeps its ink,
        # so at map size a tree reads as a pale shape with a dark rim (like Wonderdraft's own art).
        depth = ndimage.distance_transform_edt(t[..., 3] > 128)
        w = np.clip((depth - recipes.INNER_EDGE) / recipes.INNER_EDGE, 0, 1) * recipes.INNER_LIGHTEN
        g = g + (255 - g) * w
    pad = recipes.OUTLINE + 2
    a = np.pad(t[..., 3] / 255, pad)
    g = np.pad(g, pad)
    fade = None
    if recipes.BASE_FADE:
        # Open base (mountains): the bottom of the shape fades out into the ground instead of
        # ending on a line, so a range does not stack into horizontal stripes.
        rows = np.flatnonzero(a.max(1) > 0.5)
        band = max(2.0, recipes.BASE_FADE * (rows[-1] - rows[0]))
        y = np.arange(a.shape[0])[:, None]
        fade = np.clip((rows[-1] - y) / band, 0, 1)
    if recipes.OUTLINE:
        # An extra solid ring around the drawn edge. On a conifer's jagged outline even 3 px
        # of it covered a quarter of the sprite and darkened dense forests.
        inner = ndimage.grey_erosion(a, footprint=_disk(recipes.DEFRINGE)) if recipes.DEFRINGE else a
        outer = ndimage.grey_dilation(a, footprint=_disk(recipes.OUTLINE))
        g = g * inner + recipes.OUTLINE_GREY * (1 - inner)
        a = outer
    if fade is not None:
        a = a * fade
    out = np.dstack([g, g, g, a * 255]).clip(0, 255).astype(np.uint8)
    sprite = Image.fromarray(out, "RGBA")
    return sprite.crop(sprite.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def finish_cc(rgba, fam):
    """Custom-colour sprite at the family's scale-1 size. Wonderdraft draws each pixel as
    R x colour 1 + G x colour 2 + B x colour 3 (the colours picked per symbol), so the channels
    are masks: R the ink lines, G the body (walls, stone, ground), B the accents (roofs,
    banners: whatever the drawing coloured). Each keeps the drawing's shading, so a wall in
    shadow takes a darker shade of its colour; a solid ink ring of OUTLINE px goes round it."""
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA")
    th, tw = target_size(im.width, im.height, fam)
    o = recipes.OUTLINE_CC
    im = im.resize((max(1, tw - 2 * o), max(1, th - 2 * o)), Image.LANCZOS)
    t = np.asarray(im).astype(np.float32) / 255
    rgb, a = t[..., :3], t[..., 3]
    lum = rgb @ LUMA
    mx, mn = rgb.max(2), rgb.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    ink = np.clip((recipes.CC_INK_LUM - lum) / 0.25, 0, 1)
    accent = np.clip((sat - recipes.CC_ACCENT_SAT) / 0.2, 0, 1) * (1 - ink)
    body = (1 - ink) * (1 - accent)
    solid = a > 0.5

    def shade(v, weight):
        # Brightest tenth of the part = its full colour; darker parts a shade of it.
        sel = solid & (weight > 0.5)
        ref = np.percentile(v[sel], 90) if sel.sum() > 50 else 1.0
        return np.clip(v / max(ref, 0.05), 0, 1)
    R, G, B = ink, body * shade(lum, body), accent * shade(mx, accent)
    pad = o + 2
    R, G, B, a = (np.pad(c, pad) for c in (R, G, B, a))
    if o:
        outer = ndimage.grey_dilation(a, footprint=_disk(o))
        R = R * a + (1 - a)
        G, B = G * a, B * a
        a = outer
    out = np.dstack([R, G, B, a]) * 255
    sprite = Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")
    return sprite.crop(sprite.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def pack_dir(fam):
    return os.path.join(os.path.expanduser("~/.local/share/Wonderdraft/assets/Tyrnarra/sprites"), fam["kind"],
                        fam["pack_folder"])


def texture_folder(fam):
    return "user://assets/Tyrnarra/sprites/%s/%s" % (fam["kind"], fam["pack_folder"])


def texture(fam, n):
    return "%s/%s" % (texture_folder(fam), fam["file"].format(n=n))


def install(sprites, fam, folder=None, names=None):
    """Replace the pack folder's (or `folder`'s) contents with `sprites`, saved under `names`
    (default the family's numbered file names); returns the folder."""
    folder = folder or pack_dir(fam)
    names = names or [fam["file"].format(n=n) for n in range(1, len(sprites) + 1)]
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder)
    for name, sp in zip(names, sprites):
        sp.save(os.path.join(folder, name + ".png"))
    meta = {"name": os.path.basename(folder).replace("_", " "), "radius": fam["radius"],
            "offset_x": 0, "offset_y": fam["offset_y"], "draw_mode": fam.get("draw", "sample_color")}
    with open(os.path.join(folder, ".wonderdraft_symbols"), "w") as f:
        json.dump(meta, f, indent=4)
    return folder


CC_EXAMPLE = ((40, 30, 25), (226, 208, 170), (170, 62, 44))   # ink, walls, roofs for previews


def cc_colour(sp, colours=CC_EXAMPLE):
    """A custom-colour sprite drawn with example colours: R x c1 + G x c2 + B x c3."""
    t = np.asarray(sp.convert("RGBA")).astype(np.float32) / 255
    rgb = np.clip(t[..., :3] @ (np.array(colours, np.float32) / 255), 0, 1) * 255
    out = Image.fromarray(np.dstack([rgb, t[..., 3] * 255]).astype(np.uint8), "RGBA")
    return out


def contact_sheet(sprites, path, tint=(120, 170, 90), row_h=180, width=1600, cc=False):
    """Sprites tinted like Wonderdraft would on grassland (custom-colour ones drawn with
    example colours), in rows."""
    tiles = []
    for sp in sprites:
        sp = sp.resize((max(1, round(sp.width * row_h / sp.height)), row_h), Image.LANCZOS)
        if cc:
            rgb = cc_colour(sp).convert("RGB")
        else:
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
