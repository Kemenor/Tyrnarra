# Site Inventory

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

A description of what is currently published, organised by section. For repo conventions and folder layout, see [`../CLAUDE.md`](../CLAUDE.md). For sidebar architecture, see [`sidebar-nav.md`](sidebar-nav.md). For forward work — what needs writing, fleshing out, or publishing next — see [`open-threads.md`](open-threads.md).

---

## Lore files (`/lore/` — not published)

The canon source of truth. **When the pre-read rule in [`../CLAUDE.md`](../CLAUDE.md) says read the file, read it end-to-end — not just grep.** Sizes are approximate.

- **`cosmology.md`** *(~36 KB)* — How the world works. Tyrnarra/Cloud Sea/sun and two moons. Divine power tiers (Grand · Major · Minor · Demi). Gods' Law (scope, enforcement on Life Layer via Ethereal, tier-by-tier binding). Wellspring + belief mechanic, the post-Crimson-Rain leak / Lost-Era window / Stillpools / Reflections. Mortal Ascent Ladder (4 rungs, shards, the integration procedure as choke-point). Four magic schools (Arcane · Occult · Primal · Divine). Magitech (4 sub-traditions, regional producers, transport tiers — land/water/sky/Cloud Sea). Magitrains + Train Pirates + Conductor's Station. Planar structure (3 layers, 9 planes, Astral). Calendar (GR / MR).
- **`gods.md`** *(~24 KB)* — Who the gods are. The 13 Grand Gods (Primordial Six + Ascendant Six + Cronus): per-god sheets with aspects, domains, favoured weapon, magic school, city-state, worshipper base. Named Non-Bound Gods (Bikiargi · Zaharsuge · Epairima · Betibizi). Council of Thirteen. Open Sun-god thread.
- **`secret-history.md`** *(~39 KB)* — What actually happened. **The Week of Crimson Rain — True Account** (Tani killed by Storveldi Denbora; eleven Grand Gods went to war; hundreds of gods participated; Cronus rallied survivors; Gods' Law forged at the end). Cronus's secret (mortal-ascended via Law-anchor mechanism). Storveldi Denbora (true identity, integration procedure originators). The Elden → Corrupted God (fusion with Devourer). Wardstones, Nine Generals. Tani and Araphel deep dives. **Read before drafting anything that touches Crimson Rain, the Gods' Law forging, or any pre-Lost-Era event.**
- **`geography.md`** *(~71 KB)* — Where things are. All 13 god domains with their characters. Sub-regions (kingdoms, geographic features, cultural enclaves, border territories). Settlement-level detail. The Three Seas (Midarra · Hafra · Cloud Sea). Other continents (Sortalde · Red Empire homeland · unmapped).
- **`factions.md`** *(~42 KB)* — Independent organisations. Adventurers' Guild (branches, rank ladder, the Bank, the Post, Lord Albrecht Lavisburg as Demi-God). Mercenary Guild. God Churches (umbrella). Order of Steam. Pirate Lords of the Twin Cities. Iron Tide / Menagerie (Red Empire). Remnants of Corruption.
- **`cultures.md`** *(~39 KB)* — Peoples, traditions, politics, craft, warfare. Noble-naming conventions. Regional culture detail (Tahu Tangata · Lautaran mercantile · Vindul storm-folk · etc.).
- **`bestiary.md`** *(~47 KB)* — Playable ancestries (PF2e Remaster). Versatile heritages (Nephilim, Reflection, elemental sparks, wood/metal planar lines, mortal-ancestry mixes). **250-year lifespan cap** (Talan-wide principle). Per-domain ancestry distribution. Bound-god touches that aren't bloodline-borne.
- **`bolverk.md`** *(~32 KB)* — The megacity in Abyss. Geography (partition, Tunsund, 4-stage flood cycle, neutral strip). Soul-claim mechanic (pre-tagged · untagged-evil · strong-untagged → Independent). Three factions (Vice Demons · Virtue Devils · Independents) + feudal-tithe model. Demon/Devil distinction (foundational vs. parasitic). Full Vice Demon entries for Drambur, Ofunda, Reidar; placeholders for Nirfel/Lostar/Veislur/Lethar. Canonical 14 Virtue Devil table (virtue + excess + deficiency). **Read before drafting any infernal seat, Bolverk geography, or soul-routing detail.**
- **`glossary.md`** *(~64 KB)* — All coined names + etymologies. Confirmed canonical examples. Already-in-world names that predate the rule (do not retrofit). The 13 Bound Gods. Vice Demon names. God domains. Sub-regions. Fenurran / Kitsune / Sortalde proper-noun registers. Faction proper nouns. Named Non-Bound Gods. Pre-Crimson-Rain civilisations. Folk-names for cosmic things. The Binding apparatus. Wellspring sites. **Always check before coining a new name — confirm the source language and drift step land before using the name anywhere else.**
- **`timeline.md`** *(~10 KB)* — Eras, historical events, dates. GR (Gods' Reign, backward-counted) and MR (Mortal Reign, forward-counted). Crimson Rain at 0 GR / 0 MR is the hinge point. Current year: 2532 MR.
- **`pf2e-notes.md`** *(~8 KB)* — System-side notes. PF2e Remaster reshuffle. Lore-implicit domain mapping. Bound-god touches that aren't bloodline-borne (cross-ref into bestiary). PF2e cleric domain candidate annotations.
- **`unplaced.md`** *(~0.4 KB)* — Catch-all for unrouted content. Usually empty.

---

## `/` — World-level (Style A · cosmic)

- **`index.html`** — World primer and cosmology landing. Three celestial bodies (Solyra, Veyru, Calune), Cloud Sea framing, the Wellspring, **Tyrnarra-as-totality framing** (everything Wellspring-born is part of it; other multiversal realities exist but are not Wellspring-fed and not reached by mortals here), planar structure (three layers, nine planes, the Astral connecting all), soul-layer composition, link-outs to the rest of the site.
- **`grand-gods.html`** — The 13 Bound Gods (Primordial Six + Ascendant Six + Cronus). Data-driven expandable cards: aspects, cleric domains, favoured weapon, mortal-view, nature, worship, depiction, GM note, and a `⚿ GM Secret` expandable per god (Cronus's secret is filled; the other twelve are canon-pending). Council of Thirteen note at the bottom.
- **`non-bound-gods.html`** — Beyond the Thirteen. Named Non-Bound Gods (Bikiargi · Zaharsuge · Epairima · Betibizi) with tier/plane pills, aspects, worshippers, etymology, and notes. **Bolverk** intro (the megacity in Abyss, partition, Tunsund, three factions, feudal-tithe model). **Vice Demons — the Seven**: named-holders table, full character entries for **Drambur** (Pride, with GM Secret on his former name), **Ofunda** (Envy, with GM Secret on the Justice Devil's unpaid mark), **Reidar** (Wrath — once the god *Atezar* of a destroyed frontier pantheon, with GM Secret on the banishment's dependency on the Gods' Law plus the Salute-of-the-Last-Door weakness), and **Lethar** (Sloth — Outer being from beyond the Wellspring, original holder of his seat, with GM Secret on his home cosmology's auto-cannibalism and the unintended-approach weakness), placeholder for the other three seats. **Virtue Devils — the Fourteen**: canonical fourteen virtues + excess/deficiency table, Muiral-retirement note, dual-extreme mechanic explained. Updated Demon/Devil distinction callout. Sun-god open-thread callout.
- **`magic.html`** — Magic & Faith. Four Schools (Arcane · Occult · Primal · Divine), the four Magitech sub-traditions (Arcanotech · Occultech · Divitech · Primotech) with relative commonness and chaos-region resilience, Magic in Daily Life by settlement scale, Belief and the Wellspring + `⚿ GM Secret` (Mortal Ascent Ladder, shard mechanic, integration procedure, Betibizi as original holder), Faith & the Gods. The former *Domains Outside the Thirteen* table has been consolidated onto `pf2e-registrar.html`; magic.html now carries a short cross-reference pointing readers there.
- **`pf2e-registrar.html`** — PF2e Registrar. Mechanical-reference page for crunchy Tyrnarra-to-PF2e mappings. Alphabetical master table of all 61 official PF2e cleric domains. **46 domains assigned to the Bound Thirteen** under a strict no-sharing rule (each domain to the one god whose aspects align most directly). **15 Open / canon-pending** — 13 awaiting a dedicated non-bound assignment pass focused on Vice Demons, Virtue Devils, Generals of Corruption, Betibizi, and the Corrupted God; 2 (Dragon, Moon) never formally assigned. Each Open row carries an inline candidate note (Vice Demon names landed for Pride/Wrath/Gluttony; Virtue Devil candidate generic for now). Cross-links to grand-gods, non-bound-gods, the-binding, and magic. Style A, starfield omitted for the administrative feel.

## `/talan/` — Continent-level (Style B · grounded)

- **`talan.html`** — Continent overview. Three Seas (Midarra, Hafra, Cloud Sea), Chains-Beneath callout, Shape-of-the-World framing, 13 domain cards, Continental Rail Network (Northern + Southern halves, the Basogur seam, the three crossings), Other Continents pointer (Sortalde, Red Empire, Unmapped).
- **`history.html`** — Eight eras with three-tier knowledge UI (era card + amber `◈ Popular Belief` + red `⚿ GM Secret`). Creation, Elden, Gods', Week of Crimson Rain, Lost, Golden, Dark + the Guild's Birth, Adventurer (current). The Storveldi Denbora, Reflections and the Stillpool mechanic, the Golden Emperor's Reflection arc, and the Dark Era mining-truth all live in the GM-tier expandables.
- **`the-binding.html`** — Wardstones + Nine Generals + War of Seals. The Seven Wardstones distributed across four sub-regions of Myrkono (Shadow Steppes, Itzasoa, Ilun Tasun, Myrria). The Nine Generals of Corruption (Ash-Binder defeated; eight active). `⚿ GM Secret` on what is actually bound (the Elden / Corrupted God identity, the Generals as fragments of the Elden mass).
- **`bestiary.html`** — Peoples & Heritages. Ancestry distribution table by domain, per-domain ancestry cards, "Without a Single Home" scatter-list, Sortalde pointer + six Tian Xia ancestries table, versatile heritages (divine-blood, Elemental Plane sparks, Wood & Metal planar lines, mortal-ancestry mixes, other lineages including Reflection with `⚿ GM Secret` toggle), "Four bound gods whose touch passes outside bloodline" callout, pointer to Non-Bound Gods & Beings.

## `/talan/the-binding/` — Nine Dungeons

- **`hollow-of-ten-thousand-threads.html`** — Vermin Queen's hive (Shadow Steppes). Four-card chamber geography (Web-Tunnels · Brood Pits · Silken Vaults · Throne), three threat cards (Endless Swarms · Corrupted Silk · Hive-Mind Influence), Vermin Queen section with Swarm-domain grant, blue Surki Counter callout, two seal-blocks (2524 eruption + standing-threat context), Open in Canon panel.

## `/talan/domains/` — Domain hub + the 13 god domains

- **`domains.html`** — Hub. 13 colour-coded cards linking to each domain.
- **`vindul/vindul.html`** — Vindul · Wind · Fisaya · Haizava
- **`lautara/lautara.html`** — Lautara · Commerce · Jianna · Merkavar
- **`myrkono/myrkono.html`** — Myrkono · Darkness · Araphel · Myrria
- **`floteyn/floteyn.html`** — Floteyn · Water · Shuun · Uravel · *Balaena Skywhale City* featured section
- **`sumendar/sumendar.html`** — Sumendar · Fire · Komo · Eldara
- **`lioaru/lioaru.html`** — Lioaru · Time · Tani · Denbora
- **`brauogi/brauogi.html`** — Brauogi · Earth · Sarrum · Lurrath
- **`ezkudon/ezkudon.html`** — Ezkudon · Knowledge · Enki · Thekkavar
- **`egulon/egulon.html`** — Egulon · Light · Iro · Ljosarn
- **`zuzental/zuzental.html`** — Zuzental · Law · Forseti · Lograth
- **`nashavel/nashavel.html`** — Nashavel · Chaos · Vesuna · Nahaskel
- **`ehizahar/ehizahar.html`** — Ehizahar · Hunt · Hinka · Veidrath
- **`askamira/askamira.html`** — Askamira · Freedom · Cronus · Frae City

## `/talan/domains/<domain>/` — Promoted sub-regions & settlements

- **`ehizahar/fenurra.html`** — Fenurra · the Flame-Source
- **`lautara/emarrea.html`** — Emarrea · the Kitsune Kingdom
- **`lautara/crossroads.html`** — Crossroads · Tri-Domain Nexus + Spider's Silk Inn
- **`lioaru/lost-kingdom.html`** — Lost Kingdom · the Blackened Lands (with the *Meat-on-a-Stick* amber Popular Belief)
- **`myrkono/myrria/myrria.html`** — Myrria · City of Second Chances (Faith of Many Faces section — three rites, sacred iconography, edicts/anathema)
- **`sumendar/order-of-steam/order-of-steam.html`** — Order of Steam · Industrial Kingdom-Guild Hybrid
- **`sumendar/order-of-steam/house-eisenhart.html`** — House Eisenhart · Highforge Lineage + *Stahlglanz*
- **`sumendar/dragons-reach.html`** — Dragon's Reach · Dragon Capital. Mid-Gods'-Era mothership wreckage, three-tier lifespan band (non-purist / purist / "the purest"), four purist-school cards, purist-vs-pragmatist position blocks, Order-of-Steam friction, Dragonet schism, amber Popular Belief on the buried alien truth.
- **`zuzental/thousand-kingdom.html`** — Thousand Kingdom · Forseti's Realm of Law. Dual-bloodline (elf long-horizon / human short-horizon) constitutional kingdom, four-card borderlands compass. Founding & History three-tier section fully populated: open-prose names Renauld Fyrstmond (the Old King, House Fyrst founder), Garaion the Conqueror (the Demon Demigod), Aelis Marien Fyrstgilt (the Nephilim Founding Queen who reclaimed House Fyrst); amber `◈ Popular Belief` on the Returning Blood prophecy + Nephilim-as-folk-confirmation; **four themed `⚿ GM Secret` boxes** (multi-secret Storveldi pattern): *Who Garaion Really Was* (Aldwin Mero + skill-and-fear ascension mechanism, distinct from Storveldi/Golden Emperor/Cronus routes), *The Forgery That Built the Queen* (Halver Konrad Trent + Iona Marthe Vesh, sixty-year operation, Nephilim heritage as the gift the generals could not have planned for), *The Lab, the Tent, and the Conqueror's Tomb* (two confessions, the lab-burning rescue of Iona, Halver buried as Garaion at the state funeral), *Quietbarrow, the Sealed Letter, and Forseti's Silence* (Aldwin's hunter-life, Alayah Mero, the twice-called sealed letter, Forseti's clergy explicitly not in the loop and the framework making that the right design). **Names and Houses** section sits between *The Two Bloodlines* and *Forseti's Law in Practice*: the noble-naming convention ([house prefix] + [ancestry suffix]), heir-prefix and mobility rules, bastard override, royal-elevation example (*Aelis Marien Vaughn → Aelis Marien Fyrstgilt*), full 17-entry suffix register table (Cinzel suffix column, italic example column), and the commoner three-name register with two-name reading.
- **`zuzental/emerald-isles.html`** — Emerald Isles · Three Main Isles + Bridgelands. Capital Oathmoore (Middle Isle), chronicler's by-names (Watchstone · Emerald's Eye · Lyteward Bough · Bridge-Pearls), Sortalde embassy landing point.
- **`zuzental/legea-empire.html`** — Legea Empire · Demigod Theocracy of the Divine Faith. Two-sided law-vs-law tension blocks (Faith vs. Forseti positions), missionary programme + Draconis marriage, Open in Canon panel listing the canon-pending details.

## `/talan/factions/` — Independent organisations

- **`factions.html`** — Taxonomy overview + four faction-category cards + Bandit Categories & Hazards (Train Pirates, Conductor's Station).
- **`adventurers-guild.html`** — Branch hierarchy (Branch Office → Guild Office → Guildhall → Kingshall → Godshall), rank ladder (Bronze → Starsteel), the Guild Bank and the Guild Post, Lord Albrecht Lavisburg (Demi-God of Order and Ethics by accumulated mortal belief), Seraphel Duskbane (Sovereign of Myrria's Godshall), Myrria's Godshall.
- **`mercenary-guild.html`** — Mercenary Guild (shadow, coin, no loyalty beyond the contract).
- **`god-churches.html`** — Umbrella entry for the 13 bound-god churches.
- **`remnants.html`** — Remnants of Corruption (threat-not-organisation, the Nine Generals frame).

## `/talan/historical/` — Fallen civilisations

- **`historical.html`** — Hub. Three civilisation cards, all linkified: Golden Empire, Storveldi Denbora, Elden.
- **`golden-empire.html`** — The Empire's institutional page. At-a-glance, the Empire's sweep, the Emperor (public face), the Empire's work (four cards: common law · roads · script · Automatons), the mining programme + the fall (side-by-side blocks), legacy. Popular Belief expandable + `⚿ GM Secret` (Emperor was a Reflection; Layer-2 pocket dimension; lower-single-digits know). Open in Canon panel.
- **`storveldi-denbora.html`** — The civilisation's player-facing chronicler page. Written in scholarly-debate voice — chroniclers don't know who the *"Old Race"* actually were. At-a-glance (identity contested, dates disputed, capital lost), *The Chronicle Controversy* (four-tradition cards: Elden Returned · Separate Mortal Civilisation · Sorcerer-Kings · the Storveldi Denbora Hypothesis), the God Killing Incident as folk-record, the Wound (the Lost Kingdom as the only physical evidence), the Azarketi Question (chroniclers' open scholarship, not the answer), legacy in the chronicle record. Amber `◈ Popular Belief` carries the folk-memory layer (the Old Race / Elden-conflation interchangeability). **Four themed `⚿ GM Secret` boxes** (Who They Actually Were · How a Grand God Was Killed · The Azarketi Truth · The Procedure Persists), each with reveal-pills + themed cards (claim-vs-truth, three-tier court, three fragment-locations) + italic codas. Chronicler-tier *Open in the Chronicle Record* panel preserves four chronicler-visible TBDs.
- **`elden.html`** — The civilisation's player-facing chronicler page. Style B, void-blue-grey accent. Open prose treats the Elden as Talan's most-asked unanswered mystery — three thousand years of dominance, vanished in a single day in 2945 GR with cities intact. Structure: At a Glance · The Era of Dominance (four topic cards: Continental Scale · Rail Mass Acceleration · Atmospheric Vessels · Industrial Magic) · The Greatest Achievement — The Androids (single highlighted callout) · The Vanishing · The Three Theories (three tradition cards: War with Gods · Fulfilled Purpose · Departure) · The Technological Inheritance (four cards: Arcanotech · Order of Steam · Continental Rail · Automaton Failure) · Legacy in the Chronicle Record. Amber `◈ Popular Belief` carries the folk-imagination layer (Ultra-High-Tech Civilisation, "they're coming back" rumours, Azarketi descent claims). **Three themed `⚿ GM Secret` boxes**, each with reveal-pills + three cards inside + italic coda: *Why They Vanished* (the war + Devourer-as-weapon + Wellspring ritual), *What Stopped Them* (the gods' improvised counter + fusion + permanent lock), *Where They Are Now* (the Corrupted God identity + 1321 MR breach + the binding holds, with six GM-tier open threads). Chronicler-tier *Open in the Chronicle Record* panel preserves six chronicler-visible TBDs.

## `/off-continent/` — Non-Talan continents & powers

- **`off-continent.html`** — Hub. Two continent cards (Sortalde, Red Empire) + Unmapped placeholder + Hafra-vs-Cloud-Sea crossing note.
- **`sortalde.html`** — Sortalde · *Tao Hua Yuan* · The Petal Continent. Seven-petal archipelago, Concord of Courts, six ancestral petals + central Heting seat, veil-mediated clerical theology, cloudship crossing to Emerald Isles, six Tian Xia ancestries.
- **`red-empire.html`** — The Red Empire — godless mortal-supremacist state. Crimson Emperor, Pyre Throne, social hierarchy, the Iron Tide (navy) and the Menagerie (war-mage / surgeon corps with Collectors operating on Talan).
