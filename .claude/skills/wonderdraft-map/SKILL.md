---
name: wonderdraft-map
description: Use this skill only to read the frozen Tyrnarra Wonderdraft map (~/Sync/Tyrnarra/Wonderdraft/Main.wonderdraft_map) through the read tools of the `wonderdraft` MCP server or the `wdmap` command - map_info, query, preview, check, geography - when the user names Wonderdraft or its file, or asks how the published map views were made. The map has been read-only since work on Kartofuchs began; every map edit, and every map request that names neither app, goes to kartofuchs-map. Do not use for changing any map, for battlemaps (map-library), or for the published map pages' prose.
---

# wonderdraft-map

`~/Sync/Tyrnarra/Wonderdraft/Main.wonderdraft_map` (8192 x 8192 map units) is the
old Wonderdraft copy of the Tyrnarra map. It is **frozen and read-only**: the live
map is the Kartofuchs one (`kartofuchs-map`), imported from this file on 2026-10-03
and edited only there since. This file is kept as a backup until Wonderdraft is
gone. The tooling lives in `tools/wonderdraft/` (its `README.md` has the details);
the `wonderdraft` MCP server (`.mcp.json`) exposes it as tools, and the same
operations exist as `wdmap …` commands.

## Ground rules

1. **Never write to this map.** Leave the write tools (`edit`, `add_symbol`,
   `add_label`, `scatter`, `along`, `stamp_capture`, `stamp_place`,
   `process_markers`, `restore`, `split_variants`) alone. A change the user wants
   goes to the Kartofuchs map.
2. **Read only:** `map_info`, `query`, `preview`, `check`, `stamp_list`,
   `backups`, and `geography` (each shape's land neighbours, coasts and
   labels as text). The map is as it stood when Kartofuchs work began, so a fact
   read here may already be out of date in Kartofuchs.
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
`published/setting/assets/maps/` are this map's last export, made by
`wd_regions.py … --publish` (the README's *Publishing the three map views*), and
`tools/wonderdraft/map-snapshot.json` is git's record of the map as exported.
Republishing from here would only bring back the same art; the next published
views come from Kartofuchs (`kartofuchs-map`, *The published views*).
