---
name: kartofuchs-map
description: Use this skill to read or change the Tyrnarra map in Kartofuchs (~/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs), the map editor replacing Wonderdraft, through the `kartofuchs` MCP tools - opening the map, map_info, query, screenshots, editing labels and symbols, scattering, stamps, regions and shapes, terrain, views and exports. Trigger when the user names Kartofuchs or the Kartofuchs map ("in Kartofuchs", "the kartofuchs map", "open the map in Kartofuchs"), or asks to open the Tyrnarra map for editing in Kartofuchs. Until the user switches over, map requests that name neither app go to wonderdraft-map, which edits the map the published views come from. Do not use for battlemaps (map-library), the published map pages' prose, or Kartofuchs' own code (that is the kartofuchs repo).
---

# kartofuchs-map

The Tyrnarra map in Kartofuchs is `~/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs` (a folder: `map.json` plus `terrain/`; 8192 x 8192 map units). It syncs between the laptop and the tower through Syncthing. Kartofuchs lives in its own repo (`$KARTOFUCHS`, else `~/Documents/fuchs/kartofuchs`); `tools/kartofuchs/mcp-server.sh` starts its MCP server for Tyrnarra sessions as `kartofuchs` (`.mcp.json`).

This map was imported from the Wonderdraft map on 2026-10-03 and is a separate copy: a change to one does not reach the other. Until the user switches over, the Wonderdraft map (`wonderdraft-map`) stays the source for the published map views. When it is unclear which map the user means, ask.

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
