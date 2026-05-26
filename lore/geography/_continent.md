# Geography: Talan (Continental Frame)

This file holds the continent-wide geography of Talan: structure, infrastructure, seas, off-continent neighbours, and the naming convention for regions. **Per-domain canon lives in dedicated files in this folder**, one per god domain. When designing on top of a domain, read its file *and the files of its bordering domains*; each domain file declares its borders at the top.

## Domain Index

| Region | Domain | God | God's City |
|---|---|---|---|
| [Vindul](vindul.md) | Wind | Fisaya | Haizava |
| [Lautara](lautara.md) | Commerce | Jianna | Merkavar |
| [Myrkono](myrkono.md) | Darkness | Araphel | Myrria |
| [Floteyn](floteyn.md) | Water | Shuun | Uravel |
| [Sumendar](sumendar.md) | Fire | Komo | Eldara |
| [Lioaru](lioaru.md) | Time | Tani | Denbora |
| [Brauogi](brauogi.md) | Earth | Sarrum | Lurrath |
| [Ezkudon](ezkudon.md) | Knowledge | Enki | Thekkavar |
| [Egulon](egulon.md) | Light | Iro | Ljosarn |
| [Zuzental](zuzental.md) | Law | Forseti | Lograth |
| [Nashavel](nashavel.md) | Chaos | Vesuna | Nahaskel |
| [Ehizahar](ehizahar.md) | Hunt | Hinka | Veidrath |
| [Askamira](askamira.md) | Freedom | Cronus | Frae City |

## Structure

- **Tyrnarra**: the world. Encompasses all planes (Prelife, Life Layer, Postlife) and the Cloud Sea.
- **Talan**: the main continent on the Material Plane, where the 13 Bound Gods currently reside.
- **God Domains**: Talan's primary regions, one per bound god. Ancient in origin; named using the Basque/Icelandic convention with linguistic drift. Domain-borders are the bound god's territorial reach, not a polity's lines; the domain outlives every kingdom that occupies it.
- **Kingdoms / Sub-regions**: political and geographic divisions within each domain. **No Talanese kingdom predates 1 MR**, and few are older than the Dark Era (1321 MR – 2135 MR); most modern kingdoms were founded, refounded, or substantially redrawn in the Dark Era or its immediate aftermath. Old-sounding names are usually re-claimed from older Lost-Era polities that held the same ground, not inherited through unbroken rule. Full canon in `../timeline.md`, *Kingdom continuity across the eras*.
- **Settlements**: cities, towns, villages within kingdoms.

---

## The Continental Rail Network

Talan runs on **Magitrains**, common-place Arcanotech infrastructure. The continent has **two interconnected networks** that do not link to each other:

- **Northern Talan network**: connects the northern domains and their major cities.
- **Southern Talan network**: connects the southern domains; Sumendar (Order of Steam manufacturing) is its industrial heart.

