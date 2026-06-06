# The Campaign Layer (`/campaigns/`)

GM / table material for running actual campaigns. **Everything under `/campaigns/` is GM-only.** It lives in the repo but is deliberately **unlinked from the player sidebar** (`assets/site-nav.js` never references it), so it does not appear in normal player navigation. It is still served by GitHub Pages at its (unguessed) URLs; treat it as behind the screen, not as secret-from-the-internet.

This is the home for the things CLAUDE.md keeps *out* of the published site: quests, stat blocks, read-aloud boxes, adventure hooks, hidden-location detail, and GM-tier mechanisms. The published worldbuilding pages stay chronicler-tier and player-facing; their GM truths live in `⚿` boxes; the *campaign* truths and table-prep live here.

The **Furrious Five** layer (`/campaigns/furrious-five/`) is the reference implementation.

---

## Folder layout

```
campaigns/
  index.html                  ← base landing: what the layer is + a card per campaign
  assets/                     ← shared GM chrome (loaded by every campaign page)
    gm.css                    ← GM stylesheet ("behind the screen": ink-slate ground, red GM accent)
    gm.js                     ← shared interactions (tabs, secrets, NPC cards, floorplans, battlemap)
    gm-nav.css / gm-nav.js    ← GM left-sidebar drawer (its own tree; NOT the player site-nav)
  tools/                      ← GM utilities
    map-area-editor.html      ← draw clickable areas on a battlemap → export JSON (see below)
  map-library/                ← reusable map catalogues, shared across campaigns
    magirail-stock.md         ← modular train-car library (Tom Cartos "Steam Train" set)
  <campaign>/                 ← e.g. furrious-five/
    index.html                ← campaign hub (links the town notes, dossiers, quests)
    <town>-gm.html            ← GM town notes (read-aloud, tone, districts, council, NPCs, rumours)
    <location>-gm.html        ← location dossiers (floorplans + stat blocks + secrets + hooks)
    quest-<slug>.html         ← adventure modules
    assets/maps/              ← downsized web map copies (committed)
      _full/                  ← FULL-RES originals, gitignored — see "Map assets" below
```

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

Clicking any hotspot renders `n`/`t` into `#mapDetail` and highlights **every** `.map-hot` sharing that `data-area` key. Area outlines + numbers show by default; a `.map-toggle` button hides them. An area can span several rectangles (L / T / plus shapes): give each rectangle a `.map-hot` with the **same `data-area`** and put the `hot-num` badge on only the first. Reference implementation: the **Cavern Map** tab on `furrious-five/quest-venomqueen.html`.

### Map Area Editor (`tools/map-area-editor.html`)

The companion authoring tool. Load a map PNG, draw / move / resize / delete rectangles, label + describe each area, reorder, and export JSON. An **area is a union of rectangles** (`{ label, desc, rects:[{left,top,width,height}] }`, all `%`); Shift+draw (or a row's `＋`) adds a piece to the selected area for irregular shapes. The exported JSON is what you hand back to generate the map tab's hotspot markup + `GM_MAP_AREAS` scaffold. Import is back-compatible with the old single-rect format.

## Map assets (subscription battlemaps stay local)

Subscription battlemaps (the user's CzePeku / Tom Cartos subscriptions, etc.) **must not be published**. Convention:
- Full-resolution originals (and any full downloaded pack folder, which often bundles extra art and Foundry module files) live in **`<campaign>/assets/maps/_full/`**, which is **gitignored** (`.gitignore`: `campaigns/**/assets/maps/_full/`). They stay on local disk only and never reach GitHub.
- The user supplies the full-res; **Claude generates the downsized ~800px web copy** (degraded reference, useless at table resolution) that sits directly in `maps/` and *is* committed; the page references that. ImageMagick does it in one line: `magick "<_full>/<original>" -resize 800x "<maps>/<slug>.webp"` (the committed maps are 800px-wide). Any subscription art a user drops loose in `maps/` should be moved into `_full/` before staging.

If you ever find a full-res original tracked outside `_full/`, untrack it (`git rm --cached`) and, for true removal, scrub it from history — subscription art on a public repo is the thing to avoid.

**Reusable map catalogues** live in `campaigns/map-library/` (e.g. `magirail-stock.md`, the modular train-car library). They are committed *text* descriptions of local-only art, so Claude can pick cars for a scene and stitch them into a consist (cars append on the uniform 14 × 5 grid; the composite downsizes to the committed web copy) without the source images ever being published.

---

## Working notes

- The campaign layer is **not** part of `docs/site-inventory.md`'s "published" rosters; it has its own roster section there flagged GM-only.
- Canon still wins: a campaign page may reference reconciled lore, but the lore files and player pages are the source of truth. When migrating older GM content, reconcile dead canon (place-names, gods, defunct neighbours) the same way you would for a published page.
- Campaign pages do not get the GM-Vetted badge (that is a player-page, prose/canon mark).
