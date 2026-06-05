---
name: pf2e-encounter
description: Build a PF2e (2e Remaster) combat encounter to an exact XP budget from a theme, using the local bestiary tool at campaigns/tools/encounterBuilder/. Trigger on "build an encounter", "encounter for the [room/dungeon]", "[trivial/low/moderate/severe/extreme] fight for N level-M PCs", "what monsters for [theme]", "give me a [boss/horde] of [creature type]", "search the bestiary for [theme]", or any request to staff a room/scene with thematically-matched creatures at a correct PF2e difficulty. Used standalone and as the encounter phase of the quest-workflow skill. The tool draws on ~5,900 real Foundry creatures (every bestiary + Monster Core + NPC gallery), so picks and budgets come from real data, not memory. Do not use for loot/treasure (that is pf2e-loot) or for non-PF2e systems.
---

# pf2e-encounter

Drive `campaigns/tools/encounterBuilder/encounter.py` to assemble a PF2e encounter to a precise XP budget from a theme, then ground it in the real creature data. **The DB is a search index; the authoritative stat block is the creature's source JSON.** Never invent stats.

## Preconditions

The tool runs fully offline against two SQLite snapshots that are **gitignored** (rebuildable), so on a fresh checkout they may be absent.

1. Check `campaigns/tools/encounterBuilder/bestiary.db` exists.
2. If missing, run `python rebuild.py` from `campaigns/tools/encounterBuilder/` once. First run clones the Foundry pf2e repo sparsely (a few minutes, network); later runs are instant and offline.
3. Run all commands from the `campaigns/tools/encounterBuilder/` directory (`python encounter.py …`). Windows: PowerShell or the Bash tool, `python` (not `python3`).

## The math (so you can explain it)

Budgets are GM Core, exact. Party of 4: trivial 40 / low 60 / moderate 80 / severe 120 / extreme 160 XP. Add per extra PC: 10/20/20/30/40. Creature XP by level relative to party: −4→10, −3→15, −2→20, −1→30, 0→40, +1→60, +2→80, +3→120, +4→160. `build` handles all of this; you supply party + threat + theme.

## Workflow

1. **Pin the parameters.** Party level, party size (default 4), threat, shape (`boss` one big threat + chaff / `elite` a tough pair-trio / `spread` several near-level / `horde` many weak). If the caller gave a room/scene instead, infer threat and shape from its role (set-piece → severe/extreme boss; patrol → low/moderate spread; swarm room → horde).
2. **Translate the theme into filters** (see cheatsheet). Default to `--core` to cut the AP/Society stat-variant noise ("(1-2)", "(PFS 2-05)"). Start broad (one `--text` or `--family`), then narrow.
3. **Eyeball the pool with `search` first** (especially `-v` for defenses/speeds/senses), so the build draws from creatures you have actually looked at. Adjust filters until the pool reads right.
4. **Build.** `python encounter.py build --party-level L --party-size N --threat T --shape S <theme filters> --core --seed K`. Reads back budget, spent XP, fill %, and members. A stderr warning means the themed pool was too thin to reach the floor: widen the theme or lower the threat.
5. **Ground every pick in reality.** For each chosen creature, read its JSON under `_sources/pf2e/packs/pf2e/<pack>/<slug>.json` for the real Perception, saves, attacks, damage, and signature abilities. The DB carries only level/HP/AC/traits/defenses/senses/caster; the sheet carries the rest.
6. **Present** the encounter: each member with count, level, role, real HP/AC and key attacks/abilities, plus the budget line (threat, spent/budget XP, fill %). Flag anything you swapped by hand and why.

## Filter cheatsheet (compose freely; same set works for `search` and `build`)

| Want | Flag |
|---|---|
| Theme by word | `--text "crypt OR grave OR tomb"` (FTS over name/traits/flavor) |
| Creature kind | `--family dragon` (trait OR name) · `--type undead` (single best bucket) |
| Exact tag(s) | `--trait incorporeal --trait mindless` (ANDed, repeatable) |
| Defenses | `--weak fire` · `--resist physical` · `--immune poison` · magnitude: `--weak-min 10` |
| Movement / senses | `--move fly` / `--move burrow` · `--sense tremorsense` |
| Spellcaster | `--caster` · `--tradition occult` |
| Carve the pool | `--not-trait incorporeal` · `--not-weak fire` · `--not-immune fire` |
| Size (fit the room) | `--size lg --size huge` (repeatable => OR) |
| Cleanliness | `--core` (general bestiaries only) · `--no-pfs` · `--rarity common` |
| Machine-readable | `--json` (search and build both) |
| Reproducible build | `--seed K` |

Full reference: `campaigns/tools/encounterBuilder/README.md`.

## Rules

- **Never invent a stat.** If a number is not in the DB or the source JSON, it does not go in the encounter. Read the JSON.
- **The budget is the spine, the theme is the flesh.** Hit the XP math first; swap creatures by hand for flavor *within* the same relative-level band so the budget holds.
- **Surface, do not silently truncate.** If the themed pool can not fill the threat, say so and offer the widen-or-lower choice rather than shipping an under-budget fight unmarked.

## Reuse

`search()` and `build()` in `encounter.py` are plain importable functions; `--json` gives structured output. When the quest-workflow orchestrator calls this skill per room, return the encounter as structured data (members + real stat-block notes) for assembly into the quest page.
