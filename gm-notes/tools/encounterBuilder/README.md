# pf2e-prep

A static, rebuildable PF2e index for thematic session prep. Built so Claude Code
can search the bestiary by theme and draft encounters to a precise PF2e budget,
and search the equipment list by theme to assemble level-gated loot, all from
real data that you then tweak by hand.

## How it fits together

```
                  ┌─> build_db.py    ─> bestiary.db ─> encounter.py (search + build)
foundry pf2e repo ─┤     (creatures)
                  └─> build_items.py ─> items.db    ─> loot.py (search; treasure-build planned)
homebrew/*.json ───────^ (creatures only)         all SQLite + FTS5
```

- **bestiary.db / items.db** are static snapshots. Nothing queries the network at prep time.
- **rebuild.py** is the prestart/cron hook: it syncs the Foundry repo and rebuilds
  both DBs from official packs + your homebrew. Cross-platform (no bash),
  reproducible and offline after the first sync. It discovers creature packs from
  the git tree (every bestiary, Monster Core, NPC gallery) plus the `equipment`
  pack, so new AP/Lost Omens packs are picked up automatically.

## Setup

```bash
python rebuild.py     # first run clones + builds (~6k creatures, ~5.6k items); later runs pull + rebuild
```

The full official set overlaps itself (legacy Bestiary 1-3 vs. Monster Core).
Official creatures are deduped by name, **preferring the remastered entry**;
your homebrew is never deduped away.

## Querying

```bash
# Thematic search — structured filters + fuzzy flavor text (FTS5 MATCH)
python encounter.py search --type undead --level 3-7 --text "crypt OR grave" --rarity common
python encounter.py search --trait fire --trait undead --size lg   # fire AND undead (repeatable)
python encounter.py search --weak fire --move fly --level 1-8 -v   # fire-vulnerable fliers, verbose
python encounter.py search --family mephit                         # name-only family still works
python encounter.py search --type fey --source pathfinder-monster-core --no-homebrew

# Build an encounter to a threat budget
python encounter.py build --party-level 5 --party-size 4 --threat severe --type undead --shape boss
python encounter.py build --party-level 6 --party-size 4 --threat severe --trait undead --weak fire \
       --shape elite --tolerance 0.1
```

### Filters (compose; same set works for `search` and `build`)

| Filter | Meaning |
|---|---|
| `--level lo-hi` | level range (needed for encounter math) |
| `--text "a OR b"` | fuzzy FTS5 over name / traits / flavor |
| `--size` | `tiny`/`sm`/`med`/`lg`/`huge`/`grg`; **repeatable => OR** (fit the room) |
| `--type` | the single best creature-type bucket (undead, dragon, fey...) |
| `--trait` | exact trait; **repeatable, ANDed** (`--trait fire --trait undead`) |
| `--weak` / `--resist` / `--immune` | by defense; repeatable, ANDed. `--immune` covers damage types **and** conditions |
| `--weak-min` / `--resist-min` | magnitude floor; pairs with `--weak`/`--resist`, or alone for "any weakness/resistance >= N" |
| `--move` | movement type: `fly` / `swim` / `climb` / `burrow` / `land`; repeatable |
| `--move-min` | speed floor; pairs with `--move`, or alone for "any speed >= N" |
| `--sense` | `darkvision`/`tremorsense`/`scent`/`lifesense`/`blindsight`...; repeatable, ANDed |
| `--caster` | has a spellcasting entry |
| `--tradition` | spell tradition: `arcane`/`divine`/`occult`/`primal` |
| `--family` | creature kind: matches a **trait or the name** (`dragon`, `construct`, `mephit`, `sphinx`) |
| `--not-trait` / `--not-weak` / `--not-immune` | exclude (carve the pool: undead but NOT incorporeal); repeatable |
| `--rarity` | common / uncommon / rare / unique |
| `--core` | only the general bestiaries + NPC gallery (drops AP/Society scaled-variant noise) |
| `--no-pfs` | exclude Pathfinder Society scenario packs |
| `--source` | one pack folder, e.g. `pathfinder-monster-core` |
| `--no-homebrew` | exclude homebrew rows |
| `--json` | emit JSON (full records + defenses/senses) instead of the text table |

