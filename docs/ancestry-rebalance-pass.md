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

1. **Egulon (Light)** ✅ — lore committed (`6f4deec`); HTML pending. *The Year of the Vine.*
2. **Brauogi (Earth)** ✅ — lore committed; HTML pending. Earth = Minotaur/Kholo/Dragonet (Stone/Vigil/Metal). Cascade done: Goblin→Fire, Kholo→Earth, Hunt trio now Orc/Lizardfolk/Goloma.
3. **Zuzental (Law)** ⬜ — Hobgoblin as the Thousand Kingdom's standing discipline
4. **Lioaru (Time)** ⬜ — Nagaji rebirth-cult
5. **Ezkudon (Knowledge)** ⬜ — Ratfolk diggers
6. **Ehizahar (Hunt)** ⬜ — Goloma watch-hunters
7. **Nashavel (Chaos)** ⬜ — Anadi web-holds
8. **Sumendar (Fire)** ⬜ — Goblin homed (the appetite-alchemist; concept parked in Brauogi log for deep-dive)
9. **Lautara (Commerce)** ⬜ — execute the Ratfolk/Gaps removal (tracked in open-threads)
10. *(unchanged regions — grill-and-deepen only, lowest priority):* Myrkono, Floteyn, Vindul🔒, Lautara-heartland🔒, Askamira

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

### Draft (culture prose) — 📝 written to `egulon.md`, surfaced, awaiting review
- God's-city line updated (Ljosarn in Harro Distiratsue on the lake bordering Argia Esfera).
- Three sub-region bullets now name their heartland people.
- New **## The Year of the Vine** section: seed + the three peoples + the two-lights/ballast dynamic.
- **Open within Egulon (for later):** name the great kept flame/orb at Argia Esfera; Ljosarn god-city build (combines all three); Egulon wine-country economics (ties to the open-threads Azkataria→Egulon wine note); domain governance untouched.

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

### Draft — 📝 written to `brauogi.md` (## The Three Faces of Sarrum's Earth) + cascade done in `ancestries.md`; committed.

### `ancestries.md` cascade edits — ✅ DONE
- Table rows: **Earth** → Minotaur · Dragonet · Kholo; **Fire** → +Goblin; **Hunt** → Orc · Lizardfolk · Goloma.
- **Goblin** entry → Fire/Sumendar alchemist (brief; full culture later). **Kholo** entry → Brauogi/Earth herder.
- **Minotaur** entry: "alongside the Goblins" → "alongside the Kholo". **Dragonet** entry: re-frame to tradition/memory-keepers pulled up (not buried under-dark).
- **Orc / Lizardfolk / Goloma** entries: drop "alongside Kholo"; Hunt trio is now Orc/Lizardfolk/Goloma (Goloma was "wary fourth" → now "wary third/watcher"). *(Deeper Villtur re-grill happens at the Ehizahar region.)*

### Draft (culture prose) — not started

---

*(Further region sections added as we reach them.)*
