# WorldAnvil → Lore Migration Plan

Migrating content from `worldanvil-export/` into the canonical `lore/` files.
**Rule:** existing `lore/` files win on conflict — WA export is the import, not the override.

Re-run the converter any time you do a fresh WA export:
```
python tools/wa-to-md.py export/World-Tyrnarra-ec6 worldanvil-export/Tyrnarra
python tools/wa-to-md.py export/World-Talan-97c    worldanvil-export/Talan
```

---

## Source overview

| Source | Files | Notes |
|---|---|---|
| `worldanvil-export/Tyrnarra/` | 25 | Richer content, newer writing (2025) |
| `worldanvil-export/Talan/` | 208 | Shallower per-article, broader coverage |
| `lore/` (existing) | 5 files | Canon — do not overwrite, only extend |

---

## Phase 1 — Cosmology & World Rules → `lore/world-notes.md`
**Status: DONE (2026-05-16)**

*Tyrnarra export, do this first — these are the foundation everything else references.*

Source files:
- `worldanvil-export/Tyrnarra/tyrnarra.md` — Cloud Sea, Solyra/Veyru/Calune, Wellspring
- `worldanvil-export/Tyrnarra/Planes/planes.md` — full planar structure (3 layers × 3 planes)
- `worldanvil-export/Tyrnarra/Base Setting/the-age-of-corruption.md` — myth/history of the Blightfather binding
- `worldanvil-export/Tyrnarra/gods-sanctum.md` — sanctum mechanics, Council of Thirteen
- `worldanvil-export/Tyrnarra/the-thirteen.md` — all 13 gods with aspects, weapons, mortal perception
- `worldanvil-export/Talan/World Atlas/` — intro, magic, planes (cross-check against above)
- `worldanvil-export/Talan/Grand Gods/` × 13 — per-god detail pages (likely thin, worth checking)

Target: merge into `lore/world-notes.md`, expanding existing god entries.

**What was merged:**
- Added "Tyrnarra — The World & Sky" (Cloud Sea, Solyra/Veyru/Calune, cloudships).
- Expanded the Planar Travel stub into a full "Planar Structure — The Three Layers" section (Wellspring, Energy, Elemental; Feyworld, Material, Shadowplane; Elysium, Diyu, Abyss; Aurora Veil, Ethereal Plane, Duskmire; Astral Plane; Dauria; the soul-from-all-three-layers note).
- Extended "Gods' City-States" with sanctum-as-literal-home, blessing/burden examples (Komo fires, Forseti red tape, Vesuna shifting streets), and a "Council of Thirteen" subsection.
- Added "The Thirteen — Per-God Sheet" — aspects, depiction, favoured weapon, mortal perception, and PF2e cleric domains for all 13 (folded the Talan/Grand Gods/ domain tags into the per-god cleric-domain lines).
- Added "The Age of Corruption — Mortal Myth" — the *Sage Lorant of Highspire* in-world account, with a note that this is a mortal-mouth folk version and conflicts with the GM-truth Elden/Corrupted God identity already in `world-notes.md`.
- Added folk names (**Maw Below**, **Blightfather**, **Counting of Years**) to `glossary.md` under a new "Folk Names for Cosmic Things" subsection.

**Not migrated (intentional):**
- `Talan/World Atlas/introduction-to-talan.md`, `magic-of-talan.md`, `introduction-to-the-atlas.md`, `planes.md` — older 2023 drafts, superseded by the Tyrnarra-side files; nothing new to import.
- `Talan/World Atlas/education-level.md`, `technology-level.md` — campaign-prep stat tables, not lore.

**Notes for later phases:**
- Tani's biographical detail in the WA export refers to "Lost Kingdom's rebellion" and "Lost Era" — these don't yet exist in `world-notes.md` as named events. They will surface in Phase 5 (Timeline). Existing canon ties Tani's death to the Week of Crimson Rain; the "Lost Kingdom's rebellion" may be a sub-event within it. Resolve in Phase 5.

