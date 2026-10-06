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
| [Lioaru](lioaru.md) | Time | Tani | Valreka |
| [Brauogi](brauogi.md) | Earth | Sarrum | Lurrath |
| [Ezkudon](ezkudon.md) | Knowledge | Enki | Thekkavar |
| [Egulon](egulon.md) | Light | Iro | Ljosarn |
| [Zuzental](zuzental.md) | Law | Forseti | Lograth |
| [Nashavel](nashavel.md) | Chaos | Vesuna | Nahaskel |
| [Ehizahar](ehizahar.md) | Hunt | Hinka | Veidrath |
| [Askamira](askamira.md) | Freedom | Cronus | Frae City |

### The thirteen god-cities by size

**Every god-city is settlement level 20**, whatever its headcount. In PF2e terms a settlement's level is its economic capacity and the ceiling of what can be found there; a resident Grand God puts all thirteen at the top of the scale, so any common item up to 20th level is somewhere in the city and the person pouring your drink may be the most dangerous mortal in the domain. Population is a separate axis, and it varies by a factor of fifteen. The bands below are canon; the figures are 2532 MR and round.

| Band | City | Population | What sets the size |
|---|---|---|---|
| **I · the continent's city** | **Frae City** | 1,100,000 | Outgrew its rock, grew upward into towers, then spilled down the seven chains onto the lakeshore; about 350,000 on the rock and in the towers, 750,000 around the anchor-points on the shore. The great airship port and the centre of the continent. |
| **II · the great cities** | **Merkavar** | 420,000 | The market city, the lake for a street, the trains delivering the continent to it daily. |
| | **Lograth** | 380,000 | God-city and capital of the Thousand Kingdom in one; the Arteries stack it high. |
| **III · the great seats** | **Myrria** | 240,000 | Every exile and second-chancer on Talan heads there; carved into a mountain, dense and finite. |
| | **Ljosarn** | 220,000 | Pilgrimage city on Vonura; the Healing Orders; every Iro church relays lanterns home. |
| | **Thekkavar** | 180,000 | The university city; the Lanterns draw the continent's students and send them home again. |
| | **Eldara** | 160,000 | Forge and industry inside a volcano; the mountain sets the limit. |
| | **Lurrath** | 150,000 | Never fallen and always prosperous, but the rail dies at the Harrate gate and the last miles are portage. |
| **IV · the shaped cities** | **Nahaskel** | 120,000 | A city remade overnight holds only as many as can re-learn it each morning. |
| | **Haizava** | 110,000 | Sails, vanes and rope-bridges carry only so much weight in a wind that rebuilds them. |
| | **Uravel** | 90,000 | A hall no one visits drowns; the city is as large as the halls it can keep answering. |
| | **Veidrath** | 80,000 settled · up to 200,000 at a gathering-peak | Mid-settling: the Core and the belt hold the floor, the tent-rings triple it in season and empty again. |
| **the floor** | **Valreka** | 70,000 | Nineteen whales. The smallest of the thirteen, and the only one that cannot grow except by bonding a new whale. |

The thirteen together hold about 3.4 million people. The kingdom capitals sit below them; a Kingshall city of 60,000 to 150,000 is a large one.

### Population density

The countryside is sized in two tiers (GM, 2026-09-29). **Held heartlands**, the farmed country a polity has kept since the Dark Era ended, carry **20 to 40 people per square mile**: the thin end of the medieval range, refilled across four centuries of the Adventurer Era and held there by the beasts of the wild. **Wild country** (for example the Basogur, the deep forests and the high ranges) carries **2 to 10**. The Blackened Lands sit below the wild tier: almost all of the ground holds no one, and their people live behind Ida's wall (`geography/lioaru/lost-kingdom.md`). A region's population is its map area times its tier; on the full-resolution map one square pixel is a quarter of a square mile.

The cities set the floor. A kingdom capital holds one to three percent of its country, and the god-cities draw on their domains and on the rail. The reference case is the **Legea Empire**: a Dark-Era refuge turned heartland at 25 per square mile, about 140,000 square miles and 3.5 million people, with a capital of 75,000.

## Structure

- **Tyrnarra**: the world. Encompasses all planes (Prelife, Life Layer, Postlife) and the Cloud Sea.
- **Talan**: the main continent on the Material Plane, where the 13 Bound Gods currently reside.
- **God Domains**: Talan's primary regions, one per bound god. Ancient in origin; named using the Basque/Icelandic convention with linguistic drift. Domain-borders are the bound god's territorial reach, not a polity's lines; the domain outlives every kingdom that occupies it.
- **Kingdoms / Sub-regions**: political and geographic divisions within each domain. **No Talanese kingdom predates 1 MR**, and few are older than the Dark Era (1321 MR – 2135 MR); most modern kingdoms were founded, refounded, or substantially redrawn in the Dark Era or its immediate aftermath. Old-sounding names are usually re-claimed from older Lost-Era polities that held the same ground, not inherited through unbroken rule. Full canon in `../timeline.md`, *Kingdom continuity across the eras*.
- **Settlements**: cities, towns, villages within kingdoms.

---

## Scale

