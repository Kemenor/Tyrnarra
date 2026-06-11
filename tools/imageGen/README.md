# imageGen — NPC art generation (local ComfyUI, Claude-operated)

Renders NPC art **locally and free** on this machine's GPU (RX 7900 XTX, FLUX.2
[dev] via ComfyUI). **The user never runs this tooling** — Claude operates it
inside the conversational flow defined in
[`.claude/skills/npc-art/SKILL.md`](../../.claude/skills/npc-art/SKILL.md):
design the NPC in chat → ~4 variations → the user picks → full / portrait /
scene set → upscale. Kept separate from
[`../foundryExport/`](../foundryExport/README.md) (which gets art *into*
Foundry); this folder only **makes** the images.

History: this folder previously held the fal.ai (`gen_portraits.py`,
`gen_npc_set.py`) and Midjourney (`mj_prompts.py`) cloud tiers. Retired
June 2026 — git history has them if ever needed. The committed art they
produced stays where it is.

## `npc_art.py` — the renderer

One Claude-operated module, FLUX.2-only (GGUF Q4 + Turbo LoRA, ~1-2 min/image
warm). Consistency via ReferenceLatent: the chosen variation anchors the full
shot; the full shot anchors every ref-mode shot. House styles: **painterly**
(default) and **inked**, both approved against the Midjourney-era reference
art; a spec can also carry a literal style string.

```bash
python3 npc_art.py variations --spec <slug>.set.json [--count 4]
python3 npc_art.py set        --spec <slug>.set.json --draft 2 [--scene "extra detail"]
python3 npc_art.py upscale    --spec <slug>.set.json [--scale 2]
python3 npc_art.py frame      --name <frame-stem> --desc "ring description"
```

- The spec (`<slug>.set.json`, schema in the module docstring) is
  **Claude-authored**: `character` / `wardrobe` are distilled at generation
  time from the NPC block's *physical description* + *clothing & dress*
  paragraphs (see `published/gm-notes/gm-reference/npc-block.md`). Specs live
  beside the output art and record the approved seeds (`render` block) so any
  shot can be re-rolled or reproduced.
- Outputs land beside the spec (`out` field), PNG. Portrait shots are square
  (`square_hd`) so they drop straight into the token-bake step when a token is
  wanted.
- The module auto-starts the local ComfyUI server and is machine-bound to
  `/var/mnt/games1tb/comfyui` (see that folder's `QUICKSTART.md`). If a Flux
  load grinds for minutes, another model family poisoned RAM: restart the
  server (`npc_art.restart_server()`); it is encoded in the module.

## Tokens are a separate, user-directed flow

Most NPCs do **not** get a token; tokens are essentially **per-faction**. The
user says which NPC gets one and which frame to use. The pieces:

1. `npc_art.py frame --name <stem> --desc "…"` renders new **frame ring art**
   on a magenta field into `../token-frames/` (only when a new faction frame is
   actually needed; the library is shared world-wide).
2. `../foundryExport/bake_token.py prep` chroma-keys the ring, `bake`/`batch`
   composites portrait + frame into token PNGs.
3. `../foundryExport/upload_forge.py` + `foundry_macro.py assign-images`
   push and assign. Forge key in `../keys/forge_key.txt` (gitignored).

Full runbook: [`../foundryExport/README.md`](../foundryExport/README.md).

Generated art **is committed** (generation is non-deterministic; the approved
images are the canon record). Specs are committed beside them.
