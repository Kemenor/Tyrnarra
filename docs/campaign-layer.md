# The Campaign Layers (GM `/gm-notes/` + player `/player-campaigns/`)

There are **two** campaign trees: the GM-only `/gm-notes/` and the player-facing, published `/player-campaigns/`. The split is detailed in *Two campaign layers* below; this intro and the next two paragraphs cover the GM tree.

GM / table material for running actual campaigns. **Everything under `/gm-notes/` is GM-only.** It lives in the repo but is deliberately **unlinked from the player sidebar** (`published/setting/assets/site-nav.js` never references it), so it does not appear in normal player navigation. It is still served by GitHub Pages at its (unguessed) URLs; treat it as behind the screen, not as secret-from-the-internet.

This is the home for the things CLAUDE.md keeps *out* of the published site: quests, stat blocks, read-aloud boxes, adventure hooks, hidden-location detail, and GM-tier mechanisms. The published worldbuilding pages stay chronicler-tier and player-facing; their GM truths live in `⚿` boxes; the *campaign* truths and table-prep live here.

The **Furrious Five** layer (`/gm-notes/furrious-five/`) is the reference implementation.

---

## Two campaign layers: GM and player

There are **two** campaign trees, and they are different sides of the screen:

- **`/gm-notes/`** (this document) — **GM-only**, unlinked from the player sidebar, GM chrome (`gm.css` / `gm-nav.*`). Stat blocks, secrets, read-aloud, hooks, the floors below the floors.
- **`/player-campaigns/`** — **player-facing and published**, linked in the sidebar under its own **Campaigns** section. It is the players' companion to a running campaign: town/location handouts and an interactive **quest board**, with all GM-tier content stripped. It mirrors selected `/gm-notes/` material down to the player tier and cross-links out to the canonical worldbuilding pages for the world layer.

The player layer has its **own themeable chrome**, deliberately rooted in the GM look rather than the worldbuilding Style A/B:

- **`/player-campaigns/assets/campaign.css`** — shared base. Every visual token is a CSS variable with a default. Components: `.c-header`, `.section-heading`, the quest board (`.board` / `.quest-pin` / `.quest-detail`), the clickable room map (`.floor-stack` / `.room-cell` / `#roomDetail`), `.person-card`, `.reveal`, `.link-card`, `.callout`.
- **`/player-campaigns/assets/campaign.js`** — delegated interactions (no inline handlers): quest-board expand (`.quest-head` ↔ `.quest-detail`, `aria-expanded` tracked), the room map (`.room-cell[data-room]` renders `window.CAMPAIGN_ROOMS[key]` into `#roomDetail`; cells without `data-room` are inert, e.g. `.room-cell.locked`), and `.reveal` rumour toggles.
- **`/player-campaigns/assets/pc-nav.css` / `pc-nav.js`** — the layer's **own off-canvas menu**, separate from the world `/setting/assets/site-nav.*` (mirrors the GM `gm-nav.*` pattern: same drawer/toggle/scrim machinery, themed to `campaign.css`). The world/setting menu and the campaigns menu are not shared; each crosses to the other with a foot button (`site-nav`'s *Player Campaigns →* ↔ `pc-nav`'s *← The World · Setting*). Single source of truth for the campaigns menu is the `TREE` in `pc-nav.js`; slugs must match each page's `data-page`. The GM `/gm-notes/` tree is linked from neither.
- **Per-campaign theme** — one file, e.g. `/player-campaigns/furrious-five/theme.css`, loaded *after* `campaign.css`, overriding only the `--c-*` tokens (palette, accents, fonts, background glow). **One theme file = one campaign's entire look.** A new campaign drops its own `theme.css` beside its pages and gets a distinct skin on the same machinery. Pages load the layer's own menu (`/player-campaigns/assets/pc-nav.*`), not the world sidebar; only the page body is themed.

The room map is the player analogue of the GM floorplan: the GM `wayward-compass-gm.html` carries the full `GM_ROOMS` floor-stack including restricted rooms; the player `wayward-compass.html` carries a `CAMPAIGN_ROOMS` subset (accessible rooms only, player-safe text) with the off-limits doors shown as greyed `.locked` cells.

---

## Folder layout

