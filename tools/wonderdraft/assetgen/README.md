# assetgen: the art pack made for Tyrnarra, shipped with Kartofuchs as Fuchsbau

**Picking this up? Read [STATUS.md](STATUS.md) first**: the current state, the user's decisions,
what lives on which machine and how to work from the tower.

Generates our own symbol art (trees, mountains and icons) in a Tyrnarra style, with many
variants per family, to replace Wonderdraft's built-in art in `Main` (which the EULA keeps out of
any tool of our own) and the bought packs that stand in for it. The art is made in Wonderdraft's
own pack format, so it works in Wonderdraft and in Kartofuchs, which reads the same asset folder.
`build` installs straight into Fuchsbau, Kartofuchs' own pack (`art/Fuchsbau` in a Kartofuchs
checkout). The pack is tried on the real map in Kartofuchs: import `Main.wonderdraft_map` with the
"Fuchsbau" art mapping, which comes with Kartofuchs (see "Reviewing"). This tool only makes the art.

```
assetgen.sh generate conifer --seeds 1-40         # tower ComfyUI -> ~/.local/share/wdmap/assetgen/conifer/<style>/raw/
assetgen.sh build conifer --seeds 101-200 --round 7 --keep 40   # cut, check, finish, install into Fuchsbau
assetgen.sh gallery [peaks settlements ...]       # review sheets of the installed pack, by variant, numbered
```

All prompt styles in `recipes.STYLES` feed **one pack folder per family**: once greyscaled and
levelled they look alike on the map, and mixing them adds variety. `--style ink` limits
`generate` or `build` to some of them. `build` writes into `~/.local/share/wdmap/assetgen/<family>/`:
`sheet.jpg` (the installed sprites tinted grass-green), `chosen.txt` (which style and seed became
which file) and `rejects.txt` (why each other image was dropped); every raw image has a `.txt`
with its exact prompt and settings. With `--round N` all of that goes to `<family>/round-N/`
instead, and `build` keeps a copy of the round's sprites there (`round-N/sprites/`, so later
rounds can be compared with it).

The installed pack: `<Kartofuchs checkout>/art/Fuchsbau/sprites/<kind>/<Folder>/`, the checkout
`$KARTOFUCHS` (default `~/Documents/fuchs/kartofuchs`). Commit the art there after a build.

## Setup

- **ComfyUI on the tower PC** (24 GB AMD card, ROCm), started in LAN mode from its app menu
  ("ComfyUI (LAN)"); it has no login, so it listens on the home network only. The tower's
  Claude session is not allowed to start a network-exposed server itself; the owner starts it.
- **Its address stays out of this public repo**: put `http://<tower-ip>:8188` on the first line
  of `~/.config/tyrnarra/comfyui-url` on the machine running assetgen, or set
  `TYRNARRA_COMFY`. The same goes for anything else private (keys live in the gitignored
  `tools/keys/`).
- Models used: `DreamShaperXL_Turbo_v2.1` (SDXL Turbo, 7 steps, ~5 s per 832x1216 image) and
  `birefnet.safetensors` (BiRefNet Swin-L, MIT) for the built-in RemoveBackground node; FLUX.2
  dev (GGUF Q4 + Turbo LoRA, 8 steps) for the `engine: flux` families. Also on the tower:
  Juggernaut XL, NoobAI XL, IP-Adapter for SDXL.
