"""Adding things to a WDMap: single symbols and labels, scatters, rows along a path.

New symbols copy a template symbol that already uses the art (Wonderdraft computes
a sprite's offset/footprint on placement; we reuse what it computed), get the
family's typical scale unless told otherwise, and a fresh ground-colour sample.
Everything is appended; nothing is saved here.
"""
import copy
import math
import random
import statistics

from edit import art_targets
from gdvar import Vector2
from wdmap import family


def _typical_scale(m, texture):
    fam = family(texture)
    scales = [s["scale"][0] for s in m.symbols if family(s.get("texture")) == fam]
    return statistics.median(scales) if scales else 1.0


def _typical_layer(m, texture):
    """The layer this art family is used on most (a town icon lives on City Icons, not
    on the Legend where its first copy happens to be)."""
    fam = family(texture)
    layers = [s.get("z_index", 0) for s in m.symbols if family(s.get("texture")) == fam]
    return statistics.mode(layers) if layers else 0


def make_symbol(m, template, x, y, scale=None, layer=None, rotation=0.0, mirror=False):
    s = copy.deepcopy(template)
    k = scale if scale is not None else _typical_scale(m, template["texture"])
    s["position"] = Vector2(x, y)
    s["scale"] = Vector2(k, k)
    s["rotation"] = float(rotation)
    s["mirror"] = bool(mirror)
    if layer is not None:
        s["z_index"] = layer
    if s.get("sample") is not None:
        s["sample"] = m.ground_sample(x, y)
    return s


def add_symbols(m, art, points, scale=None, layer=None, seed=None, jitter_scale=0.0, mirror="random"):
    """Append one symbol per (x, y), picking variants of `art` at random. Returns the new indices."""
    targets, _ = art_targets(m, art)
    rng = random.Random(seed)
    names = list(targets)
    base = scale if scale is not None else _typical_scale(m, names[0])
    if layer is None:
        layer = _typical_layer(m, names[0])
    start = len(m.symbols)
    for x, y in sorted(points, key=lambda p: p[1]):
        k = base * (1 + rng.uniform(-jitter_scale, jitter_scale)) if jitter_scale else base
        flip = rng.random() < 0.5 if mirror == "random" else bool(mirror)
        m.symbols.append(make_symbol(m, targets[rng.choice(names)], x, y, scale=k, layer=layer, mirror=flip))
    return list(range(start, len(m.symbols)))


def label_template(m, like=None, layer=None):
    """An existing label to copy the style from: the first matching `like`, else the first on `layer`."""
    import fnmatch
    for l in m.labels:
        if like and fnmatch.fnmatch(" ".join(l["text"].split()).lower(), like.lower()):
            return l
        if not like and layer is not None and l.get("z_index") == layer:
            return l
    raise ValueError("no label to copy the style from (%s)" % (like or "layer %s" % layer))


def add_label(m, text, x, y, like=None, layer=None, size=None):
    tpl = label_template(m, like, layer)
    l = copy.deepcopy(tpl)
    l["text"] = text
    l["position"] = Vector2(x, y)
    l["rotation"] = 0.0
    if layer is not None:
        l["z_index"] = layer
    if size:
        l["size"] = size
    m.labels.append(l)
    m.invalidate()
    return len(m.labels) - 1


# --- scatter -------------------------------------------------------------------

