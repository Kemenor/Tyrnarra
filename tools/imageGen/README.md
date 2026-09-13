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
shot; the full shot anchors every ref-mode shot.

**Every pass is ONE ComfyUI prompt, deliberately.** This machine is swap-bound,
and the big Mistral text encoder gets evicted and reloaded if the shots are
split into separate prompts, which turns a 2-minute render into a thrash. The
cost is that ComfyUI only fills `/history` when the whole prompt finishes, so
nothing is written to disk until the pass ends: a 4-variation batch produces
zero files and then four at once. `run_graph` prints an elapsed-time heartbeat
every 30 s so the wait is legible. **Do not "fix" this by queueing one prompt
per image** (tried, 2026-09: it swap-thrashed and was materially slower), and
do not run two render drivers at once for the same reason. House styles: **painterly**
(default) and **inked**, both approved against the Midjourney-era reference
art; a spec can also carry a literal style string.

```bash
python3 npc_art.py variations --spec <slug>.set.json [--count 1]
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
- **ComfyUI runs inside the `comfyui` podman/distrobox container**, so killing
  it needs `podman exec comfyui pkill -f main.py`; a host-side `pkill -f
  main.py` matches only the wrapper and leaves the real Python alive holding
  ~50 GB with the API down. `restart_server()` does this correctly and verifies
  the API is actually gone before restarting (fixed 2026-09, after the host-only
  version made a wedged server strictly worse).
- **One driver at a time.** `run_graph` preflights the queue and says so if it
  is busy, and the progress heartbeat reports **queue position**, so a pass that
  is parked behind a wedged prompt says `NOT STARTED, queued behind 1 job(s)`
  instead of claiming to render. `/interrupt` returns 200 but does nothing to a
  prompt wedged inside a model load; that needs `restart_server()`.

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

## Memory on this machine (measured 2026-09)

The stack is **38.4 GB of weights** (Mistral fp8 text encoder 16.8, Q4 unet
18.7, Turbo LoRA 2.6, VAE 0.3) on a 64 GB box, and ComfyUI keeps models in
**system RAM** between runs by design (see `--highvram`'s help text). Measured
RSS: **40 GB on the first pass, 51 GB peaking at 55 GB on the second**, after
which the machine swaps at ~480 MB/s and a 2-minute image takes 15.

Things that are NOT the cause, each checked against the source:
- **Node-output cache.** The default is `RAM_PRESSURE`, and `ram_release()`
  returns early only when `available >= target`. The default inactive target is
  `min(96, total_ram)` = the whole machine, so it already evicts after *every
  node*. `--cache-ram` cannot beat "always evict"; leave it alone.
- **`--disable-smart-memory`.** Its help reads "offload to regular ram instead
  of keeping models in vram" — it moves pressure *onto* system RAM. Wrong way.
- **Graph shape.** A 4-shot variations graph (41 nodes, 4.24 MP) and a 3-shot
  set (38 nodes, 3.17 MP) are near-identical; the growth is pass-to-pass, not
  shots-per-pass.

What remains: model pins plus PyTorch's caching allocator, which never returns
freed blocks to the OS, so RSS only ratchets up. **The only lever that shrinks
the baseline is a smaller text encoder** — the fp8 Mistral is 16.8 GB while the
unet is already Q4; a GGUF quant of the encoder is the obvious asymmetry to fix.

Practical rules until then: **one driver at a time**, and expect the second pass
in a server session to be slower than the first. A restart costs ~12 min of
reload, so restarting between NPCs is not free either.
