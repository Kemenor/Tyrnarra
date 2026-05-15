# Site Inventory — Current State

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

Last updated **2026-05-15** after Phase 2 of the restructure (content migration + legacy primer deletion).

---

## Page Tree

```
/                              [Style A · cosmic]
  index.html                   landing page + sidebar
  tyrnarra-primer.html         world cosmology + sidebar
  tyrnarra-gods.html           the 13 bound gods + sidebar
  (talan-primer.html removed — content migrated 2026-05-15)

/talan/                        [Style B · grounded]
  talan.html                   continent overview, three seas, 13 domain cards     POPULATED
  magic.html                   Four Schools + Magic in Daily Life + Faith & Gods   POPULATED
  history.html                 8 eras with three-tier knowledge UI                 POPULATED

/talan/domains/                13 domain pages — each with etymology, facts,
                               character pills, god's city, sub-region cards
  vindul/vindul.html           POPULATED (stub-level prose)
  lautara/lautara.html         POPULATED
  myrkono/myrkono.html         POPULATED
  floteyn/floteyn.html         POPULATED
  sumendar/sumendar.html       POPULATED
  lioaru/lioaru.html           POPULATED
  brauogi/brauogi.html         POPULATED
  ezkudon/ezkudon.html         POPULATED
  egulon/egulon.html           POPULATED
  zuzental/zuzental.html       POPULATED
  nashavel/nashavel.html       POPULATED
  ehizahar/ehizahar.html       POPULATED
  askamira/askamira.html       POPULATED

/talan/factions/
  factions.html                taxonomy overview + 4 cards                         POPULATED
  adventurers-guild.html       At a Glance + Origin + Neutrality + Scale          POPULATED
  mercenary-guild.html         At a Glance + Origin + Work + Structure + Scale    POPULATED
  god-churches.html            13 + Other God Believers                           POPULATED
  remnants.html                Origin + Current state + GM context                POPULATED
```

**Populated** = page has substantive content beyond skeleton. Many pages can still grow — particularly the domain pages, where sub-regions are listed but not yet promoted to their own files.

---

## Shared Chrome (`/assets/`)

Loaded by every page via `<link>` and `<script defer src>`:

| File | Used by | Purpose |
|---|---|---|
| `assets/site-nav.css` | every page | Sidebar styling |
| `assets/site-nav.js` | every page | Sidebar markup + behaviour (single source of truth for menu structure) |
| `assets/style-b.css` | every page under `/talan/` | Style B base — palette, fonts, container/header/divider, facts panel, gods-city callout, sub-region grid, domain accents, **timeline + era cards, three-tier (amber/red) expandables, info-card grid, scale-row, callout, pill row** |

To add a page to the sidebar, edit `assets/site-nav.js` only. The `NAV_HTML` array is the single source of truth.

---

## Sidebar Nav

The sidebar lists:

- World & Cosmos · Cosmology, The 13 Bound Gods
- Talan · Continent Overview, History, Magic
- Domains · all 13 (with `Domain · Element` labels)
- Factions · overview + 4 organisations

The current page is highlighted via `<body data-page="<slug>">`. Settlements and sub-region pages are intentionally **not** in the sidebar — they're accessed from their parent domain page.

---

## Visual Styles in Use

| Style | Used on | Key fonts | Palette |
|---|---|---|---|
| A — Cosmic | `index.html`, `tyrnarra-primer.html`, `tyrnarra-gods.html` | Cormorant Garamond, Cormorant SC, IM Fell English | void blue, gold, cloud white |
| B — Grounded | all `/talan/**` pages | Uncial Antiqua, Crimson Pro, Cinzel | warm dark, parchment, gold |

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
| `lore/restructure-plan.md` | Phasing notes for the restructure (Phase 1 + 2 done; Phase 3 ahead) |
| `lore/sidebar-nav.md` | Architecture notes on the shared sidebar |

---

## Phase 3 — Settlements + Sub-region Promotion (ahead)

- Reintroduce Millhaven under `/talan/domains/brauogi/millhaven/millhaven.html`.
- Promote the most-developed sub-regions to their own files: Thousand Kingdom, Order of Steam, Lost Kingdom, Dragon's Reach, River Duchies, etc.
- Add the three-tier knowledge UI to remaining eras (Gods', Lost, Golden, Dark, Adventurer) as their Popular Belief / GM Secret content gets written.

---

## Three-Tier Knowledge System

- **Plain text** — common knowledge, no interaction.
- **Amber ◈ pill** — "Popular Belief", expandable. Uses `.legend-era-toggle` / `.legend-era-content`.
- **Red ⚿ pill** — "GM Secret", expandable. Uses `.secret-era-toggle` / `.secret-era-content`.

Currently used in:
- `tyrnarra-gods.html` — all 13 gods have at least the red GM Secret tier.
- `/talan/history.html` — Elden Era and Week of Crimson Rain have all three tiers.

Other eras have only common-knowledge text. To do: extend the amber + red tiers to Gods' Era, Lost Era, Golden Era, Dark Era, Adventurer Era as their content is developed.
