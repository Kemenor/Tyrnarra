---
name: quest-workflow
description: Use this skill to take a Tyrnarra campaign quest, dungeon, or adventure module from premise to a fully-built GM page in the /campaigns/ layer. Trigger on "build a quest", "design a dungeon/adventure/module", "stat out this dungeon", "make an encounter crawl for [location]", "flesh out the [location] for my party", "prep the [place] session", working on a quest-<slug>.html under /campaigns/, or any session that takes a session idea to encounters + loot + a runnable GM page. Orchestrates the pf2e-encounter and pf2e-loot leaf skills for the math, consumes clickable-map area JSON from campaigns/tools/map-area-editor.html, and assembles the page per docs/campaign-layer.md (the Furrious Five layer is the reference). The arc is: intake -> 3-5 seeds -> premise -> structure -> map (Claude searches the CzePeku / Tom Cartos catalogs, you download + draw areas) -> encounters -> loot -> quest HTML -> Foundry import macro, with a surface-before-writing pause at every seam. Do not use for player-facing worldbuilding pages (that is sub-region-workflow / god-city-workflow) or for lore canon; quest material is GM-only and lives only in /campaigns/.
---

# quest-workflow

Takes a session idea to a runnable, GM-only quest page in `/campaigns/<campaign>/quest-<slug>.html`, with PF2e-accurate encounters and treasure, a clickable battlemap, and the user's voice setting direction at every phase boundary.

This is the capstone that the `pf2e-encounter` and `pf2e-loot` leaf skills feed. It is **GM-side** work: unlike the player-facing workflows, stat blocks, read-aloud boxes, adventure hooks, and GM-tier truth are the *point* here, not leaks. Quest pages get no chronicler-voice constraint and no GM-Vetted badge. What still holds: canon-consistency with the player lore, no em-dashes, affirmative prose.

## On invocation, before anything else

Read these. Skipping is the largest source of rework.

1. **`CLAUDE.md`** (no em-dashes, affirmative prose, mortals-not-humans, the campaign-layer rule that quests live in `/campaigns/` and never in the player sidebar).
2. **`docs/campaign-layer.md`** end-to-end: folder layout, chrome conventions (`gm.css`/`gm.js`/`gm-nav.css`/`gm-nav.js`), the clickable-battlemap contract, and the subscription-map rule (`maps/_full/` gitignored).
3. **The reference implementation**: `campaigns/furrious-five/quest-venomqueen.html` (the Cavern Map battlemap pattern) and `campaigns/furrious-five/quest-veldtmark.html`. Read one end-to-end as the page template.
4. **The player-facing canon for where the quest is set** — the relevant `talan/domains/<domain>/…` page(s) and `lore/geography/<region>.md`, so NPCs, place-names, gods, and neighbours are consistent. Quest material may reveal GM-tier truth, but it must not contradict committed canon.
5. **Tooling check**: confirm `campaigns/tools/encounterBuilder/bestiary.db` and `items.db` exist; if not, run `python rebuild.py` from that directory once (first run clones the Foundry repo, a few minutes).

If anything you are about to design contradicts committed canon, the canon wins. Surface the conflict in chat before adapting.

## The phases at a glance

