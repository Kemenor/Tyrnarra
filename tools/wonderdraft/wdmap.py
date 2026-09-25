"""Wonderdraft map model: load a .wonderdraft_map into plain Python data, query it, save it.

    m = WDMap.load(path)
    m.symbols / m.labels / m.regions     # lists of dicts, edited in place
    m.save(path)                         # re-encodes; unchanged data is byte-identical
    m.save_in_place()                    # back up, check Wonderdraft/disk, overwrite m.path

Coordinates are map units (Main: 8192 x 8192). Layers are z_index: Default = 0,
"+1" = 1, "-1" = -1; the layer names the user set in Wonderdraft live in
m.data["layers"]["names"], listed from +5 down to -5.
"""
import fnmatch
import glob
import os
import re
import shutil
import struct
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import gdvar  # noqa: E402
from gdvar import Vector2  # noqa: E402

GCPF_SRC = os.path.join(HERE, "gcpf.c")
GCPF = os.path.join(HERE, "gcpf")
USER_DIR = os.path.expanduser("~/.local/share/Wonderdraft")
BACKUP_DIR = os.path.expanduser("~/.local/share/wdmap/backups")
KEEP_BACKUPS = 20
BORDER_KIND = {"border_dash": "domain", "border_gradient": "region"}
# The label layer that names each kind of region shape.
NAME_LAYER = {"domain": 1, "region": 2}
_NUM_SUFFIX = re.compile(r"[_ ]?\d+$")
_VEC2 = re.compile(r"Vector2\(\s*([-\d.e]+),\s*([-\d.e]+)\s*\)")


def ensure_codec():
    """Build the gcpf codec from source when missing or stale (the binary is gitignored)."""
    if os.path.exists(GCPF) and os.path.getmtime(GCPF) >= os.path.getmtime(GCPF_SRC):
        return
    cc = next((c for c in ("cc", "gcc", "clang") if shutil.which(c)), None)
    if not cc:
        sys.exit("need a C compiler to build %s" % GCPF_SRC)
    print("building gcpf codec with %s..." % cc, file=sys.stderr)
    subprocess.run([cc, "-O2", "-o", GCPF, GCPF_SRC], check=True)


def read_raw(path):
    ensure_codec()
    r = subprocess.run([GCPF, "d", path], stdout=subprocess.PIPE)
    if r.returncode:
        raise IOError("could not read %s" % path)
    return r.stdout


def write_raw(path, raw):
    ensure_codec()
    tmp = path + ".tmp"
    if subprocess.run([GCPF, "c", tmp], input=raw).returncode:
        raise IOError("could not write %s" % path)
    os.replace(tmp, path)


def wonderdraft_has_open(path):
    """True if a running Wonderdraft may have this map open (then saving would race it).

    Wonderdraft titles its window "<map name> - Wonderdraft". When Wonderdraft runs
    but the titles can't be read, assume the worst.
    """
    running = False
    for cmd in glob.glob("/proc/[0-9]*/cmdline"):
        try:
            with open(cmd, "rb") as f:
                argv0 = f.read().split(b"\0", 1)[0]
            if os.path.basename(argv0) == b"Wonderdraft.x86_64":
                running = True
                break
        except OSError:
            pass
    if not running:
        return False
    stem = os.path.splitext(os.path.basename(path))[0]
    try:
        out = subprocess.run(["xdotool", "search", "--name", " - Wonderdraft$", "getwindowname", "%@"],
                             capture_output=True, text=True, timeout=5,
                             env=dict(os.environ, DISPLAY=os.environ.get("DISPLAY", ":0")))
    except (OSError, subprocess.TimeoutExpired):
        return True
    titles = [t[:-len(" - Wonderdraft")].strip("* ") for t in out.stdout.splitlines()
              if t.endswith(" - Wonderdraft")]
    return not titles or stem in titles


