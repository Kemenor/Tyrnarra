#!/usr/bin/env python3
"""Inspect Wonderdraft maps: info, query, preview.

    wdmap info    MAP
    wdmap query   MAP {symbols,labels,regions} [filters] [--list N] [--json]
    wdmap preview MAP -o OUT.png [--area ...] [--grid N] [filters to highlight]

Filters (all optional, combined with AND; globs are case-insensitive):
    --texture GLOB   symbol texture path, e.g. '*hatch_pine*'
    --family GLOB    symbol art family (texture minus variant number)
    --type T         symbol type: tree, mountain, symbol
    --layer L        layer number (+1, -1, 0) or Wonderdraft layer name; repeatable
    --text GLOB      label text / region name
    --region GLOB    inside a named region or god domain; repeatable
    --rect X0,Y0,X1,Y1
    --near LABEL:R   within R map units of the label matching LABEL
    --on land|water
    --style domain|region   (regions only)
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
from wdmap import WDMap, family, label_anchor, select  # noqa: E402


def add_filters(ap):
    ap.add_argument("--texture")
    ap.add_argument("--family")
    ap.add_argument("--type")
    ap.add_argument("--layer", action="append")
    ap.add_argument("--text")
    ap.add_argument("--region", action="append")
    ap.add_argument("--rect")
    ap.add_argument("--near")
    ap.add_argument("--on", choices=("land", "water"))
    ap.add_argument("--style", choices=("domain", "region"))


def has_filters(a):
    return any(getattr(a, k) for k in
               ("texture", "family", "type", "layer", "text", "region", "rect", "near", "on", "style"))


def run_select(m, kind, a):
    rect = tuple(float(v) for v in a.rect.split(",")) if a.rect else None
    near = None
    if a.near:
        txt, _, r = a.near.rpartition(":")
        near = label_anchor(m, txt, float(r))
    layer = [m.resolve_layer(l) for l in a.layer] if a.layer else None
    return select(m, kind, texture=a.texture, family_=a.family, type_=a.type, layer=layer,
                  text=a.text, region=a.region, rect=rect, near=near, on=a.on, style=a.style)


def fmt_xy(p):
    return "(%d, %d)" % (round(p[0]), round(p[1]))


def cmd_info(m, a):
    syms, labels = m.symbols, m.labels
    info = {
        "file": m.path,
        "size": [m.width, m.height],
        "symbols": len(syms),
        "labels": len(labels),
        "regions": collections.Counter(r.kind for r in m.regions),
        "layers": {m.layer_name(z): {"symbols": sum(1 for s in syms if s.get("z_index") == z),
                                     "labels": sum(1 for l in labels if l.get("z_index") == z)}
                   for z in range(5, -6, -1)},
        "art": {"built-in": sum(1 for s in syms if (s.get("texture") or "").startswith("res://")),
                "user packs": sum(1 for s in syms if (s.get("texture") or "").startswith("user://"))},
        "packs": m.data.get("included_packs"),
    }
    if a.json:
        print(json.dumps(info, indent=2, default=dict))
        return
    print("%s  %dx%d" % (m.path, m.width, m.height))
    print("symbols %d (built-in art %d, user packs %d), labels %d, regions %s"
          % (len(syms), info["art"]["built-in"], info["art"]["user packs"], len(labels),
             ", ".join("%d %ss" % (n, k) for k, n in info["regions"].items())))
    print("layers:")
    for name, c in info["layers"].items():
        if c["symbols"] or c["labels"] or "(" in name:
            print("  %-28s %6d symbols %4d labels" % (name, c["symbols"], c["labels"]))
    print("packs: %s" % ", ".join(info["packs"] or []))


def summarize(m, kind, hits):
    if kind == "symbols":
        return {
            "by_family": collections.Counter(family(s.get("texture")) for _, s in hits).most_common(),
            "by_layer": collections.Counter(m.layer_name(s.get("z_index", 0)) for _, s in hits).most_common(),
            "by_type": collections.Counter(s.get("type") for _, s in hits).most_common(),
        }
    if kind == "labels":
        return {"by_layer": collections.Counter(m.layer_name(l.get("z_index", 0)) for _, l in hits).most_common(),
                "by_font": collections.Counter(l.get("font") for _, l in hits).most_common()}
    return {"by_kind": collections.Counter(r.kind for _, r in hits).most_common()}


def item_row(m, kind, i, it):
    if kind == "symbols":
        return {"index": i, "texture": it.get("texture"), "type": it.get("type"),
                "layer": it.get("z_index"), "position": [round(v, 1) for v in it["position"]],
                "scale": round((it.get("scale") or (1, 1))[0], 3)}
    if kind == "labels":
        return {"index": i, "text": " ".join(it["text"].split()), "layer": it.get("z_index"), "font": it.get("font"),
                "size": it.get("size"), "position": [round(v, 1) for v in it["position"]]}
    return {"index": i, "name": it.name, "kind": it.kind, "points": len(it.points),
            "bbox": [round(v) for v in it.bbox], "area": round(it.area)}


def cmd_query(m, a):
    hits = run_select(m, a.kind, a)
    if a.kind == "regions" and not a.list:
        a.list = len(hits)
    rows = [item_row(m, a.kind, i, it) for i, it in hits[:a.list or 0]]
    if a.json:
        print(json.dumps({"count": len(hits), "summary": summarize(m, a.kind, hits), "items": rows}, indent=1))
        return
    print("%d %s" % (len(hits), a.kind))
    for key, pairs in summarize(m, a.kind, hits).items():
        print("  %s:" % key.replace("_", " "))
        for k, n in pairs[:15]:
            print("    %6d  %s" % (n, k))
        if len(pairs) > 15:
            print("    ... %d more" % (len(pairs) - 15))
    for r in rows:
        if a.kind == "symbols":
            print("  #%-6d %-60s %s layer %+d" % (r["index"], r["texture"], fmt_xy(r["position"]), r["layer"]))
        elif a.kind == "labels":
            print("  #%-4d %-28s %s layer %+d size %s" % (r["index"], r["text"], fmt_xy(r["position"]), r["layer"], r["size"]))
        else:
            print("  #%-4d %-30s %-7s area %d bbox %s" % (r["index"], r["name"] or "-", r["kind"], r["area"], r["bbox"]))


def parse_area(m, spec):
    if not spec:
        return None
    if spec.startswith("region:"):
        regs = m.find_regions(spec[len("region:"):])
        x0 = min(r.bbox[0] for r in regs)
        y0 = min(r.bbox[1] for r in regs)
        x1 = max(r.bbox[2] for r in regs)
        y1 = max(r.bbox[3] for r in regs)
        pad = 0.05 * max(x1 - x0, y1 - y0)
        return (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    if spec.startswith("label:"):
        txt, _, r = spec[len("label:"):].rpartition(":")
        x, y, rad = label_anchor(m, txt, float(r))
        return (x - rad, y - rad, x + rad, y + rad)
    x0, y0, x1, y1 = (float(v) for v in spec.split(","))
    return (x0, y0, x1, y1)


def cmd_preview(m, a):
    import preview
    hl = {}
    if has_filters(a):
        kinds = [a.kind] if a.kind else ["symbols", "labels", "regions"]
        if not a.kind:
            # Filters that only make sense for one kind pick it.
            if a.texture or a.family or a.type:
                kinds = ["symbols"]
            elif a.style:
                kinds = ["regions"]
        for kind in kinds:
            hl[kind] = [i for i, _ in run_select(m, kind, a)]
    img = preview.render(m, area=parse_area(m, a.area), width=a.width, highlight=hl, grid=a.grid)
    img.save(a.output)
    print("%s (%dx%d)%s" % (a.output, img.width, img.height,
                           "".join(", %d %s highlighted" % (len(v), k) for k, v in hl.items())))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("info")
    p.add_argument("map")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("query")
    p.add_argument("map")
    p.add_argument("kind", choices=("symbols", "labels", "regions"))
    add_filters(p)
    p.add_argument("--list", type=int, default=0, help="also list the first N matches")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("preview")
    p.add_argument("map")
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--area", help="X0,Y0,X1,Y1 | region:NAME | label:TEXT:RADIUS")
    p.add_argument("--width", type=int, default=2048)
    p.add_argument("--grid", type=float, help="coordinate grid spacing in map units")
    p.add_argument("--kind", choices=("symbols", "labels", "regions"), help="what the filters highlight")
    add_filters(p)
    a = ap.parse_args()
    try:
        m = WDMap.load(a.map)
        {"info": cmd_info, "query": cmd_query, "preview": cmd_preview}[a.cmd](m, a)
    except ValueError as e:
        sys.exit("error: %s" % e)


if __name__ == "__main__":
    main()
