# assetgen: the Tyrnarra art pack for Wonderdraft

Generates our own symbol art (trees first, then mountains) in a Tyrnarra style, with many
variants per family. Since the 2026-09-26 pack swap `Main` uses bought pack art (Dotty, Moulk)
instead of Wonderdraft's built-ins; our pack is to replace that in turn. The art is made in
Wonderdraft's own pack format, so it works in Wonderdraft today and in any later tool that
reads Wonderdraft packs (Kartofuchs reads them from the same asset folder).

```
assetgen.sh generate conifer --seeds 1-40         # tower ComfyUI -> ~/.local/share/wdmap/assetgen/conifer/<style>/raw/
assetgen.sh build conifer --seeds 101-200 --round 7 --keep 40   # cut, check, finish, install into the Tyrnarra pack
assetgen.sh test conifer --round 7 --offline      # drawn here in seconds: Main's art vs round 6 vs round 7
assetgen.sh test conifer --round 7                # the same from a real Wonderdraft export (hands off ~3 min)
assetgen.sh builtin-refs                          # once: the built-ins as local reference sprites (lineups)
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
  colour 2 (trunk), blue = colour 3, dark = lines. `draw_mode: custom_colors`.
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
  once the ring is thin, and 3 px and more blobs the lines. Off by default.
- Rejected before finishing: proportions outside the family's `aspect`, cut-outs smaller than
  0.8x the delivery height (they would be enlarged), a base (bottom 4%) wider than 55% of the
  crown (ground or bushes left), fill ratio outside 0.3-0.8, anything touching the image edge.

## Testing (wdtest.py, render.py)

- **The yardstick is Wonderdraft's own art**, as in every round since the first. A family with
  a built-in counterpart (recipe `builtin`, e.g. `_hd_christmas`) is placed exactly where and as
  big as that art stood in `Main` before the pack swap: position, scale and mirroring from the
  pre-swap copy of `Main`, the recipe's size and anchor. It is compared with the Base export made
  before the swap (`assetgen-test/Assetgen PreSwap Base.webp`, kept for this).
- **Main now** is shown beside it: the recipe's `replaces` is the folder `Main` uses today
  (`Dotty_Pines` for conifers), and its column is an export of the Base as it is now
  (`Main - Base.webp` when newer than the map, else `Assetgen Reference.webp`, an export of a
  copy redone whenever the Base changes; an `.md5` beside it tells). A family without a built-in
  counterpart is fitted to that art instead: each sprite covers the drawn area of the one it
  replaces and stands on the same foot (`packswap.fit`), as a later swap into `Main` would do.
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
- Applied to `Main` itself the same day (`packswap --apply`); `Main` has no built-in art since.
  `measure-builtins` now takes the built-ins from the copy made before
  (`Main (before pack swap 2026-09-26).wonderdraft_map`); `packswap` without `--apply` has
  nothing left to test in the Base and says so.

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
- **FLUX on the tower** (2026-09-27): a graph with 4 FLUX images wedged the server even with
  the flags: the 17 GB text encoder stayed in VRAM while the 19.6 GB unet loaded, RAM went to
  swap, no step ever sampled (diagnosed by the tower's Claude session). Rules since: one FLUX
  image per graph (`FLUX_BATCH` 1), never SDXL and FLUX in one server session (restart between
  engines), and the client retries through the minutes the server stops answering while FLUX
  loads (`comfy.run`/`wait`).

## Families

`recipes.FAMILIES` holds one entry per family; `generate`, `build` and `test` take its name.
Written 2026-09-27; only the conifers are generated and installed so far.

| Family | Engine | Built-in yardstick | Replaces in Main | Pack folder |
|---|---|---|---|---|
| conifer | SDXL | `_hd_christmas` | `Dotty_Pines` | `Tyrnarra_Conifers` (round 11, 64) |
| broadleaf | FLUX | `_hd_oak` (fit) | `Dotty_Oaks` | `Tyrnarra_Broadleaves` |
| willow | SDXL | `_hd_willow` (fit) | `Dotty_Willows` | `Tyrnarra_Willows` |
| pine (cedar, umbrella pine) | SDXL | `_hd_cedar` (fit) | `Dotty_Pines` | `Tyrnarra_Pines` |
| jungle | FLUX | none | `Dotty_Kapoks` | `Tyrnarra_Jungle` |
| palm | SDXL | `toon_palm` (fit) | `Dotty_Palms` | `Tyrnarra_Palms` |
| bamboo | SDXL | none | Nibroc's `Bamboo Trees` | `Tyrnarra_Bamboo` |
| deadtree | SDXL | none | (not in Main; vs `Dotty_Dead_Trees`) | `Tyrnarra_Dead_Trees` |
| savanna (acacia, baobab) | SDXL | none | (vs `Dotty_Acacias`, `Dotty_Baobabs`) | `Tyrnarra_Savanna` |
| desert (cacti) | SDXL | none | (vs `Dotty_Cactuses`) | `Tyrnarra_Cactuses` |
| fungal (giant mushrooms) | SDXL | none | (vs `Dotty_Mushrooms`) | `Tyrnarra_Mushrooms` |
| peaks | SDXL | `playful_jagged_peaks` (fit, width) | Moulk `mountains sample 1` | `Tyrnarra_Peaks` |
| fells (rounded mountains) | SDXL | `playful_rounded_mountains` | Moulk `high hills 2` | `Tyrnarra_Fells` |
| hills | SDXL | `playful_hiils` | Moulk `medium hills 1` | `Tyrnarra_Hills` |
| dunes | SDXL | `sand_dunes_small` | `Dotty_Dunes` | `Tyrnarra_Dunes` |
| settlements (18 kinds) | FLUX | none | (vs BSG icons) | `Tyrnarra_Settlements` |
| god_cities (13) | FLUX | none | (vs BSG icons) | `Tyrnarra_God_Cities` |

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
  the names in `Tyrnarra_Settlements` (2026-09-27): `capital_*`, `castle_*`, `fortress_*` =
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

Main's tree art now sits in Dotty folders, each standing in for several built-in families:
`Dotty_Pines` (conifers, in progress), `Dotty_Oaks` (built-in oak 1518 + hazel 945 + leafy
tree 356 = 2819 uses), `Dotty_Willows` (515), `Dotty_Palms` (23). The next family is the
broadleaf one that replaces `Dotty_Oaks`. Sizes measured on the calibration grid
(builtin-sizes.json, area-equivalent at scale 1, drawn foot, sprite centre relative to the
click point): oak 353 x 301, foot 24, centre -130, height/width 0.74-1.12; hazel 214 x 233,
foot 26, centre -90, 0.83-1.71. The pre-swap copy of `Main` still tells which Dotty oak was
an oak and which a hazel (same positions), so a test could give each its own variants.

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
