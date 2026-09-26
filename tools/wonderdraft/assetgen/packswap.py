"""Swap Wonderdraft's built-in art in a map for art from installed asset packs.

The rules live in pack-swap.json (which built-in family becomes which pack folder). Sizes are
matched from measurements, not guessed: `measure` exports a calibration map with one copy of
each built-in texture on a grid, and once without; the difference is exactly the built-in art,
which gives each texture's drawn size and foot position at scale 1 (builtin-sizes.json). `swap` then gives every replaced symbol a scale and anchor so the new
art covers the same ground and stands on the same point.

No art is stored in this public repo: the rules name pack folders, the sizes are numbers.
"""
import glob
import json
import os
import re
import sys
import zlib

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from wdmap import WDMap  # noqa: E402
import gdvar  # noqa: E402
import wd_export  # noqa: E402

HERE = os.path.dirname(os.path.realpath(__file__))
RULES = os.path.join(HERE, "pack-swap.json")
SIZES = os.path.join(HERE, "builtin-sizes.json")
ASSETS = os.path.expanduser("~/.local/share/Wonderdraft/assets")
WD = os.path.expanduser("~/ProtonDrive/Wonderdraft")
BASE_MAP = os.path.join(WD, "Main - Base.wonderdraft_map")
BASE_EXPORT = os.path.join(WD, "Main - Base.webp")
TEST_DIR = os.path.expanduser("~/.local/share/wdmap/assetgen-test")
DIFF_MIN = 40          # channel difference that counts as "built-in art was here" (WebP noise stays below)
CELL = 450             # calibration grid cell, map units (18 x 18 cells on an 8192 map)
GRID_SCALE = 0.35      # calibration scale: tall trees (~700 at 1, offset upward) stay inside a cell


def builtin(s):
    return s.get("texture", "").startswith("res://") and s.get("z_index", 0) != 5


def family(texture):
    """res://sprites/trees/_hd_oak/tree_oak_03 -> res://sprites/trees/_hd_oak/"""
    return texture.rsplit("/", 1)[0] + "/"


# --- measuring the built-in art ----------------------------------------------------------

