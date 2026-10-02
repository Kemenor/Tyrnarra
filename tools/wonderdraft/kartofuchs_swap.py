#!/usr/bin/env python3
"""Main in Kartofuchs, all on Kartofuchs' own art (Fuchsbau). Two steps, both against a running
Kartofuchs (the desktop app, or `node bin/kartofuchs.ts serve <map>`):

  kartofuchs_swap.py mapping                 save the "Tyrnarra" art mapping into Kartofuchs: the
                                             Fuchsbau mapping it ships (Wonderdraft's built-ins) plus
                                             the bought packs Main uses (Dotty kapoks, Nibroc's
                                             bamboo, 2-Minute hills and mountains)
  kartofuchs_swap.py cities [--flat] [--dry] the open map's BSG city icons as Fuchsbau icons

Import Main with the "Tyrnarra" mapping (Map > Import, "Swap the art with"), or run Create > Swap
art on it, then `cities`. Each step is one undo step in Kartofuchs.

`cities` does what the old assetgen fullswap did for Wonderdraft: every cluster of BSG icons (icons
of one layer within CLUSTER_GAP of each other) becomes one Fuchsbau icon as big as the whole
cluster (by area), standing on its bottom edge, in the city's own line and wall colours with a roof
colour added. God-cities take their own icon, found by the nearest "Divine City Labels" label;
other cities go by BSG_KINDS. Legend icons stay one by one. --flat uses the flat 2D settlements
(god-cities stay raised). Mooma's markers have no Fuchsbau counterpart and stay.

Options: --port (KARTOFUCHS_PORT, default 7717), --map (title of the open map, default Main),
--art (Fuchsbau's folder; default $KARTOFUCHS/art/Fuchsbau, KARTOFUCHS default
~/Documents/fuchs/kartofuchs), --bsg (the BSG pack's icon folder, for the icons' drawn sizes).
"""
import argparse
import json
import math
import os
import sys
import urllib.parse
import urllib.request
import zlib

from PIL import Image

MAPPING = "Tyrnarra"
FB = "wd:Fuchsbau/sprites"
# The bought packs Main uses, by family: [from, Fuchsbau folder, match].
EXTRA_RULES = [
    ("wd:Dotty_Assets/sprites/trees/Dotty_Kapoks", "trees/Fuchsbau_Jungle", "area"),
    ("wd:Nibroc's Bamboo Forest/sprites/trees/Bamboo Trees", "trees/Fuchsbau_Bamboo", "area"),
    ("wd:2-Minute Table Top Wonderdraft Assets/sprites/mountains/2-min_hills", "mountains/Fuchsbau_Hills", "width"),
    ("wd:2-Minute Table Top Wonderdraft Assets/sprites/mountains/2-min_mountains", "mountains/Fuchsbau_Peaks", "area"),
    ("wd:2-Minute Table Top Wonderdraft Assets/sprites/mountains/2-min_rugged_mountains", "mountains/Fuchsbau_Peaks", "area"),
    ("wd:2-Minute Table Top Wonderdraft Assets/sprites/mountains/2-min_mountain_ranges", "mountains/Fuchsbau_Peaks", "area"),
]

BSG = "wd:BSG_elvanos_mapIcons/sprites/symbols/BSG & Elvanos - Map Icons Custom Colors Textured"
BSG_KINDS = [("Large City Stone Wall + Towers", "walled_city"), ("Large Stone Wall", "walled_town"),
             ("Small City Stone Wall", "walled_town"), ("Fortress", "fortress"), ("Cathedral", "temple"),
             ("Castle", "castle"), ("Keep", "castle"), ("Small City", "city"), ("Town", "town")]
ROOF = "#9e4533"     # colour 3 (roofs): Main's BSG icons leave it black
CLUSTER_GAP = 70     # map units between icons of one city
ALPHA = 24           # what counts as drawn (Kartofuchs' art boxes use the same)


