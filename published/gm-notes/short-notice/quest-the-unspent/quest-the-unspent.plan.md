# The Unspent · design brief (quest-workflow, Phases 1–3)

The quest pages are now the working copy: `quest-the-unspent.html`, the four part pages and `cast.html`. This brief keeps the design decisions.

Working brief for the Available on Short Notice pirate multishot, carried between machines until the quest page exists. Canon behind it: `lore/geography/askamira/twin-cities.md` (*The Unspent*, *⚿ GM Secret: the Unspent*, *Ninehulls*), `lore/geography/bolverk.md` (*Nirfel*), glossary Twin Cities block.

## Table

- Party level **11**. Encounters built for **5 combatants**; scenes must work for all **6** at the table; play goes on with players missing.
- House rule (Session 0): social rolls may use the highest modifier among party members present.
- Planned by story, not by session: four parts that run as long as the table takes. It ends when the party leaves the Twin Cities.

## Premise

The party is crossing the Midarra north to Solkai on the stillship **the Goodmeasure** (Master **Ozhra**, Kholo) as its hired guards, a Guild job taken on short notice in Rika Tikur. The cargo is luxury goods (Eldaran almosts, Emarrean sake, Lautaran silk) plus two things he must not be caught with in a locked cabin (an eight-stripe Catjomin Sake; Dreaming Cape tea). He bought no colours: he trusts no Lord's colours to hold. Unflagged poachers under **Redsail** (a bought name) attack; mid-fight Ninehulls' fleet arrives and its broadside shreds them. Ninehulls swings over ("Now what are you doing in MY waters"), kills Redsail when he attacks, apologises to the party, and will not set them adrift in the jolly boat: he brings them to Freeboard, but the ship is his (a deck needs a hull). The surviving poachers hold the Last Hands on deck: deposition; they sign under his flag. The party watches the ritual early.

In Freeboard the Goodmeasure is hoisted into the stack and becomes a deck; Skysail comes home for the Mooring. **Merrin out of the Jigger**, captain of the Unspent's keepers (voted in on Nirfel's "yours by right"), hires the stranded Guild party as old-tech experts to open Goldwake's flagship.

## Parts I and II: Struck Colours · Aboard the Unspent

1. The Goodmeasure and the poachers (fight, moderate) → Ninehulls' broadside → Redsail killed → the Last Hands (deposition).
2. Freeboard; the hoisting; Pell already telling it. The Mooring.
3. The hire; up by basket to the Unspent. The keepers do not board (none has in 140 years).
4. **The Unspent run:** trap (kill-gangway, rigged swivel guns, false caches) → puzzle (she hangs at a tilt and jams the aft doors; shift ballast/cannon until level) → **the veterans' oath-ghosts** before the cabin door (their oath: keep her shut; mid-fight clues "keep her shut") → defeating them lets the door open; the **first air** in 140 years enters; Goldwake's preserved arm falls; the **lift-heart** rolls from her hand. Nirfel's whisper starts in the cabin. If the party hesitates, Merrin shoves past and opens it herself. The Jigger lurches. End.

## Part III: The Jigger's Holds (timed dungeon)

Flowchart: `holds-routes.svg` beside this file.

