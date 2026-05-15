# Site Inventory — Current State

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

Last updated 2026-05-15 after Phase 1 of the restructure (skeleton + sidebar).

---

## Page Tree

```
/                              [Style A · cosmic]
  index.html                   landing page, curated portal + sidebar
  tyrnarra-primer.html         world cosmology + sidebar (existing)
  tyrnarra-gods.html           the 13 bound gods + sidebar (existing)
  talan-primer.html            LEGACY tabbed primer + sidebar
                               → Phase 2: content migrates to /talan/

/talan/                        [Style B · grounded]
  talan.html                   continent overview                    STUB (substantive)
  magic.html                   Four Schools                          STUB
  history.html                 Eras / timeline                       STUB

/talan/domains/                13 domain folders, each with a STUB entry page
  vindul/vindul.html           STUB (substantive — etymology, terrain, sub-regions)
  lautara/lautara.html         STUB
  myrkono/myrkono.html         STUB
  floteyn/floteyn.html         STUB
  sumendar/sumendar.html       STUB
  lioaru/lioaru.html           STUB
  brauogi/brauogi.html         STUB
  ezkudon/ezkudon.html         STUB
  egulon/egulon.html           STUB
  zuzental/zuzental.html       STUB
  nashavel/nashavel.html       STUB
  ehizahar/ehizahar.html       STUB
  askamira/askamira.html       STUB

/talan/factions/
  factions.html                taxonomy overview                     STUB (substantive)
  adventurers-guild.html       STUB (substantive)
  mercenary-guild.html         STUB (substantive)
  god-churches.html            STUB
  remnants.html                STUB
```

**Stub legend**: "STUB" = page exists with the new sidebar and skeleton content, ready for prose expansion. "Substantive stub" = stub but already carries non-trivial content drawn from the lore files. No fully-populated long-form pages yet outside the legacy primers.

---

## Sidebar Nav

Every page has the persistent sidebar (canonical snippet at `lore/sidebar-nav.md`). The sidebar lists:

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
| B — Grounded | `talan-primer.html` (legacy), all `/talan/**` pages | Uncial Antiqua, Crimson Pro, Cinzel | warm dark, parchment, gold |

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
| `lore/restructure-plan.md` | Phasing notes for the restructure (Phase 1 done, 2/3 ahead) |
| `lore/sidebar-nav.md` | Canonical sidebar HTML/CSS/JS snippet |

---

## Phase 2 — Content Migration (next)

Open work that will progressively populate the skeleton:

- Move `talan-primer.html` **History** tab content into `/talan/history.html` (with three-tier knowledge UI intact: amber `◈` Popular Belief pills, red `⚿` GM Secret pills).
- Move `talan-primer.html` **Magic** tab content (the long-form "Magic in Daily Life" section) into `/talan/magic.html`.
- Move `talan-primer.html` **Regions** tab content (13 region cards) into the respective `/talan/domains/<domain>/<domain>.html` pages.
- Move `talan-primer.html` **Factions** tab content into `/talan/factions/factions.html`.
- After migration: either delete `talan-primer.html` or leave it as a redirect to `/talan/talan.html`.

---

## Phase 3 — Settlements + Sub-region Promotion (later)

- Reintroduce Millhaven under `/talan/domains/brauogi/millhaven/millhaven.html` (plus its existing sub-pages and Quests folder).
- Promote the most-developed sub-regions to their own files: Thousand Kingdom, Order of Steam, Lost Kingdom, Dragon's Reach, River Duchies, etc.

---

## Three-Tier Knowledge System

Established in `talan-primer.html` (History tab) and `tyrnarra-gods.html` (god secrets):

- **Plain text** — common knowledge, no interaction.
- **Amber ◈ pill** — "Popular Belief", expandable.
- **Red ⚿ pill** — "GM Secret", expandable.

Currently used in: `tyrnarra-gods.html` (all 13 gods) and `talan-primer.html` (Elden Era, Week of Crimson Rain). The remaining eras have only common-knowledge text. To do: add Popular Belief / GM Secret tiers to Gods' Era, Lost Era, Golden Era, Dark Era, Adventurer Era when their content migrates.
