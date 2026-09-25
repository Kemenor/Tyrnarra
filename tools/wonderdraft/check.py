"""Consistency checks for a Wonderdraft map: the problems found by hand while fixing Main
(2026-09-25), as one pass. Each check returns Issues; nothing is changed.

error    Wonderdraft can't handle it (self-crossing outlines are left unfilled,
         "Convex partition failed" in its log).
warning  Probably wrong on the map (missing region shapes, unnamed shapes,
         unnamed capitols, overlapping labels, labels on the wrong layer, ...).
info     Worth a look (trees standing in water).
"""
import random
from collections import namedtuple

import stamps
from wdmap import family

Issue = namedtuple("Issue", "level kind message at")

# The thirteen Bound-god cities (CLAUDE.md, god-city-workflow): their names belong on
# Divine City Labels (+3), and nothing else does.
GOD_CITIES = {"Merkavar", "Myrria", "Haizava", "Eldara", "Valreka", "Thekkavar", "Frae City",
              "Uravel", "Lurrath", "Ljosarn", "Lograth", "Veidrath", "Nahaskel"}
DIVINE_LAYER = 3
CITY_NAME_LAYERS = (DIVINE_LAYER, -1)  # layers that name a settlement
CAPITOL_LEGEND = "Capitol"
CAPITOL_NAME_RADIUS = 160
OWN_NAME_RADIUS = 60  # a region label this close to a capitol names it too (city-state: Rika Tikur)
DARK_LUMINANCE = 0.12  # region colours darker than this vanish against Wonderdraft's deep-blue sea


def _txt(l):
    return " ".join(l["text"].split())


def _xy(p):
    return (round(p[0]), round(p[1]))


def _crosses(a, b, c, d):
    o = lambda p, q, r: (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])  # noqa: E731
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def self_crossings(pts):
    """Index pairs of non-adjacent outline segments that cross."""
    n = len(pts)
    return [(i, j) for i in range(n) for j in range(i + 2, n) if not (i == 0 and j == n - 1)
            and _crosses(pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n])]


def check_outlines(m):
    out = []
    for r in m.regions:
        if len(r.points) < 3:
            out.append(Issue("error", "outline", "%s shape %s has only %d points" % (r.kind, r.label, len(r.points)),
                             _xy(r.bbox[:2])))
            continue
        knots = self_crossings(r.points)
        if knots:
            i, j = knots[0]
            out.append(Issue("error", "outline", "%s shape %s crosses itself (segments %d and %d%s); "
                             "Wonderdraft leaves it unfilled" % (r.kind, r.label, i, j,
                                                                 ", +%d more" % (len(knots) - 1) if len(knots) > 1 else ""),
                             _xy(r.points[i])))
    return out


def check_shapes(m):
    out = []
    regs = [r for r in m.regions if r.kind == "region"]
    for r in m.regions:
        if not r.name and r.kind in ("domain", "region"):
            out.append(Issue("warning", "unnamed", "%s shape without a name label (colour #%02x%02x%02x)"
                             % ((r.kind,) + tuple(round(c * 255) for c in r.data["color"][:3])), _xy(r.bbox[:2])))
    # Near-identical outlines of the same kind on top of each other (Soul Tree had two).
    shapes = sorted(m.regions, key=lambda r: r.bbox)
    for i, a in enumerate(shapes):
        for b in shapes[i + 1:]:
            if b.bbox[0] - a.bbox[0] > 3:
                break
            if a.kind == b.kind and all(abs(p - q) <= 3 for p, q in zip(a.bbox, b.bbox)):
                out.append(Issue("warning", "duplicate", "two %s outlines on top of each other (%s, %s)"
                                 % (a.kind, a.label, b.label), _xy(a.bbox[:2])))
    for r in regs:
        c = r.data["color"]
        lum = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        wet = sum(1 for x, y in r.points if not m.is_land(x, y)) / len(r.points) if r.points else 0
        if lum < DARK_LUMINANCE and wet >= 0.5:
            out.append(Issue("warning", "colour", "region %s is very dark (#%02x%02x%02x) and its outline runs "
                             "mostly through water; it can vanish against the sea"
                             % ((r.label,) + tuple(round(v * 255) for v in c[:3])), _xy(r.bbox[:2])))
    # Land inside a domain outline that no region shape covers.
    rng = random.Random(1)
    for d in (r for r in m.regions if r.kind == "domain"):
        x0, y0, x1, y1 = d.bbox
        pts, tries = [], 0
        while len(pts) < 40 and tries < 4000:
            tries += 1
            x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
            if d.contains(x, y) and m.is_land(x, y):
                pts.append((x, y))
        if len(pts) < 5:
            continue
        uncovered = [p for p in pts if not any(r.contains(*p) for r in regs)]
        if len(uncovered) / len(pts) >= 0.5:
            labels = [_txt(l) for l in m.labels if d.contains(*l["position"])]
            out.append(Issue("warning", "no-region", "land in %s's domain outline has no region shape (%d%% uncovered%s)"
                             % (d.label, 100 * len(uncovered) // len(pts),
                                "; labels: " + ", ".join(labels[:3]) if labels else ""), _xy(uncovered[0])))
    return out


