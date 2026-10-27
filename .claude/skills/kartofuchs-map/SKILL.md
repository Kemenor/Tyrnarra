---
name: kartofuchs-map
description: Use this skill to read or change the Tyrnarra map, which lives in Kartofuchs (~/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs), through the `kartofuchs` MCP tools - opening the map, map_info, query, screenshots, measuring areas and distances, editing labels and symbols, scattering forests and mountains, stamps, regions and shapes, terrain, views and exports. It is the default for every map request: "look at the map", "where is X on the map", "how big is X", "rename/fix the label", "add a town/forest/mountains", "stamp", a docs/map-todo.md item, "export the maps", or anything naming Kartofuchs. The Wonderdraft map is frozen; only a request that names Wonderdraft or its file goes to wonderdraft-map. Do not use for battlemaps (map-library), the published map pages' prose, or Kartofuchs' own code (that is the kartofuchs repo).
---

# kartofuchs-map

The Tyrnarra map in Kartofuchs is `~/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs` (a folder: `map.json` plus `terrain/`; 8192 x 8192 map units). It syncs between the laptop and the tower through Syncthing. Kartofuchs lives in its own repo (`$KARTOFUCHS`, else `~/Documents/fuchs/kartofuchs`); `tools/kartofuchs/mcp-server.sh` starts its MCP server for Tyrnarra sessions as `kartofuchs` (`.mcp.json`).

This is the live Tyrnarra map: every map change goes here. It was imported from the Wonderdraft map on 2026-10-03, and the Wonderdraft map has been frozen and read-only since (`wonderdraft-map`).

## Opening the map

The MCP tools work on the map the running Kartofuchs has open; they never touch the files themselves.

1. Call `maps` with `open` set to the map's absolute path (`/home/thomas/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs`). It opens the map and makes it the map the other tools use; when Kartofuchs isn't running, it starts it in the background first (port 7717, log `~/.local/state/kartofuchs/mcp-server.log`). No need to ask the user before opening. `maps` with no arguments lists what is open.
2. **One machine at a time.** While a machine has the map open, Kartofuchs keeps a `lock.json` in the map folder naming that host; it syncs to the other PC, which then refuses the map with the host's name. If `maps` refuses it that way, tell the user which machine has the map open and stop there. Never delete `lock.json` or copy the map to get around it. A lock goes stale 3 minutes after its machine stops renewing it, and Syncthing needs a little while to carry it over, so right after the user closes the map on one PC the other may still refuse it for a moment.

Screenshots and exports are drawn by an editor. When none has the map open, Kartofuchs starts its desktop app hidden to draw them (this needs a display), so they work without a visible window; edits never need one.

## Ground rules

1. **Changes are live.** Every edit appears in the user's editor at once and joins the shared undo history; `undo` takes back your own last step.
2. **Look first, change second.** Start with `map_info` (layers, views, what the user is looking at and has selected); find things with `query`; take a `screenshot` before and after anything larger than a label fix and show it to the user.
3. **"This" or "the selected ones"** usually means the editor's selection (`selected: true`).
4. **Locked layers refuse changes.** Unlock one only when the user asks.
5. **The user's map is not test material.** Try anything destructive on a scratch copy first.

## The map's conventions

- **Layers** (top of the tree first): Map furniture, Terrain, City Icons, Legend (Legend, Legend (labels)), God Domain (God Domain Regions, God Labels), Kingdoms (Kingdom Regions, Region Labels), `-2` (landmark labels: mountains and other named features), City Labels, Divine City Labels.
- **Region shapes:** god domains are on God Domain Regions, regions on Kingdom Regions; each is named after the label inside it (God Labels / Region Labels).
- **Views:** Terrain, Regions and God Domains, the same three the published map pages show; `export` writes one image per view, `export_html` an interactive page.
- **Art:** the bought packs come from Kartofuchs' pack folder (`~/Sync/Tyrnarra/Kartofuchs/packs`), Kartofuchs' own trees and mountains from its Fuchsbau pack. New art goes in from either; `assets` lists what is available.

## Common tasks

- **Label fix:** `query` labels by text, then `edit` with the new text.
- **New settlement:** `add_symbol` with a town icon the map already uses, then `add_label` beside it on City Labels.
- **Forest or mountains:** `scatter` into a named region or an area.
- **Reuse a group:** `stamps` captures a group and places it again.
- **A whole town map:** `generate` (city) or `import_town` (Watabou's export), linked from the world map with `link_map`.
- **Measuring:** 1 map unit is 0.5 mile, so a square map unit is 0.25 square mile. `query` a region shape for its outline points; its area is the polygon's area in square units x 0.25, and a distance is map units x 0.5.
- **A map-todo item:** make the change, then mark the `docs/map-todo.md` entry done in the Kartofuchs map, with the published views' re-export still pending.

## The published views

The three views and the interactive map's tiles under `published/setting/assets/maps/` are still the last export from the Wonderdraft map (`tools/wonderdraft/README.md`, *Publishing the three map views*). No step yet takes Kartofuchs' `export` into that folder, so changes made here show on the site only once one exists. When the user asks to publish the maps, say so; running the Wonderdraft pipeline on the frozen map would republish the old art.