**The map's scale bar reads 0–1000 miles** (GM, 2026-09-25): on the 8192 px terrain original, **1 px = 0.5 mile**. At that scale Talan runs about **3,500 miles** west to east and north to south, about **4,000 miles** (6,400 km) from its north-west coast to its south-east coast, and covers about **7.5 million square miles**: the size of South America, in a round, compact shape. The thirteen god domains average about **575,000 square miles** (about Alaska each); the forty-odd regions average **150,000–190,000 square miles** (about Spain or California), with Villtur, the Basogur, and the southern deserts far larger and the island realms far smaller. The **Midarra** runs about 2,650 miles end to end and covers about 1.9 million square miles, twice the Mediterranean. Travel speeds built on this scale are in [`../transport.md`](../transport.md), *Speeds*.

**The map shows landmarks, not land cover** (GM, 2026-09-29). At this scale the map is an overview: it draws the borders, coasts, major rivers, named ranges and forests, capitals and god-cities, and lore does not contradict what it draws. Where the map shows nothing, that is no evidence of emptiness: a region the size of Spain holds river valleys, hill country, lesser woods, heath, marsh, and dozens of towns, and lore adds features below the map's resolution freely. Anything lore adds that would show at the map's scale (a range, a large forest, a lake, a named town) goes to [`../../docs/map-todo.md`](../../docs/map-todo.md) to be drawn in at a detail pass.

---

## The Continental Rail Network

Talan runs on **Magitrains**, common-place Arcanotech infrastructure. The continent has **two networks** that do not link to each other:

- **Northern Talan network**: connects the northern domains and their major cities.
- **Southern Talan network**: connects the southern domains; Sumendar (Order of Steam manufacturing) is its industrial heart.

