---
name: wonderdraft-map
description: Use this skill to read or change the Tyrnarra Wonderdraft map source (~/ProtonDrive/Wonderdraft/Main.wonderdraft_map) through the `wonderdraft` MCP tools or the `wdmap` command - looking at the map (map_info, query, preview), fixing labels, moving/retexturing/deleting symbols, recolouring regions, adding symbols and labels, scattering forests, lining up mountains, capturing and placing stamps, running the user's @stamp/@place markers, and preparing the three map-view exports. Trigger on "look at the map", "where is X on the map", "rename/fix the label", "add a town/forest/mountains", "stamp", "process my markers", a docs/map-todo.md item that is a label or symbol change, or "export/publish the maps". Do not use for painting terrain, drawing or redrawing region outlines, adding layers, or paths/roads (Wonderdraft only), nor for battlemaps (map-library) or the published map pages' prose.
---

# wonderdraft-map

The map source is `~/ProtonDrive/Wonderdraft/Main.wonderdraft_map` (8192 x 8192
map units). The tooling lives in `tools/wonderdraft/` (read its `README.md` for
details); the `wonderdraft` MCP server (`.mcp.json`) exposes it as tools, and the
same operations exist as `wdmap …` commands.

## Ground rules

1. **Wonderdraft must be closed on that map before anything is saved.** Wonderdraft
   does not notice file changes and would overwrite them on its next save; the
   tools refuse to save while its window shows the map. If a save is refused, ask
   the user to save and close the map in Wonderdraft, then retry.
2. **Look first, change second.** `query` / `preview` to find things; write tools
   with `dry_run=true` and `preview=true` first, show the user the preview for
   anything larger than a label fix, then run it for real.
3. **Every save is backed up** (`backups`, `restore`); restore only when the user asks.
4. **Don't launch Wonderdraft yourself** for checks: each launch parks ~3.5 GB in the
   GPU driver's memory pool on the laptop, and that has already caused an OOM.
   Ask the user to open the map when a check in Wonderdraft is needed.
5. After label or symbol changes that affect a published view, regenerate the
   variants (`split_variants`) and note the pending re-export in `docs/map-todo.md`.

## The map's conventions

- **Layers:** +5 Legend, +4 City Icons, +3 Divine City Labels, +2 Region Labels,
  +1 God Labels, 0 Terrain (Default), −1 City Labels (size 32), −2 landmark labels
  (mountains and other named features, size 24), −5 markers (`@stamp` / `@place`).
- **Region shapes:** god domains have the dashed border (`domain`), regions the
  gradient border (`region`); each is named after the label inside it (+1 / +2).
- **Views:** `split_variants` writes `Main - God Domains / Regions / Terrain`
  (God Domains hides +2, −1, −2; Regions hides +1; Terrain hides +1 and +2, so it
  carries city, landmark and river names but no polity names); the
  user exports each from Wonderdraft as WebP next to it, then
  `wd_regions.py … --publish` copies them into `published/setting/assets/maps/`
  (see the README's *Publishing the three map views*). Never commit/push the maps
  without the user reviewing them.

## Common tasks

- **Label fix from map-todo:** `query` labels by text → `edit` labels with
  `replace` → update the map-todo entry (source fixed, re-export pending).
- **New settlement:** `add_symbol` (art already on the map, e.g. a town icon;
  it lands on the art's usual layer) + `add_label` `like` a similar label.
- **Forest / mountains:** `scatter` into a named region or a rect (fills to the
  art's spacing, on land, clear of labels and existing icons); `along` for a ridge
  or tree line. Use `seed` so a dry run and the real run match.
- **Reuse a group:** `stamp_capture` with a tight radius (labels in range are
  included), then `stamp_place` at a point or under every matching label. The
  user can also leave `@stamp NAME [R]` / `@place NAME [DEG] [SCALE]` labels on
  layer −5 in Wonderdraft; then run `process_markers`.
- **Swap art:** `edit` symbols with `art` (a texture or family already on the map);
  footprint and ground tint are kept.

New art that isn't anywhere on the map yet must be placed once in Wonderdraft
first: the tools copy an existing instance for its sprite settings.
