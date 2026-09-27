"""A copy of Main's Base view with its art swapped for the Tyrnarra pack, to judge the pack on
the real map (assetgen.sh fullswap). Main itself is never touched.

Trees and mountains: each of Main's built-in families maps to one of our folders (BUILTIN_TO),
sized to that built-in texture's measured art (builtin-sizes.json) at its scale. Bought art Main
uses for what Wonderdraft lacks (Dotty's kapoks, Nibroc's bamboo: PACK_TO) is fitted to that art.
City icons: every cluster of BSG icons becomes one of ours, as in wdtest.icon_preview: the
god-cities by their labels, the rest by kind, in each city's own line and wall colours.
"""
import os
import sys
import zlib

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from wdmap import WDMap  # noqa: E402
import gdvar  # noqa: E402
import wd_export  # noqa: E402

import packswap  # noqa: E402
import wdtest  # noqa: E402

PACK = "user://assets/Tyrnarra/sprites/"
# Built-in family (prefix) -> our folder, and which measured dimension the new art copies.
BUILTIN_TO = [
    ("res://sprites/trees/_hd_christmas/", "trees/Tyrnarra_Conifers", "area"),
    ("res://sprites/trees/inked_pine/", "trees/Tyrnarra_Conifers", "area"),
    ("res://sprites/trees/hatch_pine/", "trees/Tyrnarra_Conifers", "area"),
    ("res://sprites/trees/_hd_larix/", "trees/Tyrnarra_Conifers", "area"),
    ("res://sprites/trees/_hd_cedar/", "trees/Tyrnarra_Pines", "area"),
    ("res://sprites/trees/_hd_pine/", "trees/Tyrnarra_Pines", "area"),
    ("res://sprites/trees/_hd_oak/", "trees/Tyrnarra_Broadleaves", "area"),
    ("res://sprites/trees/_hd_hazel/", "trees/Tyrnarra_Broadleaves", "area"),
    ("res://sprites/trees/leafy_tree/", "trees/Tyrnarra_Broadleaves", "area"),
    ("res://sprites/trees/_hd_willow/", "trees/Tyrnarra_Willows", "area"),
    ("res://sprites/trees/toon_palm/", "trees/Tyrnarra_Palms", "area"),
    ("res://sprites/mountains/playful_jagged_peaks/", "mountains/Tyrnarra_Peaks", "width"),
    ("res://sprites/mountains/inked_mountains_large/", "mountains/Tyrnarra_Peaks", "width"),
    ("res://sprites/mountains/penciled_mountains_large/", "mountains/Tyrnarra_Peaks", "width"),
    ("res://sprites/mountains/penned_mountains_large/", "mountains/Tyrnarra_Peaks", "width"),
    ("res://packs/Tang Dynasty by Chan/sprites/mountains/mountains/", "mountains/Tyrnarra_Peaks", "height"),
    ("res://sprites/mountains/playful_rounded_mountains/", "mountains/Tyrnarra_Fells", "width"),
    ("res://sprites/mountains/penciled_mountains_small/", "mountains/Tyrnarra_Fells", "width"),
    ("res://sprites/mountains/penned_mountains_small/", "mountains/Tyrnarra_Fells", "width"),
    ("res://sprites/mountains/playful_hiils/", "mountains/Tyrnarra_Hills", "width"),
    ("res://sprites/mountains/penned_hills/", "mountains/Tyrnarra_Hills", "width"),
    ("res://packs/Tang Dynasty by Chan/sprites/mountains/hills/", "mountains/Tyrnarra_Hills", "width"),
    ("res://packs/Arabia by Chan/sprites/mountains/sand_dunes_", "mountains/Tyrnarra_Dunes", "width"),
]
# Bought art Main had before the swap -> our folder, fitted to that art.
PACK_TO = [
    ("user://assets/Dotty_Assets/sprites/trees/Dotty_Kapoks/", "trees/Tyrnarra_Jungle", "area"),
    ("user://assets/Nibroc's Bamboo Forest/sprites/trees/Bamboo Trees/", "trees/Tyrnarra_Bamboo", "area"),
]
OUT_MAP = os.path.join(wdtest.TEST_DIR, "Assetgen Tyrnarra Pack.wonderdraft_map")


def _folders():
    """{our folder: (files, meta)}, read once."""
    names = {rule[1] for rule in BUILTIN_TO + PACK_TO}
    return {name: packswap.pack_folder(PACK + name) for name in names}


