# assetgen: the Tyrnarra art pack for Wonderdraft

Generates our own symbol art (trees first, then mountains) in a Tyrnarra style, with many
variants per family, to replace Wonderdraft's built-in art in `Main` (which the EULA keeps out of
any tool of our own) and the bought packs that stood in for it. `Main` uses the built-ins
again since 2026-09-27 (see "Swapping"), so every comparison draws against Wonderdraft's own
art. The art is made in Wonderdraft's own pack format, so it works in Wonderdraft today and in
any later tool that reads Wonderdraft packs (Kartofuchs reads them from the same asset folder).

```
assetgen.sh generate conifer --seeds 1-40         # tower ComfyUI -> ~/.local/share/wdmap/assetgen/conifer/<style>/raw/
assetgen.sh build conifer --seeds 101-200 --round 7 --keep 40   # cut, check, finish, install into the Tyrnarra pack
assetgen.sh test conifer --round 7 --offline      # drawn here in seconds: Main's art vs round 6 vs round 7
assetgen.sh test conifer --round 7                # the same from a real Wonderdraft export (hands off ~3 min)
assetgen.sh builtin-refs                          # once: the built-ins as local reference sprites (lineups)
assetgen.sh fullswap                              # the whole pack in a copy of the Base, exported, vs the built-ins
assetgen.sh gallery [peaks settlements ...]       # review sheets of the installed pack, by variant, numbered
```

All prompt styles in `recipes.STYLES` feed **one pack folder per family**: once greyscaled and
levelled they look alike on the map, and mixing them adds variety. `--style ink` limits
`generate` or `build` to some of them. `build` writes into `~/.local/share/wdmap/assetgen/<family>/`:
`sheet.jpg` (the installed sprites tinted grass-green), `chosen.txt` (which style and seed became
which file) and `rejects.txt` (why each other image was dropped); every raw image has a `.txt`
with its exact prompt and settings. `test` writes `compare-*.jpg` there too. With `--round N`
all of that goes to `<family>/round-N/` instead, `build` keeps a copy of the round's sprites
there (`round-N/sprites/`, so later rounds can be compared with it), and `test` names its
export `Assetgen <Family> rN.webp`.