`search` also takes `-v/--verbose` (prints each result's caster/speeds/senses/defenses)
and `--limit`. `build` takes `--party-level --party-size --threat --shape --seed
--tolerance`. Shapes: `boss`, `elite`, `spread`, `horde`. `--tolerance 0.1` lets a
build stop at 90%+ of budget instead of cramming to 100%; too-thin pools warn on stderr.
`--core` is the usual noise-cut: it drops the *(1-2)/(PFS 2-05)* stat-variants that
clutter thematic searches while keeping the canonical bestiary entries.

**Family vs. trait:** PF2e has no "family" field, so `--family` is the forgiving
knob (trait OR name) and `--trait` is the exact one. For families that are traits
(dragon, demon, construct, golem) they're equivalent; `--family` earns its keep on
name-only families (mephit, sphinx, naga, hydra, wisp).

**Full stat blocks:** the DB is a search index. Once a search narrows to a few
candidates, the authoritative sheet (Perception, saves, attacks, exact damage)
lives in that creature's JSON under `_sources/` — read it for the real numbers
rather than trusting anything not in the DB.

## Loot (items.db / loot.py)

The equipment counterpart: ~5.6k items (weapons, armor, consumables, treasure...)
with real level, price, type, traits and rarity, so loot can be themed and
level-gated against actual data.

```bash
python loot.py search --text "fire OR flame" --permanent --level 1-5
python loot.py search --type weapon --category martial --group sword --price-max 100
python loot.py search --type consumable --text healing --level 1-3 -v
```

| Filter | Meaning |
|---|---|
| `--type` | `weapon`/`armor`/`shield`/`equipment`/`consumable`/`ammo`/`treasure`; repeatable => OR |
| `--level lo-hi` | item level range |
| `--price-min` / `--price-max` | price band, in **gp** |
| `--trait` / `--not-trait` | exact trait include (ANDed) / exclude; repeatable |
| `--rarity` | common / uncommon / rare / unique |
| `--category` | weapon `simple`/`martial`/`advanced`, armor `light`/`medium`/`heavy`, elixir... |
| `--group` | `sword` / `bow` / `plate`... |
| `--permanent` / `--consumable` | kept-vs-spent split |
| `--source` | publication title (substring) |
| `--text` | fuzzy FTS5 over name / traits / flavor |
| `--json` / `-v` | JSON output / print traits inline |

### Treasure builder

Two modes, both themable and priced from real item data:

```bash
# Hand-out (default): the official Party-Treasure-by-Level basket for the level
python loot.py build --party-level 5 --text "fire cult"
python loot.py build --party-level 5 --party-size 6            # scales items + currency per PC

# Value/share: a partial or arbitrary haul
python loot.py build --party-level 8 --party-size 5 --share 0.33   # a third of the level
python loot.py build --party-level 3 --value 250                   # absolute gp target
```

- **Hand-out** (no `--value`/`--share`): the exact GM Core spread for the level —
  permanent items at 2×(L+1) + 2×L, consumables at 2×(L+1) + 2×L + 2×(L−1), plus
  the table's **currency lump**. Levels 1 and 20 use the table's special rows.
  Party size adds/removes one permanent + one consumable at L per PC off 4 and
  adjusts currency by the per-PC column. The assembled total runs near the book
  value (real item prices vary around the idealized figures).
- **Value/share**: `--value` sets gp directly; `--share` is a fraction of the
  level's total. Permanent items are held to `--perm-share` (default 0.5) of the
  target and coins absorb the remainder, so the haul lands on the number.

Theme either with `--text / --trait / --not-trait / --rarity / --source`; `--seed`
reproduces; `--json` for structured output.

> The treasure tables at the top of `loot.py` (`TREASURE_BY_LEVEL`, `CURRENCY`,
> `CURRENCY_PER_PC`, and `slots()`) are verified column-for-column against
> [AoN Rules 2656](https://2e.aonprd.com/Rules.aspx?ID=2656).

## Adding Tyrnarra / Azkataria homebrew

Drop Foundry-format actor JSON (any creature with `"type": "npc"`) into
`homebrew/`. `rebuild.py` auto-detects the folder and ingests it alongside
official content (passed as `--homebrew` to `build_db.py`). Homebrew rows carry
`is_homebrew=1` (so `--no-homebrew` excludes them) and survive dedup. Filter to
just your stuff with `--source homebrew`. No schema changes needed.

## Letting Claude Code drive it

Two options, in order of how I'd phase them:

1. **CLI first (now).** Add a short note to `CLAUDE.md` pointing at the two
   commands above. Claude Code can run `search`/`build`, read the output, and
   iterate with you. Lowest friction; nail the schema and feel here.
2. **MCP later.** Once the query shapes feel right, wrap `search()` and
   `build()` (already plain functions in `encounter.py`) as MCP tools so Claude
   gets structured returns instead of parsing stdout.

## Notes / next steps

- The encounter budget tables (GM Core) live at the top of `encounter.py` —
  trivial/low/moderate/severe/extreme and the relative-level XP table. Exact, no
  guessing.
- `creature_type` is derived from the highest-priority creature-type trait. The
  full trait list is preserved in `creature_traits` for precise filtering;
  weaknesses, resistances, immunities, speeds and senses get their own junction
  tables. `caster`/`traditions` are flattened onto `creatures` (derived from each
  actor's `spellcastingEntry` items).
- `value` is stored on weaknesses/resistances/speeds, exposed as the
  `--weak-min` / `--resist-min` / `--move-min` magnitude floors.
- The tool is meant to be driven by Claude Code (it will become a skill): search
  by theme, hand-pick creatures, build to budget, then read the source JSON for
  the chosen few. An MCP wrap is unnecessary for that (the CLI stdout is enough);
  `search()`/`build()` stay importable in case it ever helps.
```
