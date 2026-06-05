---
name: quest-workflow
description: Use this skill to take a Tyrnarra campaign quest, dungeon, or adventure module from premise to a fully-built GM page in the /campaigns/ layer. Trigger on "build a quest", "design a dungeon/adventure/module", "stat out this dungeon", "make an encounter crawl for [location]", "flesh out the [location] for my party", "prep the [place] session", working on a quest-<slug>.html under /campaigns/, or any session that takes a session idea to encounters + loot + a runnable GM page. Orchestrates the pf2e-encounter and pf2e-loot leaf skills for the math, consumes clickable-map area JSON from campaigns/tools/map-area-editor.html, and assembles the page per docs/campaign-layer.md (the Furrious Five layer is the reference). The arc is: premise -> structure -> map+areas (you draw them) -> encounters -> loot -> quest HTML, with a surface-before-writing pause at every seam. Do not use for player-facing worldbuilding pages (that is sub-region-workflow / god-city-workflow) or for lore canon; quest material is GM-only and lives only in /campaigns/.
---

# quest-workflow

Takes a session idea to a runnable, GM-only quest page in `/campaigns/<campaign>/quest-<slug>.html`, with PF2e-accurate encounters and treasure, a clickable battlemap, and the user's voice setting direction at every phase boundary.

This is the capstone that the `pf2e-encounter` and `pf2e-loot` leaf skills feed. It is **GM-side** work: unlike the player-facing workflows, stat blocks, read-aloud boxes, adventure hooks, and GM-tier truth are the *point* here, not leaks. Quest pages get no chronicler-voice constraint and no GM-Vetted badge. What still holds: canon-consistency with the player lore, no em-dashes, affirmative prose.

## On invocation, before anything else

Read these. Skipping is the largest source of rework.

1. **`CLAUDE.md`** (no em-dashes, affirmative prose, mortals-not-humans, the campaign-layer rule that quests live in `/campaigns/` and never in the player sidebar).
2. **`docs/campaign-layer.md`** end-to-end: folder layout, chrome conventions (`gm.css`/`gm.js`/`gm-nav.css`/`gm-nav.js`), the clickable-battlemap contract, and the paid-map rule (`maps/_full/` gitignored).
3. **The reference implementation**: `campaigns/furrious-five/quest-venomqueen.html` (the Cavern Map battlemap pattern) and `campaigns/furrious-five/quest-veldtmark.html`. Read one end-to-end as the page template.
4. **The player-facing canon for where the quest is set** — the relevant `talan/domains/<domain>/…` page(s) and `lore/geography/<region>.md`, so NPCs, place-names, gods, and neighbours are consistent. Quest material may reveal GM-tier truth, but it must not contradict committed canon.
5. **Tooling check**: confirm `campaigns/tools/encounterBuilder/bestiary.db` and `items.db` exist; if not, run `python rebuild.py` from that directory once (first run clones the Foundry repo, a few minutes).

If anything you are about to design contradicts committed canon, the canon wins. Surface the conflict in chat before adapting.

## The phases at a glance

| Phase | What happens | Boundary discipline |
|---|---|---|
| **0. Read** | CLAUDE.md + campaign-layer.md + a reference quest + the setting's player canon + tooling check | Do not start Phase 1 until done |
| **1. Premise + party** | Chat: where it sits, **party level + size**, hook, antagonist, stakes, tone. Surface a premise summary | Chat only. No writes. |
| **2. Structure** | Chat: the beats / scenes / rooms and the throughline; which scenes are combat vs social vs exploration; the climax. Surface a beat -> area outline | Chat only. No writes. |
| **3. Map + areas** | Decide the battlemap; **you draw the areas** in `map-area-editor.html` and hand back the exported JSON. Skill consumes it as the room list | Human handoff. Skill waits for the area JSON. |
| **4. Encounters** | Invoke **pf2e-encounter** per combat area (party params + area theme), grounded in real stat blocks. Surface the encounter set | Surface for tweaks before Phase 6 |
| **5. Loot** | Invoke **pf2e-loot** (level hand-out, or per-area/milestone), place rewards in areas. Surface | Surface for tweaks before Phase 6 |
| **6. Assemble quest HTML** | Build `quest-<slug>.html` per campaign-layer conventions + wire it in. Surface the content plan first, build on the go | Surface-before-HTML pause |