```
published/gm-notes/             ← served at /gm-notes/ (the published/ prefix is stripped)
  index.html                  ← base landing: what the layer is + a card per campaign
  assets/                     ← shared GM chrome (loaded by every campaign page)
    gm.css                    ← GM stylesheet ("behind the screen": ink-slate ground, red GM accent)
    gm.js                     ← shared interactions (tabs, secrets, NPC cards, floorplans, battlemap)
    gm-nav.css / gm-nav.js    ← GM left-sidebar drawer (its own tree; NOT the player site-nav)
  tools/                      ← GM utilities served with the layer
    map-area-editor.html      ← draw clickable areas on a battlemap → export JSON (the only tool that stays here; see below)
  gm-reference/               ← GM quick-reference docs (system rules, not campaign-specific)
    dc-cheatsheet.md          ← PF2e DCs: challenge-anchored, simple, adjustments, four degrees
  <campaign>/                 ← e.g. furrious-five/
    index.html                ← campaign hub (links the town notes, dossiers, quests)
    <town>-gm.html            ← GM town notes (read-aloud, tone, districts, council, NPCs, rumours)
    <location>-gm.html        ← location dossiers (floorplans + stat blocks + secrets + hooks)
    quest-<slug>/             ← per-quest folder (one per adventure module)
      quest-<slug>.html       ← the module page (folder-named, like settlements)
      quest-<slug>.foundry.json / .foundry.macro.js   ← Foundry import spec + generated macro
      quest-<slug>.portraits.json / .token-map.json   ← NPC portrait prompts + actor→frame map
    assets/maps/              ← downsized web map copies (committed)
      _full/                  ← FULL-RES originals, gitignored — see "Map assets" below
    assets/portraits/         ← generated NPC portrait art (committed)
    assets/tokens/            ← baked token art (portrait + frame, committed)
```

The player-facing tree mirrors the same shape, with player chrome instead of GM chrome:

```
published/player-campaigns/     ← served at /player-campaigns/ (the published/ prefix is stripped)
  index.html                  ← section landing: what the layer is + a card per campaign
  assets/                     ← shared player chrome (loaded by every campaign page)
    campaign.css              ← shared base ("companion to the table": themeable via --c-* tokens)
    campaign.js               ← shared interactions (quest board, room map, reveal toggles)
    pc-nav.css / pc-nav.js    ← player off-canvas menu (its own tree; NOT the world site-nav)
  <campaign>/                 ← e.g. furrious-five/
    <campaign>.html           ← campaign hub (links the player location pages + quest board)
    <location>.html           ← player-tier location pages (GM content stripped)
    theme.css                 ← the per-campaign skin (overrides only the --c-* tokens)
```

The private GM build tooling lives **outside** the served tree, at repo-root `/tools/` (NOT served): `tools/encounterBuilder/` (PF2e encounter + loot builders over the Foundry pf2e data, driving the `pf2e-encounter` / `pf2e-loot` skills), `tools/foundryExport/` (quest spec → paste-and-run Foundry VTT import macro), `tools/map-library/` (reusable map catalogues shared across campaigns — `magirail-stock.md`, `stitch.py`, per-car `areas/`, local-only `_full/` source art), and `tools/token-frames/` (the shared Foundry token-frame library). Only `map-area-editor.html` remains under `published/gm-notes/tools/`, since it is a browser tool the GM opens like any other page.

## Chrome conventions

Every campaign page:
- Links `gm.css` + `gm-nav.css`, defers `gm-nav.js` + `gm.js`.
- Carries `<body data-page="<slug>">` so the GM sidebar highlights the current page.
- Opens with a `.gm-banner` ("⚔ GM Material · Behind the Screen · Not Player-Facing") and a link back to the relevant player page or the campaign hub.

**`gm-nav.js`** is the single source of truth for the GM sidebar tree (mirrors how `site-nav.js` works for the player site). Add or move a GM page there. Slugs must match the page's `data-page`.

**`gm.js`** wires behaviour by delegation (no inline `onclick` needed). Supported patterns: tabbed sections (`.gm-tab-btn` + `.gm-panel`), collapsible `.gm-secret`, expandable `.npc-card`, `.level-card` floor stacks, floorplan room cells (`.room-cell[data-room]` + `#roomDetail` + `window.GM_ROOMS`), and the clickable battlemap (below).

## The clickable battlemap

