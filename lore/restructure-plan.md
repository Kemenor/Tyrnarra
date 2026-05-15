# Site Restructure Plan

Authored 2026-05-15. The goal: turn a flat collection of HTML pages into a clearly hierarchical site that mirrors the world's own hierarchy (Tyrnarra → Talan → domains → kingdoms → settlements) with a persistent sidebar menu and obvious homes for every type of content.

**Status:** Phase 1 and Phase 2 complete. Phase 3 (settlements + sub-region promotion) ahead. `talan-primer.html` was deleted on 2026-05-15 after its content migrated.

---

## Guiding principles

- **The folder tree mirrors the world.** A reader who knows the world can guess the URL of any page.
- **Cosmos at root, geography under `/talan/`.** Cosmology and the gods are world-level (apply to all of Tyrnarra). Factions, magic, history, kingdoms, and settlements are continent-level and live under `/talan/`.
- **Hybrid sub-region handling.** Each domain page lists *all* its sub-regions inline (etymology, summary, pills). When a sub-region grows enough content to warrant its own page, it gets promoted to its own file in the domain folder. No empty stub files for sub-regions that don't exist yet.
- **Settlements live under their domain folder**, keeping the existing "folder per settlement" pattern from the original convention (`millhaven/` becomes `/talan/domains/brauogi/millhaven/`).
- **Single-file HTML still applies** — the sidebar nav is a self-contained snippet (inline HTML/CSS/JS) that every page includes. No external CSS/JS files. No build step.

---

## Final folder layout

```
/                                          ← GitHub Pages root
  index.html                               ← landing page (sidebar + curated portal)
  CNAME
  CLAUDE.md
  README.md

  tyrnarra-primer.html                     ← cosmos (world-level)
  grand-gods.html                       ← the 13 bound gods (world-level)

  /talan/                                  ← continent-level content
    talan.html                             ← continent overview (geography, three seas)

    magic.html                             ← the Four Schools (Talan-specific practice)
    history.html                           ← timeline / eras

    /domains/                              ← the 13 god domains
      vindul/
        vindul.html                        ← domain entry page (lists sub-regions inline)
        haizetsua.html                     ← promoted sub-region (future)
        baerfrost.html                     ← promoted sub-region (future)
      lautara/
        lautara.html
      myrkono/
        myrkono.html
      floteyn/
        floteyn.html
      sumendar/
        sumendar.html
      lioaru/
        lioaru.html
      brauogi/
        brauogi.html
        millhaven/                         ← settlement folder (when re-added)
          millhaven.html
          lowspan.html                     ← location within settlement
          /Quests/
            quest-veldtmark.html
      ezkudon/
        ezkudon.html
      egulon/
        egulon.html
      zuzental/
        zuzental.html
      nashavel/
        nashavel.html
      ehizahar/
        ehizahar.html
      askamira/
        askamira.html

    /factions/                             ← independent organisations
      factions.html                        ← faction overview / taxonomy
      adventurers-guild.html
      mercenary-guild.html
      god-churches.html                    ← umbrella + per-church notes
      remnants.html                        ← Remnants of Corruption

  /lore/                                   ← markdown reference, not published
    world-notes.md
    geography.md
    factions.md
    glossary.md
    timeline.md
    site-inventory.md
    restructure-plan.md                    ← this file
```

---

## Where each layer of the world lives

| World layer | Folder | Example |
|---|---|---|
| **World (Tyrnarra)** | root | `tyrnarra-primer.html`, `grand-gods.html` |
| **Continent (Talan)** | `/talan/` | `talan.html`, `magic.html`, `history.html` |
| **Region (god domain)** | `/talan/domains/<domain>/` | `/talan/domains/vindul/vindul.html` |
| **Sub-region / Kingdom** | section in domain page, or own file when promoted | `Thousand Kingdom` section in `zuzental.html`, or eventually `/talan/domains/zuzental/thousand-kingdom.html` |
| **Settlement** | folder under its domain | `/talan/domains/brauogi/millhaven/millhaven.html` |
| **Sub-location of settlement** | sibling file in settlement folder | `/talan/domains/brauogi/millhaven/lowspan.html` |
| **Quest** | `Quests/` folder inside settlement | `/talan/domains/brauogi/millhaven/Quests/quest-x.html` |
| **Faction (independent org)** | `/talan/factions/` | `/talan/factions/adventurers-guild.html` |
| **God church** | umbrella in `god-churches.html`; promoted to own file later if needed | `/talan/factions/god-churches.html` |

