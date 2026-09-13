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
| **2. Variations** | `npc_art.py variations --spec …` (**default 1**) | **SendUserFile it; wait for the OK** |
| **3. Set** | `npc_art.py set --spec … --draft N` — full (anchored on the pick), then portrait + scene (anchored on the full) | SendUserFile the three shots; offer re-rolls |
| **4. Re-rolls** | `set --only <shot> --force [--seed N] [--scene "extra"]` until happy | Each re-roll surfaced |
| **5. Upscale** | `npc_art.py upscale --spec …` (2x default) | — |
| **6. Place + wire** | Outputs are already beside the spec; reference the portrait from the NPC's GM page / dossier | Surface the file list |

Shot intent: **full** = the identity anchor; **portrait** = head-and-shoulders,
square, doubles as token-bake input; **scene** = the NPC in a setting moment
(VTT character art + notes).

**Portraits stay on `ref` mode.** `"mode": "text"` renders with no reference to
the anchor and returns a different person; a shared seed does NOT preserve
identity across different sizes and framings. The old note claiming otherwise
was wrong and shipped mismatched close-ups (caught 2026-09). If ref mode crops
too loose, tighten the framing text, do not switch to text mode.

**One variation, not four.** FLUX.2 + Turbo LoRA at 8 steps barely moves between
seeds on an identical prompt, so extra variations are near-duplicates and pure
render time. `--count` defaults to 1. **If the shot is wrong, fix the spec**
(character / wardrobe / framing) rather than rolling again.

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

**Measured 2026-09-13: ~221 s per image**, flat memory, no swap — *provided*
ComfyUI runs with `--cache-none`, which `ensure_server()` passes automatically.
Without it every pass retains another copy of the loaded models (+14.7 GB per
pass, RSS 38 → 55 GB, then swap thrash) because ComfyUI's `objects` cache is
exempt from RAM-pressure eviction. Measured passes: 251 / 221 / 241 / 170 s,
RSS after each 2446 / 2642 / 2533 / 2610 MB — **+164 MB drift over four**.
Full data and the list of dead ends (pinned memory, `--cache-ram`,
`--disable-smart-memory`, the fp8 encoder, graph shape) are in
`tools/imageGen/README.md`. **Read that before changing any memory flag** —
several plausible-sounding ones were tested and make things worse.

Every pass is ONE graph and **no file appears until the whole pass finishes**,
so a multi-shot batch writes nothing and then all of them at once; `run_graph`
prints a 30 s heartbeat carrying queue position.

**Before calling a run hung**, read that heartbeat — `NOT STARTED, queued
behind N job(s)` means something else is wedged and this pass never began.
Then `rocm-smi --showuse` (74-87% = working; a single sample can catch a
legitimate lull between steps) and `vmstat` (si/so in the hundreds of MB/s is
thrashing, not slowness).

**A wedged prompt ignores `/interrupt`** — it returns 200 and nothing happens,
because it is stuck inside a model load. `npc_art.restart_server()` is the only
way out, and it must kill inside the podman container: a host-side
`pkill -f main.py` matches only the wrapper and leaves the real Python alive
holding ~50 GB with the API down.

**Never run two render drivers at once** — it doubles memory pressure on a
machine with none to spare, and the second silently queues behind the first.
