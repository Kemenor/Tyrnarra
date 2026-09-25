"""MCP server exposing the Wonderdraft map tooling (wdmap) to Claude.

Every tool runs the same code as the `wdmap` command line, so behaviour, safety
checks (backup before save, refuse while Wonderdraft has the map open, refuse if
the file changed on disk) and messages are identical. The map is loaded fresh for
each call and released afterwards: a decoded 8192px map takes ~3 GB, too much
to keep resident.

Started by tools/wonderdraft/mcp-server.sh, registered in the repo's .mcp.json.
"""
import contextlib
import gc
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)

from mcp.server.mcpserver import Image, MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

import wd  # noqa: E402

DEFAULT_MAP = os.environ.get("WD_MAP", os.path.expanduser("~/ProtonDrive/Wonderdraft/Main.wonderdraft_map"))
READ = ToolAnnotations(readOnlyHint=True)
WRITE = ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=False)

server = MCPServer(
    name="wonderdraft",
    instructions=(
        "Tools for reading and editing Wonderdraft (.wonderdraft_map) fantasy maps for the Tyrnarra "
        "setting. `map` defaults to the master map (%s). Coordinates are map units (8192x8192 on Main). "
        "Layers are numbers (+1, 0 = Default, -1) or the map's own layer names (God Labels, Region "
        "Labels, Divine City Labels, City Icons, City Labels, Terrain, Legend). Region shapes: 'domain' "
        "= god domain (dashed border), 'region' = region (gradient border), named after the label "
        "inside them. Look before and after changing things: use query and preview. Write tools save "
        "in place after a backup; pass dry_run=true to only report, preview=true to get an image of "
        "the changed area. Saving fails while Wonderdraft has the map open: ask the user to save and "
        "close it there. New symbols need art already used somewhere in the map. See "
        "tools/wonderdraft/README.md." % DEFAULT_MAP
    ),
)


def _run(argv, image_path=None):
    """Run a wdmap command, returning its printed output (and the image it wrote, if any)."""
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            wd.run(argv)
    except SystemExit as e:
        if isinstance(e.code, str):  # sys.exit("message"); argparse exits with a number after printing
            out.write(("\n" if out.getvalue() else "") + e.code)
    except Exception as e:  # report instead of killing the server
        out.write("\nerror: %s: %s" % (type(e).__name__, e))
    finally:
        gc.collect()
    text = out.getvalue().strip() or "(no output)"
    if image_path and os.path.exists(image_path):
        # JPEG: the same picture for the model at a fraction of the PNG's size.
        from PIL import Image as PILImage
        buf = io.BytesIO()
        with PILImage.open(image_path) as im:
            im.convert("RGB").save(buf, "JPEG", quality=85)
        os.remove(image_path)
        text = "\n".join(l for l in text.splitlines() if not l.startswith(("preview: ", image_path)))
        return [text or "(preview)", Image(data=buf.getvalue(), format="jpeg")]
    return text


def _png():
    fd, path = tempfile.mkstemp(suffix=".png", prefix="wdmap-")
    os.close(fd)
    os.remove(path)
    return path


def _filters(f):
    """Filter dict -> CLI args. Keys: texture, family, type, layer, text, region, rect, near, on, style."""
    argv = []
    for key, val in (f or {}).items():
        if val in (None, "", []):
            continue
        # Unknown keys pass through, so the command's own "unrecognized arguments" error names them.
        for v in (val if isinstance(val, list) else [val]):
            argv += ["--" + key, str(v)]
    return argv


def _write_opts(dry_run, preview, force=False):
    argv, img = [], None
    if dry_run:
        argv.append("--dry-run")
    if force:
        argv.append("--force")
    if preview:
        img = _png()
        argv += ["--preview", img]
    return argv, img


FILTER_DOC = (
    "filters: object with any of texture (glob on the art path, e.g. '*hatch_pine*'), family (glob on "
    "the art family = path without variant number), type (tree|mountain|symbol), layer (number or layer "
    "name; string or list), text (glob on label text / region name), region (inside a named region or "
    "god domain; string or list of globs), rect ('X0,Y0,X1,Y1'), near ('LABEL:RADIUS'), on (land|water), "
    "style (domain|region, regions only). All given filters must match."
)


# --- looking ---------------------------------------------------------------------

@server.tool(annotations=READ)
def map_info(map: str = DEFAULT_MAP) -> str:
    """Overview of a map: size, symbol/label/region counts per layer (with the map's layer names),
    built-in vs pack art, packs in use."""
    return _run(["info", map])


