"""Test a family's pack in the real Wonderdraft.

Copies the Base view with every symbol of the built-in family swapped for the pack (same
positions, scales, mirroring and sampled ground colour), exports the copies with wd_export,
and crops the same places from the current Base export for a side-by-side.
"""
import os
import sys
import zlib

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from wdmap import WDMap  # noqa: E402
import wd_export  # noqa: E402

import sprites  # noqa: E402

WD = os.path.expanduser("~/ProtonDrive/Wonderdraft")
BASE_MAP = os.path.join(WD, "Main - Base.wonderdraft_map")
BASE_EXPORT = os.path.join(WD, "Main - Base.webp")
TEST_DIR = os.path.expanduser("~/.local/share/wdmap/assetgen-test")  # outside Proton Drive: 100 MB per map
FONT = os.path.expanduser("~/.local/share/fonts/wonderdraft/GentiumBookBasic-GenBkBasB.ttf")


def _family(m, prefix):
    return [s for s in m.symbols if s.get("texture", "").startswith(prefix) and s.get("z_index", 0) != 5]


def areas(m, prefix):
    """Where to compare: the densest 640x400 patch of the family (whole, and its middle at 3x)
    and the family's largest single symbol (at 2x)."""
    syms = _family(m, prefix)
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


def make_map(fam, log=print):
    folder = sprites.pack_dir(fam)
    n = len([f for f in os.listdir(folder) if f.endswith(".png")])
    m = WDMap.load(BASE_MAP)
    swapped = 0
    for s in _family(m, fam["replaces"]):
        x, y = s["position"]
        k = zlib.crc32(("%.2f,%.2f" % (x, y)).encode()) % n + 1
        s["texture"] = sprites.texture(fam, k)
        s["radius"], s["offset"] = fam["radius"], type(s["offset"])(0, fam["offset_y"])
        swapped += 1
    os.makedirs(TEST_DIR, exist_ok=True)
    path = os.path.join(TEST_DIR, "Assetgen %s.wonderdraft_map" % fam["name"].capitalize())
    m.save(path)
    log("  %d symbols -> %d variants, %s" % (swapped, n, os.path.basename(path)))
    return path


def compare(fam, out_dir, log=print):
    Image.MAX_IMAGE_PIXELS = None
    m = WDMap.load(BASE_MAP)
    boxes = areas(m, fam["replaces"])
    del m
    srcs = [("Wonderdraft (current)", BASE_EXPORT),
            ("Tyrnarra pack", os.path.join(TEST_DIR, "Assetgen %s.webp" % fam["name"].capitalize()))]
    imgs = [(label, Image.open(p).convert("RGB")) for label, p in srcs if os.path.exists(p)]
    font = ImageFont.truetype(FONT, 24)
    out = []
    for name, box, z in boxes:
        w, h = (box[2] - box[0]) * z, (box[3] - box[1]) * z
        sheet = Image.new("RGB", (len(imgs) * (w + 10) + 10, h + 52), (236, 229, 214))
        d = ImageDraw.Draw(sheet)
        for i, (label, im) in enumerate(imgs):
            x = 10 + i * (w + 10)
            d.text((x, 10), label, font=font, fill=(40, 30, 20))
            sheet.paste(im.crop(box).resize((w, h), Image.LANCZOS), (x, 44))
        path = os.path.join(out_dir, "compare-%s.jpg" % name)
        sheet.save(path, quality=90)
        out.append(path)
        log("  %s: %s at %s" % (name, os.path.basename(path), box))
        if name == "dense":
            # How dark the forest reads: the number to match against Wonderdraft's own.
            for label, im in imgs:
                grey = im.crop(box).convert("L")
                hist = grey.histogram()
                n = sum(hist)
                mean = sum(i * c for i, c in enumerate(hist)) / n
                log("    %-22s mean grey %.0f, dark (<50) %.0f%%" % (label, mean, 100 * sum(hist[:50]) / n))
    return out


def run(fam, out_dir, export=True, log=print):
    log("Test map from %s:" % os.path.basename(BASE_MAP))
    path = make_map(fam, log)
    if export:
        wd_export.export_views([path], log=log)
    return compare(fam, out_dir, log)
