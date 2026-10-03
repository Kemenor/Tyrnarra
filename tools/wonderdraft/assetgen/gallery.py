"""Review sheets of the installed pack, Fuchsbau (assetgen.sh gallery [FAMILY...]).

One JPG per family in ~/.local/share/wdmap/assetgen/gallery/: its sprites grouped by the variant
(or icon item) each was drawn as, each labelled with its file number, so a review can name
them ("conifer 15 looks empty"). Greyscale art is tinted the way Wonderdraft tints it (one
colour per family); custom-colour icons are drawn with example colours.

A drawing's variant comes from the prompt saved next to its raw image: the installed file is
matched to the round that built it (the round's sprites/ copy and chosen.txt), and its prompt to
the family's variant whose words it shares most, so drawings from older wordings still land in
their group. Icons are grouped by the item in their file name ({item}_{n}).
"""
import hashlib
import os
import re

from PIL import Image, ImageChops, ImageDraw, ImageFont

import recipes
import sprites

WORK = os.path.expanduser("~/.local/share/wdmap/assetgen")
OUT = os.path.join(WORK, "gallery")
FONT = os.path.expanduser("~/.local/share/fonts/wonderdraft/GentiumBookBasic-GenBkBasB.ttf")
BG, INK, GROUP_INK, NUM_INK = (236, 229, 214), (40, 30, 20), (110, 70, 30), (90, 80, 70)
WIDTH, ROW_H = 1800, 190   # sheet width; the family's typical (median) sprite is drawn this tall
TITLES = {"conifer": "Conifers", "pine": "Pines and cedars", "broadleaf": "Broadleaves",
          "willow": "Willows", "jungle": "Jungle", "palm": "Palms", "bamboo": "Bamboo",
          "savanna": "Savanna", "desert": "Cacti", "deadtree": "Dead trees", "fungal": "Giant mushrooms",
          "peaks": "Peaks", "fells": "Fells (rounded mountains)", "hills": "Hills", "dunes": "Dunes",
          "swamp": "Swamp trees", "shrubs": "Shrubs", "mesas": "Mesas and buttes", "pillars": "Karst pillars", "holy_mountains": "Holy mountains", "fruit_trees": "Fruit trees", "shrine_trees": "Shrine trees", "giant_trees": "Giant trees", "named_trees": "Named trees", "special_sites": "Special sites (2D)", "volcanoes": "Volcanoes", "landmarks": "Landmarks (2.5D)",
          "settlements": "Settlements (2.5D)", "settlements_2d": "Settlements (2D)", "god_cities": "God-cities (2.5D)"}
# Stand-ins for the ground colours Wonderdraft tints greyscale art with.
TINTS = {"conifer": (84, 128, 78), "pine": (92, 132, 84), "broadleaf": (112, 158, 84),
         "willow": (126, 166, 92), "jungle": (78, 136, 72), "palm": (128, 164, 88),
         "bamboo": (138, 176, 92), "savanna": (168, 162, 86), "desert": (124, 156, 96),
         "deadtree": (138, 120, 98), "fungal": (168, 124, 150), "peaks": (156, 152, 146),
         "fells": (140, 152, 122), "hills": (178, 134, 76), "dunes": (230, 170, 74),
         "swamp": (96, 122, 80), "shrubs": (118, 150, 84), "mesas": (198, 132, 88), "pillars": (200, 196, 186)}
STOP = {"a", "an", "the", "of", "with", "on", "and", "in", "to", "its", "one", "single", "tree", "drawn"}


def _font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def _md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def _words(text):
    return set(re.findall(r"[a-z]+", text.lower())) - STOP


def _label(variant):
    """A variant's group title: the part before its colon, or the whole (shortened)."""
    head = variant.split(":")[0] if ":" in variant else variant
    head = head if len(head) <= 60 else head[:57].rsplit(" ", 1)[0] + "..."
    return head[:1].upper() + head[1:]


def _prompts(fam, files):
    """{installed file: prompt} from the round whose sprites match the installed ones."""
    folder = sprites.pack_dir(fam)
    base = os.path.join(WORK, fam["name"])
    rounds = sorted((d for d in os.listdir(base) if re.fullmatch(r"round-\d+", d)) if os.path.isdir(base) else [],
                    key=lambda d: -int(d[6:]))
    want = {f: _md5(os.path.join(folder, f)) for f in files}
    for r in rounds:
        rs = os.path.join(base, r, "sprites")
        if not all(os.path.exists(os.path.join(rs, f)) and _md5(os.path.join(rs, f)) == h for f, h in want.items()):
            continue
        out = {}
        for line in open(os.path.join(base, r, "chosen.txt")):
            m = re.match(r"(\S+) <- (\S+) seed (\d+)", line)
            if m and m[1] + ".png" in want:
                txt = os.path.join(base, m[2], "raw", "%s.txt" % m[3])
                out[m[1] + ".png"] = open(txt).readline() if os.path.exists(txt) else ""
        return out
    return {}