@server.tool(annotations=READ, description="Find symbols, labels or regions and summarise them (counts by art "
             "family / layer / type), optionally listing the first `list` matches with index and position. "
             + FILTER_DOC)
def query(kind: str, filters: dict | None = None, list: int = 20, map: str = DEFAULT_MAP) -> str:
    return _run(["query", map, kind] + _filters(filters) + ["--list", str(list)])


@server.tool(annotations=READ, description="Render an approximate preview PNG of the map or an area: real painted "
             "terrain, region shapes, pack icons in their real art, built-in icons as markers by type, labels "
             "in the map fonts. area: 'X0,Y0,X1,Y1', 'region:NAME' or 'label:TEXT:RADIUS'. grid: coordinate "
             "grid spacing in map units (useful for picking coordinates). Matches of `filters` (for `kind`) "
             "are highlighted in red. " + FILTER_DOC)
def preview(area: str | None = None, width: int = 1600, grid: float | None = None, kind: str | None = None,
            filters: dict | None = None, map: str = DEFAULT_MAP):
    img = _png()
    argv = ["preview", map, "-o", img, "--width", str(width)]
    if area:
        argv += ["--area", area]
    if grid:
        argv += ["--grid", str(grid)]
    if kind:
        argv += ["--kind", kind]
    return _run(argv + _filters(filters), image_path=img)


# --- changing ----------------------------------------------------------------------

@server.tool(annotations=WRITE, description="Edit what `filters` selects (kind = symbols|labels|regions; filters "
             "are required unless all=true). actions (object), by kind: all kinds: move 'DX,DY', delete true; "
             "symbols: scale, rotate (deg), to_layer, art (texture or art family already used in the map; "
             "keeps each symbol's footprint); labels: scale, rotate, to_layer, set_text, replace [OLD, NEW], "
             "font, size, color '#rrggbb'; regions: color, border_style (domain|region), border_width. "
             + FILTER_DOC)
def edit(kind: str, actions: dict, filters: dict | None = None, all: bool = False, dry_run: bool = False,
         preview: bool = True, map: str = DEFAULT_MAP):
    argv = ["edit", map, kind] + _filters(filters)
    if all:
        argv.append("--all")
    for key, val in (actions or {}).items():
        flag = "--" + key.replace("_", "-")
        if val is True:
            argv.append(flag)
        elif isinstance(val, (list, tuple)):
            argv += [flag] + [str(v) for v in val]
        elif val not in (None, False):
            argv += [flag, str(val)]
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


@server.tool(annotations=WRITE)
def add_symbol(art: str, at: str | None = None, under: str | None = None, offset: str | None = None,
               scale: float | None = None, layer: str | None = None, dry_run: bool = False,
               preview: bool = True, map: str = DEFAULT_MAP):
    """Place one symbol. art: texture or art family already used in the map. Position: at 'X,Y' or
    under a label (glob), plus offset 'DX,DY'. Defaults: the art's typical scale and layer."""
    argv = ["add", map, "symbol", "--art", art]
    for flag, val in (("--at", at), ("--under", under), ("--offset", offset), ("--scale", scale),
                      ("--to-layer", layer)):
        if val is not None:
            argv += [flag, str(val)]
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


@server.tool(annotations=WRITE)
def add_label(text: str, at: str | None = None, under: str | None = None, offset: str | None = None,
              like: str | None = None, layer: str | None = None, size: int | None = None,
              dry_run: bool = False, preview: bool = True, map: str = DEFAULT_MAP):
    """Place one label. Style is copied from `like` (a label text glob) or the first label on `layer`.
    Position: at 'X,Y' or under a label, plus offset 'DX,DY'. Use a newline in text for two lines."""
    argv = ["add", map, "label", "--text", text]
    for flag, val in (("--at", at), ("--under", under), ("--offset", offset), ("--like", like),
                      ("--to-layer", layer), ("--size", size)):
        if val is not None:
            argv += [flag, str(val)]
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


