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
python encounter.py search --type fey --source pathfinder-monster-core --no-homebrew

# Build an encounter to a threat budget
python encounter.py build --party-level 5 --party-size 4 --threat severe --type undead --shape boss
python encounter.py build --party-level 8 --party-size 5 --threat moderate --text "forest fey" \
       --shape horde --tolerance 0.1
```

Filters (`--type --trait --size --rarity --text --level --source --no-homebrew`)
compose, and the same set works for both `search` and `build`. `--trait` is
repeatable and ANDs (exact junction filtering); `--source` takes a pack folder
name (e.g. `pathfinder-monster-core`). Shapes: `boss`, `elite`, `spread`, `horde`.
`--seed` makes a build reproducible. `--tolerance 0.1` lets a build stop at 90%+
of budget instead of always cramming to 100%; if the filtered pool is too thin to
reach the floor, the build prints a warning to stderr.

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
  full trait list is preserved in `creature_traits` for precise filtering.
- Worth adding next: **weaknesses/resistances columns** (for theming around energy
  types, e.g. "fire-vulnerable swamp things") and, once query shapes settle,
  wrapping `search()`/`build()` as an **MCP server** (they're already plain,
  importable functions). `--source`/`--no-homebrew` and the tolerance band are done.
```
