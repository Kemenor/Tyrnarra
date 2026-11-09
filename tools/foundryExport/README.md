# foundryExport — quest → Foundry VTT import macro

Turns a compact **quest spec** into a paste-and-run **Foundry Script Macro** that,
when you run it as GM, builds the quest's actor folder (with tidy
**Monsters / NPCs / Loot** subfolders) and fills it:

- one **Actor** per distinct monster (you drop *N* tokens yourself — one actor, many tokens),
- named **NPCs**, either imported from a stat-block base and renamed, or created as a blank statless `npc` (generic token, art later),
- one **loot-actor "chest"** per haul, with its items (correct quantities) and coins,
- *(optional)* **pre-placed tokens** on the scene you have open — fanned out, grid-snapped, disposition set,
- *(optional)* **portrait + circle-masked token art** on NPCs from generated images (Dynamic Token Ring).

Subfolders are created only for non-empty categories. Imports use `keepId:false`
so a boss that shares a base creature with regular monsters (e.g. a renamed
Goblin Warrior boss alongside Goblin Warrior chaff) imports as two distinct
actors rather than colliding on the compendium's id.

This is the **Foundry export step (Phase 7)** of the [`quest-workflow`](../../.claude/skills/quest-workflow/SKILL.md) skill, and a standalone tool you can point at *any* quest (including ones already built) to generate its macro on demand.

## Setup (dependencies + API keys)

Run the Foundry commands here (`tools/foundryExport/`). **Image generation lives in [`../imageGen/`](../imageGen/README.md)** — local ComfyUI/FLUX.2 via `npc_art.py`, Claude-operated through the `npc-art` skill, no API key.

**Dependencies** (one-time): `pip install requests pillow numpy` here.
(encounters/loot also need the encounterBuilder DBs: `python ../encounterBuilder/rebuild.py`.)

**The Foundry server.** Foundry is self-hosted on the home network (Docker on a
Raspberry Pi). No key is needed: `upload_foundry.py` copies art with rsync over
ssh. Its address stays **out of this public repo**, in
`~/.config/tyrnarra/foundry-remote` on each machine (`<ssh-host>:/<foundry-root>`,
the root holding `data/Data/`), or `TYRNARRA_FOUNDRY`. Set a machine up with
[`../README.md`](../README.md); `python3 ../check_setup.py` verifies it.

**Campaigns → worlds.** [`campaigns.json`](campaigns.json) maps each repo campaign
(the folder under `published/gm-notes/`) to its Foundry world id (the folder
under `Data/worlds/`); `null` means the campaign has no world yet. Add a line
when a campaign gets a world.

