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

1. **Egulon (Light)** 🔵 — biggest change (2 new + 1 reframed); the whole domain re-reads as *sunlit life*
2. **Brauogi (Earth)** ⬜ — Dragonet homed + Goblin/Hobgoblin split (kingdom rename)
3. **Zuzental (Law)** ⬜ — Hobgoblin as the Thousand Kingdom's standing discipline
4. **Lioaru (Time)** ⬜ — Nagaji rebirth-cult
5. **Ezkudon (Knowledge)** ⬜ — Ratfolk diggers
6. **Ehizahar (Hunt)** ⬜ — Goloma watch-hunters
7. **Nashavel (Chaos)** ⬜ — Anadi web-holds
8. **Lautara (Commerce)** ⬜ — execute the Ratfolk/Gaps removal (tracked in open-threads)
9. *(unchanged regions — grill-and-deepen only, lowest priority):* Myrkono, Sumendar, Floteyn, Vindul🔒, Lautara-heartland🔒, Askamira

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

*(Further region sections added as we reach them.)*
