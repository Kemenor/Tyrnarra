# pf2e-prep

A static, rebuildable PF2e creature index for thematic encounter prep. Built so
Claude Code can search the bestiary by theme and draft encounters to a precise
PF2e budget that you then tweak by hand.

## How it fits together

```
foundry pf2e repo  ─┐
                    ├─> build_db.py ─> bestiary.db ─> encounter.py (search + build)
homebrew/*.json   ─┘     (SQLite + FTS5)
```

- **bestiary.db** is a static snapshot. Nothing queries the network at prep time.
- **rebuild.py** is the prestart/cron hook: it syncs the Foundry repo and
  rebuilds the DB from official packs + your homebrew. Cross-platform (no bash),
  reproducible and offline after the first sync. It discovers creature packs from
  the git tree (every bestiary, Monster Core, NPC gallery), so new AP/Lost Omens
  packs are picked up automatically.

## Setup

```bash
python rebuild.py     # first run clones + builds (~6k creatures); later runs pull + rebuild
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
| `--size` | tiny / sm / med / lg / huge / grg (fit the room) |
| `--type` | the single best creature-type bucket (undead, dragon, fey...) |
| `--trait` | exact trait; **repeatable, ANDed** (`--trait fire --trait undead`) |
| `--weak` / `--resist` / `--immune` | by defense; repeatable, ANDed. `--immune` covers damage types **and** conditions |
| `--weak-min` / `--resist-min` | magnitude floor; pairs with `--weak`/`--resist`, or alone for "any weakness/resistance >= N" |
| `--move` | movement type: `fly` / `swim` / `climb` / `burrow` / `land`; repeatable |
| `--move-min` | speed floor; pairs with `--move`, or alone for "any speed >= N" |
| `--family` | creature kind: matches a **trait or the name** (`dragon`, `construct`, `mephit`, `sphinx`) |
| `--rarity` | common / uncommon / rare / unique |
| `--source` | one pack folder, e.g. `pathfinder-monster-core` |
| `--no-homebrew` | exclude homebrew rows |

`search` also takes `-v/--verbose` (prints each result's speeds + weak/resist/immune)
and `--limit`. `build` takes `--party-level --party-size --threat --shape --seed
--tolerance`. Shapes: `boss`, `elite`, `spread`, `horde`. `--tolerance 0.1` lets a
build stop at 90%+ of budget instead of cramming to 100%; too-thin pools warn on stderr.

**Family vs. trait:** PF2e has no "family" field, so `--family` is the forgiving
knob (trait OR name) and `--trait` is the exact one. For families that are traits
(dragon, demon, construct, golem) they're equivalent; `--family` earns its keep on
name-only families (mephit, sphinx, naga, hydra, wisp).

**Full stat blocks:** the DB is a search index. Once a search narrows to a few
candidates, the authoritative sheet (Perception, saves, attacks, exact damage)
lives in that creature's JSON under `_sources/` — read it for the real numbers
rather than trusting anything not in the DB.

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
  weaknesses, resistances, immunities and speeds get their own junction tables.
- `value` is stored on weaknesses/resistances/speeds, exposed as the
  `--weak-min` / `--resist-min` / `--move-min` magnitude floors.
- The tool is meant to be driven by Claude Code (it will become a skill): search
  by theme, hand-pick creatures, build to budget, then read the source JSON for
  the chosen few. An MCP wrap is unnecessary for that (the CLI stdout is enough);
  `search()`/`build()` stay importable in case it ever helps.
```
