"""Test a family's pack against the art Main uses now.

Since the 2026-09-26 pack swap Main has no Wonderdraft built-in art: each family replaces a
bought pack folder (the recipe's "replaces", e.g. Dotty's pines). The test map is the Base view
with every symbol of that folder swapped for the family's pack: same position, mirroring and
sampled ground colour, each new sprite sized to cover the same area and standing on the same
foot (packswap.fit). Wonderdraft exports it, and it is compared with an export of the Base as it
is now. `offline` draws the same patches here instead (render.py): seconds instead of minutes,
no hands off the keyboard, within a few grey levels of the real export.

Rounds: `build --round N` keeps that round's sprites in <work>/<family>/round-N/sprites/, and
`test --round N` names its export after the round; the comparison then shows the round before.
"""
import hashlib
import os
import shutil
import sys
import zlib

from PIL import Image, ImageChops, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from wdmap import WDMap  # noqa: E402
import wd_export  # noqa: E402

import packswap  # noqa: E402
import sprites  # noqa: E402

WD = os.path.expanduser("~/ProtonDrive/Wonderdraft")
BASE_MAP = os.path.join(WD, "Main - Base.wonderdraft_map")
BASE_EXPORT = os.path.join(WD, "Main - Base.webp")
TEST_DIR = os.path.expanduser("~/.local/share/wdmap/assetgen-test")  # outside Proton Drive: 100 MB per map
REF_MAP = os.path.join(TEST_DIR, "Assetgen Reference.wonderdraft_map")
WORK = os.path.expanduser("~/.local/share/wdmap/assetgen")
FONT = os.path.expanduser("~/.local/share/fonts/wonderdraft/GentiumBookBasic-GenBkBasB.ttf")


def _family(symbols, prefix):
    return [s for s in symbols if s.get("texture", "").startswith(prefix) and s.get("z_index", 0) != 5]


def _stem(path):
    return path[:-len(".wonderdraft_map")]


def areas(m, prefix):
    """Where to compare: the densest 640x400 patch of the family (whole, and its middle at 3x)
    and the family's largest single symbol (at 2x)."""
    syms = _family(m.symbols, prefix)
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


def swap(symbols, fam, folder=None):
    """Swap the family's symbols in the list for the installed pack, or for the sprites in `folder`
    (a round; drawn by file path, so for render.py only). Returns how many."""
    old = {t["texture"]: t for t in packswap.pack_folder(fam["replaces"].rstrip("/"))[0]}
    files, _ = packswap.pack_folder(sprites.texture(fam, 1).rsplit("/", 1)[0], folder)
    if not files:
        raise SystemExit("no sprites in %s" % (folder or sprites.pack_dir(fam)))
    n = 0
    for s in _family(symbols, fam["replaces"]):
        x, y = s["position"]
        t = files[zlib.crc32(("%.2f,%.2f" % (x, y)).encode()) % len(files)]
        scale, off = packswap.fit(s["scale"][0], packswap.drawn(old[s["texture"]], s["offset"]), t)
        s["texture"] = t["file"] if folder else t["texture"]
        s["scale"] = type(s["scale"])(scale, scale)
        s["offset"] = type(s["offset"])(*off)
        s["radius"] = fam["radius"]
        n += 1
    return n


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
    swapped = swap(m.symbols, fam)
    os.makedirs(TEST_DIR, exist_ok=True)
    path = _test_map(fam, n)
    m.save(path)
    log("  %d symbols of %s -> %s, %s" % (swapped, _art_name(fam), fam["pack_folder"], os.path.basename(path)))
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
            # How dark the forest reads: the number to match against the art Main uses now.
            for label, im in crops:
                hist = im.convert("L").histogram()
                total = sum(hist)
                mean = sum(i * c for i, c in enumerate(hist)) / total
                log("    %-26s mean grey %.0f, dark (<50) %.0f%%" % (label, mean, 100 * sum(hist[:50]) / total))
    return out


def _art_name(fam):
    return fam["replaces"].rstrip("/").rsplit("/", 1)[1].replace("_", " ")


def run(fam, out_dir, export=True, n=None, log=print):
    """Real Wonderdraft test: test map (and the reference if stale) exported, then compared."""
    Image.MAX_IMAGE_PIXELS = None
    log("Test map from %s:" % os.path.basename(BASE_MAP))
    path = make_map(fam, n, log)
    ref, ref_map = reference(log)
    if export:
        wd_export.export_views([path] + ([ref_map] if ref_map else []), log=log)
    elif ref_map:
        raise SystemExit("the reference export is stale; run without --no-export")
    boxes = areas(WDMap.load(BASE_MAP), fam["replaces"])
    columns = [("Main now: " + _art_name(fam), Image.open(ref).convert("RGB"))]
    if n:
        prev = _earlier(n, lambda k: _stem(_test_map(fam, k)) + ".webp")
        if prev:
            columns.append(("Round %d" % prev[0], Image.open(prev[1]).convert("RGB")))
    columns.append(("Round %d" % n if n else "Tyrnarra pack", Image.open(_stem(path) + ".webp").convert("RGB")))
    return compare(boxes, [(label, im.crop) for label, im in columns], out_dir, log=log)


def offline(fam, out_dir, n=None, log=print):
    """The same comparison drawn by render.py: Main now, the round before n and round n (or the
    installed pack)."""
    import render
    m = WDMap.load(BASE_MAP)
    boxes = areas(m, fam["replaces"])
    columns = [("Main now: " + _art_name(fam), list(m.symbols))]
    sets = []
    if n:
        prev = _earlier(n, lambda k: os.path.join(round_dir(fam, k), "sprites"))
        if prev:
            sets.append(("Round %d" % prev[0], prev[1]))
        sets.append(("Round %d" % n, os.path.join(round_dir(fam, n), "sprites")))
    else:
        sets.append(("Tyrnarra pack", None))
    for label, folder in sets:
        syms = [dict(s) for s in m.symbols]
        swap(syms, fam, folder)
        columns.append((label, syms))
    log("offline render (render.py: close to Wonderdraft's; the real export has the last word):")
    out = compare(boxes, [(label, lambda box, s=syms: render.patch(s, box)) for label, syms in columns],
                  out_dir, prefix="offline", log=log)
    rows = [(columns[0][0], [t["file"] for t in packswap.pack_folder(fam["replaces"].rstrip("/"))[0]])]
    rows += [(label, [t["file"] for t in packswap.pack_folder(sprites.texture(fam, 1).rsplit("/", 1)[0], folder)[0]])
             for label, folder in sets]
    out.append(lineup(rows, os.path.join(out_dir, "lineup.jpg")))
    log("  lineup: %s" % os.path.basename(out[-1]))
    return out


def lineup(rows, path, sizes=(150, 40), ground=(92, 140, 70), per_row=16):
    """Each set's sprites side by side at full size and at map size, tinted like on grassland."""
    font = ImageFont.truetype(FONT, 22)
    bands = []
    for label, files in rows:
        files = files[:per_row]
        for h in sizes:
            tiles = []
            for f in files:
                sp = Image.open(f).convert("RGBA")
                sp = sp.resize((max(1, round(sp.width * h / sp.height)), h), Image.LANCZOS)
                # Greyscale art multiplied by the ground colour, as Wonderdraft tints it.
                bg = Image.new("RGB", sp.size, ground)
                tiles.append(Image.composite(ImageChops.multiply(sp.convert("RGB"), bg), bg, sp.getchannel("A")))
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
