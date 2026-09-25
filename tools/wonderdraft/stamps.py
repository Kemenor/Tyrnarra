"""Stamps: reusable groups of symbols and labels, stored as JSON in tools/wonderdraft/stamps/.

A stamp keeps every captured item with its position relative to the stamp's anchor,
so placing it is plain arithmetic: rotate/scale the offsets around the new anchor.

Markers let you do this from inside Wonderdraft: put a label on layer -5 reading
    @stamp NAME [RADIUS]         capture everything within RADIUS (default 250) of it
    @place NAME [DEG] [SCALE]    place stamp NAME here; DEG turns the arrangement
                                 (icons and text stay upright), SCALE resizes it
save, close Wonderdraft, run `wdmap markers MAP`. Captures run before placements,
and the marker labels are removed.
"""
import copy
import json
import math
import os
import re
import time

import gdvar
from wdmap import HERE

STAMP_DIR = os.path.join(HERE, "stamps")
MARKER_LAYER = -5
DEFAULT_RADIUS = 250.0
_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


# --- JSON with Godot types ------------------------------------------------------

def to_json(v):
    if isinstance(v, gdvar._Fixed):
        return {"$" + type(v).__name__: list(v)}
    if isinstance(v, dict):
        return {k: to_json(x) for k, x in v.items()}
    if isinstance(v, list):
        return [to_json(x) for x in v]
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    raise TypeError("can't store %r in a stamp" % type(v))


def from_json(v):
    if isinstance(v, dict):
        if len(v) == 1:
            (k, x), = v.items()
            if k.startswith("$") and hasattr(gdvar, k[1:]):
                return getattr(gdvar, k[1:])(x)
        return {k: from_json(x) for k, x in v.items()}
    if isinstance(v, list):
        return [from_json(x) for x in v]
    return v


def stamp_path(name):
    if not _NAME.match(name):
        raise ValueError("stamp names use letters, digits, - _ . (got %r)" % name)
    return os.path.join(STAMP_DIR, name + ".json")


def list_stamps():
    if not os.path.isdir(STAMP_DIR):
        return []
    out = []
    for f in sorted(os.listdir(STAMP_DIR)):
        if f.endswith(".json"):
            with open(os.path.join(STAMP_DIR, f)) as fh:
                d = json.load(fh)
            out.append(d)
    return out


def load_stamp(name):
    p = stamp_path(name)
    if not os.path.exists(p):
        raise ValueError("no stamp %r (see `wdmap stamp list`)" % name)
    with open(p) as f:
        return json.load(f)


# --- capture / place ------------------------------------------------------------

def is_marker(label):
    return label.get("z_index") == MARKER_LAYER and label["text"].lstrip().startswith("@")


def capture(m, name, x, y, radius, overwrite=False, write=True):
    """Collect every symbol and label (markers excluded) within `radius` of (x, y) as stamp
    `name`, saved to stamps/ unless write=False. Returns (report line, stamp)."""
    p = stamp_path(name)
    if write and os.path.exists(p) and not overwrite:
        raise ValueError("stamp %r exists; pass --overwrite to replace it" % name)
    r2 = radius * radius

    def rel(item):
        d = copy.deepcopy(item)
        d["position"] = gdvar.Vector2(item["position"][0] - x, item["position"][1] - y)
        return to_json(d)

    syms = [rel(s) for s in m.symbols
            if (s["position"][0] - x) ** 2 + (s["position"][1] - y) ** 2 <= r2]
    labs = [rel(l) for l in m.labels
            if not is_marker(l) and (l["position"][0] - x) ** 2 + (l["position"][1] - y) ** 2 <= r2]
    if not syms and not labs:
        raise ValueError("nothing within %g of (%g, %g) to capture" % (radius, x, y))
    stamp = {"name": name, "radius": radius, "source": os.path.basename(m.path or ""),
             "captured": time.strftime("%Y-%m-%d"), "symbols": syms, "labels": labs}
    if write:
        os.makedirs(STAMP_DIR, exist_ok=True)
        with open(p, "w") as f:
            json.dump(stamp, f, indent=1)
            f.write("\n")
    return ("captured stamp %s: %d symbols, %d labels within %g of (%d, %d) -> %s" % (
        name, len(syms), len(labs), radius, x, y,
        os.path.relpath(p, os.path.join(HERE, "..", "..")) if write else "not written (dry run)"), stamp)