class _Grid:
    """Spatial hash of occupied points for spacing checks."""

    def __init__(self, cell):
        self.cell = max(1.0, cell)
        self.cells = {}

    def add(self, x, y, r):
        self.cells.setdefault((int(x // self.cell), int(y // self.cell)), []).append((x, y, r))

    def clear(self, x, y, r):
        cx, cy = int(x // self.cell), int(y // self.cell)
        reach = 1 + int(r // self.cell)
        for gx in range(cx - reach, cx + reach + 1):
            for gy in range(cy - reach, cy + reach + 1):
                for px, py, pr in self.cells.get((gx, gy), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < max(r, pr) ** 2:
                        return False
        return True


def label_boxes(m, pad=0.0):
    """Approximate text boxes (x0, y0, x1, y1) of all labels, for keeping symbols off them."""
    out = []
    for l in m.labels:
        x, y = l["position"]
        lines = l["text"].split("\n")
        w = max(len(t) for t in lines) * l.get("size", 32) * 0.55 / 2 + pad
        h = len(lines) * l.get("size", 32) * 0.6 + pad
        out.append((x - w, y - h, x + w, y + h))
    return out


def scatter_points(m, contains, bbox, spacing, count=None, density=None, on="land",
                   avoid=True, seed=None, area_hint=None):
    """Random points inside `contains(x, y)` within `bbox`, at least `spacing` apart and
    (with avoid) clear of existing symbols and labels.

    Without count or density the area is filled as far as the spacing allows;
    density is symbols per 1000x1000 map units.
    """
    x0, y0, x1, y1 = bbox
    if count is None:
        area = area_hint if area_hint is not None else (x1 - x0) * (y1 - y0)
        count = max(1, round(density * area / 1e6 if density else area / (spacing * spacing)))
    rng = random.Random(seed)
    grid = _Grid(spacing)
    boxes = [b for b in label_boxes(m, pad=spacing / 2)
             if b[2] >= x0 and b[0] <= x1 and b[3] >= y0 and b[1] <= y1] if avoid else []
    if avoid:
        for s in m.symbols:
            x, y = s["position"]
            if x0 - spacing <= x <= x1 + spacing and y0 - spacing <= y <= y1 + spacing:
                grid.add(x, y, max(spacing, (s.get("radius") or 0) * s["scale"][0] * 0.8))
    pts = []
    tries = 0
    while len(pts) < count and tries < count * 40:
        tries += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if not contains(x, y):
            continue
        if on and m.is_land(x, y) != (on == "land"):
            continue
        if not grid.clear(x, y, spacing):
            continue
        if any(b[0] <= x <= b[2] and b[1] <= y <= b[3] for b in boxes):
            continue
        grid.add(x, y, spacing)
        pts.append((x, y))
    return pts, count


# --- along a path --------------------------------------------------------------

def path_points(path, spacing, jitter=0.0, seed=None):
    """Points every `spacing` map units along a polyline, pushed sideways by up to `jitter`."""
    rng = random.Random(seed)
    out = []
    carry = 0.0
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        seg = math.hypot(bx - ax, by - ay)
        if seg == 0:
            continue
        ux, uy = (bx - ax) / seg, (by - ay) / seg
        d = carry
        while d <= seg:
            off = rng.uniform(-jitter, jitter) if jitter else 0.0
            out.append((ax + ux * d - uy * off, ay + uy * d + ux * off))
            d += spacing
        carry = d - seg
    return out


# --- region shapes ---------------------------------------------------------------

def copy_shape(m, x, y, color, kind="region", width=None):
    """Add a region shape by copying the outline of the smallest existing shape at (x, y).

    Islands often have a god-domain outline but no region outline; copying the domain
    outline gives the region exactly the same coast. The copy gets the border style of
    `kind` and a fill `color` (alpha taken from an existing shape of that kind, so it
    matches the others). Returns the new territory index.
    """
    from edit import BORDER_STYLE, parse_color
    hits = [r for r in m.regions if r.contains(x, y)]
    if not hits:
        raise ValueError("no shape at (%g, %g) to copy the outline from" % (x, y))
    src = min(hits, key=lambda r: r.area)
    same = [r for r in m.regions if r.kind == kind]
    alpha = statistics.median([r.data["color"][3] for r in same]) if same else src.data["color"][3]
    t = copy.deepcopy(src.data)
    t["style"] = BORDER_STYLE.get(kind, kind)
    t["color"] = parse_color(color, alpha=alpha)
    if same:
        t["width"] = same[0].data.get("width", t.get("width"))
        t["opacity"] = same[0].data.get("opacity", t.get("opacity"))
    if width is not None:
        t["width"] = float(width)
    m.territories.append(t)
    m.invalidate()
    return len(m.territories) - 1, src
