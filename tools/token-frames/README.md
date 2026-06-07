# Token Frames — shared Foundry VTT token-border library

Reusable, **world-wide** token-frame art for Foundry tokens, shared across every
campaign (most frames are universal: god-domains, regions/sub-regions, world
factions, monster types). The frame mechanism, full pipeline, and the
live-combat caution are documented in
[`../foundryExport/README.md`](../foundryExport/README.md) (the
"Token frames" section).

- **`faction-frames.json`** — the generation **prompts** (one `{slug, prompt}` per
  frame), rendered on a solid magenta field so `bake_token.py prep` can hue-key it
  to a transparent ring. It is the **recipe for making a _new_ frame** (and a record
  of each frame's design intent), **not** a way to reproduce the existing ones:
  image generation is non-deterministic, so re-rendering a prompt yields a
  *different* ring. The committed `.cut.png` / `.webp` are the canonical art.
- **`<slug>.webp`** — the raw magenta-field render (kept so a frame can be re-cut).
- **`<slug>.cut.png`** — the chroma-keyed transparent ring `bake_token.py bake` composites.

**Using a frame on a quest:** map each NPC actor to a frame `slug` in that quest's
`published/gm-notes/<campaign>/<quest>.token-map.json`, then
`bake_token.py batch --frames ../token-frames …`. Adding a new frame = one new
prompt here + render + prep; every campaign can then map to it.

**The frames** (map an actor to the slug in the quest's `token-map.json`; the committed `.cut.png` is what bakes):

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
