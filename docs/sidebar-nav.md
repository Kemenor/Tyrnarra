# Sidebar Navigation — Architecture

How the persistent sidebar on every page is built and how to extend it.

---

## How it works

- The sidebar structure lives in `/assets/site-nav.js`. Three data sources drive it:
  - **`TALAN_PAGES`** — the array of continent-level reference pages (History, The Binding, Bestiary, Historical). Each entry has a `slug`, `label`, `href`, and a `children` list of nested pages. Same accordion shape as `DOMAINS`. The Continent Overview is intentionally not in this list — it is the Talan section's own clickable header.
  - **`DOMAINS`** — the array of 13 god-domains. Same shape: `slug`, `label`, `href`, `children`.
  - **The remaining top-level section markup** (World & Cosmos, Factions, Off-Continent) — string literals inside `buildNavHtml()`.
- The sidebar styling lives in `/assets/site-nav.css`.
- Every page references both via two tags in `<head>`:

  ```html
  <link rel="stylesheet" href="/assets/site-nav.css">
  <script defer src="/assets/site-nav.js"></script>
  ```

- On `DOMContentLoaded`, the script builds the sidebar markup from the data arrays, injects it as the first child of `<body>`, then wires up the toggle button, the scrim, the Escape-key handler, the `.is-current` highlight, and the accordion chevrons.

### Section headers are clickable

Each of the five section headers in the sidebar is itself a link to that section's hub page, not a passive label:

| Section | Header links to | `data-page` |
|---|---|---|
| World & Cosmos | `/index.html` (Cosmology) | `cosmology` |
| Talan | `/talan/talan.html` (Continent Overview) | `talan` |
| Domains | `/talan/domains/domains.html` (Domains hub) | `domains-hub` |
| Factions | `/talan/factions/factions.html` (All Factions) | `factions` |
| Off-Continent | `/off-continent/off-continent.html` (Off-Continent hub) | `off-continent-hub` |

Because the header itself carries the link, the hub page is **not repeated as a leaf item** inside the section's list. The `.nav-section-label.nav-section-link` styling picks up `.is-current` highlight the same way `.nav-list a` does — when on the hub page, the header lights up gold.

The page tells the sidebar which entry to highlight with:

```html
<body data-page="vindul">
```

If the page isn't in the sidebar (e.g. a settlement or sub-region page), just omit `data-page` or use any value — no match is found and nothing breaks.

---

## How `data-page` works

- The JS reads `document.body.getAttribute('data-page')`.
- It finds the matching link in the sidebar via `a[data-page="..."]`.
- Adds `.is-current` to highlight it.

The slug doesn't have to match the filename — it just has to match between the page's `<body data-page="...">` and a sidebar link's `data-page="..."` attribute.

---

## How to extend the nav

All edits happen in `/assets/site-nav.js`; the new page sets `<body data-page="<slug>">` matching the entry. Pick the spot that fits:

- **A continent-level reference page** (Talan-tier — like Historical, Bestiary): add an entry to `TALAN_PAGES`.
- **A nested accordion entry** under a domain or Talan-tier page: push `{ slug, label, href }` into the parent's `children` array in `DOMAINS` or `TALAN_PAGES`.
- **A new leaf under a fixed section** (World & Cosmos, Factions, Off-Continent): add a `<li>` to the matching string-literal block inside `buildNavHtml()`.

The accordion (used by both `TALAN_PAGES` and `DOMAINS`):
- Shows a chevron `▸` next to any row with non-empty `children`.
- Auto-expands when the current page is either the parent itself or one of its nested children (visiting Myrria opens the Myrkono submenu; visiting Myrkono opens it too).
- Toggles on chevron click. The parent name stays a normal link — clicking it navigates rather than expanding.

One file edited. No find-and-replace across pages.

---

## Mobile + accessibility

- The sidebar slides in from the left on toggle click, covers the page with a scrim, and closes on Escape, scrim click, or another toggle click.
- On mobile (`max-width: 600px`) the sidebar occupies 86% of viewport width.
- Body content does **not** shift when the sidebar opens — the sidebar overlays the page. This avoids rewriting every existing page's layout.