- **The tower's server has two modes** (the tower's own Claude session restarts it on request,
  naming the mode): **sdxl** (`--cache-none --reserve-vram 2.0`, VAE on
  the GPU, ~5 s per SDXL image) and **flux** (the same plus `--cpu-vae`, ~2 min per FLUX image;
  the flags are npc_art's, tools/imageGen/npc_art.py `ensure_server` explains each). Switch modes
  between an SDXL phase and a FLUX phase: never mix the two engines in one server session, and
  never send FLUX to an sdxl-mode server (the GPU VAE fault can crash it). The plain server
  without these flags runs one FLUX image and then wedges in a load `/interrupt` cannot stop.
  FLUX graphs here skip BiRefNet: the drawings come on clean white, cut locally
  (`sprites.flood_mask`).
- **One FLUX image per graph** (`FLUX_BATCH` 1): a graph with 4 FLUX images wedges even a
  flux-mode server (the 17 GB text encoder stays in VRAM while the 19.6 GB unet loads, RAM goes
  to swap, no step ever samples). The client retries through the minutes the server stops
  answering while FLUX loads (`comfy.run`/`wait`).
- **The tower powers off** after three empty-queue checks five minutes apart: chain batches with
  a 2 s waiter so the queue never sits empty between them.
- `assetgen.sh` builds its own gitignored `.venv` (numpy, scipy, pillow) on first run.

## Wonderdraft's rules for pack art

- **Greyscale art is tinted by the ground.** Trees and mountains in `sprites/trees` and
  `sprites/mountains` are pure greyscale; Wonderdraft multiplies them by the ground colour
  sampled under each symbol (`sample` in the map). White = full ground colour, black = black.
  That is why the same tree is green on grass and white on snow. Its own conifers are
  near-white fill with black brush strokes.
- **Custom-colour art** lives in folders ending `_Cc`: red channel = colour 1 (foliage), green =
  colour 2 (trunk), blue = colour 3, dark = lines. `draw_mode: custom_colors`. Symbol (icon)
  folders take one `.wonderdraft_symbols` entry per symbol (BSG's icons, ours); given one
  folder-wide entry, Wonderdraft rewrites the file per symbol with draw mode `normal`.
- **`.wonderdraft_symbols`** in each folder (JSON): `name`, `radius` (footprint for spacing),
  `offset_x`, `offset_y` (sprite centre relative to the click point, in scale-1 px),
  `draw_mode` (`sample_color` or `custom_colors`). Symbols stored in a map carry their own
  copies of radius and offset.
- **A map loads only the packs in its `included_packs` list**; any other pack's symbols give a
  "Missing custom assets" dialog. `wdmap` adds used packs on every save.
- Texture paths have no extension: `user://assets/Fuchsbau/sprites/trees/Fuchsbau_Conifers/conifer_01`.
- **Size**: a symbol is drawn at sprite size x its `scale`. To replace a built-in family 1:1 the
  sprite must be as big as the built-in art at scale 1. Kartofuchs' `art-sizes.json` holds those
  sizes, measured on a calibration grid: the nine built-in `tree_xmas` are 86-206 x
  197-426 px at scale 1, area-equivalent 137 x 291, centred about 70 px above the click point,
  radius 51. In `Main` conifers are used at scale 0.1-0.6, so they end up 30-250 px tall.

## Prompting (SDXL Turbo, DreamShaper XL; FLUX.2)

What works and what does not:

1. **One subject per image, portrait 832x1216.** Each tree comes out ~1000 px tall, crisp when
   shrunk to 350. Sheets of many icons ("set of ... icons, sprite sheet") give 15-30 trees per
   image but each only 150-300 px: blurry at full size. Rows of 3-4 trees always get a ground
   line joining them and often touch; negatives do not stop it at CFG 2.
2. **Ask for the map-reading shape, not realism**: "chunky", "full rounded silhouette",
   "stylized", "thick dark outline", "bold shape readable at small size". Plain "conifer icons"
   gives thin spiky firs that turn into noise at 20-30 px. At that size all styles look alike:
   silhouette and outline matter more than style.
3. **Ask for a light fill**: "light foliage with dark ink strokes". Wonderdraft's tint needs a
   light body; dark-filled art makes black blobs in forests and grey trees in snow.
4. **Style words** that hold: "black ink outlines with soft watercolor wash shading, hand-drawn
   fantasy cartography" (ink); "sepia brown ink linework with light wash shading, antique map
   illustration" (sepia). Colour does not matter (everything becomes greyscale).
5. **Failing styles**: "woodcut / linocut" gives solid black silhouettes whatever else the prompt
   says (inverting them does not help). "Gilded manuscript" gets no gold, "colored pencil"
   barely any pencil: SDXL Turbo falls back to a default look (the same clip-art fir) when a
   style word is weak.
6. **"antique"/"old map" pulls in parchment backgrounds and fake captions.** Harmless (the
   background removal drops them); keep "plain white background" in the prompt anyway.
7. **The model draws ground anyway** (tufts, rocks, a shadow ellipse) about half the time.
   `sprites.cut` trims it: below the crown the width narrows to the trunk, and the first row
   that widens again past 2.2x the trunk is where the ground starts.
8. Images with background trees or a second object are rejected ("extra objects"), not repaired.
9. **Shape variants** in the subject (`variants` in the family recipe, one per seed in turn) give a
   forest variety without changing the look: "tall narrow spruce", "broad old fir", "young small
   fir", "pine with drooping boughs", "lopsided windswept fir". Without them every tree comes out
   the same fir and a dense forest reads as a repeated arrowhead texture.
10. Ink and sepia converge after greyscale and levels; they are kept as two prompt styles feeding
   one pack, not as two looks.
11. **SDXL Turbo has shapes it will not draw.** A broadleaf tree with a short trunk under a wide
   crown is one: every wording gives long trunks, roots or tree-of-life circles, and "cloud-shaped
   crown" pulls in clouds and mountains behind the tree. "Oak" alone summons the tree-of-life;
   "icon" summons a round badge. Weeping willows come out upright, dunes as desert photos or
   abstract swooshes. Those are FLUX families (`engine`). Bold separate shapes are out of reach
   too: "chunky, bold simple shape" still gives fine engraved firs, so the bold look comes from
   the finishing ring (see Finishing).
12. **Terrain has its own frame and style** (`line`, `LINE_FRAME`): the bare "minimalist black
   line drawing of one single mountain ... sketch" draws clean single mountains, where the
   watercolour wording draws engravings and whole landscapes and a "fantasy cartography" tail
   brings the hatching back. "Steep sides" keeps a range clean; "flat bottom edge" draws base
   lines that stripe it. Hills want "one smooth curved outline like a gentle dome ... nothing on
   top", with houses and roads in the negative.
13. **FLUX.2 takes plain sentences and follows them**: shape, proportions, what to leave out
   ("no roots, no visible branches, no ground"). No negative prompt. Keep place names out of
   the prompt (it would letter them); describe what is seen.
14. **Spell the shape out**, on either engine: short names give curls and swooshes for dunes,
   where "sand dune seen from the side: a smooth crescent-shaped mound" gives dunes. The same
   goes for flat umbrella crowns on savanna trees and a flat walled town's wall as "one flat band
   across the bottom" (`FLAT_ITEMS`).
15. **FLUX draws whatever the style names, on every item.** A style that mentions smoke and lava
   makes every volcano active, the "dormant" ones included; flames or red roofs and domes put
   flames on sites with no fire and red-domed houses behind camps and standing stones; ribbons
   and lanterns turn every holy tree into a shrine tree. Give those items a style that leaves the
   words out (`quiet` volcanoes, `landmark`, `gianttree`, `site2`, where each site names its own
   red part), or say it outright ("only tents, no buildings"). FLUX still adds a small red roof
   here and there.
16. **Stray words get drawn too**: "moon-white" puts a crescent moon on the Soul Tree's trunk,
   "like a sticker" draws a sticker with a white border and a drop shadow (the `bold` wording
   says no border), and "heather" draws plain bushes with no flowers. A plain statue reads as a
   real religious figure, so the landmark statue is a hooded, faceless guardian. Some shrines and
   chapels come with a Christian cross (the user's call, see STATUS.md).
17. **FLUX varies little across seeds** within one variant (the mesas come out nearly alike), so a
   family's variety comes from its variant list.

## Finishing (sprites.py, constants in recipes.py)

- Levels are computed per family and style over all usable cut-outs, so a set stays consistent:
  2nd-98th luminance percentile stretched to 30-255, then a gamma so the average opaque grey is
  `TARGET_MEAN`.
- Size: each sprite gets the family's scale-1 area (`size`, e.g. 185 x 330) at its own
  proportions, so a broad tree comes out shorter rather than wider than the built-in art.
- Edge: the cut-out's semi-transparent edge pixels are tree colour mixed with the background;
  `sprites.cut` takes the background colour (median of the image border) back out, so no light
  halo shows at full size. No ring or erosion is needed for that.
- Outline: `OUTLINE` px solid dark ring around the drawn edge. It is what separates trees at map
  scale: the drawn ink lines are too fine to survive shrinking to 20-30 px. Measured on the densest
  conifer forest (mean grey / share of pixels darker than 50, Wonderdraft's own: 86 / 32%):
  6 px ring 55 / 59% on the inner forest (a dark scale pattern), no ring 95 / 5% (a flat green mass),
  **1 px ring 86 / 27%** (matches). On a jagged conifer even 3 px of ring covers a quarter of the
  sprite.
- Inner fade (`INNER_LIGHTEN`): strokes deeper than `INNER_EDGE` px inside the
  shape fade toward white. It pays for a thick ring: a 4 px ring with a 0.7 fade keeps the
  forest's brightness near the built-ins' while every tree reads as a pale shape with a dark rim,
  where a thick ring alone makes a dark scale pattern and a thin ring an even mat.
- `INK_THIN` (max filter on luminance) makes dark strokes narrower; it barely changes the result
  once the ring is thin, and 3 px and more blobs the lines. Off by default. Negative, it makes
  them bolder (a min filter at full size): -2 with half the inner fade keeps a conifer's branch
  tiers, which the 0.7 fade erases from the densest drawings (mushrooms take -1 for their dots
  and gills).
- Rejected before finishing: proportions outside the family's `aspect`, cut-outs smaller than
  0.8x the delivery height (they would be enlarged), a base (bottom 4%) wider than 55% of the
  crown (ground or bushes left), fill ratio outside 0.3-0.8, anything touching the image edge.
- Rejected after finishing, where a family sets it (`min_texture`, `max_haze`; conifers):
  a flat inside (share of dark stroke pixels inside the shape at a third of the size, the ring
  left out) or a grey haze round the outline (soft-alpha pixels per opaque pixel). Scored by
  `sprites.finish_look`; the build finishes every usable drawing once more for it.
- **Bold trees** (`BOLD_TREE`, the FLUX `bold` style: broadleaves, willows, jungle, swamp
  trees, shrubs) take no inner fade: the drawing's few thick strokes are the texture, as on
  Wonderdraft's own oaks and willows. Fine leaf marks blur into a muddy speckle at map size, and
  a lighter levels target turns the bold strokes grey.
- **Bare crowns and fronds** (dead trees, palms): `ink_alpha` (the paper between branches turns
  transparent), a 1 px ring and no inner fade; the mask and a thick ring fill them into leafy
  blobs and round discs.
- **Clumps** (`shape: clump`: bamboo, swamp trees, the flat 2D settlements) keep every sizeable
  piece, where the one-object check would reject a clump of stalks or a row of houses.
- **Terrain** keeps its ridge lines: the tree finish's inner fade erases them and its ring closes
  the base. Mesas and pillars take `BOLD_TERRAIN` with a 0.3 fade (6 px ring; the light fade
  keeps the rock layers), peaks and fells `BOLD_PEAKS` (the same ring with a 0.35 fade, plus
  `LINE_DARKEN`: greys below `LINE_DARKEN_BELOW`, 215, go down a gamma-3 curve, so a light body
  carries dark ridge lines, like Wonderdraft's jagged peaks), hills `HILL_FINISH`, dunes
  `TERRAIN_FINISH`. `BASE_FADE` fades the bottom and `SKIRT_TRIM` cuts the flanks lower than 20%
  of the peak, so drawn base lines and long low flanks do not line up into stripes across a range. Hills fade their whole lower half:
  Wonderdraft's hills are an upper arc, and a closed base loop shows as a circle in a range.
- **Open drawings need a body.** `fill_under` (hills) makes everything under the top contour
  solid paper; without it about half the hills are hollow. `fill_enclosed` (pillars) turns a
  pixel opaque only with drawing above it, left and right of it, since `fill_under` builds
  straight-sided boxes under pine crowns and faint background peaks. `drop_thin` (14 px; peaks,
  fells, mesas) takes strokes thinner than 28 px off the silhouette: bold base strokes reaching
  out of the body would each get the ring and hang under it like claws, and filling under them
  builds a box-shaped plinth.

## Reviewing

- **`gallery`** (gallery.py): one sheet per family in `~/.local/share/wdmap/assetgen/gallery/`,
  the installed sprites grouped by the variant (or icon item) each was drawn as and numbered
  by file, tinted like Wonderdraft tints them (icons in example colours). The user reviews the
  pack on these ("conifer 15 looks empty"). The variant comes from the prompt saved with the
  raw image, matched to the family's variant list by shared words, so older wordings still
  group right. Takes seconds.
- **On the real map, in Kartofuchs:** import `Main.wonderdraft_map` with the "Fuchsbau" art
  mapping (Map ▸ Import, "Swap the art with"), or run Map ▸ Swap art on a map already open. Each
  built-in family becomes one of our folders, fitted over the art that stood there (its measured
  size, foot and middle) and tinted by the ground; swapping again starts from the original art,
  so re-run it after installing a new round. The mapping covers only Wonderdraft's built-in trees
  and mountains (Kartofuchs' `server/artmap.ts`, `BASE_RULES`); other packs import as they are.
  The measured built-in sizes live in Kartofuchs' data folder (`art-sizes.json`), not in a repo.
- **Size**: the built-in conifers measured on the calibration grid are smaller than our `size`
  (area of 137 x 291 at scale 1 against 185 x 330). Placed at the built-ins' scales, our
  conifers are about 1.4x their linear size; fitted to Dotty's pines they come out
  at 0.7x that scale. Both read well; `size` also sets the delivered resolution.
- **Excluding a drawing**: check an exclusion against `raw/<seed>.png`, never against a position
  on a sheet. An exclusion reshuffles the picks, so to keep a reviewed set, rebuild from exactly
  its seeds (`build --seeds`).

## Families

`recipes.FAMILIES` holds one entry per family; `generate` and `build` take its name, and its
comments say why each setting is what it is. Counts are in the table. Known weak spots: dead
trees are faint at map size, fells are pointier than "rounded", one cactus group sits in flower
pots, the flat 2D camps show domed houses behind the tents, and the monastery icons carry red
flags.

| Family | Engine | Built-in yardstick | Bought pack equivalent | Pack folder |
|---|---|---|---|---|
| conifer | SDXL | `_hd_christmas` | `Dotty_Pines` | `Fuchsbau_Conifers` (round 17, 64) |
| broadleaf | FLUX | `_hd_oak` (fit) | `Dotty_Oaks` | `Fuchsbau_Broadleaves` (bold, 38) |
| willow | FLUX | `_hd_willow` (fit) | `Dotty_Willows` | `Fuchsbau_Willows` (bold, 24) |
| pine (cedar, umbrella pine) | SDXL | `_hd_cedar` (fit) | `Dotty_Pines` | `Fuchsbau_Pines` (32) |
| jungle | FLUX | none | `Dotty_Kapoks` | `Fuchsbau_Jungle` (bold, 29) |
| palm | SDXL | `toon_palm` (fit) | `Dotty_Palms` | `Fuchsbau_Palms` (24) |
| bamboo | SDXL | none | Nibroc's `Bamboo Trees` | `Fuchsbau_Bamboo` (37) |
| deadtree | SDXL | none | (not in Main; vs `Dotty_Dead_Trees`) | `Fuchsbau_Dead_Trees` (16) |
| savanna (acacia, baobab) | SDXL | none | (vs `Dotty_Acacias`, `Dotty_Baobabs`) | `Fuchsbau_Savanna` (48) |
| desert (cacti) | SDXL | none | (vs `Dotty_Cactuses`) | `Fuchsbau_Cactuses` (47) |
| fungal (giant mushrooms) | SDXL | none | (vs `Dotty_Mushrooms`) | `Fuchsbau_Mushrooms` (40) |
| swamp (cypress, mangrove, moss) | FLUX | none | (vs `Dotty_Willows`) | `Fuchsbau_Swamp_Trees` (24) |
| shrubs (bush, shrub, scrub) | FLUX | none | (vs `Dotty_Oaks`) | `Fuchsbau_Shrubs` (24) |
| fruit_trees (apple, cherry, orange, pear, olive, plum; recolourable) | FLUX | none | none | `Fuchsbau_Fruit_Trees` (26) |
| shrine_trees (ribbons, lanterns, shrine roofs) | FLUX | none | none | `Fuchsbau_Shrine_Trees` (30) |
| giant_trees (pines, firs, cedars, oaks, pale trees) | FLUX | none | none | `Fuchsbau_Giant_Trees` (24) |
| named_trees (the Soul Tree) | FLUX | none | none | `Fuchsbau_Named_Trees` (4) |
| peaks | SDXL | `playful_jagged_peaks` (fit, width) | Moulk `mountains sample 1` | `Fuchsbau_Peaks` (round 9, 30) |
| fells (rounded mountains) | SDXL | `playful_rounded_mountains` | Moulk `high hills 2` | `Fuchsbau_Fells` (round 4, 18) |
| hills | SDXL | `playful_hiils` | Moulk `medium hills 1` | `Fuchsbau_Hills` (round 6, 25) |
| dunes | FLUX | `sand_dunes_small` | `Dotty_Dunes` | `Fuchsbau_Dunes` (24) |
| mesas (mesa, butte, arch, spires) | FLUX | none | (vs `Dotty_Mesas`) | `Fuchsbau_Mesas` (24) |
| pillars (karst, Tang-style) | FLUX | Tang Dynasty `mountains` (area) | `Dotty_Pillar_Mts_Big` | `Fuchsbau_Pillars` (32) |
| volcanoes (recolourable) | FLUX | none | (vs `Dotty_Volcanoes`) | `Fuchsbau_Volcanoes` (35) |
| holy_mountains (recolourable) | FLUX | none | none | `Fuchsbau_Holy_Mountains` (25) |
| settlements (18 kinds) | FLUX | none | (vs BSG icons) | `Fuchsbau_2.5D_Settlements` (33) |
| god_cities (13) | FLUX | none | (vs BSG icons) | `Fuchsbau_2.5D_God_Cities` (26) |
| settlements_2d (18 kinds, flat) | FLUX | none | (vs BSG icons) | `Fuchsbau_2D_Settlements` (36) |
| landmarks (8 kinds) | FLUX | none | (vs `Dotty_Mixed_Structures`) | `Fuchsbau_2.5D_Landmarks` (16) |
| special_sites (flat, two per site) | FLUX | none | none | `Fuchsbau_2D_Special_Sites` (30) |

- **Built-in yardstick "fit"** (`place: fit`): each symbol covers the measured drawn size of
  the built-in texture that stood there (area for trees, width for mountains, which are built
  side by side), so a family's delivered `size` only sets its resolution and hand-placed size.
  Mountains are delivered at 3x the built-ins' size (131 x 92 for jagged peaks) to stay sharp
  at `Main`'s scales. Conifers keep the built-in's scale as is.
- **SDXL or FLUX**: SDXL Turbo (5 s per image) where its drawings work; FLUX.2 (about 4 min
  per image) where the shape matters and SDXL ignores it. `generate --engine` overrides. Each
  family also has the other engine's prompt, so switching needs no new wording.
- **Icons** (`shape: icon`, `draw: custom_colors`): recolourable Wonderdraft art. Each pixel is
  drawn as R x colour 1 + G x colour 2 + B x colour 3 with colours picked per symbol. Ours: **R
  ink lines, G walls and body, B roofs, flags and domes**, each channel keeping the drawing's
  shading (`sprites.finish_cc`: dark pixels become ink, saturated ones accents, the rest body;
  a 3 px ink ring). BSG's icons, which `Main` uses, put lines in R and the body in G and leave B
  empty, so the same three colours work for both. The icon prompt asks for flat red roofs on
  cream walls so the sorting is easy. Families with `items` build named icons (`village_1`,
  `village_2`, ...): up to `per_item` usable drawings of each.
- **Accent or body** is decided by saturation (`CC_ACCENT_SAT`, 0.28). FLUX paints snow pale blue,
  so the holy mountains sort at 0.14 to give the snow colour 3; plums and olives come out dark, so
  their fruit goes with the lines. Icon folders take one `.wonderdraft_symbols` entry per symbol,
  which the installer writes (`custom_colors`, radius 3/8 of the shorter side, Wonderdraft's own
  measure).
- **Icon file names are a contract**: Kartofuchs places settlement icons by role, guessed from
  the names in `Fuchsbau_2.5D_Settlements` (`Fuchsbau_2D_Settlements` uses the same): `capital_*`, `castle_*`, `fortress_*` =
  capital; `city_*`, `walled_city_*` = city; `town_*`, `walled_town_*` = town; `village_*`,
  `hamlet_*` = village. Folders with "god" in the name are skipped, so the god-cities stay
  one-offs. Keep the `{item}_{n}` names and these item words. Top-down houses for its town
  maps would be picked up as `house_*` or `building_*` in a folder with "town" or "city" in its
  name.
- **God-city icons** use only what a traveller sees (docs/god-city-seeds.md, chronicler tier):
  Valreka's city on a whale, Frae City's chained rock over a lake, Haizava's sails and vanes,
  Lurrath's stone ring, Ljosarn's beacon, and so on. The names stay out of the prompt, so FLUX
  writes no text.

**Runbook for new families** (round 1 each; check the build sheet and the gallery, then the
pack on Main in Kartofuchs):

```
# SDXL (plain LAN server, ~5 s per image; 60 seeds x 2 styles = 10 min per family)
for f in peaks fells hills dunes willow pine palm bamboo deadtree savanna desert fungal; do
    assetgen.sh generate $f --seeds 1-60 && assetgen.sh build $f --round 1 --keep 40 \
        && assetgen.sh gallery $f
done
# FLUX (server with npc_art's flags, ~4 min per image)
assetgen.sh generate broadleaf --seeds 1-40      # ~2.5 h
assetgen.sh generate jungle --seeds 1-25
assetgen.sh generate settlements --seeds 1-54    # seeds cycle through the 18 kinds: 3 each
assetgen.sh generate god_cities --seeds 1-52     # 4 drawings per city
```

Seeds cycle through a family's variants (or items) as seed % count, so a range that is a
multiple of the count gives each the same number of drawings. If an SDXL family comes out
wrong on the gallery, `generate --engine flux` on new seeds uses its FLUX wording.

## Built-in art in Main

By use (13,128 symbols):

Sizes measured on the calibration grid (Kartofuchs' `art-sizes.json`; area-equivalent at scale 1, drawn
foot, sprite centre relative to the click point), e.g. oak 353 x 301, foot 24, centre -130,
height/width 0.74-1.12; hazel 214 x 233, foot 26, centre -90, 0.83-1.71.

| Uses | Built-in family | | Uses | Built-in family |
|---:|---|---|---:|---|
| 4893 | trees/_hd_christmas (conifer) | | 279 | mountains/playful_hiils |
| 1518 | trees/_hd_oak | | 250 | trees/_hd_pine |
| 1082 | mountains/playful_jagged_peaks | | 215 | packs/Tang Dynasty/mountains/hills |
| 945 | trees/_hd_hazel | | 171 | packs/Arabia/mountains/sand_dunes_small |
| 653 | trees/inked_pine | | 141 | packs/Tang Dynasty/mountains/mountains |
| 648 | trees/_hd_cedar | | 99 | mountains/penciled_mountains_small |
| 515 | trees/_hd_willow | | 96 | trees/_hd_larix |
| 375 | trees/hatch_pine | | 92 | mountains/inked_mountains_large |
| 360 | mountains/penned_hills | | 50 | mountains/penciled_mountains_large |
| 356 | trees/leafy_tree | | 45 | mountains/penned_mountains_large |
| 298 | mountains/playful_rounded_mountains | | 23 | trees/toon_palm |
|  |  | | 24 | sand dunes large + penned mountains small |

A new family needs a `FAMILIES` entry: its SDXL and FLUX wording with shape variants and its
scale-1 size and anchor; where Wonderdraft has built-ins for it, add them to the Fuchsbau
mapping in Kartofuchs (`BASE_RULES` in server/artmap.ts). The pack can hold more variants than Wonderdraft's built-ins (it has 9
conifers; we install 64).
