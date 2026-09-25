# Wonderdraft tooling

Tools for the Wonderdraft source maps behind the terrain / regions / domains views (see [`docs/map-todo.md`](../../docs/map-todo.md)). The `.wonderdraft_map` sources live on Proton Drive (`~/ProtonDrive/Wonderdraft/`), not in git.

## `wd_regions.py`: one map, one file per region type

Wonderdraft has a single regions overlay, so god domains and regions can't be shown separately and there are no region layers. This script takes the one master map that holds both and writes a copy per variant, ready to export:

| Variant | Region shapes kept | Label layers dropped |
|---|---|---|
| `<map> - God Domains` | dashed border (`border_dash`) | +2 (region labels), −1 (small city names) |
| `<map> - Regions` | gradient border (`border_gradient`) | +1 (god domain labels) |
| `<map> - Terrain` | none | +1 (god domain labels) |

Everything else (terrain, symbols, +3 divine city names, +4 city icons, theme) is copied byte for byte. The input map is only read, never modified.

```bash
python3 tools/wonderdraft/wd_regions.py ~/ProtonDrive/Wonderdraft/Backup.wonderdraft_map
```

Outputs land next to the input (or in `-o <folder>`) and are overwritten on every run, so treat them as export-only: edit the master, rerun, export.

### Publishing the three map views

1. `wd-regions ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map` writes the three variants.
2. Open each variant in Wonderdraft and export it next to its map file under the same name: `Main - Terrain.webp`, `Main - Regions.webp`, `Main - God Domains.webp` (WebP is copied as is; PNG/JPG are converted at quality 92, Wonderdraft's own WebP setting).
3. `wd-regions ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map --publish` copies them to `published/setting/assets/maps/` as `terrain.webp`, `regions.webp` and `domains.webp` and runs `resize.sh` for the `display/` and `thumbs/` variants. It refuses when an export is missing or older than its variant map (stale).
4. Review the maps page and commit; pushing deploys the site.

Exporting stays manual: Wonderdraft has no command-line export, and scripting its window on KDE Wayland proved unreliable (input-permission prompt, scaled coordinates).

### Conventions the split depends on

- **Border style decides the variant.** God domains: dashed. Regions: gradient. A shape with any other border style is dropped from both.
- **Label layers:** Default = terrain icons, +1 god domain labels, +2 region labels, +3 divine city names, +4 city icons, −1 small city names. Layers are saved as `z_index` (Default = 0, +1 = 1, −1 = −1, …).

To change the rules, edit `VARIANTS` at the top of `wd_regions.py`.

## `wdmap`: inspect maps (stage 1, step 1 of the AI tooling)

`wd.py` (symlinked as `wdmap`) reads a map into plain data so it can be asked questions and previewed. Nothing here writes to a map yet.

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

`wdmap.py` is the model (`WDMap.load`, `.save`, `.symbols`, `.labels`, `.regions`, `select()`); `preview.py` renders; `test_wdmap.py` holds the tests (`python3 -m unittest tools/wonderdraft/test_wdmap.py`), including a byte-identical load/save round trip of the real map when it's on disk.

## How it works

- A `.wonderdraft_map` is a Godot 3 compressed file (`GCPF` header, FastLZ, 4096-byte blocks) wrapping one `store_var` dictionary: `territories.territories[]` holds the region shapes, `labels[]` and `symbols[]` carry a `z_index`, and the terrain is three 8192×8192 RGBA images (`mask`, `ground`, `water_tint`).
- `gcpf.c` reads and writes that container (`gcpf d in > raw`, `gcpf c out < raw`). It is compiled automatically on first run with `cc`/`gcc`/`clang`; the binary is gitignored because it is per-machine.
- `gdvar.py` is a Godot 3 Variant codec: a byte-range parser (used by the splitter to splice untouched data through) and a full `decode`/`encode` to Python values. Encoding reproduces Wonderdraft's files byte for byte: INT is always written 64-bit, REAL 64-bit only when float32 can't hold the value, and Object properties are kept as an ordered list because Godot can repeat one (ImageTexture writes `flags` twice).

This reads our own save files; it does not touch the Wonderdraft program (whose EULA forbids decompiling it).
