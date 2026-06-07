# Sidebar Navigation: Architecture

How the persistent sidebar on every page is built and how to extend it.

---

## How it works

- The sidebar structure lives in `/assets/site-nav.js`. **Every section is a data-driven array** of `{ slug, label, href, children }` nodes, rendered by the recursive `buildAccordionRow`; there is no hand-written `<li>` nav markup anymore. One array per section:
  - **`WORLD_PAGES`**: World & Cosmos. A **Gods & Powerful Beings** group (→ `gods.html` hub) nests the four divine-roster pages by planar layer: The Primordials (Prelife), The 13 Bound Gods (Material), Layer-3 Gods (Postlife), and Bolverk (the Abyss megacity). Alongside it sit the Gods' Law, Magic, and PF2e Registrar.
  - **`TALAN_PAGES`**: continent-level reference pages (Maps, History, The Binding, Ancestries, Historical).
  - **`DOMAINS`**: the 13 god-domains and their promoted sub-regions / settlements.
  - **`FACTION_PAGES`**: the cross-domain organisations.
  - **`OFFCONTINENT_PAGES`**: Sortalde, the Red Empire.

  Each section's `<div class="nav-section">` header (the clickable section-label) is still a small string literal in `buildNavHtml()`, but its `<ul class="nav-list">` body is rendered from the matching array.

  All five arrays are **recursive trees**; any `children` entry may itself carry a `children` array, and `buildExpandedSet` auto-expands the ancestor chain of the current page in any of them. The practical ceiling is around 4–5 levels (e.g. *Sumendar → Order of Steam → House Eisenhart*, or *Lautara → Dreaming Cape → Millhaven → Wayward Compass*) before sidebar labels start to wrap.
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

Because the header itself carries the link, the hub page is **not repeated as a leaf item** inside the section's list. The `.nav-section-label.nav-section-link` styling picks up `.is-current` highlight the same way `.nav-list a` does; when on the hub page, the header lights up gold.

The page tells the sidebar which entry to highlight with:

```html
<body data-page="vindul">
```

If the page isn't in the sidebar (e.g. a settlement or sub-region page), just omit `data-page` or use any value; no match is found and nothing breaks.

---

## How `data-page` works

- The JS reads `document.body.getAttribute('data-page')`.
- It finds the matching link in the sidebar via `a[data-page="..."]`.
- Adds `.is-current` to highlight it.

The slug doesn't have to match the filename; it just has to match between the page's `<body data-page="...">` and a sidebar link's `data-page="..."` attribute.

---

## How to extend the nav

All edits happen in `/assets/site-nav.js`; the new page sets `<body data-page="<slug>">` matching the entry. Pick the spot that fits:

- **A continent-level reference page** (Talan-tier, like Historical, Ancestries): add an entry to `TALAN_PAGES` with `children: []` if it has no nested pages yet.
- **A nested accordion entry** under a domain, Talan-tier page, *or any deeper node*: push `{ slug, label, href, children: [] }` into that node's `children` array. Children may themselves have children; the tree recurses to whatever depth you need.
- **A new leaf or nested entry in World & Cosmos, Factions, or Off-Continent**: add a `{ slug, label, href, children: [] }` entry to `WORLD_PAGES`, `FACTION_PAGES`, or `OFFCONTINENT_PAGES` respectively (same shape and nesting rules as `TALAN_PAGES`/`DOMAINS`). No string-literal markup is involved.

The recursive accordion (used by every section array):
- Shows a chevron `▸` next to any row whose `children` is non-empty, at any depth.
- On page load, walks the tree for the current `data-page` and **auto-expands the full ancestor chain**: visiting *House Eisenhart* opens *Sumendar → Order of Steam* so the whole path is visible. Every other branch stays collapsed by default.
- Toggles on chevron click. The label stays a normal link; clicking it navigates rather than expanding.
- Each `<li>` carries `data-depth="N"` (1 for top-level rows in a section, +1 per nested level). CSS uses this to step the indent (~14px per level), shrink the font-size, and dim the colour, so 4–5 levels read cleanly in a 280px sidebar.

One file edited. No find-and-replace across pages.

---

## Mobile + accessibility

- The sidebar slides in from the left on toggle click, covers the page with a scrim, and closes on Escape, scrim click, or another toggle click.
- On mobile (`max-width: 600px`) the sidebar occupies 86% of viewport width.
- Body content does **not** shift when the sidebar opens; the sidebar overlays the page. This avoids rewriting every existing page's layout.

---

## Scope

The sidebar carries five sections, each with its own clickable header (see *Section headers are clickable* above):

- **World & Cosmos**: Cosmology, the 13 Bound Gods, Magic & Faith.
- **Talan**: continent-level reference pages (History, The Binding with nested dungeons, Bestiary, Historical with nested fallen civilisations).
- **Domains**: the 13 god-domains, each with an optional accordion of promoted sub-region and settlement pages.
- **Factions**: independent organisations (Adventurers Guild, Mercenary Guild, God Churches, Remnants).
- **Off-Continent**: non-Talan continents and powers (Sortalde, Red Empire).

To avoid bloat, only **promoted** sub-regions get a sidebar entry: those with their own HTML page (Fenurra, Emarrea, Myrria, etc.). Sub-regions and settlements that exist only as cards or sections on a domain page are not in the sidebar; visitors reach them via the parent domain page.

---

## Other shared assets in `/assets/`

The sidebar isn't the only thing extracted from per-page inline code. Two other shared scripts live alongside `site-nav.js`:

