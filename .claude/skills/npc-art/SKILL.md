---
name: npc-art
description: Use this skill to generate the art set for a Tyrnarra NPC on the local GPU - portrait, full-body, and scene shots rendered with the local ComfyUI install (FLUX.2), free and Claude-operated end to end. Trigger on "generate the art/set/portrait for [NPC]", "we need images for [NPC]", "render the [NPC] set", the art step of building a quest cast (quest-workflow Phase 7.4), or a request for a new faction token frame. The user NEVER runs the tooling; Claude runs every command and sends images into the chat for the user's picks. Requires the NPC's physical description + clothing (the npc-block fields) to exist or be workshopped in chat first. Do not use for battlemap art (subscription catalogs cover that) or for player-facing page illustrations unless asked.
---

# npc-art

Renders a consistent multi-shot art set for one NPC on the local GPU and walks
the user through the choices in chat. Everything runs through
`tools/imageGen/npc_art.py` (Claude-operated; see its docstring and
`tools/imageGen/README.md`). Art + spec are committed beside the campaign's
assets.

## On invocation

1. Read `tools/imageGen/README.md` and the `npc_art.py` docstring (spec schema).
2. Locate the NPC's **physical description** and **clothing & dress** — from the
   GM page / npc-block. If they do not exist, workshop them in chat first
   (that is part of NPC design, not of this skill).
3. Confirm the ComfyUI install is reachable (the module auto-starts the
   server). It lives at `/var/mnt/games1tb/comfyui` on this machine.

## The flow (pause at every user pick)

| Step | What happens | User involvement |
|---|---|---|
| **1. Spec** | Distill physical + clothing into `character` / `wardrobe`; write `<slug>.set.json` beside the campaign's `assets/portraits/` with full / portrait / scene shots. Style: `painterly` (default) or `inked`, or as directed | Surface the distilled spec text before rendering |
| **2. Variations** | `npc_art.py variations --spec … --count 4` (~5-8 min) | **SendUserFile the 4 images; wait for the pick** |
| **3. Set** | `npc_art.py set --spec … --draft N` — full (anchored on the pick), then portrait + scene (anchored on the full) | SendUserFile the three shots; offer re-rolls |
| **4. Re-rolls** | `set --only <shot> --force [--seed N] [--scene "extra"]` until happy | Each re-roll surfaced |
| **5. Upscale** | `npc_art.py upscale --spec …` (2x default) | — |
| **6. Place + wire** | Outputs are already beside the spec; reference the portrait from the NPC's GM page / dossier | Surface the file list |

Shot intent: **full** = the identity anchor; **portrait** = head-and-shoulders,
square, doubles as token-bake input; **scene** = the NPC in a setting moment
(VTT character art + notes). Portrait uses `"mode": "text"` (the reference path
resists tight crops); identity holds because full + portrait share the seed and
the spec carries the full description.

## Tokens (separate, user-directed)

Most NPCs get **no token** — tokens are essentially per-faction. Only when the
user says an NPC needs one: they name the frame (from `tools/token-frames/`),
then bake with `../foundryExport/bake_token.py bake/batch` and assign per
`tools/foundryExport/README.md`. A genuinely new faction frame:
`npc_art.py frame --name <stem> --desc "…"` → `bake_token.py prep` → add to
`faction-frames.json`.

## Hard rules

- **The user picks; Claude renders.** Send images into chat at every choice
  point (SendUserFile); never advance past a pick without the user's answer.
- **Specs and approved art are committed**; test renders and rejected
  variations are not (clean up `variations/` once a set is approved).
- **The NPC block is the source of truth** for looks; the spec distills it,
  never contradicts it. New visual facts invented during art design get written
  back to the NPC's block/dossier.
- **Style discipline:** painterly is the house default; inked is the approved
  secondary. Other styles only on explicit request, recorded in the spec.
- **Local first.** This is the free tier; the user can always take a character
  back to Midjourney themselves — that is their call, not a fallback Claude
  reaches for.

## Performance notes (this machine)

First render after a server start loads ~38 GB (several minutes); warm shots
take ~1-2 min each. The module renders multi-shot passes as ONE graph so the
heavy models load once. If a Flux load grinds >5 min, another model family has
poisoned RAM: `python3 -c "import npc_art; npc_art.restart_server()"` (30 s)
and re-run. Do not run other model families (SDXL checkpoints) between stages
of a set.
