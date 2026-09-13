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
produced stays where it is. A hosted tier came **back** in September 2026 as
[`fal_art.py`](#fal_artpy--the-hosted-renderer), on a different footing: it
shares `npc_art.py`'s spec and prompt builder instead of being a parallel
implementation that drifts.

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

## `fal_art.py` — the hosted renderer

The cloud sibling of `npc_art.py`, added September 2026. **Same spec file, same
prompts, same stage names**; the render happens on fal.ai. Use it when the local
box is busy or wedged, when a set is wanted without a 12-minute model load, or
to reach a model the local install does not have.

```bash
python3 fal_art.py models                                    # backends + est. price
python3 fal_art.py variations --spec <spec> [--count 2] [--model flux2]
python3 fal_art.py set        --spec <spec> --draft 1 [--scene "extra"]
python3 fal_art.py bakeoff    --spec <spec> [--models flux2,seedream4]
#   any render stage also takes --dry-run: prints prompts + cost, spends nothing
```

- **Stdlib only**, like `npc_art` — no `fal-client`, no `requests`, no pip step.
  Reference images go up inline as base64 data URIs, so there is no upload step.
- **It imports `npc_art`** for `prompt_for()`, `SIZES`, `STYLES` and `KEEP`. That
  is deliberate and load-bearing: if this module built its own prompts they
  would drift, and a local-vs-hosted comparison would be measuring the prompt
  difference rather than the model difference. Nothing in `npc_art` runs at
  import time, so importing it never touches the local ComfyUI server.
- **Backends** are `flux2` (default, the local pipeline's model, the
  like-for-like comparison), `nano-banana-pro` (strongest identity consistency,
  pulls photoreal) and `seedream4` (cheapest, favoured for stylised fantasy
  lighting). Adding one is a `BACKENDS` entry: the families differ only in how
  they take a size and what a reference costs.
- **Every pass prints a cost estimate.** It is an *estimate* from a hardcoded
  per-image table; fal moves prices without notice, so the dashboard is the
  authority. The number is there to answer "cents or dollars", not to bill.
- `bakeoff` renders one spec through several models into `<out>/bakeoff/<model>/`,
  pinning **one seed across all of them** so the comparison is of the models and
  not of the dice. It writes nowhere near the committed art.
- **Sizes differ slightly from local.** fal's `portrait_4_3` preset is 768×1024;
  `npc_art.SIZES` maps the same name to 896×1184. Same aspect, ~30% fewer pixels.
  Fine for comparison, worth knowing before mixing outputs in one set.
- The `upscale` stage is **unverified** (`fal-ai/esrgan`, never run here). The
  local `npc_art.py upscale` with 4x-UltraSharp is the proven path and is free;
  prefer it whenever the local box is up.

Key: `FAL_KEY` in the environment, else `../keys/falai.key`. The whole
`tools/keys/` directory is gitignored (plus a `**/*.key` glob), so a key dropped
in there cannot be committed whatever it is named.

Validated 2026-09-13: `models`, `--dry-run` prompt assembly (byte-identical to
the local builder), and one real `variations` render end to end (auth, queue
polling, download, spec write-back).

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

## Memory on this machine (measured 2026-09-13)

The stack is **38.4 GB of weights** on a 64 GB box, and ComfyUI keeps models in
system RAM between runs by design. **The pipeline had never actually been run
end to end before this** (all committed art up to 2026-06-08 is Midjourney/fal;
the `~1-2 min/image` figure in the original commit was an estimate, never a
measurement), so the following is its first real benchmark.

### The one setting that matters: `--cache-none`

ComfyUI's `objects` cache holds the loaded model instances produced by the
loader nodes, and it is **exempt from RAM-pressure eviction** - `execution.py`
`init_ram_cache()` and `init_lru_cache()` both leave it a plain
`HierarchicalCache`, and only `init_null_cache()` clears it. Without the flag,
every pass stacks another copy of the model patchers on the previous one.

Measured, four identical single-image passes, one per NPC:

| config | pass 1 | RSS growth per pass |
|---|---|---|
| default (RAM cache, pinning on) | 432 s | **+14.7 GB** |
| `--disable-pinned-memory` | 462 s | **+12.2 GB** |
| **`--cache-none`** | **251 s** | **+164 MB over FOUR passes** |

`--cache-none` run in full: 251 / 221 / 241 / 170 s, RSS after each pass
2446 / 2642 / 2533 / 2610 MB. **Mean 221 s per image, flat memory, no swap.**
`npc_art.ensure_server()` passes the flag, so it applies automatically.

Its documented cost ("executes every node for each run") is real - every pass
reloads the stack - but it is *faster* here, because the reload is trivial next
to the paging it avoids.

### Dead ends, so nobody re-walks them

- **`--disable-pinned-memory`** - pinning (`ram * 0.90` = 57.8 GB cap,
  `cudaHostRegister`, registers in place, does not copy) makes that memory
  unreclaimable, but it is NOT the growth. Disabling cost 7% and left a
  +12.2 GB ratchet.
- **`--cache-ram`** - cannot help. `ram_release()` returns early only when
  `available >= target`, and the default inactive target is the whole machine,
  so the *outputs* cache already evicts after every node. It never touched
  `objects`.
- **`--disable-smart-memory`** - its help says "offload to regular ram instead
  of keeping models in vram": moves pressure onto system RAM, the wrong way.
- **The fp8 text encoder** - `supports_fp8_compute()` is false on all
  non-NVIDIA, so it does manual-cast per layer, but this is NOT the growth
  either. fp8 is fine with `--cache-none`. A `mistral_3_small_flux2_fp4_mixed`
  (11.4 GB) was downloaded chasing this and is unnecessary; fp8 is still the
  configured encoder. No GGUF of this encoder exists (every flux2 text-encoder
  GGUF on HF targets *klein*, a different architecture).
- **Graph shape** - a 4-shot variations graph (41 nodes) and a 3-shot set
  (38 nodes) are near-identical, and growth happened between two passes of the
  *same* shape. Shape was never the variable.

### Operating rules

**One driver at a time** - two concurrent renders doubled pressure on a machine
with none to spare. ComfyUI runs inside the `comfyui` podman container, so
killing it needs `podman exec comfyui pkill -f main.py`; a host-side pkill
matches only the wrapper and leaves the real Python alive holding ~50 GB with
the API down. `restart_server()` does this correctly. A prompt wedged in a
model load ignores `/interrupt` (returns 200, does nothing); only a restart
clears it, and `run_graph`'s heartbeat reports queue position so a pass parked
behind a wedged prompt says so instead of claiming to render.
