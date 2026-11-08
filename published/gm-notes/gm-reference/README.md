# GM Reference

The guides for building GM-layer material: start here, then follow the row for what you are making.

| Making | Guide |
|---|---|
| An NPC: depth, fields, Level and Non-Combat Level, the numbers grid | [`npc-block.md`](npc-block.md) |
| A DC: by level, simple DCs, adjustments, the four degrees | [`dc-cheatsheet.md`](dc-cheatsheet.md) |
| A Recall Knowledge check: voice, falsehoods, plain / lenses / stacked | [`recall-knowledge.md`](recall-knowledge.md) |
| A quest, premise to built GM page | the `quest-workflow` skill (`.claude/skills/quest-workflow/SKILL.md`) |
| An encounter to an XP budget; a treasure haul | the `pf2e-encounter` and `pf2e-loot` skills (`tools/encounterBuilder/`) |
| A clickable map | draw areas in `published/gm-notes/tools/map-area-editor.html` (served by `tools/map-area-server.py`), fill the page with `tools/map_areas_html.py`; the pattern is in `docs/campaign-layer.md` |
| NPC and place art | the `image-prompts` skill for the words, the `npc-art` skill and `tools/imageGen/README.md` for rendering; species from `tools/imageGen/ancestries.json` |
| Foundry: actors, tokens, journals | `tools/foundryExport/README.md` (`foundry_macro.py`, `quest_journal.py`, `upload_foundry.py`); NPC actors take the Non-Combat Level as their actor level |
| Page chrome: classes, nav, the GM / player split | `docs/campaign-layer.md` |

The prose rules of the whole project (no em-dashes, affirmative phrasing, *mortals*) hold here too; see `CLAUDE.md`.
