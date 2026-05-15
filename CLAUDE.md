# Tyrnarra — Worldbuilding Project

This repo is a personal worldbuilding project for the setting **Tyrnarra**. The deliverable is a static HTML site published via GitHub Pages. Pages are hand-crafted HTML; **shared chrome lives in `/assets/`** (sidebar nav, Style B base CSS) and is referenced via `<link>` and `<script defer src>` tags. Page-specific styling and unique content stay inline in the page itself.

---

## The naming convention (most important rule)

**For anything new you create**, follow this convention strictly:

- **Old or ancient things** — ruins, kingdoms, geographic features, deity names, anything pre-modern or "of the world itself" — are named by:
  1. Translating a meaningful word or phrase into **Basque** or **Icelandic**
  2. Then slightly altering it to represent linguistic drift over time

  Example: *"Ehizahar"* (Hunt domain of Hinka) comes from Basque *"ehiza"* (hunt) + *"zahar"* (ancient), naturally eroded to its current form. Drift can happen anywhere in the word, not just the end.

- **New or modern things** — recently founded institutions, contemporary city-states, modern organizations — are named **plainly in English** but they may have drifted lightly.

  Examples: *"Free City"* -> *"Frae City"*, *"Order of Steam"*, *"The Wayward Compass"*, *"Clearwater Exchange"*.

**When you coin a new name, always show your work**: note the source language, the literal meaning, and the drift step. Save it in `lore/glossary.md` so the etymology is preserved.

**Existing names predate this rule** — don't try to retrofit names that are already in the HTML pages (Forseti, Cronus, etc.). Just follow the rule going forward.

---

## File layout

The site is hierarchical: **Tyrnarra → Talan → Domains → Sub-Regions/Kingdoms → Settlements.** The folder tree mirrors the world. World-level (cosmic) content lives at root; continent-level content lives under `/talan/`.

```
/                                      ← GitHub Pages serves from here
  index.html                           ← landing page (curated portal + sidebar)
  tyrnarra-primer.html                 ← cosmology (world-level)
  tyrnarra-gods.html                   ← the 13 bound gods (world-level)

  talan/                               ← continent-level content
    talan.html                         ← continent overview (geography, three seas, all 13 domains)
    magic.html                         ← The Four Schools
    history.html                       ← Eras / timeline
    domains/                           ← the 13 god domains
      <domain>/<domain>.html           ← e.g. vindul/vindul.html — domain entry page
      <domain>/<sub-region>.html       ← optional: promoted sub-region with its own page
      <domain>/<settlement>/           ← settlement folder, when content warrants
        <settlement>.html
        <sub-location>.html            ← location within the settlement
        Quests/                        ← quests nest under their location
          quest-<slug>.html
    factions/                          ← independent organisations
      factions.html                    ← faction overview / taxonomy
      adventurers-guild.html
      mercenary-guild.html
      god-churches.html
      remnants.html

  assets/                              ← shared chrome (loaded by every page)
    site-nav.css                       ← sidebar styling
    site-nav.js                        ← sidebar HTML + behaviour (single source of truth)
    style-b.css                        ← Style B base (used by every page under /talan/)

  lore/                                ← markdown reference notes (NOT published)
    world-notes.md                     ← authoritative canon
    geography.md                       ← domain etymologies + sub-regions
    factions.md                        ← faction taxonomy + entries
    glossary.md                        ← coined names + etymologies
    timeline.md                        ← eras + dates
    site-inventory.md                  ← what's published + what's stub
    restructure-plan.md                ← phasing notes for the restructure
    sidebar-nav.md                     ← legacy snippet doc — superseded by /assets/

  CLAUDE.md                            ← this file
  README.md
  CNAME
```

**Layer-to-folder mapping:**

| World layer | Folder | Example |
|---|---|---|
| World (Tyrnarra) | root | `tyrnarra-primer.html`, `tyrnarra-gods.html` |
| Continent (Talan) | `/talan/` | `talan.html`, `magic.html`, `history.html` |
| Region (god domain) | `/talan/domains/<domain>/` | `/talan/domains/vindul/vindul.html` |
| Sub-region / Kingdom | section in domain page, or own file when promoted | `Thousand Kingdom` lives inside `zuzental.html` until it earns its own file |
| Settlement | folder under its domain | `/talan/domains/brauogi/millhaven/millhaven.html` |
| Sub-location of settlement | sibling file in settlement folder | `/talan/domains/brauogi/millhaven/lowspan.html` |
| Quest | `Quests/` inside settlement folder | `/talan/domains/brauogi/millhaven/Quests/quest-x.html` |
| Faction (independent org) | `/talan/factions/` | `/talan/factions/adventurers-guild.html` |
| God church | umbrella `god-churches.html`; promoted to its own file when content warrants | `/talan/factions/god-churches.html` |

**Conventions:**