def backups(path):
    """Backups of a map, newest first."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return sorted(glob.glob(os.path.join(BACKUP_DIR, stem, "*.wonderdraft_map")), reverse=True)


def backup(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    d = os.path.join(BACKUP_DIR, stem)
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, time.strftime("%Y-%m-%d_%H%M%S") + ".wonderdraft_map")
    shutil.copy2(path, dst)
    for old in backups(path)[KEEP_BACKUPS:]:
        os.remove(old)
    return dst


def family(texture):
    """Art family of a symbol texture: the path without its trailing variant number."""
    return _NUM_SUFFIX.sub("", texture or "")


def parse_points(s):
    return [(float(x), float(y)) for x, y in _VEC2.findall(s or "")]


def point_in_poly(x, y, pts):
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


class Region:
    """A region shape (Wonderdraft "territory") with its polygon and inferred name."""

    def __init__(self, index, data):
        self.index, self.data = index, data
        style = (data.get("style") or "").rsplit("/", 1)[-1]
        self.kind = BORDER_KIND.get(style, style)
        ox, oy = data.get("position") or (0.0, 0.0)
        self.points = [(x + ox, y + oy) for x, y in parse_points(data.get("points"))]
        xs = [p[0] for p in self.points] or [0]
        ys = [p[1] for p in self.points] or [0]
        self.bbox = (min(xs), min(ys), max(xs), max(ys))
        self.name = None

    def contains(self, x, y):
        x0, y0, x1, y1 = self.bbox
        return x0 <= x <= x1 and y0 <= y <= y1 and point_in_poly(x, y, self.points)

    @property
    def area(self):
        p = self.points
        return abs(sum(p[i - 1][0] * p[i][1] - p[i][0] * p[i - 1][1] for i in range(len(p)))) / 2

    @property
    def label(self):
        return self.name or "unnamed %s #%d" % (self.kind, self.index)


class WDMap:
    def __init__(self, data, path=None):
        self.data, self.path = data, path
        self._regions = None
        self._mask = None
        self._stat = self._file_stat()

    def _file_stat(self):
        try:
            st = os.stat(self.path)
            return (st.st_mtime_ns, st.st_size)
        except (OSError, TypeError):
            return None

    def invalidate(self):
        """Drop caches derived from the data (region names, land mask) after edits."""
        self._regions = None
        self._mask = None

    # --- load / save -------------------------------------------------------

    @classmethod
    def load(cls, path):
        raw = read_raw(path)
        (length,) = struct.unpack_from("<I", raw, 0)
        data, end = gdvar.decode(raw, 4)
        if end != 4 + length or not isinstance(data, dict):
            raise ValueError("%s: unexpected map layout" % path)
        return cls(data, os.path.abspath(path))

    def to_raw(self):
        body = gdvar.encode(self.data)
        return struct.pack("<I", len(body)) + body

    def save(self, path):
        write_raw(path, self.to_raw())

    def save_in_place(self, force=False):
        """Overwrite the map it was loaded from, after backing it up. Returns the backup path.

        Refuses when Wonderdraft may have the map open (its next save would wipe
        these edits) or when the file changed on disk since it was loaded.
        """
        if not force and wonderdraft_has_open(self.path):
            raise RuntimeError("Wonderdraft has %s open; save and close it there first"
                               % os.path.basename(self.path))
        if self._file_stat() != self._stat:
            raise RuntimeError("%s changed on disk since it was loaded; reload and redo the edit"
                               % os.path.basename(self.path))
        raw = self.to_raw()
        dst = backup(self.path)
        write_raw(self.path, raw)
        self._stat = self._file_stat()
        return dst

    # --- basic accessors ---------------------------------------------------

    @property
    def width(self):
        return self.data["map_width"]

    @property
    def height(self):
        return self.data["map_height"]

    @property
    def symbols(self):
        return self.data["symbols"]

    @property
    def labels(self):
        return self.data["labels"]

    @property
    def territories(self):
        return self.data["territories"]["territories"]

    def layer_names(self):
        """{z_index: display name}, e.g. {1: "God Labels", 0: "Terrain", -1: "City Labels"}."""
        names = self.data.get("layers", {}).get("names") or []
        return {5 - i: n for i, n in enumerate(names)}

    def layer_name(self, z):
        n = self.layer_names().get(z)
        tag = "Default" if z == 0 else "%+d" % z
        return "%s (%s)" % (tag, n) if n and n not in (tag, "Default") else tag

    def resolve_layer(self, spec):
        """Layer by number ("+1", "-1", "0", "default") or by its Wonderdraft name."""
        s = str(spec).strip()
        if s.lower() == "default":
            return 0
        try:
            return int(s)
        except ValueError:
            pass
        for z, n in self.layer_names().items():
            if n.lower() == s.lower():
                return z
        raise ValueError("unknown layer %r" % spec)

    # --- regions -----------------------------------------------------------

    @property
    def regions(self):
        if self._regions is None:
            regs = [Region(i, t) for i, t in enumerate(self.territories)]
            for r in regs:
                want = NAME_LAYER.get(r.kind)
                inside = [l for l in self.labels
                          if r.contains(*l["position"]) and (want is None or l["z_index"] == want)]
                if inside:
                    r.name = " ".join(max(inside, key=lambda l: l["size"])["text"].split())
            # A god domain is one colour across all its pieces, so unlabelled
            # islands inherit the name. Region colours are reused, so only domains.
            by_colour = {}
            for r in regs:
                if r.kind == "domain":
                    by_colour.setdefault(tuple(r.data.get("color") or ()), []).append(r)
            for group in by_colour.values():
                names = {r.name for r in group if r.name}
                if len(names) == 1:
                    for r in group:
                        r.name = r.name or next(iter(names))
            self._regions = regs
        return self._regions

    def find_regions(self, pattern):
        pat = pattern.lower()
        hits = [r for r in self.regions if r.name and fnmatch.fnmatch(r.name.lower(), pat)]
        if not hits:
            raise ValueError("no region named %r" % pattern)
        return hits

    # --- land / water ------------------------------------------------------

    def is_land(self, x, y):
        """True where the landmass mask is set (alpha channel of the mask image)."""
        if self._mask is None:
            img = self.data["mask"].get("data")
            self._mask = (img["data"], img["width"], img["height"])
        buf, w, h = self._mask
        px = int(x * w / self.width)
        py = int(y * h / self.height)
        if not (0 <= px < w and 0 <= py < h):
            return False
        return buf[(py * w + px) * 4 + 3] >= 128

    def ground_sample(self, x, y):
        """The ground colour Wonderdraft stores as a symbol's `sample`: the ground
        image's pixel under the symbol, as a Color."""
        img = self.data["ground"].get("data")
        w, h = img["width"], img["height"]
        px = min(w - 1, max(0, int(x * w / self.width)))
        py = min(h - 1, max(0, int(y * h / self.height)))
        o = (py * w + px) * 4
        return gdvar.Color(*(v / 255 for v in img["data"][o:o + 4]))

    def image(self, name):
        """One of the terrain images (mask, ground, water_tint) as a PIL RGBA image."""
        from PIL import Image
        img = self.data[name].get("data")
        return Image.frombuffer("RGBA", (img["width"], img["height"]), img["data"], "raw", "RGBA", 0, 1)

    # --- assets ------------------------------------------------------------

    @staticmethod
    def asset_file(texture):
        """Local file for a user-pack texture (user://...), or None for built-in (res://) art."""
        if not texture or not texture.startswith("user://"):
            return None
        base = os.path.join(USER_DIR, texture[len("user://"):])
        for ext in (".png", ".webp", ".jpg"):
            if os.path.exists(base + ext):
                return base + ext
        return None


