# Token Frames — shared Foundry VTT token-border library

Reusable, **world-wide** token-frame art for Foundry tokens, shared across every
campaign (most frames are universal: god-domains, regions/sub-regions, world
factions, monster types). The frame mechanism, full pipeline, and the
live-combat caution are documented in
[`../tools/foundryExport/README.md`](../tools/foundryExport/README.md) (the
"Token frames" section).

- **`faction-frames.json`** — the prompts (one `{slug, prompt}` per frame),
  rendered on a solid magenta field so `bake_token.py prep` can hue-key it to a
  transparent ring.
- **`<slug>.webp`** — the raw magenta-field render (kept so a frame can be re-cut).
- **`<slug>.cut.png`** — the chroma-keyed transparent ring `bake_token.py bake` composites.

**Using a frame on a quest:** map each NPC actor to a frame `slug` in that quest's
`gm-notes/<campaign>/<quest>.token-map.json`, then
`bake_token.py batch --frames ../../token-frames …`. Adding a new frame = one new
prompt here + render + prep; every campaign can then map to it.

Current slugs: `sable-rei`, `brood`, `crypt`, `lautara`, `rika-tikur`,
`millhaven`, `dreaming-cape`, `itsasalda`, `wayward-compass` (+ the parked
`lautara-tilework` variant).
