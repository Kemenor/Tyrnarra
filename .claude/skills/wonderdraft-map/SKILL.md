---
name: wonderdraft-map
description: Use this skill only to read the frozen Tyrnarra Wonderdraft map (~/Sync/Tyrnarra/Wonderdraft/Main.wonderdraft_map) through the read tools of the `wonderdraft` MCP server or the `wdmap` command - map_info, query, preview, check, geography - when the user names Wonderdraft or its file, or asks how the published map views were made. The map is read-only; every map edit, and every map request that names neither app, goes to kartofuchs-map. Do not use for changing any map, for battlemaps (map-library), or for the published map pages' prose.
---

# wonderdraft-map

`~/Sync/Tyrnarra/Wonderdraft/Main.wonderdraft_map` (8192 x 8192 map units) is the
Wonderdraft copy of the Tyrnarra map, kept as a **frozen, read-only** backup: the
live map is the Kartofuchs one (`kartofuchs-map`). The tooling lives in `tools/wonderdraft/` (its `README.md` has the details);
the `wonderdraft` MCP server (`.mcp.json`) exposes it as tools, and the same
operations exist as `wdmap …` commands.

## Ground rules

1. **Never write to this map.** Leave the write tools (`edit`, `add_symbol`,
   `add_label`, `scatter`, `along`, `stamp_capture`, `stamp_place`,
   `process_markers`, `restore`, `split_variants`) alone. A change the user wants
   goes to the Kartofuchs map.
2. **Read only:** `map_info`, `query`, `preview`, `check`, `stamp_list`,
   `backups`, and `geography` (each shape's land neighbours, coasts and
   labels as text). A fact read here can differ from the live Kartofuchs map.
3. **Don't launch Wonderdraft yourself:** each launch parks ~3.5 GB in the GPU
   driver's memory pool on the laptop, and that has already caused an OOM.

## The map's conventions

- **Layers:** +5 Legend, +4 City Icons, +3 Divine City Labels, +2 Region Labels,
  +1 God Labels, 0 Terrain (Default), −1 City Labels, −2 landmark labels
  (mountains and other named features), −5 markers.
- **Region shapes:** god domains have the dashed border (`domain`), regions the
  gradient border (`region`); each is named after the label inside it (+1 / +2).

## The published views

The three views and the interactive map's tiles under
`published/setting/assets/maps/` come from this map, through
`wd_regions.py … --publish` (the README's *Publishing the three map views*), and
`tools/wonderdraft/map-snapshot.json` is git's record of the map as exported.
A publish from here republishes this map's art; publishing the live map is
`kartofuchs-map`, *The published views*.