The **Great Jungle (Basogur Jungle)**, straddling Nashavel and Ehizahar, prevents all through-rail between the two. North-south travel uses **ships across Midarra** (bulk cargo), **airships over Basogur** (premium passenger / urgent freight; Arcanotech airships do this regularly but Occultech airships fly cleaner through the jungle's chaos-magic uplift), or the **long overland road that loops around Basogur**. **Cloudships** serve the Cloud Sea crossing only; they are rare specialist craft, never deployed for domestic transport. Full canon in [`../cosmology.md`](../cosmology.md), *Technology: Magitech and Infrastructure*.

---

## The Three Seas

**Midarra**: the central freshwater inner sea of Talan. Cronus's island (Freedom domain) sits within it. Millhaven is on its southern shore. Etymology TBD; name is old, predates mortal settlements.

**Notable feature, Twin Cities** (the pirate capital). A paired settlement that drifts together through Midarra on a course set by the council of pirate lords; never in the same place twice. The two halves are:
- A floating raft-city of lashed-together hulls and ship-decks, sitting on the water.
- A sky-suspended sister-city of tethered airships and lifted islets, hanging directly above the water-city.
Both move as one. The Twin Cities answer to no god and no kingdom; they are the seat of pirate sovereignty on Talan, the place where the Pirate Lords meet, settle disputes, and divide the seas. Modern English name.

**Hafra**: the saltwater sea surrounding Talan. Sits between the continent and the Cloud Sea, with a **sharp, visible boundary** where water ends and cloud begins, a clean line on the horizon, recognisable from kilometres out.
*Etymology: Icelandic haf (ocean, open sea) → shortened and drifted to Hafra.*

**The Cloud Sea**: the vast luminous white expanse beyond Hafra. Surrounds the known world. **Crossing it requires a cloudship.** The vapor will not support weight: any ordinary hull that crosses the boundary sinks fast and the crew sinks with it; a swimmer who falls in drowns the same way they would in deep water (the surrounding cloud reads as solid until they try to grip it). Cloudships (purpose-built dual-school Magitech vessels) are the only craft that cross safely. Full canon in [`../cosmology.md`](../cosmology.md), *The Cloud Sea* and *Technology: Magitech and Infrastructure*.

### Domain sea-access summary

Most domains coast both seas. Five do not, and the absences shape continent-wide trade and politics. Each per-domain file declares its sea access at the top alongside its land borders.

| Domain | Hafra | Midarra | Cloud Sea |
|---|:---:|:---:|:---:|
| Vindul | ✓ | – | – |
| Lautara | **—** | ✓ | – |
| Myrkono | ✓ | – | ✓ |
| Floteyn | ✓ | ✓ | – |
| Sumendar | ✓ | ✓ | – |
| Lioaru | ✓ | **—** | – |
| Brauogi | ✓ | ✓ | – |
| Ezkudon | ✓ | **—** | – |
| Egulon | ✓ | **—** | – |
| Zuzental | ✓ | ✓ | ✓ |
| Nashavel | ✓ | – | – |
| Ehizahar | ✓ | – | – |
| Askamira | **—** | ✓ | – |

**Hafra-locked:** Lautara, Askamira (both reach the world by Midarra only). **Midarra-locked:** Egulon, Ezkudon, Lioaru (all reach the world by Hafra only). **Cloud-Sea touching:** Myrkono (western coast) and Zuzental (the Bridgelands; canonical Sortalde cloudship landing).

---

## Other Continents

Tyrnarra has more than one continent. Most are little known to Talanese scholars: Hafra is wide, the Cloud Sea wider, and active contact is rare. **Two are named in canon: the Red Empire's home continent (west across Hafra) and Sortalde (east across Hafra).** Others exist but remain unnamed in Talanese sources.

The bound thirteen reside on Talan, not on any other continent. The Gods' Law applies anywhere on the Material Plane (it's physics, not jurisdiction), but the gods themselves do not have established sancta or temple complexes off-continent. **This means every other continent runs on a fundamentally different theological substrate from Talan**: no walking gods, no auditioned sancta, clerical work runs through Layer-3-resident or Prelife-resident gods only (see `../gods.md`, *Named Non-Bound Gods*).

### The Red Empire's home continent (west across Hafra)

Largely unknown on Talan, but canonical: somewhere across Hafra lies a continent ruled by a godless authoritarian mortal-supremacist empire, its Iron Tide navy in routine and usually unfriendly contact with Talan's coasts. Full faction detail in `../factions.md`, *Off-Continent Powers*.

**Open thread:** The home continent's name, internal map, and any non-Imperial polities that share it with the Empire are TBD. Crossing distance is "long enough that landings are campaigns, not raids."

### Sortalde (east across Hafra): the Petal Continent

**Talanese name:** *Sortalde* (Basque *sortaldea* "sunrise-land / east"). **Sortalde-internal name:** *Tao Hua Yuan* (桃花源, "Peach Blossom Spring," after the Tao Yuanming poem about a hidden paradise reachable only through a difficult passage). Same external/internal naming split that Emarrea/Biozuri and Fenurra/Aeris use. Full etymology in `../glossary.md`.

**Shape.** A great archipelago: **seven major islands arranged in a petal formation**, six ancestral petals around a smaller central seat. Internal seas between the petals are narrow and routinely sailed by Sortalde-native vessels; the outer ring is wide, stormy, and historically the graveyard of Talanese shipping.

**Crossing from Talan.** **Hard.** The stormy outer ring of Sortalde routinely sinks Talanese ships. Surviving merchants typically reach only the **outer petals** (the three petals on the Talan-facing arc of the archipelago: Wandao, Xidao, Niudao); the inner petals (Yingdao, Lingdao, Lundao) and the central Concord seat (Heting) are rumour to most Talanese. The Iron Tide has lost ships trying; raids on Sortalde are unprofitable enough that the Red Empire's standing policy is "don't bother."

