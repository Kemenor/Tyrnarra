# tools/ — private GM build tooling (not served)

Everything here runs on a machine on the **home network**: the desktop (which
also has the GPU) or the laptop. The site itself needs none of it.

| Folder | What | Needs |
|---|---|---|
| `encounterBuilder/` | PF2e encounter + loot builders (`pf2e-encounter` / `pf2e-loot` skills) | python, node, rsync + ssh to the Foundry server |
| `foundryExport/` | quest spec → Foundry import macro, token baking, art upload | python (pillow, numpy), rsync + ssh |
| `imageGen/` | NPC / scene art via ComfyUI (`npc-art` skill), Midjourney inbox | the desktop's ComfyUI (local there, over the LAN from the laptop) |
| `wonderdraft/` | tooling for the frozen, read-only Wonderdraft map, the source of the published map views (`wonderdraft-map` skill) | its own venv; the map file in the sync folder |
| `kartofuchs/` | starts the Kartofuchs MCP server (`kartofuchs` in `.mcp.json`) from the Kartofuchs checkout | the checkout (`$KARTOFUCHS`, else `~/Documents/fuchs/kartofuchs`), Node 26, the Kartofuchs app running with the map open |
| `region-pages/` | regenerates a region's published page from its lore files | python |
| `map-library/`, `token-frames/` | shared map catalogues and token frames | nothing extra |
| `keys/` | gitignored paid-service keys, linked from the sync folder | see [`keys/README.md`](keys/README.md) |

## The sync folder

Everything that is neither code nor public travels between machines through
Syncthing, in **`~/Sync/Tyrnarra/`** (`TYRNARRA_SYNC` moves it). An always-on
relay keeps an encrypted copy, so the machines sync even when only one is on:

| Folder | What | Reached through |
|---|---|---|
| `Wonderdraft/` | `Main.wonderdraft_map` and its backups; `app/themes` | the `wonderdraft` tools directly; links in Wonderdraft's data folder |
| `Kartofuchs/` | `Main.kartofuchs`; `app/` stamps, themes, mappings, `art-sizes.json` | Kartofuchs; links in its data folder |
| `Kartofuchs/packs/` | the bought asset packs (2-Minute Tabletop, Dotty, Avoro, ...) | the links `~/.local/share/kartofuchs/packs` (Kartofuchs' pack folder) and `~/.local/share/Wonderdraft/assets` (while Wonderdraft is installed) |
| `Dungeondraft/` | Dungeondraft packs | Dungeondraft |
| `assetgen-work/work/` | the asset generator's raw work | the link `~/.local/share/wdmap/assetgen` |
| `map-library/` | licensed battlemap art | the link `map-library/_full` |
| `keys/` | paid-service keys | a link per key in `keys/` |
| `config/` | `foundry-remote` | the link `~/.config/tyrnarra/foundry-remote` |
| `fonts/` | the maps' fonts: labels (Uncial Antiqua, Gentium Book Basic) and the ones the Avoro themes name | the link `~/.local/share/fonts/tyrnarra` |
| `published-full/` | the GM notes' full-res art | a link `_full` per art folder in `published/gm-notes/` |

The real files live in the sync folder and the links point into it, never the
other way: Syncthing copies a link as a link, without its files. `check_setup.py
--link` creates the links (moving a local file or folder with no synced copy into
the sync folder first) and the plain check reports any that are missing.
`comfyui-url` stays a local file, because it differs per machine, and so do app
settings and backups. When two machines change the same file before syncing,
Syncthing keeps both and names the older one `.sync-conflict-...`, so let a big
file like the map sync before opening it on another machine. Keep the sync folder
outside any Proton Drive folder: two sync tools on one folder fight.

## This repo is public: what stays out of it

- **Keys** live in the sync folder's `keys/`, linked into `tools/keys/` (gitignored).
- **Machine addresses** live outside the repo entirely, in
  `~/.config/tyrnarra/` on each machine (one value on the first line of each file;
  an env var overrides it):

  | File | Env var | Value |
  |---|---|---|
  | `foundry-remote` | `TYRNARRA_FOUNDRY` | `<ssh-host>:/<foundry-root>`, the folder holding `app/` and `data/Data/` (a link into the sync folder) |
  | `comfyui-url` | `TYRNARRA_COMFY` | `http://<desktop-ip>:8188` (laptop only; the desktop defaults to its own server) |

  Use an **ssh alias** from `~/.ssh/config` as the host, so IPs and hostnames
  stay in your ssh config, never in a committed file.
- **Paid content** (module packs, full-res maps, the Foundry mirror) lands in
  gitignored folders (`encounterBuilder/_sources/`, `maps/_full/`) or the sync folder.

## Setting up a machine (e.g. the laptop)

1. **Clone** the repo, then install the toolchain: Python 3.10+, `node`, `rsync`,
   `ssh`, `git`, and `pip install requests pillow numpy` (`scipy` too for the
   wonderdraft tools).
2. **SSH to the Foundry server.** Give the server an alias in `~/.ssh/config`
   (`Host <alias>` / `HostName <server-ip>` / `User <user>` / `IdentityFile ...`),
   then `ssh-copy-id <alias>`. Copy the alias block from the desktop's
   `~/.ssh/config` to use the same name on every machine.
3. **Link the sync folder, write the addresses** and run the check:
   ```bash
   python3 tools/check_setup.py --link --foundry "<alias>:/<foundry-root>" --comfy "http://<desktop-ip>:8188"
   ```
   Once one machine has written `foundry-remote`, the others get it through the
   sync folder, and `--link` alone is enough.
   It reports what is missing, with the fix for each, and lists the server's
   worlds against [`foundryExport/campaigns.json`](foundryExport/campaigns.json).
4. **Build the databases:** `python3 tools/encounterBuilder/rebuild.py`
   (clones the pf2e data, mirrors the server's modules; a few minutes the first time).
5. **Keys**, only if needed: put `falai.key` in the sync folder's `keys/` and run `check_setup.py --link`.
6. **Art from the laptop:** start ComfyUI on the desktop in LAN mode
   (`run-comfyui-lan.sh`, the "ComfyUI (LAN)" menu entry); `npc_art.py`,
   `scene_art.py` and `assetgen` then use it through `comfyui-url`, and never
   try to start or restart a server that lives on another machine.

Rerun `check_setup.py` any time something stops working; it changes nothing
except the address files you pass it and, with `--link`, the links.

## Campaigns and Foundry worlds

Each campaign folder under `published/gm-notes/` maps to a Foundry world id in
[`foundryExport/campaigns.json`](foundryExport/campaigns.json) (`null` until the
campaign has a world). `upload_foundry.py --campaign <slug>` and
`check_setup.py` read it. A new campaign gets its line when its world exists.
