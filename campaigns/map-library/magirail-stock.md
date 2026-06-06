# Magirail Rolling Stock — Map Library

A reusable catalogue of modular train-car battlemaps for any magirail scene on Talan. Source art is Tom Cartos's **"Steam Train" (ST)** modular set: 36 numbered cars, "Clean" (ungrimed) variants, roof tiles, plus prop overlays and seamless terrain backgrounds. Every car is a uniform **14 × 5 grid**, so consists line up tile-to-tile with no fiddling.

This catalogue is the part that travels in the repo. The **art itself is subscription/licensed and local-only**: it lives (gitignored) under `campaigns/map-library/_full/trains/`, synced between machines via the user's private Proton Drive (restore steps in [`README.md`](README.md)). The descriptions below let Claude pick cars for a scene without the images being committed.

## How to use it

1. Tell Claude the scene (a freight robbery, a luxury express heist, a prison-train break). Claude reads this catalogue and proposes a **consist**: an ordered list of cars front-to-rear.
2. **Claude runs `stitch.py`** to assemble the consist: it appends the cars over the chosen terrain background, writes the full-res composite (local in `_full/`) plus a downsized web copy, and builds the merged `*.areas.json`. Any car with a per-car area file in `areas/` (see below) has its interior hotspots offset into place; cars without one get a single whole-car area. Pass `--verify` for an overlay check.
3. You load the composite in `campaigns/tools/map-area-editor.html`, draw one area per car, and export the JSON (the quest-workflow Phase 3 handoff).

**Variants.** Most common cars also ship a **Clean** version (less grime/blood; same layout) for a freshly-built or higher-class train. Four **roof tiles** (`TC_ST Roof 01–04`) give the over-the-top traversal layer for running fights. **Prop overlays** (`Luggage and Cargo/`: crates, barrels, parcels, suitcases) dress any car; the **seamless backgrounds** (five terrains, day/night) tile the ground under an assembled consist (see *Seamless backgrounds & track* below).

**Per-car detail areas (optional).** Draw a car's interior once on the bare 14 × 5 car image in `map-area-editor.html` (benches, compartments, the strongroom) and save the export to `areas/<car filename>.areas.json` (committed: it is coordinates, not art). Every consist `stitch.py` builds then auto-inherits those hotspots, offset into the car's slot, with no redrawing; a car without a detail file falls back to one whole-car area. Detailing is incremental, so do the set-piece cars and skip the cargo hoppers.

A car can also carry a finer **variant** named `areas/<car filename>.areas.<variant>.json` (e.g. `.detailed`, marking every bench). The base file is the default; opt one car of a consist into its variant with a `token:variant` suffix, for example `14 Steerage:detailed`. Keep the base **coarse** (a few meaningful zones) for the clickable page and reserve a per-feature variant for when you want exact token or NPC placement (a VTT run, a set-piece car). NPC identities stay at the quest layer; the car file only gives generic structure.

---

## The roster

Tags: `motive` `crew` `service` `passenger` `cargo` `military` `grim` `roof` `background` · `enclosed` (roofed interior) · `open-top` (no roof, exposed deck).

### Motive & crew
- **01 Engine** `motive` `open-top` — The locomotive: red cowcatcher and plow at the nose, boiler banded with pressure valves and gauges, the driver's cab, the firebox and footplate at the rear coupling. The front of every train and the natural home of a sabotage/clock beat.
- **01 Engine Roof** `motive` `open-top` — The engine's top plate with a hatch; pair with the roof tiles for a fight that runs forward over the boiler.
- **02 Crew Quarters** `crew` `enclosed` — Bunks with beds, a chart/work table, lockers, toilet, washroom. Where the off-shift crew sleep.
- **03 Crew Quarters** `crew` `enclosed` — Bunks with hammocks, a small table, storage, kitchen, toilet, washroom. A second crew-car layout; good as a caboose/brakeman's car at the rear.

### Service & dining
- **06 Dining** `service` `enclosed` — Upper and lower side of the car filled with rows of tables and red banquette seating, in the middle a central aisle. Lots of cover, lots of bystanders. Toilets at one end.
- **07 Lounge** `service` `enclosed` — Plush red sofas, armchairs, low tables. A relaxed social car, toilets at right end.
- **08 Bar** `service` `enclosed` — A long bar counter with bottles and stools, booth seating. The saloon car; pure Western.
- **16 Cafe** `service` `enclosed` — Pale-wood cafe tables and chairs, a service counter for bar food, café and beer. Casual, lighter than the Dining car. Contains two storage rooms.
- **17 Kitchen** `service` `enclosed` — Galley counters, a stove/range, prep tables, hanging storage. Tight quarters, knives and fire to hand, two storage rooms.

### Passenger
- **04 Premium** `passenger` `enclosed` — Wood-panelled bays of bench seats, windowed and comfortable.
- **05 Premium** `passenger` `enclosed` — A second premium-seating layout, each bay containing two benches and a table in the middle.
- **09 VIP** `passenger` `enclosed` — Opulent: red carpet, ornate sofas, a central table, gilt trim. The car a wealthy mark rides in.
- **10 Private** `passenger` `enclosed` — A side corridor off private compartments (lounges behind doors).
- **11 Sleeper Premium** `passenger` `enclosed` — A corridor of five walled sleeping compartments with a bed, a desk, a chair and a chest in each compartment.
- **12 First Class** `passenger` `enclosed` — Enclosed two compartments of highest living standard a train can offer, true VIP experience. Each compartment has a double bed, nightstands, a couch with a low table, a private bathroom. Two chairs outside in the hallway for bodyguards.
- **13 First Class** `passenger` `enclosed` — Enclosed two compartments of second best living standard. Each room contains two single beds, a couch with a low table, a desk with a chair, a private bathroom. Two chairs outside in the hallway for bodyguards.
- **14 Steerage** `passenger` `enclosed` — Wood benches in two rows, red cushions. Cheap but not cheapest. Eleven benches per row, two rows in the middle the aisle. 44 Seats total.
- **15 Steerage** `passenger` `enclosed` — The true cheap option, wooden benches no cushioning, 44 Seats.
- **18 Sleeper Basic** `passenger` `enclosed` — 10 sleeping compartments with basic beds, four shared toilets.
- **19 Sleeper Hammock** `passenger` `enclosed` — 10 sleeping hammocks, four shared toilets; the cheapest sleep on the line.

