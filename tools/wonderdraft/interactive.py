"""Data for the interactive map page (published/setting/talan/interactive-map.html).

The page shows Wonderdraft's "Base" export (terrain, trees, mountains, city icons; no
region shapes, no labels except the legend) as zoomable tiles, and draws region and
domain shapes and the name labels on top as SVG from map-data.json, so each can be
switched on and off. This module writes both:

    write_tiles(base_image, out_dir)   Leaflet tile pyramid tiles/{z}/{x}/{y}.webp
    build_data(m, site_root)           shapes + labels + page links -> dict for map-data.json

Region and domain shapes link to their site page when one can be found (see
resolve_links); tools/wonderdraft/map-links.json overrides or blocks a match.
"""
import html
import json
import os
import re
import shutil

TILE = 256
TILE_QUALITY = 82
# Label layers the page can switch; the legend (+5) is baked into the Base export.
LABEL_GROUPS = {1: "god", 2: "region", 3: "divine", -1: "city", -2: "landmark"}
LINKS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map-links.json")


def _hex(c):
    return "#%02x%02x%02x" % tuple(round(max(0, min(1, v)) * 255) for v in c[:3])


def write_tiles(image_path, out_dir, log=print):
    """Cut an image into a Leaflet CRS.Simple tile pyramid; zoom z has 2^z x 2^z tiles."""
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(image_path).convert("RGB")
    size = im.width
    max_z = max(0, (size // TILE).bit_length() - 1)
    tmp = out_dir + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    count = 0
    for z in range(max_z + 1):
        n = 2 ** z
        level = im if n * TILE == size else im.resize((n * TILE, n * TILE), Image.LANCZOS)
        for x in range(n):
            os.makedirs(os.path.join(tmp, str(z), str(x)), exist_ok=True)
            for y in range(n):
                tile = level.crop((x * TILE, y * TILE, (x + 1) * TILE, (y + 1) * TILE))
                tile.save(os.path.join(tmp, str(z), str(x), "%d.webp" % y), "WEBP", quality=TILE_QUALITY)
                count += 1
    shutil.rmtree(out_dir, ignore_errors=True)
    os.replace(tmp, out_dir)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(out_dir) for f in fs)
    log("  tiles: %d (zoom 0-%d) in %s, %.1f MB" % (count, max_z, os.path.basename(out_dir), total / 1e6))
    return max_z


# --- page links --------------------------------------------------------------------

def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")


def _lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def site_pages(site_root):
    """[(url, stem, title, is_domain_page)] for every page under setting/talan/domains/."""
    base = os.path.join(site_root, "setting", "talan", "domains")
    pages = []
    for dp, _, files in os.walk(base):
        for f in files:
            if not f.endswith(".html") or f == "domains.html":
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, site_root).replace(os.sep, "/")
            stem = f[:-5]
            parts = os.path.relpath(path, base).split(os.sep)
            with open(path, encoding="utf-8") as fh:
                head = fh.read(4000)
            t = re.search(r"<title>(.*?)</title>", head, re.S)
            title = html.unescape(t.group(1)).split("·")[0].strip() if t else stem
            is_domain = len(parts) == 2 and parts[0] == stem
            # A region's main page: file named like its folder, or a page directly in the domain folder.
            is_main = is_domain or (len(parts) == 3 and parts[1] == stem) or len(parts) == 2
            pages.append(("/" + rel, stem, title, is_domain, is_main))
    return pages


def resolve_link(name, kind, pages, overrides):
    """Best page for a region/domain name: exact slug or title, a slug the name starts with
    ("Kaosadaemi Principality" -> kaosadaemi), or one letter off (a misspelt label still finds its page)."""
    if not name:
        return None
    if name in overrides:
        return overrides[name]
    want = [p for p in pages if (p[3] if kind == "domain" else (p[4] and not p[3]))]
    s = _slug(name)
    s_nothe = s[4:] if s.startswith("the-") else s
    for test in (lambda p: p[1] in (s, s_nothe) or _slug(p[2]) in (s, s_nothe),
                 lambda p: s.startswith(p[1] + "-") or s_nothe.startswith(p[1] + "-"),
                 lambda p: len(s) >= 6 and _lev(s, p[1]) <= 1):
        hits = [p for p in want if test(p)]
        if len(hits) == 1:
            return hits[0][0]
    return None


def load_overrides():
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, encoding="utf-8") as f:
            return {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    return {}


# --- data --------------------------------------------------------------------------

def build_data(m, site_root, max_zoom):
    pages = site_pages(site_root)
    overrides = load_overrides()
    shapes = []
    domain_of = {}
    for r in m.regions:
        if r.kind == "domain":
            domain_of[r.index] = r.name
    for r in sorted(m.regions, key=lambda r: (r.kind != "domain", -r.area)):
        if r.kind not in ("domain", "region") or len(r.points) < 3:
            continue
        cx, cy = (r.bbox[0] + r.bbox[2]) / 2, (r.bbox[1] + r.bbox[3]) / 2
        dom = None
        if r.kind == "region":
            dom = next((d.name for d in m.regions if d.kind == "domain" and d.contains(cx, cy)), None)
        shapes.append({
            "kind": r.kind, "name": r.name, "domain": dom,
            "href": resolve_link(r.name, r.kind, pages, overrides),
            "color": _hex(r.data["color"]), "alpha": round(r.data["color"][3], 3),
            "opacity": r.data.get("opacity", 0.25), "width": r.data.get("width", 10),
            "smoothing": r.data.get("smoothing", 0.2),
            "points": [[round(x, 1), round(y, 1)] for x, y in r.points],
        })
    labels = []
    for l in m.labels:
        group = LABEL_GROUPS.get(l.get("z_index"))
        if not group:
            continue
        labels.append({
            "group": group, "text": l["text"], "x": round(l["position"][0], 1), "y": round(l["position"][1], 1),
            "font": l.get("font"), "size": l.get("size"), "color": _hex(l.get("color") or (0, 0, 0, 1)),
            "outline": l.get("outline_size") or 0, "outline_color": _hex(l.get("outline_color") or (1, 1, 1, 1)),
            "rotation": round(l.get("rotation") or 0.0, 4),
        })
    layer_names = {("%+d" % z if z else "0"): n for z, n in m.layer_names().items()}
    return {"size": [m.width, m.height], "tile": TILE, "max_zoom": max_zoom, "layers": layer_names,
            "shapes": shapes, "labels": labels}


def write_data(m, site_root, out_path, max_zoom, log=print):
    data = build_data(m, site_root, max_zoom)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    named = [s for s in data["shapes"] if s["name"]]
    linked = [s for s in named if s["href"]]
    log("  map data: %d shapes (%d linked to a page), %d labels, %.0f KB"
        % (len(data["shapes"]), len(linked), len(data["labels"]), os.path.getsize(out_path) / 1e3))
    missing = sorted({"%s %s" % (s["kind"], s["name"]) for s in named if not s["href"]})
    if missing:
        log("  no page for: " + ", ".join(missing))
    return data