The installed pack: `~/.local/share/Wonderdraft/assets/Tyrnarra/sprites/<kind>/<Folder>/`.
Test maps and their exports: `~/.local/share/wdmap/assetgen-test/` (outside Proton Drive on
purpose: 100 MB maps and 120 MB PNGs should not sync).

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
- **The tower's server has two modes** (since 2026-09-27; the tower's own Claude session
  restarts it on request, naming the mode): **sdxl** (`--cache-none --reserve-vram 2.0`, VAE on
  the GPU, ~5 s per SDXL image) and **flux** (the same plus `--cpu-vae`, ~2 min per FLUX image;
  the flags are npc_art's, tools/imageGen/npc_art.py `ensure_server` explains each). Switch modes
  between an SDXL phase and a FLUX phase: never mix the two engines in one server session, and
  never send FLUX to an sdxl-mode server (the GPU VAE fault can crash it). The plain server
  without these flags ran one FLUX image and then wedged in a load `/interrupt` cannot stop.
  FLUX graphs here skip BiRefNet: the drawings come on clean white, cut locally
  (`sprites.flood_mask`).
- `assetgen.sh` builds its own gitignored `.venv` (numpy, scipy, pillow) on first run.
- `test` needs Wonderdraft installed as for `wd-regions --export`, and closed (`test --offline` does not).

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
  "Missing custom assets" dialog. `wdmap` adds used packs on every save since 2026-09-26.
- Texture paths have no extension: `user://assets/Tyrnarra/sprites/trees/Tyrnarra_Conifers/conifer_01`.
- **Size**: a symbol is drawn at sprite size x its `scale`. To replace a built-in family 1:1 the
  sprite must be as big as the built-in art at scale 1. The calibration grid measures it
  (`measure-builtins` -> builtin-sizes.json): the nine built-in `tree_xmas` are 86-206 x
  197-426 px at scale 1, area-equivalent 137 x 291, centred about 70 px above the click point,
  radius 51. (An earlier estimate from isolated trees in an export, 180-210 x 300-415, caught only
  the big ones.) In `Main` conifers are used at scale 0.1-0.6, so they end up 30-250 px tall.

## Prompting (SDXL Turbo, DreamShaper XL)

What worked and what did not, in the order we found it (2026-09-26):

1. **One subject per image, portrait 832x1216.** Each tree comes out ~1000 px tall, crisp when
   shrunk to 350. Sheets of many icons ("set of ... icons, sprite sheet") give 15-30 trees per
   image but each only 150-300 px: blurry at full size. Rows of 3-4 trees always get a ground
   line joining them and often touch; negatives do not stop it at CFG 2.
2. **Ask for the map-reading shape, not realism**: "chunky", "full rounded silhouette",
   "stylized", "thick dark outline", "bold shape readable at small size". Plain "conifer icons"
   gave thin spiky firs that turn into noise at 20-30 px.
3. **Ask for a light fill**: "light foliage with dark ink strokes". Wonderdraft's tint needs a
   light body; dark-filled art makes black blobs in forests and grey trees in snow.
4. **Style words** that held: "black ink outlines with soft watercolor wash shading, hand-drawn
   fantasy cartography" (ink); "sepia brown ink linework with light wash shading, antique map
   illustration" (sepia). Colour does not matter (everything becomes greyscale).
5. **Failed styles**: "woodcut / linocut" gives solid black silhouettes whatever else the prompt
   says (inverting them does not help). "Gilded manuscript" got no gold, "colored pencil"
   barely any pencil; 4 of 8 styles collapsed into the same clip-art fir. SDXL Turbo falls back
   to a default look when a style word is weak.
6. **"antique"/"old map" pulls in parchment backgrounds and fake captions.** Harmless now (the
   background removal drops them); keep "plain white background" in the prompt anyway.
7. **The model draws ground anyway** (tufts, rocks, a shadow ellipse) about half the time.
   `sprites.cut` trims it: below the crown the width narrows to the trunk, and the first row
   that widens again past 2.2x the trunk is where the ground starts.
8. Images with background trees or a second object are rejected ("extra objects"), not repaired.
9. **Shape variants** in the subject (`variants` in the family recipe, one per seed in turn) give a
   forest variety without changing the look: "tall narrow spruce", "broad old fir", "young small
   fir", "pine with drooping boughs", "lopsided windswept fir". Without them every tree came out
   the same fir and a dense forest read as a repeated arrowhead texture.
10. Ink and sepia converge after greyscale and levels; they are kept as two prompt styles feeding
   one pack, not as two looks.
11. **SDXL Turbo has shapes it will not draw.** A broadleaf tree with a short trunk under a wide
   crown was one: every wording gave long trunks, roots or tree-of-life circles (Results log,
   broadleaf trials). "Oak" alone summons the tree-of-life; "icon" summons a round badge.
12. **FLUX.2 takes plain sentences and follows them**: shape, proportions, what to leave out
   ("no roots, no visible branches, no ground"). No negative prompt. Keep place names out of
   the prompt (it would letter them); describe what is seen.

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
  **1 px ring 86 / 27%** (matches). On a jagged conifer even 3 px of ring covered a quarter of the
  sprite. `test` prints these two numbers for every run.
- Inner fade (`INNER_LIGHTEN`, since round 8): strokes deeper than `INNER_EDGE` px inside the
  shape fade toward white. It pays for a thick ring: a 4 px ring with a 0.7 fade keeps the
  forest's brightness near the built-ins' while every tree reads as a pale shape with a dark rim,
  where a thick ring alone made the dark scale pattern of round 4 and a thin ring an even mat.
- `INK_THIN` (max filter on luminance) makes dark strokes narrower; it barely changes the result
  once the ring is thin, and 3 px and more blobs the lines. Off by default. Negative, it makes
  them bolder (a min filter at full size): -2 with half the inner fade keeps a conifer's branch
  tiers, which the 0.7 fade had erased from the densest drawings (tree review, conifer round 13).
- Rejected before finishing: proportions outside the family's `aspect`, cut-outs smaller than
  0.8x the delivery height (they would be enlarged), a base (bottom 4%) wider than 55% of the
  crown (ground or bushes left), fill ratio outside 0.3-0.8, anything touching the image edge.
- Rejected after finishing, where a family sets it (`min_texture`, `max_haze`; conifers):
  a flat inside (share of dark stroke pixels inside the shape at a third of the size, the ring
  left out) or a grey haze round the outline (soft-alpha pixels per opaque pixel). Scored by
  `sprites.finish_look`; the build finishes every usable drawing once more for it.

## Testing (wdtest.py, render.py)

- **`gallery`** (gallery.py): one sheet per family in `~/.local/share/wdmap/assetgen/gallery/`,
  the installed sprites grouped by the variant (or icon item) each was drawn as and numbered
  by file, tinted like Wonderdraft tints them (icons in example colours). The user reviews the
  pack on these ("conifer 15 looks empty"). The variant comes from the prompt saved with the
  raw image, matched to the family's variant list by shared words, so older wordings still
  group right. Takes seconds.

- **The yardstick is Wonderdraft's own art**, as in every round since the first. A family with
  a built-in counterpart (recipe `builtin`, e.g. `_hd_christmas`) takes over those symbols in a
  copy of the Base view: same position, scale and mirroring, sized by the recipe (`place:
  scale`, the conifers) or to the measured art of the built-in texture that stood there (`place:
  fit`). Its first column is the Base's own export (`Main - Base.webp` when newer than the map,
  else `Assetgen Reference.webp`, an export of a copy redone whenever the Base changes; an `.md5`
  beside it tells).
- **The bought pack** is the second column where a family has one (recipe `replaces`, e.g.
  `Dotty_Pines`): the Base export from the days `Main` used the packs
  (`assetgen-test/Assetgen PostSwap Base.webp`). A family without a built-in counterpart takes
  over the bought art `Main` has for it (Dotty's kapoks, Nibroc's bamboo), fitted to it: each
  sprite covers the drawn area of the one it replaces and stands on the same foot
  (`packswap.fit`).
- **`fullswap`**: the whole pack in a copy of the Base (every built-in family by `BUILTIN_TO`
  in fullswap.py, the bought jungle and bamboo, every city cluster by the icon rules), exported
  and compared with the Base region by region (`~/.local/share/wdmap/assetgen/fullswap/`).
  It waits 30 s for the load (the user timed it under 30 s); the runs that once looked like slow
  loads were a locked screen (see the export notes in `tools/wonderdraft/README.md`).
