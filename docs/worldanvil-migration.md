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
**Status: DONE — initial pass 2026-05-16 (am); patch 2026-05-16 (pm) for Wardstones + Nine Generals + Araphel deep dive that lived in `Tyrnarra/Araphel/` and `Tyrnarra/Myrria/`, missed on the first sweep**

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

**What was merged (am pass):**
- Added "Tyrnarra — The World & Sky" (Cloud Sea, Solyra/Veyru/Calune, cloudships).
- Expanded the Planar Travel stub into a full "Planar Structure — The Three Layers" section (Wellspring, Energy, Elemental; Feyworld, Material, Shadowplane; Elysium, Diyu, Abyss; Aurora Veil, Ethereal Plane, Duskmire; Astral Plane; Dauria; the soul-from-all-three-layers note).
- Extended "Gods' City-States" with sanctum-as-literal-home, blessing/burden examples (Komo fires, Forseti red tape, Vesuna shifting streets), and a "Council of Thirteen" subsection.
- Added "The Thirteen — Per-God Sheet" — aspects, depiction, favoured weapon, mortal perception, and PF2e cleric domains for all 13 (folded the Talan/Grand Gods/ domain tags into the per-god cleric-domain lines).
- Added "The Age of Corruption — Mortal Myth" — the *Sage Lorant of Highspire* in-world account, with a note that this is a mortal-mouth folk version and conflicts with the GM-truth Elden/Corrupted God identity already in `world-notes.md`.
- Added folk names (**Maw Below**, **Blightfather**, **Counting of Years**) to `glossary.md` under a new "Folk Names for Cosmic Things" subsection.

**What was added in the patch (pm pass, after discovering Tyrnarra-side regional folders had been treated as "Phase 1 only" and skimmed):**
- **The Seven Wardstones** — full section in `world-notes.md`. Seven relics forged at the end of the Age of Corruption, all sitting inside Myrkono (Shadow Steppes ×2, Itzasoa ×2, Ilun Tasun ×2, Myrria ×1). Anchors of the Corrupted God's binding. Source: `Tyrnarra/Araphel/the-wardstones.md`.
- **The Nine Generals of Corruption + the Nine Dungeons** — full section in `world-notes.md`. Nine corruption-lords erupted ~2524 MR; one (the Ash-Binder) defeated; eight remain. Source: `Tyrnarra/Araphel/the-nine-generals-of-corruption.md`. Cross-referenced from `factions.md` (Remnants of Corruption entry rewritten).
- **Araphel deep dive** — extended `world-notes.md` Araphel section. God of Shadows AND of new faces/rebirth; God of Many Faces epithet; fetchling appearances at apparent age 35; Sanctum of Veils; sacred iconography (half-mask, raven, dagger, violet/black/silver); rites (Shadowed Palm, Lantern Rite, Shadow-Coin). Source: `Tyrnarra/Myrria/araphel.md` + `araphel-deity-block.md`.

**Not migrated (intentional):**
- `Talan/World Atlas/introduction-to-talan.md`, `magic-of-talan.md`, `introduction-to-the-atlas.md`, `planes.md` — older 2023 drafts, superseded by the Tyrnarra-side files; nothing new to import.
- `Talan/World Atlas/education-level.md`, `technology-level.md` — campaign-prep stat tables, not lore.

**Notes for later phases:**
- Tani's biographical detail in the WA export refers to "Lost Kingdom's rebellion" and "Lost Era" — these don't yet exist in `world-notes.md` as named events. They will surface in Phase 5 (Timeline). Existing canon ties Tani's death to the Week of Crimson Rain; the "Lost Kingdom's rebellion" may be a sub-event within it. Resolve in Phase 5.

**Procedural lesson from the pm patch:** the original Phase 1 sweep mapped one folder per phase, but the Tyrnarra-side regional folders (`Tyrnarra/Araphel/`, `Tyrnarra/Myrria/`, `Tyrnarra/Shadow Steppes/`, `Tyrnarra/Random/`) hold a mix of cosmology, geography, and faction content. **Don't trust folder names** — read by content per future re-runs. The migration plan should be read as topic-driven, not folder-driven.

---

## Phase 2 — Geography & Domains → `lore/geography.md`
**Status: DONE (2026-05-16). Fenurra placed in Lands of Villtur (Ehizahar) with meteor + volcanism; Twin Cities canonised as the mobile pirate capital in Midarra. Fenurran culture imported in full into a new `lore/cultures.md` on the same date. See [wa-name-reconciliation.md](wa-name-reconciliation.md).**

*Talan export, largest batch by file count — but see headline finding in the reconciliation: almost all 77 source files are empty stubs.*

