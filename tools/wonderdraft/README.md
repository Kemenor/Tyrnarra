# Wonderdraft tooling

Tools for the Wonderdraft source maps behind the terrain / regions / domains views (see [`docs/map-todo.md`](../../docs/map-todo.md)). The `.wonderdraft_map` sources live on Proton Drive (`~/ProtonDrive/Wonderdraft/`), not in git.

## `wd_regions.py`: one map, one file per region type

Wonderdraft has a single regions overlay, so god domains and regions can't be shown separately and there are no region layers. This script takes the one master map that holds both and writes a copy per variant, ready to export:

| Variant | Region shapes kept | Label layers dropped |
|---|---|---|
| `<map> - God Domains` | dashed border (`border_dash`) | +2 (region labels), −1 (small city names), −2 (landmark names) |
| `<map> - Regions` | gradient border (`border_gradient`) | +1 (god domain labels) |
| `<map> - Terrain` | none | +1 (god domain labels), +2 (region labels) |

Everything else (terrain, symbols, +3 divine city names, +4 city icons, theme) is copied byte for byte. The input map is only read, never modified.

```bash
python3 tools/wonderdraft/wd_regions.py ~/ProtonDrive/Wonderdraft/Backup.wonderdraft_map
```

Outputs land next to the input (or in `-o <folder>`) and are overwritten on every run, so treat them as export-only: edit the master, rerun, export.

### Publishing the three map views

1. `wd-regions ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map` writes the three variants.
2. `wd-regions ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map --export` exports them (~1.5 min per view; hands off keyboard and mouse meanwhile). Or by hand: open each variant in Wonderdraft and export it next to its map file under the same name: `Main - Terrain.webp`, `Main - Regions.webp`, `Main - God Domains.webp` (WebP is copied as is; PNG/JPG are converted at quality 92, Wonderdraft's own WebP setting).
3. `wd-regions ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map --publish` copies them to `published/setting/assets/maps/` as `terrain.webp`, `regions.webp` and `domains.webp`, runs `resize.sh` for the `display/` and `thumbs/` variants, and refreshes `map-snapshot.json`. It refuses when an export is missing or older than its variant map (stale).
4. Review the maps page and commit; pushing deploys the site.

**`--export`** (`wd_export.py`) drives Wonderdraft itself, since it has no command-line export: for each view it launches Wonderdraft with the map, waits `--load-wait` seconds (default 15; Main loads in ~10 s), then sends Ctrl+E, Enter (Export Options, PNG), a file name and Enter (save dialog), waits for the PNG to stop growing (~40 s), closes Wonderdraft, converts the PNG to WebP at quality 92 and deletes it. `--only Regions` (repeatable) limits it to some views. Lessons baked in:

- **Keyboard only, no clicks:** clicking by screenshot coordinates missed under display scaling.
- **Focus is checked before every keystroke;** keys go to whichever window is active, so if another window has focus the run stops instead of typing into it.
- **The typed file name is `wdexport.png`,** renamed afterwards: xdotool types as a US keyboard while KDE applies the German layout, so `-` arrives as `ß` (and y/z swap). If any other PNG appears instead, the run stops and names it.
- **On the laptop Wonderdraft runs on the RTX 5070** (PRIME offload): on the integrated Radeon every launch parked ~3.5 GB in the GPU driver's page pool (`GPUReclaim`), which once ran the session out of memory.
- Pause the Proton sync while it runs if you can: the 120 MB PNGs are transient.

### Conventions the split depends on

- **Border style decides the variant.** God domains: dashed. Regions: gradient. A shape with any other border style is dropped from both.
- **Label layers:** Default = terrain icons, +1 god domain labels, +2 region labels, +3 divine city names, +4 city icons, −1 small city names, −2 landmark names (mountains, rivers). Layers are saved as `z_index` (Default = 0, +1 = 1, −1 = −1, …).

To change the rules, edit `VARIANTS` at the top of `wd_regions.py`.

## `wdmap`: inspect and edit maps (stage 1 of the AI tooling)

`wd.py` (symlinked as `wdmap`) reads a map into plain data so it can be asked questions, previewed and edited.

```bash
wdmap info    MAP                                   # size, counts per layer (with your layer names), packs
wdmap query   MAP symbols --family '*kapok*' --on water
wdmap query   MAP labels --layer "Region Labels" --list 20
wdmap query   MAP regions --style domain             # every shape with its inferred name
wdmap preview MAP -o out.png --area region:Nashavel --grid 512 --type mountain
```

- **Filters** (for `query`, and for highlighting in `preview`): `--texture`/`--family` (globs on the art path), `--type` (tree, mountain, symbol), `--layer` (number or Wonderdraft layer name), `--text`, `--region` (inside a named region or god domain), `--rect`, `--near LABEL:R`, `--on land|water`, `--style domain|region`.
- **Region names** are inferred: a god-domain shape takes the +1 label inside it, a region shape the +2 label; unlabelled domain pieces (islands) inherit the name of the same-coloured domain. Region colours are reused, so regions don't inherit.
- **Preview** is an approximation for seeing where things are: the real painted terrain (ground over the land mask), region shapes, user-pack symbols with their real art (greyscale trees/mountains tinted by their sampled ground colour, custom-colour icons by their palette), built-in symbols as markers by type, labels in a stand-in font (`fc-match` of the map font). `--grid N` adds a coordinate grid in map units.
- **Land/water** is the alpha channel of the map's `mask` image.

### Editing

```bash
wdmap edit MAP labels  --text '*prinicpality*' --replace Prinicpality Principality
wdmap edit MAP symbols --region Myrkono --family '*hatch_pine*' --art 'user://assets/Dotty_Assets/sprites/trees/Dotty_Kapoks/Kapok_Tree' --preview swap.png
wdmap edit MAP symbols --on water --type tree --delete --dry-run
wdmap edit MAP labels  --text Veidrath --to-layer "Divine City Labels" --move 0,-40
wdmap edit MAP regions --text 'Three Pines' --color '#aa3355' --border-style domain
wdmap backups MAP
wdmap restore MAP --backup 0
```

- **Actions:** symbols `--move --scale --rotate --to-layer --art --delete`; labels `--move --scale --size --rotate --to-layer --set-text --replace --font --color --delete`; regions `--move --color --border-style --border-width --delete`. Filters select what is edited (same as `query`); editing with no filter needs `--all`.
- **Saving** happens in place, edit by edit. Every save first copies the map to `~/.local/share/wdmap/backups/<map>/` (newest 20 kept); `restore` puts one back (backing up the current file first). Saving is refused while Wonderdraft has the map open (checked by window title, since Wonderdraft would overwrite the edit on its next save) and when the file changed on disk after it was read. `--dry-run` reports without saving; `--preview` renders the edited area with the changes highlighted.
- **Art swaps** (`--art`) take a texture or an art family already used somewhere in the map, which supplies the sprite's offset, footprint (`radius`), type and colour setup. The swapped symbol keeps its footprint (`radius x scale` stays the same, so a kapok replaces a pine at a pine's size; add `--scale` to change that), keeps its variant number where the new family has it, and gets its ground-colour `sample` recomputed from the ground image, as Wonderdraft does on placement. Art not yet in the map has to be placed once in Wonderdraft first.
- Moving a symbol also refreshes its `sample`.

