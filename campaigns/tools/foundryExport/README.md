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

This is the **Foundry export step (Phase 7)** of the [`quest-workflow`](../../../.claude/skills/quest-workflow/SKILL.md) skill, and a standalone tool you can point at *any* quest (including ones already built) to generate its macro on demand.

## Why a macro, not a REST push

A macro runs inside your GM browser with the full `game` API. It needs **no module, no relay server, no API key**, and works identically on Forge-hosted and self-hosted worlds. It ships **zero Paizo stat data**: every actor and item is resolved *by name* from the compendiums your world already has, so the numbers always match your installed system version. The macro is plain text — it lives in the repo next to the quest and is fully inspectable.

> Verified live against **Foundry VTT 14.363 / pf2e 8.2.0**: the full
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

- **Actors:** `pf2e.pathfinder-monster-core`, `-monster-core-2`, `pathfinder-npc-core`, `npc-gallery`, `pathfinder-bestiary`, `-2`, `-3`, then **every other** Actor compendium in the world (your homebrew / Forge-shared packs included) as fallback.
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

1. **Prompts.** A per-quest `*.portraits.json` holds each NPC's invented
   appearance (ancestry/age/looks) + a style-consistent `prompt`, with a shared
   `style` suffix so the whole cast looks like one artist.
2. **Generate.** `gen_portraits.py` batch-renders one square image per entry via
   fal.ai, model-agnostic (`--model`, e.g. Flux.2 [dev] now, swap later); the
   same prompts JSON is reusable by a local ComfyUI/Replicate runner.
   `pip install fal-client requests`, `set FAL_KEY=...`, then:
   `python gen_portraits.py --portraits <quest>.portraits.json --out <dir> --model fal-ai/flux/dev`
3. **Upload.** On The Forge, `upload_forge.py` pushes the folder into your Assets
   Library via the Forge API (needs a Forge API key with write-assets, in a
   gitignored `forge_key.txt`); it prints + saves a `{filename: asset URL}` map:
   `python upload_forge.py --dir <dir> --target furrious-five/below-the-quiet-docks --out forge_urls.json`
   (Self-hosted, or no key: drag the `<dir>` into a Foundry file-picker instead.)
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

1. **Frame art.** Faction/monster frame prompts live in `faction-frames.json`
   (same shape as the portraits file); render them with `gen_portraits.py` into a
   `frames/` dir. They can be ornate rings on any background - transparency is
   not required.
2. **Bake.** `tokenize.py` circle-crops the portrait, masks the frame to a clean
   circular **annulus** (keeps the outer band, drops center + corners), and lays
   it over the rim -> one RGBA token PNG with transparent corners:
   `python tokenize.py bake --portrait portraits/sable-rei.webp --frame frames/bridge-council.webp --out tokens/sable-rei.png`
   or `tokenize.py batch --portraits portraits --frames frames --out tokens --map faction_frames.json --default frames/generic.webp`.
   `--inner` controls the portrait/band split (default 0.84).
3. **Use it.** Upload the `tokens/` dir (upload_forge.py), then assign the framed
   image to the **token only** with the ring **off** - keep the un-framed
   portrait as the actor `img`. (assign-images sets both with the ring on; for
   baked frames assign the token texture and set `prototypeToken.ring.enabled`
   false so the border is not doubled.)

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
- **You place tokens and add art.** The macro stops at "folder full of ready actors + a loot chest." Token placement, prototype-token art, and scene work stay manual by design.
- **Idempotency guard.** The folder-exists check prevents accidental double-imports; delete and re-run to rebuild from an edited spec.