# --- selection ---------------------------------------------------------------

KINDS = ("symbols", "labels", "regions")


def select(m, kind, texture=None, family_=None, type_=None, layer=None, text=None,
           region=None, rect=None, near=None, on=None, style=None):
    """Return [(index, item)] of `kind` matching every given filter.

    texture/family_/text/region are case-insensitive globs; layer is a list of
    z_index values; rect is (x0, y0, x1, y1); near is (x, y, radius); on is
    "land" or "water"; style is "domain"/"region" (regions only).
    """
    if kind == "regions":
        items = [(r.index, r) for r in m.regions]
        pos = None
    else:
        items = list(enumerate(m.symbols if kind == "symbols" else m.labels))

        def pos(it):
            return it["position"]

    regs = [r for pat in (region or []) for r in m.find_regions(pat)] if region else None
    out = []
    for i, it in items:
        if kind == "regions":
            if style and it.kind != style:
                continue
            if text and not (it.name and fnmatch.fnmatch(it.name.lower(), text.lower())):
                continue
            if layer is not None and it.data.get("z_index") not in layer:
                continue
            cx = (it.bbox[0] + it.bbox[2]) / 2
            cy = (it.bbox[1] + it.bbox[3]) / 2
            x, y = cx, cy
        else:
            if layer is not None and it.get("z_index") not in layer:
                continue
            if kind == "symbols":
                tex = (it.get("texture") or "").lower()
                if texture and not fnmatch.fnmatch(tex, texture.lower()):
                    continue
                if family_ and not fnmatch.fnmatch(family(tex), family_.lower()):
                    continue
                if type_ and it.get("type") != type_:
                    continue
            elif text and not fnmatch.fnmatch(" ".join((it.get("text") or "").split()).lower(), text.lower()):
                continue
            x, y = pos(it)
        if rect and not (rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]):
            continue
        if near and (x - near[0]) ** 2 + (y - near[1]) ** 2 > near[2] ** 2:
            continue
        if regs is not None and kind != "regions" and not any(r.contains(x, y) for r in regs):
            continue
        if regs is not None and kind == "regions" and it not in regs:
            continue
        if on and (m.is_land(x, y) != (on == "land")):
            continue
        out.append((i, it))
    return out


def label_anchor(m, text, radius):
    """(x, y, radius) around the first label whose text matches the glob."""
    for l in m.labels:
        if fnmatch.fnmatch(" ".join(l["text"].split()).lower(), text.lower()):
            x, y = l["position"]
            return (x, y, radius)
    raise ValueError("no label matching %r" % text)
