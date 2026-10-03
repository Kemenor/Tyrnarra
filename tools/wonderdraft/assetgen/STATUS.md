# assetgen: status and handoff

Where the art pack (made for Tyrnarra, shipped with Kartofuchs as Fuchsbau) stands, what the user has decided, and how to pick the work up in a
new session on either machine. The full record (every round, lesson and number) is
[README.md](README.md); this file is the short version to read first. Update it at the end of
every working session.

## State (2026-10-03)

- **Pack:** 30 folders, 863 sprites, in Kartofuchs as its own pack Fuchsbau (`art/Fuchsbau` in
  the Kartofuchs checkout `$KARTOFUCHS`). `build` installs there since 2026-10-02; commit the art
  in Kartofuchs after a build. The Wonderdraft-installed "Tyrnarra" copy and its Proton mirror
  are gone (identical to Fuchsbau when trashed). Counts per folder: the families table in the README.
- **Trees:** conifers, pines, broadleaves, willows, jungle, palms, bamboo, savanna, cacti, dead
  trees, giant mushrooms, swamp trees, shrubs.
- **Terrain:** peaks, fells, hills, dunes, mesas, karst pillars (for Main's Tang Dynasty mountains);
  volcanoes (recolourable, active and extinct).
- **Icons** (recolourable, R ink / G body / B roofs and accents):
  - `Fuchsbau_2.5D_Settlements`: 18 kinds, raised view.
  - `Fuchsbau_2D_Settlements`: the same kinds, flat and straight-on, two per kind.
  - `Fuchsbau_2.5D_God_Cities`: two per god-city.
  - `Fuchsbau_2.5D_Landmarks`: standing stones, obelisk, lighthouse, shrine, statue, bridge,
    beacon, portal arch.
- **Last real Wonderdraft test** (the old fullswap, 2026-09-30): every region read close to the
  built-ins, the Air Monastery's karst ring included (numbers in the README results log).
- **Trimmed to generation (2026-09-30, the user):** the Wonderdraft swap and test tools (packswap,
  fullswap, the test command, built-in reference renders) are gone. The pack is tried on a real
  map in Kartofuchs: import `Main.wonderdraft_map` with the "Fuchsbau" art mapping (Map ▸ Import,
  or Map ▸ Swap art on an open map). That mapping comes with Kartofuchs (`server/artmap.ts`,
  `BASE_RULES`) and covers only Wonderdraft's built-in trees and mountains; other packs' art
  imports as it is. The measured built-in sizes live in Kartofuchs' data folder
  (`art-sizes.json`). Never modify `Main.wonderdraft_map` unless the user asks.

## Decisions (the user's)

- **Scope:** trees for every biome, mountains of every kind, settlement and divine-city icons, and
  whatever else a world or region map needs.
- **Style:** bold black lines on a flat pale fill, like Wonderdraft's own trees, with textured
  insides (branch tiers, a few thick curved strokes). No grey wash, no hazy edges: flat or soft
  sprites "jump out" in a forest. New families aim for this from the start. "If it looks good,
  it looks good": no need to match Wonderdraft closely.
- **Icons:** recolourable. One themed icon per god-city (two drawings each). The raised icons
  are filed as 2.5D; the flat 2D set was wanted "to see", then two per kind.
- **Reviewing:** the gallery sheets per family, and the whole pack on Main in Kartofuchs (see
  State). Wonderdraft's built-in art is never extracted or published (EULA).
- **Open, the user's call:**
  - The crosses on some shrines and chapels are fine for now.
  - The young compact firs come later: they dropped out in conifer round 17, and a new batch
    needs SDXL.
- **Shared with Kartofuchs (2026-10-01, the user):** the whole pack, god cities included, ships with
  Kartofuchs as its base pack "Fuchsbau" (art/Fuchsbau). Since 2026-10-02 (the user) it lives only
  there: `build` installs into it, and the Wonderdraft "Tyrnarra" pack was deleted.
- **Known leftovers:** the flat 2D camps still show domed houses behind the tents.

## Where things live

| What | Local (the tools' paths) | Proton Drive (`Wonderdraft/...`) | In git? |
|---|---|---|---|
| Code, recipes, README, this file | `tools/wonderdraft/assetgen/` | | yes |
| Work folder: raw drawings, rounds, sheets, galleries (about 2.6 GB) | `~/.local/share/wdmap/assetgen/` | `assetgen-work/work/` | no |
| The pack (Fuchsbau) | `$KARTOFUCHS/art/Fuchsbau` | | yes, in Kartofuchs |
| Main | | `Main.wonderdraft_map` | no |
| Measured built-in sizes (`art-sizes.json`) | Kartofuchs' data folder (`~/.local/share/kartofuchs/`) | | no |
| ComfyUI address | `~/.config/tyrnarra/comfyui-url` or `TYRNARRA_COMFY` | | never |

**Moving between machines** (`assetgen.sh sync`):
- **Starting a session:** `git pull` in Kartofuchs (the pack), then `sync --pull`. It copies the
  work folder from Proton Drive into the local path. It only adds and updates.
- **Ending a session:** commit and push the pack in Kartofuchs, then run `sync`. It mirrors this
  machine's work folder into Proton Drive, deleting
  there whatever is gone here.
- **One machine at a time:** push only after pulling the other machine's work, or its new
  drawings are deleted.
- **Proton Drive folder:** `TYRNARRA_PROTON` points `sync` at it when it isn't `~/ProtonDrive`.
- **Laptop:** its `~/ProtonDrive` is a local folder that rclone bisync syncs every 15 minutes.
  A push there is a local copy, and the upload follows.
- **Tower:** its Proton Drive is an rclone mount that needs a fresh 2FA code after each reboot.

**Working from the tower:** after `git pull` (here and in Kartofuchs) and `sync --pull`, a session there can generate
(ComfyUI runs locally: `TYRNARRA_COMFY=http://127.0.0.1:8188`), build and make galleries.

## The tower's ComfyUI

- **Two modes:** "sdxl mode" (about 5 s per SDXL image) and "flux mode" (about 2 min per FLUX
  image). The tower's Claude session switches them with its restart script. From the laptop, ask
  that session over Remote Control, naming the mode.
- **Engine rules:**
  - Never mix SDXL and FLUX jobs in one server session.
  - Never send FLUX to an sdxl-mode server.
  - One FLUX image per graph.
- **Waking it:** the user shuts the tower down when it's not needed. It wakes over LAN, and its
  Claude Remote Control session then starts and brings ComfyUI up.
- **Away from home (VPN):** the tower's firewall lets the home LAN and the user's VPN reach
  ComfyUI, so the usual address works over the VPN too. Fallback: an SSH tunnel through a machine
  on the home LAN, with the tools pointed at it (`TYRNARRA_COMFY=http://127.0.0.1:<local port>`).
- **After a wake:** the tower's session can come back under a new ID; a message queued for its
  old ID is lost, so send to the live one.
- **Auto-shutdown:** the tower powers itself off after three empty-queue checks in a row, five
  minutes apart (about 10-15 minutes of real idle). The short gaps between one-image jobs, or
  between chained batches, can't trip it. Wake it again over LAN if it went down (`generate`
  skips drawings that already exist).
- **Engines by family:**
  - SDXL: conifers, pines, palms, bamboo, savanna, cacti, dead trees, mushrooms, and the
    line-art peaks, fells and hills.
  - FLUX: broadleaves, willows, jungle, swamp, shrubs, dunes, mesas, pillars, volcanoes and all icons.

## Commands

All run through `assetgen.sh`, or with `.venv/bin/python assetgen.py` (in a worktree, use the main
checkout's venv).

```
generate <fam> --seeds 1-40 [--style S]      # drawings from ComfyUI into the work folder
build <fam> --round N [--no-install] [--seeds ...] [--set KEY=V]
gallery [families]                           # numbered review sheets per family, by variant
sync [--pull]                                # work files to (from) Proton Drive
```

## Rules for this repo

- The repo is public. Before committing, grep new and changed files for LAN addresses, host
  names and personal details.
- Stage explicit paths only; commit and push per finished step, to `main`.
- The icon file names (`{item}_{n}`) are a contract with Kartofuchs' role guessing (README).
- Log every round in the README results log, and update this file when the state changes.