- **`builtin-refs`** (two exports, once): every built-in texture `Main` used, placed on an empty
  copy of the Base, exported drawn white and drawn black; per pixel alpha = 1 - black / terrain
  and grey = (white - (1 - alpha) terrain) / alpha give each built-in as a clean greyscale sprite
  in `~/.local/share/wdmap/assetgen/builtins/` (local only, like the pack art: Wonderdraft's art
  never goes into the repo). They fill the "Wonderdraft built-ins" row of `lineup.jpg`.
- **`--offline`** draws our columns here (`render.py`) in a few seconds, without Wonderdraft,
  beside the real exports of the built-ins and of `Main` now: the Empty export (Base terrain, no
  symbols or labels) as ground, symbols y-sorted, straight-alpha mipmaps like Godot's, greyscale
  art multiplied by the ground. Wonderdraft draws the soft edges of shrunk sprites darker than
  plain alpha blending; an empirical fit (`EDGE_COVER` 0.5, `COLOUR_POWER` 2), refitted on four
  real exports, brings the densest patch within a few points (mean grey / share darker than 50,
  real vs here): Dotty pines 87/35% vs 86/35%, round 9 81/39% vs 83/34%, round 11 83/37% vs
  84/34%; thin-ringed round 6 comes out darker here (86/27% vs 82/35%). The first fit (0.7)
  had round 9 at 86/30%. Single trees match to the pixel. The real export has the last word.
- `--offline` also writes `lineup.jpg`: the built-ins, the art `Main` uses now and each round,
  sprite by sprite at full size and at map size (40 px), tinted grass-green.
- **Size**: the built-in conifers measured on the calibration grid are smaller than our `size`
  (area of 137 x 291 at scale 1 against 185 x 330). Placed at the built-ins' scales, as in all
  rounds, our conifers are about 1.4x their linear size; fitted to Dotty's pines they come out
  at 0.7x that scale. Both read well; `size` also sets the delivered resolution.

## Swapping built-in art for installed packs (packswap.py)

Since 2026-09-26 the plan is to use bought packs first (Dotty Advanced + Booster bundles,
Moulk's AI Fantasy Cartography Megapack; installed in the Wonderdraft asset folder, backed up in
Proton Drive, never in this repo) and to generate our own art later.

```
assetgen.sh measure-builtins     # calibration: two exports, sizes -> builtin-sizes.json
assetgen.sh packswap             # Base copy with every rule in pack-swap.json applied, exported, compared
```

- `measure-builtins` puts one copy of each built-in texture used in Main (262) on a grid in an
  otherwise empty copy of the Base terrain, at scale 0.35, untinted, exports it with and without
  the grid and measures each cell's difference: drawn width, height, centre and foot at scale 1.
  Earlier attempts measured isolated symbols in the real map; in a map this dense almost none
  are isolated, and stroke-drawn art falls apart into single strokes as connected blobs.
- `packswap` swaps every symbol whose texture starts with a rule's `from` for a file of the
  rule's `to` folder (picked by a hash of the position), with a scale that makes the new art
  cover the same measured `match` dimension and an offset that puts its drawn foot and centre
  where the old art's were. Radius comes from the folder's `.wonderdraft_symbols`. Custom-colour
  folders (`_Cc`, draw_mode custom_colors) are refused until a rule gives colours.
- Comparisons land in `~/.local/share/wdmap/assetgen/packswap/swap-*.jpg`.
- First run (2026-09-26): all 24 families, 13,128 symbols swapped. Trees, dunes and the overall
  map read like the original; Moulk mountains and hills came out somewhat small and the Tang
  mountains faint, so their rules need a `size` above 1.