@server.tool(annotations=WRITE)
def scatter(art: str, region: list[str] | None = None, rect: str | None = None, count: int | None = None,
            density: float | None = None, spacing: float | None = None, on: str = "land",
            avoid_existing: bool = True, scale: float | None = None, layer: str | None = None,
            seed: int | None = None, dry_run: bool = False, preview: bool = True, map: str = DEFAULT_MAP):
    """Fill named regions/god domains (region: list of names or globs) or rect 'X0,Y0,X1,Y1' with random,
    non-overlapping placements of an art family, on land by default, clear of existing symbols and
    label text. Without count/density it fills as far as spacing allows (density = per 1000x1000
    units). Use dry_run first and look at the preview."""
    argv = ["scatter", map, "--art", art, "--on", on]
    for r in region or []:
        argv += ["--region", r]
    for flag, val in (("--rect", rect), ("--count", count), ("--density", density), ("--spacing", spacing),
                      ("--scale", scale), ("--to-layer", layer), ("--seed", seed)):
        if val is not None:
            argv += [flag, str(val)]
    if not avoid_existing:
        argv.append("--no-avoid")
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


@server.tool(annotations=WRITE)
def along(art: str, path: str | None = None, from_label: str | None = None, to_label: str | None = None,
          spacing: float | None = None, jitter: float = 0.0, scale: float | None = None,
          layer: str | None = None, seed: int | None = None, dry_run: bool = False, preview: bool = True,
          map: str = DEFAULT_MAP):
    """Place art every `spacing` units along path 'X,Y X,Y ...' or from one label to another,
    pushed sideways by up to `jitter` (a ridge of mountains, a tree line, a chain of towers)."""
    argv = ["along", map, "--art", art, "--jitter", str(jitter)]
    for flag, val in (("--path", path), ("--from", from_label), ("--to", to_label), ("--spacing", spacing),
                      ("--scale", scale), ("--to-layer", layer), ("--seed", seed)):
        if val is not None:
            argv += [flag, str(val)]
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


# --- stamps ------------------------------------------------------------------------

@server.tool(annotations=READ)
def stamp_list() -> str:
    """List saved stamps (tools/wonderdraft/stamps/) with their contents."""
    return _run(["stamp", "list"])


@server.tool(annotations=WRITE)
def stamp_capture(name: str, at: str | None = None, near: str | None = None, radius: float = 250.0,
                  overwrite: bool = False, map: str = DEFAULT_MAP) -> str:
    """Save every symbol and label within `radius` of at 'X,Y' or of a label (near) as stamp `name`.
    Labels in the radius are included, so keep it tight. Does not change the map."""
    argv = ["stamp", "capture", map, name, "--radius", str(radius)]
    if at:
        argv += ["--at", at]
    if near:
        argv += ["--near", near]
    if overwrite:
        argv.append("--overwrite")
    return _run(argv)


@server.tool(annotations=WRITE)
def stamp_place(name: str, at: str | None = None, under: str | None = None, offset: str | None = None,
                rotate: float = 0.0, scale: float = 1.0, dry_run: bool = False, preview: bool = True,
                map: str = DEFAULT_MAP):
    """Place stamp `name` at 'X,Y' or under every label matching `under`, plus offset. rotate turns the
    arrangement (icons and text stay upright); scale resizes it."""
    argv = ["stamp", "place", map, name, "--rotate", str(rotate), "--scale", str(scale)]
    for flag, val in (("--at", at), ("--under", under), ("--offset", offset)):
        if val is not None:
            argv += [flag, str(val)]
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


@server.tool(annotations=WRITE)
def process_markers(overwrite: bool = False, dry_run: bool = False, preview: bool = True,
                    map: str = DEFAULT_MAP):
    """Run the user's marker labels on layer -5: '@stamp NAME [RADIUS]' captures, then
    '@place NAME [DEG] [SCALE]' places; the markers are removed."""
    argv = ["markers", map] + (["--overwrite"] if overwrite else [])
    opts, img = _write_opts(dry_run, preview)
    return _run(argv + opts, image_path=img)


# --- safety net and exports ----------------------------------------------------------

@server.tool(annotations=READ)
def backups(map: str = DEFAULT_MAP) -> str:
    """List the automatic backups of a map, newest (0) first."""
    return _run(["backups", map])


@server.tool(annotations=WRITE)
def restore(backup: int = 0, map: str = DEFAULT_MAP) -> str:
    """Put backup N (0 = newest) back as the map; the current version is backed up first.
    Only on the user's request."""
    return _run(["restore", map, "--backup", str(backup)])


@server.tool(annotations=WRITE)
def split_variants(map: str = DEFAULT_MAP) -> str:
    """Write the export variants next to the map: '<map> - God Domains', '- Regions', '- Terrain'
    (wd_regions.py). The user then exports each from Wonderdraft."""
    r = subprocess.run([sys.executable, os.path.join(HERE, "wd_regions.py"), map],
                       capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


if __name__ == "__main__":
    server.run("stdio")