Pause at each seam even under broad "work through it" framing. Reading is fine within a phase; writes (and the big HTML build) trigger the boundary.

---

## Phase 1: Premise + party (chat only)

Ask a tight batch of questions, then surface a premise summary. The non-negotiable two are **party level and party size** (every encounter and the loot math depend on them). Cover:

- **Setting + campaign.** Which campaign folder (`/campaigns/<campaign>/`), and where in Talan does this sit? Tie it to a real place so canon stays consistent.
- **Party.** Level and size. Note any party weaknesses/strengths that should shape encounters (no healer, a fire mage, etc.).
- **The hook.** Why are they here, and who sent them?
- **The opposition.** The antagonist or threat, and its theme (this becomes the encounter and loot theme).
- **Stakes + tone.** What happens if they fail; how grim/pulpy/eerie it plays.
- **Shape + length.** One-shot vs multi-session; dungeon-crawl vs investigation vs set-piece.

Surface a 4-6 sentence premise back before Phase 2. Use the `grill-me` skill if the premise reads generic or the antagonist is a stock villain; specificity here pays off in every later phase.

## Phase 2: Structure (chat only)

Lay out the beats and the spaces they happen in. Produce a **beat -> area outline**:

- The dramatic shape (approach, complication, midpoint turn, climax, aftermath).
- One line per scene/room: its role (combat / social / exploration / trap / set-piece), its mood, and what the party learns or gains there.
- The throughline that connects rooms (a recurring sign, a rising threat clock, the antagonist's footprint).
- Flag which areas will need an encounter (Phase 4) and which will carry the marquee loot (Phase 5).

Surface the outline. The user may reorder, cut, or add scenes before any map work.

## Phase 3: Map + areas (human handoff)

The clickable battlemap is built from areas **you draw**.

1. **Pick the map.** Identify or choose the battlemap image. Paid art (CzePeku, etc.) stays local: full-res in `campaigns/<campaign>/assets/maps/_full/` (gitignored); a downsized ~800px web copy sits in `maps/` and is the one the page references. See campaign-layer.md "Map assets".
2. **Hand off to the editor.** Tell the user to open `campaigns/tools/map-area-editor.html`, load the map, draw one area per room/scene from the Phase 2 outline (Shift+draw to add rectangles for L/T/plus shapes), label + describe each, and export the JSON.
3. **Wait.** This is the user's step ("I create areas and notes"). Do not fabricate areas; consume the exported JSON they hand back as the authoritative room list. Each area is `{ label, desc, rects:[{left,top,width,height}] }` in percentages.

If the user would rather skip the visual map (theatre-of-mind), take an ordered room list in chat instead and build the page without the map tab.

## Phase 4: Encounters (invoke pf2e-encounter)

For each combat area from the outline, **invoke the `pf2e-encounter` skill** with the party level/size and the area's theme. Let that skill do the budget math and the real-data grounding; this phase is about choosing threat and shape per room so the dungeon has a difficulty arc (patrols low/moderate, set-pieces severe, the climax severe/extreme boss).

- Keep the theme coherent with the antagonist (one faction reads as one bestiary family + a few outliers).
- Pull the real stat block (HP/AC/Perception/saves/attacks/abilities) for every creature from its source JSON; the page needs runnable numbers.
- Surface the full encounter set (area -> creatures -> budget line) for the user to tweak before assembly.

## Phase 5: Loot (invoke pf2e-loot)

**Invoke the `pf2e-loot` skill.** Default to a level hand-out for the quest's intended level (the official Party-Treasure-by-Level basket), or split it across milestones/areas with `--value`/`--share` if the reward should be parcelled out. Theme it to the antagonist and the place.

- Place the marquee permanent items in fitting rooms (the boss carries the magic weapon; the vault holds the coins).
- Read the source JSON for any item that needs its activation/effect written into the page.
- Surface the haul (permanent / consumable / coins + placement) before assembly.

## Phase 6: Assemble the quest HTML (surface first, then build)

Surface the content plan (sections, which areas, which secrets, the map tab) before writing the page. On the go-ahead, build `campaigns/<campaign>/quest-<slug>.html`.

**Structure (model on `quest-venomqueen.html`):**

- `<head>`: links `gm.css` + `gm-nav.css`, defers `gm-nav.js` + `gm.js`. `<body data-page="quest-<slug>">`.
- **`.gm-banner`** ("⚔ GM Material · Behind the Screen · Not Player-Facing") + a link back to the campaign hub and the relevant player page.
- **Overview**: premise, party level/size, hook, stakes, the throughline.
- **Tabbed sections** (`.gm-tab-btn` + `.gm-panel`) or a linear flow: overview, the map, the rooms, NPCs, rewards.
- **The clickable battlemap tab** (if a map was drawn): the map `<img>` + one `.map-hot` button per rectangle (percentage-positioned, same `data-area` key for multi-rect areas, `hot-num` badge on the first only) + `window.GM_MAP_AREAS = { key: { n: "1 · Title", t: "<p>room notes</p>" }, … }` generated from the exported area JSON. Behaviour is already in `gm.js`.
- **Per-room blocks**: read-aloud box, GM notes, the encounter (creatures with real stat lines), traps/secrets (`.gm-secret`), and the room's loot.
- **NPC cards** (`.npc-card`) for the antagonist and key figures: real stat block, motive, tactics, voice.
- **Rewards section**: the full haul with item levels, prices, and effects; where each piece is found.
- **Hooks / aftermath**: where the story can go next.

**Conventions:** no em-dashes (en-dashes for numeric ranges only); affirmative prose; mortals not humans; all links absolute; canon-consistent names. GM-tier content is welcome and expected here.

**Wire it in:**

1. **`campaigns/assets/gm-nav.js`** — add the quest to the GM sidebar tree under its campaign; the entry's slug must match the page's `data-page`.
2. **`campaigns/<campaign>/index.html`** — add a card for the quest in the campaign hub.
3. **`docs/site-inventory.md`** — add the page to the GM-only roster section (campaign layer is not in the published rosters).
4. **Maps** — confirm the committed copy is the downsized web image and any full-res original is in `_full/` (gitignored). If a full-res file is tracked outside `_full/`, untrack it.

---

## Hard rules

- **GM-only, always.** Everything this skill writes lives under `/campaigns/` and is never added to the player sidebar (`assets/site-nav.js`). The GM sidebar is `campaigns/assets/gm-nav.js`.
- **Real data, never invented.** Encounter budgets, creature stats, item levels and prices come from the tools and the source JSON via the leaf skills. If a number is not grounded, it does not ship.
- **Party level + size first.** Capture them in Phase 1; all encounter and loot math depends on them.
- **Canon-consistent.** NPCs, places, gods, and neighbours reconcile with the player lore. A quest may reveal GM-tier truth; it may not contradict committed canon.
- **The user draws the map.** Areas come from `map-area-editor.html` (or an explicit chat room-list), not from invention.
- **Surface at every seam.** Premise -> structure -> areas -> encounters -> loot -> page. Pause and surface before each write, and before the HTML build.
- **No em-dashes; affirmative prose; mortals not humans.** The project-wide prose rules apply to GM pages too.

## Common pitfalls

- **Skipping the canon read.** A quest set in a real domain must match its page; grep the place-name and read the domain page in Phase 0.
- **Inventing map areas.** The room list is the user's exported JSON. Wait for it.
- **Inventing stats to save a tool run.** Run the leaf skills; read the JSON. The whole point of the tooling is reality-accurate numbers.
- **Flat difficulty.** Vary threat and shape per room (Phase 4) so the crawl has an arc; a dungeon of five identical moderate fights reads dead.
- **Loot off the party's level.** Use the hand-out or value math; do not drop a high-level item because it fits the theme.
- **Publishing a paid map.** Full-res stays in `_full/`; the page references the downsized copy only.
- **Chronicler-voice creep.** This is GM material; write plainly and mechanically. Save the in-world voice for the read-aloud boxes.