def capitol_family(m):
    """Art family of the Legend's "Capitol" icon: the legend symbol nearest that legend label."""
    lab = [l for l in m.labels if l.get("z_index") == 5 and _txt(l) == CAPITOL_LEGEND]
    legend = [s for s in m.symbols if s.get("z_index") == 5]
    if not lab or not legend:
        return None
    x, y = lab[0]["position"]
    s = min(legend, key=lambda s: (s["position"][0] - x) ** 2 + (s["position"][1] - y) ** 2)
    return family(s["texture"])


def check_capitols(m):
    fam = capitol_family(m)
    if not fam:
        return []
    names = [l for l in m.labels if l.get("z_index") in CITY_NAME_LAYERS]
    own = [l for l in m.labels if l.get("z_index") == 2]
    out = []
    for s in m.symbols:
        if s.get("z_index") == 5 or family(s.get("texture")) != fam:
            continue
        x, y = s["position"]
        if not any((l["position"][0] - x) ** 2 + (l["position"][1] - y) ** 2 <= CAPITOL_NAME_RADIUS ** 2 for l in names) \
                and not any((l["position"][0] - x) ** 2 + (l["position"][1] - y) ** 2 <= OWN_NAME_RADIUS ** 2 for l in own):
            region = next((r.label for r in m.regions if r.kind == "region" and r.contains(x, y)), "no region")
            out.append(Issue("warning", "capitol", "capitol icon without a city name (in %s)" % region, _xy((x, y))))
    return out


def label_box(l):
    """Text box (x0, y0, x1, y1) in map units, measured with the map's font."""
    from preview import _font
    from PIL import Image, ImageDraw
    size = int(l.get("size", 32))
    f = _font(l.get("font") or "serif", size)
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    bx = d.multiline_textbbox((0, 0), l["text"], font=f, anchor="mm", align="center")
    x, y = l["position"]
    return (x + bx[0], y + bx[1], x + bx[2], y + bx[3])


def check_labels(m, views):
    out = []
    for l in m.labels:
        t, z = _txt(l), l.get("z_index")
        if stamps.is_marker(l):
            out.append(Issue("warning", "marker", "leftover marker label %r (run `wdmap markers`)" % t,
                             _xy(l["position"])))
        elif t in GOD_CITIES and z != DIVINE_LAYER:
            out.append(Issue("warning", "layer", "god-city %s is on %s, not Divine City Labels" % (t, m.layer_name(z)),
                             _xy(l["position"])))
        elif z == DIVINE_LAYER and t not in GOD_CITIES:
            out.append(Issue("warning", "layer", "%s is on Divine City Labels but isn't one of the thirteen god-cities"
                             % t, _xy(l["position"])))
    # Overlaps, per exported view (a pair only matters where both are shown).
    live = [(l, label_box(l)) for l in m.labels if not stamps.is_marker(l)]
    seen = {}
    for i, (a, ba) in enumerate(live):
        for b, bb in live[i + 1:]:
            w = min(ba[2], bb[2]) - max(ba[0], bb[0])
            h = min(ba[3], bb[3]) - max(ba[1], bb[1])
            if w <= 0 or h <= 0:
                continue
            small = min((ba[2] - ba[0]) * (ba[3] - ba[1]), (bb[2] - bb[0]) * (bb[3] - bb[1]))
            if w * h < 0.15 * small:
                continue
            shown_in = [v for v, hide in views.items()
                        if a.get("z_index") not in hide and b.get("z_index") not in hide]
            if shown_in:
                seen[(id(a), id(b))] = Issue("warning", "overlap", "labels %r and %r overlap (%s)"
                                             % (_txt(a), _txt(b), ", ".join(shown_in)), _xy(a["position"]))
    return out + list(seen.values())


def check_symbols(m):
    wet = [s for s in m.symbols if s.get("type") in ("tree", "mountain") and s.get("z_index") != 5
           and not m.is_land(*s["position"])]
    return [Issue("info", "water", "%s %s standing in water" % (s["type"], family(s["texture"]).rsplit("/", 1)[-1]),
                  _xy(s["position"])) for s in wet]


def run(m, views):
    """All checks; views = {view name: set of hidden label layers}."""
    issues = (check_outlines(m) + check_shapes(m) + check_capitols(m) + check_labels(m, views)
              + check_symbols(m))
    order = {"error": 0, "warning": 1, "info": 2}
    return sorted(issues, key=lambda i: (order[i.level], i.kind, i.at))
