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
python3 fal_art.py bakeoff    --spec <spec> [--models flux2,seedream4] [--style digital]
#   any render stage also takes --dry-run: prints prompts + cost, spends nothing
```

- **Stdlib only**, like `npc_art` — no `fal-client`, no `requests`, no pip step.
  Reference images go up inline as base64 data URIs, so there is no upload step.
- **It imports `npc_art`** for `prompt_for()`, `SIZES`, `STYLES` and `KEEP`. That
  is deliberate and load-bearing: if this module built its own prompts they
  would drift, and a local-vs-hosted comparison would be measuring the prompt
  difference rather than the model difference. Nothing in `npc_art` runs at
  import time, so importing it never touches the local ComfyUI server.
- **Backends** are `seedream45` (**default**, the house model), `seedream4` (its
  predecessor) and `flux2` (the local pipeline's model, kept as the like-for-like
  second opinion). Adding one is a `BACKENDS` entry: the families differ only in
  how they take a size, what a reference costs, which `extra` args they want, and
  which fields they have no input for (`omit`).
- **Output format is whatever the model returns, and the file is named for it.**
  Seedream has no `output_format` input and ignores the one we send, so it
  returns JPEG however politely we ask for PNG. `download()` sniffs the magic
  bytes and writes `<file>.jpg` rather than lying in a `.png`, which matters
  downstream: `bake_token.py` composites expecting real PNG with alpha. Every
  skip-if-exists and anchor lookup therefore goes through `existing()`, which
  finds the shot under any known extension. Without it, a set cannot find the
  anchor it just rendered and re-renders everything, every run.
- **Every pass prints a cost estimate.** It is an *estimate* from a hardcoded
  per-image table; fal moves prices without notice, so the dashboard is the
  authority. The number is there to answer "cents or dollars", not to bill.
- `bakeoff` renders one spec through several models into `<out>/falai/<model>/`
  (`--subdir` to change it), pinning **one seed across all of them** so the
  comparison is of the models and not of the dice. It writes nowhere near the
  committed art and writes **no** `render` metadata back into the spec: a
  comparison is not an approved render, and the specs it reads are live files
  another session may be editing.
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
the local builder), and full three-model bake-offs end to end (auth, queue
polling, data-URI references, download, spec write-back).

### FLUX.2 has TWO content checkers, and only one of them is a flag

This is the constraint that shapes which renderer a given NPC goes to.

- **The image check**, over `image_urls` on an *edit* call, refuses reference
  pictures of visibly injured characters. Sera Vance's anchor (a beaten
  prisoner, blood on her shirt) came back `422 content_policy_violation` with
  `loc: ["body","image_urls"]`. Caevan's unbloodied anchor went through the
  identical code path with a 1.8 MB data URI and no complaint, so it is the
  picture's content, not the transport, the payload size, or the C2PA metadata
  FLUX.2 embeds. **`enable_safety_checker: false` governs this one**, and it is
  on (i.e. checking disabled) for FLUX.2 in `BACKENDS` by GM decision.
- **The prompt check**, over the edit call's prompt text, is **separate and has
  no flag**. With the safety checker already disabled, Odo Mast's shots still
  came back 422 with `loc: ["body","prompt"]`: his wardrobe is written in dried
  blood, and the words alone are enough. Note the asymmetry: the *same* blood
  text passed on the text-to-image anchor, so the edit endpoint screens prompts
  harder than t2i does.

**Seedream 4 refused nothing.** Odo Mast rendered his full three-shot set there,
blood-writing and all, while FLUX.2 refused two of three. Combined with the style
result below, that is the reason Seedream is the default.

So the routing rule is: **Seedream for almost everything; the local renderer for
anything Seedream also refuses** (`npc_art.py` has no checker at all). A refused
shot no longer kills the pass, so a partial set comes back with a line naming
what to re-render locally.

`_summarise()` exists for this: fal replays the whole request in the error body,
so the one useful sentence is buried under a megabyte of echoed base64. It prints
the message *and the field*, because `image_urls` and `prompt` are different
problems with different remedies.

### The reference governs identity, the framing governs composition

An edit call inherits the **reference image's composition** unless told not to.
That is why a portrait shot whose framing already said *"head and upper chest
filling the frame"* kept coming back as the anchor's three-quarter body: the
words described the crop, but nothing overrode what the reference showed.

Writing stronger framing prose does not fix it. Tested on Odo Mast 2026-09-13:
the wording had to explicitly contradict the reference before the crop moved. So
`RECOMPOSE` is appended to **every ref-mode shot**, saying the reference is for
identity only and the framing overrides how it is cropped, posed and staged. The
unmodified spec then produced a correct head-and-shoulders portrait.

It goes on every ref shot rather than only tight ones, because a scene shot is a
recomposition too. **Specs need no change**; do not hand-write crop overrides
into `framing` and do not "fix" a loose crop by moving a portrait to `mode:
text`, which returns a different person.

### House style: `digital` (2026-09-13)

`--style digital` (in `STYLE_OVERRIDES`, an overlay on `npc_art.STYLES` so the
other session's `npc_art.py` stays untouched). Stylised digital painting, crisp
clean rendering, confident linework, cel-influenced shading, muted palette,
uncluttered background, with explicit negatives against oil/canvas/photographic
texture.

It replaces the older `painterly` oil language, which existed mainly to drag
FLUX.2 off photorealism and pulled the look further into smeared oils than
wanted. Crisper is explicitly fine; the ceiling is a confident digital
illustration, not an oil painting.

### Model results, 2026-09-13

**Seedream 4.5 is the house model.** Across the four-NPC trial (Caevan the
Vishkanya, Odo Mast the kitsune, Aldous the hovering revenant butler, Sera Vance
the orc) it refused nothing, held identity through the reference chain, matched
the `digital` brief, kept the `seed` input, and returned **3072×4096** for a flat
$0.04. Sera is the proof: FLUX.2 refused her outright, and 4.5 rendered her
correctly, as a woman, which FLUX.2 had also got wrong. It handles awkward
specifics unprompted too: Odo's blood-written sleeves, Aldous's feet dissolving
where he hovers clear of the floor.

Seedream 4 stays wired: same character, half the wall time, a quarter of the
pixels, a penny cheaper. FLUX.2 stays as the second opinion, crisp and clean
under `digital` but flatter, greyer, 768×1024, and it renders ancestry markers
(Caevan's jewel-toned scaling) as plain grey. Both rejected models are described
in the `BACKENDS` comments with the reasons.

Sample set: `published/gm-notes/furrious-five/assets/portraits/fal-trial/`
(untracked; trial art, not approved art).

### Speed, measured 2026-09-13

| | per shot | 3-shot set |
|---|---|---|
| Seedream 4 | 20 s | 61 s |
| Seedream 4.5 | 34–43 s | ~110 s |
| local FLUX.2 | ~220 s | ~660 s + cold load |

fal's reported GPU time is 85–90% of wall clock, so queueing is a rounding error
and these numbers should hold rather than swinging with fal's load.

4.5 reads as slower than 4 until you account for output size: **four times the
pixels in 1.7× the time**, so ~2.3× more efficient per pixel. Against local, a
set is ~6× faster on 4.5 and ~11× on v4, before the multi-minute cold model load
that local pays on a first pass. Compare set against set, not image against
image: `npc_art.py` renders a whole set in one graph precisely to pay that load
once.

## `mj_server.py` + `mj-overlay.user.js` — the Midjourney helper

The third tier, and the odd one out: **the GM drives this one, not Claude.**
Midjourney has no API and forbids automated access, so there is nothing to
drive. The helper removes the tedium around the manual flow and touches nothing
else: it fills the prompt bar and it saves images. It never presses generate,
never clicks `--oref`, never navigates.

```bash
python3 mj_server.py            # http://127.0.0.1:8765, loopback only
```
Then install `mj-overlay.user.js` in Tampermonkey and open midjourney.com.

The working loop (V8.2): pick an NPC in the panel → click the anchor shot (prompt
bar fills) → enter → on the grid image you like hit **Quick Edit**, which
attaches it with the role *Attach to prompt* → click the next shot → enter.
Saving is manual for now; see below.

### Do not use Omni Reference on V8.2

`--oref` still appears on older jobs and still works, but **a prompt carrying
`--oref` renders in V7.** The anchor would come back as 8.2 and the ref shots as
7, with nothing in the UI saying so, and the set would quietly fail to match.

The **Edit Model** replaced it in V8.2, absorbing Omni Reference, Character
Reference and Retexture. It takes up to 4 reference images, reached by Quick
Edit on an image, dragging into the prompt bar, the Edit tab, or `--edit <url>`.
Attaching offers three roles: *Attach to prompt* (the `--oref` successor, and
the one this flow wants), *Style reference*, and *Image Prompts*.

### Ref-shot prompts are compact, deliberately

Midjourney shows a **"Long Prompt"** warning past roughly 150 words. Measured by
bisection on the live prompt bar (2026-09-13): 148 words is clean, 152 warns.

`npc_art.prompt_for` repeats `character` and `wardrobe` in every shot. That is
right for fal, whose edit endpoint leans on the words, and wrong here: the
attached image *is* the identity, so the description is redundant and it was
most of a 175-word prompt. `ref_prompt()` builds ref shots from the KEEP clause,
the framing, and a shortened recompose line only.

Result on this roster: ref shots fell from ~175 words to 61–76, anchors sit at
105–125, and no shot trips the warning. Every shot in the `/prompts` response
carries `words` and `long`, and the panel prints the count and flags anything
over budget.

- **Same prompts as the other two renderers.** It builds through
  `npc_art.prompt_for` with `fal_art`'s `RECOMPOSE`, so Midjourney art comes out
  of the same `<slug>.set.json` rather than hand-retyped prose that drifts.
- **Style is off by default.** Midjourney carries the house look in a
  personalization profile (`--profile`), which the long style sentence competes
  with; the panel has a checkbox to add it back for a one-off.
- **No standing `--no` list.** A defensive `photo, 3d render, text, watermark`
  set was tried and dropped: the profile already holds the look, and the
  renderings showed none of the problems it guarded against. Exclusions for
  things that are not happening cost prompt weight and buy nothing.
- **Style negatives still become `--no`,** when the style *is* switched on.
  Left inline, "no oil paint texture" reads to Midjourney as a thing to *draw*,
  so `split_negatives()` lifts every `no …` clause into the flag.
  "non-photorealistic" stays in the prompt: it describes the rendering, it is
  not an exclusion. With style off there are no negatives and no flag is emitted.
- `--ar` comes from each shot's `size`. With the style off, that plus the
  description is the whole prompt.

### Save-back: built, working, and currently removed

A `⤓` button was drawn on each grid image and saved it into the spec folder. It
worked end to end, and it was **removed in v1.1**: drawn on the image, it sat on
top of the zoom view. The complaint was placement, not function.

`mj_server`'s `/save` endpoint is still live, and the userscript's history has
the client half, so re-wiring it to a control that does not overlap the image is
a small job rather than a rebuild. Everything it needs was measured on the live
site (2026-09-13):

- **The server cannot download the images.** `cdn.midjourney.com` serves a page
  fetch but answers a plain server-side one with **403**. The bytes must be read
  in the page and posted base64; `/save` takes bytes, not a URL. Do not
  "simplify" it back into a server-side download; it cannot work.
- **The page fetch must be bare.** Adding `credentials: 'include'` turns a
  working cross-origin read into `Failed to fetch`.
- **Full-resolution is `cdn.midjourney.com/<uuid>/0_<index>.png`,** derived from
  the job link. The rendered `<img>` is a 640 px webp thumbnail.
- **The feed is virtualised,** so anything attached per-image needs a
  `MutationObserver`; a one-shot pass decorates only what is on screen at load.

### The prompt bar is a React-controlled `<textarea>`

Assigning `.value` updates the DOM but not React's state, so the text vanishes
on the next render and submitting sends an empty prompt. Going through the
native value setter and dispatching an `input` event is what makes it stick
(verified on the live page: the fill survives a re-render).

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