**Confirmed working:** Foundry VTT **14.368** / pf2e on the self-hosted server; local renders are free (FLUX.2 dev on the desktop's GPU). Foundry serves its `Data/` folder at the site root, so uploaded art is addressed by the relative path `worlds/<world>/assets/<sub>/<file>`.

## The full pipeline, end to end

A quest goes from premise to a populated, art-framed Foundry scene through these steps. Each is a standalone command; stop at any layer.

1. **Encounters + loot** — drive `pf2e-encounter` / `pf2e-loot` (../encounterBuilder), saving each `--json`.
2. **Spec** — `foundry_macro.py spec …` → `<quest>.spec.json` (monsters, NPCs, chests, areas, placement).
3. **Import macro** — `foundry_macro.py build --spec …` → paste-run in Foundry: foldered actors + loot, tokens placed on the open scene.
4. **Portraits** — invoke the **`npc-art` skill**: Claude distills each NPC's block into a spec and renders locally (`../imageGen/npc_art.py`, variations → set → upscale, user picks in chat) → `<campaign>/assets/portraits/`.
5. **(optional, user-directed) Faction frames** — tokens are per-faction and most NPCs get none. When a new frame is wanted: extend the shared `tools/token-frames/faction-frames.json`; render the magenta-field ring with `npc_art.py frame`; `bake_token.py prep` (hue chroma-key) → `*.cut.png`; map actors→frames in `<quest>.token-map.json`; `bake_token.py batch` → `<campaign>/assets/tokens/<slug>.png`.
6. **Upload** — `upload_foundry.py --dir <art dir> --campaign <campaign> [--sub tokens/npc]` → copies into `worlds/<world>/assets/<sub>/` on the server and prints the `--base` to use.
7. **Assign** — `foundry_macro.py assign-images --folder "<quest folder>" --base "worlds/<world>/assets/<sub>/" [--token-only --no-ring] --map "Name=file" …` → paste-run; sets portraits / framed tokens and re-skins placed tokens.

The frame library is **shared, world-wide**: prompts + art live in `tools/token-frames/` (`faction-frames.json` + the `.webp`/`.cut.png` rings), reusable by any campaign — most frames are universal (domains, regions, world factions, monster types). Only the per-quest **actor→frame map** (`published/gm-notes/<campaign>/<quest>.token-map.json`, beside the quest HTML) and the per-quest **portrait/token art** (`published/gm-notes/<campaign>/assets/portraits/` + `assets/tokens/`, beside `assets/maps/`) stay with the campaign. Generated images **are committed** so the exact approved art travels with the repo; only scratch (`foundry_urls.json`, `_variant-*` test-bakes, `_reup/`) is gitignored.

## Quest journals

`quest_journal.py` turns a quest's GM pages into Foundry journals in one JournalEntry folder: each scene page as a journal (one page per section, plus one per place card), the cast page as a journal with one page per NPC (portrait on top, numbers as tables, GM secrets as Foundry secret blocks), and an art spec of place views as image pages for "Show Players". The GM-layer markup is rewritten into plain HTML, since Foundry does not load `gm.css`; links to the website are kept as words.

```bash
Q=../../published/gm-notes/short-notice/quest-the-unspent
python quest_journal.py --quest $Q --folder "The Unspent" \
    --chapter "Chapter 1: Struck Colours=struck-colours.html" \
    --cast cast.html --views art/twin-cities-views.set.json --views-title "The Twin Cities" \
    --campaign short-notice --sub the-unspent --stage _stage/the-unspent \
    --macro $Q/quest-the-unspent.journal.macro.js
python upload_foundry.py --dir _stage/the-unspent --campaign short-notice --sub the-unspent
```

Art is resized to `.webp` in `--stage` (gitignored) and referenced only when its file exists, so a re-run after new renders picks the new art up; upload the stage folder again before running the macro. Players get each journal as Observer and every page as None, so the GM reveals pages one at a time (a page's ownership, or "Show Players" on a page); GM secret blocks stay hidden on a revealed page. The macro is **add-only** by default: a journal that already exists keeps every page it has (edits made in Foundry, layout, reveals), and only pages missing by name are added. `--replace` deletes and rebuilds same-named journals instead, losing anything done in Foundry.

## Why a macro, not a REST push

A macro runs inside your GM browser with the full `game` API. It needs **no module, no relay server, no API key**, and works on any Foundry server (ours is self-hosted). It ships **zero Paizo stat data**: every actor and item is resolved *by name* from the compendiums your world already has, so the numbers always match your installed system version. The macro is plain text — it lives in the repo next to the quest and is fully inspectable.

> Verified live: the full
> create → verify → delete cycle (`Folder.create`, `importFromCompendium` with
> rename, blank-`npc` `Actor.create`, loot `Actor.create`,
> `createEmbeddedDocuments`, and the pf2e `inventory.addCoins` coin API) passes.

## Usage

```bash
python foundry_macro.py build --spec example-spec.json --out lair.js   # macro -> file
python foundry_macro.py build --spec example-spec.json                 # macro -> stdout
cat spec.json | python foundry_macro.py build                          # spec on stdin
```

Then in Foundry: **Macros (or the hotbar) → Create Macro → Type: `script` →
paste the generated JS → Save → double-click to run** (as GM). A whispered chat
summary lists everything created, plus any unresolved names. Re-running is
blocked if the folder already exists — delete that folder first to rebuild.

## The spec

```json
{
  "folder": "Venomqueen's Lair",
  "monsters": [
    { "name": "Giant Viper", "count": 4 },
    { "name": "Goblin Warrior", "count": 6, "pack": "pathfinder-monster-core" }
  ],
  "npcs": [
    { "name": "The Venomqueen", "base": "Drow Priestess" },
    { "name": "Innkeeper Bren" }
  ],
  "chests": [
    { "name": "Hoard Chest",
      "items": [ { "name": "Dagger", "count": 1 },
                 { "name": "Healing Potion (Minor)", "count": 3 } ],
      "coins": "120 gp" }
  ]
}
```

| Field | Meaning |
|---|---|
| `folder` | **required.** The Actor folder the quest's actors are imported into. |
| `monsters[]` | `name` (exact compendium name) + `count` (tokens you'll drop). One actor is imported per entry. |
| `npcs[]` | `name`. With `actor` → create a full **custom statblock** (an embedded pf2e `npc` document) for bespoke benchmark monsters. With `base` → import that creature and rename it to `name`. With neither → a blank statless `npc`. Optional `image` → portrait + circle-masked token (see below). |
| `imageBase` *(optional)* | Path prefix joined to bare `image` filenames (the folder you upload portraits into, e.g. `"portraits/"`). A per-npc `image` containing a `/` is used as-is. |
| `chests[]` | A loot actor: `name`, `items[]` (`name` + `count`), and `coins`. |
| `coins` | A `{pp,gp,sp,cp}` dict, a plain gp number, or a loot.py-style string (`"120 gp"`, `"1.5 gp"`, `"50 cp"`). |
| `pack` *(optional, on any monster/npc/item)* | Exact-pack hint. A bare repo folder name (`"pathfinder-monster-core"`) is read as `pf2e.<name>`; a dotted value (`"my-module.my-pack"`) is used verbatim. |
| `areas` *(optional)* | The map-area-editor export verbatim: `[{label, rects:[{left,top,width,height}]}]`, all percentages of the map image. Used only to position tokens. |
| `placement` *(optional)* | `[{area, name, count, disposition}]` — drop `count` tokens of imported actor `name` into `area` (matched to `areas` by label, or a numeric index). `disposition` is `hostile` (default) / `neutral` / `friendly` / `secret`. |

## Token placement (optional)

Your scenes are already prepared (Tom Cartos / Czepeku Foundry modules ship the
scene with walls + lighting). So the macro **never creates a scene** — it places
tokens onto the scene you currently have **open** (`game.scenes.viewed`, else the
active scene). Your flow stays: upload the module, open the scene, run the macro.

If the spec carries `areas` + `placement`, the macro converts each area's
percentage rectangle (same map-area-editor coordinates the quest's clickable map
tab uses) into scene pixels via `scene.dimensions`, fans `count` tokens out in a
grid-snapped block centered on the area, and sets disposition. Multiple tokens of
one actor don't stack. The scene name is reported in the summary so a wrong open
scene is obvious. No `placement`, or no scene open → it simply skips placement and
still builds the folder; an unmatched area or actor is reported, never guessed.

## Name resolution

Names are matched against the world's compendiums, **remaster-first**, mirroring
`encounter.py`'s dedup preference:

- **Actors:** `pf2e.pathfinder-monster-core`, `-monster-core-2`, `pathfinder-npc-core`, `npc-gallery`, `pathfinder-bestiary`, `-2`, `-3`, then **every other** Actor compendium in the world (your homebrew and installed modules such as Battlezoo included) as fallback.
- **Items:** `pf2e.equipment-srd` first (where `loot.py`'s item DB comes from), then every other Item compendium.

Use an exact `pack` hint when a name is ambiguous across packs, or to force a
homebrew version. Unresolved names are **reported in the chat summary, never
silently dropped** — fix the spelling (names must match the compendium exactly,
e.g. `Healing Potion (Minor)`, not `Minor Healing Potion`) or add a `pack` hint.

## NPC portrait / token images

The tool doesn't generate art (no image model here), but it owns everything
around it: tuned prompts and the Foundry-side assignment. NPC tokens use
**portrait busts as circle-masked tokens** via Foundry's **Dynamic Token Ring**
(disposition-coloured), the same image doubling as the actor portrait.

The four steps:

1. **Prompts.** Claude distills each NPC's physical + clothing block into a
   per-NPC `<slug>.set.json` spec at generation time, with the shared house style
   (painterly) so the whole cast looks like one artist.
2. **Generate.** The **`npc-art` skill** renders locally (`../imageGen/npc_art.py`,
   ComfyUI/FLUX.2 on this machine, no key): Claude authors the spec from the NPC's
   block and renders square portraits the user approves in chat.
3. **Upload.** `upload_foundry.py` rsyncs the folder into the campaign's world
   on the self-hosted server (`Data/worlds/<world>/assets/<sub>/`, default
   `tokens/npc`, the worlds' existing convention). It never deletes what is
   already there, prints the `--base` for step 4, and can save a
   `{filename: foundry path}` map:
   `python upload_foundry.py --dir <dir> --campaign furrious-five --out foundry_urls.json`
   (`--world <id>` targets a world directly; `--list-worlds` shows them.)
4. **Assign.** Either bake `image` filenames into the spec so a fresh import
   sets them, or, for an already-imported quest, generate a one-off assignment
   macro that matches names → files on the existing actors (and re-skins their
   placed tokens):
   `python foundry_macro.py assign-images --folder "<quest folder>" --base "portraits/" --map "Davo Kenn=davo-kenn.webp" --map ...`

The assignment sets `actor.img` + `prototypeToken.texture.src` + enables the
token ring; placed tokens inherit it (or are re-skinned by `assign-images`).

## Token frames (faction borders, Tokenizer-style)

Foundry's Dynamic Token Ring only gives a generic disposition ring. For custom
per-faction / special-monster borders, bake a frame into the token image:

1. **Frame art.** Frame prompts live in the shared library
   `tools/token-frames/faction-frames.json`; render with
   `../imageGen/npc_art.py frame --name <slug> --desc "<motif>"` into
   `tools/token-frames/`. The ring renders on a **solid magenta field**
   (background AND centre) so only the ring is non-magenta. Frames are reusable
   across campaigns — add a new one once, map to it from any quest's token-map.
2. **Cut.** `bake_token.py prep` chroma-keys the magenta away, leaving the ornate
   ring with real transparency (no gray edge):
   `python bake_token.py prep --in frames/bridge-council.webp --out frames/bridge-council.cut.png`
   (Hand-cut transparent frame PNGs skip this step and bake directly.)
3. **Bake.** `bake_token.py` circle-crops the portrait and composites the
   transparent ring, **auto-fitting** it to the token edge (scales by its alpha
   bbox, so any ring size lands as a proper border) -> one RGBA token PNG with
   transparent corners:
   `python bake_token.py bake --portrait <campaign>/assets/portraits/sable-rei.webp --frame ../token-frames/sable-rei.cut.png --out <campaign>/assets/tokens/sable-rei.png`
   or `bake_token.py batch --portraits <campaign>/assets/portraits --frames ../token-frames --out <campaign>/assets/tokens --map <quest>.token-map.json` (frames resolve from the shared library by stem).
   (Opaque frames with no alpha fall back to an annulus mask; `--inner` tunes that band.)
4. **Pop-out (optional).** For a head or an arm that breaks the border, cut the portrait's figure out of its background, then name the boxes (fractions of the token) where the figure goes back over the ring:
   `uvx --python 3.12 --from "rembg[cpu,cli]" rembg i -m birefnet-portrait <portrait>.png <slug>-cutout.png` (Python 3.12 through `uvx`, since rembg has no wheels for the system Python; the model downloads once, about 1 GB, into `~/.rembg/`), then
   `python bake_token.py bake --portrait <portrait>.png --frame <frame>.cut.png --cutout <slug>-cutout.png --pop 0.36,0,0.64,0.16 --pop 0,0.38,0.22,0.78 --out <campaign>/assets/tokens/<slug>.png`
   (here: Ninehulls' head at the top and his right arm on the left). Keep the cut-out beside the portrait as `<slug>-cutout.png`. `--zoom` and `--dy` move portrait and cut-out together, to push the figure further over the ring: `--ring` draws the frame smaller than the token and `--ring-dy` moves it down, leaving room above it for a head to come out. Ninehulls' token is `--ring 0.88 --ring-dy 0.06 --zoom 1.25 --dy 0.085 --pop 0.28,0,0.72,0.24 --pop 0,0.3,0.26,0.62`: his head out above the ring, his arm over it, the hand back inside.
   **For a whole cast, head only:** `bake_token.py headpop` does it without boxes. Give it the portraits, their cut-outs (`<slug>-cutout.png`, from one `rembg p -m birefnet-portrait <in-dir> <out-dir>` batch through `uvx`) and a map `{frame: [slugs]}`; for each it moves the figure so the head sits just under the token's top edge, draws the frame a little smaller and lower, and lifts only the head's widest run of columns over the band (a stray bit of the cut-out stays inside). A head already cut off at the top of the art is lifted where it is; a head that sits low in its art is zoomed in a step (1.1 to 1.3) until it clears the band; a token listed under `"_by_hand"` in the map stays at zoom 1 and is flagged for a pass in Pinta. Every bake cuts the portrait to the **inside** of the ring: rays from the ring's centre take the longest stretch of frame along each as the band (a thin rope line or a tiny airship inside the ring is skipped and erased), and the portrait reaches 3 px under the band, so nothing shows outside the frame. `prep` ends with `solidify`, which makes the ring opaque (the magenta key leaves near-key colours half-transparent); `bake_token.py solidify <frame>.cut.png` fixes an older frame (`--floor` is 24; a frame with a soft drop shadow, like `lautara`, wants 90). The Unspent's map is `quest-the-unspent.token-map.json`:
   `python bake_token.py headpop --portraits <quest>/art --cutouts <quest>/art --map <quest>/quest-the-unspent.token-map.json --out <campaign>/assets/tokens`
5. **Use it.** Upload the `<campaign>/assets/tokens/` dir (upload_foundry.py), then assign with the
   token-only / ring-off flags (keeps the un-framed portrait as the actor `img`,
   no doubled ring):
   `python foundry_macro.py assign-images --folder "<quest>" --base "<tokens-url>/" --token-only --no-ring --map "Sable Rei=sable-rei.png" --map ...`

> **Caution on a live scene.** `assign-images` re-skins already-placed tokens by
> **deleting and recreating** them (pf2e reverts a direct texture update), which
> gives them new ids. On a scene with an **active combat**, recreating a
> *combatant's* token orphans it from the tracker. Re-skin before a session, or
> on a paused scene check the Combat Tracker afterward and re-add any boss whose
> token you replaced.

## Assembling a spec from the leaf tools (Phase 7)

The `spec` subcommand builds a spec straight from the encounter/loot tools'
`--json` output, so the spec **falls out of the quest build** instead of being
hand-mapped:

```bash
python foundry_macro.py spec --folder "Broodmother's Hollow" \
    --encounter room1.json room2.json \      # encounter.py build --json (one per area)
    --loot haul.json --chest-name "Egg-Sac Cache" \   # loot.py build --json (one chest each)
    --npc "The Broodmother=Giant Tarantula" \  # promote a boss: import base + rename
    --npc "Trapped Miner Sela" \               # blank narrative npc
    --areas areas.json \                       # map-area-editor export (token positions)
    --place "1 . Entry=Giant Tarantula*3" \    # AREA=Name[*N][:disp]; default disp hostile
    --place "5 . Brood=The Broodmother:hostile" \
    --out broodmother.spec.json
python foundry_macro.py build --spec broodmother.spec.json --out broodmother.js
```

The mapping:

- `encounter.py build --json` → `members[]` are merged across all `--encounter` files (counts summed by name) into `monsters[]`.
- `--npc "Name=Base"` promotes a creature: it becomes an NPC imported from `Base` and renamed to `Name`, and one count of `Base` is removed from `monsters` (the boss is no longer chaff). `--npc "Name"` (no `=`) makes a blank statless npc.
- `loot.py build --json` → each `--loot` file becomes one chest: `permanent[]` + `consumables[]` → `items[]`, `currency` (e.g. `"120 gp"`) → `coins`. Names match exactly, because `items.db` is built from the same `equipment-srd` pack the macro resolves against.

**Accumulate while building.** Pass `--merge <existing.spec.json>` to extend a
saved spec as each area is finished (monsters summed, npcs/chests appended), so
the spec grows room-by-room through the quest build and is ready at Phase 7.

`make_macro(spec)`, `spec_from_tools(...)` and `coins_to_dict(value)` are
importable for an orchestrator that builds the spec in-process.

> Verified live end-to-end: real `encounter.py` picks (Giant Tarantula boss +
> Wasp Swarm) and a real `loot.py` handout (10 items + 120 gp) assembled into a
> spec and imported into Foundry with **zero unresolved names**.

## Conventions

- **One actor, many tokens.** Six goblins = one imported Goblin Warrior actor; you place six tokens at the table. Each token is its own combatant.
- **You place tokens and add art, unless the spec asks.** By default the macro stops at "folder full of ready actors + a loot chest"; pre-placed tokens and portrait/token art are the opt-in steps above, and scene work stays manual.
- **Idempotency guard.** The folder-exists check prevents accidental double-imports; delete and re-run to rebuild from an edited spec.