def swap_art(syms, ours, log=print):
    """Trees and mountains in place; returns {our folder: count}."""
    sizes = wdtest.SIZES()
    bought = {}
    done = {}
    for s in syms:
        key = wdtest._key(s)
        b = s if packswap.builtin(s) else None
        rule = next((r for r in BUILTIN_TO if b and b["texture"].startswith(r[0])), None)
        if rule:
            src, scale0 = packswap._size_for(sizes, b["texture"]), b["scale"][0]
        else:
            rule = next((r for r in PACK_TO if s.get("texture", "").startswith(r[0])), None)
            if not rule:
                continue
            if rule[0] not in bought:
                bought[rule[0]] = {t["texture"]: t for t in packswap.pack_folder(rule[0].rstrip("/"))[0]}
            old = bought[rule[0]].get(s["texture"])
            if not old or not src_ok(old):
                continue
            src, scale0 = packswap.drawn(old, s["offset"]), s["scale"][0]
        files, meta = ours[rule[1]]
        t = files[zlib.crc32(key.encode()) % len(files)]
        scale, off = packswap.fit(scale0, src, t, rule[2])
        s["texture"] = t["texture"]
        s["scale"] = type(s["scale"])(scale, scale)
        s["offset"] = type(s["offset"])(*off)
        if "radius" in meta:
            s["radius"] = float(meta["radius"])
        done[rule[1]] = done.get(rule[1], 0) + 1
    return done


def src_ok(t):
    bx0, by0, bx1, by1 = t["bbox"]
    return bx1 > bx0 and by1 > by0


def swap_icons(syms, log=print):
    """Every BSG city cluster becomes one of our icons; returns the new symbol list and counts."""
    theirs = {t["texture"]: t for t in packswap.pack_folder(wdtest.BSG.rstrip("/"))[0]}
    groups = {}
    for folder in ("symbols/Tyrnarra_Settlements", "symbols/Tyrnarra_God_Cities"):
        files, meta = packswap.pack_folder(PACK + folder)
        for t in files:
            groups.setdefault(t["texture"].rsplit("/", 1)[1].rsplit("_", 1)[0], []).append((t, meta))
    icons = [i for i, x in enumerate(syms) if x.get("texture", "") in theirs]
    clusters = wdtest._clusters(syms, icons)
    god = {}
    main = WDMap.load(wdtest.MAIN_MAP)
    for lb in main.labels:
        if "Divine City" not in main.layer_name(lb.get("z_index", 0)):
            continue
        item = lb.get("text", "").strip().lower().replace(" ", "_")
        x, y = lb["position"]
        c = min(range(len(clusters)), key=lambda g: min((syms[k]["position"][0] - x) ** 2 +
                                                       (syms[k]["position"][1] - y) ** 2 for k in clusters[g]))
        god[c] = item
    drop, counts = set(), {}
    for g, c in enumerate(clusters):
        names = {syms[k]["texture"].rsplit("/", 1)[1] for k in c}
        item = god.get(g) or next((kind for name, kind in wdtest.BSG_KINDS if name in names), None)
        if item not in groups:
            continue
        boxes = [wdtest._drawn_box(syms[k], theirs[syms[k]["texture"]]) for k in c]
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        first = syms[c[0]]
        t, meta = groups[item][zlib.crc32(wdtest._key(first).encode()) % len(groups[item])]
        bx0, by0, bx1, by1 = t["bbox"]
        scale = (((x1 - x0) * (y1 - y0)) / ((bx1 - bx0) * (by1 - by0))) ** 0.5
        new = dict(first)
        new["texture"], new["scale"] = t["texture"], type(first["scale"])(scale, scale)
        new["position"] = type(first["position"])((x0 + x1) / 2, y1)
        new["offset"] = type(first["offset"])(t["W"] / 2 - (bx0 + bx1) / 2, t["H"] / 2 - by1)
        cc = list(first.get("custom_colors") or [gdvar.Color(0, 0, 0, 1)] * 3)
        new["custom_colors"] = [cc[0], cc[1], gdvar.Color(*wdtest.ROOF, 1)]
        new["custom_color_mode"] = 1
        if "radius" in meta:
            new["radius"] = float(meta["radius"])
        syms[c[0]] = new
        drop.update(c[1:])
        counts[item] = counts.get(item, 0) + 1
    return [s for i, s in enumerate(syms) if i not in drop], counts