### Adding things

```bash
wdmap add     MAP symbol --art 'user://assets/.../Town' --under Valreka --offset 0,-60
wdmap add     MAP label  --text 'Testford' --at 2700,6600 --like Valreka
wdmap scatter MAP --art 'user://assets/Dotty_Assets/sprites/trees/Dotty_Kapoks/Kapok_Tree' --region 'Galdua Jendea' --preview forest.png
wdmap along   MAP --art 'res://sprites/mountains/playful_jagged_peaks/peak' --from Valreka --to 'Haraour Eliza' --jitter 40
wdmap stamp capture MAP castle-town --near Valreka --radius 150
wdmap stamp place   MAP castle-town --under 'Ljos*' --offset 0,80
wdmap stamp list
wdmap markers MAP
```

- **New symbols** copy a symbol that already uses the art (so it must appear in the map once), take the family's typical scale and the layer that art is most used on (a town icon goes to City Icons, not the Legend), a random variant and mirror, and a fresh ground-colour sample.
- **New labels** copy the style of `--like LABEL`, or of the first label on `--to-layer`.
- **`scatter`** fills a region (`--region`, by inferred name) or `--rect` with random, non-overlapping placements: on land by default, clear of existing symbols and of label text. Without `--count`/`--density` it fills as far as `--spacing` allows (default: from the art's footprint). `--seed` makes it repeatable.
- **`along`** places art every `--spacing` along `--path "X,Y X,Y …"` or from one label to another, pushed sideways by up to `--jitter`.
- **Stamps** live as JSON in [`stamps/`](stamps/) (committed, so both machines have them). `capture` takes everything within `--radius` of a point or label, labels included, so keep the radius tight around what you want. `place` puts it at `--at` or under every label matching `--under`, optionally `--rotate`d (the arrangement turns; icons and text stay upright, which suits loose groups more than multi-piece towns) and `--scale`d.
- **Markers** do the same from inside Wonderdraft: a label on layer **−5** reading `@stamp NAME [RADIUS]` or `@place NAME [DEG] [SCALE]`. Save and close Wonderdraft, run `wdmap markers MAP`: captures run first, then placements, then the marker labels are removed. `--overwrite` lets an `@stamp` replace an existing stamp.

All of these save in place the same way `edit` does (backup, open-in-Wonderdraft and changed-on-disk checks, `--dry-run`, `--preview`).

### Checking the map

```bash
wdmap check ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map            # everything
wdmap check ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map --level warning
```

One pass (`check.py`, ~2 s) over the problems found by hand while fixing Main, each with map coordinates; exits 1 if there are errors:

- **error** outlines that cross themselves (Wonderdraft leaves those regions unfilled and logs "Convex partition failed") or have under 3 points.
- **warning** land inside a domain outline that no region shape covers; unnamed or duplicate (stacked) shapes; a domain shape lying mostly inside another domain shape (a second outline on the domains view, as Merkavar's circle was); very dark regions whose outline runs mostly through water (they vanish against the sea); capital icons (the Legend's "Capital" art) with no city name (+3 or −1) within 160 units; labels overlapping in a view where both are shown, measured with the real fonts; god-city names off Divine City Labels and non-god-cities on it; leftover `@stamp`/`@place` markers.
- **info** trees and mountains standing in water.

The god-city list is `GOD_CITIES` in `check.py`.

### Interactive map

`published/setting/talan/interactive-map.html` shows the map with every layer on a switch. `--export` also exports a fourth view, **Base** (terrain, trees, mountains, city icons and the legend; no region shapes and no other labels), and `--publish` turns it into the page's data (`interactive.py`):

- **Tiles:** the Base export cut into a Leaflet `CRS.Simple` pyramid at `published/setting/assets/maps/tiles/{z}/{x}/{y}.webp` (256 px, zoom 0–5, ~1,365 files, ~15 MB). All tiles are rewritten on every publish, so each publish adds that much to git history.
- **`map-data.json`:** every region and domain outline (points, colour, border width, smoothing, its domain), every label on +1, +2, +3, −1, −2 (text, position, font, size, colours, rotation) and each shape's page link. The page draws them as one SVG in map units, so they scale with the map; outlines are smoothed like Wonderdraft's, domains dashed, regions with an inner glow.
- **Links** are matched by name to the pages under `published/setting/talan/domains/`: exact name or title, a page slug the name starts with ("Kaosadaemi Principality" → `kaosadaemi`), or one letter off (so a misspelt label still finds its page). `map-links.json` sets or blocks a link by name (e.g. Twin Suns → the Tvisol page). `--publish` prints the shapes without a page.

The fixed three-map page stays as it is; the interactive map is an addition.

### Snapshot for git

The map itself stays out of git: at ~100 MB it is over GitHub's per-file limit, compressed and undiffable, and every save would add a full copy to history. Proton Drive syncs it and `wdmap` keeps backups. Git tracks [`map-snapshot.json`](map-snapshot.json) instead, a readable text snapshot of what the map says: every label (layer, text, position, font, size), every region shape (kind, inferred name, bbox, area, colour), every icon-type symbol (settlements, castles) with its position, symbol counts per layer and art family, the scale bar and the layer names. It is deterministic, one item per line, so `git diff` reads like a changelog of the map.

```bash
wdmap snapshot ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map     # "updated" or "unchanged"
```

`wd_regions.py … --publish` refreshes it too, so the published views and the snapshot of their source are committed together.

### MCP server

`mcp_server.py` exposes all of the above to Claude as the `wonderdraft` MCP server, registered in the repo's [`.mcp.json`](../../.mcp.json) and started by `mcp-server.sh` (which builds a gitignored `.venv` with the `mcp` package on first run). Tools: `map_info`, `query`, `preview` (returns the image), `edit`, `add_symbol`, `add_label`, `scatter`, `along`, `stamp_list`, `stamp_capture`, `stamp_place`, `process_markers`, `check`, `backups`, `restore`, `snapshot`, `split_variants`. Each tool runs the same code path as the `wdmap` command, so the backups and safety checks apply; write tools take `dry_run` and `preview` (default on). The map defaults to `~/ProtonDrive/Wonderdraft/Main.wonderdraft_map` (or `$WD_MAP`) and is loaded per call, not kept in memory (~3 GB decoded). The [`wonderdraft-map`](../../.claude/skills/wonderdraft-map/SKILL.md) skill describes how Claude should use it.

`wdmap.py` is the model (`WDMap.load`, `.save`, `.symbols`, `.labels`, `.regions`, `select()`); `edit.py`, `place.py` and `stamps.py` hold the operations; `preview.py` renders; `test_wdmap.py` holds the tests (`python3 -m unittest tools/wonderdraft/test_wdmap.py`), including a byte-identical load/save round trip of the real map when it's on disk. The real map is decoded once per run (a decoded map takes a few GB; loading it per test class ran the laptop out of memory).

## How it works

- A `.wonderdraft_map` is a Godot 3 compressed file (`GCPF` header, FastLZ, 4096-byte blocks) wrapping one `store_var` dictionary: `territories.territories[]` holds the region shapes, `labels[]` and `symbols[]` carry a `z_index`, and the terrain is three 8192×8192 RGBA images (`mask`, `ground`, `water_tint`).
- `gcpf.c` reads and writes that container (`gcpf d in > raw`, `gcpf c out < raw`). It is compiled automatically on first run with `cc`/`gcc`/`clang`; the binary is gitignored because it is per-machine.
- `gdvar.py` is a Godot 3 Variant codec: a byte-range parser (used by the splitter to splice untouched data through) and a full `decode`/`encode` to Python values. Encoding reproduces Wonderdraft's files byte for byte: INT is always written 64-bit, REAL 64-bit only when float32 can't hold the value, and Object properties are kept as an ordered list because Godot can repeat one (ImageTexture writes `flags` twice).

This reads our own save files; it does not touch the Wonderdraft program (whose EULA forbids decompiling it).
