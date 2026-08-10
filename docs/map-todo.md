# Map TODO

Pending label work for the map art. The three views (terrain / kingdoms / domains) live at `published/setting/assets/maps/` as full-size originals with `display/` and `thumbs/` variants; labels are baked into the art, so canon renames accumulate **here** until the maps are next edited. Any future build that renames or adds a mapped region should add a line to this file. After replacing an original, re-run `resize.mjs` / `resize.sh` (ImageMagick) to refresh the variants.

**2026-07-05 redraw:** the maps were redone and the whole first batch landed (Earth Realm → Greenward, Shadow Steppes → Izarelai, Denbora → Valreka, Ljorsan → Ljosarn, Thousand Kingdom singular, Hareaveldi typo, Azkamour → Haldmark, Sugeiturri and Bikitsa added, Gotorlekua confirmed gone). Verified against the new kingdoms view.

## Awaiting export + variant regeneration

- **Harro Distiratsua → Harro Distiratsue** (Egulon). Canon is **Distiratsue** everywhere (glossary etymology *harro* + *distiratsu* with the drift to *-e*; egulon.md, ancestries table, and the Egulon HTML all agree). **Fixed in the map source 2026-07-05**, but the exported originals in `published/setting/assets/maps/` (and their display/thumb variants) still carry the old *-a* label. On the next map work: re-export the originals, then run `resize.mjs`.

## Backlog for the next map edit

- **Tvisol** (Brauogi/Myrkono corner). The Twin Suns + Bikitsa joint kingdom now carries the canon name **Tvisol** (2026-07-06 build); consider a kingdom-view label for it, keeping the two half-labels. Optional settlement marks: **Solkai** (sunward ferry-capital) and **Gaulabe** (shade-half oven-town).
- **Balatur Erui** (Floteyn). The 2026-08-10 build places the island *on* the Hafra/Midarra boundary: shift the island (or the sea-boundary art) so the salt/sweet line (**Gazmuga**) touches its western shore. The settlement mark on the south coast is canon-named **Gesalkai**; the central mountain is **Lomendi**. Optional: mark the **Riseway** on no view (it is a sky-lane; charts carry it, terrain art should not).