def make_map(log=print):
    m = WDMap.load(wdtest.BASE_MAP)
    done = swap_art(m.symbols, _folders(), log)
    m.data["symbols"], icons = swap_icons(m.symbols, log)
    for k, v in sorted(done.items(), key=lambda kv: -kv[1]):
        log("  %5d  %s" % (v, k))
    log("  %5d  city icons (%s)" % (sum(icons.values()), ", ".join("%s %d" % kv for kv in sorted(icons.items()))))
    left = {}
    for s in m.symbols:
        t = s.get("texture", "")
        if t.startswith("user://assets/") and not t.startswith(PACK):
            fam = t.rsplit("/", 1)[0].split("/sprites/")[-1]
            left[fam] = left.get(fam, 0) + 1
    log("  still other art: %s" % (", ".join("%s %d" % kv for kv in sorted(left.items(), key=lambda kv: -kv[1])) or "none"))
    m.save(OUT_MAP)
    log("  -> %s" % OUT_MAP)
    return OUT_MAP


def compare(out_dir, log=print):
    """The whole map and a few regions, Wonderdraft's built-ins (the Base's own export: the
    baseline) | Tyrnarra pack. Main's jungle and bamboo are bought art, not built-ins."""
    ref, stale = wdtest.reference(lambda *_: None)
    if stale:
        raise SystemExit("the Base's export is older than the Base; export it first (wd-regions --export)")
    now = wdtest._open(ref)
    ours = wdtest._open(OUT_MAP[:-len(".wonderdraft_map")] + ".webp")
    base = pre = WDMap.load(wdtest.BASE_MAP).symbols
    font = ImageFont.truetype(wdtest.FONT, 26)
    out = []
    whole = Image.new("RGB", (2 * 1600 + 30, 1600 + 50), (236, 229, 214))
    d = ImageDraw.Draw(whole)
    for i, (label, im) in enumerate((("Wonderdraft built-ins", now), ("Tyrnarra pack", ours))):
        d.text((10 + i * 1610, 10), label, font=font, fill=(40, 30, 20))
        whole.paste(im.resize((1600, 1600), Image.LANCZOS), (10 + i * 1610, 44))
    path = os.path.join(out_dir, "pack-whole-map.jpg")
    whole.save(path, quality=88)
    out.append(path)
    regions = [("conifer forest", wdtest.areas(pre, "res://sprites/trees/_hd_christmas/")[0][1]),
               ("oak forest", wdtest.areas(pre, "res://sprites/trees/_hd_oak/")[0][1]),
               ("jagged peaks", wdtest.areas(pre, "res://sprites/mountains/playful_jagged_peaks/")[0][1]),
               ("hills", wdtest.areas(pre, "res://sprites/mountains/playful_hiils/")[0][1]),
               ("dunes", wdtest.areas(pre, "res://packs/Arabia by Chan/sprites/mountains/sand_dunes_")[0][1]),
               ("jungle (Main: Dotty's kapoks)", wdtest.areas(base, "user://assets/Dotty_Assets/sprites/trees/Dotty_Kapoks/")[0][1]),
               ("willows", wdtest.areas(pre, "res://sprites/trees/_hd_willow/")[0][1]),
               ("cities", wdtest.areas(base, wdtest.BSG)[0][1])]
    cw, ch = 960, 600
    sheet = Image.new("RGB", (2 * cw + 30, len(regions) * (ch + 44) + 10), (236, 229, 214))
    d = ImageDraw.Draw(sheet)
    for r, (label, box) in enumerate(regions):
        y = 10 + r * (ch + 44)
        for name, im in (("built-ins", now), ("pack", ours)):
            g = im.crop(box).convert("L").histogram()
            n = sum(g)
            log("  %-40s %-9s mean grey %3.0f, dark (<50) %2.0f%%"
                % (label, name, sum(i * c for i, c in enumerate(g)) / n, 100 * sum(g[:50]) / n))
        d.text((10, y), "%s: Wonderdraft built-ins | Tyrnarra pack" % label, font=font, fill=(40, 30, 20))
        for i, im in enumerate((now, ours)):
            sheet.paste(im.crop(box).resize((cw, ch), Image.LANCZOS), (10 + i * (cw + 10), y + 36))
    path = os.path.join(out_dir, "pack-regions.jpg")
    sheet.save(path, quality=88)
    out.append(path)
    for p in out:
        log("  %s" % p)
    return out


LOAD_WAIT = 120   # s: Wonderdraft's first load of ~570 new pack images outlasts the usual 15 s


def run(out_dir, export=True, log=print):
    log("Tyrnarra pack in a copy of %s:" % os.path.basename(wdtest.BASE_MAP))
    path = make_map(log)
    if export:
        wd_export.export_views([path], log=log, load_wait=LOAD_WAIT)
    return compare(out_dir, log)
