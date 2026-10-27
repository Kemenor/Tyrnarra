# Region-page generators

Private build tooling (not served). Each `build_<slug>.py` writes a region's published Style B page from its lore deep file and its in-world document, so the page cannot drift from the lore. Shared helpers (Markdown-to-HTML inlining, section slicing, voice quotes, panels, ◈ and ⚿ boxes, log cards) live in `pagegen.py`.

Run a builder from the repository root:

```
python3 tools/region-pages/build_river_duchies.py
```

**Rule:** when a canon move touches a region whose page is generated, re-run its builder; never hand-patch the page. A new build copies the nearest builder and remaps its sections.

| Page | Builder |
|---|---|
| `published/setting/talan/domains/lioaru/hareaveldi/hareaveldi.html` | `build_hareaveldi.py` |
| `published/setting/talan/domains/lioaru/auran/auran.html` | `build_auran.py` |
| `published/setting/talan/domains/lioaru/river-duchies/river-duchies.html` | `build_river_duchies.py` |
| `published/setting/talan/domains/sumendar/haraour-eliza/haraour-eliza.html` | `build_haraour_eliza.py` |
| `published/setting/talan/domains/sumendar/red-dominion/red-dominion.html` | `build_red_dominion.py` (also copies the sketches from `tools/imageGen/scenes/red-dominion/`) |

**Hand-built pages with synced parts:** the Heartcourt page (`published/setting/talan/domains/lautara/emarrea/heartcourt.html`) is hand-built; `sync_heartcourt_letters.py` replaces the body of each *Letters from Biozuri* column on it from `lore/geography/lautara/heartcourt-letters.md`, matched by title.

**Missing builders:** Galdua Jendea and the Lost Kingdom have no builder here. Their pages stand as published; write a builder for each (from its page and lore file) before their lore next changes.
