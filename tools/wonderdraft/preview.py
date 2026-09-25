"""Approximate preview renders of a Wonderdraft map.

Not Wonderdraft's look: the painted terrain comes from the map's own images,
user-pack symbols are drawn with their real art, built-in (res://) symbols are
simple markers by type, labels use a local stand-in for the map font. Good
enough to see where things are and to check an edit.
"""
import math
import subprocess
from functools import lru_cache

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

from wdmap import WDMap

WATER = (104, 142, 158)
MARKER = {"tree": (46, 110, 52), "mountain": (120, 96, 74), "symbol": (70, 70, 70)}
HIGHLIGHT = (230, 30, 60)


@lru_cache(maxsize=None)
def _font_file(family):
    try:
        out = subprocess.run(["fc-match", "-f", "%{file}", family], capture_output=True, text=True)
        return out.stdout.strip() or None
    except OSError:
        return None


@lru_cache(maxsize=512)
def _font(family, px):
    path = _font_file(family) or _font_file("serif")
    try:
        return ImageFont.truetype(path, max(6, px))
    except (OSError, TypeError):
        return ImageFont.load_default(size=max(6, px))


@lru_cache(maxsize=None)
def _sprite(path):
    """(image, is_greyscale) for a pack sprite, or (None, False)."""
    try:
        im = Image.open(path).convert("RGBA")
    except OSError:
        return None, False
    solid = im.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    sat = ImageStat.Stat(im.convert("RGB").convert("HSV"), mask=solid).mean[1] if solid.getbbox() else 0
    return im, sat < 8


def _tint(sp, s, grey):
    """Approximate Wonderdraft's symbol colouring on a resized sprite."""
    cc = s.get("custom_colors")
    if cc and s.get("custom_color_mode"):
        # Custom-colour sprites carry three masks in R, G, B; each gets a palette colour.
        r, g, b, a = sp.split()
        out = [Image.new("L", sp.size, 0) for _ in range(3)]
        for mask, col in zip((r, g, b), cc):
            for ch in range(3):
                layer = mask.point(lambda v, c=col[ch]: int(v * c))
                out[ch] = ImageChops.add(out[ch], layer)
        return Image.merge("RGBA", out + [a])
    if grey and s.get("sample") and s.get("type") in ("tree", "mountain"):
        # Greyscale trees/mountains are multiplied by the ground colour sampled under them.
        col = tuple(int(v * 255) for v in s["sample"][:3])
        rgb = ImageChops.multiply(sp.convert("RGB"), Image.new("RGB", sp.size, col))
        rgb.putalpha(sp.getchannel("A"))
        return rgb
    return sp


def _rgba(c, alpha=None):
    r, g, b, a = (int(max(0, min(1, v)) * 255) for v in c)
    return (r, g, b, a if alpha is None else alpha)


