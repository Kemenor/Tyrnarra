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
  index.html                           ← landing page = world primer (cosmology)
  grand-gods.html                   ← the 13 bound gods (world-level)
  magic.html                           ← Magic & Faith — Four Schools, daily life, faith (world-level)

  talan/                               ← continent-level content
    talan.html                         ← continent overview (geography, three seas, all 13 domains)
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
    style-a.css                        ← Style A base (used by world-level pages: /, gods, magic)
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
| World (Tyrnarra) | root | `index.html` (cosmology), `grand-gods.html`, `magic.html` |
| Continent (Talan) | `/talan/` | `talan.html`, `history.html` |
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
Used for: the landing/cosmology, the 13 gods, magic — anything world-scale or mythic.

- **Source:** `/assets/style-a.css`. Page-specific tweaks (orb effects, soul bars) stay inline in the page itself.
- **Fonts:** Cinzel Decorative (page titles), Cinzel (labels, small caps), Crimson Pro (body)
- **Palette:** deep void (`--bg: #06060a`), purple/blue ambient gradients, gold accents (`--gold: #c8a84a`, `--gold-bright: #f0d080`), parchment text (`--text: #c8c4d8`), per-god accent colours
- **Signature elements:** animated starfield, god orbs that gently float, group dividers with sub-labels, expandable god cards with red `⚿ GM Secret` pills, planar-layer expandables
- **References:** `index.html` (cosmology landing), `grand-gods.html` (the pantheon), `magic.html`

### Style B — Grounded / Continent + Settlement-level
Used for: continent primer, domain pages, faction pages, town primers, district guides, NPC rosters, anything ground-level and lived-in.

- **Fonts:** Uncial Antiqua (page titles), Crimson Pro (body), Cinzel (labels/small caps)
- **Palette:** warm dark (`--bg: #0f0c08`), gold accents (`--gold: #c8900a`, `--gold-bright: #f0b020`), parchment text (`--text: #d0c8a8`), per-domain accent colour driven by the location's character
- **Signature elements:** parchment noise overlay, ornament dividers (`✦ · ✦ · ✦`), "At a Glance" facts panel, god-city callout boxes, sub-region grid cards
- **References:** `talan/talan.html` (continent overview), any of `talan/domains/<domain>/<domain>.html` (domain page), `talan/factions/adventurers-guild.html` (faction page)

### Shared conventions
- **Shared chrome lives in `/assets/`** (sidebar nav, Style A and Style B base CSS). Every page references it via `<link>` and `<script defer src>`. Page-specific styling stays inline.
- **Style A pages** (root world-level pages — landing, gods, magic) include `<link rel="stylesheet" href="/assets/style-a.css">`. This provides palette, fonts, starfield, header, group dividers, portal cards, god-card grid, secret pills, scale rows, info cards, and the planar-layer accents.
- **Style B pages** (everything under `/talan/`) include `<link rel="stylesheet" href="/assets/style-b.css">`. This provides palette, fonts, container/header/divider primitives, facts panel, gods-city callout, sub-region cards, domain accent classes, era cards, three-tier (amber/red) expandables, pill rows. Pages define `--domain-accent` in a small inline `<style>` when they want a custom accent.
- **Dark mode only.** All pages assume a dark background.
- **No build step.** Open in browser, it just works.
- **Mobile responsive.** Pages use `@media (max-width: 600px)` breakpoints — match this.
- **Tone in copy:** specific over generic. Small concrete details (the smell, the named NPCs, the inside-joke aside) over abstract worldbuilding.

---

## GitHub Pages setup

The site is live at **https://tyrnarra.kunkel.swiss** (custom domain, HTTPS enabled). Deploys automatically on push to `main` — no build step, no Actions workflow needed. `index.html` at the repo root is the landing page (the world primer / cosmology); sub-pages are reachable at their absolute paths (e.g. `/grand-gods.html`, `/magic.html`, `/talan/talan.html`, `/talan/domains/vindul/vindul.html`).

**Always use absolute paths in links** (starting with `/`). The sidebar is on every p