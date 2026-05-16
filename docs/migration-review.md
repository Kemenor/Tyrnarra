# WorldAnvil → Lore Migration Review
*Generated 2026-05-16 against `worldanvil-export/` and `lore/`. **All discrepancies resolved 2026-05-16 — see Resolution log at bottom.***

## Summary
- Files audited: 233 (25 Tyrnarra-side + 208 Talan-side)
- Confirmed migrated (substantive content present in lore): 50
- Intentionally and correctly skipped (empty WA stubs or pre-declared skips): 173
- Discrepancies / questionable skips found: 10
- Stub batches spot-checked: 4 (Regions, Settlementsja, Kingdoms, Grand Gods per-god files)

The migration is in excellent shape overall — every substantive piece of WA prose has been carried into `lore/`, often with expanded detail beyond the source. The discrepancies below are small named-detail omissions and a handful of standalone worldbuilding sketches that the migration doc treated as "skip" without clearly justifying why.

---

## Discrepancies

### High priority — missed content

1. **`worldanvil-export/Talan/balaena.md` — the Skywhale City "Balaena"**
   The migration doc lists `balaena.md` under "Skip / Discard" alongside player/NPC session notes — but `balaena.md` is not a session note. It is a self-contained worldbuilding sketch for a settlement: a city built atop a half-submerged weak skywhale in a lake, with a weight-management entry protocol, twice-daily fountain shower from the blowhole, and a secret organisation keeping the whale alive-but-grounded. No content from this file appears anywhere in `lore/`.
   → Suggested target: `lore/unplaced.md` (no placement decided) or a new entry in `lore/geography.md` once a domain is chosen. The skywhale concept is too distinctive to discard silently.