def render(m: WDMap, area=None, width=2048, highlight=None, grid=None,
           show=("regions", "symbols", "labels")):
    """Render `area` (x0, y0, x1, y1 in map units, default whole map) to a PIL image.

    highlight: {"symbols": [idx], "labels": [idx], "regions": [idx]} drawn in red.
    grid: spacing in map units for a labelled coordinate grid.
    """
    x0, y0, x1, y1 = area or (0, 0, m.width, m.height)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(m.width, x1), min(m.height, y1)
    k = width / (x1 - x0)
    height = max(1, round((y1 - y0) * k))
    highlight = highlight or {}

    def to_px(x, y):
        return ((x - x0) * k, (y - y0) * k)

    # Terrain: ground paint over water, cut by the landmass mask.
    ground, mask = m.image("ground"), m.image("mask")
    sx = ground.width / m.width
    box = (round(x0 * sx), round(y0 * sx), round(x1 * sx), round(y1 * sx))
    g = ground.crop(box).resize((width, height), Image.BILINEAR)
    land = mask.crop(box).resize((width, height), Image.BILINEAR).getchannel("A")
    img = Image.new("RGBA", (width, height), WATER + (255,))
    img.paste(g.convert("RGB"), (0, 0), land)

    if "regions" in show:
        ov = Image.new("RGBA", img.size)
        d = ImageDraw.Draw(ov)
        for r in m.regions:
            if len(r.points) < 3:
                continue
            pts = [to_px(x, y) for x, y in r.points]
            col = r.data.get("color") or (0.5, 0.5, 0.5, 1)
            hl = r.index in highlight.get("regions", ())
            d.polygon(pts, fill=_rgba(col, 60), outline=HIGHLIGHT + (255,) if hl else _rgba(col, 255),
                      width=5 if hl else (3 if r.kind == "domain" else 2))
        img = Image.alpha_composite(img, ov)

    if "symbols" in show:
        d = ImageDraw.Draw(img)
        order = sorted(range(len(m.symbols)),
                       key=lambda i: (m.symbols[i].get("z_index", 0), m.symbols[i]["position"][1]))
        for i in order:
            s = m.symbols[i]
            x, y = s["position"]
            if not (x0 - 300 <= x <= x1 + 300 and y0 - 300 <= y <= y1 + 300):
                continue
            scale = (s.get("scale") or (1, 1))[0]
            off = s.get("offset") or (0, 0)
            px, py = to_px(x + off[0] * scale, y + off[1] * scale)
            art, grey = (_sprite(WDMap.asset_file(s.get("texture")) or "")
                         if s.get("texture", "").startswith("user://") else (None, False))
            if art is not None:
                w = max(1, round(art.width * scale * k))
                h = max(1, round(art.height * scale * k))
                sp = _tint(art.resize((w, h), Image.BILINEAR), s, grey)
                if s.get("mirror"):
                    sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
                if s.get("rotation"):
                    sp = sp.rotate(-math.degrees(s["rotation"]), expand=True, resample=Image.BILINEAR)
                img.alpha_composite(sp, (round(px - sp.width / 2), round(py - sp.height / 2)))
            else:
                r = max(1.5, (s.get("radius") or 30) * scale * k)
                c = MARKER.get(s.get("type"), MARKER["symbol"])
                if s.get("type") == "mountain":
                    d.polygon([(px - r, py + r * 0.6), (px + r, py + r * 0.6), (px, py - r)], fill=c)
                elif s.get("type") == "tree":
                    d.ellipse((px - r * 0.7, py - r * 0.7, px + r * 0.7, py + r * 0.7), fill=c)
                else:
                    d.rectangle((px - r * 0.6, py - r * 0.6, px + r * 0.6, py + r * 0.6), fill=c)
        for i in highlight.get("symbols", ()):
            px, py = to_px(*m.symbols[i]["position"])
            d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=HIGHLIGHT, outline=(255, 255, 255), width=1)

    if "labels" in show:
        d = ImageDraw.Draw(img)
        for i, lb in sorted(enumerate(m.labels), key=lambda t: t[1].get("z_index", 0)):
            x, y = lb["position"]
            if not (x0 <= x <= x1 and y0 <= y <= y1):
                continue
            px, py = to_px(x, y)
            size = round(lb.get("size", 32) * k)
            if size < 5:
                continue
            f = _font(lb.get("font") or "serif", size)
            hl = i in highlight.get("labels", ())
            d.text((px, py), lb["text"], font=f, anchor="mm",
                   fill=HIGHLIGHT if hl else _rgba(lb.get("color") or (0, 0, 0, 1)),
                   stroke_width=max(1, round((lb.get("outline_size") or 0) * k * 2)) if lb.get("outline_size") else 0,
                   stroke_fill=_rgba(lb.get("outline_color") or (1, 1, 1, 1)))

    if grid:
        d = ImageDraw.Draw(img)
        f = _font("sans", 14)
        gx = math.ceil(x0 / grid) * grid
        while gx <= x1:
            px, _ = to_px(gx, y0)
            d.line((px, 0, px, height), fill=(255, 255, 255, 110), width=1)
            d.text((px + 3, 3), str(int(gx)), font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            gx += grid
        gy = math.ceil(y0 / grid) * grid
        while gy <= y1:
            _, py = to_px(x0, gy)
            d.line((0, py, width, py), fill=(255, 255, 255, 110), width=1)
            d.text((3, py + 3), str(int(gy)), font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
            gy += grid

    return img.convert("RGB")
