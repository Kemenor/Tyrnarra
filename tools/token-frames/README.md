# Token Frames — shared Foundry VTT token-border library

Reusable, **world-wide** token-frame art for Foundry tokens, shared across every
campaign (most frames are universal: god-domains, regions/sub-regions, world
factions, monster types). The downstream pipeline (how a frame is baked onto a
portrait, uploaded, and assigned, plus the **live-combat caution**) lives in
[`../foundryExport/README.md`](../foundryExport/README.md), *Token frames* section.
**This file is the guide to authoring a _new_ frame** (the part Claude usually does).

## How a frame works (the chroma trick)

A frame is a thin ornate ring with a transparent centre, composited around a
circular portrait. To get clean transparency out of an image model, the ring is
rendered on a **solid magenta field** (background *and* centre), then
`bake_token.py prep` hue-keys the magenta away, leaving only the ring band with
real transparency. So the whole job of the prompt is: *produce only the ring, on
magenta, nothing else.*

## Files here

- **`faction-frames.json`** — the generation **prompts** (one `{slug, prompt}` per
  frame). This is the **recipe for a new frame** and a record of each frame's
  design intent; it is **not** a way to reproduce the existing ones (image
  generation is non-deterministic, so re-rendering a prompt yields a *different*
  ring). The committed `.cut.png` / `.webp` are the canonical art. Safe to re-run:
  `gen_portraits.py` **skips any slug whose file already exists**, so adding an
  entry and re-rendering only produces the new one.
- **`<slug>.webp`** — the raw magenta-field render (kept so a frame can be re-cut).
- **`<slug>.cut.png`** — the chroma-keyed transparent ring; what `bake_token.py bake` composites.

## The frames

(map an actor to the slug in the quest's `token-map.json`; the committed `.cut.png` is what bakes)

| Frame | Kind | For |
|---|---|---|
| `lautara` | domain | Lautara (Commerce / Jianna) — caravan-silk, the two hands |
| `rika-tikur` | sub-region | Rika Tikur plutocracy — trade-coins, scales, brass |
| `dreaming-cape` | sub-region | the Dreaming Cape — twin moons, twin-flame lantern |
| `itsasalda` | sub-region | Itsasalda harbour — rope, anchor, tide-marks, the watching eye |
| `millhaven` | settlement | Millhaven — mill-wheel, bridge, river |
| `wayward-compass` | location | the Guild Office — compass-rose, sextant + dividers |
| `crypt` | monster / theme | undead & funerary — gravestone, bone, ghost-light |
| `brood` | monster | spiders — chitin, web, violet egg-glow |
| `sable-rei` | faction | the Sable-rei (Millhaven & *Below the Quiet Docks*) — fox + theatrical-mask |
| `lautara-tilework` | parked variant | unused Lautara alt — Samarkand tilework (art kept; not in faction-frames.json) |

## Authoring a new frame

### 1. Write the prompt

Every frame uses the **same fixed boilerplate**; you change only the **motif
clause** (`{MOTIF}` below). The boilerplate is what makes the chroma-key clean, so
keep it verbatim:

> A single thin ornate circular token-border ring, floating on a completely solid flat pure magenta (#ff00ff) background that ALSO fills the entire circular center of the ring, so the only non-magenta thing in the image is the slim decorative ring band itself. The ring: **{MOTIF}**, thin band, perfectly centered, symmetrical, top-down flat view. No portrait, no scene, nothing inside the ring - just pure magenta. No text.

**Rules that keep it bakeable (do not drop any):**
- magenta `#ff00ff` is **both** the background **and** the ring's centre; the only non-magenta pixels are the ring band;
- a **thin** band, **perfectly centered**, **bilaterally symmetric**, **top-down flat** view;
- **no** portrait, face, creature, scene, or **text** anywhere; just the ring on magenta.

**Designing the motif** (the one creative part): choose **2–4 signature visual
elements** plus a **tight palette** that reads instantly as the place / faction /
monster, and keep it a *border*, never a scene. Rules of thumb:
- **place** (domain / sub-region / settlement) → its landmark features in the domain's palette (a harbour → rope, anchor, tide-marks in sea-green and brass);
- **faction** → its emblem, trade, or craft (commerce → coins, scales, ledger-knots in gold and brass);
- **monster / theme** → its body or material (spiders → chitin, web, egg-glow; undead → bone, grave-stone, ghost-light).

**Worked motif examples** (lifted from `faction-frames.json`):
- **`dreaming-cape`** (sub-region): *a dream-coast border, twin moons (one bright, one dark) and a twin-flame lighthouse lantern amid drifting dream-mist, in pale silver, mother-of-pearl and moonlit deep blue.*
- **`wayward-compass`** (location): *a deep blue enamel band edged in gold; a large ornate gold compass-rose star at top, crossed brass sextant and dividers over a gold scroll-banner at bottom, gold vine filigree along the two sides; bilaterally symmetric.*
- **`brood`** (monster): *chitinous black carapace with spider legs, webbing and faint violet egg-glow.*

Add the finished prompt as a new `{ "slug": "...", "prompt": "..." }` entry in
`faction-frames.json`.

### 2. Render, cut, map

Run these from **`tools/foundryExport/`** (where the scripts live); the paths are
relative to there, and the fal key must be set (`fal_key.txt` or `$env:FAL_KEY`):

```powershell
# render ONLY the new slug (existing frames are skipped, so they are never re-rolled)
python gen_portraits.py --portraits ../token-frames/faction-frames.json --out ../token-frames --ext webp --only <slug>
# chroma-key the magenta field down to a transparent ring
python bake_token.py prep --in ../token-frames/<slug>.webp --out ../token-frames/<slug>.cut.png
```

Eyeball `<slug>.cut.png` (the centre and corners should be fully transparent, only
the band visible). To deliberately re-roll an existing frame, add `--force` to the
render. Then map an actor to the new `<slug>` in the quest's
`published/gm-notes/<campaign>/<quest>.token-map.json` and batch-bake
(`bake_token.py batch --frames ../token-frames …`); the full bake / upload / assign
pipeline is in [`../foundryExport/README.md`](../foundryExport/README.md). Finally,
add the new row to **The frames** table above.