def place(m, stamp, x, y, rotate=0.0, scale=1.0):
    """Place a loaded stamp with its anchor at (x, y). Returns (line, new symbol idx, new label idx)."""
    a = math.radians(rotate)
    ca, sa = math.cos(a), math.sin(a)

    def at(item):
        # Rotation turns the arrangement; icons and text stay upright as on any map.
        d = from_json(item)
        dx, dy = d["position"]
        d["position"] = gdvar.Vector2(x + (dx * ca - dy * sa) * scale, y + (dx * sa + dy * ca) * scale)
        return d

    s0, l0 = len(m.symbols), len(m.labels)
    for item in stamp["symbols"]:
        s = at(item)
        if scale != 1.0:
            s["scale"] = gdvar.Vector2(s["scale"][0] * scale, s["scale"][1] * scale)
        if s.get("sample") is not None:
            s["sample"] = m.ground_sample(*s["position"])
        m.symbols.append(s)
    for item in stamp["labels"]:
        l = at(item)
        if scale != 1.0:
            l["size"] = max(1, round(l["size"] * scale))
        m.labels.append(l)
    m.invalidate()
    line = "placed stamp %s at (%d, %d)%s%s: %d symbols, %d labels" % (
        stamp["name"], x, y, " rotated %g deg" % rotate if rotate else "",
        " scaled %g" % scale if scale != 1.0 else "", len(stamp["symbols"]), len(stamp["labels"]))
    return line, list(range(s0, len(m.symbols))), list(range(l0, len(m.labels)))


# --- markers --------------------------------------------------------------------

def process_markers(m, overwrite=False, write=True):
    """Run every @stamp then @place marker label on layer -5, then remove the markers.

    Returns (lines, new symbol indices, new label indices).
    """
    markers = [(i, l) for i, l in enumerate(m.labels) if is_marker(l)]
    lines, new_s, new_l = [], [], []
    caps = [(i, l, l["text"].split()) for i, l in markers if l["text"].split()[0] == "@stamp"]
    places = [(i, l, l["text"].split()) for i, l in markers if l["text"].split()[0] == "@place"]
    unknown = [l["text"] for i, l in markers if l["text"].split()[0] not in ("@stamp", "@place")]
    fresh = {}
    for _, l, w in caps:
        if len(w) < 2:
            raise ValueError("marker %r needs a stamp name" % l["text"])
        radius = float(w[2]) if len(w) > 2 else DEFAULT_RADIUS
        line, fresh[w[1]] = capture(m, w[1], *l["position"], radius, overwrite=overwrite, write=write)
        lines.append(line)
    placements = []
    for _, l, w in places:
        if len(w) < 2:
            raise ValueError("marker %r needs a stamp name" % l["text"])
        rot = float(w[2]) if len(w) > 2 else 0.0
        sc = float(w[3]) if len(w) > 3 else 1.0
        placements.append((fresh.get(w[1]) or load_stamp(w[1]), l["position"], rot, sc))
    # Drop the markers before placing, so new label indices stay valid.
    drop = {i for i, l in markers if l["text"].split()[0] in ("@stamp", "@place")}
    m.data["labels"] = [l for i, l in enumerate(m.labels) if i not in drop]
    for stamp, (x, y), rot, sc in placements:
        line, s_idx, l_idx = place(m, stamp, x, y, rot, sc)
        lines.append(line)
        new_s += s_idx
        new_l += l_idx
    if drop:
        lines.append("removed %d marker label%s" % (len(drop), "s" if len(drop) > 1 else ""))
    if unknown:
        lines.append("left alone (not @stamp/@place): %s" % ", ".join(unknown))
    m.invalidate()
    return lines, new_s, new_l