def api(base, path, body=None):
    req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"content-type": "application/json", "x-kartofuchs": "1"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("%s: %s %s" % (path, e.code, e.read().decode(errors="replace")))
    except urllib.error.URLError as e:
        sys.exit("no Kartofuchs at %s (%s): start the app or `kartofuchs serve`" % (base, e.reason))


def cmd_mapping(a, base):
    rules = api(base, "/api/art-mappings?name=Fuchsbau")["rules"]
    rules += [{"from": f, "to": "%s/%s" % (FB, to), "match": m} for f, to, m in EXTRA_RULES]
    api(base, "/api/art-mappings", {"name": MAPPING, "rules": rules})
    print('saved the "%s" mapping: %d rules (%d of them for bought packs)' % (MAPPING, len(rules), len(EXTRA_RULES)))


_boxes = {}


def art_box(path):
    """(W, H, x0, y0, x1, y1) of a picture's drawn part."""
    if path not in _boxes:
        im = Image.open(path).convert("RGBA")
        bb = im.getchannel("A").point(lambda v: 255 if v > ALPHA else 0).getbbox() or (0, 0, im.width, im.height)
        _boxes[path] = (im.width, im.height) + bb
    return _boxes[path]


def drawn(it, box):
    """The map box an icon's art covers: Kartofuchs draws the picture's middle at its position +
    anchor x scale."""
    W, H, x0, y0, x1, y1 = box
    s = it["scale"]
    cx, cy = it["x"] + it["anchorX"] * s, it["y"] + it["anchorY"] * s
    return (cx + (x0 - W / 2) * s, cy + (y0 - H / 2) * s, cx + (x1 - W / 2) * s, cy + (y1 - H / 2) * s)


def clusters(icons, gap):
    groups, left = [], list(icons)
    while left:
        group, todo = [], [left.pop()]
        while todo:
            i = todo.pop()
            group.append(i)
            near = [j for j in left if (j["x"] - i["x"]) ** 2 + (j["y"] - i["y"]) ** 2 < gap ** 2]
            for j in near:
                left.remove(j)
            todo += near
        groups.append(group)
    return groups


def layers(nodes):
    for n in nodes:
        if n["kind"] == "layer":
            yield n
        yield from layers(n.get("children") or [])


