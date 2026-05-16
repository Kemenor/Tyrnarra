# WorldAnvil → Lore Migration Plan

> ## Resume Point — 2026-05-16 (end of session)
>
> **Lore-side migration: COMPLETE.** All five phases (plus a 3.5 canon-corrections pass) are integrated into `lore/`. No further WorldAnvil-export-driven work remains.
>
> ### Current state
>
> | Phase | Lore | HTML |
> |---|---|---|
> | 1 — Cosmology | ✅ DONE | ⏳ partial |
> | 2 — Geography | ✅ DONE | ⏳ partial |
> | 3 — Factions | ✅ DONE | ❌ not started |
> | 3.5 — Canon corrections (Storveldi Denbora) | ✅ DONE | ❌ not started |
> | 4 — Bestiary | ✅ DONE (with post-remaster versatile-heritage rework) | ❌ not started |
> | 5 — Timeline | ✅ closed (absorbed into 3.5) | — |
>
> ### Most-recent canon work (late session, 2026-05-16)
> - **Mortal Ascent Ladder** + shard mechanic locked in (`world-notes.md`). Shards are *found*, not granted. Five sources: ruins, godblood battlefields, killing a Minor/Major God, Aurora Veil + Duskmire veil, planes where gods have died. **Integration procedure** is the rare-but-not-lost choke-point knowledge.
> - **Storveldi Denbora** reframed as the real Tani-killers (false-Elden-claim civilisation). The Blackened Lands are their ruined capital and the natural source of Fleshwarp and Skeleton ancestries.
> - **Versatile heritages post-remaster:** full reshuffle done. Wood (Ardande) → Feyworld lineage; Metal (Talos) → Shadowplane lineage; neither plane belongs to a bound god. Nephilim is universal divine-blood (any god) OR fiendish (any demon/devil). Dhampir reframed as undead-touched (Vampire heritage), *not* Araphel-aligned. Demons AND devils are both canonically redeemable in principle.
> - Talan HTML sanitised: Cronus tile on `talan.html` no longer leaks the GM-truth that he was mortal.
>
> ### Open work — pick up here
>
> **Bestiary follow-ups** (PF2e remaster reconciliation):
> - **Base ancestry roster rework** — the bestiary's 41 entries are pre-remaster WA imports. Needs a post-remaster pass: new ancestries to add, retired/renamed ones to remove, the domain-distribution table to re-check.
> - **Tian Xia ancestries pass** — entire Eastern-stratum batch (Oni and others). **Hungerseed** currently sits in `bestiary.md` as a TBD placeholder pending this.
> - **Individual virtue-demon names** beyond Muiral the Misshapen.
> - **Sin-devil names, planar seats, politics** — currently placeholder.
>
> **Worldbuilding hooks raised this session, not yet resolved:**
> - **Vampire origin on Talan.** Dhampir got reframed as undead-touched (not god-touched), which made vampires-as-an-independent-lineage canon. Their origin is undefined. Candidate hooks: failed Storveldi Denbora integrations, Blackened Lands émigrés, banned-god creations, Feyworld émigrés.
> - **Eight remaining Nine Generals dungeons** still need geographic placement (only the Vermin Queen's Hollow is placed).
> - **Divine Faith** — god identity, demigod ruler, theocratic prince identity all TBD.
> - **Red Empire home continent** — name, internal map, non-Imperial neighbours, crossing distance all TBD.
> - **The Storveldi Denbora integration procedure** — who holds it now, how complete the surviving record is, whether the bound thirteen know. The single largest open hook in the setting.
>
> **HTML publishing — not started yet:** full per-phase tracker in *HTML Publishing — Status Tracker* below. The user holds the publish signal; nothing should be pushed to HTML without an explicit go-ahead.
>
> **Memory:** A `feedback` memory exists noting that the user wants check-ins between phases of this migration. Future sessions should respect that.

---



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
**Status: DONE in lore (2026-05-16). Not yet published to HTML.**

*Mixed sources.*

Source files (all processed):
- ✅ `worldanvil-export/Talan/Organizations/adventurers-guild.md` — empty stub; nothing to merge.
- ✅ `worldanvil-export/Talan/Organizations/bounty-hunter-guild.md` — empty stub; dropped from scope.
- ✅ `worldanvil-export/Tyrnarra/Adventurer Guild/adventurers-guild.md` — richer write-up; merged.
- ✅ `worldanvil-export/Tyrnarra/Adventurer Guild/lord-albrecht-lavisburg.md` — merged.
- ✅ `worldanvil-export/Tyrnarra/Myrria/myrrias-godshall.md` — merged.
- ✅ `worldanvil-export/Tyrnarra/Myrria/guild-sovereign-seraphel-duskbane.md` — merged.
- ✅ `worldanvil-export/Tyrnarra/Red Empire/red-empire.md` — merged (off-continent placement, see below).
- ✅ `worldanvil-export/Tyrnarra/Red Empire/iron-tide.md` — merged.
- ✅ `worldanvil-export/Tyrnarra/Red Empire/the-menagerie.md` — merged.
- ✅ `worldanvil-export/Tyrnarra/Random/house-eisenhart.md` — merged.
- ✅ `worldanvil-export/Tyrnarra/Random/the-spiders-silk.md` — merged + Crossroads geographically placed.
- ✅ `worldanvil-export/Talan/History/golden-empire.md` — empty stub; nothing to merge (Golden Empire canon already complete in `timeline.md`).
- ✅ `worldanvil-export/Talan/History/storveldi-denbora.md` — single-line stub that triggered a major canon clarification with the user; **see Phase 3.5 below** for the full Storveldi Denbora canon and the Mortal Ascent Ladder rewrite.
- ✅ `worldanvil-export/Talan/Powerfull Beings/` — both files are empty stubs; the only useful content was the cleric-domain table, already folded into the per-god sheet in `world-notes.md`.

**What landed in `lore/factions.md`:**
- Adventurers Guild fully expanded — Scale & Branch Hierarchy (Branch Office → Guild Office → Guildhall → Kingshall → Godshall, with original "one person managing four villages" prose preserved), Rank ladder (Bronze → Silver → Gold → Platinum → Mithral → Orichalcum → Starsteel), Grand Assembly, First of the Quill & Blade, Guild Bank, Guild Post.
- Notable Guild figures: **Lord Albrecht Lavisburg** (Demi-God of Order and Ethics by accumulated belief — contemporary case study of the Wellspring & Belief mechanic), **Guild Sovereign Seraphel Duskbane** (current Sovereign of Myrria's Godshall).
- **Myrria's Godshall** — full facility writeup (public halls, restricted upper halls, regional command role).
- **Off-Continent Powers** section — the **Red Empire** placed on a separate continent across Hafra. Includes the Iron Tide (their navy, the only branch most Talanese see) and the Menagerie (Collectors are their only routine Talan presence). Established the strategic posture: a godless mortal-supremacist state attacking a god-bearing continent.
- **House Eisenhart** — dwarven noble house of the Order of Steam; Matriarch Tharka Eisenhart; the *Stahlglanz* amphibious mobile fortress; Siege of Nine Storms; Council of the Forge seats.
- **Spider's Silk Inn** at Crossroads — Matron Charna (ancient Anadi); enchanted silver silk; neutral-ground / mercenary-hiring-hall / information-exchange / sanctuary.

**What landed in `lore/geography.md`:**
- **Crossroads** placed on the tri-domain border of Lautara / Zuzental / Ezkudon (Commerce / Law / Knowledge).
- **Other Continents** section added — frames the Red Empire's home continent as canonical-but-unmapped, across Hafra.

**Open threads carried into later phases:**
- Eight remaining Nine Generals dungeons still need geographic placement.
- Divine Faith's god + demigod ruler + theocratic prince identity still TBD.
- The Red Empire home continent's name, internal map, neighbours, crossing distance — TBD.

---

## Phase 3.5 — Canon Corrections (Storveldi Denbora reveal)
**Status: DONE in lore (2026-05-16). Not yet published to HTML.**

A storveldi-denbora.md single-line stub in the WA export ("Old Race, caused death of Tani which resulted in the cataclysm — the black spot on the map") triggered a major canon clarification when raised with the user. The Storveldi Denbora are not a folk-myth name for the Elden; they are a separate real civilisation that *claimed* Elden descent falsely. This re-shapes several existing canon points.

**What got rewritten:**
- **`lore/world-notes.md`** — new dedicated section *The Storveldi Denbora — The Real History* (placed after the Elden, before the Devourer). New section *The Blackened Lands*. The Tani section names her killers and her death location. The Week of Crimson Rain trigger explicitly names the Storveldi Denbora. The Cronus secret clarifies he's the only mortal to ascend to *Grand God* specifically (the Storveldi Denbora demonstrated Demi-God and Minor God mortal ascents are possible).
- **`lore/world-notes.md`** — *The Wellspring & Belief* expanded with the **Mortal Ascent Ladder** subsection: four explicit rungs with their gates. Shards of divinity are **found, not granted** — no god's consent required. Five canonical shard sources (Talan ruins, godblood battlefields, killing a Minor/Major God, the Aurora Veil + Duskmire veil, other planes where gods have died). The **integration procedure** is the genuinely rare knowledge — the Storveldi Denbora developed it; it persists somewhere on Talan but is not public knowledge.
- **`lore/timeline.md`** — Gods' Era entry now includes the rise of the Storveldi Denbora and the Dragon mothership crash a few hundred years before era's end. Week of Crimson Rain entry names the killers and the homeland-annihilation aftermath.
- **`lore/geography.md`** — Lost Kingdom sub-region of Lioaru fully expanded as the Blackened Lands / Storveldi Denbora capital ruins. Origin of natural-born Fleshwarp and Skeleton ancestries.
- **`lore/glossary.md`** — new entries for *The Storveldi Denbora*, *The God Killing Incident*, *The Blackened Lands*, *The Darklands* (pf2e import, dominion of the Corrupted God), and *Shard of divinity*.
- **`lore/factions.md`** — Menagerie's Fleshwarp creation line clarified as distinct from the natural-born Fleshwarp ancestry of the Lost Kingdom (two origins, similar end-product).

**One HTML touch (sanitisation, not publishing):**
- `talan/talan.html:161` — the Cronus tile previously read *"Home to the only mortal ever to ascend"* which would have leaked the GM-truth that Cronus was mortal. Replaced with *"Home to Frae City, where the Council of Thirteen convenes."* The full ascension secret already lives in a proper `⚿ GM Secret` expandable in `grand-gods.html` and was not touched.

**Net effect:** Phase 3.5 absorbs about 60% of what was originally scoped for Phase 5 (the Storveldi Denbora was the more substantive of Phase 5's two stub sources). The remaining Phase 5 work is now smaller.

---

## Phase 4 — Bestiary & Species → `lore/bestiary.md` *(new file)*
**Status: DONE in lore (2026-05-16). Not yet published to HTML.**

*Talan export, purely additive.*

Source files (all processed):
- ✅ `worldanvil-export/Talan/Ancestries/` × 41 — every ancestry entry (mostly 1–3 lines each) folded in. The *ancestry-overview.md* domain mapping became the bestiary's distribution table.
- ✅ `worldanvil-export/Talan/Versatile Heritages/` × 14 — all merged. *Aasimar → Nephilim* rename applied per pf2e remaster. Heritage rework flagged as pending.
- ✅ `worldanvil-export/Talan/Demons/` × 14 — Aristotelian virtue/excess/deficiency pattern preserved; full table built. Muiral the Misshapen recorded as the only named virtue demon so far.
- ✅ `worldanvil-export/Talan/Devils/` × 7 — placeholder section with the seven-sin frame; devil-lord names TBD.
- ~~`worldanvil-export/Tyrnarra/Kitsune/` × 5~~ — bulk merged in Phase 2; species-mechanics-only summary referenced from the Kitsune entry in `bestiary.md`.

Design decisions (resolved with user 2026-05-16):
- **Dragons** are an alien race — mothership crash-landed during the Gods' Era a few hundred years before the Week of Crimson Rain. Corrupted by the gods. Capital at Dragon's Reach in Sumendar. Seeking purity / their roots.
- **Dragonkin** descend from an unholy creation of one of the gods later expelled by the Gods' Law. No relation to Dragons.
- **Azarketi** are descendants of Storveldi Denbora self-experimented survivors. They sometimes still claim Elden blood — wrong, that's the original Storveldi Denbora lie inherited forward.
- **Fleshwarps** and **Skeletons** originate from the Blackened Lands / Lost Kingdom. (Menagerie fleshwarps are a separate off-continent origin — same end-product, distinct lineage.)
- **Darklands** acknowledged as a pf2e-import term meaning deep-underground / Corrupted God's dominion. Candidate for renaming later.
- **Sentinel Dwarves** patrol the upper Darklands; **Ratfolk** originate from there; **Slimes** are concentrated there.
- **Versatile Heritages** — Jianna and Cronus left without heritage mappings (no inherited-trait blessing in current canon). Full system needs rework once pf2e remaster reshuffle settles.

**What landed in `lore/bestiary.md`:**
- Header with status note framing this as a reference, not a PF2e rules-duplicate.
- **Ancestry Distribution by Domain** table — clean per-domain ancestry breakdown derived from the WA *ancestry-overview.md* mapping.
- **41 alphabetical ancestry entries** with their world-flavour notes plus cross-references to existing canon. Major canon-load entries (Dragons, Azarketi, Fleshwarp, Skeleton, Android, Automaton, Drow elves, the two dwarf cultures) received fuller writeups; thin WA sources got concise entries.
- **Versatile Heritages** — table of the 12 mapped heritages (bound god + domain) with rework note for the unmapped two (Jianna, Cronus) and the unchanged-pending ones (Reflection, Tiefling).
- **Virtue Demons — the Aristotelian Pattern** — full virtue/excess/deficiency table; Muiral the Misshapen recorded.
- **Sin Devils — the Seven** — placeholder section with the seven-sin frame and a clean demon-vs-devil theological distinction (demons corrupt a virtue, can in principle be redeemed; devils embody a sin, cannot).
- Cross-references section linking back to `world-notes.md`, `geography.md`, `cultures.md`, `factions.md`.

**Bestiary additions in `lore/glossary.md`:**
- *Muiral the Misshapen*, *The Virtue Demons*, *The Sin Devils* — bestiary proper nouns.
- *"Elden blood"* and *"the corruption by the gods"* — folklore claims preserved with truth-status notes.

**Open threads:**
- **Base ancestry roster rework** — the pf2e remaster also reshuffled the core ancestry list (renames, splits, merges, new options, retired options). The bestiary's 41 entries are imported from the WA export (pre-remaster) and need a remaster-era pass.
- **Tian Xia ancestries pass** — the full Eastern-stratum ancestry roster (Oni and others) is planned as a batch. **Hungerseed** sits in the bestiary as a *TBD* placeholder pending this pass.
- Individual virtue-demon names beyond Muiral.
- Sin-devil names, planar seats, and politics.

**Recently closed (post-remaster pass 2026-05-16):**
- ✅ **Versatile heritage rework** — full post-remaster roster placed. New cosmology established: divine-blood heritages map to bound thirteen + demons/devils (Nephilim now universal); Elemental Plane heritages (Ifrit/Oread/Sylph/Undine/Suli) carry Layer-1 Prelife sparks with domain affinity; **Wood (Ardande) → Feyworld lineage**, **Metal (Talos) → Shadowplane lineage** — the two new elements occupy the two non-Material planes of the Life Layer. Aiuvarin / Dromaar are genetic; Dragonblood ties to alien Dragons; Reflection is Wellspring-mishap. Tiefling absorbed into Nephilim (no longer a distinct heritage).

Target: ✅ achieved. Bestiary is the reference; deeper development happens as the world is played.

---

## Phase 5 — Timeline & History → `lore/timeline.md`
**Status: Mostly absorbed by Phase 3.5. Remaining: trivial.**

The two WA source files were both stubs (`golden-empire.md` empty; `storveldi-denbora.md` single-line). The Storveldi Denbora line drove the Phase 3.5 canon corrections, which then folded the Storveldi Denbora rise/fall and the Dragon mothership crash directly into `lore/timeline.md`'s Gods' Era entry and updated the Week of Crimson Rain entry. The Golden Empire entry in `timeline.md` was already complete and required no addition.

**No further Phase 5 work is required.** Closing out.

---

## HTML Publishing — Status Tracker

The migration above describes work into **`lore/`**. None of it has been published to the HTML site yet — the user holds the publish signal (per `CLAUDE.md` drafting protocol).

The table below tracks which lore additions await HTML publication when the user gives the go-ahead.

| Lore content | Lore file | Awaiting HTML publish to |
|---|---|---|
| **Phase 1 — Cosmology & Foundation** | | |
| Tyrnarra & the Cloud Sea (Solyra/Veyru/Calune) | `world-notes.md` | `index.html` (cosmology landing) — possibly already covered, audit pending |
| Full Three-Layer planar structure | `world-notes.md` | `index.html` planar section — audit pending |
| Sanctum-as-literal-home + Council of Thirteen | `world-notes.md` | `grand-gods.html` / Cronus's Frae City page |
| Per-God Sheet (aspects, weapons, depictions for all 13) | `world-notes.md` | `grand-gods.html` cards — partially mirrored, audit per-card |
| Age of Corruption mortal myth | `world-notes.md` | history page mortal-myth expandable |
| **The Seven Wardstones** (full table) | `world-notes.md` | `the-binding.html` — partially mirrored (Araphel context), table needs publishing |
| **The Nine Generals + Nine Dungeons** | `world-notes.md` | `the-binding.html` + `factions/remnants.html` |
| **Araphel deep dive** (sanctum, rites, iconography) | `world-notes.md` | `domains/myrkono/myrria/myrria.html` — partially mirrored; rites + sacred-symbol detail to add |
| **Phase 2 — Geography** | | |
| Fenurra placement (Lands of Villtur, meteor + volcanism) | `geography.md` | new `domains/ehizahar/fenurra.html` — already exists, audit completeness |
| Twin Cities (Midarra pirate capital) | `geography.md` | new section on `domains/askamira/` or Midarra-themed page |
| Emarrea + Biozuri + Kawaakari (kitsune kingdom) | `geography.md` | new `domains/lautara/emarrea/` folder |
| Myrria's 8 districts | `geography.md` | `domains/myrkono/myrria/myrria.html` — district detail to publish |
| Hollow of Ten Thousand Threads | `geography.md` | `the-binding.html` (Nine Dungeons section) or own page |
| **Crossroads** (tri-domain trade nexus) | `geography.md` | new page or section on Lautara |
| **The Blackened Lands / Lost Kingdom expansion** | `geography.md` | new page under `domains/lioaru/` |
| **Other Continents** framing | `geography.md` | continent-overview note on `talan.html` or own page |
| Fenurran culture (4 tribes, weapons, doctrine) | `cultures.md` | section on `fenurra.html` |
| Kitsune culture (Heartcourt, 9 Hearts, Catjomin Sake) | `cultures.md` | section on emarrea-area page |
| **Phase 3 — Factions** | | |
| Adventurers Guild full expansion (ranks, branches, Bank, Post, Grand Assembly) | `factions.md` | `factions/adventurers-guild.html` — currently has the original short writeup; needs major expansion |
| Lord Albrecht Lavisburg | `factions.md` | Guild page (Notable Figures section) |
| Seraphel Duskbane + Myrria's Godshall | `factions.md` | Guild page or Myrria page |
| The Divine Faith / Legea Empire | `factions.md` | new page under `factions/` (or Zuzental sub-page) |
| **The Red Empire + Iron Tide + Menagerie** | `factions.md` | new page under `factions/` — flagged as off-continent |
| **House Eisenhart** + Tharka + *Stahlglanz* | `factions.md` | new page under `factions/` (or Order of Steam settlement page) |
| **Spider's Silk Inn** + Matron Charna | `factions.md` | new page under `factions/` or under Crossroads |
| **Phase 3.5 — Canon Corrections** | | |
| **The Storveldi Denbora** full history | `world-notes.md` | new GM-Secret expandable on `history.html` Gods' Era card |
| **The Blackened Lands** entry | `world-notes.md` | new GM-Secret expandable on `history.html` or Lioaru page |
| **The Mortal Ascent Ladder** (4 rungs, shard sources, integration procedure) | `world-notes.md` | best on a magic / theology subpage; partly fits in `magic.html` (Wellspring & Belief expansion) |
| Updated Tani section (her killers, where she died) | `world-notes.md` | `grand-gods.html` Tani card (mortal-side stays neutral; full detail in GM Secret) |
| Updated Cronus secret framing (only Grand-God ascender) | `world-notes.md` | `grand-gods.html` Cronus secret — minor tweak; current text is broadly OK |
| **Phase 4 — Bestiary** | | |
| Ancestry distribution by domain (table) | `bestiary.md` | new `bestiary.html` overview page, or per-domain ancestry notes on each domain page |
| 41 ancestry entries (Dragons, Azarketi, Fleshwarp, Skeleton, etc.) | `bestiary.md` | new `bestiary.html` or per-ancestry pages under `bestiary/` |
| Versatile Heritages mapping | `bestiary.md` | `bestiary.html` heritages section — flag rework-pending |
| Virtue Demons (Aristotelian pattern) | `bestiary.md` | new page under `factions/` (or sit on a new `bestiary/demons.html`) |
| Sin Devils (placeholder) | `bestiary.md` | placeholder section on the same demons/devils page |

**Publishing order suggestion (when ready):**
1. The Wardstones and Nine Generals (`the-binding.html`) — already partially built, lowest-friction completion.
2. New domain/settlement pages for the placed locations (Crossroads, Emarrea, Lost Kingdom).
3. New faction pages (Red Empire, House Eisenhart, Spider's Silk Inn).
4. Adventurers Guild HTML rewrite to incorporate the rank ladder, branch hierarchy, Bank, Post, and figures.
5. Storveldi Denbora secret on `history.html` (sensitive — GM-Secret expandable; mortal-facing history should preserve the Elden-conflation folk-myth).
6. Mortal Ascent Ladder on `magic.html` or a new theology page (player-facing portions; the integration-procedure detail stays GM-only).

---

## Skip / Discard

These are campaign artefacts or non-canon imports — do not migrate:

- `worldanvil-export/Talan/Campaigns/`, `Player Handbook/`, `Staging Area/` — campaign ops, not world lore
- `worldanvil-export/Talan/Other/readme.md` — WorldAnvil housekeeping
- `worldanvil-export/Talan/balaena.md`, `ashka.md`, `lukas-s.md`, `mad-mage.md` — player/NPC session notes
- `worldanvil-export/Talan/Gods/golarion-gods.md` — Pathfinder import, not Tyrnarra canon
