"""The map's geography as text: neighbours, coasts, and contents of every domain and region shape.

For checking lore against the map. Each god domain and region shape is reported with its land
neighbours (compass direction centroid to centroid, and the shared border's length in cells),
shapes nearby that it does not border, its coasts per sea, and the labels inside it.

Works on a 1024-cell grid (8 map units per cell on Main). Seas: the Hafra is every sea reached
from the map edge; the Midarra is the largest water body left once its western mouth is closed
along MOUTH_X (the Balatur Erui line). Lakes and rivers are painted terrain, not part of the land
mask, so they are not seen here: look at the terrain export for them (the preview does not draw
them either). The Cloud Sea is not drawn on the map.
"""
import fnmatch
import math

import numpy as np
from PIL import Image, ImageDraw

N = 1024
MOUTH_X, MOUTH_Y = 900.0, (3000.0, 5200.0)   # Main: the Midarra's mouth at Balatur Erui
GROUPS = {1: "god", 2: "region", 3: "god-city", -1: "city"}
COMPASS = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]


def _flood(seed, passable):
    seen = seed & passable
    stack = list(zip(*np.nonzero(seen)))
    while stack:
        y, x = stack.pop()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < N and 0 <= nx < N and passable[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                stack.append((ny, nx))
    return seen


def _dilate(a, r):
    out = a.copy()
    for _ in range(r):
        o = out.copy()
        o[1:, :] |= out[:-1, :]
        o[:-1, :] |= out[1:, :]
        o[:, 1:] |= out[:, :-1]
        o[:, :-1] |= out[:, 1:]
        out = o
    return out


def _compass(dx, dy):
    ang = math.degrees(math.atan2(-dy, dx)) % 360
    return COMPASS[int(((ang + 22.5) % 360) // 45)]


def seas(m):
    """(land, {sea name: cell mask}) on the N x N grid."""
    s = N / m.width
    land = np.array(m.image("mask").split()[3].resize((N, N), Image.BILINEAR)) >= 128
    barrier = np.zeros_like(land)
    bx = int(MOUTH_X * s)
    barrier[int(MOUTH_Y[0] * s):int(MOUTH_Y[1] * s), bx - 1:bx + 2] = True
    water = ~land & ~barrier
    edge = np.zeros_like(water)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    hafra = _flood(edge, water)
    inner = water & ~hafra
    midarra = np.zeros_like(inner)
    if inner.any():
        # the largest inner body; start from each unclaimed cell until one covers most of it
        left = inner.copy()
        while left.any():
            y, x = next(zip(*np.nonzero(left)))
            seed = np.zeros_like(left)
            seed[y, x] = True
            body = _flood(seed, left)
            left &= ~body
            if body.sum() > midarra.sum():
                midarra = body
    return land, {"Hafra": hafra, "Midarra": midarra, "the Midarra's mouth": barrier & ~land}


def report(m, name=None):
    s = N / m.width
    land, sea = seas(m)
    shapes = {}
    for r in m.regions:
        if not r.name or len(r.points) < 3:
            continue
        im = Image.new("1", (N, N), 0)
        ImageDraw.Draw(im).polygon([(x * s, y * s) for x, y in r.points], fill=1)
        key = (r.kind, r.name)
        e = shapes.setdefault(key, {"mask": np.zeros((N, N), bool), "parts": 0})
        e["mask"] |= np.array(im, dtype=bool)
        e["parts"] += 1
    for e in shapes.values():
        e["land"] = e["mask"] & land
        use = e["land"] if e["land"].any() else e["mask"]
        ys, xs = np.nonzero(use)
        e["centre"] = (xs.mean() / s, ys.mean() / s)
        e["bbox"] = (xs.min() / s, ys.min() / s, xs.max() / s, ys.max() / s)
        e["near"] = _dilate(e["land"], 3)
        ring = _dilate(e["land"], 2) & ~land
        e["coast"] = {k: int((ring & v).sum()) for k, v in sea.items() if (ring & v).sum() >= 3}
    labels = [(" ".join(l["text"].split()), GROUPS.get(l["z_index"]), l["position"]) for l in m.labels]

    def rel(a, b):
        (ax, ay), (bx, by) = shapes[a]["centre"], shapes[b]["centre"]
        return _compass(bx - ax, by - ay)

    out = [__doc__.split("\n\n")[0], "",
           "Map units, x east and y south (smaller y is further north). Directions run centroid to "
           "centroid. Border and coast figures count grid cells (larger = longer).", ""]
    for kind in ("domain", "region"):
        keys = sorted(k for k in shapes if k[0] == kind)
        out += ["## %ss" % kind.capitalize(), ""]
        for key in keys:
            if name and not fnmatch.fnmatch(key[1].lower(), name.lower()):
                continue
            e = shapes[key]
            out.append("### %s" % key[1])
            out.append("- parts %d; centre (%d, %d); bbox (%d, %d, %d, %d)"
                       % ((e["parts"],) + tuple(int(v) for v in e["centre"] + e["bbox"])))
            if kind == "region":
                n = max(1, int(e["land"].sum()))
                dom = ["%s %d%%" % (d[1], 100 * (e["land"] & shapes[d]["land"]).sum() / n)
                       for d in shapes if d[0] == "domain" and (e["land"] & shapes[d]["land"]).sum() / n > 0.05]
                out.append("- in: %s" % (", ".join(dom) or "no domain"))
            nb, near = [], []
            reach = _dilate(e["land"], int(450 * s))
            for other in keys:
                if other == key:
                    continue
                w = int((e["near"] & shapes[other]["land"]).sum())
                if w >= 6:
                    nb.append((w, "%s (%s, %d)" % (other[1], rel(key, other), w)))
                elif (reach & shapes[other]["land"]).sum() >= 4:
                    near.append("%s (%s)" % (other[1], rel(key, other)))
            out.append("- borders: %s" % (", ".join(t for _, t in sorted(nb, reverse=True)) or "none"))
            if near:
                out.append("- nearby, not bordering: %s" % ", ".join(near))
            out.append("- coasts: %s" % (", ".join("%s %d" % kv for kv in sorted(e["coast"].items(), key=lambda kv: -kv[1]))
                                          or "landlocked"))
            inside = sorted({"%s [%s]" % (t, g) for t, g, (x, y) in labels
                             if g in ("region", "god-city", "city") and t != key[1]
                             and 0 <= int(x * s) < N and 0 <= int(y * s) < N and e["mask"][int(y * s), int(x * s)]})
            if inside:
                out.append("- labels inside: %s" % ", ".join(inside))
            out.append("")
    return "\n".join(out)
