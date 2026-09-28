# assetgen: status and handoff

Where the Tyrnarra art pack stands, what the user has decided, and how to pick the work up in a
new session on either machine. The full record (every round, lesson and number) is
[README.md](README.md); this file is the short version to read first. Update it at the end of
every working session.

## State (2026-09-28 morning)

- **Pack:** 23 folders, 714 sprites, installed on the laptop in
  `~/.local/share/Wonderdraft/assets/Tyrnarra` and mirrored to the Proton Drive copy
  `~/ProtonDrive/Wonderdraft/Wonderdraft/assets/Tyrnarra` (`rsync -a --delete` after every
  install). Counts per folder: the families table in the README.
- **Trees:** conifers, pines, broadleaves, willows, jungle, palms, bamboo, savanna, cacti, dead
  trees, giant mushrooms, swamp trees, shrubs.
- **Terrain:** peaks, fells, hills, dunes, mesas; volcanoes (recolourable, active and extinct).
- **Icons** (recolourable, R ink / G body / B roofs and accents):
  - `Tyrnarra_2.5D_Settlements`: 18 kinds, raised view.
  - `Tyrnarra_2D_Settlements`: the same kinds, flat and straight-on, two per kind.
  - `Tyrnarra_2.5D_God_Cities`: two per god-city.
  - `Tyrnarra_2.5D_Landmarks`: standing stones, obelisk, lighthouse, shrine, statue, bridge,
    beacon, portal arch.
- **Last real Wonderdraft test** (`fullswap`, 2026-09-28): every region reads close to the
  built-ins (numbers in the README results log).
- **Main.wonderdraft_map** is on Wonderdraft's built-in art, the baseline for every comparison.
  The version with bought art is kept as "Main (after pack swap 2026-09-26)". Never modify any
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
  blank map as local reference sprites only, never committed.
- **Real Wonderdraft tests:** as often as useful, but tell the user first (the export drives the
  keyboard for about 90 s). With the laptop's screen locked the exporter refuses to run.
- **Open, the user's call:**
  - The crosses on some shrines and chapels are fine for now.
  - The young compact firs come later: they dropped out in conifer round 17, and a new batch
    needs SDXL.
  - Whether and how to swap the pack into Main (`fullswap.py` has the mapping).
- **Known leftovers:** the flat 2D camps still show domed houses behind the tents.

## Where things live

| What | Where | In git? |
|---|---|---|
| Code, recipes, README, this file | `tools/wonderdraft/assetgen/` | yes |
| Raw drawings, rounds, sheets, galleries (about 2.6 GB) | laptop `~/.local/share/wdmap/assetgen/` | no |
| Built-in reference sprites (EULA: local only) | laptop `~/.local/share/wdmap/assetgen/builtins/` | never |
| Test maps and exports | laptop `~/.local/share/wdmap/assetgen-test/` | no |
| Installed pack | laptop `~/.local/share/Wonderdraft/assets/Tyrnarra` + the Proton Drive mirror | no |
| ComfyUI address | `~/.config/tyrnarra/comfyui-url` or `TYRNARRA_COMFY` | never |

**Working from the tower:** a session there has the code and these notes (after `git pull`),
and ComfyUI runs locally (`TYRNARRA_COMFY=http://127.0.0.1:8188`). It does not have the raw
drawings, the built-in references, Wonderdraft's test maps or the installed pack: those live on
the laptop. So from the tower:
- **Generating** new drawings works.
- **Rebuilding existing families, offline tests and real exports** need the laptop's work
  folder, or are done back on the laptop.

Keep one machine as the owner of the installed pack (the laptop so far). The tower's Proton
Drive is an rclone mount that needs a fresh 2FA code after each reboot.

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
- **Engines by family:**
  - SDXL: conifers, pines, palms, bamboo, savanna, cacti, dead trees, mushrooms, and the
    line-art peaks, fells and hills.
  - FLUX: broadleaves, willows, jungle, swamp, shrubs, dunes, mesas, volcanoes and all icons.

## Commands

All run through `assetgen.sh`, or with `.venv/bin/python assetgen.py` (in a worktree, use the main
checkout's venv).

```
generate <fam> --seeds 1-40 [--style S]      # drawings from ComfyUI into the work folder
build <fam> --round N [--no-install] [--seeds ...] [--set KEY=V]
test <fam> --round N --offline               # seconds: lineup and map crops drawn here
test <fam> --round N                         # real Wonderdraft export (hands off)
fullswap                                     # whole pack in a copy of the Base, exported, vs built-ins
gallery [families]                           # numbered review sheets per family, by variant
```

## Rules for this repo

- The repo is public. Before committing, grep new and changed files for LAN addresses, host
  names and personal details.
- Stage explicit paths only; commit and push per finished step, to `main`.
- The icon file names (`{item}_{n}`) are a contract with Kartofuchs' role guessing (README).
- Log every round in the README results log, and update this file when the state changes.
