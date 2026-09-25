#!/usr/bin/env python3
"""Inspect Wonderdraft maps: info, query, preview.

    wdmap info    MAP
    wdmap query   MAP {symbols,labels,regions} [filters] [--list N] [--json]
    wdmap preview MAP -o OUT.png [--area ...] [--grid N] [filters to highlight]
    wdmap edit    MAP {symbols,labels,regions} [filters | --all] ACTIONS [--dry-run] [--preview OUT.png]
    wdmap backups MAP
    wdmap restore MAP [--backup N]

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

Edit actions:
    all kinds    --move DX,DY  --delete
    symbols      --scale F  --rotate DEG  --to-layer L  --art TEXTURE_OR_FAMILY
    labels       --scale F  --rotate DEG  --to-layer L  --set-text T  --replace OLD NEW
                 --font NAME  --size N  --color #rrggbb
    regions      --color #rrggbb  --border-style domain|region  --border-width W

edit saves in place: it backs the map up first (~/.local/share/wdmap/backups),
refuses while Wonderdraft has the map open, and refuses if the file changed on
disk since it was read. --dry-run reports without saving.
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import edit  # noqa: E402
from wdmap import WDMap, backup, backups, family, label_anchor, select, wonderdraft_has_open  # noqa: E402


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


def _xy(spec):
    x, y = (float(v) for v in spec.split(","))
    return (x, y)


def cmd_edit(m, a):
    if not (has_filters(a) or a.all):
        sys.exit("error: give filters to select what to edit, or --all")
    if not (a.dry_run or a.force) and wonderdraft_has_open(m.path):
        sys.exit("not saved: Wonderdraft has %s open; save and close it there first (or use --dry-run)"
                 % os.path.basename(m.path))
    hits = run_select(m, a.kind, a)
    if not hits:
        print("nothing matched; no changes")
        return
    move = _xy(a.move) if a.move else None
    layer = m.resolve_layer(a.to_layer) if a.to_layer is not None else None
    if a.kind == "symbols":
        lines = edit.edit_symbols(m, hits, move=move, scale=a.scale, rotate=a.rotate, layer=layer,
                                  art=a.art, delete=a.delete)
    elif a.kind == "labels":
        lines = edit.edit_labels(m, hits, move=move, scale=a.scale, rotate=a.rotate, layer=layer,
                                 text=a.set_text, replace=a.replace, font=a.font, size=a.size,
                                 color=a.color, delete=a.delete)
    else:
        lines = edit.edit_regions(m, hits, move=move, color=a.color, style=a.border_style,
                                  width=a.border_width, delete=a.delete)
    if not lines:
        print("%d %s matched, but no actions given; no changes" % (len(hits), a.kind))
        return
    print("%d %s selected" % (len(hits), a.kind))
    for line in lines:
        print("  " + line)
    if a.preview:
        import preview
        if a.delete:
            hl, pts = {}, [(it.bbox[0], it.bbox[1]) if a.kind == "regions" else it["position"] for _, it in hits]
        else:
            hl = {a.kind: [i for i, _ in hits]}
            pts = ([p for _, it in hits for p in (it.bbox[:2], it.bbox[2:])] if a.kind == "regions"
                   else [it["position"] for _, it in hits])
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        pad = max(200, 0.1 * max(max(xs) - min(xs), max(ys) - min(ys)))
        area = (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
        preview.render(m, area=area, width=1600, highlight=hl).save(a.preview)
        print("preview: %s" % a.preview)
    if a.dry_run:
        print("dry run: not saved")
        return
    try:
        bak = m.save_in_place(force=a.force)
    except RuntimeError as e:
        sys.exit("not saved: %s" % e)
    print("saved %s (backup: %s)" % (m.path, bak))


def cmd_backups(path):
    for i, b in enumerate(backups(path)):
        print("%3d  %s  %.0f MB" % (i, os.path.basename(b), os.path.getsize(b) / 1e6))


def cmd_restore(path, n, force):
    import shutil
    bs = backups(path)
    if not bs or n >= len(bs):
        sys.exit("error: no backup #%d for %s" % (n, path))
    if not force and wonderdraft_has_open(path):
        sys.exit("not restored: Wonderdraft has %s open; close it there first" % os.path.basename(path))
    chosen = bs[n]
    safety = backup(path)
    shutil.copy2(chosen, path)
    print("restored %s from %s (the version it replaced is backed up as %s)"
          % (path, os.path.basename(chosen), os.path.basename(safety)))


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
    p = sub.add_parser("edit")
    p.add_argument("map")
    p.add_argument("kind", choices=("symbols", "labels", "regions"))
    add_filters(p)
    p.add_argument("--all", action="store_true", help="edit every item of the kind (no filters)")
    p.add_argument("--move", metavar="DX,DY")
    p.add_argument("--scale", type=float)
    p.add_argument("--rotate", type=float, metavar="DEG")
    p.add_argument("--to-layer")
    p.add_argument("--art", metavar="TEXTURE_OR_FAMILY")
    p.add_argument("--set-text")
    p.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"))
    p.add_argument("--font")
    p.add_argument("--size", type=int)
    p.add_argument("--color")
    p.add_argument("--border-style")
    p.add_argument("--border-width", type=float)
    p.add_argument("--delete", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--preview", metavar="OUT.png")
    p.add_argument("--force", action="store_true", help="skip the Wonderdraft-has-it-open check")
    p = sub.add_parser("backups")
    p.add_argument("map")
    p = sub.add_parser("restore")
    p.add_argument("map")
    p.add_argument("--backup", type=int, default=0, help="which backup (0 = newest, see `wdmap backups`)")
    p.add_argument("--force", action="store_true")
    a = ap.parse_args()
    try:
        if a.cmd == "backups":
            return cmd_backups(a.map)
        if a.cmd == "restore":
            return cmd_restore(os.path.abspath(a.map), a.backup, a.force)
        m = WDMap.load(a.map)
        {"info": cmd_info, "query": cmd_query, "preview": cmd_preview, "edit": cmd_edit}[a.cmd](m, a)
    except ValueError as e:
        sys.exit("error: %s" % e)


if __name__ == "__main__":
    main()