2. **`worldanvil-export/Talan/Other/the-conductor-and-his-station.md` — the Lost-and-Found train station**
   Not addressed by the migration doc at all (the doc skips `Other/readme.md` but doesn't name this file). The file is substantive: a pocket-dimension train-station gimmick where trains occasionally derail into a void-bound "Lost and Found" siding presided over by a five-eyed Conductor, with an escape-via-riddle puzzle hook. Includes a Swiss-German design note from the author. Nothing about this in lore.
   → Suggested target: `lore/unplaced.md` for now; eventually fits as a Cronus / Travel-domain or chaos planar hazard.

3. **`worldanvil-export/Talan/Staging Area/train-pirates.md` — Grav Trains + ultra-high-tech remnants**
   Migration doc skips the whole `Staging Area/` folder as "campaign ops, not world lore" — but this file is worldbuilding, not ops. It establishes: trains are slow on land but very fast on rail (Grav Train physics); the technology is recovered from an "Ultra High Tech Civilisation"; only short routes exist; faster speeds only during the Hunt era. The "ultra high tech civilisation" line is genuinely interesting and could plug into the Storveldi Denbora / pre-Counting-of-Years tech canon.
   → Suggested target: a glossary entry plus a note in `lore/world-notes.md` under a tech / pre-history hook.

### Medium priority — partial migration

4. **Domara, Judge of Souls (from `Talan/World Atlas/planes.md`)**
   The Talan-side planes file names "Domara, the judge of souls" as residing in Dauria, the City of the Dead. Lore has Dauria (geography correct) but no Domara — the named entity is dropped. Migration doc declared the Talan World Atlas planes file "superseded by Tyrnarra-side files; nothing new to import," but the Tyrnarra-side planes file does not name Domara either. So the name was dropped without conscious decision.
   → Suggested target: `lore/world-notes.md` Diyu / Dauria entry; `lore/glossary.md` as a coined name (note: "Domara" reads English-plain, may want to be re-coined to the Basque/Icelandic deep stratum per CLAUDE.md if Dauria-era).

5. **Vesuna and Hinka — missing "Extra Domains"**
   The per-god cleric-domain table in `world-notes.md` was sourced from `Talan/Powerfull Beings/domain-overview.md`. Two extras were dropped:
   - **Vesuna — Extra Domain: Free Will** (WA source has it; lore lists only Passion, Luck, Trickery).
   - **Hinka — Extra Domain: Violent Death** (WA source has it; lore lists only Might, Nature, Zeal).
   All other Grand Gods with an extra domain (Jianna→Progress, Araphel→Second Chances, Cronus→Soul, Tani→Peaceful Death) made it across, so this is a two-entry oversight rather than a policy.
   → Add to `world-notes.md` per-god sheet.

6. **The "No Extra Gods" domain list (`Talan/Powerfull Beings/domain-overview.md`)**
   At the bottom of the same file, an unexplained list: *"Abomination; Pain; Plague; Swarm; Undeath; Naga; Delirium; Indulgence; Sorrow; Tyranny; Destruction; Nightmares; Decay; Toil"*. Reads like a list of cleric domains that are deliberately not bound to any of the Thirteen (i.e. evil/demonic/devilish domains owned by demons, devils, or the Corrupted God). Not reflected anywhere in lore.
   → Worth a one-line note in `world-notes.md` or `bestiary.md` clarifying that these PF2e domains exist in the setting but belong to demons/devils/the Corrupted God, not the bound Thirteen.

7. **`Talan/Kingdoms/lost-kingdom.md` — single odd line "Human meat on a stick - food"**
   The Lost Kingdom / Blackened Lands has been fully migrated as the Storveldi Denbora ruin (Phase 3.5). But the one prose detail in the WA stub — that the inhabitants ate human-flesh-on-a-stick as everyday food — is not reflected. Small but distinctive cannibalism flavour for the Storveldi Denbora.
   → One line in the `lore/geography.md` Lost Kingdom entry would close this.

8. **`Talan/Major Gods/the-twins.md` and `Talan/Minor Gods/the-eldest.md`** *(low confidence — listing for completeness)*
   Both files are pure empty stubs in WA. The `domain-overview.md` reveals their domains: **The Twins (Major God) → Moon**, **The Eldest (Minor God) → Wyrmkin**. The migration doc declared Major/Minor gods skipped because the files are empty, which is correct as far as it goes, but the *names* "The Twins" and "The Eldest" plus their domain assignments are an explicit canon signal that non-Grand gods exist on Talan with stated portfolios — and that signal is not picked up anywhere in lore. The lore implicitly treats the Thirteen plus the bound Corrupted God plus the Divine-Faith god as the whole pantheon.
   → Either accept these as deprecated 2023 drafts and ignore, or add a brief "Other Gods (named but underdeveloped)" sub-section in `world-notes.md`. Worth a user decision, not a silent fix.

### Low priority — wrong-place / minor

9. **Aphorite / Beastkin / Changeling / Dhampir / Duskwalker / Ganzi original god-pairings**
   The WA Versatile Heritages folder pairs each heritage to a specific Grand God (Aphorite→Forseti, Beastkin→Hinka, Changeling→Araphel, Dhampir→Araphel, Duskwalker→Tani, Ganzi→Vesuna). The post-remaster rework in `lore/bestiary.md` rearranged most of these for legitimate reasons (Aasimar→Nephilim is universal divine-blood; Dhampir reframed as undead-touched; etc.) and the migration doc flags the rework explicitly. So this is *not* a discrepancy — it's a documented canon correction. **Listed here only so the audit trail is complete.**

10. **Aeris / Scar of Aeris etymology** *(already a known open thread in the migration doc)*
    The Fenurra content is migrated wholesale into `cultures.md`, including the Latinate names "Aeris" and "Scar of Aeris." The migration doc flags this as an open question (Latinate vs. retrofit to the Basque/Icelandic deep stratum). No action needed beyond what's already tracked.

---

## Confirmed migrations (by phase)

- **Phase 1 — Cosmology & World Rules** (`world-notes.md`): All Tyrnarra-side core files (`tyrnarra.md`, `the-thirteen.md`, `gods-sanctum.md`, `Planes/planes.md`, `Base Setting/the-age-of-corruption.md`) verified present with full detail. The Wardstones (×7 by location), the Nine Generals (all named: Vermin Queen, Rot-Tyrant, Blight-Seer, Flesh-Sculptor, Ash-Binder, Whisperer in Dreams, Maw Serpent, False Saint, Root-Twister), Sage Lorant of Highspire / Blightfather / Maw Below folk names, Council of Thirteen, sanctum-as-home, Cloud Sea / Solyra / Veyru / Calune, Three-Layer planar structure with Aurora Veil + Ethereal + Duskmire — all confirmed.
- **Phase 1 (Grand Gods folder)**: All 13 per-god Talan-side files are 10-13 line domain-tag stubs; the cleric domains were folded into the per-god sheet (except for the two extra-domain omissions noted above).
- **Phase 2 — Geography** (`geography.md`, `cultures.md`): Fenurra full transplant — all four tribes (Draconis, Vexiren, Brakkaun, Seravain), all weapons (Drakar Talons, Blackglass blades, Ghost Willow / Whisperfang bow, Fanghook, Meteor Hammer variants, Asp Coil + Wrist Launcher, Claw Dart + Bastion Ringblade, Inferna Blades, Cradle Halberd, Sulflare tubes, all five Emberframe arrow variants), all institutions (Bone Gong, War Council, Speaker's Mantle, Ash Seat Trial), all materials (Blackglass, Velthite, Ghost Willow, Spice Wine), the Infernal-Smoked Hook-Line-Sinker doctrine, and the Three Bodies One Mind mounted style — all verified in `cultures.md`. Kitsune kingdom (Emarrea/Biozuri/Kawaakari/Heartplaza), Heartcourt with all nine Hearts and their colours, Catjomin Sake with the nine-stripe table fully preserved, House of a Thousand Flavors with all seven named chefs (Rinza, Maeko, Tairen, Shouka, Virel, Kyome, Elhara), Kawaakari amenities (Hoshigawa, Yukihime-shu, Foxfire Stone Massage, Festival of the Fox Lanterns) — all confirmed. Myrria full 8-district breakdown and the Hollow of Ten Thousand Threads also verified.
- **Phase 3 — Factions** (`factions.md`): Adventurers Guild full hierarchy (Branch → Office → Guildhall → Kingshall → Godshall, all 7 ranks, Grand Assembly, First of the Quill & Blade, Guild Bank, Guild Post), Lord Albrecht Lavisburg (titles, Aura of Compliance, Ethics Smite, all the comic detail), Guild Sovereign Seraphel Duskbane, Myrria's Godshall internal layout (Postboard, Taproom, Trophy Wall, Hall of Quests, Lantern Archive, War Vaults, Council Chamber), Red Empire complete (Crimson Emperor, Pyre Throne, all seven social castes plus Fodder, Ashen Guard, Trial of Ash), Iron Tide (Flamefangs, Frostfangs, Steam Hulks, Corsair Auxilia, Admirals of Flame and Frost, Frost-Bolt Ballistae, Steam Cannons), Menagerie (Master Curator → Curators → Keepers → Collectors, plus Augments / Exemplars / Apex Line / Ashborn / Harvested / Fleshwarps categories, Fleshwright slang, Perfection-has-no-pity motto), House Eisenhart (Tharka, *Stahlglanz*, Eisenhart Leviathan-class, Ironwing line, runeblade bayonets, Siege of Nine Storms, Council of the Forge), Spider's Silk Inn (Matron Charna, Webroom, Hiring Wall, the regular's narrative description) — all confirmed.
- **Phase 3.5 — Canon Corrections** (`world-notes.md`, `geography.md`, `timeline.md`, `glossary.md`, `factions.md`): Storveldi Denbora canon, Blackened Lands, Mortal Ascent Ladder (four rungs, five shard sources, integration procedure), Tani killers, Cronus-only-Grand-Ascender clarification, Dragon mothership crash, Lost Kingdom expansion as Storveldi Denbora capital ruin — all verified.
- **Phase 4 — Bestiary** (`bestiary.md`): All 41 `Talan/Ancestries/` files (each was a 10-14 line WA stub, all reflected with at least short entry; major ancestries — Dragons, Azarketi, Fleshwarp, Skeleton, Sentinel Dwarves, Drow elves, Android, Automaton — expanded properly). All 14 `Talan/Versatile Heritages/` files migrated and reworked per post-remaster canon. All 14 `Talan/Demons/` virtue-demon files (Aristotelian virtue/excess/deficiency mapping for Ambition, Conscientious, Courage, Friendliness, Friendly, Industrious, Liberality, Magnanimity, Modesty, Patience, Spirited, Temperate, Truthfulness, Wittiness) preserved as a table; Muiral the Misshapen named. All 7 `Talan/Devils/` files (the seven sins) are pure single-word stubs in WA — the seven-sin frame is present as a placeholder in bestiary, individual sin-devil names remain TBD as the migration doc acknowledges.
- **Phase 5 — Timeline** (`timeline.md`): Both WA source files (`golden-empire.md` empty, `storveldi-denbora.md` one line) absorbed via Phase 3.5. Golden Empire entry was already complete in lore. No work outstanding.

---

## Stub batches spot-checked

- **`Talan/Regions/` (13 files)** — sampled chaos, darkness, earth, fire, hunt, water, freedom, light, commerce. **Confirmed: every Regions file is a pure WA reference-link manifest** (no prose; just `@(article:...)` and `@(ethnicity:...)` cross-reference tokens listing the god, kingdoms, and dominant/uncommon races for the region). The link-manifest data (which races dominate which domain) was already captured in `bestiary.md`'s Ancestry Distribution table via `ancestry-overview.md`. No prose to migrate.
- **`Talan/Settlementsja/` (14 files)** — sampled azmaria, baria, dauria, ezaria, frae-city, hairia, justiria, kaoria, ljoria, mendia, varia, zilarria, twin-cities, myrria. **Confirmed: 12 of 14 are pure header-only stubs**. The only two with prose: `myrria.md` (one paragraph, already migrated and superseded by the much fuller Tyrnarra-side `Myrria/myrria.md`), and `twin-cities.md` (six words: "Flying Pirate + Floating Pirate" — fully reflected in the Twin Cities canon). Migration doc's claim holds.
- **`Talan/Kingdoms/` (51 files)** — sampled azkamour, baerfrost, thousand-kingdom, order-of-steam, legea-empire, vernua-dominion, lost-kingdom, dragons-reach, emarrea, tahu-tangata, ardo-beroa, basamortua, basogur-jungle, emerald-isles, soul-tree. **Confirmed: 50 of 51 are pure 8-line header-only stubs**. The single exception is `lost-kingdom.md` (one line: "Human meat on a stick - food") — flagged above as Discrepancy 7.
- **`Talan/Grand Gods/` (13 files)** — all sampled. **Confirmed: 12 of 13 are 10-line domain-tag stubs**; only `hinka-god-of-hunt.md` has an extra 2 lines ("God of Hunt. Typically depicted as Redheaded Women of orcish or" — sentence truncates mid-word). The orc redhead depiction is already preserved in `world-notes.md` Hinka entry.

---

## Open questions for the user

*(All resolved — see Resolution log below.)*

---

## Resolution log — 2026-05-16

All ten discrepancies addressed in a single follow-up pass.

### Mechanical fixes (no creative choices)

1. **Balaena, the Conductor's Station, Train Pirates** → captured in `lore/unplaced.md` under new *Settlements* and *Technology* sections, with full WA detail preserved and placement candidates noted.
2. **Vesuna's "Free Will"** → added to her cleric-domains line in `world-notes.md` per-god sheet.
3. **Hinka's "Violent Death"** → added to her cleric-domains line in `world-notes.md` per-god sheet.
4. **Lost Kingdom cannibalism flavour line** ("meat on a stick") → added to the Lost Kingdom entry in `geography.md` (Lioaru sub-region).
5. **Aphorite/Beastkin/Changeling/Dhampir/Duskwalker/Ganzi** → confirmed canon-corrected by post-remaster rework (not a discrepancy, listed for audit completeness).
6. **Aeris / Scar of Aeris etymology** → confirmed pre-existing open thread, no action needed.

### Creative work (proposed then approved by user)

7. **Domara → Epairima** (Basque *epai* "judgment" + *arima* "soul" → drifted). Adopted with recoinage. Placed in Diyu, as Judge of Souls of Dauria. Added to `glossary.md`; full entry in `world-notes.md` under *Named Non-Bound Gods*.
8. **The Twins → Bikiargi** (Basque *biki* "twin" + *argi* "light"). Major God of the Moon, two beings sharing one portfolio (one good, one evil). Placed in Diyu (neutral, because they balance). Added to `glossary.md`; full entry in `world-notes.md`. **Sun god noted as future thread** — paired-mate by symmetry, not yet detailed.
9. **The Eldest → Zaharsuge** (Basque *suge* "serpent" + *zahar* "ancient"). Minor God of Wyrmkin, predates the alien Dragons. Placed in Diyu. Added to `glossary.md`; full entry in `world-notes.md`. Hook seeded: indigenous wyrm-cults vs. Dragon's Reach's authority claim.
10. **"No Extra Gods" domain list (14 domains)** → mapped to specific granters in a new *Domains Outside the Thirteen — Source Mapping* table in `world-notes.md`. Bucket spread: 1 Corrupted God direct (Plague), 4 Generals of Corruption (Decay/Swarm/Naga/Nightmares — serve Corrupted God), 1 Muiral the Misshapen (Abomination), 1 Betibizi (Undeath), 3 Sin-Devils (Tyranny/Destruction/Indulgence — Pride/Wrath/Gluttony respectively), 4 virtue-demons (Pain/Toil/Sorrow/Delirium). Cross-referenced from `bestiary.md`.

### Bonus closures (free from the above)

- **Undeath god created: Betibizi** (Basque *betiko* "eternal/forever" + *bizi* "life" → drifted). Self-named Minor God of Undeath, resident in Abyss. **Canonised as a Storveldi Denbora ruling-class survivor** who ascended via the integration procedure after the Week of Crimson Rain — which simultaneously closes the *who holds the integration procedure?* thread from the migration doc (he is the original holder; fragments persist with his cult on Talan). Spiritual root of the Blackened Lands' Skeleton ancestry and ambient necromancy.
- **The integration-procedure thread** is now anchored — see updates in `world-notes.md` *The Mortal Ascent Ladder* and *The Storveldi Denbora — The Real History*.

### Files touched
- `lore/world-notes.md` (per-god sheet, Mortal Ascent Ladder, Storveldi Denbora section, Layer 3 description, Other Pantheons, new *Named Non-Bound Gods* and *Domains Outside the Thirteen* sections)
- `lore/geography.md` (Lost Kingdom)
- `lore/glossary.md` (four new coined names, new *Named Non-Bound Gods* subsection)
- `lore/bestiary.md` (Skeleton, Muiral, Sin Devils table, Cross-References)
- `lore/unplaced.md` (Balaena, Conductor's Station, Grav Trains / Train Pirates / Ultra-High-Tech Civilisation)