- **`site-interactions.js`**: shared click handlers for the three-tier knowledge widgets and the history-page era cards. Exposes `toggleSecret`, `toggleEraSecret`, `toggleEraLegend`, `toggleEra` on `window`, so the existing inline `onclick="toggleEraSecret(event, this)"` attributes on each page work unchanged. The toggles snapshot the button's initial `innerHTML` on first click via `data-original`, so each page's exact button copy is preserved without JS-side hardcoding of label text. A per-button `data-hide-label="…"` attribute overrides the default open-state label if a page wants a shorter form.

  Include it on any page that uses `onclick="toggle*"`:
  ```html
  <script defer src="/assets/site-interactions.js"></script>
  ```

- **`site-starfield.js`**: generates the ambient star field for Style A "cosmic" pages. Picks up `<div class="starfield" id="starfield" data-stars="180"></div>` and fills it. `data-stars` is optional (defaults to 180). No-ops on pages without the placeholder, so it is safe to include anywhere, though it is only included on the three Style A pages today (`index.html`, `grand-gods.html`, `magic.html`).

  ```html
  <script defer src="/assets/site-starfield.js"></script>
  ```

### The favicon is injected by `site-nav.js`

`site-nav.js` also injects the favicon/manifest tags (`injectFavicon()`, runs immediately on load, before the nav is built), so the icon is wired in one place and applies to every page that loads the sidebar; no per-page `<head>` markup is needed. The favicon files live at the **site root** (not `/assets/`, by the web's favicon convention): `favicon.ico`, `favicon.svg`, the PNG size set (`favicon-16/32/48/64/96/128/180/192/256/512.png`), and `site.webmanifest`. A bare `/favicon.ico` at root is auto-requested by browsers as a no-JS baseline; the injected tags upgrade to the SVG / Apple touch icon / PWA manifest and set `theme-color` (`#101C3A`). GM campaign pages under `/gm-notes/` load `gm-nav.js` rather than `site-nav.js`; `gm-nav.js` mirrors the same `injectFavicon()` so the GM layer gets the full icon set too.

The `.open-canon` panel (dashed TBD-inventory box at the bottom of several pages) lives as a shared rule in `style-b.css`; pages just write `<div class="open-canon">…</div>` and the panel inherits the page's `--domain-accent` for the heading colour and border edge.

### Three utility families in `style-b.css`

- **`.card-grid` + `.card-name`**: the single most-repeated structure on the site, a responsive auto-fit grid of `.accent-card` items each headed by an uppercase Cinzel label over body prose. Before this existed, dozens of pages re-declared the identical pattern under bespoke names (`.gov-grid`/`.gov-card`/`.gov-name`, `.peoples-grid`, `.tier-grid`, `.craft-grid`, `.tension-grid`, …) plus matching `-name` and `-card p` clones. They all collapse to:

  ```html
  <div class="card-grid">
    <div class="accent-card">
      <div class="card-name">Label</div>
      <p>Body prose.</p>
    </div>
  </div>
  ```

  The grid wrapper, the label, and the body `<p>` are all styled by the shared rule. Tune a grid by setting CSS variables on `.card-grid` (inline, or via a tiny per-page marker rule): `--col-min` (min column width before wrap, default 230px), `--grid-gap` (default 14px), `--grid-max` (default 1000px), `--card-pad` (per-card padding, default 14px 16px). Recolour a single label with `--card-accent` on the card; resize it with `--card-name-size` on the label. **Rich cards** (those with extra sub-labels: a number row, an italic band, a sub-heading) keep those extra elements as their own page class and add a thin marker rule (`.X-grid { --col-min: … }`) on a `class="card-grid X-grid"` wrapper; only the grid / name / body trio collapses. Reference implementations: `dreaming-cape.html` (plain theory/tension grids + rich five-tier grid with colour-variant labels), `rika-tikur.html` (variant-coloured cards with role sub-labels). **Do not** use `.card-grid` for fixed-column "fact" grids (`grid-template-columns: 130px 1fr`), two-column `1fr 1fr` blocks (use `.two-column`), or clickable/framed link-card indexes (those keep their own grid + card classes).

- **`.accent-card`**: shared shell for the many "panel with an accent edge" cards across the site. Provides background, border-radius, and a left-stripe (or full border via `.framed`). Customise per card by setting two CSS variables:
  - `--card-bg`: background colour (defaults to warm dark)
  - `--card-accent`: stripe / border colour (falls through to `--domain-accent` then `--gold`)
  
  Modifiers: `.thin` (3px stripe instead of 4px), `.framed` (full 1px border, replaces the left stripe), `.outlined` (subtle 1px frame on top/right/bottom *plus* the left stripe; set `--card-outline` for the frame colour), `.cut-left` (sharp left corners / rounded right, pairing naturally with the left-stripe look), `.is-link` (clickable card with hover lift). Pages keep their own semantic class (`.dom-card`, `.hazard-card`, `.isle-card`, etc.) for padding/margin/max-width; the base only owns the shape, not the size.

  Usage:
  ```html
  <a class="accent-card is-link dom-card d-vindul">…</a>
  <div class="accent-card framed continent-card c-sortalde">…</div>
  <div class="accent-card thin service-card">…</div>
  ```

- **`.two-column`**: side-by-side 1fr 1fr grid that collapses to a single column under 800px. Used for opposing-positions blocks (bloodline pair, faith-vs-forseti tension, mining-and-fall narrative). Children carry their own styling.

  Usage:
  ```html
  <div class="two-column">
    <div class="accent-card bloodline bloodline-elf">…</div>
    <div class="accent-card bloodline bloodline-human">…</div>
  </div>
  ```