---

## Phase 2 — Geography & Domains → `lore/geography.md`
**Status: TODO**

*Talan export, largest batch.*

**Important:** The WA export uses old working names throughout. Before migrating any entry:
- **Regions** (chaos, commerce, darkness, etc.) — canonical domain names are already established in the HTML pages and `lore/geography.md`. Use those, not the WA folder/file names.
- **God city-states** (Azmaria, Baria, Dauria, etc.) — many have already been renamed. Cross-check against the existing domain HTML pages (`talan/domains/<domain>/<domain>.html`) for the correct current name before writing anything into lore.

Source files:
- `worldanvil-export/Talan/Regions/` × 13 — one per domain (chaos, commerce, darkness, etc.) — content only, ignore names
- `worldanvil-export/Talan/Kingdoms/` × ~50 — sub-regions and kingdoms within domains
- `worldanvil-export/Talan/Settlementsja/` × 14 — god city-states — verify names against published HTML
- `worldanvil-export/Talan/Fenurra/` — Fenurra region + its weapons/factions

Target: extend `lore/geography.md` with sub-region entries per domain; promote major kingdoms to their own sections.

---

## Phase 3 — Factions & Organisations → `lore/factions.md`
**Status: TODO**

*Mixed sources.*

Source files:
- `worldanvil-export/Talan/Organizations/adventurers-guild.md` — guild overview
- `worldanvil-export/Talan/Organizations/bounty-hunter-guild.md`
- `worldanvil-export/Tyrnarra/Adventurer Guild/adventurers-guild.md` — richer write-up
- `worldanvil-export/Tyrnarra/Adventurer Guild/lord-albrecht-lavisburg.md`
- `worldanvil-export/Tyrnarra/Red Empire/red-empire.md` — new faction, needs full entry
- `worldanvil-export/Tyrnarra/Red Empire/iron-tide.md`
- `worldanvil-export/Tyrnarra/Red Empire/the-menagerie.md`
- `worldanvil-export/Talan/History/golden-empire.md`
- `worldanvil-export/Talan/History/storveldi-denbora.md`
- `worldanvil-export/Talan/Powerfull Beings/` — domain overview, powerful being types

Target: extend `lore/factions.md`; Red Empire and Menagerie are new and need full entries.

---

## Phase 4 — Bestiary & Species → `lore/bestiary.md` *(new file)*
**Status: TODO**

*Talan export, purely additive.*

Source files:
- `worldanvil-export/Talan/Ancestries/` × 41 — all playable ancestries with world-flavour notes
- `worldanvil-export/Talan/Versatile Heritages/` × 14 — tieflings, aasimar, etc.
- `worldanvil-export/Talan/Demons/` × 14 — virtue demons
- `worldanvil-export/Talan/Devils/` × 7 — sin devils
- `worldanvil-export/Tyrnarra/Kitsune/` × 5 — species, Heartcourt, Catjomin Sake, Kawaakari, House of Flavors

Target: new `lore/bestiary.md`; kitsune get their own section as the most fully written species.

---

## Phase 5 — Timeline & History → `lore/timeline.md`
**Status: TODO**

Source files:
- `worldanvil-export/Talan/History/golden-empire.md`
- `worldanvil-export/Talan/History/storveldi-denbora.md`

Target: cross-reference and extend existing `lore/timeline.md` eras.

---

## Skip / Discard

These are campaign artefacts or non-canon imports — do not migrate:

- `worldanvil-export/Talan/Campaigns/`, `Player Handbook/`, `Staging Area/` — campaign ops, not world lore
- `worldanvil-export/Talan/Other/readme.md` — WorldAnvil housekeeping
- `worldanvil-export/Talan/balaena.md`, `ashka.md`, `lukas-s.md`, `mad-mage.md` — player/NPC session notes
- `worldanvil-export/Talan/Gods/golarion-gods.md` — Pathfinder import, not Tyrnarra canon
