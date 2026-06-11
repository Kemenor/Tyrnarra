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

**METHOD DOC:** the distilled how-to-define-ancestries rules live in [`ancestry-conventions.md`](ancestry-conventions.md) (permanent; survives this tracker). Read it before any feeling-work.

**STATE SNAPSHOT (2026-06-11, end of session):** the thirteen-domain feelings sweep is **COMPLETE**, the
conventions review-pass is **COMPLETE** (Brauogi/Shoony/Sprite reworked), the made-and-cursed peoples and
Awakened Animal are **judged**, and the **HTML is fully reconciled** (ancestries.html, all domain pages,
eldara, nahaskel, itsasalda + Lautara sub-regions, registrar; grep-verified clean of Eizhalun/Seal-folk/
migration text). Every people on Talan now carries a conventions-judged feeling; Sortalde six stay
pointer-entries by design. **NEXT PHASE: the heritages pass.** After it: Fenurra rework (per-tribe ancestry
grill) + Zaharsuge rework (paired), god-cities reconciliation (10 remaining; Thekkavar/Nahaskel/Eldara done),
seeded sub-regions (Hareaveldi + parked colour), pf2e rarity-pill mechanics note.

---

## HTML reconciliation (started before the remaining lore regions, at user direction)

- **Batch 1 — `ancestries.html` REBUILT 🌐** (ancestry-first): alphabetical feeling-led prose roster → rebalanced Who-Lives-Where table (full-expression sub-regions) → Heritages (content unchanged, pass pending) → Sortalde last. Old domain-card grid and Without-a-Homeland scatter-list removed. site-inventory description updated.
- **Batch 2 — domain pages 🌐 DONE**: Egulon (Year of the Vine section + peopled sub-region cards + wine-country terrain + Ljosarn placement), Brauogi (Three Faces section + trio swap + Soul Tree Duskwalker note), Zuzental (Three Tempers of the Law section + Order of Law Hobgoblin-dominant), Vindul (Four Ways of Meeting the Same Sky section; **GM-Vetted badge stripped** — more-than-minor canon addition), Lautara (Three Tempers of the Road section + full-expression Peoples line + Itsasalda card de-mountain-Halflinged + Atarialda card fixed). Peoples facts-lines added to floteyn/sumendar/lioaru/ezkudon/ehizahar/nashavel (these six previously had NO roster). Ancestries-page links added to the five culture-pages' Continue Reading.
- **FEELINGS BUNDLE 🌐 DONE (3 commits, 2026-06-11)**: (1/3) `ancestries.html` — every entry mirrored to its committed feeling, Eizhalun + migration + Seal-folk + Fenurran-human-stock removed, Dragonblood row re-anchored, Darkness row anchored. (2/3) nine domain pages — Peoples lines mirrored (lioaru/ezkudon/nashavel/ehizahar/sumendar/floteyn/brauogi updated; egulon/myrkono added); myrkono Steppe Watch fully de-Eizhalunned. (3/3) `eldara.html` three-handed (Goblin card + argument + flavor + Peoples), `nahaskel.html` web-walks (Peoples + conveyances), `pf2e-registrar.html` 12 placement rows updated (rarity pills untouched — mechanics decision for a pf2e-notes pass; note: Sprite/Anadi/Goloma/Ratfolk/Dragonet pills may want review now that they hold heartlands). Published HTML grep-verified CLEAN of Eizhalun/Seal-folk. **The site now matches the canon for the whole rebalance.**
- **Batch 3 — sub-region pages 🌐 DONE**: `itsasalda.html` reworked (Peoples/pills/prose to the Vishkanya watch; tilt-cards → the Watch & the Rail; Watchroll gravity inverted; Reckoners re-banded; Hringseyja "Halfling Side" → "Itsasaldan Side"; see-also fixed). Touch-ups: `atarialda.html` (fullest-expression framing, HRA as contrast partner), `merkavar.html` (clergy every-ancestry; Vishkanya → fine-artisan guilds), `dreaming-cape.html` (broker → waking-record truth-guides, facts + peoples + faith-stack), `rika-tikur.html` (Gaps re-anchored on the people the register cannot see; Ratfolk card → "The Gaps' Own"), `pf2e-registrar.html` (stale Halfling row). No GM-Vetted badges on any Batch-3 page. NOTE: "Merkavar-kitsune" survives on merkavar/emarrea pages legitimately (Merkavar's own tradition).

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
4. **Lioaru (Time)** ✅ — lore committed (`7db5441`). The tense-trio (hold/answer/become); Nagaji de-zealed; Hareaveldi seed placed. **HTML mirror PENDING (bundle):** lioaru.html Peoples line + ancestries.html Ghoran/Azarketi/Nagaji entries.
5. **Ezkudon (Knowledge)** ✅ — lore committed (`6d96ef9`). Enki's three faces one-per-people (Catfolk Wisdom / Shisk Mystery / Ratfolk Discovery; Arrogance unclaimed); Thekkavar three-faces restructure. HTML in the bundle.
6. **Ehizahar (Hunt)** ✅ — lore committed. Three phases of one hunt (Orc close / Lizardfolk never stop coming / Goloma see it first, the hunt from the prey's side); Hinka = Predation·Survival·Patience·Cruelty, with **Cruelty the face nature itself claims** (cruelty of survival, not machination; no hunter needs to be cruel for the hunt to have cruelty in it); the roaming-vs-rooted tension (settling clans at fords and railheads; "scouts in new country or prey that built its own pen"). HTML in the bundle (ehizahar.html Peoples line). **METHOD (user, all remaining regions): surface proposed file-prose in chat FIRST; on yes, write files + commit in one motion.**

**QUEUED — Fenurra rework (major).** The Fenurran tribes are reflavored: mostly-human is GONE; the four tribes are united by the **Dragonblood versatile heritage** with a **differing major ancestry per tribe** (per-tribe roster = its own grill). **Dragonblood unlinked from the alien Dragons**, re-anchored to the Wyrmkin line (Zaharsuge), same base stock as the Dragonet. Done this pass: ancestries.md (Fenurran stub rewritten, Dragonblood heritage row re-anchored, cross-ref line), ehizahar.md (Fenurra bullet sentence). Still to do: the per-tribe ancestry grill; `fenurra.md` (27 KB) de-humanizing rework; `fenurra.html`; ancestries.html Human entry (drop the Fenurran human-stock sentence) + Dragonblood row + heritage mentions on dragons-reach page. Pairs with the parked **Zaharsuge rework** (both hang off the Wyrmkin line).
7. **Nashavel (Chaos)** ✅ — lore committed (`98d36be`). Four stances toward change (Gnome spin / Vanara ride / Anadi re-weave / Conrasu know-what's-underneath); Nahaskel web-walks. HTML in the bundle.
8. **Sumendar (Fire)** ✅ — lore committed. Feelings (individually shaped, NOT god-aspect templated; user pushed back twice): **Dwarf = methodical** (ten thousand corrected errors), **Kobold = the leap** (reads wreckage like a schematic), **Goblin = appetite** (the world is a meal half-cooked), **Dragons = the remembering** (the long ember). Eldara now three-handed (Dwarf schematic / Kobold prototypes / Goblin distils the residue; still-rooms paragraph; Dragons work the fires too). **Kobold + Goblin heartland regions deliberately UNASSIGNED — settled at the Sumendar build-out** (undefined regions available then: Haraour Eliza, Red Dominion, Tahu Tangata, Burdineyja). HTML in the bundle: sumendar.html Peoples line (re-mirror), eldara.html three-handed edits, ancestries.html Dwarf/Kobold/Goblin/Dragons entries.
9. **Lautara (Commerce)** ✅ — feelings committed (`79b866b`) + **one-region-per-people rework committed** (`b9ea197`); HTML pending (itsasalda.html = real rework):
   - **Full-expression board:** Emarrea = Kitsune · Atarialda = Halfling · **Itsasalda = Vishkanya** (the steady watch IS the shaping hand; Watchers mostly Vishkanya, Reckoners the same people's scrivener arm; Watchroll "Vishkanya by gravity"). **Mountain-Halfling concept retired**; the HRA-vs-Vordsbench friction is now the two feelings meeting at one harbour ("the rails carry the deal, the dock holds the deal" = road in the blood vs the hand that stays).
   - **Azkataria + Dreaming Cape stay unsorted by people** (the floor and the faith define them); **Merkavar belongs to everyone**.
   - **Merkavar switch:** Vishkanya emphasis moved OUT of clergy (now plainly every-ancestry-at-every-rank) INTO the **fine-artisan guilds** — the parked maker-tradition LANDED (instruments, seal-craft, fine inks/glass, heirloom-grade work).
   - **Cape kitsune replaced:** the Merkavar-info-broker copy is gone; Cape kitsune are **keepers of the waking-record**, foxfire + Occult witness-craft, truth-guides if they choose to be ("did you go down that road if nobody was there to witness it"). Night-side clergy / day-side kitsune ledger, polite mutual impertinence.
   - Aligned: ancestries.md (Halfling/Vishkanya/Kitsune), glossary.md (Itsasalda entry, Atarialda entry, Watchroll gravity line), open-threads (itsasalda.html rework bullet).
   - **HTML divergence (for the HTML pass):** `itsasalda.html` = real rework (mountain-Halfling framing throughout); `atarialda.html` + `merkavar.html` + Cape page = touch-ups (contrast lines, clergy/artisan switch, broker→truth-guides); `ancestries.html` = mirror. **Also stale (docs, not canon):** `docs/site-inventory.md` line ~110 and the skill docs (`sub-region-workflow`, `grill-me`) cite the mountain-Halflings as the exemplar pair — update exemplar wording to the Vishkanya-watch/hearth-Halfling pair when convenient.
   **PARKED — Vishkanya maker-tradition** *(sub-region flow)*: canon gives two values but the regions spent "keeping community" four times (Reckoners, Merkavar admin, Cape ledgers) and "creative pursuit" once (form-masters); the "artisan-merchant guilds / refined corners of the market" line never landed anywhere. Give the maker-half a home: refined precision-craft (seal-craft, instruments, fine inks/glass, heirloom-grade objects), natural anchor Merkavar's refined market corners. Distinct from Goblin-alchemists: Goblins transform matter to consume it, Vishkanya shape it to last.
10. **Vindul (Wind)** ✅ — audited + feelings layer committed. Quartet: Tengu *answer* the wind / Strix *ride* it / Kashrishi *watch* it / Jotunborn *stand in* it. Sub-regions needed NO changes (4↔4 mapping + cultures-with-places already correct). Strix/Kashrishi lookup entries de-institutionalized; stale "Nagaji of Egulon" cross-ref removed.
11. **Myrkono (Darkness)** ✅ — lore committed (two passes). Three answers to the same dark (Araphel's faces deliberately unmapped): **Fetchling = the self is made, not given** (the unasked question as its courtesy; the old name as the deepest gift), **Centaur = they run it out** (emotion lived through the body at full speed and FINISHED: rage galloped down, grief ridden to the horizon; the new face arrives by fully living through the old one — the only emotional-process feeling in the canon; user-verified unique vs Nagaji shed/Sprite shine/Orc charge), **Surki = not their shell, and never alone** (ten thousand wills choosing the same thing vs the hive's one will; the *we* woven, never granted — hospitality immediate, membership earned, never dropped). **Centaur migration ERASED and the name Eizhalun REMOVED ENTIRELY** (user: no other ancestry got a second name; glossary entry deleted; all references now "Centaur"/"the centaur clans"; fully Myrkono-native, no night-hunt framing anywhere). Anchors: Fetchling/Ilun Tasun, Centaur/Shadow Steppes, Surki/Itzasoa; **Myrria belongs to no one people**. HTML in the bundle: myrkono.html Peoples block + ancestries.html Centaur entry (migration text AND Eizhalun name!)/Fetchling/Surki entries. **Eizhalun survives in exactly three published files** (grep-verified): `ancestries.html`, `myrkono.html`, `pf2e-registrar.html` — all three on the bundle.
12. **Floteyn (Water)** ✅ — lore committed. **THE THIRTEEN-DOMAIN SWEEP IS COMPLETE** (Askamira all-equally by design; nothing needed). Three answers to water that will not hold still (Shuun = Rivers · Seas · Adaptability · Drowning; domains Water · Introspection · Repose, inspiration only): **Tripkee = home is made, not found** (three planks and a tide, a porch by evening; settledness as craft), **Athamaru = at ease above the abyss** (FISH-folk — the seal-folk label was wrong; equanimity, dread gets no purchase, panic is a land-emotion; user picked this over play-in-earnest and school-turn options; no cross-people contrast lines per the new rule-9 addendum), **Merfolk = move as water moves** (never forcing, around/over/through, the certainty of water; the claim deepened to oneness). **Drowning = the nature-claim**: the sea's own face, belonging to no people; none of the three can drown, all three have pulled out those who can. HTML in the bundle: floteyn.html Peoples line + ancestries.html Tripkee/Athamaru (says "Seal-folk"!)/Merfolk entries. Conventions doc gains the rule-9 addendum: an ancestry describes itself, never itself-through-others.

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

## § Lioaru (Time · Tani) — 🔵 grilling

**Canon (from `lioaru.md`):** desert dominant, orange dunes; green river valley (**River Duchies**, noble
houses, downstream trade from Emarrea); **Lost Kingdom / Blackened Lands** (Tani's death-site, cursed ground,
Fleshwarp + Skeleton origin); **Lost Isle**; **Galdua Jendea** (sand-whale territory, holds **Valreka**);
**Hareaveldi** (partially independent identity, name predates Tani, "flesh out during Lioaru work" — EMPTY).
Valreka: whale-borne city, recovers Oroiri; Ghoran majority + Azarketi water-bearers; ◈ old-woman-at-the-dig;
⚿ Amona of the Strays (Tani among the youth-riders).

**The three peoples (target):**
- **Ghoran** — memory rooted; the Guardians of Time; Valreka's heart. (Culture already lives with Valreka — correct.)
- **Azarketi** — the past carried as daily labour; water-bearers; southern coast + offshore islands ancestral ground.
- **Nagaji** *(new)* — shed-and-renewed; the fervent faithful of the goddess who died and returned. Needs a heartland; NO migration framing (always were Lioaru's).

### Grill log (decisions)
- **Hareaveldi = Nagaji heartland, approved in principle** ("a good idea"): the serpent-kingdom of the desert; the empty sub-region whose pre-Tani name becomes the feature (an old desert kingdom whose people found in the returned goddess what their own skins always told them; no migration). Mapping: Galdua Jendea ↔ Ghoran, southern coast/isles ↔ Azarketi, Hareaveldi ↔ Nagaji; River Duchies + Lost Kingdom unsorted. **Details deferred until the feelings are set** (user: feelings first).
- **The tense-trio (user confirmed: "reads good"):** the three feelings stand in Tani's three tenses (her subtitle Fate · Patience · Memory · Decay as inspiration, not mapping). **Ghoran = the ones who hold what was** (past; memory as temperament; vs Elf = long view forward, vs Leshy = place-memory). **Azarketi = the ones who answer it now** (present; born carrying a story bigger than their life, defined by today's answer — pride daily, penance daily; unifies the Elden-blood-pride majority and Valreka's penance community as two answers to one inheritance). **Nagaji = the ones who become what's next** (future; shed-and-whole-again; selves laid down finished; Tani recognised, not zealously revered).
- **Nagaji DE-ZEALED (user: zeal was an Egulon holdover).** The fervour was their old Light-domain function and the zeal-role already re-homed to Egulon's Shoony. Rewritten: the people who begin again completely; kinship with Tani instead of fervour. `ancestries.md` entry rewritten; `lioaru.html` + `ancestries.html` Nagaji lines need the same de-zeal at HTML mirror time.
- **Decay over all:** "the sand that buries is also the goddess" closes the Peoples block.
- **Hareaveldi seed placed in `lioaru.md`** (serpent-kingdom of the desert, kingdom of becoming, name older than its cult); **full region write deferred** to the sub-region flow.

### Draft — ✅ committed (`7db5441`). HTML mirror in the BUNDLE: lioaru.html Peoples line + ancestries.html Ghoran/Azarketi/Nagaji entries.

---

## § Ezkudon (Knowledge · Enki) — 🔵 grilling

**Canon (from `ezkudon.md`):** the hidden domain; ring-fortress terrain around the archives. Sub-regions:
**Jakinduria** (holds **Thekkavar**: the Lanterns, the descent, writs, Quiet Hour, Convocation; Catfolk=Wisdom
pole / Shisk=Discovery pole — city culture, correctly placed), **the Wildreach** (wild people, wild-magic,
Iratxobaso fey-forest), **the Golden Coast** (tea/paper/ink trade in, finished thought out), **Lua Lasai**
(shared w/ Egulon; Leshy-dominant per the Egulon pass). ⚿ secrets: the price in the deep (the Sealed), what
waits in the Leize.

**The three peoples (target):** Shisk · Catfolk · **Ratfolk** *(new)*. Feelings first, then Ratfolk placement.

### Grill log (decisions)
- **The three faces sort one-per-people (user: "that split is better").** Enki = Wisdom · Discovery · Mystery · Arrogance (domains Knowledge · Magic · Perfection). Old city canon split him between two peoples; with three: **Catfolk = Wisdom** (curiosity that keeps; the keeping eye; closed door = kept promise), **Shisk = MYSTERY** (relabelled off Discovery — the ones the hidden calls; the people of Mystery becoming mysteries, feeding the Sealed), **Ratfolk = Discovery** (every question has an answer; nothing truly closed; discovery as motion — GENERALIZED off the digger/physical register per user). **Arrogance unclaimed**: the shared sin threatening each from its own side.
- **Thekkavar restructured two-poles → three-faces** (user approved): Ratfolk thread = the page-runners (the city's vertical circulation) + warren-crews; the Sealed now drawn from all three peoples.
- **Ratfolk anchor = the under-ring**: warrens threading Ezkudon's central mountain-fortress, older than any writ; the people of Discovery live inside the walls the rest of the domain lives behind.
- **FUTURE PHASE (user): god-cities reconciliation pass** — go through ALL thirteen divine cities at the end, checking each against its domain's rebalanced peoples (Thekkavar handled here; the other twelve pending).

### Draft — 📝 written (ezkudon.md Peoples block + Jakinduria warrens + Thekkavar three-faces + Sealed line; ancestries.md Catfolk/Shisk/Ratfolk rewritten), surfaced, awaiting review. HTML mirror in the BUNDLE: ezkudon.html Peoples line (Shisk still says "divers of the sealed shelves" — fine — but Ratfolk line is digger-register and Shisk needs Mystery relabel) + thekkavar page if exists + ancestries.html entries.

---

## § Nashavel (Chaos · Vesuna) — 🔵 grilling

**Canon (from `nashavel.md`):** dense old-growth forest, wild magic, paths don't stay fixed. Sub-regions:
**Vernua Dominion** (holds **Nahaskel**, the Unmapped City: remake-what's-yours, the Casting/coin, Tellers,
Dossa, Pim; ⚿ the coin honest except at the two edges; the Unthrown), **Kaosadaemi Principality**, **Basogur
Jungle** (shared w/ Ehizahar; the continental rail-blocker; "indigenous Vanara/leshy/beast-spirits/druid
resistance"). Nahaskel texture already names Gnomes (the temperament), Ganzi, Conrasu (the thread of caution).

**The four peoples (target):** Gnome · Vanara · Conrasu · **Anadi** *(promoted)*. Feelings first.

### Grill log (decisions)
- **Vesuna's portfolio (user):** subtitle **Change · Creativity · Spontaneity · Madness**; domains **Change · Luck · Trickery · Disorientation**.
- **The four stances, faces as inspiration (user: "reads good"):** **Gnome = Spontaneity, the ones who spin it** (the idea arrives and the hands are already moving; they generate the churn). **Vanara = Change, the ones who ride it** (change as their native element; sure-footed on moving ground). **Anadi = Creativity, the ones who re-weave** (making as devotion; the web tears and the weaving was the point; serene about destruction). **Conrasu = Madness known from the inside** (the Hobgoblin/Tyranny move: they have BEEN formlessness; the chosen shape is sanity as a daily act). **Luck stays in the coin** — the goddess's, no people's.
- **Anadi in Nahaskel (user): the web-walks** — silken rooftop walkways re-strung weekly/overnight, walkable by all; the one transport that keeps pace with the city; "the nearest thing Nahaskel has to infrastructure," lasting because their makers never mind taking them down. Added to the conveyance paragraph + the ordinary-day peoples line.
- Anadi added to the Basogur rail-blocker resistance list + Basogur bullet (web-holds in the deep interior).

### Draft — 📝 written (nashavel.md Peoples block + Nahaskel web-walks + Basogur anchors; ancestries.md Gnome/Vanara/Conrasu/Anadi rewritten feeling-first), surfaced, awaiting review. HTML mirror in the BUNDLE: nashavel.html Peoples line + nahaskel.html (web-walks + peoples texture) + ancestries.html entries.

---

*(Further region sections added as we reach them.)*

---

## § Heritages pass — ✅ LORE COMPLETE (all 19 carries written + committed; remaining: the end-of-pass HTML bundle)

**Design locks (user-confirmed, 2026-06-11):**
1. **Carry-register, not full feelings.** A heritage entry describes the **carry** (what the blood/spark does to whatever ancestry-feeling is already there), the **reception** (how the world reads the visible trait), and **one concrete proof**. The text must hold on any ancestry (the test: a Duskwalker Goblin and a Duskwalker Elf both recognizable). The ancestry keeps deciding who the person is. Rule-9 analogue: a heritage describes itself, never the ancestries it sits on.
2. **Prose entries.** The origin tables retire; each heritage becomes a prose entry in the ancestry-roster register, existing canon folded into the opening sentence and preserved where load-bearing (Voroir Daua stance, Reflection cover story, Nephilim sub-sections).
3. **Interlocks: canon pairs only.** Aphorite/Ganzi as counterparts (asymmetric: sense vs. field); elemental four as one chord with Suli the unresolved fifth; Ardande/Talos as the plane-mirror pair; every other heritage stands alone, individually shaped.

**Portfolios (read from canon, gods.md aspects + registrar domains; nothing needed asking):**
Forseti Order·Justice·Oath·Tyranny / Truth·Secrecy·Star·Glyph · Hinka Predation·Survival·Patience·Cruelty / Death·Might·Nature·Wood · Araphel Shadows·New Faces·Rebirth·Erasure / Darkness·Nothingness·Protection · Tani Fate·Patience·Memory·Decay / Fate·Soul·Time · Vesuna Change·Creativity·Spontaneity·Madness / Change·Luck·Trickery·Disorientation.

**Grill log (decisions):**
- **Aphorite = order as a born sense** (the blood notices; the person and their people decide). Shadow: the straighten-the-world itch (Forseti's Tyranny from the inside). Proof: at the swearing of a false oath, the Aphorite is the one who looked up.
- **Beastkin = one particular beast per carrier, instinct ahead of thought.** Flank held against Awakened Animal (animal-to-someone vs. someone-with-a-beast-alongside). Cruelty stays nature's unclaimed face (Ehizahar decision); the Beastkin shadow is **the reins** (the beast deciding before the person is consulted).
- **Changeling = becoming as an unbidden tide** (offered, where the Fetchling **decides**; that distinction keeps Araphel's own people clear of his heritage). Mismatched eyes; folk-belief: the second eye belongs to the next face. Shadow: Erasure.
- **Duskwalker = the cycle's child**, structural opposite of the Skeleton (outside the cycle vs. the cycle made flesh). **NEW CANON CLAIM (approved): undeath cannot take a Duskwalker; their soul is promised home.** Voroir Daua extend their rare courtesy accordingly. **Site duality: the Blackened Lands (the wound) + the Soul Tree of Brauogi's Twin Suns (the door)** as the two great sources; the rest of Lioaru a steady third. Shadow: the remove (letting go what should have been fought for).
- **Ganzi = the improbable leans in.** Asymmetric mirror of the Aphorite: the Aphorite has a *sense* (notices the world), the Ganzi has a *field* (the world notices them). Distinct from Gnome (spins change by temperament) and Vanara (rides it): the Ganzi has it happen *to* them. Trait declines to settle on the skin. Shadow: Madness as abandoned planning.
- **Nephilim = the parent's nature as a light pull** (USER CORRECTION: generalization had to go deeper than mark-and-reception; the carry is a light pull/tendency from the parent line, and this is the one heritage where examples are a boon). Example lines locked: Iro (hope easier than the evidence warrants), Shuun (steadied by still water, moved by the tide), Hinka (reads exits before faces), Drambur (praise to another lands as a small debt), Jafnar (keeps the favour-ledger by reflex). Shadow: feeding the pull until the lean becomes the direction. Celestial/fiendish mapping bullets + *Bound gods whose touch is not bloodline-borne* block stay beneath, unchanged.
- **METHOD (user, hard lesson):** prose proposals must be surfaced in the final chat message, never between question dialogs (text between tool calls is not shown). Surface in plain text; the explicit yes comes on visible prose.

**HTML notes for the end-of-pass bundle:** registrar Dragonblood row still says "concentrates around Dragon's Reach" (re-anchor to the Wyrmkin line / Fenurra); registrar Duskwalker row lacks the Soul Tree.

**ARCHITECTURE LOCKED (user: deep-C, full re-sourcing).** Five families, stratified by where the otherness comes from:
1. **Sparks of the substrate (Layer 1):** Ifrit→Suzar · Undine→Urzar · Oread→Lurzahar · Sylph→Haizar · Ardande→Zurzar · Talos→Burdinzar · Suli=the blend. Bound elemental gods keep doctrinal affinity by cultural gravity, never blood. **Carries = next grill batch**; the primordial personality sketches in `gods.md` are the carry-seeds.
2. **Essence of the sibling planes (Layer 2):** Aphorite→Shadowplane (order-essence, a SENSE) · Ganzi→Feyworld (chaos-essence, a FIELD); the counterpart pair, mirroring Ardande/Talos as the substance pair (a 2×2: each sibling plane expresses once as substance, once as essence).
3. **Divine parentage (Layer 3):** Nephilim ONLY, any god or devil, the bound thirteen included. New rule: a god's TOUCH never rides a bloodline (Jianna=fortune, Enki=aptitude, Cronus=choice, now generalized to all thirteen); PARENTAGE is the one way a god enters the veins. The old *Bound gods whose touch is not bloodline-borne* block dissolved into the Nephilim entry.
4. **Mortal mixes:** Aiuvarin · Dromaar (carry-entries pending) · **Beastkin → the Awakened line** (descent from an Awakened Animal ancestor; the carried beast IS the ancestor; the Ehizahar tribes' Hinka-reading kept as folk-theology, wrong about the source and right about everything else).
5. **The old powers' lines:** **Duskwalker → Epairima** (Tani dropped ENTIRELY per user; Soul Tree corrected = its own island off the coast of Twin Suns; Betibizi-countercurrent folded into the Blackened Lands clause; the Voroir Daua courtesy is now kinship with their own goddess's line) · **Changeling → Bikiargi** (the Twins' tide; mismatched eyes one Unaru's and one Veyru's; Myrria welcome survives as Araphel-doctrine culture; the shadow folk-given to Veyru) · Dhampir · Dragonblood · Hungerseed · Reflection (standing canon kept; carry passes queued).

**REGION-FREE PRINCIPLE (user):** heritage entries carry no regional reception (Zuzental dropped from Aphorite; Nashavel/Kaosadaemi/Nahaskel dropped from Ganzi); regions mention heritages in their own files when wanted. Origin-site mechanics (Duskwalker's two sources) and explicitly approved folk-readings (Beastkin's Ehizahar, Changeling's Myrria) stay.

**WRITTEN + COMMITTED:** `ancestries.md` Versatile Heritages fully restructured to the five families (all tables retired; spark and mortal-mix placeholders pending their grills); `glossary.md` mapping block remapped (also fixed the stale "Dragonblood → alien Dragon descent" line). **HTML mirrors for the end-of-pass bundle:** ancestries.html Heritages section (full restructure), registrar heritage rows (Aphorite/Beastkin/Changeling/Duskwalker/Ganzi source text, Dragonblood→Wyrmkin, Duskwalker+Soul Tree), mention checks on brauogi.html / lost-kingdom.html / nahaskel.html.

**SPARKS BATCH ✅ (user-approved, committed):** the seven carry-entries written as one chord, somatic register (the spark is substance, the body keeps the element's rules): **fire spends, water levels, earth bears, air alights; wood grows, metal is set; the Suli carries more than one** (the chord line now opens the family intro; the source-lock bullets are replaced by full entries). Ifrit = the burn (shadow: consumption; proof: "tired of being fuel"). Undine = the level (shadow: the flood; flank held vs Merfolk-moves and Centaur-rides-it-out). Oread = the bearing, weight felt like temperature (shadow: the swallow, grief become geology; flank held vs Minotaur-pace and Athamaru-no-floor). Sylph = lightness-of-hold (shadow: the fickle; flank held vs Strix-weather and Halfling-road). Ardande = grows around what happens, ring on ring (shadow: the dead branch; flank held vs Nagaji-sheds and Leshy-place-memory). Talos = set by being worked, chooses her forges (shadow: the bad set; flank held vs Aphorite-order-sense and Dwarf-method). Suli = the strata take turns (shadow: the argument; proof: tea cold, bathwater steaming, same hour).

**FINAL BATCH ✅ (user-approved, committed): mortal mixes + old-powers carries.** Aiuvarin = the second clock (the long view ticking under the other people's tempo; shadow: the long escape; proof: plants the oak for herself). Dromaar = the close, a finishing instinct (body votes a beat early, waiting spends her; shadow: the foreclosure; flank held vs Beastkin: the Beastkin senses first, the Dromaar moves first). Per the region-free principle the Zuzental/Ehizahar placement clauses were dropped from the mix bullets (they survive in the registrar). Dhampir = the threshold, alive at an angle (thirst as an echo never owed obedience; the first grey hair a private festival; shadow: the echo indulged). Dragonblood = the undertone (quiet under threat, the bones hear it first; Fenurra-compatible, temperament-level only; shadow: the cold). Hungerseed = the second helping of want (connoisseurs of enough; shadow: the bargain; flank held vs Goblin-appetite and Ifrit-consumption). Reflection = the quiet, public-tier only (the refunded lineage-reading; shadow: the undertow, a Stillpool wink with no mechanics leaked; GM paragraph untouched). The four old-powers entries keep their standing canon with the carry appended beneath. **Every heritage on Talan now carries a conventions-judged carry-entry.**

### Committed prose

The six carry-entries (Aphorite, Ganzi, Nephilim, Beastkin, Duskwalker, Changeling) are written in `lore/ancestries.md`, *Versatile Heritages*, in their locked deep-C form; the lore file is the source of truth. The superseded pre-rearchitecture draft versions (Forseti-Aphorite, Tani-Duskwalker, etc.) have been removed from this tracker.
