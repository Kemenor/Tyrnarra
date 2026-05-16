# WorldAnvil → Canon Name Reconciliation (Phase 2 prep)

Built **2026-05-16** as the first step of [Phase 2 — Geography & Domains](worldanvil-migration.md#phase-2--geography--domains-loregeographymd). Cross-checks WA export folder/file names against canon in [`lore/geography.md`](../lore/geography.md) and the published HTML at [`talan/domains/`](../talan/domains/).

**Rule reminder:** WA names are old working names from 2023. `lore/geography.md` wins on conflict.

---

## Headline finding — almost nothing to migrate

The WA Talan export for Phase 2 is overwhelmingly **empty stubs**:

| Source folder | Files | With real content | Notes |
|---|---|---|---|
| `Talan/Regions/` | 13 | **0** | All are UUID-reference shells (god + kingdoms + races) — zero narrative. |
| `Talan/Kingdoms/` | 50 | **0** | All 8-line frontmatter stubs. (`lost-kingdom.md` has one throwaway line "Human meat on a stick - food".) |
| `Talan/Settlementsja/` | 14 | **1** | Only `myrria.md` has a paragraph. `twin-cities.md` has the phrase "Flying Pirate + Floating Pirate". The rest are empty. |
| `Talan/Fenurra/` | 20 | **most** | `fenurra.md` is a full culture write-up; siblings cover the four major tribes (Draconis / Vexiren / Brakkaun / Seravain) and their signature weapons. Substantial new lore. |

**Practical consequence for Phase 2:** the geography migration is essentially a *name-mapping exercise plus one Myrria paragraph plus the Fenurra block*. Almost no prose to merge.

Fenurra is a Phase-2/3 hybrid (it's geography *and* culture *and* weapons/factions) and probably deserves its own discussion before merging — see open questions below.

---

## Name mapping

### Regions/ — WA file → canonical domain

The WA Region files are named by the god's domain-concept word (chaos, commerce, etc.). 1:1 mapping, no ambiguity:

| WA file | Canonical domain | God |
|---|---|---|
| `chaos.md` | Nashavel | Vesuna |
| `commerce.md` | Lautara | Jianna |
| `darkness.md` | Myrkono | Araphel |
| `earth.md` | Brauogi | Sarrum |
| `fire.md` | Sumendar | Komo |
| `freedom.md` | Askamira | Cronus |
| `hunt.md` | Ehizahar | Hinka |
| `knowledge.md` | Ezkudon | Enki |
| `law.md` | Zuzental | Forseti |
| `light.md` | Egulon | Iro |
| `time.md` | Lioaru | Tani |
| `water.md` | Floteyn | Shuun |
| `wind.md` | Vindul | Fisaya |

### Kingdoms/ — WA slug → canonical sub-region

The WA Kingdom slugs already match canonical sub-region names in `lore/geography.md`. No translation needed. A few notes on edge cases:

- **`no-mans-land-knowledge.md` / `no-mans-land-komo.md`** — WA split the canonical entries. In canon, **No Man's Land** is the *shared* unclaimed border between Brauogi and Ezkudon (the wild-touched live there); separately, **No Man's Land (Komo)** is the unclaimed territory inside Sumendar that houses Eldara. Keep the two distinct in lore — they are different places that share a name.
- **`harro-distiratsua.md`** — canon spelling is **Harro Distiratsue** (final -e, not -a). Use the canon spelling.
- **`soul-tree.md` / `star-island.md` / `lost-isle.md` / `emerald-isles.md` / `burdineyja.md` / `haizetsua.md` / `three-pines.md` / `floating-isles-of-shuun.md` / `ardo-beroa.md`** — these are technically islands, not kingdoms, but they're catalogued under Kingdoms in WA. Already represented under their parent domains in canon.
- **WA has no entries for** these canon sub-regions: Hareaveldi ✓ (it does — `hareaveldi.md`), Fellibylur ✓, Emarrea ✓. Good coverage. **Missing from WA**: any new sub-regions added to canon after the WA freeze date — none currently identified.
- **`order-of-steam.md` / `order-of-law.md`** — these are political orders, not pure geography. Order of Steam is already a canonical sub-region of Sumendar; Order of Law is a Zuzental sub-region in canon. Treat as places when migrating, not as factions (factions get their own Phase 3 pass).

All 50 WA Kingdom slugs have a canonical home. Since the files are empty, there's nothing to *write* — just confirms the canon naming is complete enough that future content placement is unambiguous.

### Settlementsja/ — WA working name → canonical god-city

The 14 settlement files are old working names for the god city-states. **All 14 files are empty stubs except `myrria.md` and `twin-cities.md` (which has one fragment line).** Mapping below is for *future reference only* — there's no prose to migrate.

| WA file | Canonical god-city | Domain | Confidence | Reasoning |
|---|---|---|---|---|
| `frae-city.md` | Frae City | Askamira (Cronus) | **certain** | Same name |
| `myrria.md` | Myrria | Myrkono (Araphel) | **certain** | Same name; file content confirms ("Arophel the god of Darkness, resides in the city state of Myrria") |
| `hairia.md` | Haizava | Vindul (Fisaya) | high | Both rooted in Basque *haize* (wind) |
| `ljoria.md` | Ljosarn | Egulon (Iro) | high | Shared Icelandic *ljós* (light) root |
| `kaoria.md` | Nahaskel | Nashavel (Vesuna) | high | "Kao-" = chaos |
| `justiria.md` | Lograth | Zuzental (Forseti) | high | "Just-" = law/justice |
| `ezaria.md` | Thekkavar | Ezkudon (Enki) | high | "Ez-" matches Ezkudon (hidden/concealed) |
| `baria.md` | Lurrath | Brauogi (Sarrum) | medium | B for bread/earth; no clearer signal |
| `mendia.md` | Eldara | Sumendar (Komo) | medium | Basque *mendi* (mountain) matches the volcanic-mountain Sumendar identity |
| `azmaria.md` | **DROPPED** | — | — | User confirmed 2026-05-16: drop, not canon. |
| `zilarria.md` | **DROPPED** | — | — | User confirmed 2026-05-16: drop, not canon. |
| `dauria.md` | Denbora | Lioaru (Tani) | low | Note: "Dauria" is *also* the canonical plane-of-rebirth name in `world-notes.md` — easy to confuse. If this file represents the city, it's likely Denbora. If it represents the plane, skip (already covered in Phase 1). |
| `varia.md` | Veidrath | Ehizahar (Hinka) | low | V→V; no other strong signal |
| `twin-cities.md` | **Twin Cities (new canon)** | Midarra — independent | **canon** | User defined 2026-05-16: paired pirate-capital settlement (water-raft city + sky-island of airships) drifting through Midarra on a course set by the Pirate Lords. Not a god-city. Captured in `lore/geography.md` (Three Seas → Midarra) and `lore/glossary.md`. |

**Unmatched canonical city** (no WA file even speculatively maps to it): **none** — the 14 WA files cover all 13 canonical city-states with one over-counted slot (azmaria + zilarria both plausibly Merkavar).

---

## Fenurra — RESOLVED (2026-05-16) — fully imported

**Geography (2026-05-16, am):** Fenurra placed as a sub-territory of **Lands of Villtur** (Ehizahar). Volcanic activity around an ancient meteor crater added to Ehizahar's terrain in `lore/geography.md`. Etymology coined in `lore/glossary.md` (Icelandic *funi* "flame" + Basque *iturri* "source" → *funi-iturri* → eroded to *Fenurra*).

**Culture (2026-05-16, pm):** Full Fenurran cultural import completed into new file `lore/cultures.md`. Covers:
- All four tribes — Draconis (The Scaled Flame), Vexiren (The Ember-Eyed), Brakkaun (The Bone-Burdened), Seravain (The Soulbound). Each with character, geography, beliefs, signature tactics, symbols.
- The Speaker's Mantle (currently Draconis-held).
- The Bone Gong call-system (1/2/3/5 strikes + the single-strike Ash Seat Trial during council).
- The War Council institution — earned consensus over chain-of-command.
- Materials: Blackglass, Velthite, Ghost Willow, Obsidian Silk, Spice Wine, plus the Fenurran technical vocabulary (Slagsteel, Cratersteel, Emberframe, etc.).
- The Infernal-Smoked Hook-Line-Sinker Charge doctrine.
- Notable weapons table (Drakar Talons, Blackglass blades, Draconic Double-Glaive, Whisperfang bow + arrow variants, Vexiren Fanghook, Brakkaun Meteor Hammers, Siege Splitter, Seravain Asp Coil/Wrist Launcher, Claw Dart/Bastion Ringblade, Inferna Blades, Cradle Halberd).
- Open threads logged at the bottom of `cultures.md` — the **Divine Faith** missionary religion (identity TBD), the **theocratic prince** married into the Draconis (faction TBD), and a placeholder note on whether Aeris/Scar-of-Aeris should be retrofitted to the deep-old naming stratum.

Filename note: WA used "sevarain" in file slugs but "Seravain" in the master article. Canon spelling is **Seravain**.

---

## Fenurra — original analysis (pre-decision, kept for record)

`Talan/Fenurra/fenurra.md` describes a fully-realised culture: volcanic wasteland, four named tribes (Draconis / Vexiren / Brakkaun / Seravain), a meteor-crater origin ("the Scar of Aeris"), Blackglass / Velthite / Ghost Willow materials, the Speaker's Mantle politics, recent schism caused by Divine Faith missionaries, political marriage with a theocratic prince.

This **doesn't appear anywhere in `lore/geography.md`** or the published domain HTML. Before migrating, decide:

1. **Is Fenurra inside Sumendar?** The volcanic/sulfurous character and "monstrous beasts" framing fits Komo's domain, and it could plausibly be one of Sumendar's currently-TBD sub-regions (Haraour Eliza? Tahu Tangata? — note Tahu Tangata is already in canon as Sumendar's indigenous coastal culture, and the names don't match Fenurran tribe names). It's *probably not* Tahu Tangata.
2. **Is Fenurra a separate northern region?** The text says "To the opulent kingdoms of the south, Fenurra is a nightmare given form" — implies Fenurra is *north* of the rich southern kingdoms. Doesn't fit Sumendar (south-southwest).
3. **Is Fenurra a non-Talan continent?** It could be a separate landmass entirely.
4. **Naming check:** Fenurra ends in -rra like Tyrnarra. Likely an old-language name (the convention permits this). Tribe names — Draconis, Vexiren, Brakkaun, Seravain — are English/Latinate, fitting *new* things. Mixed-age naming is consistent with a long-lived culture.

**Recommendation:** Treat Fenurra as a deferred sub-item. Migrate `Fenurra/fenurra.md` into `lore/geography.md` as a new sub-region/region *after* deciding placement, and migrate the four tribe write-ups + weapons into either `lore/factions.md` (Phase 3) or a new `lore/cultures.md`. Don't merge until placement is settled.

---

## What this means for the rest of Phase 2

Phase 2 is much smaller than the file count suggests:

1. **No-op:** Confirm the 13 Region mappings and 50 Kingdom slug matches — done above. Nothing to write into `lore/geography.md` from these.
2. **Tiny merge:** Myrria's paragraph into a future Myrkono settlement entry. (Or skip — the published `talan/domains/myrkono/myrkono.html` likely already captures the equivalent.)
3. **Open decision then merge:** Fenurra block — needs a placement decision before it can land in lore.
4. **Cleanup note for the migration doc:** flag that the Settlementsja and Kingdoms folders are not worth re-running through any future converter — they are placeholder entries from the 2023 WA build and won't gain content unless re-edited on WA first.

After this, Phase 2 effectively closes pending the Fenurra placement call.