**Theology.** Sortalde has **no walking gods.** The bound thirteen all maintain their sancta on Talan; none have crossed Hafra to establish presence on Sortalde, and no indigenous Sortalde bound god has emerged. All clerical work on Sortalde channels through **Layer-3-resident gods**: a Sortalde-internal pantheon of dynasty-spirits, ancestor-judges, and place-gods who reside in Diyu and (less often) Elysium. **The pantheon is not yet named in Tyrnarra canon**; it exists as a placeholder for future development. The practical effect on daily Sortalde life is profound: religion is invocation across the veil, never personal audition. No mortal in Sortalde has ever met their god in person.

**Politics: the Concord of Courts.** The seven petals are bound together by an ancient confederation, **the Concord of Courts**, which convenes at Heting. The Concord is held together by long agreement, not enforced authority. **Samsaran chancellors** carry political memory across reincarnations, providing institutional continuity that no human lifetime can match. Each petal has its own internal governance (typically a hereditary court with a long-lived ancestral lineage), but inter-petal disputes are mediated through Concord channels.

**The seven petals.**

| Petal | Ancestry | Character |
|---|---|---|
| **Wandao** (Myriad Island) | Yaoguai | Common-folk petal, vast taxonomic spectrum; most populous; nearest Talan-side reach. Outer petal. |
| **Xidao** (Theatre Island) | Tanuki | Convivial merchants, performers, mischievous shapeshifters. Outer petal; Tanuki troupes occasionally cross to Talan. |
| **Niudao** (Ox Island) | Sarangay | Bull-folk warrior caste, strong oath-keepers, hereditary martial nobility. Outer petal. |
| **Yingdao** (Shadow Island) | Wayang | Shadow-courtiers, spies, shadow-puppet archivists. Inner petal; most Sortalde secrets pass through here. |
| **Lingdao** (Spirit Island) | Yaksha (+ Oni) | Dynastic place-spirits bound to specific lands; **also the concentration zone for bound Oni** (Yaksha's darker spirit-cousins). Inner petal. |
| **Lundao** (Wheel Island) | Samsaran | Contemplatives, senior bureaucrats; multi-life memory keepers. Inner petal. |
| **Heting** (Concord-Court) | shared | Central island; Concord seat; ambassadors from all six ancestral petals reside here. Mythically hard to reach from outside. |

**Active diplomatic interface with Talan.** Sortalde maintains **standing embassies on the Emerald Isles**, the Zuzental island kingdom whose outer holdings sit on the Hafra / Cloud Sea boundary (see [zuzental.md](zuzental.md), *Emerald Isles*). Cloudships from Sortalde make landfall on the kingdom's outer-rim islands; the embassies are staffed mostly by Wandao Yaoguai and Xidao Tanuki (the petals whose ancestries find the crossing survivable in numbers). The Adventurers' Guild does *not* maintain a Sortalde branch; expeditions there are commissioned individually and pay survivor-tax rates.

**Cultural quirk: kitsune coincidence.** The kitsune of Emarrea (Lautara) use a Japanese-flavoured internal naming register; Sortalde residents use a Chinese-flavoured register. The parallel is **purely coincidental**; kitsune are not descended from Sortalde populations and have no ancestral connection to the continent. Diplomats from the two cultures can sometimes guess at each other's pronunciation but cannot trust each other's grammar. Both cultures find the coincidence faintly insulting if pointed out, for opposite reasons.

**Hooks:**
- Any voyage to Sortalde is a campaign in itself; the outer-ring storms are the framing obstacle.
- The Tao Hua Yuan poetic-self-mythology suggests that even Sortalde residents have an ambivalent relationship with the outside; defectors and exiles exist but cannot easily return.
- A Talanese character with a Sortalde ancestry is rare enough to draw notice; their story of crossing is half-formed legend by the time they reach Lautara.
- The unnamed Sortalde Layer-3 pantheon is a deep open thread; anyone who pursues planar contact with Sortalde's gods is doing original theological work.

---

## Naming Convention (regions)

God domains are ancient; they predate mortal civilization and carry old-world names (Basque or Icelandic root, drifted). The god's domain character shapes the name but does not describe it directly. Drift can happen anywhere in the word, not just the end. Creativity and cross-language compounds are encouraged.
