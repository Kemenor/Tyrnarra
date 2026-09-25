#!/usr/bin/env python3
"""Inspect and edit Wonderdraft maps: info, query, preview, edit, add, scatter, along, stamps.

    wdmap info    MAP
    wdmap query   MAP {symbols,labels,regions} [filters] [--list N] [--json]
    wdmap preview MAP -o OUT.png [--area ...] [--grid N] [filters to highlight]
    wdmap edit    MAP {symbols,labels,regions} [filters | --all] ACTIONS [--dry-run] [--preview OUT.png]
    wdmap backups MAP
    wdmap restore MAP [--backup N]
    wdmap add     MAP symbol --art ART (--at X,Y | --under LABEL) [--offset DX,DY] [--scale K] [--to-layer L]
    wdmap add     MAP label --text T (--at X,Y | --under LABEL) [--offset DX,DY] [--like LABEL] [--to-layer L] [--size N]
    wdmap add     MAP region (--at X,Y | --under LABEL) --color #rrggbb [--kind region|domain]
                  (copies the outline of the smallest shape there, e.g. an island's domain outline)
    wdmap scatter MAP --art ART (--region NAME | --rect X0,Y0,X1,Y1) [--count N | --density D] [--spacing S]
    wdmap along   MAP --art ART (--path "X,Y X,Y ..." | --from LABEL --to LABEL) [--spacing S] [--jitter J]
    wdmap stamp list
    wdmap stamp capture MAP NAME (--at X,Y | --near LABEL) [--radius R] [--overwrite]
    wdmap stamp place   MAP NAME (--at X,Y | --under LABEL) [--rotate DEG] [--scale K]
    wdmap markers MAP        (runs @stamp / @place marker labels on layer -5)
    wdmap snapshot MAP [-o PATH]   (readable text snapshot for git: tools/wonderdraft/map-snapshot.json)
    wdmap check   MAP [--level error|warning|info] [--json]   (consistency checks, see check.py)

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

Every command that changes a map saves in place: it backs the map up first
(~/.local/share/wdmap/backups), refuses while Wonderdraft has the map open, and
refuses if the file changed on disk since it was read. --dry-run reports without
saving; --preview OUT.png renders the changed area with the changes highlighted.
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import edit  # noqa: E402
import place  # noqa: E402
import stamps  # noqa: E402
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
    check_writable(m, a)
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
    if a.delete:
        hl, pts = {}, [(it.bbox[0], it.bbox[1]) if a.kind == "regions" else it["position"] for _, it in hits]
    else:
        hl = {a.kind: [i for i, _ in hits]}
        pts = ([p for _, it in hits for p in (it.bbox[:2], it.bbox[2:])] if a.kind == "regions"
               else [it["position"] for _, it in hits])
    finish(m, a, lines, hl, pts)


def check_writable(m, a):
    """Refuse early (before any work) when the save would be refused anyway."""
    if not (a.dry_run or a.force) and wonderdraft_has_open(m.path):
        sys.exit("not saved: Wonderdraft has %s open; save and close it there first (or use --dry-run)"
                 % os.path.basename(m.path))


def finish(m, a, lines, hl, pts):
    """Report, optionally preview the changed area, then save in place (unless --dry-run)."""
    for line in lines:
        print("  " + line)
    if a.preview and pts:
        import preview
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


def anchor(m, a):
    """--at X,Y or --under LABEL, plus --offset."""
    if getattr(a, "at", None):
        x, y = _xy(a.at)
    elif getattr(a, "under", None):
        x, y, _ = label_anchor(m, a.under, 0)
    else:
        sys.exit("error: give --at X,Y or --under LABEL")
    dx, dy = _xy(a.offset) if getattr(a, "offset", None) else (0.0, 0.0)
    return x + dx, y + dy


def cmd_add(m, a):
    check_writable(m, a)
    x, y = anchor(m, a)
    layer = m.resolve_layer(a.to_layer) if a.to_layer is not None else None
    if a.what == "region":
        if not a.color:
            sys.exit("error: add region needs --color")
        i, src = place.copy_shape(m, x, y, a.color, kind=a.kind)
        r = m.regions[i]
        finish(m, a, ["added %s shape %s (outline copied from %s, %d points, area %d)" % (
            a.kind, r.label, src.label, len(r.points), r.area)], {"regions": [i]},
            [r.bbox[:2], r.bbox[2:]])
        return
    if a.what == "symbol":
        if not a.art:
            sys.exit("error: add symbol needs --art")
        idx = place.add_symbols(m, a.art, [(x, y)], scale=a.scale, layer=layer, mirror=False)
        s = m.symbols[idx[0]]
        finish(m, a, ["added %s at (%d, %d) layer %s" % (s["texture"], x, y, m.layer_name(s["z_index"]))],
               {"symbols": idx}, [(x, y)])
    else:
        if not a.text:
            sys.exit("error: add label needs --text")
        i = place.add_label(m, a.text, x, y, like=a.like, layer=layer, size=a.size)
        l = m.labels[i]
        finish(m, a, ["added label %r at (%d, %d) layer %s, %s %s" % (
            a.text, x, y, m.layer_name(l["z_index"]), l["font"], l["size"])], {"labels": [i]}, [(x, y)])


def cmd_scatter(m, a):
    check_writable(m, a)
    targets, _ = edit.art_targets(m, a.art)
    tpl = next(iter(targets.values()))
    scale = a.scale if a.scale is not None else place._typical_scale(m, tpl["texture"])
    spacing = a.spacing or (tpl.get("radius") or 30) * scale * 1.2
    if a.region:
        regs = [r for pat in a.region for r in m.find_regions(pat)]
        bbox = (min(r.bbox[0] for r in regs), min(r.bbox[1] for r in regs),
                max(r.bbox[2] for r in regs), max(r.bbox[3] for r in regs))
        contains = lambda x, y: any(r.contains(x, y) for r in regs)  # noqa: E731
        area = sum(r.area for r in regs)
        where = "in " + ", ".join(sorted({r.label for r in regs}))
    elif a.rect:
        bbox = tuple(float(v) for v in a.rect.split(","))
        contains = lambda x, y: True  # noqa: E731
        area = None
        where = "in rect %s" % a.rect
    else:
        sys.exit("error: scatter needs --region or --rect")
    on = None if a.on == "any" else a.on
    pts, wanted = place.scatter_points(m, contains, bbox, spacing, count=a.count, density=a.density,
                                       on=on, avoid=not a.no_avoid, seed=a.seed, area_hint=area)
    layer = m.resolve_layer(a.to_layer) if a.to_layer is not None else None
    idx = place.add_symbols(m, a.art, pts, scale=scale, layer=layer, seed=a.seed, jitter_scale=a.jitter_scale)
    lines = ["scattered %d x %s %s (spacing %g, scale %g)" % (len(idx), a.art, where, spacing, scale)]
    if len(pts) < wanted and (a.count or a.density):
        lines.append("note: asked for %d, only %d fit (spacing, land/water and existing symbols limit it)"
                     % (wanted, len(pts)))
    finish(m, a, lines, {"symbols": idx}, pts)


def cmd_along(m, a):
    check_writable(m, a)
    if a.path:
        path = [_xy(p) for p in a.path.split()]
    elif a.from_ and a.to:
        path = [label_anchor(m, a.from_, 0)[:2], label_anchor(m, a.to, 0)[:2]]
    else:
        sys.exit("error: along needs --path or --from/--to")
    targets, _ = edit.art_targets(m, a.art)
    tpl = next(iter(targets.values()))
    scale = a.scale if a.scale is not None else place._typical_scale(m, tpl["texture"])
    spacing = a.spacing or (tpl.get("radius") or 30) * scale * 2
    pts = place.path_points(path, spacing, jitter=a.jitter, seed=a.seed)
    layer = m.resolve_layer(a.to_layer) if a.to_layer is not None else None
    idx = place.add_symbols(m, a.art, pts, scale=scale, layer=layer, seed=a.seed)
    finish(m, a, ["placed %d x %s along a %d-point path (spacing %g)" % (len(idx), a.art, len(path), spacing)],
           {"symbols": idx}, pts + path)


def cmd_stamp(a):
    if a.action == "list":
        for st in stamps.list_stamps():
            print("  %-24s %4d symbols %3d labels  radius %g  from %s, %s" % (
                st["name"], len(st["symbols"]), len(st["labels"]), st["radius"], st["source"], st["captured"]))
        return
    if not a.map or not a.name:
        sys.exit("error: stamp %s needs MAP and NAME" % a.action)
    m = WDMap.load(a.map)
    if a.action == "capture":
        if a.near:
            x, y, _ = label_anchor(m, a.near, 0)
        elif a.at:
            x, y = _xy(a.at)
        else:
            sys.exit("error: give --at X,Y or --near LABEL")
        line, _ = stamps.capture(m, a.name, x, y, a.radius, overwrite=a.overwrite)
        print("  " + line)
        return
    check_writable(m, a)
    st = stamps.load_stamp(a.name)
    if a.under:
        import fnmatch
        spots = [tuple(l["position"]) for l in m.labels
                 if fnmatch.fnmatch(" ".join(l["text"].split()).lower(), a.under.lower())]
        if not spots:
            sys.exit("error: no label matching %r" % a.under)
    elif a.at:
        spots = [_xy(a.at)]
    else:
        sys.exit("error: give --at X,Y or --under LABEL")
    dx, dy = _xy(a.offset) if a.offset else (0.0, 0.0)
    lines, hs, hl_ = [], [], []
    for x, y in spots:
        line, si, li = stamps.place(m, st, x + dx, y + dy, a.rotate, a.stamp_scale)
        lines.append(line)
        hs += si
        hl_ += li
    finish(m, a, lines, {"symbols": hs, "labels": hl_}, [(x + dx, y + dy) for x, y in spots])


def cmd_check(m, a):
    import check
    from wd_regions import VARIANTS
    views = {name: set(spec["hide_label_layers"]) for name, spec in VARIANTS.items()}
    levels = {"error": 0, "warning": 1, "info": 2}
    issues = [i for i in check.run(m, views) if levels[i.level] <= levels[a.level]]
    if a.json:
        print(json.dumps([i._asdict() for i in issues], indent=1))
    else:
        if not issues:
            print("no issues at level %s or above" % a.level)
        kind = None
        for i in issues:
            if (i.level, i.kind) != kind:
                kind = (i.level, i.kind)
                n = sum(1 for j in issues if (j.level, j.kind) == kind)
                print("%s: %s (%d)" % (i.level.upper(), i.kind, n))
            print("  (%5d, %5d)  %s" % (i.at[0], i.at[1], i.message))
    if any(i.level == "error" for i in issues):
        sys.exit(1)


def cmd_snapshot(m, a):
    import snapshot
    path, changed = snapshot.write(m, a.output or snapshot.DEFAULT_PATH)
    print("%s %s" % ("updated" if changed else "unchanged:", path))


def cmd_markers(m, a):
    check_writable(m, a)
    lines, hs, hl_ = stamps.process_markers(m, overwrite=a.overwrite, write=not a.dry_run)
    if not lines:
        print("no @stamp/@place marker labels on layer -5")
        return
    pts = [m.symbols[i]["position"] for i in hs] + [m.labels[i]["position"] for i in hl_]
    finish(m, a, lines, {"symbols": hs, "labels": hl_}, pts)


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


def add_write_opts(p):
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--preview", metavar="OUT.png")
    p.add_argument("--force", action="store_true", help="skip the Wonderdraft-has-it-open check")


def build_parser():
    ap = argparse.ArgumentParser(prog="wdmap", description=__doc__.split("\n\n")[0],
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
    add_write_opts(p)
    p = sub.add_parser("add")
    p.add_argument("map")
    p.add_argument("what", choices=("symbol", "label", "region"))
    p.add_argument("--color", help="region: fill colour #rrggbb")
    p.add_argument("--kind", default="region", choices=("region", "domain"), help="region: border style")
    p.add_argument("--art")
    p.add_argument("--text")
    p.add_argument("--at", metavar="X,Y")
    p.add_argument("--under", metavar="LABEL", help="at the position of the label matching this")
    p.add_argument("--offset", metavar="DX,DY")
    p.add_argument("--like", metavar="LABEL", help="copy the style of this label (default: first label on the layer)")
    p.add_argument("--scale", type=float)
    p.add_argument("--size", type=int)
    p.add_argument("--to-layer")
    add_write_opts(p)
    p = sub.add_parser("scatter")
    p.add_argument("map")
    p.add_argument("--art", required=True)
    p.add_argument("--region", action="append")
    p.add_argument("--rect")
    p.add_argument("--count", type=int)
    p.add_argument("--density", type=float, help="symbols per 1000x1000 map units (default: fill to --spacing)")
    p.add_argument("--spacing", type=float, help="minimum distance (default: from the art's footprint)")
    p.add_argument("--on", choices=("land", "water", "any"), default="land")
    p.add_argument("--no-avoid", action="store_true", help="allow overlapping existing symbols")
    p.add_argument("--scale", type=float, help="default: the art's typical scale in this map")
    p.add_argument("--jitter-scale", type=float, default=0.1)
    p.add_argument("--to-layer")
    p.add_argument("--seed", type=int)
    add_write_opts(p)
    p = sub.add_parser("along")
    p.add_argument("map")
    p.add_argument("--art", required=True)
    p.add_argument("--path", help='"X,Y X,Y ..."')
    p.add_argument("--from", dest="from_", metavar="LABEL")
    p.add_argument("--to", metavar="LABEL")
    p.add_argument("--spacing", type=float)
    p.add_argument("--jitter", type=float, default=0.0)
    p.add_argument("--scale", type=float)
    p.add_argument("--to-layer")
    p.add_argument("--seed", type=int)
    add_write_opts(p)
    p = sub.add_parser("stamp")
    p.add_argument("action", choices=("list", "capture", "place"))
    p.add_argument("map", nargs="?")
    p.add_argument("name", nargs="?")
    p.add_argument("--at", metavar="X,Y")
    p.add_argument("--near", metavar="LABEL", help="capture around this label")
    p.add_argument("--under", metavar="LABEL", help="place at every label matching this")
    p.add_argument("--offset", metavar="DX,DY")
    p.add_argument("--radius", type=float, default=stamps.DEFAULT_RADIUS)
    p.add_argument("--rotate", type=float, default=0.0)
    p.add_argument("--scale", dest="stamp_scale", type=float, default=1.0)
    p.add_argument("--overwrite", action="store_true")
    add_write_opts(p)
    p = sub.add_parser("markers")
    p.add_argument("map")
    p.add_argument("--overwrite", action="store_true", help="let @stamp markers replace existing stamps")
    add_write_opts(p)
    p = sub.add_parser("check")
    p.add_argument("map")
    p.add_argument("--level", choices=("error", "warning", "info"), default="info",
                   help="lowest severity to show (default info = everything)")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("snapshot")
    p.add_argument("map")
    p.add_argument("-o", "--output", help="default: tools/wonderdraft/map-snapshot.json")
    p = sub.add_parser("backups")
    p.add_argument("map")
    p = sub.add_parser("restore")
    p.add_argument("map")
    p.add_argument("--backup", type=int, default=0, help="which backup (0 = newest, see `wdmap backups`)")
    p.add_argument("--force", action="store_true")
    return ap


def run(argv=None):
    """Parse and run one wdmap command (argv without the program name)."""
    a = build_parser().parse_args(argv)
    try:
        if a.cmd == "backups":
            return cmd_backups(a.map)
        if a.cmd == "restore":
            return cmd_restore(os.path.abspath(a.map), a.backup, a.force)
        if a.cmd == "stamp":
            return cmd_stamp(a)
        m = WDMap.load(a.map)
        {"info": cmd_info, "query": cmd_query, "preview": cmd_preview, "edit": cmd_edit, "add": cmd_add,
         "scatter": cmd_scatter, "along": cmd_along, "markers": cmd_markers,
         "snapshot": cmd_snapshot, "check": cmd_check}[a.cmd](m, a)
    except ValueError as e:
        sys.exit("error: %s" % e)


def main():
    run()


if __name__ == "__main__":
    main()
