# Map TODO

Pending label work for the map art. The three views (terrain / kingdoms / domains) live at `published/setting/assets/maps/` as full-size originals with `display/` and `thumbs/` variants; labels are baked into the art, so canon renames accumulate **here** until the maps are next edited. Any future build that renames or adds a mapped region should add a line to this file. After replacing an original, re-run `resize.mjs` / `resize.sh` (ImageMagick) to refresh the variants.

Verified against the kingdoms view on 2026-07-05.

## Renames (canon settled, map label stale)

- **The Earth Realm → Greenward** (Brauogi). Renamed at the 2026-06-29 build (the Furrowsworn breadbasket). Canon: `lore/geography/brauogi/greenward.md`.
- **Shadow Steppes → Izarelai** (Myrkono). The outsider-tongue name was retired at the Izarelai build; the rename is swept across lore + HTML, the map is the last holdout. Canon: `lore/geography/myrkono.md`, *Izarelai, the Star Plain*.
- **Denbora → Valreka** (city label inside Galdua Jendea, Lioaru). Tani's whale-borne god-city was renamed. Canon: `lore/glossary.md`.
- **Ljorsan → Ljosarn** (city label, Egulon). Spelling fix; canon spelling **Ljosarn** (light-hearth etymology, `lore/glossary.md`).
- **Thousand Kingdoms → Thousand Kingdom** (Zuzental). The map label carries a stray plural; canon is singular.
- **Haeaveldi → Hareaveldi** (small island label off the southern coast). Typo of the Lioaru sub-region's name.
- **Azkamour → Haldmark** (the north-western Brauogi march). The march was renamed at the Haldmark build (the Kholo Kept March, fully Brauogi now rather than a shared Vindul/Brauogi border); *Azkamour* survives only as its principal frontier trade-town, so the old name can stay on the map as a town label on the Hafra-and-border edge. Canon: `lore/geography/brauogi/haldmark.md`.

## Additions (canon exists, not yet drawn/labelled)

- **Sugeiturri** (Brauogi): the Dragonet source-country, built 2026-06-23. Northern Brauogi from the Hafra coast up the **Iturmen** source-mountains, carved from the Earth Realm's northern uplands plus the inland shoulder of the march now called Haldmark; the border between Greenward, Sugeiturri, and Haldmark needs drawing. Canon: `lore/geography/brauogi/sugeiturri.md`.
- **Bikitsa** (Myrkono): the northern coastal sub-region paired with Twin Suns across the domain border. Add when the Bikitsa/Twin Suns build lands (the last unbuilt Myrkono sub-region; see `open-threads.md`).

## Verify against current art

- Whether **Gotorlekua** appears anywhere (retired 2026-06-13; its ground is the Eraztumen interior, Lurrath's territory). Not spotted on the kingdoms view; confirm on terrain/domains.

*(Vernua Dominion, spotted north-east on the kingdoms view, checked out fine: it is the canon Nashavel sub-region housing Nahaskel; see `lore/geography/nashavel.md`.)*