### Cargo & baggage
- **20 Luggage** `cargo` `enclosed` — Loose stacks of crates, barrels and sacks with piled luggage on an open floor.
- **21 Luggage** `cargo` `enclosed` — Wall racks and shelving stacked with trunks and parcels; an organised baggage car.
- **26 Artefacts** `cargo` `enclosed` — A near-empty floor with a single featured/crated object centred, chained to the walls. Built to haul **one special thing**; The obvious, carrying very special cargo wagon.
- **27 Cargo Crates** `cargo` `enclosed` — Stacked crates, barrels and boxes with some dunnage; general freight and good cover.
- **28 Cargo Coal** `cargo` `open-top` — An open hopper heaped with black coal. The natural tender behind the engine.
- **29 Cargo Gold Ore** `cargo` `open-top` — An open hopper heaped with gold ore; a high-value haul.
- **30 Cargo Purple Crystal** `cargo` `open-top` — An open hopper of raw purple crystal. Reads as arcane/Magitech cargo (Eldaran "almosts", Wellspring material).
- **31 Cargo Turquoise Crystal** `cargo` `open-top` — An open hopper of teal crystal; a second arcane-cargo colourway.
- **32 Cargo Logs** `cargo` `open-top` — An open gondola of stacked timber.

### Military
- **22 Ballista** `military` `open-top` — An open weapons deck with four mounted ballistae per side and bolt racks.
- **23 Cannons** `military` `open-top` — An open car with four mounted cannons on each side and shot racks. Usable. Defensive.
- **24 Military Transport** `military` `enclosed` — An armoured car with two storage rooms for weaponry, two benches for people and a table to discuss strategy, weapon rack in the middle and on some walls. If you need to transport troops.
- **25 Military Bunk** `military` `enclosed` — Sleeping for troops, ten hammocks, no walls, two storage rooms for equipment.

### Grim & captivity
- **33 Prison** `grim` `enclosed` — Barred cells down the car with a guard space. Prisoner transport.
- **34 Prison Skeletons** `grim` `enclosed` — The same cell layout with skeletal remains; a horror dressing for an abandoned or massacred train.
- **35 Stables** `grim` `enclosed` — Stalls with horses, hay and tack. Mount/livestock transport.
- **36 Cages** `grim` `enclosed` — Beast cages down the car for creature (or "creature") transport.


### Roofing
- **01 Roof** `roof` simple roof with no roof windows
- **02 Roof** `roof` roof with a row of small roof windows wide enough to peek in
- **03 Roof** `roof` roof with two windows wide enough to get in and one hatch
- **04 Roof** `roof` simple alternative roof

### Seamless backgrounds & track
The ground a consist sits on. Each background is a **14 × 7** tile: the train is 14 × 5, so the background leaves one square of terrain along each side of the cars for moving outside and around the train, and it tiles seamlessly end-to-end down the consist. Pick one terrain to match the scene; each comes in **day and night**, and in **gridded / ungridded** copies (use the *No Grid* copy under a stitched composite).

- **01 Grass** `background` — open green plains and meadow trackside; the default countryside line.
- **02 Snow** `background` — snowfield and frozen ground; for Baerfrost and the northern routes.
- **03 Urban** `background` — paved station platform and city siding; the in-town stop or rail yard.
- **04 Rock** `background` — bare rock and stone; canyon cuts and the volcanic shoulder (the Narrows).
- **05 Desert** `background` — sand and dry steppe; the southern badlands.
- **Train Tracks** (`TC_Train Tracks_14x3`) — a standalone 14 × 3 rail strip to extend track past a background's edge or bridge a gap between tiles.

*Variant note: Grass ships day, night, and gridded-day but no gridded-night; the other four terrains have all four copies.*

---

## Ready-made consists

Front (engine) to rear. Mix in roof tiles for an over-the-top layer.

- **Freight robbery (the Narrows Job pattern).** `01 Engine` → `28 Cargo Coal` (tender) → `24 Military Transport` (the strongbox + the featured crate) → `12 First Class` or `14 Steerage` (passengers/guards) → `27 Cargo Crates` or `23 Cannons` (freight flat) → `03 Crew Quarters` (rear/brakeman). Swap the marquee crate car for `26 Artefacts` if the prize is one object.
- **Luxury express (heist / social caper).** `01 Engine` → `02 Crew Quarters` → `13 First Class` → `09 VIP` → `06 Dining` → `08 Bar` → `11 Sleeper Premium`. A mark, a manifest, and a lot of bystanders.
- **Prison train (rescue / break-out).** `01 Engine` → `25 Military Bunk` (the guards) → `33 Prison` → `36 Cages` → `24 Military Transport` (the warden's strongroom). Use `34 Prison Skeletons` if the party arrives to a massacre.
- **Treasure freight (high-value haul).** `01 Engine` → `28 Cargo Coal` → `29 Cargo Gold Ore` / `30 Cargo Purple Crystal` → `26 Artefacts` → `24 Military Transport`. The richest train on the Southern network and the most-hunted.
