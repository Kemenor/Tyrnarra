"""Test a family's pack against Wonderdraft's built-in art, which Main uses (again).

The yardstick is Wonderdraft's own art. Main was swapped to bought packs on 2026-09-26 and back to
the built-ins on 2026-09-27 (the post-swap copy was cleared away on 2026-09-30).
A family with a built-in counterpart (the recipe's "builtin") takes over those symbols in a copy
of the Base view: same position, scale and mirroring, sized either by the recipe's scale-1 size
("place": "scale", the conifers' rounds) or to the measured art of the built-in texture that
stood there ("place": "fit"). A family without one takes over the bought art Main has for it
(the recipe's "replaces", e.g. Dotty's kapoks), fitted to that art (packswap.fit). The export of
the Base itself is the "Wonderdraft built-ins" column; the post-swap export shows the bought
packs beside it where a family had one.

`run` exports the test map with Wonderdraft (hands off ~3 min); `offline` draws our columns
here (render.py) in seconds, within a few grey levels of a real export, beside the real
exports. `lineup` puts single sprites side by side, with the built-ins recovered from a
Wonderdraft export of them on an empty map (`builtin_refs`).

Rounds: `build --round N` keeps that round's sprites in <work>/<family>/round-N/sprites/, and
`test --round N` names its export after the round; the comparison then shows the round before.
"""
import hashlib
import json
import os
import shutil
import sys
import zlib

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from wdmap import WDMap  # noqa: E402
import gdvar  # noqa: E402
import wd_export  # noqa: E402

import packswap  # noqa: E402
import sprites  # noqa: E402

WD = os.path.expanduser("~/ProtonDrive/Wonderdraft")
BASE_MAP = os.path.join(WD, "Main - Base.wonderdraft_map")
BASE_EXPORT = os.path.join(WD, "Main - Base.webp")
TEST_DIR = os.path.expanduser("~/.local/share/wdmap/assetgen-test")  # outside Proton Drive: 100 MB per map
REF_MAP = os.path.join(TEST_DIR, "Assetgen Reference.wonderdraft_map")
POST_SWAP_EXPORT = os.path.join(TEST_DIR, "Assetgen PostSwap Base.webp")   # the Base with Dotty/Moulk art
EMPTY_EXPORT = os.path.join(TEST_DIR, "Assetgen Empty.webp")
WORK = os.path.expanduser("~/.local/share/wdmap/assetgen")
BUILTIN_REFS = os.path.join(WORK, "builtins")   # local only: Wonderdraft's art stays on this machine
FONT = os.path.expanduser("~/.local/share/fonts/wonderdraft/GentiumBookBasic-GenBkBasB.ttf")


def _family(symbols, prefix):
    return [s for s in symbols if s.get("texture", "").startswith(prefix) and s.get("z_index", 0) != 5]


def _key(s):
    return "%.2f,%.2f" % (s["position"][0], s["position"][1])


def _stem(path):
    return path[:-len(".wonderdraft_map")]