def measure(export=True, log=print):
    """Drawn size and foot of every built-in texture at scale 1 -> builtin-sizes.json.

    A calibration map (the Base terrain, no labels) gets one copy of each built-in texture used
    in Main on a grid, at GRID_SCALE, drawn untinted (white sample). Exported once with the grid
    and once without, the difference inside each grid cell is exactly that texture's art."""
    os.makedirs(TEST_DIR, exist_ok=True)
    grid_map = os.path.join(TEST_DIR, "Assetgen Grid.wonderdraft_map")
    empty_map = os.path.join(TEST_DIR, "Assetgen Empty.wonderdraft_map")
    m = WDMap.load(BASE_MAP)
    templates = {}
    for s in m.symbols:
        if builtin(s) and s["texture"] not in templates:
            templates[s["texture"]] = s
    per_row = int(m.width // CELL)
    cells = {}
    grid = []
    for i, tex in enumerate(sorted(templates)):
        t = dict(templates[tex])
        cx, cy = CELL / 2 + (i % per_row) * CELL, CELL / 2 + (i // per_row) * CELL
        t["position"] = type(t["position"])(cx, cy)
        t["scale"] = type(t["scale"])(GRID_SCALE, GRID_SCALE)
        t["rotation"], t["mirror"], t["z_index"] = 0.0, False, 0
        t["sample"] = gdvar.Color(1, 1, 1, 1)
        grid.append(t)
        cells[tex] = (cx, cy)
    if len(grid) > per_row * per_row:
        raise SystemExit("%d textures do not fit a %dx%d grid" % (len(grid), per_row, per_row))
    if export:
        m.data["labels"] = []
        m.data["symbols"] = []
        m.save(empty_map)
        m.data["symbols"] = grid
        m.save(grid_map)
        log("calibration: %d built-in textures on a %d-unit grid at scale %.2f" % (len(grid), CELL, GRID_SCALE))
        wd_export.export_views([grid_map, empty_map], log=log)
    Image.MAX_IMAGE_PIXELS = None
    a = np.asarray(Image.open(grid_map[:-len(".wonderdraft_map")] + ".webp").convert("RGB")).astype(np.int16)
    b = np.asarray(Image.open(empty_map[:-len(".wonderdraft_map")] + ".webp").convert("RGB")).astype(np.int16)
    k = a.shape[1] / m.width
    art = np.abs(a - b).max(2) > DIFF_MIN
    del a, b
    sizes = {}
    for tex, (cx, cy) in cells.items():
        x0, y0 = int((cx - CELL / 2) * k), int((cy - CELL / 2) * k)
        win = art[y0:y0 + int(CELL * k), x0:x0 + int(CELL * k)]
        rows, cols = np.flatnonzero(win.any(1)), np.flatnonzero(win.any(0))
        if len(rows) < 2:
            log("  nothing drawn for %s" % tex)
            continue
        f = k * GRID_SCALE
        edge = rows[0] == 0 or cols[0] == 0 or rows[-1] == win.shape[0] - 1 or cols[-1] == win.shape[1] - 1
        xa, xb, ya, yb = x0 + cols[0], x0 + cols[-1] + 1, y0 + rows[0], y0 + rows[-1] + 1
        sizes[tex] = {"w": round((xb - xa) / f, 1), "h": round((yb - ya) / f, 1),
                      "cx": round(((xa + xb) / 2 - cx * k) / f, 1), "foot": round((yb - cy * k) / f, 1)}
        if edge:
            # Art at the cell edge is cut off or is a neighbour's reaching in: not a measurement.
            del sizes[tex]
            log("  %s reaches its cell edge; left out (its family's median stands in)" % tex)
    fams = {}
    for tex, v in sizes.items():
        fams.setdefault(family(tex), []).append(v)
    for fam, vs in sorted(fams.items()):
        log("  %-62s %3d textures  ~%4.0f x %4.0f" % (fam, len(vs), np.median([v["w"] for v in vs]),
                                                     np.median([v["h"] for v in vs])))
    with open(SIZES, "w") as f:
        json.dump(sizes, f, indent=1, sort_keys=True)
    return sizes


def _size_for(sizes, texture):
    """Measured size of a texture, else the median of its family."""
    if texture in sizes:
        return sizes[texture]
    fam = [v for t, v in sizes.items() if family(t) == family(texture)]
    if not fam:
        return None
    return {key: float(np.median([v[key] for v in fam])) for key in ("w", "h", "cx", "foot")}


# --- the pack art ----------------------------------------------------------------------

def pack_folder(texture_folder):
    """(files, meta) for a pack folder given as user://assets/<pack>/sprites/<kind>/<folder>."""
    rel = texture_folder[len("user://assets/"):]
    path = os.path.join(ASSETS, rel)
    meta = {}
    if os.path.exists(os.path.join(path, ".wonderdraft_symbols")):
        with open(os.path.join(path, ".wonderdraft_symbols")) as f:
            meta = json.load(f)
    files = []
    for p in sorted(glob.glob(os.path.join(path, "*.png"))):
        im = Image.open(p)
        bb = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox() if im.mode in ("RGBA", "LA") else None
        bb = bb or (0, 0, im.width, im.height)
        files.append({"texture": texture_folder.rstrip("/") + "/" + os.path.basename(p)[:-4],
                      "W": im.width, "H": im.height, "bbox": bb})
    return files, meta


# --- swapping ----------------------------------------------------------------------------

def load_rules():
    with open(RULES) as f:
        return [r for r in json.load(f)["rules"]]


def swap(m, rules, sizes, log=print):
    """Replace built-in symbols in `m` per the rules; returns {rule from: count}."""
    targets = {}
    done = {}
    for s in m.symbols:
        if not builtin(s):
            continue
        rule = next((r for r in rules if s["texture"].startswith(r["from"])), None)
        if not rule:
            continue
        src = _size_for(sizes, s["texture"])
        if src is None:
            continue
        if rule["to"] not in targets:
            targets[rule["to"]] = pack_folder(rule["to"])
        files, meta = targets[rule["to"]]
        if not files:
            raise SystemExit("no art in %s (is the pack installed?)" % rule["to"])
        x, y = s["position"]
        t = files[zlib.crc32(("%.2f,%.2f" % (x, y)).encode()) % len(files)]
        bx0, by0, bx1, by1 = t["bbox"]
        tw, th = bx1 - bx0, by1 - by0
        match = rule.get("match", "area")
        if match == "width":
            ratio = src["w"] / tw
        elif match == "height":
            ratio = src["h"] / th
        else:
            ratio = (src["w"] * src["h"] / (tw * th)) ** 0.5
        old = s["scale"][0]
        new = old * ratio * rule.get("size", 1.0)
        # Anchor: the new art's drawn foot and centre land where the old art's were.
        foot_old = src["foot"] * old
        cx_old = src["cx"] * old
        oy = (foot_old - (by1 - t["H"] / 2) * new) / new
        ox = (cx_old - ((bx0 + bx1) / 2 - t["W"] / 2) * new) / new
        s["texture"] = t["texture"]
        s["scale"] = type(s["scale"])(new, new)
        s["offset"] = type(s["offset"])(round(ox, 2), round(oy, 2))
        if "radius" in meta:
            s["radius"] = float(meta["radius"])
        if meta.get("draw_mode") == "custom_colors":
            raise SystemExit("%s is custom-colour art; give the rule colours first" % rule["to"])
        done[rule["from"]] = done.get(rule["from"], 0) + 1
    return done


def make_swapped(log=print):
    with open(SIZES) as f:
        sizes = json.load(f)
    m = WDMap.load(BASE_MAP)
    left_before = {family(s["texture"]) for s in m.symbols if builtin(s)}
    done = swap(m, load_rules(), sizes, log)
    for k, v in sorted(done.items(), key=lambda kv: -kv[1]):
        log("  %5d  %s" % (v, k))
    left = sorted({family(s["texture"]) for s in m.symbols if builtin(s)})
    log("  %d of %d built-in families swapped; still built-in: %s"
        % (len(left_before) - len(left), len(left_before), ", ".join(left) or "none"))
    path = os.path.join(TEST_DIR, "Assetgen PackSwap.wonderdraft_map")
    m.save(path)
    log("  -> %s, packs: %s" % (os.path.basename(path), ", ".join(m.data["included_packs"])))
    return path



def apply(path, log=print):
    """Swap the built-ins in a real map, in place: wdmap's backup, and its refusal when
    Wonderdraft has the map open or the file changed since loading."""
    with open(SIZES) as f:
        sizes = json.load(f)
    m = WDMap.load(path)
    done = swap(m, load_rules(), sizes, log)
    left = sorted({family(s["texture"]) for s in m.symbols if builtin(s)})
    backup = m.save_in_place()
    log("%s: %d symbols swapped in %d families; still built-in: %s; packs: %s; backup %s"
        % (os.path.basename(path), sum(done.values()), len(done), ", ".join(left) or "none",
           ", ".join(m.data["included_packs"]), backup))
    return backup

def slug(prefix):
    return re.sub(r"[^a-z0-9]+", "-", prefix.lower().replace("res://sprites/", "").replace("res://packs/", "")).strip("-")


# --- comparing ---------------------------------------------------------------------------

COMPARE = [  # (name, built-in prefix whose densest patch is shown, zoom)
    ("conifers", "res://sprites/trees/_hd_christmas/", 2),
    ("oaks", "res://sprites/trees/_hd_oak/", 2),
    ("hazel", "res://sprites/trees/_hd_hazel/", 2),
    ("willows", "res://sprites/trees/_hd_willow/", 2),
    ("jagged-peaks", "res://sprites/mountains/playful_jagged_peaks/", 2),
    ("rounded-mountains", "res://sprites/mountains/playful_rounded_mountains/", 2),
    ("hills", "res://sprites/mountains/playful_hiils/", 2),
    ("dunes", "res://packs/Arabia by Chan/sprites/mountains/sand_dunes_", 2),
    ("tang", "res://packs/Tang Dynasty by Chan/sprites/mountains/", 2),
]


def compare(out_dir, log=print):
    """Side-by-side crops of the current Base export and the swapped one."""
    from PIL import ImageDraw, ImageFont
    import wdtest
    Image.MAX_IMAGE_PIXELS = None
    m = WDMap.load(BASE_MAP)
    swapped = os.path.join(TEST_DIR, "Assetgen PackSwap.webp")
    imgs = [("Wonderdraft built-ins", Image.open(BASE_EXPORT).convert("RGB")),
            ("Dotty + Moulk packs", Image.open(swapped).convert("RGB"))]
    font = ImageFont.truetype(wdtest.FONT, 24)
    os.makedirs(out_dir, exist_ok=True)
    out = []

    def sheet(name, box, z):
        w, h = round((box[2] - box[0]) * z), round((box[3] - box[1]) * z)
        im = Image.new("RGB", (2 * w + 30, h + 52), (236, 229, 214))
        d = ImageDraw.Draw(im)
        for i, (label, src) in enumerate(imgs):
            d.text((10 + i * (w + 10), 10), label, font=font, fill=(40, 30, 20))
            im.paste(src.crop(box).resize((w, h), Image.LANCZOS), (10 + i * (w + 10), 44))
        path = os.path.join(out_dir, "swap-%s.jpg" % name)
        im.save(path, quality=88)
        out.append(path)
        log("  %s: %s" % (name, os.path.basename(path)))

    sheet("whole-map", (0, 0, m.width, m.height), 1400 / m.width)
    for name, prefix, z in COMPARE:
        if any(s.get("texture", "").startswith(prefix) for s in m.symbols):
            sheet(name, wdtest.areas(m, prefix)[0][1], z / 1.6)
    return out
