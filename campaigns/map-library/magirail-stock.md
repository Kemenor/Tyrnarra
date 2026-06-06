# Magirail Rolling Stock — Map Library

A reusable catalogue of modular train-car battlemaps for any magirail scene on Talan. Source art is Tom Cartos's **"Steam Train" (ST)** modular set: 36 numbered cars, "Clean" (ungrimed) variants, roof tiles, plus prop overlays and a seamless track background. Every car is a uniform **14 × 5 grid**, so consists line up tile-to-tile with no fiddling.

This catalogue is the part that travels in the repo. The **art itself is subscription/licensed and local-only**: it lives (gitignored) under `campaigns/map-library/_full/trains/`, re-downloadable from Tom Cartos onto any machine. The descriptions below let Claude pick cars for a scene without the images being committed.

## How to use it

1. Tell Claude the scene (a freight robbery, a luxury express heist, a prison-train break). Claude reads this catalogue and proposes a **consist**: an ordered list of cars front-to-rear.
2. **Claude stitches the chosen cars into one composite image** with ImageMagick (the cars append left-to-right over the track background; the 14 × 5 grid makes the seams clean), then downsizes it to the committed ~800px web copy the quest page references. The full-res composite stays in `_full/`.
3. You load the composite in `campaigns/tools/map-area-editor.html`, draw one area per car, and export the JSON (the quest-workflow Phase 3 handoff).

**Variants.** Most common cars also ship a **Clean** version (less grime/blood; same layout) for a freshly-built or higher-class train. Four **roof tiles** (`TC_ST Roof 01–04`) give the over-the-top traversal layer for running fights. **Prop overlays** (`Luggage and Cargo/`: crates, barrels, parcels, suitcases) dress any car; the **seamless background** tiles the track and ground under an assembled consist.

---

## The roster

Tags: `motive` `crew` `service` `passenger` `cargo` `military` `grim` `flex` · `enclosed` (roofed interior) · `open-top` (no roof, exposed deck).

### Motive & crew
- **01 Engine** `motive` `open-top` — The locomotive: red cowcatcher and plow at the nose, boiler banded with pressure valves and gauges, the driver's cab, the firebox and footplate at the rear coupling. The front of every train and the natural home of a sabotage/clock beat.
- **01 Engine Roof** `motive` `open-top` — The engine's top plate with a hatch; pair with the roof tiles for a fight that runs forward over the boiler.
- **02 Crew Quarters** `crew` `enclosed` — Bunks, a chart/work table, lockers. Where the off-shift crew sleep.
- **03 Crew Quarters** `crew` `enclosed` — Side bunks, a small table, storage. A second crew-car layout; good as a caboose/brakeman's car at the rear.

### Service & dining
- **06 Dining** `service` `enclosed` — Two long rows of white-clothed tables with red banquette seating down a central aisle. Lots of cover, lots of bystanders.
- **07 Lounge** `service` `enclosed` — Plush red sofas, armchairs, low tables. A relaxed social car.
- **08 Bar** `service` `enclosed` — A long bar counter with bottles and stools, booth seating. The saloon car; pure Western.
- **16 Cafe** `service` `enclosed` — Pale-wood cafe tables and chairs, a service counter. Casual, lighter than the Dining car.
- **17 Kitchen** `service` `enclosed` — Galley counters, a stove/range, prep tables, hanging storage. Tight quarters, knives and fire to hand.

### Passenger
- **04 Premium** `passenger` `enclosed` — Wood-panelled bays of bench seats, windowed and comfortable.
- **05 Premium** `passenger` `enclosed` — A second premium-seating layout.
- **09 VIP** `passenger` `enclosed` — Opulent: red carpet, ornate sofas, a central table, gilt trim. The car a wealthy mark rides in.
- **10 Private** `passenger` `enclosed` — A side corridor off private compartments (beds/lounges behind doors).
- **11 Sleeper Premium** `passenger` `enclosed` — A corridor of walled sleeping compartments with made beds.
- **12 First Class** `passenger` `enclosed` — Enclosed compartments of facing bench seats off a side corridor (the classic first-class car); each compartment is a little room to clear.
- **13 First Class** `passenger` `enclosed` — An open saloon of individual upholstered seats in rows.
- **14 Steerage** `passenger` `enclosed` — Plain wood benches in rows, minimal trim. The cheap seats.
- **15 Steerage** `passenger` `enclosed` — An open car with simple perimeter benches and standing room; packs a crowd.
- **18 Sleeper Basic** `passenger` `enclosed` — Rows of plain stacked berths.
- **19 Sleeper Hammock** `passenger` `enclosed` — Slung hammocks in an open car; the cheapest sleep on the line.

