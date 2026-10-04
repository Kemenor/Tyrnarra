# Map TODO

Pending label work for the map art. The three views (terrain / regions / domains) live at `published/setting/assets/maps/` as full-size originals with `display/` and `thumbs/` variants; labels are baked into the art, so canon renames accumulate **here** until the maps are next edited. Any future build that renames or adds a mapped region should add a line to this file. After replacing an original, re-run `resize.mjs` / `resize.sh` (ImageMagick) to refresh the variants.

**2026-07-05 redraw:** the maps were redone and the whole first batch landed (Earth Realm → Greenward, Shadow Steppes → Izarelai, Denbora → Valreka, Ljorsan → Ljosarn, Thousand Kingdom singular, Hareaveldi typo, Azkamour → Haldmark, Sugeiturri and Bikitsa added, Gotorlekua confirmed gone). Verified against the new regions view.

## Awaiting export + variant regeneration

- **Harro Distiratsua map label: keep the *-a*.** Canon adopted the map's *-a* spelling on 2026-08-13 (the authentic Basque definite form; glossary and lore updated at the Harro Distiratsua build), reversing the 2026-07-05 map-source fix to *-tsue*. **Done 2026-09-25:** the map source label is back to "Harro Distiratsua" (`wdmap edit`), matching the published exports; the next regions-view re-export (pending for the Kaosadaemi fix) carries it too.

## Scale bar: halved in the source (GM, 2026-09-25)

**Done in the map source 2026-09-25:** the GM halved the bar. It now reads **0–1000 miles** over the same 2000 px (10 segments × 100 mi), so **1 full-res px = 0.5 mi**; units are still miles. **Confirmed as canon 2026-09-26** (`lore/geography/_continent.md`, *Scale*). **Done:** the views were re-exported and published with the new bar (2026-09-25), and the scale and speeds are recorded in `lore/geography/_continent.md`, *Scale*, and `lore/transport.md`, *Scale and speeds* (2026-09-26). The analysis that led here:

The scale bar (bottom-left of the terrain view) read **0–2000 miles**. On the 8192 px original, 1000 bar-miles span ~1000 px, so **1 px ≈ 1 mile** as labelled. At that label Talan runs ~7,000 mi west–east and ~7,500 mi north–south (NW coast to SE coast ~8,300 mi; island to island ~9,200 mi), the Midarra ~5,300 mi long, and the Basogur ~1,500 mi deep: larger than Asia.

Canon travel times want a map 6–8× smaller. The long road crosses the Basogur in 11 days on foot with sledges (165–275 mi at a hard 15–25 mi/day, against ~1,500 on the map); Rustam Varaz flies Merkavar to Sombral between noon and just after sunset (~8 h; ~425 mi at a plausible airship pace, against 3,000+ on the map). Both point to the bar's "2000" reading about **250–350 miles** (**~400–550 km**), which puts Talan at roughly 1,000–1,300 mi (1,700–2,100 km) across: Europe-sized. **Draft working scale (2026-09-25, GM to confirm):** halve the bar, so its "2000" reads **1000 miles** and 1 full-res px = 0.5 mi. Talan ~3,500 mi across (NW–SE coast ~4,000 mi / 6,400 km), the Midarra ~2,650 mi; checks and travel paces in `open-threads.md`, *Continental scale (draft)*. The GM plans to relabel the bar (and switch units); once settled, record the scale in `lore/geography/_continent.md` and derive Magitrain and airship figures from it (`lore/transport.md`, *Still open*).

## Capital icons without a name (2026-09-25)

The map's 37 capital icons (*Large City Stone Wall + Towers*, the Legend's "Capital"; it read "Capitol" until 2026-09-26) were checked against the lore. **Labelled 2026-09-25** (City Labels, `wdmap`): Brasswatch (Fellibylur), Vindboorg (Haizetsua), Botbar (Ilun Tasun), Izarbil (Izarelai), Ehunbaso (Itzasoa), Ringhold (Kaosadaemi), Oathmoore (Emerald Isles), Moonwatch (Dreaming Cape), Margolora (Lua Lasai), Sombral (Argia Esfera). Lograth already names the Thousand Kingdom's.