def cmd_cities(a, base):
    maps = [m for m in api(base, "/api/app")["maps"] if m["title"] == a.map]
    if not maps:
        sys.exit("no open map called %r" % a.map)
    mb = base + "/m/" + maps[0]["id"]
    doc = api(mb, "/api/map")["doc"]
    ours = {}
    for folder in ("Fuchsbau_2D_Settlements" if a.flat else "Fuchsbau_2.5D_Settlements", "Fuchsbau_2.5D_God_Cities"):
        meta = json.load(open(os.path.join(a.art, "sprites", "symbols", folder, ".wonderdraft_symbols")))
        for f in sorted(os.listdir(os.path.join(a.art, "sprites", "symbols", folder))):
            if f.endswith(".png"):
                name = f[:-4]
                ours.setdefault(name.rsplit("_", 1)[0], []).append(
                    ("%s/symbols/%s/%s" % (FB, folder, name), os.path.join(a.art, "sprites", "symbols", folder, f), meta.get(name, {})))
    bsg_file = lambda it: os.path.join(a.bsg, it["asset"].rsplit("/", 1)[1] + ".png")
    gods = [(l["text"].strip().lower().replace(" ", "_"), l["x"], l["y"])
            for ly in layers(doc["layers"]) if ly["name"] == "Divine City Labels" for l in ly["items"] if l["kind"] == "label"]
    cs, legend = [], set()   # clusters of every layer; the legend's, one icon each
    for ly in layers(doc["layers"]):
        icons = [i for i in ly["items"] if i["kind"] == "symbol" and i["asset"].startswith(BSG + "/")]
        if "Legend" in ly["name"]:
            legend.update(range(len(cs), len(cs) + len(icons)))
            cs += [[i] for i in icons]
        elif icons:
            cs += clusters(icons, CLUSTER_GAP)
    # Each god-city label takes the nearest city on the map (never a legend icon).
    god = {}
    for name, x, y in gods:
        on_map = [g for g in range(len(cs)) if g not in legend]
        near = min(on_map, key=lambda g: min((i["x"] - x) ** 2 + (i["y"] - y) ** 2 for i in cs[g]), default=None)
        if near is not None and name in ours:
            god[near] = name
    work = []   # (cluster, item)
    for g, c in enumerate(cs):
        names = {i["asset"].rsplit("/", 1)[1] for i in c}
        item = god.get(g) or next((kind for n, kind in BSG_KINDS if n in names), None)
        if item in ours:
            work.append((c, item))
    ops, counts = [], {}
    for c, item in work:
        boxes = [drawn(i, art_box(bsg_file(i))) for i in c]
        X0, Y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        X1, Y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        first = c[0]
        ref, path, meta = ours[item][zlib.crc32(("%d" % first["id"]).encode()) % len(ours[item])]
        W, H, bx0, by0, bx1, by1 = art_box(path)
        # The cluster's area, not its width: ours are wide raised views, BSG's tall fronts.
        scale = math.sqrt(((X1 - X0) * (Y1 - Y0)) / ((bx1 - bx0) * (by1 - by0)))
        cc = first["tint"]["colors"] if first["tint"].get("mode") == "custom" else ["#000000", "#ffffff", "#000000"]
        was = {k: first[k] for k in ("asset", "scale", "anchorX", "anchorY", "footprint", "tint")}
        ops.append({"op": "item.update", "id": first["id"], "set": {
            "asset": ref, "x": round((X0 + X1) / 2, 2), "y": round(Y1, 2), "scale": round(scale, 5), "rotation": 0, "mirror": False,
            "anchorX": round(W / 2 - (bx0 + bx1) / 2, 2), "anchorY": round(H / 2 - by1, 2),
            "footprint": meta.get("radius", first["footprint"]),
            "tint": {"mode": "custom", "colors": [cc[0], cc[1], ROOF]}, "was": first.get("was") or was}})
        if len(c) > 1:
            ops.append({"op": "item.remove", "ids": [i["id"] for i in c[1:]]})
        counts[item] = counts.get(item, 0) + 1
    print("%d city icons in %d places: %s" % (sum(len(c) for c, _ in work), len(work),
                                              ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
    if a.dry or not ops:
        return
    r = api(mb, "/api/tx", {"ops": ops, "label": "City icons to Fuchsbau", "origin": "script"})
    print("done (map version %s): one undo step in Kartofuchs" % r.get("version"))


def main():
    repo = os.path.expanduser(os.environ.get("KARTOFUCHS", "~/Documents/fuchs/kartofuchs"))
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", type=int, default=int(os.environ.get("KARTOFUCHS_PORT", 7717)))
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("mapping").set_defaults(fn=cmd_mapping)
    s = sub.add_parser("cities")
    s.add_argument("--map", default="Main")
    s.add_argument("--flat", action="store_true", help="the flat 2D settlements (god-cities stay raised)")
    s.add_argument("--dry", action="store_true", help="say what would change, change nothing")
    s.add_argument("--art", default=os.path.join(repo, "art", "Fuchsbau"))
    s.add_argument("--bsg", default=os.path.expanduser("~/.local/share/Wonderdraft/assets/BSG_elvanos_mapIcons/sprites/symbols/"
                                                       "BSG & Elvanos - Map Icons Custom Colors Textured"))
    s.set_defaults(fn=cmd_cities)
    a = p.parse_args()
    a.fn(a, "http://127.0.0.1:%d" % a.port)


if __name__ == "__main__":
    main()
