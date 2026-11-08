#!/usr/bin/env python3
"""Turn map-area-editor exports into the clickable-battlemap markup of a GM page.

    python3 tools/map_areas_html.py published/gm-notes/<campaign>/<quest>/<page>.html [...]

A page marks where a map goes and where the area notes go:

    <!-- map: /gm-notes/short-notice/quest-the-unspent/maps/unspent-l3 -->
    <!-- /map -->
    ...
    <!-- map-areas -->
    <!-- /map-areas -->

Each `map:` block is filled with the map image, one hotspot per piece (rectangles as
`.map-hot` buttons, polygons in an `svg.map-poly`), the hide-areas toggle and the
detail panel; the `map-areas` block with the `window.GM_MAP_AREAS` notes for every
map on the page, keyed `<map name>-<area number>`. The areas come from
`published<path>.areas.json`, the image from that file's `image` field. Rerun after
editing areas in the editor; everything between the markers is rewritten.
"""
import html
import json
import re
import sys
from pathlib import Path

PUBLISHED = Path(__file__).resolve().parent.parent / "published"
MAP_RE = re.compile(r"(<!-- map: (\S+) -->)(.*?)(<!-- /map -->)", re.S)
AREAS_RE = re.compile(r"(<!-- map-areas -->)(.*?)(<!-- /map-areas -->)", re.S)


def pct(n):
    return f"{n:g}%"


def map_block(path, notes):
    data = json.loads((PUBLISHED / (path.lstrip("/") + ".areas.json")).read_text())
    name = path.rstrip("/").split("/")[-1]
    image = str(Path(path).parent / data["image"])
    out = [f'<div class="map-wrap">',
           f'  <img src="{image}" alt="{html.escape(name)} battlemap (downsized reference)">']
    polys, nums = [], []
    for i, area in enumerate(data["areas"], 1):
        key = f"{name}-{i}"
        label = area.get("label", "").strip() or f"Area {i}"
        desc = area.get("desc", "").strip()
        paras = "".join(f"<p>{html.escape(p.strip())}</p>" for p in re.split(r"\n\s*\n", desc) if p.strip())
        notes[key] = {"n": f"{i} · {label}", "t": paras or "<p></p>"}
        numbered = False
        for r in area.get("rects", []):
            badge = f'<span class="hot-num">{i}</span>' if not numbered else ""
            numbered = True
            out.append(f'  <button class="map-hot" data-area="{key}" style="left:{pct(r["left"])};top:{pct(r["top"])};'
                       f'width:{pct(r["width"])};height:{pct(r["height"])}">{badge}</button>')
        for p in area.get("polys", []):
            polys.append(f'    <polygon class="map-hot" data-area="{key}" points="{" ".join(f"{x:g},{y:g}" for x, y in p)}"/>')
            if not numbered:
                numbered = True
                cx = sum(x for x, _ in p) / len(p)
                cy = sum(y for _, y in p) / len(p)
                nums.append(f'  <span class="map-num" style="left:{cx:.1f}%;top:{cy:.1f}%"><span class="hot-num">{i}</span></span>')
    if polys:
        out.append('  <svg class="map-poly" viewBox="0 0 100 100" preserveAspectRatio="none">')
        out += polys
        out.append("  </svg>")
    out += nums
    out.append("</div>")
    out.append('<button class="map-toggle" type="button">Hide areas</button>')
    out.append('<div class="map-detail"><div class="map-detail-empty">Select a numbered area on the map above.</div></div>')
    return "\n".join(out)


def build(page):
    text = page.read_text()
    notes = {}
    text = MAP_RE.sub(lambda m: f"{m.group(1)}\n{map_block(m.group(2), notes)}\n{m.group(4)}", text)
    script = ("<script>\nwindow.GM_MAP_AREAS = "
              + json.dumps(notes, indent=1, ensure_ascii=False).replace("</", "<\\/") + ";\n</script>")
    text, n = AREAS_RE.subn(lambda m: f"{m.group(1)}\n{script}\n{m.group(3)}", text)
    if notes and not n:
        sys.exit(f"{page}: has maps but no <!-- map-areas --> block")
    page.write_text(text)
    print(f"{page}: {len(notes)} areas")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        build(Path(p))