**Important:** The WA export uses old working names throughout. Before migrating any entry:
- **Regions** (chaos, commerce, darkness, etc.) — canonical domain names are already established in the HTML pages and `lore/geography.md`. Use those, not the WA folder/file names.
- **God city-states** (Azmaria, Baria, Dauria, etc.) — many have already been renamed. Cross-check against the existing domain HTML pages (`talan/domains/<domain>/<domain>.html`) for the correct current name before writing anything into lore.

Source files:
- `worldanvil-export/Talan/Regions/` × 13 — one per domain (chaos, commerce, darkness, etc.) — **empty stubs, no prose**
- `worldanvil-export/Talan/Kingdoms/` × ~50 — sub-regions and kingdoms within domains — **empty stubs, no prose**
- `worldanvil-export/Talan/Settlementsja/` × 14 — god city-states — **empty stubs except Myrria** (one paragraph)
- `worldanvil-export/Talan/Fenurra/` — Fenurra region + its tribes/weapons — **substantial new content; placement decision needed**

Target: extend `lore/geography.md` with sub-region entries per domain; promote major kingdoms to their own sections.

**Closed during this phase:**
1. ✅ Fenurra placed as sub-territory of Lands of Villtur (Ehizahar). Meteor + volcanic activity added to Ehizahar terrain in `lore/geography.md`. Etymology recorded in `lore/glossary.md`.
2. ✅ Twin Cities canonised — mobile pirate capital (water-raft + sky-island pair) drifting through Midarra, sovereign of any god/kingdom. Recorded in `lore/geography.md` (Midarra) and `lore/glossary.md`.
3. ✅ Azmaria / Zilarria dropped per user decision — not canon.
4. ✅ Fenurran culture imported in full into new `lore/cultures.md` — four tribes (Draconis / Vexiren / Brakkaun / Seravain), Speaker's Mantle politics, Bone Gong + War Council institutions, Blackglass / Velthite / Ghost Willow materials, the Infernal-Smoked Hook-Line-Sinker Charge doctrine, all weapons. Tribe names, materials, place names, institutions all catalogued in `glossary.md`.
5. ✅ **Kitsune kingdom placed** (2026-05-16). The TBD Emarrea sub-region of Lautara is now defined as the kitsune kingdom, with capital **Biozuri**, central district **Heartplaza**, mountain village **Kawaakari**, and landmark **House of a Thousand Flavors**. Geography in `lore/geography.md` (Lautara > Emarrea); full kitsune culture entry added to `lore/cultures.md` (Heartcourt + nine Hearts, Circles of Importance, Catjomin Sake's nine tiers, lifespan + tail-growth, the Cook's Circle). Etymologies coined: *Emarrea* (Basque ema "soft" + arrea "tawny") and *Biozuri* (bihotz+hiri "heart-city"). Source: `worldanvil-export/Tyrnarra/Kitsune/` (4 of 5 files merged — geography + politics + tradition + landmark; the pure-species lifespan/tail-growth bits also folded in since they're cultural too).
6. ✅ **Myrria full city placed** (2026-05-16 pm patch). All 8 districts written into `lore/geography.md`: The Lantern Stairs, Cliffside Bazaar, The Veiled Quarter, The Sanctum of Veils, Shadowguard Keep, The Hidden Vaults, The Blackstone Stronghold, The Starlight Cliffs. Government structure noted (the Council of Adventurers governs; Araphel resides but does not rule). The Sanctum of Veils holds the seventh (Divine) Wardstone. Source: `Tyrnarra/Myrria/myrria.md`.
7. ✅ **The Hollow of Ten Thousand Threads placed** (2026-05-16 pm patch). The Vermin Queen's dungeon, in the Shadow Steppes sub-region of Myrkono. Full structural detail (Web-Tunnels, Brood Pits, Silken Vaults, Throne) and threats catalogued in `lore/geography.md`. Source: `Tyrnarra/Shadow Steppes/the-hollow-of-ten-thousand-threads.md`.
8. ✅ **Wardstone geography distribution** (2026-05-16 pm patch). All seven Wardstones threaded into the Myrkono sub-region entries in `geography.md` (Shadow Steppes — 2; Itzasoa — 2; Ilun Tasun — 2; Myrria — 1). Cosmological role of Myrkono updated accordingly.

**Open threads kicked into later phases:**
- ~~**The Divine Faith**~~ — RESOLVED 2026-05-16. State religion of the **Legea Empire** (Zuzental sub-region); serves a non-bound god residing in the third (Postlife) planar layer. Captured in `factions.md` under a new "Non-Bound God Faiths" heading and threaded into `geography.md`, `cultures.md`, and `glossary.md`. Earlier same-day draft placed the Faith in the Vernua Dominion (Nashavel) — superseded; Vernua reverted to its prior simpler entry.
- ~~**The theocratic prince**~~ — RESOLVED 2026-05-16. Heir to the **Legea Empire** (and thus heir of the demigod ruling line).
- **The Aeris / Scar of Aeris etymology** — Latinate-feeling names imported as-is from WA. Decide whether they stay Fenurran-internal Latinate or get retrofitted to the deep-old Basque/Icelandic stratum. Low priority.
- **The Faith's deity** — specific plane (Elysium / Diyu / Abyss), name, and nature of the demigod ruler. Pending. Phase 3 work.

**Skipped (intentional):**
- `Settlementsja/myrria.md`'s short paragraph — already redundant with the published Myrkono page; nothing new to merge.
- The 13 Regions, 50 Kingdoms, and 11 other Settlementsja files — pure empty stubs.

---

## Phase 3 — Factions & Organisations → `lore/factions.md`
**Status: TODO**

*Mixed sources.*

Source files:
- `worldanvil-export/Talan/Organizations/adventurers-guild.md` — guild overview
- `worldanvil-export/Talan/Organizations/bounty-hunter-guild.md`
- `worldanvil-export/Tyrnarra/Adventurer Guild/adventurers-guild.md` — richer write-up
- `worldanvil-export/Tyrnarra/Adventurer Guild/lord-albrecht-lavisburg.md`
- `worldanvil-export/Tyrnarra/Myrria/myrrias-godshall.md` — **NEW** (surfaced in 2026-05-16 audit). Major regional guild facility — architecture, Quill & Blade sigil, ranks (Bronze, Silver, Mithral, Starsteel), Grand Assembly governance hint.
- `worldanvil-export/Tyrnarra/Myrria/guild-sovereign-seraphel-duskbane.md` — **NEW** (same audit). The current Guild Sovereign of Myrkono; fetchling, *Duskbane* epithet from corruption-cult hunts; lieutenant during the Nine Dungeons eruption.
- `worldanvil-export/Tyrnarra/Red Empire/red-empire.md` — new faction, needs full entry
- `worldanvil-export/Tyrnarra/Red Empire/iron-tide.md`
- `worldanvil-export/Tyrnarra/Red Empire/the-menagerie.md`
- `worldanvil-export/Tyrnarra/Random/house-eisenhart.md` — **NEW** (same audit). Major dwarven noble house in the Order of Steam. Matriarch Tharka Eisenhart (217-year mountain dwarf); the *Stahlglanz* mobile fortress; the historical *Siege of Nine Storms*.
- `worldanvil-export/Tyrnarra/Random/the-spiders-silk.md` — **NEW** (same audit). The Spider's Silk Inn at Crossroads — Matron Charna (ancient Anadi), enchanted silver silk that suppresses hostile magic and extends her awareness. Major neutral-ground info-hub. Note: **Crossroads** itself is an undefined location — "a bustling trade nexus where multiple territories meet"; needs geographic placement during this phase.
- `worldanvil-export/Talan/History/golden-empire.md`
- `worldanvil-export/Talan/History/storveldi-denbora.md`
- `worldanvil-export/Talan/Powerfull Beings/` — domain overview, powerful being types

Target: extend `lore/factions.md`; Red Empire and Menagerie are new and need full entries. **Also resolve**: the Nine Generals lair locations (only the Vermin Queen's Hollow placed so far — eight more dungeons to site, including a former volcanic one for the defeated Ash-Binder); the identity of the Divine Faith's god + demigod + theocratic prince (carried over from Phase 2); Crossroads' geographic placement.

---

## Phase 4 — Bestiary & Species → `lore/bestiary.md` *(new file)*
**Status: TODO**

*Talan export, purely additive.*

Source files:
- `worldanvil-export/Talan/Ancestries/` × 41 — all playable ancestries with world-flavour notes
- `worldanvil-export/Talan/Versatile Heritages/` × 14 — tieflings, aasimar, etc.
- `worldanvil-export/Talan/Demons/` × 14 — virtue demons
- `worldanvil-export/Talan/Devils/` × 7 — sin devils
- ~~`worldanvil-export/Tyrnarra/Kitsune/` × 5~~ — **merged in Phase 2 (2026-05-16)**: geography + politics + tradition + landmark folded into `lore/cultures.md` (Kitsune section) and `lore/geography.md` (Lautara > Emarrea). Pure-species mechanical detail (ancestry stats, PF2e crunch) still pending if/when Phase 4 produces a `lore/bestiary.md`.

Target: new `lore/bestiary.md` for the remaining ancestries, heritages, demons, and devils.

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
