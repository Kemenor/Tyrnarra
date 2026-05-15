# Tyrnarra — Worldbuilding Project

This repo is a personal worldbuilding project for the setting **Tyrnarra**. The deliverable is a static HTML site published via GitHub Pages. Pages are hand-crafted, single-file HTML with embedded CSS and JS — each page is its own self-contained artifact.

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

```
/                          ← GitHub Pages serves from here
  index.html               ← landing page (links to all primers)
  tyrnarra-primer.html     ← world cosmology
  tyrnarra-gods.html       ← the 13 bound gods
  talan-primer.html        ← the continent
  millhaven/               ← one folder per major settlement
    millhaven.html         ← settlement primer (entry point)
    lowspan.html           ← location within the settlement
    guildhall.html
    Quests/                ← quests are nested under their location
      quest-venomqueen.html
      quest-veldtmark.html
  lore/                    ← markdown reference notes (NOT published)
    glossary.md            ← coined names + etymologies
    (geography.md, factions.md, timeline.md as the world grows)
  CLAUDE.md                ← this file
  README.md
```

**Conventions:**
- Each settlement gets its own folder. The folder's main page is named the same as the folder (`millhaven/millhaven.html`).
- Sub-locations sit alongside the main page at the same level.
- Quests nest under `Quests/` within their settlement folder, named `quest-<slug>.html`.
- World/continent-level primers sit at the repo root.
- `lore/` is markdown for *my* reference — it does not get published to the site. Use it to keep track of canon, names, and cross-references that don't need a polished HTML page yet.

---

## Two page styles (match the existing aesthetic)

The existing pages establish two visual modes. New pages should pick one and match it closely — don't invent a third style without asking.

### Style A — Cosmic / World-level
Used for: world primers, cosmology, planar structure, deity overviews, anything mythic in scope.

- **Fonts:** Cormorant Garamond (body), Cormorant SC (headings, small caps), IM Fell English (accent)
- **Palette:** deep void/astral backgrounds (`--void: #04060f`, `--deep: #080d1e`), gold accents (`--gold: #c8a84b`, `--gold-bright: #f0d080`), cloud-white text (`--text: #d4cbb8`)
- **Signature elements:** animated starfield background, celestial orbs, planar-layer color coding (prelife purple, life green, postlife red)
- **Reference:** `tyrnarra-primer.html`

### Style B — Grounded / Settlement-level
Used for: town primers, district guides, NPC rosters, anything ground-level and lived-in.

- **Fonts:** Libre Baskerville (body), Philosopher (headings), Josefin Sans (labels, small caps)
- **Palette:** warmer/darker (`--bg: #0c0e0f`), gold accent (`--gold: #c89040`), per-district color coding driven by the location's character
- **Signature elements:** tabbed layout (Overview / Districts / Council / People / Hooks & Rumors / GM Notes), district strip header, NPC accordion cards, rumor pills with per-tag color, "Read Aloud" callout boxes
- **Reference:** `millhaven/millhaven.html`

### Shared conventions
- **Single-file HTML.** No external CSS/JS files. Fonts come from Google Fonts via `<link>` in the head.
- **Dark mode only.** All pages assume a dark background.
- **No build step.** Open in browser, it just works.
- **Mobile responsive.** Existing pages have `@media (max-width: 600px)` breakpoints — match this.
- **Tone in copy:** specific over generic. The Millhaven primer is the gold standard — small concrete details (the smell, the named NPCs, the inside-joke aside about the town's name) over abstract worldbuilding.

---

## GitHub Pages setup

The site is live at **https://tyrnarra.kunkel.swiss** (custom domain, HTTPS enabled). Deploys automatically on push to `main` — no build step, no Actions workflow needed. `index.html` at the repo root is the landing page; sub-pages are reachable at their relative paths (e.g. `/tyrnarra-primer.html`, `/millhaven/millhaven.html`).

---

## Working notes

- **HTML files can be edited freely.** Everything is in git, so changes are safe and reversible. No need to surface diffs before editing.
- **When in doubt about canon**, check `lore/world-notes.md`, `lore/glossary.md`, and `lore/timeline.md` first, then read the relevant primer HTML, then ask.
