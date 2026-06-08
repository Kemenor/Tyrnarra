# imageGen — NPC art generation (fal.ai)

Image generation for the campaign layer: turn text prompts into character art via
fal.ai (FLUX.2). Kept separate from [`../foundryExport/`](../foundryExport/README.md)
(which gets art *into* Foundry); this folder only **makes** the images.

Run commands from here; use `python` (not `python3`) on Windows.

- **Dependencies:** `pip install fal-client requests`
- **Key:** `FAL_KEY` env var, or `../keys/fal_key.txt` (gitignored; see [`../keys/`](../keys/README.md)).
- **Model:** `fal-ai/flux-2` (~$0.012/megapixel, ≈ $0.013 per 1024² image).

## `gen_portraits.py` — independent portraits from a portraits JSON

Batch-renders one square image per entry of a `{"portraits":[{slug,prompt}]}`
file (the per-quest `*.portraits.json`). Used for quest casts and for token-frame
art (rendered onto a magenta field, then cut + baked in `../foundryExport/`).

```
python gen_portraits.py --portraits <quest>.portraits.json --out <dir> --model fal-ai/flux-2 --ext webp
# --only slug1,slug2 for a subset; --force to overwrite; skips existing by default
```

## `gen_npc_set.py` — a consistent multi-shot set for ONE character

Renders a coherent set (e.g. portrait + full body + an in-scene shot) that stays
one character: a text-to-image **anchor** first (usually the full body), then the
other shots via FLUX.2's reference endpoint (`fal-ai/flux-2/edit`) with the anchor
passed as a reference image. A shot can set `"mode": "text"` for a fresh
composition the reference endpoint will not produce (e.g. a tight
head-and-shoulders portrait, which it otherwise refuses to crop to).

Driven by a co-located set-spec JSON (`<slug>.set.json`): shared
`character` / `wardrobe` / `style` blocks reused in every shot, plus per-shot
`file` / `size` / `framing` (+ optional `mode`). Reference spec:
`published/gm-notes/furrious-five/assets/portraits/sable-rei.set.json`.

```
python gen_npc_set.py --spec <path>/<slug>.set.json --force
# --only shot1,shot2 for a subset (the on-disk anchor is uploaded as the reference)
```

## `mj_prompts.py` — Midjourney prompts (no API), for parallel testing

Emits ready-to-paste Midjourney `/imagine` prompts from the **same `*.set.json`**,
so you can test a character in Midjourney alongside the fal render and compare. It
calls nothing and needs no key; you paste the prompts manually.

```
python mj_prompts.py --spec <path>/<slug>.set.json
# after rendering the anchor, bake its omni-reference into the other shots:
python mj_prompts.py --spec <path>/<slug>.set.json --anchor-url <anchor image URL>
# --profile <id>; --version 8.1; --stylize 250; --ow 400; --artists "Brom, Donato Giancola"
```

It maps each shot's `size` to `--ar` and adds `--v` and `--raw`, plus any of `--s`,
`--profile`, and `--no` that are set. For a **consistent set**, Midjourney's
character lock is the omni-reference (`--oref <image URL> --ow 0-1000`, **V7-only**):
generate the anchor shot first, then pass `--anchor-url <its URL>` to bake
`--oref … --ow` into the other shots (or append it by hand / drag the anchor image
in). With no anchor URL given, the output prints the hint per shot instead.

### Config layers (each overrides the previous)

1. the spec's top-level **fal** fields,
2. **`mj.defaults.json`** (here) — house-wide MJ settings shared by every character:
   your personalization `profile`, default `style`, `version`, `raw`, `ow`,
3. the spec's optional **`mj` block** — per-character overrides,
4. **CLI flags**.

So your profile and house style live once in `mj.defaults.json`; a character's `mj`
block only carries what is specific to it. With a profile set, the profile carries
the look, so you usually drop artists and heavy style strings; negatives (`--no`)
and artists are **off unless set**.

**Beast ancestries (the `mj` block).** Midjourney reads "kitsune", "tengu",
"catfolk" as a human with animal features, not the PF2e anthro folk that FLUX
renders. Give such a character an `mj` block with anthro/furry phrasing so it reads
as fox-folk, not a human with fox ears:

```json
"mj": {
  "character": "an anthropomorphic fox character (anthro, furry), a bipedal humanoid fox-folk, full muzzle, fur over the whole face and body, ..."
}
```

`mj.character` / `mj.wardrobe` / `mj.style` / `mj.artists` / `mj.profile` /
`mj.version` / `mj.stylize` / `mj.negative` / `mj.ow` override the fal text **for
Midjourney only**; the fal pipeline ignores the block. Worked example:
`sable-rei.set.json` (anthro `character`) + `mj.defaults.json` (profile + style).

**No profile? Ground it manually.** Name painter anchors via `mj.artists` (or
`--artists "Brom, Donato Giancola"`) and add cartoon-pushing negatives
(`--negative "cartoon, cel shaded, flat colors, chibi"`). With a personalization
profile, the profile carries the look and you can skip both.

Generated art **is committed** (generation is non-deterministic, so the prompts
alone can't reproduce the exact approved images). Downstream Foundry steps
(upload to Forge, token frames, assign) live in
[`../foundryExport/`](../foundryExport/README.md).
