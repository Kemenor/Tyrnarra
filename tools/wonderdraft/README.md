# Wonderdraft tooling

Tools for the Wonderdraft source maps behind the terrain / kingdoms / domains views (see [`docs/map-todo.md`](../../docs/map-todo.md)). The `.wonderdraft_map` sources live on Proton Drive (`~/ProtonDrive/Wonderdraft/`), not in git.

## `wd_regions.py`: one map, one file per region type

Wonderdraft has a single regions overlay, so god domains and regions can't be shown separately and there are no region layers. This script takes the one master map that holds both and writes a copy per variant, ready to export:

| Variant | Region shapes kept | Label layers dropped |
|---|---|---|
| `<map> - God Domains` | dashed border (`border_dash`) | +2 (region labels) |
| `<map> - Regions` | gradient border (`border_gradient`) | +1 (god domain labels) |

Everything else (terrain, symbols, +3 divine city names, +4 city icons, theme) is copied byte for byte. The input map is only read, never modified.

```bash
python3 tools/wonderdraft/wd_regions.py ~/ProtonDrive/Wonderdraft/Backup.wonderdraft_map
```

Outputs land next to the input (or in `-o <folder>`) and are overwritten on every run, so treat them as export-only: edit the master, rerun, export.

### Conventions the split depends on

- **Border style decides the variant.** God domains: dashed. Regions: gradient. A shape with any other border style is dropped from both.
- **Label layers:** Default = terrain icons, +1 god domain labels, +2 region labels, +3 divine city names, +4 city icons. Layers are saved as `z_index` (Default = 0, +1 = 1, …).

To change the rules, edit `VARIANTS` at the top of `wd_regions.py`.

## How it works

- A `.wonderdraft_map` is a Godot 3 compressed file (`GCPF` header, FastLZ, 4096-byte blocks) wrapping one `store_var` dictionary: `territories.territories[]` holds the region shapes, `labels[]` and `symbols[]` carry a `z_index`, and the terrain is three 8192×8192 RGBA images (`mask`, `ground`, `water_tint`).
- `gcpf.c` reads and writes that container (`gcpf d in > raw`, `gcpf c out < raw`). It is compiled automatically on first run with `cc`/`gcc`/`clang`; the binary is gitignored because it is per-machine.
- `gdvar.py` parses Godot 3 Variant encoding; the splitter rewrites only the `territories` and `labels` entries and splices the rest through untouched.

This reads our own save files; it does not touch the Wonderdraft program (whose EULA forbids decompiling it).
