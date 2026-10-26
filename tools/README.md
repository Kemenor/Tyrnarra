# tools/ — private GM build tooling (not served)

Everything here runs on a machine on the **home network**: the desktop (which
also has the GPU) or the laptop. The site itself needs none of it.

| Folder | What | Needs |
|---|---|---|
| `encounterBuilder/` | PF2e encounter + loot builders (`pf2e-encounter` / `pf2e-loot` skills) | python, node, rsync + ssh to the Foundry server |
| `foundryExport/` | quest spec → Foundry import macro, token baking, art upload | python (pillow, numpy), rsync + ssh |
| `imageGen/` | NPC / scene art via ComfyUI (`npc-art` skill), Midjourney inbox | the desktop's ComfyUI (local there, over the LAN from the laptop) |
| `wonderdraft/` | the map source tooling (`wonderdraft-map` skill) | its own venv; the map file in Proton Drive |
| `map-library/`, `token-frames/` | shared map catalogues and token frames | nothing extra |
| `keys/` | gitignored paid-service keys, from Proton Drive | see [`keys/README.md`](keys/README.md) |

## This repo is public: what stays out of it

- **Keys** live in `tools/keys/` (gitignored), copied from Proton Drive.
- **Machine addresses** live outside the repo entirely, in
  `~/.config/tyrnarra/` on each machine (one value on the first line of each file;
  an env var overrides it):

  | File | Env var | Value |
  |---|---|---|
  | `foundry-remote` | `TYRNARRA_FOUNDRY` | `<ssh-host>:/<foundry-root>`, the folder holding `app/` and `data/Data/` |
  | `comfyui-url` | `TYRNARRA_COMFY` | `http://<desktop-ip>:8188` (laptop only; the desktop defaults to its own server) |

  Use an **ssh alias** from `~/.ssh/config` as the host, so IPs and hostnames
  stay in your ssh config, never in a committed file.
- **Paid content** (module packs, full-res maps, the Foundry mirror) lands in
  gitignored folders (`encounterBuilder/_sources/`, `maps/_full/`).

## Setting up a machine (e.g. the laptop)

1. **Clone** the repo, then install the toolchain: Python 3.10+, `node`, `rsync`,
   `ssh`, `git`, and `pip install requests pillow numpy` (`scipy` too for the
   wonderdraft tools).
2. **SSH to the Foundry server.** Give the server an alias in `~/.ssh/config`
   (`Host <alias>` / `HostName <server-ip>` / `User <user>` / `IdentityFile ...`),
   then `ssh-copy-id <alias>`. Copy the alias block from the desktop's
   `~/.ssh/config` to use the same name on every machine.
3. **Write the addresses** and run the check:
   ```bash
   python3 tools/check_setup.py --foundry "<alias>:/<foundry-root>" --comfy "http://<desktop-ip>:8188"
   ```
   It reports what is missing, with the fix for each, and lists the server's
   worlds against [`foundryExport/campaigns.json`](foundryExport/campaigns.json).
4. **Build the databases:** `python3 tools/encounterBuilder/rebuild.py`
   (clones the pf2e data, mirrors the server's modules; a few minutes the first time).
5. **Keys**, only if needed: copy `falai.key` from Proton Drive into `tools/keys/`.
6. **Art from the laptop:** start ComfyUI on the desktop in LAN mode
   (`run-comfyui-lan.sh`, the "ComfyUI (LAN)" menu entry); `npc_art.py`,
   `scene_art.py` and `assetgen` then use it through `comfyui-url`, and never
   try to start or restart a server that lives on another machine.

Rerun `check_setup.py` any time something stops working; it changes nothing
except the address files you pass it.

## Campaigns and Foundry worlds

Each campaign folder under `published/gm-notes/` maps to a Foundry world id in
[`foundryExport/campaigns.json`](foundryExport/campaigns.json) (`null` until the
campaign has a world). `upload_foundry.py --campaign <slug>` and
`check_setup.py` read it. A new campaign gets its line when its world exists.