A quest page can carry a **map tab** where clicking an area expands its notes beneath the map. Styling is in `gm.css` (`.map-wrap` / `.map-hot` / `.map-detail`); behaviour is in `gm.js`. The page supplies only:

- the map `<img>` + one `.map-hot` button per rectangle (percentage-positioned), and
- `window.GM_MAP_AREAS = { key: { n: "1 · Title", t: "<p>notes html</p>" }, … }`.

Clicking any hotspot renders `n`/`t` into `#mapDetail` and highlights **every** `.map-hot` sharing that `data-area` key. Area outlines + numbers show by default; a `.map-toggle` button hides them. An area can span several rectangles (L / T / plus shapes): give each rectangle a `.map-hot` with the **same `data-area`** and put the `hot-num` badge on only the first. Reference implementation: the **Cavern Map** tab on `furrious-five/quest-venomqueen/quest-venomqueen.html`.

### Map Area Editor (`published/gm-notes/tools/map-area-editor.html`)

The companion authoring tool. Load a map PNG, draw / move / resize / delete rectangles, label + describe each area, reorder, and export JSON. An **area is a union of rectangles** (`{ label, desc, rects:[{left,top,width,height}] }`, all `%`); Shift+draw (or a row's `＋`) adds a piece to the selected area for irregular shapes. The exported JSON is what you hand back to generate the map tab's hotspot markup + `GM_MAP_AREAS` scaffold. Import is back-compatible with the old single-rect format.

## Foundry VTT export (`tools/foundryExport/`)

For tables run on Foundry VTT, `foundry_macro.py` turns a compact quest spec
(folder + monsters + NPCs + loot chests) into a **paste-and-run Foundry Script
Macro**. Run as GM, it creates the quest's actor folder, imports one actor per
distinct monster (the GM places *N* tokens), renames imported NPCs or makes a
blank `npc` for narrative-only ones, and builds a loot-actor "chest" per haul
with items + coins. It resolves everything **by name** from the world's own
compendiums, so it redistributes no Paizo data and always matches the installed
system version; it needs no module, relay, or API key and works on Forge-hosted
worlds. It is the **Phase 7** step of the `quest-workflow` skill and a standalone
tool you can run against any quest. Verified live on Foundry VTT 14.363 / pf2e
8.2.0. Full reference: [`tools/foundryExport/README.md`](../tools/foundryExport/README.md).

## Map assets (subscription battlemaps stay local)

Subscription battlemaps (the user's CzePeku / Tom Cartos subscriptions, etc.) **must not be published**. Convention:
- Full-resolution originals (and any full downloaded pack folder, which often bundles extra art and Foundry module files) live in **`<campaign>/assets/maps/_full/`**, which is **gitignored** (`.gitignore`: `published/gm-notes/**/_full/`). They stay on local disk only and never reach GitHub.
- The user supplies the full-res; **Claude generates the downsized ~800px web copy** (degraded reference, useless at table resolution) that sits directly in `maps/` and *is* committed; the page references that. ImageMagick does it in one line: `magick "<_full>/<original>" -resize 800x "<maps>/<slug>.webp"` (the committed maps are 800px-wide). Any subscription art a user drops loose in `maps/` should be moved into `_full/` before staging.

If you ever find a full-res original tracked outside `_full/`, untrack it (`git rm --cached`) and, for true removal, scrub it from history — subscription art on a public repo is the thing to avoid.

**Reusable map catalogues** live in `tools/map-library/` (e.g. `magirail-stock.md`, the modular train-car library). They are committed *text* descriptions of local-only art, so Claude can pick cars for a scene and stitch them into a consist (cars append on the uniform 14 × 5 grid; the composite downsizes to the committed web copy) without the source images ever being published. On a fresh clone the `_full/` art is restored from the user's private Proton Drive sync, not from git; see [`tools/map-library/README.md`](../tools/map-library/README.md).

---

## Working notes

- The campaign layer is **not** part of `docs/site-inventory.md`'s "published" rosters; it has its own roster section there flagged GM-only.
- Canon still wins: a campaign page may reference reconciled lore, but the lore files and player pages are the source of truth. When migrating older GM content, reconcile dead canon (place-names, gods, defunct neighbours) the same way you would for a published page.
- Campaign pages do not get the GM-Vetted badge (that is a player-page, prose/canon mark).
