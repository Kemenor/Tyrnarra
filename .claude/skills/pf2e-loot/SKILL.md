---
name: pf2e-loot
description: Assemble a PF2e (2e Remaster) treasure haul, either the official Party-Treasure-by-Level hand-out or an arbitrary gp value, themed and priced from real Foundry item data, using the local tool at campaigns/tools/encounterBuilder/loot.py. Trigger on "assign loot", "treasure for [the dungeon/level/party]", "what loot for N level-M PCs", "a [theme] haul", "reward for this quest", "search the items/equipment for [theme]", or any request to give out level-appropriate, themed treasure (permanent items, consumables, coins). Used standalone and as the loot phase of the quest-workflow skill. Draws on ~5,600 real items with real level, price, type, traits. Do not use for building combat encounters (that is pf2e-encounter).
---

# pf2e-loot

Drive `campaigns/tools/encounterBuilder/loot.py` to assemble a level-appropriate, themed treasure haul from real item data. The treasure tables are verified column-for-column against [AoN Rules 2656](https://2e.aonprd.com/Rules.aspx?ID=2656). **The DB indexes items; read an item's source JSON for its full rules/activation when writing it up.**

## Preconditions

Same as pf2e-encounter: the snapshots are gitignored/rebuildable.

1. Check `campaigns/tools/encounterBuilder/items.db` exists.
2. If missing, run `python rebuild.py` from `campaigns/tools/encounterBuilder/` once (it builds both `bestiary.db` and `items.db`).
3. Run from the tool directory (`python loot.py …`), `python` not `python3`.

## Two modes

- **Hand-out (default, no `--value`/`--share`)** — the official basket for the level: permanent items at 2×(L+1)+2×L, consumables at 2×(L+1)+2×L+2×(L−1), plus the table's currency lump. Levels 1 and 20 use the special rows; party size adds/removes one permanent + one consumable at L per PC off 4 and adjusts currency per the per-PC column. Use this for "the party's treasure for this level/dungeon."
  `python loot.py build --party-level 5 [--party-size 6]`
- **Value / share** — `--value 450` sets a gp target directly; `--share 0.33` is a fraction of the level's total (party-size scaled). Permanent items are held to `--perm-share` (default 0.5) and coins absorb the remainder, so the haul lands on the number. Use this for a single room, a milestone, or a deliberately partial reward.
  `python loot.py build --party-level 8 --party-size 5 --share 0.33`

## Workflow

1. **Pick the mode.** Whole-level reward → hand-out. A specific room or a "worth about X gp" reward → `--value`/`--share`.
2. **Theme it.** `--text "fire OR flame OR ash"`, `--trait magical`, `--not-trait cursed`, `--rarity`, `--source`. Same FTS + trait grammar as the bestiary tool. `--seed K` reproduces.
3. **Inspect candidates with `search` when hand-picking** a marquee item: `python loot.py search --type weapon --trait magical --level 5-8 --price-max 500 -v`. Filters: `--type` (weapon/armor/shield/equipment/consumable/ammo/treasure, repeatable => OR), `--level`, `--price-min/--price-max` (gp), `--trait/--not-trait`, `--rarity`, `--category` (martial/heavy/elixir…), `--group` (sword/bow…), `--permanent/--consumable`, `--source`, `--text`, `--json`, `-v`.
4. **Write it up from reality.** For the items that matter (the magic items, the signature consumable), read the source JSON under `_sources/pf2e/packs/pf2e/equipment/<slug>.json` for the actual activation, effect, and rules text. The DB carries name/level/price/type/traits/rarity, not the full description.
5. **Present** the haul: permanent items, consumables, coins, the assembled total versus the book/target value (fill %). Note that hand-out totals run near but not exactly on the book value, because real item prices vary around the idealized figures; that is expected.

## Rules

- **Level-gate everything.** A haul should match the party's level; the hand-out enforces it, and value mode clusters item levels around the party level. Do not drop a level-12 item in a level-3 haul because it fits the theme.
- **Read the item, do not paraphrase from memory.** Activation costs, durations, and bonuses come from the JSON.
- **Consumables are type=consumable only** in `build` (no ammo or gem spam); if you want ammunition or art objects as flavor, add them by hand from `search`.

## Reuse

`search()` and `build()` are importable; `--json` returns the basket as structured data. When the quest-workflow orchestrator calls this skill, return the haul structured (permanent/consumable/coins + per-item source notes) for assembly into the quest page's treasure section.