The **Great Jungle (Basogur Jungle)**, straddling Nashavel and Ehizahar, prevents all through-rail between the two. North-south travel uses **stillships across Midarra** (bulk cargo), **airships over Basogur** (premium passenger / urgent freight; Arcanotech airships do this regularly but Occultech airships fly cleaner through the jungle's chaos-magic uplift), or the **long road** through the jungle, eleven days from Greenmouth to Veidrath under the Roadwards. **Cloudships** serve the Cloud Sea crossing only; they are rare specialist craft, never deployed for domestic transport. Full canon in [`../cosmology.md`](../cosmology.md), *Technology: Magitech and Infrastructure*.

---

## The Three Seas

**Midarra**: the central freshwater inner sea of Talan. Cronus's island (Freedom domain) sits within it. Millhaven is on its southern shore. Etymology TBD; name is old, predates mortal settlements.

**The Villveder.** The Midarra is rarely violent and occasionally strange. Without warning that any chronicler has learned to read, magic turns unreliable across a stretch of open water: a needle wanders, a bearing true at dawn is wrong by noon, worked charms slip their intent, and the sky over the affected water carries weather the crews cannot place. The record calls these the **Villveder**. Scholarship agrees on little beyond that they are something other than ordinary storm, and the reading most often written down is a fluctuation in the Wellspring itself, reaching the inner sea and unsettling it; the Listeners at Uravel have been asked and decline to be drawn. They are rare enough that a working captain may cross the Midarra for thirty years and meet one, or none. Crews caught in a Villveder steer by eye, by shore-shape, and by the sea's own behaviour until it lifts. The Villveder is the standing reason the inner sea demands instruments that do not lie, and the reason Breidey's helmworks hold the trust of every serious captain on it.

**Notable feature, Twin Cities** (the pirate capital). A paired settlement that drifts together through Midarra on a course set by the council of pirate lords; never in the same place twice. The two halves are:
- A floating raft-city of lashed-together hulls and ship-decks, sitting on the water.
- A sky-suspended sister-city of tethered airships and lifted islets, hanging directly above the water-city.
Both move as one. The Twin Cities answer to no god and no kingdom; they are the seat of pirate sovereignty on Talan, the place where the Pirate Lords meet, settle disputes, and divide the seas. Modern English name.

**Hafra**: the saltwater sea surrounding Talan. Sits between the continent and the Cloud Sea, with a **sharp, visible boundary** where water ends and cloud begins, a clean line on the horizon, recognisable from kilometres out.
*Etymology: Icelandic haf (ocean, open sea) → shortened and drifted to Hafra.*

**The Cloud Sea**: the vast luminous white expanse beyond Hafra. Surrounds the known world. **Crossing it requires a cloudship.** The vapor will not support weight: any ordinary hull that crosses the boundary sinks fast and the crew sinks with it; a swimmer who falls in drowns the same way they would in deep water (the surrounding cloud reads as solid until they try to grip it). Cloudships (purpose-built dual-school Magitech vessels) are the only craft that cross safely. Full canon in [`../cosmology.md`](../cosmology.md), *The Cloud Sea* and *Technology: Magitech and Infrastructure*.

**Sea-craft.** Talanese hulls divide by the water they are built for. A **saltkeel** is a Hafra craft: sealed and timbered against brine, deep-keeled for the open saltwater ring and its storms. A **stillship** is a Midarra craft: lighter, shallower, untreated for brine, built for the calm freshwater inner sea and its bulk runs. The split is a hull-class, independent of whether the vessel is plain wood-and-sail or Magitech. Each *can* cross onto the other sea, but poorly: a stillship pushed onto the Hafra is eaten by salt within a season and swamped far more easily by open-water swell, while a saltkeel on the Midarra rides too deep and handles heavy and slow. In practice most cargo passing between the seas changes hulls at **Gesalkai** on **Balatur Erui**, the fixed island in the Midarra's mouth (see [`floteyn/balatur-erui.md`](floteyn/balatur-erui.md)). **Cloudships are a separate matter entirely**, the rare dual-school craft built for the Cloud Sea alone; they are never the everyday hull of either sea.

**Sea-charts.** Charting follows pilotage: each water is mapped by the craft that reads it. The open **Hafra** is charted by Fellibylur's **Stormriders**, the only pilots who hold its deep lanes, currents, and storm-roads out of sight of land; a Stormrider's working copy is a personal **field-book**, and the master charts are certified and kept by **the Skybell Republic** in its port-archive at Brasswatch, **the Saltkeep**. This makes Vindul the keeper of both great cartographic traditions: the **Wyndwalken** map the land from the shore, the Stormriders chart the saltwater past it. The enclosed **Midarra**'s master charts belong to the **Sweetwater League** of the Floating Isles: **the living chart**, corrected voyage by voyage by the League's ever-sailing crews and kept at the **List-house** at Uravel, the only chart of a sea whose islands move (see [`floteyn/floating-isles.md`](floteyn/floating-isles.md)). The Dreaming Cape's **Wakehelm** hold the bay-mouth and Midarra-coastal pilotage, and **Gesalkai's pilots on Balatur Erui** hold the gate crossing where the two seas meet (and are politely definite that the inner sea's deep charts are not their craft).

### Domain sea-access summary

Seven domains coast both seas (Nashavel, Ehizahar, Brauogi, Myrkono, Floteyn, Sumendar, Zuzental; GM, 2026-09-26); the rest reach only one, and the absences shape continent-wide trade and politics. Each per-domain file declares its sea access at the top alongside its land borders.

| Domain | Hafra | Midarra | Cloud Sea |
|---|:---:|:---:|:---:|
| Vindul | ✓ | – | – |
| Lautara | **—** | ✓ | – |
| Myrkono | ✓ | ✓ | – |
| Floteyn | ✓ | ✓ | – |
| Sumendar | ✓ | ✓ | – |
| Lioaru | ✓ | **—** | – |
| Brauogi | ✓ | ✓ | – |
| Ezkudon | ✓ | **—** | – |
| Egulon | ✓ | **—** | ✓ |
| Zuzental | ✓ | ✓ | ✓ |
| Nashavel | ✓ | ✓ | – |
| Ehizahar | ✓ | ✓ | – |
| Askamira | **—** | ✓ | – |

**Midarra only:** Lautara, Askamira. **Hafra only:** Vindul, Lioaru, Ezkudon, Egulon. **Cloud-Sea touching:** two islands only, and both are the Cloud Sea's special ground: the **Bridgelands** of the Emerald Isles off Villtur's east coast (Zuzental; the canonical Sortalde cloudship landing) and **Jadrey**, Lua Lasai's exclave off Egulon's south-east coast (Egulon; quayless by island law).

---

## Other Continents

Tyrnarra has more than one continent. Two are named in canon: **the Red Empire's home continent** (west across the Cloud Sea) and **Sortalde** (east across the Cloud Sea). Both, plus the six Sortalde petal-peoples, the Iron Tide, and the Menagerie, live in [`_off-continent.md`](_off-continent.md).

---

## Naming Convention (regions)

God domains are ancient; they predate mortal civilization and carry old-world names (Basque or Icelandic root, drifted). The two roots are the two deep tongues (see *Naming strata across the eras*): an Icelandic root is the **Silent Tongue**, ground the Elden named and the god kept (Vindul, Floteyn, Lioaru); a Basque root is the **Court Tongue**, a name the gods gave (Ehizahar, the oldest name on Talan); a compound is Elden ground the gods renamed and half kept (Brauogi, Myrkono). The god's domain character shapes the name but does not describe it directly. Drift can happen anywhere in the word, not just the end. Creativity and cross-language compounds are encouraged.

---

## Languages

### The Common Tongue: Talanese

The continental common language is called **Talanese**, and it is an **inheritance of the Golden Empire**.

Under the Empire (560 MR – 1325 MR), **Imperial Dwarvish** was the language of administration, contract, and trade across roughly two thirds of the continent. Every kingdom under Imperial reach had to deal with it: the legions, the road-stations, the tax-collectors, the road-merchants who paid Imperial tolls all spoke it as a working language. Seven centuries of compulsory exposure produced a steady braid in every local mortal community: Imperial Dwarvish vocabulary and clause-grammar woven through whatever the local tongue had been, mortared together by the simple convenience of being understood by the next caravan-stop.

By the time the Empire fell, the braid had a name. **Talanese** is what came out of it.

**Modern Talanese** is the continental lingua franca: spoken in every kingdom, taught to children alongside the local tongue, used for inter-domain trade, diplomacy, the Adventurers' Guild's standing reports, the Magitrain conductors' announcements, and the Imperial-fossil law-books every kingdom still reads. The spine of the grammar is Imperial Dwarvish; the surface vocabulary is whatever each region kept, drifted, and mixed in. A Talanese speaker today reading an Empire-era legal document recognises perhaps a third of the words at sight, more with any scholarly training.

**Post-Imperial spread.** Two regions of Talan were never under the Golden Empire's banner: **Ehizahar** (the wild Hunt domain) and the **Basogur Jungle** that straddles Nashavel and Ehizahar. Talanese is spoken in both today anyway. The principal vector is **the Adventurers' Guild**, whose official working language is Talanese: Guild Branch Offices and Office-tier outposts carried the tongue into every settlement that ever took a contract, and centuries of Guild presence have made Talanese the trade-language of even the tribal Lands of Villtur and the river-villages on the Basogur fringes. **It is not universal in either region.** Pockets persist where the local tongue is the only one anyone speaks: certain remote Villtur tribes whose grievances with outsiders run too deep to admit a foreign language, certain Basogur holds, clans, and tribes whose Anadi, Vanara, and druid residents have never had a Guild contract delivered to them, and ritual-only languages preserved by druids and shamans across both. An adventurer fluent in Talanese will be understood in any settlement on a Guild map; off the map, fluency is a roll.

### Dialects

Talanese carries regional dialects in every domain. They diverge in vocabulary, accent, and idiom but not in mutual intelligibility: a Lautaran merchant and a Vindul highland herder can negotiate without an interpreter. Major recognised dialects include:

- **Lautaran merchant cant**: quick, contract-heavy, with a Jianna-tradition habit of finishing a deal with a verbal seal-phrase
- **Vindul highland Talanese**: sing-song intonation from the mountain monasteries; preserves more old-Imperial vocabulary than most dialects
- **Ehizahar tribal registers**: pruned-down, faster, with a clan's own inflection over the shared spine, so that grass clans, snow clans and jungle-edge clans are told apart by ear
- **Sumendar industrial Talanese**: heavy with Order-of-Steam coinages for machinery and Magitech parts; faster than the southern average
- **Zuzental legal Talanese**: formal, sub-clausal, the closest of the modern dialects to the original Imperial Dwarvish
- **Brauogi village Talanese**: slow, agricultural-calendar-rich, the dialect outsider chroniclers most often hear as *"the way Talan really sounds"*
- **Egulon temple Talanese**: Iro-clergy-shaped, with characteristic ritual-cadence
- **Myrkono shadow-cant**: softer consonants, hedged grammar, Araphel-doctrine influence on the choice of indirect-address forms

Other domains carry recognised variants but the eight above are the most-named by scholars. The dialects are converging at the speed of the rail network: a town with daily Magitrain service hears two or three other dialects every day, and the convergence of usage is visible across decades.

### The families of Talan

Talan speaks more than a dozen families of tongue, and a family is a kinship: tongues of one family share their roots, and the nearer the kin, the more of a neighbour's speech a traveller catches. A tongue belongs to a place and the culture raised there, never to a people's blood. A kitsune raised in Merkavar speaks Merkavar's tongue, and anyone raised in Emarrea speaks Emarrea's; an ancestry shares a tongue only as far as its people live together in one culture. Families follow the ground and the history laid on it, not the god-domains: a domain border is no language line, Zuzental holds four families, and Uralic crosses from Vindul into Brauogi.

**In our voice.** Each family is rendered with a real-world language family for its sound, and the real-world kinship stands for the Tyrnarran one. Kinship is counted at the branch (Germanic, Romance, Celtic, Iranian, Berber), never the superfamily: Germanic, Romance and Celtic are three unrelated families on Talan, and so are Iranian and Berber. Within a family, a closer real-world relation means a closer Tyrnarran one (Italian and Portuguese are near cousins). Every base is rendered speakable for a German- and English-speaking table: the real-world language is inspiration for the sound, never a transcription, in plain letters, with a hard sound (an ejective, a click, a tone) suggested by a spelling a reader can say, or dropped. Three layers stand outside the rule: the two deep tongues (see *Naming strata across the eras*), Talanese, and the speech of the Wildreach, which the Feyworld touches and which answers to no mortal family (designed at the Wildreach's build).

| Family (in our voice; the chroniclers' name) | Where it is spoken | Notes |
|---|---|---|
| **Germanic, the imperial root** (Imperial Dwarvish's daughters); chroniclers: *the imperial dwarven tongues* | the Thousand Kingdom's spine; Kaosadaemi | The tongue the Golden Empire's dwarves carried; **Talanese** grew on its spine. The Thousand braids it with its native Romance. |
| **Germanic, the southern root** (Old Dwarvish's line); chroniclers: *the southern dwarven tongues* | the Order of Steam (German); the drifting isles of Floteyn: the Floating Isles, Balaena, Balatur Erui, Uravel (Norse, the mainland Scandinavian end) | Old Dwarvish is the southern mountain dwarves' old speech, kept on purpose by the Order. The isles are its sea-daughters, every docking a new dialect; the boats share a common crew-tongue on the Hanseatic model. |
| **Romance**; chroniclers: *the inner-sea tongues* | Legea (French); the Thousand's native layer; Namur (Italian); Harro Distiratsua and Lua Lasai (Iberian); Argia Esfera (Portuguese) | Sister tongues from a root older than the Crimson Rain, along the inner sea and down the south-east. |
| **Celtic**; chroniclers: *the jungle-edge tongues* | Vernua (Irish), Nahaskel (Welsh) | The east's oldest family, once wider, pressed back to the jungle's edge. |
| **Japonic**; chroniclers: *the Lautaran tongues* | Emarrea (Japanese: Kotokoe, the highland core); the Lautaran plain: Itsasalda, Merkavar, Azkataria, Atarialda, the Dreaming Cape at home (Ryukyuan-sounding sisters) | One family across Lautara; each region adds sound rules of its own, so the busiest country on the continent never sounds like one place. |
| **Greek**; chroniclers: *the Ezkudon tongue* | Ezkudon: Jakinduria and Thekkavar (Attic); the Golden Coast and the ring country (a Doric or Ionic drift) | The scholars' tongue meets the plain's Japonic on Azkataria's coffee-house floor. |
| **Iranian**; chroniclers: *the tongues of the south-western sands* | Hareaveldi (Persian: **Sokhan**); the Lost Kingdom (**Hizva**, an Avestan or Old Persian sound, the oldest form) | The Lost Isle's tongue is decided at its build. |
| **Berber**; chroniclers: *the whale-tongues* | Galdua Jendea and Valreka (Awal); the River Duchies (a sister) | The herd and the valley trade and marry, and the kinship is audible. |
| **Polynesian** (a Māori base); chroniclers: *the mountain tongues of Sumendar* | Tahu Tangata, Haraour Eliza, the Red Dominion, Burdineyja (both island groups) | Sumendar's own: an inland and mountain family, the Red Dominion its only seafaring branch. The Elden gate carries the same tongue to Burdineyja's Midarra group. |
| **Kartvelian** (Georgian); chroniclers: *the Reach-tongue* | Dragon's Reach | No kin on Talan: the Dragons came from beyond the world. |
| **Mongolic**; chroniclers: *the clan tongues* | Villtur (a continuum by ground: grass, snow and jungle-edge clans each sound different); Veidrath (the common Mongolic of the gathering); Ardo Beroa (the island dialect); Fenurra (four tribal dialects sharing a harder crater sound) | Talan's largest family never under the Empire. |
| **Uralic**; chroniclers: *the northern tongues* | Baerfrost (Sami); Haizetsua (Finnish); Haldmark (Estonian or Karelian); Fellibylur (Hungarian; the Skybell ports lean Talanese); Haizava | The old north-west, never held by the Empire in its far north. |
| **Quechuan**; chroniclers: *the Myrkonan tongues* | Myrkono: Ilun Tasun, Itzasoa, Izarelai, Three Pines (Cusco, Central and Kichwa sounds); Tvisol (a sister with a Norse sound rule over it, from the ferry trade) | Myrkono held through the Dark Era and kept its own. |
| **Dravidian**; chroniclers: *the island tongues of Askamira* | Askamira: Maitagarri (Malayalam), Basamortua (Telugu), Dea Elurra (Kannada), a Tamil core | The island's own people, there before Frae City. |
| **Bantu** (Swahili) | the Anadi of the Basogur | |
| **Indo-Aryan** (Sanskrit) | the Vanara of the Basogur | |
| **Tibetic** | the Order of Law | A monastic pocket, carried in by the founding and kept apart. |
| **Ainu** (an isolate); chroniclers: *the Grove Tongue* | the Elkaride of Hirubaso, taught only within the order | Kin to nothing on Talan and spoken by no one else: the druid order's own tongue, kept beside its members' Talanese. Its own name and sound rules land at Hirubaso's naming pass. |
| **Outside the rule**; chroniclers: *the speech of the Wildreach* | the Wildreach | Touched by the Feyworld, answering to no mortal family; designed at the Wildreach's build. |
| **Talanese, native** | Brauogi's reclaimed ground (Greenward, Baratalda, Hirubaso at home, the Soul Tree, Lurrath); the Emerald Isles; Rika Tikur; No Man's Land; Eldara; Frae City; Star Island; the Air Monastery | Where a land was emptied and refilled by many peoples, or where strangers gather from everywhere, the tongue they share becomes the native one. |
| **The Court Tongue, still spoken** | Sugeiturri's River Houses; the druid tribes of the Basogur | See *Naming strata across the eras*. |

Off the continent, **Sortalde**'s petals keep their own Chinese-flavoured tongue; Talanese diplomats need interpreters. A **god-city** speaks its host region's tongue and keeps a naming scheme of its own. **Hringseyja** is split along the Quietline: the Itsasaldan half speaks the plain's Japonic, the Legean half French, and the protocol-day markets are where the two meet.

**What every tongue carries.** No tongue stands alone: each carries a **contact layer** of words lent by its neighbours and its trade. And everywhere the Golden Empire ruled, the old tongue carries **the imperial loan layer**: Talanese and old Imperial words in its names and trades, deepest where the Empire held longest. Never-held ground (Ehizahar, the Basogur, Baerfrost, the Thousand after it broke away) carries the least, so a traveller with an ear can hear whether a place was ever Imperial. The strangest entry on the family map is in Zuzental's far east: the Thousand Kingdom, which the Empire did not hold at its height, speaks the living tongue nearest to Imperial Dwarvish, and its legal Talanese is the closest of all the dialects to the Imperial original. The chronicles leave it unexplained; the answer is GM-tier (`../timeline.md`, *⚿ The cradle*).

**Before the Rain.** Families were spoken on Talan long before the Crimson Rain: the Romance root, Celtic in the east, and an old Iranian root in the south-west, where the Storveldi Denbora rose. Scholars argue over a likeness between fragments recovered from the Blackened Lands and the speech of Hareaveldi, and the argument has never been settled.

#### ⚿ GM Secret: the tongue of Tani's killers

The likeness is descent. The Iranian family came from the Storveldi Denbora's own tongue, the speech of their homeland under the two deep tongues they dressed themselves in: the Nagaji of Hareaveldi speak its daughter, and the oldest form of it survives in the Blackened Lands as **Hizva**, the tongue of Ida, coming back to the risen through the memories in the Storveldi bones they got up in. The Storveldi tongue is lost to the chronicle record and alive on the ground.

**Imperial Dwarvish and Old Dwarvish.** Imperial Dwarvish is now an antique: read by scholars to parse Empire-era law-books, spoken by no community as a living tongue. The Golden Empire's spine is the spine of Talanese itself, and that is the form in which the Empire still speaks. Old Dwarvish is its sister in one family, the tongue of the southern mountain dwarves, preserved on purpose as the Order of Steam's antique register (House Eisenhart's internal tongue). Two dwarven peoples, two roots of one family: see [`../timeline.md`](../timeline.md), *The Golden Era*.

### Naming strata across the eras

What a thing is called depends on when it was named, and a place carries its history on the surface of its names. Chroniclers who date a house, a hall, or a road by the sound of its name are usually right.

| Era | Stratum | What it sounds like |
|---|---|---|
| Elden Era (6000 GR – 2945 GR), and the first stretch of the Gods' Era | **Deep: the Silent Tongue** | The Elden's tongue (Icelandic with drift in our voice). Its names outlived the Elden; its meaning did not. They vanished in a single day, so the peoples who had lived under them went on using their words for a time, fading as the gods' speech took over. |
| Gods' Era (2944 GR – 1 GR), the hinge of 1 MR, and the early Lost Era | **Deep: the Court Tongue** | The tongue the gods ruled Talan in (Basque with drift in our voice). Old and holy things were named in it across every family's ground while mortals spoke their own families' tongues at home; after the Rain the namers held to it a while longer. Few things were named in those years, and a name from either deep tongue is opaque and worn. |
| Late Lost Era | Deep giving way to **regional** | Each region's own tongue begins naming what it founds. |
| Golden Era (560 MR – 1325 MR) | **Talanese** | The Imperial braid, rendered as English with drift; the Empire named nearly the whole continent in it, and Golden-Era foundations still carry those names. |
| Dark Era (1321 MR – 2135 MR) to today | **Regional** | The Empire gone, the regions named in their own registers again, and the Dark-Era refoundings are the reason most living names sound local. |
| The Adventurer Era, tending | Talanese returning | The rail and the Guild connect everyone, and plain Talanese is creeping back for the simple reason that everyone understands it. |

**Two deep tongues.** The deep stratum is two tongues, and a scholar who knows them can read a deep name's age off its sound. The **Silent Tongue** was the Elden's, the speech of the three thousand years they held Talan; it survives in names and ruin-inscriptions, and no one has spoken it since the generations after the Elden vanished. The **Court Tongue** was the speech of the gods' courts and households in the Gods' Era, when the gods ruled as kings, landlords and law. The gods themselves speak every tongue, and a prayer reaches its god in whatever language it is prayed; the Court Tongue is the one they ruled Talan in, not their own true speech. Folk say *the old tongue* for both and keep them apart only in the scholar's mouth.

**Reading a deep name.** A Silent-Tongue name is Elden ground that outlasted its namers, and a domain named in it is ground the god kept (Vindul, Floteyn, Lioaru). A Court-Tongue name was given by the gods or their courts (Ehizahar, the oldest name on Talan). A compound is the gods renaming Elden ground and keeping half of it: Brauogi, the bread named twice over (*brauð* + *ogi*), and Myrkono (*myrkur* + *kono*). The **Storveldi Denbora** wore both, a word from each on a people who spoke neither at home: their claim to Elden descent, made in language.

**The Court Tongue lives on.** Two communities never stopped speaking it. **Sugeiturri**'s River Houses kept the gods' rivers before mortals took them at the Rain, and still speak the tongue the rivers were kept in; Brauogi spoke it as a living tongue until the Dark-Era blight emptied the basin. The **druid tribes of the Basogur** keep it among the old wood. It is also the **holy tongue of the bound thirteen's clergy**, carried in their rites the way an older language carries a liturgy, and the sanctums bear it: Igarbe, Zutarri, Urbarren, Urdeia, and the Legedi's *lege-*.

#### ⚿ GM Secret: whose tongue the Silent Tongue is

The Elden became the Corrupted God (see [`../cosmology.md`](../cosmology.md), *⚿ GM Secret: The Corrupted God: True Identity*). Every Silent-Tongue name on the map is a word in the tongue of the thing bound beneath the world. Scholars who tell the two deep strata apart credit the Silent Tongue to the Elden from ruin-inscriptions, and stop there.

**Silent-Tongue names after the Elden** (authoring rule). A Silent-Tongue name on something named after the first stretch of the Gods' Era is out of its era. By default it is re-rendered at the region's naming pass, into the region's family or the Court Tongue. It is kept where the place plausibly is Elden ground, named then and settled later (case by case; a GM-Written page only on the GM's word). A learned coinage, a scholar or founder reaching for Elden words the way scholars reach for an old learned tongue, is allowed only where the name has a real scholarly reason.

**The regional registers.** A register has two parts. Its **word-base** names the region's places and things, and neighbouring regions may share one. Its **personal-name structure** is the region's fingerprint: no two regions are alike, and a mortal's name says where their family is from even two generations after it moved. The structures are recorded in [`../glossary.md`](../glossary.md) under each region's block; the word-bases are listed here.

| Region | Word-base (in our voice) | Personal-name structure | Recorded |
|---|---|---|---|
| Emarrea (Lautara) | Japanese (Kotokoe) | kitsune convention | `glossary.md`, *Kitsune proper nouns*; `geography/lautara/emarrea.md` |
| Fenurra (Ehizahar) | **Re-render pending at Fenurra's naming pass:** Mongolic, four tribal dialects sharing a harder crater sound (hard *k* and *kh*, doubled consonants, hyphenated compounds); formerly Latinate / Germanic | Fenurran tribal convention | `glossary.md`, *Fenurran proper nouns*; `geography/ehizahar/fenurra.md` |
| Thousand Kingdom (Zuzental) | Germanic / French | house prefix + ancestry suffix, heir-status mobility | `glossary.md`, *Thousand Kingdom: the noble-naming convention* |
| Haizetsua (Vindul) | Tengu register, on a Uralic (Finnish) sound | Tengu convention | `geography/vindul/haizetsua.md` |
| Sortalde (off-continent) | Chinese-flavoured | dynastic | `_off-continent.md` |
| Nahaskel (Nashavel) | Welsh; field-words in old Talanese | whim-name + coin-name + felt-family, field last; the coin-name is the one fixed part, the rest changes freely; eight fields (beod · wyrht · bytel · fare · laec · ceap · lar · wraec) | `glossary.md`, *Nahaskel → the Nahaskel register*; `geography/nashavel.md`, *Nahaskel → What a Nahaskeli is called* |
| Vernua Dominion (Nashavel) | Irish | two given names + two steadings, one of each from each parent, the same-sex parent's first; steadings never change; the Maors carry one house with the particle *O* | `glossary.md`, *Vernua Dominion → the Vernua register*; `geography/nashavel/vernua.md`, *What a Vernuan is called* |
| Kaosadaemi (Nashavel) | old Germanic (the Thousand's pre-Dark-Era layer); Talanese for places and trades | given + born + tuning: the birthplace as the middle name, the line's first repeatable making as the family name (or its trade-word); the house alone carries the Thousand's surname | `glossary.md`, *Kaosadaemi → the Kaosadaemi register*; `geography/nashavel/kaosadaemi.md`, *What a Daemi is called* |
| Lands of Villtur (Ehizahar) | Mongolian (Khalkha) | given + hunt + clan; the clan half is current belonging, with the Talanese particles *of* (kinrider), *is* (leader), *was* (clanless); marriage moves a name; the stopped carry the place | `glossary.md`, *Lands of Villtur → the Villtur register*; `geography/ehizahar/villtur.md`, *What a Villturian is called* |
| Valreka (Lioaru) | Tamazight (Awal, the herd's speech) | given + birth-whale + chosen whale; *u* / *ult* for the guiding blood; *Mez-* child prefix, *-ghar* elder suffix | `glossary.md`, *Valreka → the Valrekan register*; `geography/lioaru.md`, *Valreka → What a Valrekan is called* |
| Galdua Jendea (Lioaru) | Tamazight (Awal, the rock dialect: places in the feminine frame, endings kept) | given + *n* + rock + the waterings stood (*of sixteen*), counted by the keepers at every watering; counts compare only within a rock | `glossary.md`, *Galdua Jendea → the Galduan register*; `geography/lioaru/galdua-jendea.md`, *What a Galduan is called* |
| The Lost Kingdom (Lioaru) | the oldest Iranian form (Hizva: Avestan and Old Persian sound, archaic endings kept) | given + the reading (*Ast* / *Urvan* / *Zam*, the source of the first marthra one could read), + a remembered name for many | `glossary.md`, *The Lost Kingdom → the register of Ida*; `geography/lioaru/lost-kingdom.md`, *What the people of Ida are called* |
| Hareaveldi (Lioaru) | Persian (Sokhan), modern endings, plain letters | given + self-name + family: the self-name taken at each carrying-out and given to the sand with the old self's portrait; a child carries given + family until the first carrying-out | `glossary.md`, *Hareaveldi → the Hareaveldi register*; `geography/lioaru/hareaveldi.md`, *What a Hareaveldi is called* |
| Basogur Jungle: the Anadi (Nashavel · Ehizahar) | Swahili | given + story + hold: the story is the title of her first woven story, taken at coming of age and replaced only by a grander one (the hold says both for a year); the hold she was strung in never changes | `geography/nashavel/basogur.md`, *What the jungle's people are called*; `glossary.md`, *Basogur Jungle* |
| Basogur Jungle: the Vanara | Sanskrit | given + clan + the name the led gave, given by the first travelers she brings through and kept in their tongue; two names until she has led a crossing | as above |
| Basogur Jungle: the druid tribes | the Court Tongue, still spoken (Basque tree-words, worn); Talanese for groves and tribes | tree + grove + tribe: the child and her tree share a name, and the survivor keeps it; the grove is named for what happened there | as above |
| Argia Esfera (Egulon) | Portuguese, plain letters; Basque for the mountain, its fires, and the wines | given + well (the household's cistern or spring, kept for life); + *da/do* comenda for the Aguarda; + the heat walked, in Talanese, for a paladin | `glossary.md`, *Argia Esfera → the Argian register*; `geography/egulon/argia-esfera.md`, *What an Argian is called* |
| Legea Empire (Zuzental) | **Re-render pending at Legea's naming pass:** Romance (French); the names now in canon are Ge'ez / Amharic, plain letters; holy words in the Court Tongue's *lege-* | day-name + Deia + reading-house (*ye-*): the day-name is the first free name on the birth-day's litany (ten per sex per day) among the house's living faithful, freed again at death or apostasy; the Deia given by the book at fifteen and changed with each new life; converts named for the day of reception; demigods alone choose a throne-name | `glossary.md`, *Legea Empire → the Legean register*; `geography/zuzental/legea-empire.md`, *What a Legean is called* |
| Order of Law (Zuzental) | Tibetan, plain letters; the Order's practices and offices in plain Talanese; Kyrrskog in the deep stratum | two names given by a monk; after sitting the Court of One, one is set down for a self-chosen name, anything except a monk-given name, so a name shows whether its bearer has sat | `glossary.md`, *Order of Law → the Order's register*; `geography/zuzental/order-of-law.md`, *What an Orderman is called* |
| No Man's Land (Sumendar) | frontier Talanese (plain English with drift), the tongue every arrival shares | given name kept + a fire-name bestowed by the cinder at the first Apprentice's Fire; the family name is burned | `glossary.md`, *No Man's Land → the Noman register*; `geography/sumendar/no-mans-land.md`, *What a Noman is called* |
| Tahu Tangata (Sumendar) | Reahi: Māori base, the Sumendar family's core; plain letters, long vowels unmarked; Talanese for the garners and the trade | given + house + first field: the field of one's first burn, shared by all who first danced it (burn-kin); a child has no field, a kinless dancer no house until one takes them in | `glossary.md`, *Tahu Tangata*; `geography/sumendar/tahu-tangata.md`, *What a Tangatan is called* |
| Namur Republic (Zuzental) | Italian, plain letters; Venetian family names lightly drifted | given + family + a sworn name from one's own citizen's oath (*detto/detta*), lost on oathbreaking; *Posaspada* after it for a Dictator who laid the office down | `glossary.md`, *Namur Republic → the Namurese register*; `geography/zuzental/namur-republic.md`, *What a Namurese is called* |

Regions without a row have no defined register yet; define one at the region's build, choosing a word-base inside the family *The families of Talan* gives the region, with sound rules of its own so it stays distinct from its kin, and a personal-name structure that no other region uses.

---

## Common culture

Practices that belong to a trade or a way of life rather than to a domain, and travel with the people who keep them.

### Overlade, the game of the quays

Every working waterfront on Talan plays **Overlade**, and nobody says the whole word. On the quay it is **Lade**: two players, a scratched grid, and a pocketful of flat discs.

The form is an answer to weather. The pieces are **bales**, discs of lead, bone, holystone, ballast-chip, or coin worn faceless, cut wide and low and heavy enough to sit still in a blow. Inland taverns play with tall carved figures and painted cards, and any quay in a wind delivers those to the harbour. The board is dock furniture: cut into a bollard cap, burned into a hatch cover, chalked onto a mooring block, gone glossy under generations of thumbs. A docker owns bales and borrows boards.

Play is loading. Moving onto an opposing bale takes it *under* yours rather than off the board, so a capture is cargo picked up and a stack in play is a **lift**. A lift moves as many squares as it stands tall, which makes a heavy lift the fastest thing on the board, and a lift walked to the far edge is **landed**, its whole load counted to the player who carried it.

The counterweight is **the mark**, the height a lift may stand before it is loaded past safety. Most ports set the mark at four. A lift over the mark can no longer be taken; it is **spilled**. An opposing bale moves onto it, the stack scatters to the squares around it, and every bale that goes off the edge leaves the game for both players, in the water. The strongest position on the board is the only fragile one, and most of any match is one player trying to walk a fat lift the last three squares to the edge while the other works out where to hit it.

On an open quay the wind spills lifts on its own, and the convention at every port is that a spill counts however it came. Players pick which side of a bollard to sit on the way a duelist picks ground, and a docker who loses four bales to a gust is told he loaded them.

Ports disagree about the rest. The mark stands at five along the Breidey arm and at three at some of the Hafra fishing stations; some boards hold that a bale in the water is salvage for whoever fishes it out, some that wagers ride on landed bales only, some that the loser owes the next round. Every port also claims the game, and none can produce the older board, because the boards that would settle it are cut into furniture that gets replaced.

The vocabulary has walked inland. *Over the mark* is said of any overreach, *carrying five* of someone whose ambition has outgrown their footing, *he landed it* of a thing brought off against the odds, and *that one went in the water* of a loss nobody is getting back; all four are heard in counting-houses and barrack rooms a long way from salt.