def areas(symbols, prefix):
    """Where to compare: the densest 640x400 patch of the family (whole, and its middle at 3x)
    and the family's largest single symbol (at 2x)."""
    syms = _family(symbols, prefix)
    cw, ch = 640, 400
    count = {}
    for s in syms:
        x, y = s["position"]
        for dx in (0, cw // 2):
            for dy in (0, ch // 2):
                key = ((int(x) + dx) // cw, (int(y) + dy) // ch, dx, dy)
                count[key] = count.get(key, 0) + 1
    (cx, cy, dx, dy), _ = max(count.items(), key=lambda kv: kv[1])
    x0, y0 = cx * cw - dx, cy * ch - dy
    dense = (x0, y0, x0 + cw, y0 + ch)
    mid = (x0 + cw // 2 - 120, y0 + ch // 2 - 80, x0 + cw // 2 + 120, y0 + ch // 2 + 80)
    big = max(syms, key=lambda s: s["scale"][0])
    bx, by = big["position"][0], big["position"][1] + big["offset"][1] * big["scale"][0]
    largest = (round(bx - 200), round(by - 125), round(bx + 200), round(by + 125))
    return [("dense", dense, 1), ("dense-3x", mid, 3), ("largest-2x", largest, 2)]


def _target(fam):
    """The texture prefix of the symbols in Main a family takes over."""
    return fam.get("builtin") or fam["replaces"]


def swap(symbols, fam, folder=None, ground=None):
    """Swap the family's symbols in the list (its built-in counterpart, else the bought art it
    replaces) for the installed pack, or for the sprites in `folder` (a round; drawn by file
    path, so for render.py only). Returns how many."""
    builtin = fam.get("builtin")
    old = {} if builtin else {t["texture"]: t for t in packswap.pack_folder(fam["replaces"].rstrip("/"))[0]}
    files, _ = packswap.pack_folder(sprites.texture_folder(fam), folder)
    if not files:
        raise SystemExit("no sprites in %s" % (folder or sprites.pack_dir(fam)))
    n = 0
    for s in _family(symbols, _target(fam)):
        t = files[zlib.crc32(_key(s).encode()) % len(files)]
        if builtin and fam.get("place") == "fit":
            # Cover the measured drawn size of the built-in texture that stands here.
            scale, off = packswap.fit(s["scale"][0], packswap._size_for(SIZES(), s["texture"]), t,
                                      fam.get("match", "area"))
        elif builtin:
            scale, off = s["scale"][0], (0, fam["offset_y"])
        else:
            scale, off = packswap.fit(s["scale"][0], packswap.drawn(old[s["texture"]], s["offset"]), t)
        s["texture"] = t["file"] if folder else t["texture"]
        s["scale"] = type(s["scale"])(scale, scale)
        s["offset"] = type(s["offset"])(*off)
        s["radius"] = fam["radius"]
        if ground and not s.get("sample"):
            # Full-colour art was never tinted; our greyscale art must be (else it comes out white).
            s["sample"] = ground(s["position"][0], s["position"][1])
        n += 1
    return n


_sizes = {}


def SIZES():
    """builtin-sizes.json, loaded once."""
    if not _sizes:
        with open(packswap.SIZES) as f:
            _sizes.update(json.load(f))
    return _sizes


def round_dir(fam, n):
    return os.path.join(WORK, fam["name"], "round-%d" % n)


def _test_map(fam, n=None):
    return os.path.join(TEST_DIR, "Assetgen %s%s.wonderdraft_map" % (fam["name"].capitalize(), " r%d" % n if n else ""))


def _earlier(n, path_for):
    """(round, path) of the latest round before n whose path_for(round) exists, or None."""
    return next(((k, path_for(k)) for k in range(n - 1, 0, -1) if os.path.exists(path_for(k))), None)


def _digest(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def reference(log=print):
    """(export, map to export first or None) showing the Base as it is now: the Base's own export
    when it was made after the map's last change, else a test copy's, redone whenever the Base
    changes (the copy's checksum is kept beside it)."""
    if os.path.exists(BASE_EXPORT) and os.path.getmtime(BASE_EXPORT) >= os.path.getmtime(BASE_MAP):
        return BASE_EXPORT, None
    webp, stamp = _stem(REF_MAP) + ".webp", _stem(REF_MAP) + ".md5"
    digest = _digest(BASE_MAP)
    same = os.path.exists(stamp) and open(stamp).read().strip() == digest
    if same and os.path.exists(webp) and os.path.getmtime(webp) > os.path.getmtime(REF_MAP):
        return webp, None
    if not same:
        shutil.copyfile(BASE_MAP, REF_MAP)
        with open(stamp, "w") as f:
            f.write(digest + "\n")
    log("  no export of the Base as it is now: a copy of it is exported too")
    return webp, REF_MAP


def make_map(fam, n=None, log=print):
    m = WDMap.load(BASE_MAP)
    swapped = swap(m.symbols, fam, ground=m.ground_sample)
    os.makedirs(TEST_DIR, exist_ok=True)
    path = _test_map(fam, n)
    m.save(path)
    how = "in place of the built-ins" if fam.get("builtin") else "fitted to %s" % _art_name(fam)
    log("  %d symbols -> %s, %s, %s" % (swapped, fam["pack_folder"], how, os.path.basename(path)))
    return path


def compare(boxes, columns, out_dir, prefix="compare", log=print):
    """Side-by-side sheets: columns are (label, box -> RGB image of that map box)."""
    font = ImageFont.truetype(FONT, 24)
    out = []
    for name, box, z in boxes:
        w, h = (box[2] - box[0]) * z, (box[3] - box[1]) * z
        sheet = Image.new("RGB", (len(columns) * (w + 10) + 10, h + 52), (236, 229, 214))
        d = ImageDraw.Draw(sheet)
        crops = []
        for i, (label, crop) in enumerate(columns):
            x = 10 + i * (w + 10)
            im = crop(box)
            crops.append((label, im))
            d.text((x, 10), label, font=font, fill=(40, 30, 20))
            sheet.paste(im.resize((w, h), Image.LANCZOS), (x, 44))
        path = os.path.join(out_dir, "%s-%s.jpg" % (prefix, name))
        sheet.save(path, quality=90)
        out.append(path)
        log("  %s: %s at %s" % (name, os.path.basename(path), box))
        if name == "dense":
            # How dark the forest reads: the numbers to compare with the built-ins'.
            for label, im in crops:
                hist = im.convert("L").histogram()
                total = sum(hist)
                mean = sum(i * c for i, c in enumerate(hist)) / total
                log("    %-34s mean grey %.0f, dark (<50) %.0f%%" % (label, mean, 100 * sum(hist[:50]) / total))
    return out


def _art_name(fam):
    return fam["replaces"].rstrip("/").rsplit("/", 1)[1].replace("_", " ")


def _open(path):
    Image.MAX_IMAGE_PIXELS = None
    return Image.open(path).convert("RGB")


def _boxes(fam, base):
    return areas(base, _target(fam))


def _columns(fam, ref):
    """The real exports to compare with: the Base as it is (Wonderdraft's built-ins, or the
    bought art a family without a built-in counterpart replaces) and, for built-in families,
    the bought packs of the 2026-09-26 swap (post-swap export) beside it."""
    cols = [("Wonderdraft built-ins" if fam.get("builtin") else "Main now: " + _art_name(fam), ref)]
    if fam.get("builtin") and fam.get("replaces") and os.path.exists(POST_SWAP_EXPORT):
        cols.append(("bought pack: " + _art_name(fam), POST_SWAP_EXPORT))
    return cols


def run(fam, out_dir, export=True, n=None, log=print):
    """Real Wonderdraft test: test map (and the reference if stale) exported, then compared."""
    base = WDMap.load(BASE_MAP).symbols
    if not _in_main(fam, base):
        raise SystemExit("nothing of %s in Main to swap; use --offline for its lineup" % fam["name"])
    log("Test map from %s:" % os.path.basename(BASE_MAP))
    path = make_map(fam, n, log)
    ref, ref_map = reference(log)
    if export:
        wd_export.export_views([path] + ([ref_map] if ref_map else []), log=log)
    elif ref_map:
        raise SystemExit("the reference export is stale; run without --no-export")
    columns = [(label, _open(p)) for label, p in _columns(fam, ref)]
    if n:
        prev = _earlier(n, lambda k: _stem(_test_map(fam, k)) + ".webp")
        if prev:
            columns.append(("Round %d" % prev[0], _open(prev[1])))
    columns.append(("Round %d" % n if n else "Tyrnarra pack", _open(_stem(path) + ".webp")))
    return compare(_boxes(fam, base), [(label, im.crop) for label, im in columns], out_dir, log=log)


def _in_main(fam, base):
    return bool(fam.get("builtin") or fam.get("replaces")) and any(True for _ in _family(base, _target(fam)))


def offline(fam, out_dir, n=None, log=print):
    """The same comparison with our columns drawn here (render.py), and a lineup. A family with
    nothing to take over in Main (icons, biomes Main does not have yet) gets the lineup only."""
    import render
    base = WDMap.load(BASE_MAP).symbols
    sets = []
    if n:
        prev = _earlier(n, lambda k: os.path.join(round_dir(fam, k), "sprites"))
        if prev:
            sets.append(("Round %d" % prev[0], prev[1]))
        sets.append(("Round %d" % n, os.path.join(round_dir(fam, n), "sprites")))
    else:
        sets.append(("Tyrnarra pack", None))
    if not _in_main(fam, base):
        out = [lineup(_lineup_rows(fam, sets), os.path.join(out_dir, "lineup.jpg"))]
        log("  nothing of this family in Main to swap; lineup: %s" % os.path.basename(out[0]))
        if fam.get("shape") == "icon":
            out.append(icon_preview(fam, sets[-1][1], os.path.join(out_dir, "icons-in-main.jpg"), base))
            log("  icons in Main: %s" % os.path.basename(out[-1]))
        return out
    ref, stale = reference(lambda *_: None)
    columns = []
    for label, p in _columns(fam, ref):
        if p == ref and stale:
            columns.append((label + " (drawn here)", lambda box: render.patch(base, box)))
        else:
            columns.append((label, _open(p).crop))
    for label, folder in sets:
        syms = [dict(s) for s in base]
        swap(syms, fam, folder)
        columns.append((label + " (drawn here)", lambda box, s=syms: render.patch(s, box)))
    log("offline (our columns drawn by render.py, the others are real exports):")
    out = compare(_boxes(fam, base), columns, out_dir, prefix="offline", log=log)
    out.append(lineup(_lineup_rows(fam, sets), os.path.join(out_dir, "lineup.jpg")))
    log("  lineup: %s" % os.path.basename(out[-1]))
    return out


def _lineup_rows(fam, sets):
    """(label, files, custom colours?) per lineup row: built-ins, the bought art, each round."""
    cc = fam.get("draw") == "custom_colors"
    rows = []
    if fam.get("builtin"):
        refs = os.path.join(BUILTIN_REFS, packswap.slug(fam["builtin"]))
        if os.path.isdir(refs):
            rows.append(("Wonderdraft built-ins", sorted(os.path.join(refs, f) for f in os.listdir(refs)
                                                          if f.endswith(".png")), False))
    for folder in fam.get("compare", [fam["replaces"]] if fam.get("replaces") else []):
        rows.append((folder.rstrip("/").rsplit("/", 1)[1].replace("_", " "),
                     [t["file"] for t in packswap.pack_folder(folder.rstrip("/"))[0]], cc))
    rows += [(label, [t["file"] for t in packswap.pack_folder(sprites.texture_folder(fam), folder)[0]], cc)
             for label, folder in sets]
    return rows


def lineup(rows, path, sizes=(150, 40), ground=(92, 140, 70), per_row=18):
    """Each set's sprites side by side at full size and at map size, tinted like on grassland
    (custom-colour art drawn with example colours: dark ink, cream walls, red roofs)."""
    font = ImageFont.truetype(FONT, 22)
    bands = []
    for label, files, cc in rows:
        files = files[:per_row]
        for h in sizes:
            tiles = []
            for f in files:
                sp = Image.open(f).convert("RGBA")
                sp = sp.resize((max(1, round(sp.width * h / sp.height)), h), Image.LANCZOS)
                bg = Image.new("RGB", sp.size, ground)
                # Greyscale art multiplied by the ground colour, as Wonderdraft tints it.
                rgb = sprites.cc_colour(sp).convert("RGB") if cc else ImageChops.multiply(sp.convert("RGB"), bg)
                tiles.append(Image.composite(rgb, bg, sp.getchannel("A")))
            bands.append((label if h == sizes[0] else None, tiles, h))
    width = max(sum(t.width + 6 for t in tiles) for _, tiles, _ in bands) + 20
    height = sum(h + 12 + (30 if label else 0) for label, _, h in bands) + 10
    sheet = Image.new("RGB", (width, height), (236, 229, 214))
    d = ImageDraw.Draw(sheet)
    y = 8
    for label, tiles, h in bands:
        if label:
            d.text((10, y), label, font=font, fill=(40, 30, 20))
            y += 30
        band = Image.new("RGB", (width - 20, h + 6), ground)
        x = 3
        for t in tiles:
            band.paste(t, (x, 3))
            x += t.width + 6
        sheet.paste(band, (10, y))
        y += h + 12
    sheet.save(path, quality=90)
    return path


# --- the built-ins as local reference sprites ------------------------------------------------

REF_CELL = 480     # grid cell, map units (17 x 17 cells on an 8192 map)
REF_SIZE = 400     # longest side of each texture's drawn art in its cell


def builtin_refs(export=True, log=print):
    """Every built-in texture Main used, recovered from Wonderdraft's own export as a greyscale
    sprite with alpha, for lineups. Wonderdraft's art may not be extracted from its files, and
    these stay on this machine (BUILTIN_REFS). Two exports of the same grid, drawn white and
    drawn black, over the Empty export's terrain T give per pixel alpha = 1 - black / T and
    grey = (white - (1 - alpha) T) / alpha."""
    with open(packswap.SIZES) as f:
        sizes = json.load(f)
    templates = {}
    for s in WDMap.load(BASE_MAP).symbols:
        if packswap.builtin(s) and s["texture"] not in templates and s["texture"] in sizes:
            templates[s["texture"]] = s
    m = WDMap.load(BASE_MAP)
    per_row = int(m.width // REF_CELL)
    if len(templates) > per_row * per_row:
        raise SystemExit("%d textures do not fit a %dx%d grid" % (len(templates), per_row, per_row))
    cells = {}
    maps = {}
    for tone in ("white", "black"):
        grid = []
        for i, tex in enumerate(sorted(templates)):
            v = sizes[tex]
            scale = min(3.0, REF_SIZE / max(v["w"], v["h"]))
            cx, cy = REF_CELL / 2 + (i % per_row) * REF_CELL, REF_CELL / 2 + (i // per_row) * REF_CELL
            # Click point placed so the drawn art's middle lands on the cell's middle.
            px, py = cx - v["cx"] * scale, cy - (v["foot"] - v["h"] / 2) * scale
            t = dict(templates[tex])
            t["position"] = type(t["position"])(px, py)
            t["scale"] = type(t["scale"])(scale, scale)
            t["rotation"], t["mirror"], t["z_index"] = 0.0, False, 0
            t["sample"] = gdvar.Color(1, 1, 1, 1) if tone == "white" else gdvar.Color(0, 0, 0, 1)
            grid.append(t)
            cells[tex] = (cx, cy)
        m.data["labels"], m.data["symbols"] = [], grid
        maps[tone] = os.path.join(TEST_DIR, "Assetgen Builtins %s.wonderdraft_map" % tone.capitalize())
        if export:
            m.save(maps[tone])
    if export:
        log("built-in reference grid: %d textures, exported drawn white and drawn black" % len(templates))
        wd_export.export_views([maps["white"], maps["black"]], log=log)
    T = np.asarray(_open(EMPTY_EXPORT).convert("L")).astype(np.float32)
    W = np.asarray(_open(_stem(maps["white"]) + ".webp").convert("L")).astype(np.float32)
    B = np.asarray(_open(_stem(maps["black"]) + ".webp").convert("L")).astype(np.float32)
    alpha = np.clip(1 - B / np.maximum(T, 1), 0, 1)
    alpha[alpha < 0.06] = 0     # WebP noise
    grey = np.clip((W - (1 - alpha) * T) / np.maximum(alpha, 0.05), 0, 255)
    k = W.shape[1] / m.width
    count = 0
    for tex, (cx, cy) in cells.items():
        x0, y0 = int((cx - REF_CELL / 2) * k), int((cy - REF_CELL / 2) * k)
        x1, y1 = x0 + int(REF_CELL * k), y0 + int(REF_CELL * k)
        a, g = alpha[y0:y1, x0:x1], grey[y0:y1, x0:x1]
        # Trim to the art: paper grain leaves faint specks all over the cell.
        rows, cols = np.flatnonzero((a > 0.25).sum(1) > 1), np.flatnonzero((a > 0.25).sum(0) > 1)
        if len(rows) < 2:
            log("  nothing drawn for %s" % tex)
            continue
        ya, yb = max(0, rows[0] - 3), min(a.shape[0], rows[-1] + 4)
        xa, xb = max(0, cols[0] - 3), min(a.shape[1], cols[-1] + 4)
        a, g = a[ya:yb, xa:xb], g[ya:yb, xa:xb]
        out = np.dstack([g, g, g, a * 255]).clip(0, 255).astype(np.uint8)
        folder = os.path.join(BUILTIN_REFS, packswap.slug(packswap.family(tex)))
        os.makedirs(folder, exist_ok=True)
        Image.fromarray(out, "RGBA").save(os.path.join(folder, tex.rsplit("/", 1)[1] + ".png"))
        count += 1
    log("  %d reference sprites in %s" % (count, BUILTIN_REFS))
    return BUILTIN_REFS


# --- icons in Main --------------------------------------------------------------------------

MAIN_MAP = os.path.join(WD, "Main.wonderdraft_map")   # the Base view has no labels
BSG = "user://assets/BSG_elvanos_mapIcons/sprites/symbols/BSG & Elvanos - Map Icons Custom Colors Textured/"
# A city in Main is a cluster of BSG icons (a god-city: Fortress + Town + Large Stone Wall).
# A cluster becomes one of our settlement kinds by its most important member, in this order.
BSG_KINDS = [("Large City Stone Wall + Towers", "walled_city"), ("Large Stone Wall", "walled_town"),
             ("Small City Stone Wall", "walled_town"), ("Fortress", "fortress"), ("Cathedral", "temple"),
             ("Castle", "castle"), ("Keep", "castle"), ("Small City", "city"), ("Town", "town")]
ROOF = (0.62, 0.27, 0.20)     # colour 3 for the preview: Main's BSG icons leave it black
CLUSTER_GAP = 70              # map units between icons of one city


def _drawn_box(x, t):
    """Map box (x0, y0, x1, y1) a symbol's art covers, from its file's bbox."""
    sc = x["scale"][0]
    bx0, by0, bx1, by1 = t["bbox"]
    cx = x["position"][0] + x["offset"][0] * sc
    cy = x["position"][1] + x["offset"][1] * sc
    return (cx + (bx0 - t["W"] / 2) * sc, cy + (by0 - t["H"] / 2) * sc,
            cx + (bx1 - t["W"] / 2) * sc, cy + (by1 - t["H"] / 2) * sc)


def _clusters(syms, idx):
    """Groups of symbol indices whose positions chain within CLUSTER_GAP."""
    groups, left = [], list(idx)
    while left:
        group, todo = [], [left.pop()]
        while todo:
            i = todo.pop()
            group.append(i)
            xi, yi = syms[i]["position"][0], syms[i]["position"][1]
            near = [j for j in left if (syms[j]["position"][0] - xi) ** 2 + (syms[j]["position"][1] - yi) ** 2
                    < CLUSTER_GAP ** 2]
            for j in near:
                left.remove(j)
            todo += near
        groups.append(group)
    return groups


def icon_preview(fam, folder, path, base):
    """Main's city icons replaced by ours, drawn here. Each city (a cluster of BSG icons) becomes
    one of ours as wide as the whole cluster, standing on its bottom edge, in the city's own
    line and wall colours with a roof colour added: the god-cities by their labels, other
    cities by BSG_KINDS. Two crops per city: Main now | ours."""
    import render
    ours = {}
    for t in packswap.pack_folder(sprites.texture_folder(fam), folder)[0]:
        ours.setdefault(t["texture"].rsplit("/", 1)[1].rsplit("_", 1)[0], []).append(t)
    theirs = {t["texture"]: t for t in packswap.pack_folder(BSG.rstrip("/"))[0]}
    syms = [dict(x) for x in base]
    icons = [i for i, x in enumerate(syms) if x.get("texture", "") in theirs]
    clusters = _clusters(syms, icons)
    targets = []   # (label, cluster, our item)
    if fam["name"] == "god_cities":
        main = WDMap.load(MAIN_MAP)
        for lb in main.labels:
            if "Divine City" not in main.layer_name(lb.get("z_index", 0)):
                continue
            item = lb.get("text", "").strip().lower().replace(" ", "_")
            x, y = lb["position"]
            c = min(clusters, key=lambda g: min((syms[k]["position"][0] - x) ** 2 + (syms[k]["position"][1] - y) ** 2
                                                for k in g))
            if item in ours:
                targets.append((lb.get("text", "").strip(), c, item))
    else:
        for c in clusters:
            names = {syms[k]["texture"].rsplit("/", 1)[1] for k in c}
            kind = next((kind for name, kind in BSG_KINDS if name in names), None)
            if kind in ours:
                targets.append((kind, c, kind))
    crops = []
    for label, c, item in targets:
        boxes = [_drawn_box(syms[k], theirs[syms[k]["texture"]]) for k in c]
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        first = syms[c[0]]
        t = ours[item][zlib.crc32(_key(first).encode()) % len(ours[item])]
        bx0, by0, bx1, by1 = t["bbox"]
        # The cluster's area, not its width: ours are wide raised views, BSG's tall fronts.
        scale = (((x1 - x0) * (y1 - y0)) / ((bx1 - bx0) * (by1 - by0))) ** 0.5
        new = dict(first)
        new["texture"], new["scale"] = t["file"], type(first["scale"])(scale, scale)
        new["position"] = type(first["position"])((x0 + x1) / 2, y1)
        new["offset"] = type(first["offset"])(t["W"] / 2 - (bx0 + bx1) / 2, t["H"] / 2 - by1)
        cc = list(first.get("custom_colors") or [gdvar.Color(0, 0, 0, 1)] * 3)
        new["custom_colors"] = [cc[0], cc[1], gdvar.Color(ROOF[0], ROOF[1], ROOF[2], 1)]
        new["custom_color_mode"] = 1
        for k in c:
            syms[k] = dict(syms[k], texture="")      # the cluster's own icons leave
        syms[c[0]] = new
        if label not in {lab for lab, _ in crops}:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            crops.append((label, (round(mx - 120), round(my - 80), round(mx + 120), round(my + 80))))
    font = ImageFont.truetype(FONT, 20)
    cw, chh = 480, 320
    per_row = 3
    rows = (len(crops) + per_row - 1) // per_row
    sheet = Image.new("RGB", (per_row * (2 * cw + 30) + 10, rows * (chh + 40) + 10), (236, 229, 214))
    d = ImageDraw.Draw(sheet)
    for k, (label, box) in enumerate(crops):
        x0 = 10 + (k % per_row) * (2 * cw + 30)
        y0 = 10 + (k // per_row) * (chh + 40)
        d.text((x0, y0), "%s: Main now | Tyrnarra" % label, font=font, fill=(40, 30, 20))
        sheet.paste(render.patch(base, box).resize((cw, chh), Image.LANCZOS), (x0, y0 + 28))
        sheet.paste(render.patch(syms, box).resize((cw, chh), Image.LANCZOS), (x0 + cw + 6, y0 + 28))
    sheet.save(path, quality=88)
    return path
