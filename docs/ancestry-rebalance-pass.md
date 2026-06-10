# Ancestry Rebalance — Geography Culture Pass (working tracker)

**Temporary working file.** Tracks the multi-region culture-write that follows the ancestry
rebalance committed in [`6049ee9`](https://github.com/Kemenor/Tyrnarra) (`lore/ancestries.md`).
Delete this file when the pass is complete and the last region is published.

**Method:** region by region. For each region we (1) grill every ancestry it carries
(`grill-me`, one axis at a time, ancestry-is-not-culture), capturing decisions here, then
(2) write the culture into `lore/geography/<region>.md`, surface, commit; HTML + site-inventory
come after the lore reads right. New/moved peoples need a full living-culture write + a ruling
sub-region; existing peoples get a review-and-deepen pass.

**Resume after a context reset:** read this file top-to-bottom, find the first region whose
status is not ✅, and continue from its grill/decision log. The locked board below is canon
(already in `lore/ancestries.md`); do not re-litigate it.

**Status legend:** ⬜ pending · 🔵 grilling (decisions being captured) · 📝 lore written (surfaced) · ✅ lore committed · 🌐 HTML published

---

## HTML reconciliation (started before the remaining lore regions, at user direction)

- **Batch 1 — `ancestries.html` REBUILT 🌐** (ancestry-first): alphabetical feeling-led prose roster → rebalanced Who-Lives-Where table (full-expression sub-regions) → Heritages (content unchanged, pass pending) → Sortalde last. Old domain-card grid and Without-a-Homeland scatter-list removed. site-inventory description updated.
- **Batch 2 — domain pages** ⬜: Peoples/feelings onto egulon/brauogi/zuzental/vindul/lautara pages; roster-line corrections on floteyn (−Leshy), sumendar (+Goblin), lioaru (+Nagaji), ezkudon (+Ratfolk), ehizahar (Kholo→Goloma), nashavel (+Anadi). Check GM-Vetted badges per page; strip where more than minor.
- **Batch 3 — sub-region pages** ⬜: `itsasalda.html` REAL REWORK (Vishkanya watch); touch-ups: `atarialda.html` (contrast line), `merkavar.html` (clergy/artisan switch), Dreaming Cape page (broker→truth-guides), `rika-tikur.html` (Gaps line).

---

## Locked board (already in `lore/ancestries.md` — reference only)

| Domain · God | Heartland ancestries | New/Moved this pass |
|---|---|---|
| Light · Egulon · Iro | Shoony · **Leshy** · **Sprite** | Leshy (from Water), Sprite (promoted); Shoony reframed |
| Darkness · Myrkono · Araphel | Fetchling · Centaur · Surki | — |
| Fire · Sumendar · Komo | Dragons · Dwarf · Kobold | — |
| Water · Floteyn · Shuun | Tripkee · Athamaru · Merfolk | lost Leshy |
| Earth · Brauogi · Sarrum | Goblin · Minotaur · **Dragonet** | Dragonet homed; Hobgoblin left; kingdom → **Goblin Kingdom** |
| Wind · Vindul · Fisaya 🔒 | Kashrishi · Tengu · Strix · Jotunborn | locked |
| Time · Lioaru · Tani | Ghoran · Azarketi · **Nagaji** | Nagaji homed |
| Law · Zuzental · Forseti | Elf · Human · **Hobgoblin** | Hobgoblin from Earth |
| Hunt · Ehizahar · Hinka | Orc · Kholo · Lizardfolk · **Goloma** | Goloma promoted |
| Commerce · Lautara · Jianna 🔒 | Kitsune · Halfling · Vishkanya | locked |
| Knowledge · Ezkudon · Enki | Shisk · Catfolk · **Ratfolk** | Ratfolk homed |
| Chaos · Nashavel · Vesuna | Gnome · Vanara · Conrasu · **Anadi** | Anadi promoted |
| Freedom · Askamira · Cronus | *all equally* | — |

---

## Region queue (in working order)

1. **Egulon (Light)** 📝 — committed (`6f4deec`), then **restructured to feeling/culture split** (surfaced, awaiting re-review): feelings → peoples block, cultures → sub-region bullets (3↔3 mapping).
2. **Brauogi (Earth)** ✅ — lore committed; HTML pending. Earth = Minotaur/Kholo/Dragonet (Stone/Vigil/Metal). Cascade done: Goblin→Fire, Kholo→Earth, Hunt trio now Orc/Lizardfolk/Goloma.
3. **Zuzental (Law)** ✅ — lore committed; HTML pending. Feeling-level Peoples block (Elf long view / Human short fire / Hobgoblin given word); Order of Law = Hobgoblin-dominant.
4. **Lioaru (Time)** ⬜ — Nagaji rebirth-cult
5. **Ezkudon (Knowledge)** ⬜ — Ratfolk diggers
6. **Ehizahar (Hunt)** ⬜ — Goloma watch-hunters
7. **Nashavel (Chaos)** ⬜ — Anadi web-holds
8. **Sumendar (Fire)** ⬜ — Goblin homed (the appetite-alchemist; concept parked in Brauogi log for deep-dive)
9. **Lautara (Commerce)** ✅ — feelings committed (`79b866b`) + **one-region-per-people rework committed** (`b9ea197`); HTML pending (itsasalda.html = real rework):
   - **Full-expression board:** Emarrea = Kitsune · Atarialda = Halfling · **Itsasalda = Vishkanya** (the steady watch IS the shaping hand; Watchers mostly Vishkanya, Reckoners the same people's scrivener arm; Watchroll "Vishkanya by gravity"). **Mountain-Halfling concept retired**; the HRA-vs-Vordsbench friction is now the two feelings meeting at one harbour ("the rails carry the deal, the dock holds the deal" = road in the blood vs the hand that stays).
   - **Azkataria + Dreaming Cape stay unsorted by people** (the floor and the faith define them); **Merkavar belongs to everyone**.
   - **Merkavar switch:** Vishkanya emphasis moved OUT of clergy (now plainly every-ancestry-at-every-rank) INTO the **fine-artisan guilds** — the parked maker-tradition LANDED (instruments, seal-craft, fine inks/glass, heirloom-grade work).
   - **Cape kitsune replaced:** the Merkavar-info-broker copy is gone; Cape kitsune are **keepers of the waking-record**, foxfire + Occult witness-craft, truth-guides if they choose to be ("did you go down that road if nobody was there to witness it"). Night-side clergy / day-side kitsune ledger, polite mutual impertinence.
   - Aligned: ancestries.md (Halfling/Vishkanya/Kitsune), glossary.md (Itsasalda entry, Atarialda entry, Watchroll gravity line), open-threads (itsasalda.html rework bullet).
   - **HTML divergence (for the HTML pass):** `itsasalda.html` = real rework (mountain-Halfling framing throughout); `atarialda.html` + `merkavar.html` + Cape page = touch-ups (contrast lines, clergy/artisan switch, broker→truth-guides); `ancestries.html` = mirror. **Also stale (docs, not canon):** `docs/site-inventory.md` line ~110 and the skill docs (`sub-region-workflow`, `grill-me`) cite the mountain-Halflings as the exemplar pair — update exemplar wording to the Vishkanya-watch/hearth-Halfling pair when convenient.
   **PARKED — Vishkanya maker-tradition** *(sub-region flow)*: canon gives two values but the regions spent "keeping community" four times (Reckoners, Merkavar admin, Cape ledgers) and "creative pursuit" once (form-masters); the "artisan-merchant guilds / refined corners of the market" line never landed anywhere. Give the maker-half a home: refined precision-craft (seal-craft, instruments, fine inks/glass, heirloom-grade objects), natural anchor Merkavar's refined market corners. Distinct from Goblin-alchemists: Goblins transform matter to consume it, Vishkanya shape it to last.
10. **Vindul (Wind)** ✅ — audited + feelings layer committed. Quartet: Tengu *answer* the wind / Strix *ride* it / Kashrishi *watch* it / Jotunborn *stand in* it. Sub-regions needed NO changes (4↔4 mapping + cultures-with-places already correct). Strix/Kashrishi lookup entries de-institutionalized; stale "Nagaji of Egulon" cross-ref removed.
11. *(unchanged regions — grill-and-deepen only, lowest priority):* Myrkono, Floteyn, Askamira

*(Ehizahar (#6) also loses Kholo to Earth — handle the Villtur re-grill there.)*

**Future phase — Heritages.** After the ancestry regions, grill the versatile heritages: divine-blood (Aphorite, Beastkin, Changeling, Duskwalker, Ganzi, Nephilim), elemental (Ifrit, Oread, Sylph, Undine, Suli), Life-Layer (Ardande, Talos), mortal-mixes (Aiuvarin, Dromaar), and other lineages (Dhampir, Dragonblood, Hungerseed, Reflection). Reconcile each to the rebalanced ancestry homes. The **Soul Tree → Duskwalker** connection slots in here.

---

## § Egulon (Light · Iro) — 🔵 grilling

**Canon (from `egulon.md`):** sun/warmth/golden, the most settled & prosperous domain, now
**Talan's wine country** (south-facing vineyard slopes). Terrain: open flat, scattered ranges,
a distinctive **circular mountain-ring with forest to the east**, a large forested SE-coast island.
God's city **Ljosarn, the Everbright City**. Sub-regions: Harro Distiratsue (Proud Radiance),
Lua Lasai (border w/ Ezkudon), Argia Esfera (sphere of light).

**The three peoples (target):**
- **Shoony** — loyal/devoted; the devotional heart of Iro's church (was second to Nagaji; now the anchor).
- **Leshy** *(new, from Water)* — grove/vineyard spirits; the green life the sun grows.
- **Sprite** *(new, promoted)* — Material-plane bright-fey courts; light as glamour; fey-origin uneasy under Iro's zeal.

**Reconception:** Light shifts from "two fervent faith-peoples" to *sunlit life* — devotion, growth, glamour.

### Grill log (decisions)
- **Seed = the year of the vine.** Wine country is the domain's spine: grow it (Leshy), revel in it (Sprite), bless it (Shoony); Iro's church is the calendar that times all three. Wine = sunlight made material, Light you can drink/offer.
- **Inclination, not definition.** The three peoples *lean into* the wine-year by temperament; they are NOT reduced to civic functions ("sprites make wine"). Each is a full ancestry with culture beyond the vine. Hold **ancestry ≠ culture** on every question: push for what being *from Egulon* adds to the people, not the job it assigns them.
- **Sub-region ↔ people mapping (each gets a ruling heartland):** Lua Lasai (calm border-march toward Ezkudon) = **Leshy**; Harro Distiratsue ("Proud Radiance") = **Sprite**; Argia Esfera ("Sphere of Light") = **Shoony**. Concentrated/leading there, not exclusive to it.
- **Leshy culture = rooted keepers of place-memory** in the longest-cultivated land on Talan (opposite of the wild/wandering water-Leshy). Lineages stay with the same grove/vine-stock for generations. Tentative gesture: a planting isn't truly done until the local Leshy has taken to the new stock / names it. *(confirmed: "reads nicely")*
- **Leshy are a FULL ancestry in this setting** — born, have children, hold lineages; drop the PF2e "created through ritual" framing. ✅ fixed in `ancestries.md` (Leshy entry).
- **Sprite culture = proud settled light-artisans.** Material-native, generational (not flighty fey). Turned fey-glamour into a civic light-craft they take pride in: the radiance Egulon is known for (festival/press-night illumination, lantern & living-light work, the staged brilliance of Ljosarn high rites). "Proud Radiance" = pride in the making.
- **Sprite/Shoony seam = the domain's live tension.** Glamour vs zeal, made-light vs true-light. Real friction of temperament, generative not hostile: Sprites celebrated in their own Harro Distiratsue, side-eyed as "chaos in the Light's colours" out in devout Argia Esfera (Shoony country).
- **Shoony culture = the light of Iro across the domain.** Loyal as dogs; *varied in being* — "not one but many," many dog-forms, almost all sharing Iro's faith. Three faces of devotion: **warm welcome** (hospitality), **bright zeal** (the fervour — Shoony now carry the old Nagaji zeal-role), **healers of Hope** (healing, hope-bringing). Heartland **Argia Esfera**, devotional core = a **great kept flame / radiant orb** (literal, name TBD).
- **Ljosarn (god-city) deferred** — combine all three peoples when built. Placement: in **Harro Distiratsue, on the lake bordering Argia Esfera** → sits right on the Sprite/Shoony seam, the natural meeting-ground of all three.
- **Leshy = the domain's ballast.** They decline the Sprite/Shoony quarrel (a single-lifetime squabble; a Leshy line has watched ten lifetimes). Both hot peoples defer to them on anything touching the soil: no Sprite festival-claim on an unblessed grove, no Shoony first-pressing consecration the Leshy didn't see ripen. The hot two argue; the cool one holds the weight.

### Draft — committed (`6f4deec`), then RESTRUCTURED per the feeling-vs-culture rule (📝 surfaced, awaiting re-review)
**The structure (the model for remaining regions):** ancestries get **feeling**, sub-regions get **culture**;
Egulon's 3 peoples ↔ 3 sub-regions map one-to-one, but the layers stay differentiated (same feeling, different
culture by place: a Harro Leshy works the light-craft register, a Lua Lasai Leshy the husbandry-courtesy).
- **Peoples (feeling):** Leshy = *the ones who stay* (root, tend, remember); Sprite = *the ones who shine* (pride of making, brightness as self-expression); Shoony = *the ones who keep faith* (loyalty/constancy one temperament; welcome, zeal, healer's hope).
- **Sub-region cultures:** Harro Distiratsue = **the light-craft** (standing by brightness made; made-light holy; craft belongs to the place, all peoples work it); Lua Lasai = **husbandry-courtesy** (planting finished when the grove's Leshy takes to the vine and names it; kept by every people farming there); Argia Esfera = **the kept flame** (unbroken-shift vigil as central institution; devout country; "a Sprite learns to dim, or to dazzle very carefully").
- Two-lights tension + Leshy ballast kept at temperament level; the rite-list ("cannot claim a grove / consecrate a pressing") generalized to deference, "the courtesies that deference takes are each region's own."
- `ancestries.md` Shoony entry aligned (three faces as feeling; liturgy-keeping line dropped).
- **Open within Egulon (for later):** name the great kept flame/orb; Ljosarn god-city build; wine-country economics; domain governance.

---

## § Brauogi (Earth · Sarrum) — 🔵 grilling

**Canon (from `brauogi.md`):** Earth domain, **Sarrum-the-Steadfast**; the continent's **breadbasket**;
ancestry politics deliberately **cooperative** (trade > feud, "the rivers were always worth more to
share than to fight over"); the steady counterweight to flashier neighbours. Old noble houses run river
trade + granaries. Sub-regions: Gotorlekua (the Stronghold, holds god-city **Lurrath**), the Earth Realm
(breadbasket plains), **Hirubaso** (sacred druid grove; only routine Primotech site; the grown heart-stone),
Baratalda (orchard frontier-trade with Ehizahar's hunters), Azkamour (Vindul border march), Twin Suns (+
**Soul Tree** island, natural soul-passage, Voroir Daua's oldest charter). Iturmen spine + Iturburu source-lake
= unclaimed druid-tended heart.

**Changes this pass:** **Dragonet** homed (deep wyrm-memory in the old substrate); **Hobgoblin** left for Law.
NOTE: no goblinoid-kingdom sub-region exists in `brauogi.md` — the rename is just updating the *Peoples* +
*Cultural character* lines to **Goblin / Minotaur / Dragonet**.

**The three peoples (FINAL after reshuffle):** **Minotaur · Dragonet · Kholo** (Goblin left for Fire).

### Grill log (decisions)
- **Sarrum's ACTUAL portfolio (corrected — "tradition"/"soil-bread" was my invention, not canon):** subtitle **Stone · Harvest · Endurance · Burden**; domains **Earth · Confidence · Duty · Vigil · Metal**. Map the three peoples onto these; Harvest + Confidence read as domain-wide threads.
- **Minotaur = Stone · Endurance · Burden (+ Earth/Confidence).** Sarrum's image; stone-cutters and burden-bearers, the enduring immovable backbone; grain-farmers and wall-builders.
- **Kholo = Vigil · Duty (+ pasture-Harvest).** Matriarchal, bone-token herder-clans of Brauogi: night-vigil over the flock, duty to clan-line; meat/milk/leather to Minotaur bread/stone. **PROSE RULE: Kholo always were Earth herders — NO Villtur/hunter past, NO migration language** (the Hunt→Earth move is meta-only bookkeeping). Same trap as the Shoony "gone south" line; applies to the lookup entry and the later Hunt re-grill too.
- **Dragonet = Metal + the deep Earth (CONFIRMED; reframed off "tradition").** Deep-substrate people of ore and mineral: miners, metal-wrights, keepers of the deep where stone turns to metal. Wyrm-lineage + ancient memory = texture, not headline. Pulled UP into a living craft. **Primotech / heart-stone hook deferred** to the sub-region flow.
- **Soul Tree (sub-region) = Duskwalker-coded.** The natural soul-passage island + Voroir Daua's oldest charter make it a Duskwalker-generating site (psychopomp-touched, like the Blackened Lands). Note for the Brauogi write / heritages pass.
- **Sub-region detail deferred** — Primotech/Hirubaso and the 7 sub-regions are too many for now; handle in the later sub-region flow.
- **CASCADE — Goblin out, Kholo in.** Goblins fit steadfast-Earth poorly (Chaos-coded). Resolution:
  - **Goblin: Earth → Fire (Sumendar).** Goblin = **fire-as-alchemy, driven by appetite** (vs Kobold = fire-as-invention/machine). "Can I consume it?" is the first question about anything; bite → cook → distil → combine → transmute until consumable. Classical lead→gold bores them (gold isn't edible). Craft: brews, ferments, tinctures, medicines, poisons, intoxicants, acids, alchemical fire, the volatile *charge*. Bomb-split: **Goblin mixes the charge, Kobold builds the shell/firing mechanism** (Goblin paste in Kobold cannon; they collaborate). Concrete: an elder Goblin alchemist is a walking catalogue of survived experiments (iron-gutted, scarred, fingers short, half-deaf), prized possession = the *tongue-ledger* of everything tasted and what it did. **PARKED for the Fire/Sumendar deep-dive — log only, full culture-write later.**
  - **Kholo: Hunt → Earth (Brauogi).** Kholo = the **matriarchal herder-clans**, the *livestock* half of the breadbasket (canon already lists "grain, livestock"): drovers of the pasture-margins, meat/leather/milk to the Minotaurs' bread/walls. Bone-token clan-tradition → "Earth = tradition." Good agrarian fit.
- **Balance:** Fire → 4 (Dragons/Dwarf/Kobold/**Goblin**); Earth → 3 (Minotaur/Dragonet/**Kholo**); Hunt → 3 (Orc/Lizardfolk/Goloma). Three 4s now Fire/Chaos/Wind (was Hunt/Chaos/Wind) — lateral, no net imbalance.

### Feeling-vs-culture audit (post-Zuzental rule) — ✅ fixed
- Kholo: dropped "bone-token-marked" + the winter-standing reckoning custom (both were domain-universal practices); kept **matriarchal as disposition**. **PARKED for sub-region work:** bone-token marks, clan-standing-by-winter-herd reckoning — Kholo clan-culture colour for wherever the clans concentrate.
- Dragonet: "venerates the deep as Zaharsuge's own" softened to "most Dragonets feel a natural affinity toward Zaharsuge, whom their tradition holds as progenitor." Affinity IS ancestry-level here (his children, kind of — they believed him into shape).
- Minotaur occupations ruled acceptable: occupations-at-domain-level = the economy (grain/herd/ore), not a practice.

**FUTURE TASK — Zaharsuge rework.** The Zaharsuge canon (`gods.md`, Named Non-Bound Gods) likely still
carries the old homeless-Dragonet framing (upper-Darklands concentrations etc.). Rework for: Dragonets as
Brauogi Earth-people; the "his children, kind of — they believed him into shape" relationship (check what is
public Dragonet tradition vs ⚿ GM-tier; the Wyrmkin Real History secret in `timeline.md` already complicates
the progenitor claim). Do alongside or after the heritages pass.

### Draft — 📝 written to `brauogi.md` (## The Three Faces of Sarrum's Earth) + cascade done in `ancestries.md`; committed.

### `ancestries.md` cascade edits — ✅ DONE

---

## § Zuzental (Law · Forseti) — 🔵 grilling

**Canon (from `zuzental.md`):** Forseti = **Order · Justice · Oath · Tyranny**; she does NOT prescribe law —
mortals write their own laws, her clergy are judges/oath-witnesses/contract-arbiters. Sub-regions: **Emerald
Isles** (island kingdom + Bridgelands/Sortalde embassies), **Thousand Kingdom** (dominant; Lograth = god-city +
capital; refounded 2457 MR by Aelis Fyrstgilt; GM-tier: forged lineage, Garaion lives as Aldwin Mero in
Quietbarrow), **Legea Empire** (Layer-3 theocracy, Legaun, Divine Faith), **Namur Republic** (democratic
city-state network), **Order of Law** (institutional sub-region, central to Forseti's framework), **Crossroads**
(neutral tri-domain trade nexus; Spider's Silk Inn / Matron Charna).

**The three peoples (target):**
- **Elf** — long-planning ruling bloodline (Thousand Kingdom); generational politics.
- **Human** — short-planning ruling bloodline; fast political cycles; the volatility-and-longevity engine.
- **Hobgoblin** *(new)* — disciplined, hierarchical, oath-bound; Forseti's soldiery (marshals, border-wardens, regiments that hold a judgment). NO migration framing — always been Zuzental's.

**Forseti corrected:** subtitle **Order · Justice · Oath · Tyranny**; domains **Truth · Secrecy · Star · Glyph**.

**GENERAL RULE (user):** not every ancestry needs to map cleanly onto its god's portfolio/facets. Drop the facet-assignment reflex; a people's culture stands on its own.

**STANDING RULE (user, 3rd correction — apply to ALL remaining regions):** the ancestry layer sets a
**feeling of a people** (temperament, disposition, what they're like to meet), NEVER specific cultural
practices. Practices (naming schemes, rites, institutions, dress) belong to **sub-region cultures**: a
sub-region may have a dominant ancestry, but a Hobgoblin in the Thousand Kingdom, Namur Republic, Legea
Empire, Order of Law, and Emerald Isles lives five different cultures. Domain-level peoples-prose must stay
at the feeling level; cultural specifics get written per sub-region (later, in the sub-region flow).
Example of the trap: the oath-honorific naming idea = a cultural practice → parked as possible
Thousand-Kingdom/Order-of-Law colour for sub-region work, NOT an ancestry trait.

### Grill log (decisions)
- **Hobgoblin = the people of the kept oath.** Structural gap they fill: Forseti's clergy judge/witness but a judgment is just words; someone must HOLD it (escort verdicts, enforce contract terms, garrison disputed boundaries). Elves plan, Humans politick, Hobgoblins keep what was sworn. The sworn word is their load-bearing social unit.
- **Heartland = the Order of Law** (institutional sub-region, previously people-less): marshals' colleges, warden-garrisons, verdict-escort companies. Disproportionately Hobgoblin, NOT "the Hobgoblin state" (Elves/Humans serve too; most Hobgoblins are ordinary folk whose oath-culture shows in daily life). No migration framing — always been Zuzental's.
- **Feeling-level definitions locked (user confirmed):** **Hobgoblin** = the given word as load-bearing; slow to promise, immovable once sworn; shadow = the grip that doesn't let go (Tyranny-texture, written as the people's own acknowledged shadow). **Elf** = the long view; patience outlasting dynasties; trust accrued in decades. **Human** = the short fire; risk and renewal; the churn. Elf/Human volatility+longevity interplay stays as *Thousand Kingdom politics*, not ancestry.
- **Order of Law: Hobgoblin = dominant ancestry there** (user). The institutional sub-region reads Hobgoblin-coded; note in the sub-region bullet. Still a place they're *many*, not what they *are*.
- **Oath-honorific naming idea PARKED** for Thousand-Kingdom/Order-of-Law sub-region work (cultural practice, not ancestry trait).

### Draft (culture prose) — not started
- Table rows: **Earth** → Minotaur · Dragonet · Kholo; **Fire** → +Goblin; **Hunt** → Orc · Lizardfolk · Goloma.
- **Goblin** entry → Fire/Sumendar alchemist (brief; full culture later). **Kholo** entry → Brauogi/Earth herder.
- **Minotaur** entry: "alongside the Goblins" → "alongside the Kholo". **Dragonet** entry: re-frame to tradition/memory-keepers pulled up (not buried under-dark).
- **Orc / Lizardfolk / Goloma** entries: drop "alongside Kholo"; Hunt trio is now Orc/Lizardfolk/Goloma (Goloma was "wary fourth" → now "wary third/watcher"). *(Deeper Villtur re-grill happens at the Ehizahar region.)*

### Draft — 📝 written to `zuzental.md` (Peoples block + Order of Law bullet) + `ancestries.md` Hobgoblin entry rewritten to feeling-level; committed.

---

*(Further region sections added as we reach them.)*