### Cargo & baggage
- **20 Luggage** `cargo` `enclosed` — Loose stacks of crates, barrels and sacks with piled luggage on an open floor.
- **21 Luggage** `cargo` `enclosed` — Wall racks and shelving stacked with trunks and parcels; an organised baggage car.
- **26 Artefacts** `cargo` `enclosed` — A near-empty floor with a single featured/crated object centred. Built to haul **one special thing**; the obvious "the bandits want this crate" car.
- **27 Cargo Crates** `cargo` `enclosed` — Stacked crates, barrels and boxes with some dunnage; general freight and good cover.
- **28 Cargo Coal** `cargo` `open-top` — An open hopper heaped with black coal. The natural tender behind the engine.
- **29 Cargo Gold Ore** `cargo` `open-top` — An open hopper heaped with gold ore; a high-value haul.
- **30 Cargo Purple Crystal** `cargo` `open-top` — An open hopper of raw purple crystal. Reads as arcane/Magitech cargo (Eldaran "almosts", Wellspring material).
- **31 Cargo Turquoise Crystal** `cargo` `open-top` — An open hopper of teal crystal; a second arcane-cargo colourway.
- **32 Cargo Logs** `cargo` `open-top` — An open gondola of stacked timber.

### Military
- **22 Ballista** `military` `open-top` — An open weapons deck with corner-mounted ballistae and bolt racks.
- **23 Cannons** `military` `open-top` — An open car with side-mounted cannons and shot racks. Eisenhart artillery in transit.
- **24 Military Transport** `military` `enclosed` — An armoured car with a central locked strongroom/payload and troop benches along the sides. The **strongbox + escort car**: the marquee climax room for a robbery.
- **25 Military Bunk** `military` `enclosed` — A troop car with round mess tables, bunks and barrels.

### Grim & captivity
- **33 Prison** `grim` `enclosed` — Barred cells down the car with a guard space. Prisoner transport.
- **34 Prison Skeletons** `grim` `enclosed` — The same cell layout with skeletal remains; a horror dressing for an abandoned or massacred train.
- **35 Stables** `grim` `enclosed` — Stalls with horses, hay and tack. Mount/livestock transport.
- **36 Cages** `grim` `enclosed` — Beast cages down the car for creature (or "creature") transport.

### Flex / blank
- **Clean 12 Open** `flex` `enclosed` — A bare open-plan wood car with no fittings; drop props to make anything.
- **Clean 18 Empty** `flex` `enclosed` — A completely empty wood box; total blank canvas.

---

## Ready-made consists

Front (engine) to rear. Mix in roof tiles for an over-the-top layer.

- **Freight robbery (the Narrows Job pattern).** `01 Engine` → `28 Cargo Coal` (tender) → `24 Military Transport` (the strongbox + the featured crate) → `12 First Class` or `14 Steerage` (passengers/guards) → `27 Cargo Crates` or `23 Cannons` (freight flat) → `03 Crew Quarters` (rear/brakeman). Swap the marquee crate car for `26 Artefacts` if the prize is one object.
- **Luxury express (heist / social caper).** `01 Engine` → `02 Crew Quarters` → `13 First Class` → `09 VIP` → `06 Dining` → `08 Bar` → `11 Sleeper Premium`. A mark, a manifest, and a lot of bystanders.
- **Prison train (rescue / break-out).** `01 Engine` → `25 Military Bunk` (the guards) → `33 Prison` → `36 Cages` → `24 Military Transport` (the warden's strongroom). Use `34 Prison Skeletons` if the party arrives to a massacre.
- **Treasure freight (high-value haul).** `01 Engine` → `28 Cargo Coal` → `29 Cargo Gold Ore` / `30 Cargo Purple Crystal` → `26 Artefacts` → `24 Military Transport`. The richest train on the Southern network and the most-hunted.