| Phase | What happens | Boundary discipline |
|---|---|---|
| **0. Read** | CLAUDE.md + campaign-layer.md + a reference quest + the setting's player canon + tooling check | Do not start Phase 1 until done |
| **1. Intake + seeds** | Chat: take the intake text, lock **party level + size**, generate **3-5 distinct seeds**, user picks, workshop the winner into a premise | Chat only. No writes. |
| **2. Structure** | Chat: the beats / scenes / rooms and the throughline; which scenes are combat vs social vs exploration; the climax. Surface a beat -> area outline | Chat only. No writes. |
| **3. Map + areas** | Claude searches CzePeku / Tom Cartos / Lost Atlas and surfaces **3-5 map options**; **user downloads** the pick; **user draws the areas** in `map-area-editor.html` and hands back the exported JSON | Human handoff. Skill waits for the area JSON. |
| **4. Encounters** | Invoke **pf2e-encounter** per combat area (party params + area theme), grounded in real stat blocks. Surface the encounter set | Surface for tweaks before Phase 6 |
| **5. Loot** | Invoke **pf2e-loot** (level hand-out, or per-area/milestone), place rewards in areas. Surface | Surface for tweaks before Phase 6 |
| **6. Assemble quest HTML** | Build `quest-<slug>.html` per campaign-layer conventions + wire it in. Surface the content plan first, build on the go | Surface-before-HTML pause |
| **7. Foundry export** (optional) | Assemble a spec from the encounter + loot results, run `foundry_macro.py` to emit the import macro, surface it for the user to paste-run in Foundry | Surface the macro + spec |

Pause at each seam even under broad "work through it" framing. Reading is fine within a phase; writes (and the big HTML build) trigger the boundary.

---

## Phase 1: Intake + seeds + party (chat only)

The user opens with a block of raw material: themes, story beats, a location, a villain, a vibe. Two moves here.

**First, lock the non-negotiables.** Party **level and size** drive every encounter and the loot math; if the intake text doesn't state them, ask before generating seeds. Also note which campaign folder (`/campaigns/<campaign>/`) and roughly where in Talan this sits, so the seeds stay canon-consistent. Tie it to a real place.

**Then generate 3-5 quest seeds** from the intake material and surface them for the user to pick. Each seed is a tight pitch (2-4 sentences) that reads as a *distinct* quest, not a reskin of its siblings:

- a one-line title or working name,
- **the hook** (why the party is here, who sent them),
- **the opposition** (antagonist + its theme; this becomes the encounter and loot theme),
- **the shape** (one-shot vs multi-session; dungeon-crawl / investigation / set-piece),
- **the stakes + tone** (what failure costs; how grim / pulpy / eerie it plays).

Make the seeds pull in genuinely different directions (different antagonist, different shape, different moral texture) so the pick is a real choice. Run them against the specificity test: if a seed's antagonist is a stock villain or its hook could be lifted into any other quest unchanged, sharpen it or replace it. Use the `grill-me` skill if the whole set reads generic.

The user picks one seed (or splices two). **Workshop the winner into a 4-6 sentence premise** and surface that before Phase 2: setting + campaign, party level/size (plus any party weakness/strength that should shape encounters, e.g. no healer, a fire mage), hook, opposition, stakes, tone, and shape + length.

## Phase 2: Structure (chat only)

Lay out the beats and the spaces they happen in. Produce a **beat -> area outline**:

- The dramatic shape (approach, complication, midpoint turn, climax, aftermath).
- One line per scene/room: its role (combat / social / exploration / trap / set-piece), its mood, and what the party learns or gains there.
- The throughline that connects rooms (a recurring sign, a rising threat clock, the antagonist's footprint).
- Flag which areas will need an encounter (Phase 4) and which will carry the marquee loot (Phase 5).

Surface the outline. The user may reorder, cut, or add scenes before any map work.

## Phase 3: Map — search, buy, draw areas (web search + human handoff)

Three steps: Claude surfaces map options from the user's CzePeku / Tom Cartos subscription catalogs, the user downloads the pick, then the user draws the areas.

**1. Search the catalogs and surface 3-5 options.** Using the Phase 2 mood + room list as the theme, search CzePeku and Tom Cartos for fitting battlemaps and present a shortlist of titled links for the user to choose from. These are visual, JS-heavy galleries, so drive the search with `WebSearch` scoped by domain rather than trying to scrape the gallery pages:
   - **CzePeku** — `WebSearch` with `allowed_domains: ["czepeku.com"]` (fantasy maps live under `/fantasy/maps`, sci-fi under `/scifi/maps`).
   - **Tom Cartos** — `WebSearch` with `allowed_domains: ["tomcartos.com"]` (`/map-gallery` for fantasy, `/modern-map-gallery` for modern).
   - **Lost Atlas** (`lostatlas.co`) — a cross-creator keyword/creator-filtered battlemap search engine that indexes Tom Cartos and others; good when a domain-scoped search comes up thin.

   Surface each candidate as a titled link with a one-line "why it fits" (the cavern with the central pool; the three-storey manor; the flooded crypt). `WebFetch` a candidate page only to confirm what is actually on it. Present 3-5 and let the user pick.

**2. The user downloads; Claude downsizes.** These come from the user's **CzePeku / Tom Cartos subscriptions**, so **the user does the download** — Claude never fetches or commits the art. The user hands over the full-res original (and any full downloaded pack, which often bundles extra art + Foundry module files); it belongs in `campaigns/<campaign>/assets/maps/_full/` (gitignored, local only). **Claude generates the downsized ~800px web copy** that sits directly in `maps/` (committed; the page references this one), with ImageMagick: `magick "<_full>/<original>" -resize 800x "<maps>/<slug>.webp"` (match the 800px-wide precedent of the existing committed maps). If the user dropped subscription art loose in `maps/`, move it into `_full/` before staging anything. See campaign-layer.md "Map assets".

**3. Hand off to the editor.** Tell the user to open `campaigns/tools/map-area-editor.html`, load the map (the full-res original is fine — area coordinates are stored as percentages, so the same JSON applies to the downsized copy the page references), draw one area per room/scene from the Phase 2 outline (Shift+draw to add rectangles for L/T/plus shapes), label + describe each, and export the JSON. **Wait** for it: this is the user's step ("I create areas and notes"). Do not fabricate areas; consume the exported JSON they hand back as the authoritative room list. Each area is `{ label, desc, rects:[{left,top,width,height}] }` in percentages. The same export feeds the Phase-7 Foundry token placement (`--areas`), so the area labels become the placement targets; keep them stable.

If the user would rather skip the visual map (theatre-of-mind), take an ordered room list in chat instead and build the page without the map tab.

## Phase 4: Encounters (invoke pf2e-encounter)

For each combat area from the outline, **invoke the `pf2e-encounter` skill** with the party level/size and the area's theme. Let that skill do the budget math and the real-data grounding; this phase is about choosing threat and shape per room so the dungeon has a difficulty arc (patrols low/moderate, set-pieces severe, the climax severe/extreme boss).

- Keep the theme coherent with the antagonist (one faction reads as one bestiary family + a few outliers).
- Pull the real stat block (HP/AC/Perception/saves/attacks/abilities) for every creature from its source JSON; the page needs runnable numbers.
- Surface the full encounter set (area -> creatures -> budget line) for the user to tweak before assembly.
- If Foundry export (Phase 7) is in scope, save each area's `encounter.py build --json` output; Phase 7 assembles the import spec straight from it.

## Phase 5: Loot (invoke pf2e-loot)

**Invoke the `pf2e-loot` skill.** Default to a level hand-out for the quest's intended level (the official Party-Treasure-by-Level basket), or split it across milestones/areas with `--value`/`--share` if the reward should be parcelled out. Theme it to the antagonist and the place.

- Place the marquee permanent items in fitting rooms (the boss carries the magic weapon; the vault holds the coins).
- Read the source JSON for any item that needs its activation/effect written into the page.
- Surface the haul (permanent / consumable / coins + placement) before assembly.
- If Foundry export (Phase 7) is in scope, save the `loot.py build --json` output; Phase 7 turns it into the chest's items + coins.

## Phase 6: Assemble the quest HTML (surface first, then build)

Surface the content plan (sections, which areas, which secrets, the map tab) before writing the page. On the go-ahead, build `campaigns/<campaign>/quest-<slug>.html`.

**Structure (model on `quest-venomqueen.html`):**

- `<head>`: links `gm.css` + `gm-nav.css`, defers `gm-nav.js` + `gm.js`. `<body data-page="quest-<slug>">`.
- **`.gm-banner`** ("⚔ GM Material · Behind the Screen · Not Player-Facing") + a link back to the campaign hub and the relevant player page.
- **Overview**: premise, party level/size, hook, stakes, the throughline.
- **Tabbed sections** (`.gm-tab-btn` + `.gm-panel`) or a linear flow: overview, the map, the rooms, NPCs, rewards.
- **The clickable battlemap tab** (if a map was drawn): the map `<img>` + one `.map-hot` button per rectangle (percentage-positioned, same `data-area` key for multi-rect areas, `hot-num` badge on the first only) + `window.GM_MAP_AREAS = { key: { n: "1 · Title", t: "<p>room notes</p>" }, … }` generated from the exported area JSON. Behaviour is already in `gm.js`.
- **Per-room blocks**: read-aloud box, GM notes, the encounter (creatures with real stat lines), **skill-check callouts** (Recall Knowledge / social / exploration, each with skill + DC + four degrees), traps/secrets (`.gm-secret`), and the room's loot.
- **NPC cards** (`.npc-card`) for the antagonist and key figures: real stat block, motive, tactics, voice.
- **Rewards section**: the full haul with item levels, prices, and effects; where each piece is found.
- **Hooks / aftermath**: where the story can go next.

**Skill checks (weave them in).** A quest is not only fights. Seed Recall Knowledge, social, and exploration checks through the scenes and write each as **skill + DC + four degrees** (Critical Success / Success / Failure / Critical Failure; a nat 20 shifts up one step, a nat 1 down one). **Set the DC by the challenge, not the party level**: knowledge from the Simple-DC proficiency that would know it; NPC interaction from the NPC's level-based DC; a hazard from its own level; then layer difficulty (±2/±5/±10) and rarity (+2/+5/+10). Full tables, the degree rules, and worked examples live in `campaigns/gm-reference/dc-cheatsheet.md`. Reference implementation: the statue (Religion, DC 17) and factor (Diplomacy, DC 23) checks on `quest-the-narrows-job.html`.

**Conventions:** no em-dashes (en-dashes for numeric ranges only); affirmative prose; mortals not humans; all links absolute; canon-consistent names. GM-tier content is welcome and expected here.

**Wire it in:**

1. **`campaigns/assets/gm-nav.js`** — add the quest to the GM sidebar tree under its campaign; the entry's slug must match the page's `data-page`.
2. **`campaigns/<campaign>/index.html`** — add a card for the quest in the campaign hub.
3. **`docs/site-inventory.md`** — add the page to the GM-only roster section (campaign layer is not in the published rosters).
4. **Maps** — confirm the committed copy is the downsized web image and any full-res original is in `_full/` (gitignored). If a full-res file is tracked outside `_full/`, untrack it.

## Phase 7: Foundry export (optional, invoke foundryExport)

If the user runs their table on Foundry VTT, turn the quest's encounters + loot into a **paste-and-run Foundry Script Macro** that builds the quest's actor folder (with **Monsters / NPCs / Loot** subfolders), imports one actor per distinct monster (the GM drops *N* tokens), renames imported NPCs (or makes a blank `npc` for narrative-only ones), creates a loot-actor "chest" per haul with items + coins, and **optionally pre-places tokens** on the scene the GM has open. The macro resolves everything **by name** from the user's own installed compendiums, so it ships no Paizo data and always matches their system version. No module, relay, or API key; it runs in the GM browser and works on Forge-hosted worlds. Full reference: [`campaigns/tools/foundryExport/README.md`](../../../campaigns/tools/foundryExport/README.md).

To make the spec **fall out of the build**, save the `--json` from each
`pf2e-encounter` (Phase 4) and `pf2e-loot` (Phase 5) run; the `spec` subcommand
turns them straight into a spec, no hand-mapping.

1. **Assemble the spec** with `foundry_macro.py spec` (from `campaigns/tools/foundryExport/`): pass the saved encounter JSONs (`--encounter room1.json room2.json …`, members merged by name), the loot JSON(s) (`--loot haul.json`, one chest each, `--chest-name` to name them), and the NPCs (`--npc "The Venomqueen=Drow Priestess"` promotes a boss out of the monster list into a renamed import; `--npc "Innkeeper Bren"` makes a blank statless npc). For **token placement**, add `--areas <the Phase-3 map-area-editor export>` and one `--place "AREA=Name[*N][:disp]"` per group (e.g. `--place "1 · Entry=Goblin Warrior*6"`, `--place "5 · Brood=The Venomqueen:hostile"`); area labels match the drawn areas. Save to `<slug>.spec.json`. To grow the spec area-by-area as you build, add `--merge <prior.spec.json>`.
2. **Generate the macro:** `python foundry_macro.py build --spec <slug>.spec.json --out <slug>.js`.
3. **Surface it.** Hand back the macro (and the spec) plus the paste-instructions (Create Macro → type `script` → paste → run as GM; **for token placement, open the quest's scene first** so it is the viewed scene). Do not attempt to push into a live world; the macro is the deliverable. Loot item names resolve exactly because `items.db` is built from the same `equipment-srd` pack the macro reads.

---

## Hard rules

- **GM-only, always.** Everything this skill writes lives under `/campaigns/` and is never added to the player sidebar (`assets/site-nav.js`). The GM sidebar is `campaigns/assets/gm-nav.js`.
- **Real data, never invented.** Encounter budgets, creature stats, item levels and prices come from the tools and the source JSON via the leaf skills. If a number is not grounded, it does not ship.
- **Party level + size first.** Capture them in Phase 1; all encounter and loot math depends on them.
- **DCs are the challenge, not the party.** Set every skill-check DC from the task's own level or proficiency (Simple DC for knowledge, the NPC's level for social, the hazard's level for traps), then adjust for difficulty and rarity; never default to the party level. Reference: `campaigns/gm-reference/dc-cheatsheet.md`.
- **Canon-consistent.** NPCs, places, gods, and neighbours reconcile with the player lore. A quest may reveal GM-tier truth; it may not contradict committed canon.
- **Claude surfaces map links and downsizes; the user downloads and draws.** Claude searches the CzePeku / Tom Cartos / Lost Atlas catalogs and presents 3-5 options as links, but never fetches or commits the art — the user downloads it from their subscription. The user provides the full-res (it lives in gitignored `_full/`); **Claude generates the committed ~800px web copy** the page references. Areas come from `map-area-editor.html` (or an explicit chat room-list), not from invention.
- **Surface at every seam.** Premise -> structure -> areas -> encounters -> loot -> page. Pause and surface before each write, and before the HTML build.
- **No em-dashes; affirmative prose; mortals not humans.** The project-wide prose rules apply to GM pages too.

## Common pitfalls

- **Skipping the canon read.** A quest set in a real domain must match its page; grep the place-name and read the domain page in Phase 0.
- **Inventing map areas.** The room list is the user's exported JSON. Wait for it.
- **Inventing stats to save a tool run.** Run the leaf skills; read the JSON. The whole point of the tooling is reality-accurate numbers.
- **Flat difficulty.** Vary threat and shape per room (Phase 4) so the crawl has an arc; a dungeon of five identical moderate fights reads dead.
- **Loot off the party's level.** Use the hand-out or value math; do not drop a high-level item because it fits the theme.
- **Publishing subscription map art.** Full-res stays in `_full/`; the page references the downsized copy only.
- **Chronicler-voice creep.** This is GM material; write plainly and mechanically. Save the in-world voice for the read-aloud boxes.
