# assetgen: status and handoff

Where the Tyrnarra art pack stands, what the user has decided, and how to pick the work up in a
new session on either machine. The full record (every round, lesson and number) is
[README.md](README.md); this file is the short version to read first. Update it at the end of
every working session.

## State (2026-09-30)

- **Pack:** 24 folders, 746 sprites, installed in `~/.local/share/Wonderdraft/assets/Tyrnarra`
  and mirrored to Proton Drive (`assetgen.sh sync` after every install, which also carries the
  work files). Counts per folder: the families table in the README.
- **Trees:** conifers, pines, broadleaves, willows, jungle, palms, bamboo, savanna, cacti, dead
  trees, giant mushrooms, swamp trees, shrubs.
- **Terrain:** peaks, fells, hills, dunes, mesas, karst pillars (for Main's Tang Dynasty mountains);
  volcanoes (recolourable, active and extinct).
- **Icons** (recolourable, R ink / G body / B roofs and accents):
  - `Tyrnarra_2.5D_Settlements`: 18 kinds, raised view.
  - `Tyrnarra_2D_Settlements`: the same kinds, flat and straight-on, two per kind.
  - `Tyrnarra_2.5D_God_Cities`: two per god-city.
  - `Tyrnarra_2.5D_Landmarks`: standing stones, obelisk, lighthouse, shrine, statue, bridge,
    beacon, portal arch.
- **Last real Wonderdraft test** (`fullswap`, 2026-09-30): every region reads close to the
  built-ins, the Air Monastery's karst ring included (numbers in the README results log).
- **Main.wonderdraft_map** is on Wonderdraft's built-in art, the baseline for every comparison.
  The copies from before and after the 2026-09-26 pack swap were cleared away on 2026-09-30. Never modify any
  `Main*.wonderdraft_map` unless the user asks.

## Decisions (the user's)

- **Scope:** trees for every biome, mountains of every kind, settlement and divine-city icons, and
  whatever else a world or region map needs.
- **Style:** bold black lines on a flat pale fill, like Wonderdraft's own trees, with textured
  insides (branch tiers, a few thick curved strokes). No grey wash, no hazy edges: flat or soft
  sprites "jump out" in a forest. New families aim for this from the start. "If it looks good,
  it looks good": no need to match Wonderdraft closely.
- **Icons:** recolourable. One themed icon per god-city (two drawings each). The raised icons
  are filed as 2.5D; the flat 2D set was wanted "to see", then two per kind.
- **Comparisons:** against Wonderdraft's built-in art, not Dotty (Dotty only as an extra
  column). The built-ins may not be extracted (EULA); they are exported from Wonderdraft onto a
  blank map as private reference sprites (on the machines and in the user's own Proton Drive),
  never committed or published.
- **Real Wonderdraft tests:** as often as useful, but tell the user first (the export drives the
  keyboard for about 90 s). With the laptop's screen locked the exporter refuses to run.
- **Open, the user's call:**
  - The crosses on some shrines and chapels are fine for now.
  - The young compact firs come later: they dropped out in conifer round 17, and a new batch
    needs SDXL.
  - Whether and how to swap the pack into Main (`fullswap.py` has the mapping). Decided
    2026-09-30: through Kartofuchs. `assetgen.sh kartofuchs` writes the mapping ("Tyrnarra") and
    the measured built-in sizes into Kartofuchs' data folder; Kartofuchs swaps on import (or Map ▸
    Swap art). Settlement icons are its next step. Re-run the command after changing
    BUILTIN_TO/PACK_TO or re-measuring.
- **Known leftovers:** the flat 2D camps still show domed houses behind the tents.

## Where things live

| What | Local (the tools' paths) | Proton Drive (`Wonderdraft/...`) | In git? |
|---|---|---|---|
| Code, recipes, README, this file | `tools/wonderdraft/assetgen/` | | yes |
| Work folder: raw drawings, rounds, sheets, galleries (about 2.6 GB) | `~/.local/share/wdmap/assetgen/` | `assetgen-work/work/` | no |
| Built-in reference sprites (EULA: private, never published) | `.../assetgen/builtins/` | inside `assetgen-work/work/` | never |
| Test references (empty map, Base before and after the pack swap) | `~/.local/share/wdmap/assetgen-test/` | `assetgen-work/test/` | no |
| Installed pack | `~/.local/share/Wonderdraft/assets/Tyrnarra` | `Wonderdraft/assets/Tyrnarra` | no |
| Main and its Base view + export | | `Main*.wonderdraft_map`, `Main - Base.webp` | no |
| ComfyUI address | `~/.config/tyrnarra/comfyui-url` or `TYRNARRA_COMFY` | | never |

The test maps themselves (100 MB each) are rebuilt by the tools from Main's Base, so only the
three reference images travel.

**Moving between machines** (`assetgen.sh sync`):
- **Starting a session:** run `sync --pull`. It copies the work folder, the test references and
  the installed pack from Proton Drive into the local paths. It only adds and updates.
- **Ending a session:** run `sync`. It mirrors this machine's copies into Proton Drive, deleting
  there whatever is gone here.
- **One machine at a time:** push only after pulling the other machine's work, or its new
  drawings are deleted.
- **Proton Drive folder:** `TYRNARRA_PROTON` points `sync` at it when it isn't `~/ProtonDrive`.
- **Laptop:** its `~/ProtonDrive` is a local folder that rclone bisync syncs every 15 minutes.
  A push there is a local copy, and the upload follows.
- **Tower:** its Proton Drive is an rclone mount that needs a fresh 2FA code after each reboot.

**Working from the tower:** after `git pull` and `sync --pull`, a session there can generate
(ComfyUI runs locally: `TYRNARRA_COMFY=http://127.0.0.1:8188`), build, run offline tests and make
galleries. Real Wonderdraft exports need Wonderdraft installed there and an unlocked desktop.

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
test <fam> --round N --offline               # seconds: lineup and map crops drawn here
test <fam> --round N                         # real Wonderdraft export (hands off)
fullswap                                     # whole pack in a copy of the Base, exported, vs built-ins
kartofuchs                                   # fullswap's families as Kartofuchs' "Tyrnarra" art mapping + measured built-in sizes
gallery [families]                           # numbered review sheets per family, by variant
sync [--pull]                                # work files and pack to (from) Proton Drive
```

## Rules for this repo

- The repo is public. Before committing, grep new and changed files for LAN addresses, host
  names and personal details.
- Stage explicit paths only; commit and push per finished step, to `main`.
- The icon file names (`{item}_{n}`) are a contract with Kartofuchs' role guessing (README).
- Log every round in the README results log, and update this file when the state changes.