---

## Scope

The sidebar carries five sections, each with its own clickable header (see *Section headers are clickable* above):

- **World & Cosmos** — Cosmology, the 13 Bound Gods, Magic & Faith.
- **Talan** — continent-level reference pages (History, The Binding with nested dungeons, Bestiary, Historical with nested fallen civilisations).
- **Domains** — the 13 god-domains, each with an optional accordion of promoted sub-region and settlement pages.
- **Factions** — independent organisations (Adventurers Guild, Mercenary Guild, God Churches, Remnants).
- **Off-Continent** — non-Talan continents and powers (Sortalde, Red Empire).

To avoid bloat, only **promoted** sub-regions get a sidebar entry — those with their own HTML page (Fenurra, Emarrea, Myrria, etc.). Sub-regions and settlements that exist only as cards or sections on a domain page are not in the sidebar — visitors reach them via the parent domain page.

---

## Other shared assets in `/assets/`

The sidebar isn't the only thing extracted from per-page inline code. Two other shared scripts live alongside `site-nav.js`:

- **`site-interactions.js`** — shared click handlers for the three-tier knowledge widgets and the history-page era cards. Exposes `toggleSecret`, `toggleEraSecret`, `toggleEraLegend`, `toggleEra` on `window`, so the existing inline `onclick="toggleEraSecret(event, this)"` attributes on each page work unchanged. The toggles snapshot the button's initial `innerHTML` on first click via `data-original`, so each page's exact button copy is preserved — no JS-side hardcoding of label text. A per-button `data-hide-label="…"` attribute overrides the default open-state label if a page wants a shorter form.

  Include it on any page that uses `onclick="toggle*"`:
  ```html
  <script defer src="/assets/site-interactions.js"></script>
  ```

- **`site-starfield.js`** — generates the ambient star field for Style A "cosmic" pages. Picks up `<div class="starfield" id="starfield" data-stars="180"></div>` and fills it. `data-stars` is optional (defaults to 180). No-ops on pages without the placeholder, so it is safe to include anywhere — but is only included on the three Style A pages today (`index.html`, `grand-gods.html`, `magic.html`).

  ```html
  <script defer src="/assets/site-starfield.js"></script>
  ```

The `.open-canon` panel (dashed TBD-inventory box at the bottom of several pages) lives as a shared rule in `style-b.css` — pages just write `<div class="open-canon">…</div>` and the panel inherits the page's `--domain-accent` for the heading colour and border edge.

### Two utility families in `style-b.css`

- **`.accent-card`** — shared shell for the many "panel with an accent edge" cards across the site. Provides background, border-radius, and a left-stripe (or full border via `.framed`). Customise per card by setting two CSS variables:
  - `--card-bg` — background colour (defaults to warm dark)
  - `--card-accent` — stripe / border colour (falls through to `--domain-accent` then `--gold`)
  
  Modifiers: `.thin` (3px stripe instead of 4px), `.framed` (full 1px border, replaces the left stripe), `.outlined` (subtle 1px frame on top/right/bottom *plus* the left stripe — set `--card-outline` for the frame colour), `.cut-left` (sharp left corners / rounded right — pairs naturally with the left-stripe look), `.is-link` (clickable card with hover lift). Pages keep their own semantic class (`.dom-card`, `.hazard-card`, `.isle-card`, etc.) for padding/margin/max-width — the base only owns the shape, not the size.

  Usage:
  ```html
  <a class="accent-card is-link dom-card d-vindul">…</a>
  <div class="accent-card framed continent-card c-sortalde">…</div>
  <div class="accent-card thin service-card">…</div>
  ```

- **`.two-column`** — side-by-side 1fr 1fr grid that collapses to a single column under 800px. Used for opposing-positions blocks (bloodline pair, faith-vs-forseti tension, mining-and-fall narrative). Children carry their own styling.

  Usage:
  ```html
  <div class="two-column">
    <div class="accent-card bloodline bloodline-elf">…</div>
    <div class="accent-card bloodline bloodline-human">…</div>
  </div>
  ```