- Applied to `Main` itself the same day (`packswap --apply`), and **swapped back on 2026-09-27**
  at the owner's wish, so comparisons draw against Wonderdraft's own art again. The pack-art
  version is kept as `Main (after pack swap 2026-09-26).wonderdraft_map` (its only other
  difference: Moulk's pack in `included_packs`), the copy from before as
  `Main (before pack swap 2026-09-26).wonderdraft_map`; the four views were regenerated and the
  exports from before the swap match them again.

## Results log

- **Round 1-2** (styleboard, 8 styles on sprite sheets): shortlisted ink, woodcut, sepia. On the
  map at 20-30 px all styles looked alike; silhouette and outline matter more than style.
- **Round 3** (chunky prompt, outline, sized to measured 350 px): at the right size the forest
  density matched Wonderdraft's. Woodcut dropped.
- **Wonderdraft test 1** (ink and sepia, 20 variants each, from sheets): works end to end. Forests
  read darker and denser than Wonderdraft's, snow trees grey instead of white, full-size trees
  soft, a light halo inside the outline, stray ground and small side trees on a few.
- **Round 4** (this tool): one tree per portrait image, ground trim, defringe, TARGET_MEAN 190,
  6 px outline, sized to 350 px height. In Wonderdraft: snow trees now white and crisp at full
  size. But about 1.5x too wide (single trees came out broader, and only height was matched),
  and dense forests too dark: every tree's closed thick outline made a dark scale pattern.
- **Round 5**: sized by area (185 x 330 at scale 1, keeping each tree's proportions), 3 px
  outline (covers the cut seam only; the drawn ink line carries the edge), TARGET_MEAN 195,
  six shape variants, ink and sepia pooled, 32 variants installed from 158 usable of 200.
  In Wonderdraft: size right, full-size trees good, forests still too dark (thick drawn lines plus
  a 3 px ring that covered 25% of each sprite).
- **Round 6**: edge colour cleaned instead of eroded, ring down to 1 px (tested 0 and 1): the
  forest matches Wonderdraft's brightness and darkness numbers and reads as separate trees; snow
  trees clean. New subject wording with less ink ("pale foliage drawn with a few confident ink
  lines, lots of white paper showing, minimal shading": ink share 45% -> 33%) for seeds 101-200.
- **Round 7** (2026-09-27; seeds 101-200 with that wording; first test fitted to `Main`'s Dotty
  pines, compared offline): 121 usable of 200 (34 wide base, 45 proportions, mostly broad
  trees just under 1.3), 40 installed. Worked: the raw art is lighter (share darker than 80:
  ink 51% -> 44%, sepia 66% -> 54%), the "drooping boughs" variant adds two umbrella-crowned
  pines for variety, and full-size trees are far crisper than Dotty's (its pine sprites are
  ~180 px tall and blur where `Main` enlarges them up to scale 3.4). Did not change: levels to
  `TARGET_MEAN` even out the lighter drawing, so at map size round 7 looks like round 6
  (densest patch offline: Dotty 89/30%, round 6 89/25%, round 7 87/27%). Open: style. Dotty's
  pines read as separate bold shapes with thick outlines; ours are fine engraved firs that read
  as texture at 20-40 px. "Chunky, bold simple shape" in the prompt does not get SDXL Turbo
  there; a bolder look needs a different prompt or a stronger finishing outline.
  Real export (2026-09-27, placed as the built-ins were, like rounds 1-6): built-ins 86/32%,
  Dotty 87/35%, round 6 86/27%, round 7 84/30%.
- **Rounds 8-10** (finishing only, same 40 cut-outs as round 7, `build --set`): a thicker ring
  plus `INNER_LIGHTEN`, which fades strokes deep inside the shape toward white, so each tree
  reads as a pale shape with a dark rim. Round 8: ring 3 px, fade 0.5. Round 9: ring 4 px, fade
  0.7. Round 10: ring 2 px, fade 0.35. The ring and the fade cancel in brightness (offline all
  86/29-30%) while the forest turns from an even mat into separate trees.
- **Round 9 chosen and installed** (overnight decision, 2026-09-27): real export 81/39%, a
  little darker than the built-ins' 86/32% and read as distinct treetops with dark gaps, like the
  built-ins and Dotty; at full size a bold ink rim with a clean pale inside. Its settings are the
  new defaults in recipes.py (`OUTLINE` 4, `INNER_LIGHTEN` 0.7).
- **Round 11 installed** (overnight decision): round 9's finishing on all 400 conifer images
  (seeds 1-200, both wordings, ink and sepia): 279 usable, **64 installed** for more variety.
  Real export 83/37%, reads like round 9. The installed conifer set since 2026-09-27.
- **Broadleaf prompt trials** (2026-09-27, SDXL Turbo, square canvas): the conifer wording gave
  tall naturalistic watercolour trees with long trunks and visible branching, taller than wide.
  "Cloud-shaped crown" pulled in clouds and mountains behind the tree; "icon" put it in a
  circular badge; "coloring book" and "oak" drew tree-of-life oaks with roots, in circles;
  "storybook cartoon tree" still gave a big trunk and roots. SDXL Turbo will not draw a short
  trunk under a wide crown. **FLUX.2** did exactly as asked on the first image (a clean ink map
  tree, puffy round crown, short trunk, bold outline, pale fill, soft grey wash on one side), so
  broadleaf and jungle are FLUX families (`engine`). But the tower's LAN server wedged on the
  second FLUX job (README: Setup).
- **SDXL families, round 1-2** (2026-09-27 early morning, after the server restart with the
  FLUX flags: ~22 s per image with the VAE on the CPU; quality pass of 6 images each first):
  - pine: 33 of 48 usable, installed; umbrella pines, cedars, windswept pines. Densest built-in
    cedar patch offline 111/18% vs built-ins 113/17%.
  - bamboo: 1 of 48 as a tree (a clump is many stalks: "extra objects", "wide base", low fill);
    as `shape: clump` 44 usable, 40 installed. Reads like Main's bamboo (112/13% vs 112/12%).
  - deadtree: 0 of 48 (roots as wide as the crown, sparse fill); with `base_max` and a lower
    fill 17, but the mask and the 4 px ring filled every crown into a leafy blob. With
    `ink_alpha` (alpha from the ink: the paper between branches turns transparent), a 1 px ring
    and no inner fade: 18 bare trees, installed.
  - palm: 29 usable, but the mask and ring made the fronds round discs; with `ink_alpha` and a
    thin ring 24 palms that read as palms, installed.
  - willow: SDXL drew upright trees for "weeping willow" (1 in 6 wept): moved to FLUX.
  - savanna, desert, fungal: good single subjects in the quality pass (acacias read as ordinary
    trees; cacti and mushrooms clear); their full runs were cut short by the FLUX wedge and rerun.
  - peaks, fells, hills: the watercolour wording drew engravings and whole landscapes; the
    bare "minimalist black line drawing of one single mountain ... sketch" drew clean single
    mountains (the "fantasy cartography" tail brought the hatching back, so terrain has its own
    frame and style). Tree finishing flattened them (the inner fade erased ridge lines, the ring
    closed the base): terrain keeps its inner lines with a 2 px ring. In a dense range the drawn
    base lines and long low flanks lined up into horizontal stripes: `BASE_FADE` fades the
    bottom 15%, `SKIRT_TRIM` cuts the flanks lower than 20% of the peak. Peaks round 3: 28
    installed (offline 103/13% vs built-ins 100/26%, lighter line art); fells 21; hills 14
    (132/9% vs 134/8%). A few faint stripes remain where a drawing's base line sits above the
    fade; dropping "flat bottom edge" from the wording is the next try.
  - dunes: every SDXL wording gave desert photos or abstract swooshes: moved to FLUX.
- **Fine-tuning round** (2026-09-27 midday; SDXL in sdxl mode, then FLUX in flux mode):
  - peaks round 4 (seeds 101-148, "steep sides" instead of "flat bottom edge"): the stripes
    across ranges are gone; 31 installed.
  - hills round 2 ("one smooth curved outline like a gentle dome ... nothing on top", houses and
    roads negative, fill down to 0.04 since Wonderdraft's own hills are little more than an
    arc): 29 clean dome outlines (round 1: 14 mixed); one scribble excluded.
  - cacti round 3 (six shapes, the old near-identical barrel seeds excluded): 47 saguaros,
    prickly pears and groups; one group came out in flower pots.
  - savanna round 3 (flat umbrella crowns spelled out): 48 flat-topped acacias and baobabs.
  - broadleaves and jungle: the maple-leaf and leaf-bush drawings excluded by seed (39, 29).
  - icons (FLUX, "roofs and domes red; no flags or banners"): settlements 33 (all 18 kinds,
    the two monasteries from round 1 with flags since both new ones touched the edge),
    god-cities 26 (two per city). The icon preview fits by area now: wide raised views next to
    BSG's tall fronts.
  - dunes round 3 (the side-view crescent shape spelled out for FLUX): all 24 read as dunes
    with a crest line and a shaded steep face (round 1-2: curls and swooshes).
- **Whole-map test and fixes** (2026-09-27 afternoon, `fullswap`, compared with the built-ins
  after `Main` went back to them):
  - Myrkono's forest came out white: the inked and hatched pines (and toon palms) are
    full-colour built-ins without a ground sample, so our greyscale art in their place was
    never tinted. Swapped symbols without a sample now get the ground colour under them.
  - Peaks were small, busy and light next to Wonderdraft's bold peaks: round 7 (6 px ring,
    inner fade 0.7, sized by area instead of width) reads like the built-ins' bold outlines;
    fells the same. Densest built-in peak patch: 100/26% built-in, 112/16% ours.
  - Hills drew closed base loops that showed as circles in a range: round 4 fades the lower
    half out (Wonderdraft's hills are an upper arc), 4 px ring; 133/8% vs 134/8%.
  - Two black circles stayed in the hills: the exclude list named the wrong seeds, so the empty
    ellipse (134) and the volcano seen from above (122) went in and two good hills stayed out.
    Round 5 (seeds 101-148, exclusions checked against the raw drawings; 113 and 147 also out,
    both standing on a full ellipse): 25 hills, no circles in the offline render of the range.
    Check an exclusion against `raw/<seed>.png`, never against a position on the sheet.
  - Matching the built-ins closely: conifers 86/33% vs 86/32%, oaks 87/20% vs 88/18%, willows,
    dunes. The jungle has no built-in; ours reads much lighter than Dotty's kapoks (91/13% vs
    68/41%).
  - The first automatic export of the test map timed out: Wonderdraft's first load of the new
    pack images outlasts 15 s. With a 120 s load wait it runs through (178 s in all). (Later
    found: the failures were a locked screen swallowing the keystrokes; 30 s is enough.)
- **Tree review** (2026-09-27 evening; the user went through every tree sprite on the gallery
  sheets: `gallery/NN-<family>.jpg`, grouped by the variant each was prompted as):
  - "Wonderdraft has stronger lines in the trees." Its oaks and willows are a flat pale fill
    with a few thick curved brush strokes; ours lost their inner lines to the 0.7 inner fade.
  - Conifers: some looked empty (15, 34, 38, 49; six more like them). The densest drawings lost
    their branch tiers; round 13 (inner fade 0.35, `INK_THIN` -2, same 64 picks) keeps them,
    82/35% offline vs the built-ins' 86/32%. Installed.
  - Broadleaves, willows, jungle "mostly green without texture": no inner fade and bolder
    strokes brought FLUX's small leaf marks back (broadleaf rounds 3-5), but at map size they
    blur into a muddy speckle (72/36% vs 88/18%). The drawings need fewer, bigger strokes:
    a new FLUX style `bold` asks for Wonderdraft's look (thick outline, a few big rounded
    shapes with thick curved strokes where they overlap, flat pale fill). "Like a sticker"
    drew stickers with a white border and a drop shadow, so the wording now says no border.
  - `bold` in full (FLUX, 2026-09-27 18:16-21:37, 94 images at ~140 s): broadleaves 40, willows
    24, jungle 30; dropped by hand broadleaf 37 (a blob with a flat cut-off bottom) and jungle 23
    (a giant leaf bush). Finishing `BOLD_TREE` (no inner fade; the drawing's strokes are the
    texture). Installed: broadleaves round 8 (38), willows round 4 (24), jungle round 4 (29).
    Offline: willows 121/12% (built-ins 129/9%), jungle 74/23% (was 81/16%; Dotty's kapoks
    68/41%), oaks 72/37% like Dotty's oaks (73/36%). A lighter levels target (228, 238) got the
    oaks to round 2's brightness but turned the bold strokes grey, the opposite of the review.
  - The offline renderer draws this oak forest about 10 grey darker than Wonderdraft: round 2
    renders 77/33% here and measured 87/20% in the real export (the forest's other built-in
    trees come out as blurry dark blobs). Compare offline rounds with each other, not with the
    built-ins' export column, and confirm with a real export.
  - Mushrooms "a touch more texture": round 3, inner fade 0.35 and `INK_THIN` -1 (caps' dots and
    gills back), same 40 picks. Installed.
  - Dropped by hand: pine 13 (a watercolour stain came with it), bamboo 16, 19, 46 (forest
    scenes cut into loose stalks; rebuilt from exactly the 37 reviewed seeds, since an exclusion
    reshuffles the picks), dead trees 21 and 41 (hollow stumps drawn in 3D).
  - Liked as they are: pines, palms, savanna, cacti, the rest of the bamboo and dead trees.
  - Real export of the whole pack (`fullswap`, 88 s with a 30 s load wait), vs the built-ins:
    conifers 84/35% (86/32%), oaks 78/31% (88/18%: the bold strokes read darker, by design),
    willows 128/9% (129/9%), hills 134/8% (134/8%, no circles), dunes 148/3% (152/1%), jungle
    77/27% (Dotty's kapoks 68/41%; was 91/13%). The user: "these look by tree already better".
  - The user settled the style: bold lines on a flat pale fill ("this is good and the style we
    want to go for"), but "conifer still has some less textured ones that jump out". Scored all
    279 usable conifers after finishing: the flat ones kept 4-9% dark strokes inside at map
    scale (median 13%), and some sepia ones carried a grey haze round the outline. Round 17
    keeps texture >= 13% and haze < 0.06 (77 pass), 64 installed; offline 81/34% (round 13:
    82/35%). The young compact firs were all among the soft ones, so that variant is gone.
- **Galleries for review** (2026-09-27 night): `assetgen.sh gallery` for every family, the
  mountains and icons reviewed next. Seen while making them: about half the hills are hollow
  (the flood mask leaves an open drawing's inside transparent), the others filled; some peaks
  and fells trail heavy dark base strokes (peaks 02, 14, 27; fells 03, 04, 19, 20).
- **Mountain and icon review** (2026-09-27 night, on the galleries): "fix the hollow and the base".
  - Hollow hills: the mask of an open line drawing sees only the strokes, so about half the
    hills were transparent inside. `fill_under` (hills round 6) makes everything under the top
    contour solid paper: 25 even mounds, 131/10% offline (round 5: 132/10%).
  - Dark base strokes: bold strokes reaching out of a peak's or fell's body each got the 6 px
    ring and hung under it like claws. Filling under them built a box-shaped plinth; `drop_thin`
    (14 px) takes strokes thinner than 28 px off the silhouette and keeps the body as drawn.
    Peaks round 8 (30; seed 144 had too little body left), fells round 3 (18; seeds 4, 6, 29
    were built of those strokes). Real export: peaks 115/14% (built-ins 100/26%), hills 133/8%
    (134/8%), clean ranges. The offline render drew stepped blocks under the filled hills that
    the real export does not show: its soft-alpha handling, not the art.
  - Icons: "they look good, and should probably be under 2.5D": the raised-view folders are
    `Tyrnarra_2.5D_Settlements` and `Tyrnarra_2.5D_God_Cities` now; `settlements_2d`, the
    same kinds as flat straight-on symbols ("just to see"), goes to `Tyrnarra_2D_Settlements`.
    Lograth "might need some work": its aerial lines came out as a tent-like sheet; new wording
    (seeds 203+) spells out the twin seats across one square, the bridging hall of courts and
    thin cables with gondolas.
  - Wonderdraft had rewritten both icon folders' `.wonderdraft_symbols` into one entry per symbol
    with draw mode `normal` (raw red/green/blue instead of the chosen colours): icon folders take
    per-symbol entries, like BSG's. The installer writes them now (`custom_colors`, radius 3/8
    of the shorter side, Wonderdraft's own measure); the installed files were repaired.
  - Lograth round 3 (seeds 203, 216, 229, 242 on the new wording): all four show the throne-hall
    and the scales-temple across one square, joined by colonnades, cables between the towers;
    203 and 229 installed, the other twelve god-cities rebuilt from their installed seeds.
  - `settlements_2d` round 1 (seeds 1-19, one per kind plus a second village): flat skylines
    and fronts, like the symbols on old maps; the walled town and walled city still came out
    raised. A flat village is a row of separate houses, which the one-object check rejected:
    the family keeps every sizeable piece (`shape: clump`). 19 installed in
    `Tyrnarra_2D_Settlements`, "just to see".
  - Paused ~30 min for the user's wake-on-LAN test of the tower; its Claude session now brings
    ComfyUI up after a wake.
- **Night of 2026-09-28** (the user asleep: "do two per kind and flatter walled towns", then "feel
  free to do any yet missing assets during the nights, I think for example volcanic was missing"):
  - `settlements_2d` round 2 (seeds 20-41): a second drawing of every kind. The walled town and
    walled city spelled out as "the wall one flat band across the bottom" (`FLAT_ITEMS`, used by
    the 2D family only, so the item names stay) came out flat; the raised round-1 ones (3, 5) are
    excluded. 35 installed, two per kind but the camp (both new camps ran off the image edge).
  - New families queued on the tower (FLUX, one after another): `volcanoes` (recolourable,
    lava in the accent channel, style `lava`), `swamp` trees, `mesas`, `shrubs`.
  - `volcanoes` round 1 (seeds 1-30, 6 variants): all 30 usable and installed in
    `Tyrnarra_Volcanoes` (custom colours: lines, rock and smoke, lava). Bold outlines, pale rock,
    lava streams and a smoke plume; about Dotty's volcanoes' size. FLUX drew every variant
    active, the "dormant" ones included: a quiet volcano needs its own wording.
  - `swamp` round 1 (seeds 1-30, 5 variants): moss-hung trees, gnarled leaning trunks, mangroves
    on stilt roots and bald cypresses read as a swamp set; the young mangroves (seed % 5 == 4)
    drew big single leaves across the crown, like the maples, and are excluded. 24 installed
    in `Tyrnarra_Swamp_Trees`, about Dotty's willows' size (kept whole: `shape: clump`).
  - `mesas` round 2 (seeds 1-25, 5 variants: mesa, butte, pair of mesas, rock arch, spire
    cluster): clean line drawings, but FLUX drew each variant nearly alike across seeds. The
    peaks' finish (inner fade 0.7) washed out the rock layers; 0.3 keeps them. Seed 21 dropped
    (a notch in its base). 24 installed in `Tyrnarra_Mesas`, about Dotty's mesas' size.
  - `shrubs` round 1 (seeds 1-24, 4 variants): round bushes, low wide shrubs and open twiggy
    scrub, all 24 usable and installed in `Tyrnarra_Shrubs` (about a third of a broadleaf's
    height at scale 1). The "heather" drew plain bushes, no flowers.
  - Quiet volcanoes: "extinct ... no smoke, no fire, no lava" still drew smoke and lava, since the
    family's style names them; a second style `quiet` (rock and outlines only) drew five clean
    extinct cones (seeds 35-59; the same seeds in `lava` are excluded). Volcanoes round 2: 35.
  - Camps: the style's "roofs and domes painted red" put red-domed stone houses behind every
    camp's tents. "Only tents, no buildings" fixed the 2.5D camp (seed 214, tent pavilions around
    a fire; 196 ran off the edge), which replaces the old one; the flat 2D camps kept their domed
    houses (seeds 70, 88 installed as the most compact; 106, 124 no better).
  - `landmarks` round 1 (seeds 1-24, style `icon`): lighthouses, shrines and hilltop beacons came
    out right (6 installed in `Tyrnarra_2.5D_Landmarks`). The style's roofs and domes built red-
    domed houses around the standing stones, the obelisk, the bridge and the arch, and set the
    statue on a whole castle; the statue also looked like a real religious figure. A style
    `landmark` ("a single structure standing alone: no houses, towers, domes or walls around it")
    and a hooded, faceless guardian statue redraw those five (seeds 104-127).
  - Follow-ups queued behind the first night queue: five quiet volcanoes (the last variant
    reworded "extinct ... no smoke, no fire, no lava"), two compact flat camps (`FLAT_ITEMS`),
    and a new `landmarks` family (standing stones, obelisk, lighthouse, shrine, statue, stone
    bridge, beacon, portal arch; 2.5D recolourable icons, three drawings each).
- **FLUX on the tower** (2026-09-27): a graph with 4 FLUX images wedged the server even with
  the flags: the 17 GB text encoder stayed in VRAM while the 19.6 GB unet loaded, RAM went to
  swap, no step ever sampled (diagnosed by the tower's Claude session). Rules since: one FLUX
  image per graph (`FLUX_BATCH` 1), never SDXL and FLUX in one server session (restart between
  engines), and the client retries through the minutes the server stops answering while FLUX
  loads (`comfy.run`/`wait`).

## Families

`recipes.FAMILIES` holds one entry per family; `generate`, `build` and `test` take its name.
All generated and installed on 2026-09-27, then fine-tuned the same day (570 sprites; counts
in the table; details in the Results log). Left for later: dead trees are faint at map size,
fells are pointier than "rounded", one cactus group sits in flower pots, the camp's tents have
red dome tops, and the monastery icons still carry the old red flags.

| Family | Engine | Built-in yardstick | Bought pack equivalent | Pack folder |
|---|---|---|---|---|
| conifer | SDXL | `_hd_christmas` | `Dotty_Pines` | `Tyrnarra_Conifers` (round 17, 64) |
| broadleaf | FLUX | `_hd_oak` (fit) | `Dotty_Oaks` | `Tyrnarra_Broadleaves` (bold, 38) |
| willow | FLUX | `_hd_willow` (fit) | `Dotty_Willows` | `Tyrnarra_Willows` (bold, 24) |
| pine (cedar, umbrella pine) | SDXL | `_hd_cedar` (fit) | `Dotty_Pines` | `Tyrnarra_Pines` (32) |
| jungle | FLUX | none | `Dotty_Kapoks` | `Tyrnarra_Jungle` (bold, 29) |
| palm | SDXL | `toon_palm` (fit) | `Dotty_Palms` | `Tyrnarra_Palms` (24) |
| bamboo | SDXL | none | Nibroc's `Bamboo Trees` | `Tyrnarra_Bamboo` (37) |
| deadtree | SDXL | none | (not in Main; vs `Dotty_Dead_Trees`) | `Tyrnarra_Dead_Trees` (16) |
| savanna (acacia, baobab) | SDXL | none | (vs `Dotty_Acacias`, `Dotty_Baobabs`) | `Tyrnarra_Savanna` (48) |
| desert (cacti) | SDXL | none | (vs `Dotty_Cactuses`) | `Tyrnarra_Cactuses` (47) |
| fungal (giant mushrooms) | SDXL | none | (vs `Dotty_Mushrooms`) | `Tyrnarra_Mushrooms` (40) |
| swamp (cypress, mangrove, moss) | FLUX | none | (vs `Dotty_Willows`) | `Tyrnarra_Swamp_Trees` (24) |
| shrubs (bush, shrub, scrub) | FLUX | none | (vs `Dotty_Oaks`) | `Tyrnarra_Shrubs` (24) |
| peaks | SDXL | `playful_jagged_peaks` (fit, width) | Moulk `mountains sample 1` | `Tyrnarra_Peaks` (round 8, 30) |
| fells (rounded mountains) | SDXL | `playful_rounded_mountains` | Moulk `high hills 2` | `Tyrnarra_Fells` (round 3, 18) |
| hills | SDXL | `playful_hiils` | Moulk `medium hills 1` | `Tyrnarra_Hills` (round 6, 25) |
| dunes | FLUX | `sand_dunes_small` | `Dotty_Dunes` | `Tyrnarra_Dunes` (24) |
| mesas (mesa, butte, arch, spires) | FLUX | none | (vs `Dotty_Mesas`) | `Tyrnarra_Mesas` (24) |
| volcanoes (recolourable) | FLUX | none | (vs `Dotty_Volcanoes`) | `Tyrnarra_Volcanoes` (35) |
| settlements (18 kinds) | FLUX | none | (vs BSG icons) | `Tyrnarra_2.5D_Settlements` (33) |
| god_cities (13) | FLUX | none | (vs BSG icons) | `Tyrnarra_2.5D_God_Cities` (26) |
| settlements_2d (18 kinds, flat) | FLUX | none | (vs BSG icons) | `Tyrnarra_2D_Settlements` (36) |
| landmarks (8 kinds) | FLUX | none | (vs `Dotty_Mixed_Structures`) | `Tyrnarra_2.5D_Landmarks` (6 so far) |

- **Built-in yardstick "fit"** (`place: fit`): each symbol covers the measured drawn size of
  the built-in texture that stood there (area for trees, width for mountains, which are built
  side by side), so a family's delivered `size` only sets its resolution and hand-placed size.
  Mountains are delivered at 3x the built-ins' size (131 x 92 for jagged peaks) to stay sharp
  at `Main`'s scales. Conifers keep the rounds-1-11 placement (the built-in's scale as is).
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
- **Icon file names are a contract**: Kartofuchs places settlement icons by role, guessed from
  the names in `Tyrnarra_2.5D_Settlements` (2026-09-27; `Tyrnarra_2D_Settlements` uses the same): `capital_*`, `castle_*`, `fortress_*` =
  capital; `city_*`, `walled_city_*` = city; `town_*`, `walled_town_*` = town; `village_*`,
  `hamlet_*` = village. Folders with "god" in the name are skipped, so the god-cities stay
  one-offs. Keep the `{item}_{n}` names and these item words. Top-down houses for its town
  maps would be picked up as `house_*` or `building_*` in a folder with "town" or "city" in its
  name.
- **God-city icons** use only what a traveller sees (docs/god-city-seeds.md, chronicler tier):
  Valreka's city on a whale, Frae City's chained rock over a lake, Haizava's sails and vanes,
  Lurrath's stone ring, Ljosarn's beacon, and so on. The names stay out of the prompt, so FLUX
  writes no text.
- A family with nothing in `Main` to swap gets only the lineup from `test --offline`.

**Runbook for the families still to generate** (round 1 each; check the lineup and the
compare sheets, then `test --round 1` for a real export where the family is in `Main`):

```
# SDXL (plain LAN server, ~5 s per image; 60 seeds x 2 styles = 10 min per family)
for f in peaks fells hills dunes willow pine palm bamboo deadtree savanna desert fungal; do
    assetgen.sh generate $f --seeds 1-60 && assetgen.sh build $f --round 1 --keep 40 \
        && assetgen.sh test $f --round 1 --offline
done
# FLUX (server with npc_art's flags, ~4 min per image)
assetgen.sh generate broadleaf --seeds 1-40      # ~2.5 h
assetgen.sh generate jungle --seeds 1-25
assetgen.sh generate settlements --seeds 1-54    # seeds cycle through the 18 kinds: 3 each
assetgen.sh generate god_cities --seeds 1-52     # 4 drawings per city
```

Seeds cycle through a family's variants (or items) as seed % count, so a range that is a
multiple of the count gives each the same number of drawings. If an SDXL family comes out
wrong in the lineup, `generate --engine flux` on new seeds uses its FLUX wording.

## Built-in art in Main before the swap

By use (13,128 symbols):

Sizes measured on the calibration grid (builtin-sizes.json, area-equivalent at scale 1, drawn
foot, sprite centre relative to the click point), e.g. oak 353 x 301, foot 24, centre -130,
height/width 0.74-1.12; hazel 214 x 233, foot 26, centre -90, 0.83-1.71.

| Uses | Built-in family | | Uses | Built-in family |
|---:|---|---|---:|---|
| 4893 | trees/_hd_christmas (conifer, in progress) | | 279 | mountains/playful_hiils |
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

A new family needs a `FAMILIES` entry: its SDXL and FLUX wording with shape variants, the
built-in yardstick and the folder of `Main` it replaces, its scale-1 size and anchor from
builtin-sizes.json. The pack can hold more variants than Wonderdraft's built-ins (it has 9
conifers; we install 64).
