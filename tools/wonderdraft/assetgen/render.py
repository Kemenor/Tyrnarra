"""Quick look at map patches with pack art, drawn here instead of by Wonderdraft.

Every symbol in the patch is drawn onto the Empty export (the Base terrain without symbols
and labels, made by `measure-builtins`) as close to Wonderdraft's Godot renderer as we could
get it: sorted by layer then y, sprites filtered through mipmaps built from straight (not
premultiplied) alpha, greyscale art multiplied by the ground under it. Labels are left out.

Wonderdraft draws the soft edges of shrunk sprites darker and more opaque than plain alpha
blending does; in a dense forest those edges are most of the picture. EDGE_COVER and
COLOUR_POWER are a fit, not a mechanism, made on four real exports of the densest conifer
patch (mean grey / share darker than 50, real vs here, 2026-09-27): Dotty pines 87/35% vs
86/35%, round 9 (4 px ring) 81/39% vs 83/34%, round 11 83/37% vs 84/34%, round 6 (1 px ring)
86/27% vs 82/35%. Thin-ringed art comes out a little dark; the pack's art has thick rings
since round 9. Single trees and fills match to the pixel. Good for comparing art in seconds;
`test` (the real export) has the last word.
"""
import math
import os
import sys
from functools import lru_cache

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from wdmap import WDMap  # noqa: E402

EMPTY = os.path.expanduser("~/.local/share/wdmap/assetgen-test/Assetgen Empty.webp")
# Built-in art: the local reference sprites (wdtest.builtin_refs), placed by the measured size and
# foot of each texture (builtin-sizes.json), so neighbours a test leaves built-in are drawn too.
BUILTIN_REFS = os.path.expanduser("~/.local/share/wdmap/assetgen/builtins")
SIZES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "builtin-sizes.json")
PAD = 400   # symbols this far outside a patch can still reach into it
EDGE_COVER = 0.5   # background left under a symbol: 1 - alpha ** EDGE_COVER (see above)
COLOUR_POWER = 2.0  # the symbol's colour counts alpha ** COLOUR_POWER (see above)


@lru_cache(maxsize=1)
def background():
    if not os.path.exists(EMPTY):
        raise SystemExit("no %s: run `assetgen.sh measure-builtins` once (README)" % EMPTY)
    Image.MAX_IMAGE_PIXELS = None
    return Image.open(EMPTY).convert("RGB")


@lru_cache(maxsize=None)
def _mips(path):
    """Straight-alpha 2x2 box mip chain, float RGBA 0-1, as Godot builds it for a loaded PNG."""
    a = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32) / 255
    chain = [a]
    while min(chain[-1].shape[:2]) > 2:
        b = chain[-1]
        b = b[:b.shape[0] // 2 * 2, :b.shape[1] // 2 * 2]
        chain.append((b[0::2, 0::2] + b[1::2, 0::2] + b[0::2, 1::2] + b[1::2, 1::2]) / 4)
    return chain


def _resample(path, w, h):
    chain = _mips(path)
    lod = max(0.0, math.log2(chain[0].shape[0] / h))
    i = min(int(lod), len(chain) - 1)
    j = min(i + 1, len(chain) - 1)
    t = lod - int(lod)

    def level(a):
        return np.dstack([np.asarray(Image.fromarray(a[..., c]).resize((w, h), Image.BILINEAR))
                          for c in range(4)])
    return level(chain[i]) * (1 - t) + level(chain[j]) * t


def _file(texture):
    """A symbol's art: a local path (an uninstalled round) or an installed pack texture."""
    return texture if texture.startswith("/") else WDMap.asset_file(texture)


@lru_cache(maxsize=1)
def _sizes():
    import json
    with open(SIZES) as f:
        return json.load(f)


def _builtin(texture):
    """(reference sprite path, measured size) of a built-in texture, or (None, None)."""
    import re
    fam, name = texture.rsplit("/", 1)
    slug = re.sub(r"[^a-z0-9]+", "-", (fam + "/").lower().replace("res://sprites/", "")
                  .replace("res://packs/", "")).strip("-")
    path = os.path.join(BUILTIN_REFS, slug, name + ".png")
    size = _sizes().get(texture)
    if not size:
        same = [v for k, v in _sizes().items() if k.rsplit("/", 1)[0] == fam]
        size = {k: sorted(v[k] for v in same)[len(same) // 2] for k in ("w", "h", "cx", "foot")} if same else None
    return (path, size) if size and os.path.exists(path) else (None, None)


def patch(symbols, box):
    """RGB image of map box (x0, y0, x1, y1), 1 px per map unit, like the 8192 px export."""
    x0, y0, x1, y1 = box
    X0, Y0 = x0 - PAD, y0 - PAD
    ground = np.asarray(background().crop((X0, Y0, x1 + PAD, y1 + PAD))).astype(np.float32) / 255
    dst = ground.copy()
    near = [s for s in symbols if x0 - PAD < s["position"][0] < x1 + PAD and y0 - PAD < s["position"][1] < y1 + PAD]
    near.sort(key=lambda s: (s.get("z_index", 0), s["position"][1]))
    for s in near:
        texture = s.get("texture", "")
        sc = s["scale"][0]
        if texture.startswith("res://"):
            path, size = _builtin(texture)
            if not path:
                continue
            # The reference sprite is the drawn art only: stretch it to the measured size and put
            # its middle where the measured foot and centre say.
            w, h = max(1, round(size["w"] * sc)), max(1, round(size["h"] * sc))
            art = _resample(path, w, h)
            if s.get("mirror"):
                art = art[:, ::-1]
            px = round(s["position"][0] + size["cx"] * sc - X0 - w / 2)
            py = round(s["position"][1] + (size["foot"] - size["h"] / 2) * sc - Y0 - h / 2)
        else:
            path = _file(texture)
            if not path:
                continue
            H, W = _mips(path)[0].shape[:2]
            w, h = max(1, round(W * sc)), max(1, round(H * sc))
            art = _resample(path, w, h)
            if s.get("mirror"):
                art = art[:, ::-1]
            ox, oy = s["offset"]
            px = round(s["position"][0] + ox * sc - X0 - w / 2)
            py = round(s["position"][1] + oy * sc - Y0 - h / 2)
        ya, yb, xa, xb = max(0, py), min(dst.shape[0], py + h), max(0, px), min(dst.shape[1], px + w)
        if ya >= yb or xa >= xb:
            continue
        art = art[ya - py:yb - py, xa - px:xb - px]
        rgb, a = art[..., :3], art[..., 3:4]
        if s.get("custom_color_mode") and s.get("custom_colors"):
            # Custom-colour art: R, G, B are masks for three palette colours.
            cols = np.array([c[:3] for c in s["custom_colors"][:3]], np.float32)
            rgb = np.clip(rgb @ cols, 0, 1)
        elif s.get("type") in ("tree", "mountain"):
            rgb = rgb * ground[ya:yb, xa:xb]
        region = dst[ya:yb, xa:xb]
        region[:] = region * (1 - a ** EDGE_COVER) + rgb * a ** COLOUR_POWER
    out = dst[PAD:PAD + y1 - y0, PAD:PAD + x1 - x0]
    return Image.fromarray((out * 255).clip(0, 255).astype(np.uint8))