### What about "kingdoms" specifically?

The user's mental model is `regions → kingdoms → settlements`. In the project's existing terminology, the layer between domain and settlement is **sub-region**, and *some* sub-regions are kingdoms while others are geographic, cultural, or political-but-not-kingdoms:

- Kingdoms / political entities: Thousand Kingdom, Legea Empire, Namur Republic, River Duchies, Order of Steam, Vernua Dominion, Kaosadaemi Principality, etc.
- Geographic sub-regions: Baerfrost, Haizetsua, Basogur Jungle, Burdineyja, etc.
- Cultural sub-regions: Tahu Tangata, Hareaveldi, Lands of Villtur.
- Border territories: Azkamour, Lua Lasai, Harro Distiratsue, No Man's Land.

All four types live as sections in their domain page until they earn their own file. When a kingdom (or any sub-region) earns its own file, it lands at `/talan/domains/<domain>/<subregion-slug>.html`. No separate `/kingdoms/` folder — the relationship to the parent domain is the more important hierarchy.

---

## Persistent sidebar navigation

Every page gets a left-side sidebar showing the full site tree, with the current page highlighted. The sidebar is inline HTML/CSS/JS (self-contained snippet) so it respects the no-external-files rule.

**Behaviour:**
- Default state on desktop: visible, ~240px wide, collapsible to a slim rail.
- Default state on mobile: collapsed; tap a hamburger icon top-left to open as an overlay.
- The current page is highlighted with the gold accent.
- Sections (World, Talan, Domains, Factions, Lore Tools) are collapsible.
- "You are here" highlight is driven by a `data-page` attribute on the `<body>`.

**Two visual variants (matching existing Style A and Style B):**
- Style A sidebar: void-blue background, gold text, Cormorant SC for labels, used on cosmos and gods pages.
- Style B sidebar: warmer dark background, philosopher headings, used on Talan + settlement pages.
- Both variants share the same HTML structure and behaviour — only the CSS variables change.

**Implementation:**
- The sidebar markup is identical across pages — only the `data-page` attribute on `<body>` changes.
- A small inline `<script>` reads `data-page` and toggles the `.is-current` class on the matching link.
- Mobile detection is pure CSS (`@media (max-width: 800px)`).

---

## Naming for new pages (recap)

The naming convention in `CLAUDE.md` still governs:
- **Old/ancient things** → Basque or Icelandic source, drifted.
- **New/modern things** → plain English, optionally lightly drifted.

Folder slugs use **lowercase ASCII with hyphens**: `myrkono/`, `thousand-kingdom.html`, `adventurers-guild.html`. Diacritics are stripped from slugs but preserved in display titles.

---

## Phasing

### Phase 1 — Skeleton + navigation (this pass)

1. Create the `/talan/` tree (folders + stub HTML pages).
2. Stub pages for all 13 domains, 4 factions, magic, history, faction overview, Talan overview.
3. Each stub uses the appropriate visual style (A or B) and has the sidebar nav, breadcrumb, title, and short flavor line. No deep content yet.
4. Existing root pages (`tyrnarra-primer.html`, `grand-gods.html`, `talan-primer.html`) get the sidebar nav patched in but keep their current content unchanged.
5. `index.html` is reworked to point at the new layout. Broken Millhaven link is stubbed (links to a placeholder until Millhaven returns).
6. `CLAUDE.md` is updated with the new conventions.
7. `lore/site-inventory.md` is refreshed.

### Phase 2 — Content migration (later)

- Split `talan-primer.html` content into its proper homes: History tab → `/talan/history.html`, Magic tab → `/talan/magic.html`, Regions tab → each domain page, Factions tab → `/talan/factions/`.
- Decide whether `talan-primer.html` becomes a redirect or is replaced by `/talan/talan.html`.
- Begin populating domain pages with the rich data already in `lore/geography.md`.

### Phase 3 — Settlements + sub-region promotion (later)

- Reintroduce Millhaven under `/talan/domains/brauogi/millhaven/`.
- Promote the most-developed sub-regions (Thousand Kingdom, Order of Steam, Lost Kingdom, etc.) to their own files as content warrants.

---

## What this plan deliberately does *not* do

- It does not rename `tyrnarra-primer.html` or `grand-gods.html`. They stay at root because they are world-level, and changing their URLs would break the live site's existing bookmarks.
- It does not introduce a build step. Every page remains hand-crafted, standalone HTML.
- It does not retrofit existing names to the Basque/Icelandic rule. Per `CLAUDE.md`, the rule applies going for