def groups(fam):
    """[(group title, [installed file names])] in the family's variant or item order."""
    folder = sprites.pack_dir(fam)
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    if "items" in fam:
        by = {}
        for f in files:
            by.setdefault(f[:-4].rsplit("_", 1)[0], []).append(f)
        return [(item.replace("_", " ").title(), by.pop(item)) for item, _ in fam["items"] if item in by] + \
               [(item, fs) for item, fs in by.items()]
    variants = recipes.variants(fam)
    prompts = _prompts(fam, files)
    by = {}
    for f in files:
        p = prompts.get(f, "")
        exact = [v for v in variants if v and v.lower() in p.lower()]
        if exact:
            v = max(exact, key=len)
        elif p and variants != [""]:
            v = max(variants, key=lambda v: len(_words(v) & _words(p)) / max(1, len(_words(v))))
        else:
            v = ""
        by.setdefault(v, []).append(f)
    return [(_label(v) if v else "All", by[v]) for v in variants if v in by]


def _block(title, fs, tiles, font, draw):
    """A group laid out on its own: (width, height, rows of (file, x), row heights)."""
    rows, x, cur = [], 0, []
    for f in fs:
        w = max(tiles[f][0].width, 36)
        if cur and x + w > WIDTH - 40:
            rows.append(cur)
            cur, x = [], 0
        cur.append((f, x))
        x += w + 14
    rows.append(cur)
    width = max([draw.textlength(title, font=font)] +
                [xx + max(tiles[f][0].width, 36) for row in rows for f, xx in row])
    heights = [max(tiles[f][0].height for f, _ in row) + 34 for row in rows]
    return int(width), 44 + sum(heights), rows, heights


def sheet(name):
    """Write one family's review sheet; returns its path."""
    fam = dict(recipes.FAMILIES[name], name=name)
    folder = sprites.pack_dir(fam)
    cc = fam.get("draw") == "custom_colors"
    grouped = groups(fam)
    count = sum(len(fs) for _, fs in grouped)
    ims = {f: Image.open(os.path.join(folder, f)).convert("RGBA") for _, fs in grouped for f in fs}
    # The typical sprite is drawn ROW_H tall; the family's relative sizes stay (a tower stays tall).
    scale = ROW_H / sorted(im.height for im in ims.values())[len(ims) // 2]
    tint = TINTS.get(name, (150, 150, 150))
    tiles = {}
    for f, im in ims.items():
        sp = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        rgb = sprites.cc_colour(sp, fam.get("cc_example", sprites.CC_EXAMPLE)).convert("RGB") if cc else \
            ImageChops.multiply(sp.convert("RGB"), Image.new("RGB", sp.size, tint))
        tiles[f] = (rgb, sp.getchannel("A"))
    f_title, f_group, f_num = _font(40), _font(28), _font(18)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    # Groups flow side by side where they fit (icon items with two drawings each stay compact);
    # a group of many sprites fills the width and wraps on its own.
    placed, x, y, line_h = [], 20, 80, 0
    for title, fs in grouped:
        label = "%s (%d)" % (title, len(fs))
        bw, bh, rows, heights = _block(label, fs, tiles, f_group, probe)
        if x > 20 and x + bw > WIDTH - 20:
            x, y, line_h = 20, y + line_h + 10, 0
        placed.append((label, x, y, rows, heights))
        x += bw + 48
        line_h = max(line_h, bh)
    out = Image.new("RGB", (WIDTH, y + line_h + 20), BG)
    d = ImageDraw.Draw(out)
    d.text((20, 18), "%s  ·  %s  ·  %d sprites" % (TITLES.get(name, name), fam["pack_folder"], count),
           font=f_title, fill=INK)
    for label, bx, by, rows, heights in placed:
        d.text((bx, by + 8), label, font=f_group, fill=GROUP_INK)
        top = by + 44
        for row, h in zip(rows, heights):
            base = top + h - 34
            for f, xx in row:
                rgb, a = tiles[f]
                out.paste(rgb, (bx + xx, base - rgb.height), a)
                num = f[:-4].rsplit("_", 1)[1]
                d.text((bx + xx + (rgb.width - d.textlength(num, font=f_num)) / 2, base + 4), num,
                       font=f_num, fill=NUM_INK)
            top += h
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "%02d-%s.jpg" % (list(recipes.FAMILIES).index(name) + 1, name.replace("_", "-")))
    out.save(path, quality=86)
    return path


def run(names):
    if set(names) == set(recipes.FAMILIES):
        for f in os.listdir(OUT) if os.path.isdir(OUT) else []:
            if f.endswith(".jpg"):
                os.remove(os.path.join(OUT, f))   # a full run replaces the whole set
    return [sheet(n) for n in names if os.path.isdir(sprites.pack_dir(dict(recipes.FAMILIES[n], name=n)))]
