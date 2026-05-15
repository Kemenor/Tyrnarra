# Site Inventory — Current State

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

Last updated **2026-05-15** after Phase 3 of the restructure (cosmology → landing page, Magic moved to World & Cosmos, shared `style-a.css` extracted, gods page wired to domains).

---

## Page Tree

```
/                              [Style A · cosmic]
  index.html                   landing = world primer (cosmology)                POPULATED
  grand-gods.html           the 13 bound gods (data-driven, expandable)       POPULATED
  magic.html                   Magic & Faith — Four Schools / Daily Life / Faith POPULATED

/talan/                        [Style B · grounded]
  talan.html                   continent overview, three seas, 13 domain cards  POPULATED
  history.html                 8 eras with three-tier knowledge UI               POPULATED

/talan/domains/                13 domain pages — etymology, facts, character pills,
                               god's city, sub-region cards
  vindul/vindul.html           POPULATED      lautara/lautara.html     POPULATED
  myrkono/myrkono.html         POPULATED      floteyn/floteyn.html     POPULATED
  sumendar/sumendar.html       POPULATED      lioaru/lioaru.html       POPULATED
  brauogi/brauogi.html         POPULATED      ezkudon/ezkudon.html     POPULATED
  egulon/egulon.html           POPULATED      zuzental/zuzental.html   POPULATED
  nashavel/nashavel.html       POPULATED      ehizahar/ehizahar.html   POPULATED
  askamira/askamira.html       POPULATED

/talan/factions/
  factions.html                taxonomy overview + 4 cards                      POPULATED
  adventurers-guild.html       POPULATED      mercenary-guild.html     POPULATED
  god-churches.html            POPULATED      remnants.html            POPULATED
```

Removed in earlier phases: `talan-primer.html` (Phase 2), `tyrnarra-primer.html` and `/talan/magic.html` (Phase 3).

---

## Shared Chrome (`/assets/`)

Loaded by every page via `<link>` and `<script defer src>`:

| File | Used by | Purpose |
|---|---|---|
| `assets/site-nav.css` | every page | Sidebar styling |
| `assets/site-nav.js` | every page | Sidebar markup + behaviour (single source of truth) |
| `assets/style-a.css` | world-level pages (`index.html`, `grand-gods.html`, `magic.html`) | Cosmic palette + fonts (Cinzel Decorative / Cinzel / Crimson Pro), starfield, header, group dividers, portal cards, god-card grid, scale rows, info cards, planar layer expandables, red GM-Secret pills |
| `assets/style-b.css` | every page under `/talan/` | Grounded palette + fonts (Uncial Antiqua / Crimson Pro / Cinzel), parchment overlay, container/header/divider, facts panel, gods-city callout, sub-region grid, domain accents, timeline + era cards, amber/red expandables, pill rows |

To add a page to the sidebar, edit `assets/site-nav.js` only.

---

## Sidebar Nav (Phase 3)

- **World & Cosmos** — Cosmology (→ `/index.html`), The 13 Bound Gods, Magic &amp; Faith
- **Talan** — Continent Overview, History &amp; Eras
- **Domains** — all 13
- **Factions** — overview + 4 organisations

The current page is highlighted via `<body data-page="<slug>">`. Settlements and sub-region pages are intentionally **not** in the sidebar.

---

## Visual Styles in Use

| Style | Used on | Key fonts | Palette |
|---|---|---|---|
| A — Cosmic | `index.html`, `grand-gods.html`, `magic.html` | Cinzel Decorative, Cinzel, Crimson Pro | void (`#06060a`), purple/blue ambient, gold, parchment text, per-god accents |
| B — Grounded | all `/talan/**` pages | Uncial Antiqua, Crimson Pro, Cinzel | warm dark (`#0f0c08`), parchment, gold, per-domain accents |

---

## Cross-Links

- Each god card on `grand-gods.html` has a **"Visit [Domain Name] →"** link in its expanded view, pointing to the matching `/talan/domains/<slug>/<slug>.html`. When god city-states get their own pages later, a second link will go there.
- The landing page's portal cards link out to the gods, magic, Talan, and history pages.
- Each domain page breadcrumbs back to `/talan/talan.html` and `/index.html`.

---

## Lore Reference Files (not published)

| File | Contents |
|---|---|
| `lore/world-notes.md` | Divine power tiers, Gods' Law, the Twelve, Wellspring & belief, Four Schools, Cronus secret, Tani lore, Elden/Corrupted God, calendar |
| `lore/geography.md` | All 13 god domains — position, terrain, god's city, sub-regions with etymologies |
| `lore/factions.md` | Faction taxonomy; detailed entries for Adventurers Guild, Mercenary Guild, Remnants |
| `lore/glossary.md` | All coined names with etymologies; domain name table; sub-region name list by domain |
| `lore/timeline.md` | All eight eras with dates |
| `lore/site-inventory.md` | this file |
| `lore/restructure-plan.md` | Phasing notes for the restructure (Phases 1, 2, 3 done) |
| `lore/sidebar-nav.md` | Architecture notes on the shared sidebar |

---

## Future Work

- **Settlements**: reintroduce Millhaven under `/talan/domains/brauogi/millhaven/millhaven.html`.
- **Sub-region promotion**: promote major kingdoms (Thousand Kingdom, Order of Steam, Lost Kingdom, Dragon's Reach, River Duchies) to their own files.
- **God city-state pages**: when those get content, add them as second links from each god card.
- **Three-tier UI on remaining eras**: extend the amber Popular Belief / red GM Secret expandables to Gods', Lost, Golden, Dark, Adventurer eras as content gets written.

---

## Three-Tier Knowledge System

- **Plain text** — common knowledge, no interaction.
- **Amber ◈ pill** — "Popular Belief", expandable. `.legend-era-toggle` / `.legend-era-content` (Style B / history page).
- **Red ⚿ pill** — "GM Secret", expandable. `.secret-toggle` / `.secret-content` (gods page) or `.secret-era-toggle` (history page).

Currently used in:
- `grand-gods.html` — all 13 gods have at least the red GM Secret tier (Cronus's is fully written; others have placeholder text).
- `/ta