- **Sink Clock, 8 stages.** +1 per 10-minute activity (Treat Wounds, Refocus, Repair), per crit fail, for the gallery; −1 at B2, via Kesti's lines (costs a favour), or by dumping weight (homes into the Midarra). Stages: 1 airship tears free · 2 tilt, gardens slide · 3 the Main lurches · 4 the dead Lord's spire falls · 5 debris on the top decks · 6 settles on the stack · 7 the stack buckles · **8 engine stops, part of the lower city lost (true failure)**. 6–7 grim but fixable. Played clean: room for about two rests.
- **The carry:** the heart must go up to the Jigger's empty socket. Near it, lift fails (no flying, loose things drift to it). The engine's defenders target the carrier.
- 0 The Fall (skill challenge; the crew hauls the hoard before people) · 1 Kesti's briefing (clock starts; Old Hobb offers to guide) · 2 the Underside, route choice.
- **Inside (the reading):** A1 tended holds (Hobb's rite reveals WAKE) → A2 root-choked hull (hazard) → A3 gallery of old writing (puzzle, +1 stage, reveals TURN and BIND) → A4 wardens in the corridors (moderate) → A5 shaft, upper landing.
- **Outside (open air):** B1 the Gate (spot the shaft mouth; cross open air with no lift; checks, or a creative plan replaces a check; fail: +1 stage, go inside) → B2 the hanging fleet (skill challenge; help a crew hold: −1 stage, lives saved) → B3 wardens on the root-beard (moderate, open air) → B4 full shaft climb (hazard).
- **The gear chamber (A5/B4, map `lift-shaft`).** The narrated shaft climb ends in the old work's governor room. Foundry scene: 140 px grid = 5 ft, 33 × 46 squares, no walls. Goal: the carrier and the heart reach the **exit** (top stairs). Entries: **outside route** at the bottom stairs, **inside route** at the lower-right stairs; the upper-left and upper-right stairs are blocked. Route lengths (approximate, traced by eye): right way about 39 sq / 195 ft; inside route about 27 sq / 135 ft; the runner from the bottom stairs to the governor about 15 sq / 75 ft.
  - **The pull:** drift toward the governor, light on the outer walkways, strong on the inner walkways, more for the carrier. Checked at the end of a creature's turn unless it Braced: two Strides + Brace (10 squares at Speed 25) means no check; three Strides (15 squares) means a pull check (failure slides toward the governor, critical failure further or off the edge). The carrier keeps full Speed, but its Brace needs an Athletics check, which an ally can Aid. Off a walkway is a fall back down the shaft (+1 stage, back in at the bottom stairs).
  - **The clockworks:** G5 and G6 dangerous, G8 easy; always turning until shut off at the governor. Passing one: the clockwork check (crit no damage · success half · failure full damage and blocked). Dangerous clockwork on a crit fail throws the creature off the platform: one chance to grab a ledge, or an adjacent ally catches them (the catcher takes half the clockwork's damage); otherwise the fall.
  - **The strikes (`gear-chamber-strikes.webp`):** the walkway sections are named in `maps/lift-shaft.areas.json`. On the hazard's own turn (a Reflex save; Brace does not help) four sections are struck on a three-round cycle, spread over the room, never two neighbours in the same round: **round 1** Ring South-East, Ring North-East, Ring West (G8), Crescent North (above the governor) · **round 2** Ring South-West, Crescent South-East, Ring North (before the exit), Crescent West · **round 3** Crescent South-West, Crescent East (the right jump), Ring North-West (G6), Dangerous Ground; then again. Every section is hit one round in three.
    - **Reading the pattern:** after watching a round (the stairs lie outside the room), Perception (Seek) or Crafting (Recall Knowledge on the old work). Critical success: as success, and they also see each round's wild strike. Success: from then on the GM marks next round's four sections at the end of each round. Failure: nothing yet, try again next round. Critical failure: the wrong set is shown once.
    - **The wild strike:** one extra section each round (a loose cable, falling debris), never one of that round's four. Unmarked; spotting it costs an action each round (Seek against the DC) and shows it only to the spotter, so a spotter cannot both Brace and move a full distance. d12: 1 Ring South-East · 2 Ring South-West · 3 Ring West (G8) · 4 Ring North-West (G6) · 5 Ring North (before the exit) · 6 Ring North-East · 7 Crescent South-West · 8 Crescent South-East · 9 Crescent East (the right jump) · 10 Crescent North (above the governor) · 11 Crescent West · 12 Dangerous Ground. Pre-rolled: R1: Crescent South-West · R2: Dangerous Ground · R3: Ring South-East · R4: Crescent South-West · R5: Ring North-West (G6) · R6: Crescent North (above the governor) · R7: Crescent South-East · R8: Ring South-East · R9: Ring West (G8) · R10: Ring North-West (G6).
  - **The governor (the den of lions):** reached through the strong pull of the inner walkways and the jumps. The jumps are hard; for the carrier, the heart's pull makes them all but impossible (incredibly hard DC). Working the governor (Crafting/Arcana/Thievery) stops a clockwork: success for 1 round, critical success for 2. The crumbling ground on the upper ramp gives way under a Medium creature (Trap Sense to notice).
  - **The routes:** *right way*, the easy one once someone has shut down G5 at the governor: Ring South-East, G5, Ring North-East, Ring North (about 35 squares). *Left way*, no one in the middle: Ring South-West, Ring West with G8 (easy), then Crescent West, Crescent North and the crumbling ground, avoiding both dangerous clockworks (about 50 squares, the longest under the strikes); or straight on through Ring North-West and G6 (about 41 squares). *Inside route*: past G5 (or wait for it to be shut down), then Ring North-East and Ring North. *Inner route*: Crescent South-West, Crescent South-East, Crescent East (across the right jump), Ring North-East, Ring North: no clockworks, strongest pull, and the jump the carrier cannot reliably make (hand the heart off, or leave the carrier to another route).
- **Boss: the engine heart.** Warden (severe) + engine as complex hazard. Seating: 4 steps in order at the socket, each 2 actions + check: **Cradle** (Athletics, always known) · **Turn** (Crafting/Arcana) · **Wake** (Occultism/Religion/Performance) · **Bind** (Thievery/Crafting). Known step: standard DC; unknown: Recall Knowledge first, harder DC. Crit fail: engine lashes the seater; crit success: step done and the engine holds a round. Inside arrives with all 4 known; outside with Cradle only.
- The Rise: the Jigger lifts and warms.

## Part IV: The Last Hands

1. Morning after: Kesti pays coin + passage out on a Skysail airship. The tellers tell the holds.
2. **Nirfel's night whisper** to the party: go now, take it, you earned it. Taking from the hoard marks the taker (Greed-mark); stealing it also crosses the crew.
3. Share-out **on the Unspent**, the crew having made it safe. Merrin offers a share. An Occultism/Religion check shows the mark for what it is. Payment and passage come unmarked; the hoard is the temptation.
4. **Ninehulls** claims the dead Lord's prize by the hold-custom (what you can hold is yours) and calls the party out ("you're the ones they're telling"). Fight on the Unspent (severe–extreme). Arena mechanics: ballast tilt (Interact + Athletics; Reflex/Acrobatics or slide), surviving swivel guns, the kill-gangway if still rigged, cutting a line. **The Man Who Cannot Die:** a reaction at 0 HP, he stays up and heals substantially, once per fight. Losing: he takes the hoard and leaves them alive.
5. The Last Hands: **deposition** (fixed). Pell tells it; the table picks the told name.
6. Coda: Ninehulls walks into their tavern and pays the round; his flag goes back up. They leave.

## Maps

Foundry modules installed on the server: Tom Cartos Schooner, Bharzul (unused); CzePeku Crystal Veil, Yggdrasil Roots, Ancient Tech Treasury, Chrono Chaos Ruins Interior, Void Dragon Lair, Clockwork Dragon Lair Interior, Floating Sky Castle (unused). Full-res copies in the sync folder (`maps/_full` → `~/Sync/Tyrnarra/published-full/short-notice/quest-the-unspent/maps`); 800px web copies + starter `*.areas.json` (GM to refine in the map-area-editor) in `maps/`.

| Web copy | Scene | Source |
|---|---|---|
| goodmeasure-deck | opening fight | Schooner main deck |
| unspent-l0-hold … unspent-l4 | the Unspent (S1, S3) | Crystal Veil, Original L0, Black Sails L1–L4 |
| root-choked-hull | A2 | Yggdrasil Roots, Original Empty |
| wardens-corridors | A3/A4 | Ancient Tech Treasury, Abandoned |
| lift-shaft | A5/B4 | Chrono Chaos Ruins Interior |
| root-beard | B3 | Void Dragon Lair, Floating Islands |
| engine-heart | boss | Clockwork Dragon Lair Interior, Silver (cold); Original after seating; Rising 1–3 as the hazard worsens |

## Next

Encounters (pf2e-encounter, 5 PCs at 11: low 75 · moderate 100 · severe 150 · extreme 200 XP), loot (pf2e-loot), then the quest page `quest-the-unspent.html` + gm-nav + hub card + site-inventory. Foundry for the gear chamber: a macro that creates the sections as hidden drawings and shows next round's strikes (and the wild strike) by click or automatically each round, with hazard actors placed on the map (clockworks, strikes, pull, crumbling ground) so their checks can be posted to chat. Open: Redsail's crew and Ninehulls' stat basis, the ghosts (Ghost Pirate Captain / Ghostly Mob are candidates), the wardens and the engine's warden, the lift-shaft hazard.