**GM decisions (2026-09-25), applied:** Hverhofn (Ardo Beroa's town, far-north icon), Cold-Hall (Baerfrost, provisional name), Hartzar Erruta (Air Monastery), Ontzola (Three Pines) labelled. The capital icons of the Floating Isles of Shuun (no capital), Haldmark (no capital by design) and Atarialda (no capital by design; Crossroads is a separate city with its own icon) were removed.

**No capital in canon yet** (name at the build): Dea Elurra, Maitagarri, Basamortua (Askamira), Order of Steam, Burdineyja, Haraour Eliza, The Red Dominion (Sumendar), Lost Isle, River Duchies, Hareaveldi (Lioaru), The Golden Coast (Ezkudon).

## Awaiting the next export

Nothing pending: the 2026-09-26 exports carried everything so far (last: the Lautara god label corrected to its canon spelling; Merkavar's separate domain circle removed, it is only a region now).

- **Star Island capital**: its capital icon has no city name yet; name it at the Star Island build (the check accepts the region label on the icon as a name, as for Rika Tikur, so it no longer flags this).

## Backlog for the next map edit

- **The rock mountains of Galdua Jendea** (Lioaru; GM, 2026-10-04, sited at the build's Phase 4). Draw **nineteen rock massifs** rising out of the dune sea, each about **10–40 miles across** (20–80 px on the full-res map): **17 living rocks** with cities hung on their shaded faces, and **2 lost rocks**. Every rock lies within one night's sand-glider run (~150 mi, 300 px) of a neighbour, so the chain reaches every edge. Reference sketch: [`map-refs/galdua-jendea-rocks.webp`](map-refs/galdua-jendea-rocks.webp) (regions view, 1 px there ≈ 1 mile; brown = living, grey = lost; the red lines are the night-runs, not roads to draw). Approximate centres on the full-res map; place the exact massifs by eye:

  | Rock | Centre (x, y) | Note |
  |---|---|---|
  | 1 | 2140, 5890 | north-west, below the badland ridge |
  | 2 | 2390, 5830 | north |
  | 3 | 2730, 5980 | north-east, the great-river landing (Tahu Tangata) |
  | 4 | 3060, 6220 | east, the Emarrea corner |
  | 5 | 2890, 6440 | east, facing Hareaveldi's river |
  | 6 | 2670, 6620 | south-east, toward the Duchies |
  | 7 | 2400, 6960 | south, near the short south shore |
  | 8 | 2150, 6780 | south-west, the frontier against the pale band |
  | 9 | 1870, 6540 | west coast |
  | 10 | 1900, 6210 | west coast |
  | 11 | 2210, 6060 | inner north-west |
  | 12 | 2530, 6160 | centre-north |
  | 13 | 2350, 6400 | **the great rock**, largest massif, beside Valreka's icon (keep clear of the icon at ~2450, 6400) |
  | 14 | 2730, 6280 | centre-east |
  | 15 | 2070, 6440 | centre-west |
  | 16 | 2390, 6680 | centre-south |
  | 17 | 2550, 5900 | north, among the north dune field |
  | 18 *(lost)* | 1950, 6820 | in the pale band against the Blackened Lands; the frontier rock |
  | 19 *(lost)* | 1980, 6050 | north-west gap; the dead spring |

  **Labels** (named at the build, 2026-10-04): 13 **Yemmazru** (the capital: give it a capital icon), 4 **Tamalut**, 3 **Saltlanden**, 8 **Tassast**, 18 **Tazrut**, 19 **Taghbalut**; the other eleven await names (`docs/deepening-ideas.md`). The region label stays **Galdua Jendea**.

- **Vardana, Ida, the Mugarri** (the Lost Kingdom, Lioaru; named at the 2026-10-05 build). Label the ruined-city icon (~1792, 7095) **Vardana**. Add a capital icon on the south coast at about (2050, 7255) and label it **Ida**, the city of the cursed-born. Optionally mark **the Mugarri** as a ring of standing stones around Vardana. The Dakhma lies under Vardana and needs no mark.

- **Repaint the Lost Isle** (Lioaru; GM, 2026-10-02). The island is painted black on the map for no reason canon gives; repaint it as ordinary island ground with **three volcanic peaks**, each with a crater lake, and **a port** on the coast (the seed, the three rains, is in `docs/pencilled/seed-bank.md`; the coast the port faces is open until the build).

- **Ahika, Tihiwera** (Tahu Tangata, Sumendar; named at the 2026-10-02 build). Label the capital icon at the centre of the plain (~3134, 5766) **Ahika** (the rail maps' **Garnerstow**). Label the pale spire on the southern edge by Emarrea (~3360, 5900) **Tihiwera**.

- **Portoferma, the Sickwell** (Namur Republic, Zuzental; named at the 2026-09-30 build). Label the capital icon at the river-mouth on the coast (~5550, 4860) **Portoferma**; add or label **the Sickwell**, the Blight-Seer's sealed gate, in the south-western hills (the small mountain group near the coast).

- **The Neck, the Cold Furnace** (No Man's Land, Sumendar; named at the 2026-09-29 build). Label **the Neck**, the single-track rail valley where Eldara's line crosses the No Man's Land / Tahu Tangata line (the mountain gap between the Order of Steam's ridge and the border range); label **the Cold Furnace**, the Ash-Binder's dead lair, in the south-eastern badlands (the brown ridges). Consider rush-camp icons around the Furnace.

- **Drukha, the Ankerhold, Kyrrskog** (Order of Law, Zuzental; named at the 2026-09-29 build). Label the capital icon on the river mouth (~6815, 5346) **Drukha** (City Labels); label the cathedral icon in the central forest (~6786, 4978) **the Ankerhold**; consider a terrain label **Kyrrskog** on the forest itself. The lore adds farm country and heath in the north, steppe in the south-west, river valleys and hill country between (below map resolution, per the landmarks rule).

- **Debreqal and the Orratzak** (Legea Empire, Zuzental; named at the 2026-09-29 region pass). Label the Legea capital icon (~5934, 4766) **Debreqal** (City Labels); consider a small terrain label **Orratzak** on the three needle peaks west of it (~5800–5890, 4710–4790), where the cathedral icon (~5825, 4668) is the high reading-house. The keep on Legea's half of Hringseyja stays unnamed until its build.

**From the geography audit (GM rulings 2026-09-28; details in [`geo-audit-2026-09-28.md`](geo-audit-2026-09-28.md)):**
- **Haizava** (Vindul, D1). Move the god-city's mark from open Baerfrost (~3085, 920) onto the great river's bend (~3100, 1210): the lore puts it on the river that runs the Baerfrost/Fellibylur border, the Eye anchored at the bend. The Air Monastery then lies to its north-east.
- **Brasswatch** (Vindul, D2). Move the Fellibylur port-capital's mark from the inland lake (~2390, 1131) to the Hafra coast; canon calls it a Hafra port with the Saltkeep in its port-archive.
- **Helgafjall** (Lautara, D10). Move the white peak from the lake's north shore (~4569, 5838) into the centre of Merkavar's lake; the lore has it rise from the lake's centre with the city ringed by water.
- **Kaosadaemi** (Nashavel, D13). Pull the Kaosadaemi/Vernua region line down to the Hegandi escarpment, so no strip of Vernua runs between Kaosadaemi and the escarpment (the Thousand Kingdom lies directly below it; the southern rail climbs the Hegandi to Ringhold).
- **Izarbil** (Myrkono, D14). Move the lake-city's mark from the foot of the eastern ridge (~2295, 3209) to the shore of lake Izaru (~1995–2095, 3080–3190).
- **Sumendar volcanoes** (D19). Add active volcanoes in the west (the Red Dominion) once volcano sprites exist; the lore's "cluster of active volcanoes to the west" has no art yet.
- **Muino-saila** (Lautara, D18). Cut two or three gaps into the unbroken coastal ridge along Itsasalda's Midarra shore (x ~4380–4960); the lore's port-towns sit in the gaps.
- **Ljosarn** (Egulon, D15). Move the god-city's icon and label from Vonura's west shore to its east shore, on the Harro/Argia line: the lore has Harro's railhead on the near shore facing the city across the lake, and the Lamp Ride ending at Sidijos with Ljosarn burning across the water.
- **Gesalkai** (Floteyn, D20). At the Balatur Erui shift below, place Gesalkai on the island's western shore, on the Gazmuga, so its salt front faces the Hafra and its sweet front the Midarra.

- **More region fixes (2026-09-25, `wdmap`):** region shapes added for Ardo Beroa (from its Ehizahar outline, #7fb3d5) and the south-east Lua Lasai island (Lua Lasai's colour); Balatur Erui's region recoloured from near-sea indigo to #8a5cf0 so it shows; the outlines of Namur Republic, No Man's Land and The Golden Coast each had a knot at their closing point (Wonderdraft's "Convex partition failed", unfilled regions) and lost that one point. The small Lautara outline at (4461–4668, 5840–6011) is Merkavar's circle (its lake and mountain belong to the god-city): it got a Merkavar region shape (#d4a017), like Myrria's circle; its own domain circle was removed on 2026-09-26.
- **Region shapes and label fixes (2026-09-25, `wdmap`):** the Emerald Isles (4 islands), Rika Tikur and Lost Isle had only god-domain outlines; region shapes were added by copying those outlines (colours emerald #2e8b57, #b5651d, #708090; recolour freely). Their domain outlines were near-miss colours; now recoloured to their domains (GM): Emerald Isles → Zuzental, Rika Tikur → Lautara. The last two unnamed domain outlines were resolved (GM): Soul Tree's was a stray duplicate of its Brauogi outline and was removed; the circle around Myrria became a region shape (Myrria's own circle on the regions view; Myrkono's domain covers it on the domains view). Nahaskel moved from Region Labels to Divine City Labels; "FraeCity" corrected to **Frae City** and moved below its icon; Askamira moved up off the Frae City icon. All three views need a re-export.
- **Kaosadaemi Principality label typo** (Nashavel; found 2026-09-25 by the `wdmap` preview). The Region Labels (+2) label read **"Kaosadaemi Prinicpality"**; canon is **Kaosadaemi Principality** (`nashavel/kaosadaemi.md`). **Source fixed 2026-09-25** (`wdmap edit`) and the variants regenerated; **still to do: re-export and publish the regions view** (`tools/wonderdraft/README.md`, *Publishing the three map views*).

- **Basogur: pull the top-right down** (Nashavel/Ehizahar; draft, 2026-09-25). At the draft scale the long road runs ~525–785 mi from Greenmouth to Veidrath, far past what walking parties with sledges cover in the log's 11 days. Pull the jungle's north-east lobe (the top right, where Veidrath stands) lower, so the road's line through the trees is roughly **600–700 px** on the full-res original (**~300–350 mi**), with the crossing lengthened lightly to match (target to confirm with the GM). Coordinate with the *Veidrath move* below, and with Zenerious's Skoga leg, whose "peak of the bend" is that lobe.

- **Tvisol** (Brauogi/Myrkono corner). The Twin Suns + Bikitsa joint kingdom now carries the canon name **Tvisol** (2026-07-06 build); consider a regions-view label for it, keeping the two half-labels. **Label added 2026-09-25** (Region Labels, smaller than the half-labels, on the shared border; `wdmap add`); goes out with the next regions-view export. Still optional: settlement marks **Solkai** (sunward ferry-capital) and **Gaulabe** (shade-half oven-town).
- **Balatur Erui** (Floteyn). The 2026-08-10 build places the island *on* the Hafra/Midarra boundary: shift the island (or the sea-boundary art) so the salt/sweet line (**Gazmuga**) touches its western shore. The settlement mark on the south coast is canon-named **Gesalkai** (**label added 2026-09-25** above the south-coast city, City Labels); the central mountain is **Lomendi** (**label added 2026-09-25** beside the island's mountain group, on layer −2, the new landmark-label layer, size 24). Optional: mark the **Riseway** on no view (it is a sky-lane; charts carry it, terrain art should not).
- **Jakinduria rework** (Ezkudon). The map shows Jakinduria as a **ring of forest**, open in two places, with **mountains only on its northern edge**, Jakinduria's own capital beneath them, and **Thekkavar alone in the open middle**. The lore says otherwise: `ezkudon.md` has "central mountains … the natural fortress the whole domain shelters behind", and `egulon/lua-lasai.md` has "the fortress-ring". Settle which is true at the Jakinduria build, then redraw to match. Add the missing rivers at the same pass. The airship route in Rustam Varaz's letter (`egulon/argia-esfera-letter.md`) already follows the map's version: ships skirt the northern mountains and see Thekkavar in its forest ring. See `open-threads.md`, *Jakinduria*.
- **Veidrath move** (Ehizahar). The Basogur build sites Hinka's god-city at the **northeast edge of the Basogur Jungle**, with the lake **Aintzir** just inside the trees (`ehizahar.md`, *Basogur Jungle*; `nashavel/basogur.md`). Move the city mark to that edge and draw **Aintzir**. Optional: a mark for the long road's northern gate, held by the Oihandar Red Tusks.
- **Fenurra draw-in** (Ehizahar). Draw Fenurra in as its own sub-region in the **northeast of Ehizahar, in the snow lands**, beside the Lands of Villtur (Villtur is "the whole domain outside Fenurra", map-authoritative, 2026-08-30). Mark the **Scar of Aeris** (the meteor crater) with **Aeris**, the capital carved into its inner walls, and add volcanic terrain around it: basalt fields, fume vents and slow lava flows (`ehizahar/fenurra.md`). Mark its **single warm port** on the coast. The port is on the mainland: keep it distinct from Hverhofn, the warm harbour on Urbero in the Ardo Beroa isles offshore.