- **Folder slugs** are lowercase ASCII with hyphens. Diacritics are stripped from slugs but kept in display titles.
- **Each settlement gets its own folder under its domain.** The folder's main page is named the same as the folder (`millhaven/millhaven.html`).
- **Sub-regions** start as sections inside the domain page. When one earns enough content, promote it to its own file in the domain folder (e.g. `zuzental/thousand-kingdom.html`). Don't create empty stub files for sub-regions that don't exist yet.
- **Kingdoms vs. sub-regions:** the term "sub-region" is the umbrella; some sub-regions are kingdoms (Thousand Kingdom, Order of Steam), others are geographic (Baerfrost), cultural (Tahu Tangata), or border territories (Azkamour). All live in the same place in the folder tree — the political type is a property, not a folder.
- **Quests** nest under `Quests/` within their settlement folder, named `quest-<slug>.html`.
- **World-level primers** (cosmology, the 13 gods) sit at the repo root.
- **`lore/`** is markdown reference — not published. Authoritative canon lives here. Use it to keep track of canon, names, and cross-references that don't need a polished HTML page yet.

---

## Persistent sidebar navigation

Every page references the shared sidebar by including two tags in `<head>`:

```html
<link rel="stylesheet" href="/assets/site-nav.css">
<script defer src="/assets/site-nav.js"></script>
```

The JS injects the sidebar markup into the DOM on page load and wires up the toggle, scrim, and Escape-to-close behaviour. The page declares its location with:

```html
<body data-page="vindul">
```

The sidebar reads `data-page` and highlights the matching link. If the page isn't in the sidebar (e.g. a settlement or sub-region page), just omit `data-page` or use any value — it'll silently fail to find a match and that's fine.

**To add or rename a page in the sidebar:** edit `/assets/site-nav.js` (the `NAV_HTML` array near the top). One file, one place. No find-and-replace.

**Sidebar scope:** the sidebar carries top-level structure only — World & Cosmos, Talan, Domains, Factions. Settlements and sub-region pages are accessed from their parent domain page, not from the sidebar.

---

## Two page styles (match the existing aesthetic)

The existing pages establish two visual modes. New pages should pick one and match it closely — don't invent a third style without asking.

### Style A — Cosmic / World-level
Used for: world primers, cosmology, planar structure, deity overviews, anything mythic in scope.

- **Fonts:** Cormorant Garamond (body), Cormorant SC (headings, small caps), IM Fell English (accent)
- **Palette:** deep void/astral backgrounds (`--void: #04060f`, `--deep: #080d1e`), gold accents (`--gold: #c8a84b`, `--gold-bright: #f0d080`), cloud-white text (`--text: #d4cbb8`)
- **Signature elements:** animated starfield background, celestial orbs, planar-layer color coding (prelife purple, life green, postlife red)
- **Reference:** `tyrnarra-primer.html`

### Style B — Grounded / Continent + Settlement-level
Used for: continent primer, domain pages, faction pages, town primers, district guides, NPC rosters, anything ground-level and lived-in.

- **Fonts:** Uncial Antiqua (page titles), Crimson Pro (body), Cinzel (labels/small caps)
- **Palette:** warm dark (`--bg: #0f0c08`), gold accents (`--gold: #c8900a`, `--gold-bright: #f0b020`), parchment text (`--text: #d0c8a8`), per-domain accent colour driven by the location's character
- **Signature elements:** parchment noise overlay, ornament dividers (`✦ · ✦ · ✦`), "At a Glance" facts panel, god-city callout boxes, sub-region grid cards
- **References:** `talan/talan.html` (continent overview), any of `talan/domains/<domain>/<domain>.html` (domain page), `talan/factions/adventurers-guild.html` (faction page)

### Shared conventions
- **Shared chrome lives in `/assets/`** (sidebar nav, Style B base CSS). Every page references it via `<link>` and `<script defer src>`. Page-specific styling stays inline.
- **Style B pages** (everything under `/talan/`) also include `<link rel="stylesheet" href="/assets/style-b.css">` — this provides the palette, fonts, container/header/divider primitives, facts panel, gods-city callout, sub-region cards, and the domain accent classes. The page only needs to define `--domain-accent` in a small inline `<style>` if it wants a custom accent.
- **Style A pages** (root cosmic primers) keep their unique styling inline. They only reference `/assets/site-nav.css` and `/assets/site-nav.js`.
- **Dark mode only.** All pages assume a dark background.
- **No build step.** Open in browser, it just works.
- **Mobile responsive.** Pages use `@media (max-width: 600px)` breakpoints — match this.
- **Tone in copy:** specific over generic. Small concrete details (the smell, the named NPCs, the inside-joke aside) over abstract worldbuilding.

---

## GitHub Pages setup

The site is live at **https://tyrnarra.kunkel.swiss** (custom domain, HTTPS enabled). Deploys automatically on push to `main` — no build step, no Actions workflow needed. `index.html` at the repo root is the landing page; sub-pages are reachable at their absolute paths (e.g. `/tyrnarra-primer.html`, `/talan/talan.html`, `/talan/domains/vindul/vindul.html`).

**Always use absolute paths in links** (starting with `/`). The sidebar is on every page and the navigation works the same regardless of depth — relative paths would break it.

---

## Working notes

- **HTML files can be edited freely.** Everything is in git, so changes are safe and reversible. No need to surface diffs before editing.
- **When in doubt about canon**, check `lore/world-notes.md`, `lore/glossary.md`, and `lore/timeline.md` first, then read the relevant primer HTML, then ask.
