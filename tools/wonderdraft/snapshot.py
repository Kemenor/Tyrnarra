"""A readable, diffable text snapshot of a Wonderdraft map, for git history.

The .wonderdraft_map itself is a ~100 MB compressed binary (over GitHub's file limit,
and undiffable), so the repo tracks this instead: every label, every region shape,
every settlement-type symbol, symbol counts per layer and art family, the scale bar
and the layer names. Deterministic: the same map always gives the same bytes, one
item per line, so `git diff` shows exactly what changed ("Tvisol added", "+105
kapoks"). It does not restore a map; Proton Drive and the wdmap backups do that.
"""
import collections
import json
import os

from wdmap import HERE, family

DEFAULT_PATH = os.path.join(HERE, "map-snapshot.json")


def _hex(c):
    return "#%02x%02x%02x" % tuple(round(max(0, min(1, v)) * 255) for v in c[:3])


def _xy(p):
    return [round(p[0]), round(p[1])]


def build(m):
    layer_names = {z: m.layer_name(z) for z in range(5, -6, -1)}
    labels = sorted(
        ({"layer": layer_names.get(l.get("z_index", 0), str(l.get("z_index"))),
          "text": " ".join(l["text"].split()), "at": _xy(l["position"]),
          "font": l.get("font"), "size": l.get("size")} for l in m.labels),
        key=lambda d: (-int(d["layer"].split()[0].replace("Default", "0")), d["text"].lower(), d["at"]))
    regions = sorted(
        ({"kind": r.kind, "name": r.name, "bbox": [round(v) for v in r.bbox], "area": round(r.area),
          "color": _hex(r.data.get("color") or (0, 0, 0))} for r in m.regions),
        key=lambda d: (d["kind"], (d["name"] or "~").lower(), d["bbox"]))
    # Settlements, castles, markers: the icon-type symbols, few enough to list one by one.
    icons = sorted(
        ({"layer": layer_names.get(s.get("z_index", 0), str(s.get("z_index"))), "art": os.path.basename(family(s.get("texture"))),
          "at": _xy(s["position"])} for s in m.symbols if s.get("type") == "symbol"),
        key=lambda d: (d["layer"], d["art"].lower(), d["at"]))
    counts = collections.defaultdict(collections.Counter)
    for s in m.symbols:
        counts[layer_names.get(s.get("z_index", 0), str(s.get("z_index")))][family(s.get("texture"))] += 1
    sc = m.data.get("scale") or {}
    scale = None
    if sc:
        total = sc.get("segments", 0) * sc.get("segment_distance", 0)
        width = (sc.get("size") or (0, 0))[0]
        scale = {"reads": "%g %s" % (total, sc.get("units", "")), "segments": sc.get("segments"),
                 "per_segment": sc.get("segment_distance"), "bar_map_units": round(width),
                 "per_map_unit": round(total / width, 4) if width else None}
    return {
        "map": os.path.basename(m.path or ""),
        "size": [m.width, m.height],
        "layers": {("%+d" % z if z else "0"): n for z, n in m.layer_names().items()},
        "scale": scale,
        "totals": {"labels": len(m.labels), "symbols": len(m.symbols),
                   "regions": dict(sorted(collections.Counter(r.kind for r in m.regions).items()))},
        "labels": labels,
        "regions": regions,
        "icons": icons,
        "symbol_counts": {layer: dict(sorted(c.items())) for layer, c in sorted(counts.items())},
    }


def dumps(snap):
    """JSON with one list item or count per line, so diffs are line-per-change."""
    out = ["{"]
    keys = list(snap)
    for n, key in enumerate(keys):
        val = snap[key]
        comma = "," if n < len(keys) - 1 else ""
        if isinstance(val, list) and val and isinstance(val[0], dict):
            out.append(" %s: [" % json.dumps(key))
            out += ["  %s%s" % (json.dumps(v, ensure_ascii=False), "," if i < len(val) - 1 else "")
                    for i, v in enumerate(val)]
            out.append(" ]" + comma)
        elif key == "symbol_counts":
            out.append(" %s: {" % json.dumps(key))
            layers = list(val)
            for i, layer in enumerate(layers):
                fams = val[layer]
                out.append("  %s: {" % json.dumps(layer))
                out += ["   %s: %d%s" % (json.dumps(f, ensure_ascii=False), c, "," if j < len(fams) - 1 else "")
                        for j, (f, c) in enumerate(fams.items())]
                out.append("  }" + ("," if i < len(layers) - 1 else ""))
            out.append(" }" + comma)
        else:
            out.append(" %s: %s%s" % (json.dumps(key), json.dumps(val, ensure_ascii=False), comma))
    out.append("}")
    return "\n".join(out) + "\n"


def write(m, path):
    """Write the snapshot; returns (path, changed) where changed is False if it was already current."""
    text = dumps(build(m))
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
    if old != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    return path, old != text
