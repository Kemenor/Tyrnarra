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
  `birefnet.safetensors` (BiRefNet Swin-L, MIT) for the built-in RemoveBackground node. Also on
  the tower: Juggernaut XL, NoobAI XL, IP-Adapter for SDXL, FLUX.2 dev (GGUF Q4, ~2 min/image).
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
- `INK_THIN` (max filter on luminance) makes dark strokes narrower; it barely changes the result
  once the ring is thin, and 3 px and more blobs the lines. Off by default.
- Rejected before finishing: proportions outside the family's `aspect`, cut-outs smaller than
  0.8x the delivery height (they would be enlarged), a base (bottom 4%) wider than 55% of the
  crown (ground or bushes left), fill ratio outside 0.3-0.8, anything touching the image edge.

## Testing (wdtest.py, render.py)

- **What a family replaces**: the recipe's `replaces` is the art folder in `Main` today, e.g.
  `Dotty_Pines` for conifers (it stands in for all six built-in conifer families since the
  swap). The test map is the Base view with every symbol of that folder swapped for our pack,
  each new sprite scaled to cover the drawn area of the art it replaces and standing on the
  same foot (`packswap.fit`). The future swap of our pack into `Main` works the same way.
- **The comparison export** is the Base as it is now: `Main - Base.webp` when it is newer than
  the map, otherwise `assetgen-test/Assetgen Reference.webp`, an export of a copy that is redone
  when the Base changes (`.md5` beside it). The built-in art before the swap is kept as
  `Assetgen PreSwap Base.webp`.
- **`--offline`** draws the patches here (`render.py`) in a few seconds, without Wonderdraft:
  the Empty export (Base terrain, no symbols or labels) as ground, symbols y-sorted, straight-
  alpha mipmaps like Godot's, greyscale art multiplied by the ground. Wonderdraft draws the soft
  edges of shrunk sprites darker than plain alpha blending; an empirical fit (`EDGE_COVER`,
  alpha squared on the colour) brings the densest patches within a few points of the real
  exports: Dotty pines 87/35% real vs 89/30% here (mean grey / share darker than 50), round-6
  conifers 86/27% vs 86/29%, Dotty oaks 73/36% vs 68/41%. Single trees match to the pixel.
  Without the fit the dense numbers were far off (round 6: 96/7%). The real export has the last word.
- `--offline` also writes `lineup.jpg`: every set's sprites side by side at full size and at
  map size (40 px), tinted grass-green. The quickest way to compare art styles.
- **Size**: the built-in conifers measured on the calibration grid are smaller than our
  `size` (area of 137 x 291 at scale 1 against 185 x 330). So the fitted test draws our trees
  at about 0.7x the scale rounds 5-6 used (median), the same area as the built-ins had.
  `size` still sets the delivered resolution and the hand-placed size in Wonderdraft.

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

## Families still to do

Main's tree art now sits in Dotty folders, each standing in for several built-in families:
`Dotty_Pines` (conifers, in progress), `Dotty_Oaks` (built-in oak 1518 + hazel 945 + leafy
tree 356 = 2819 uses), `Dotty_Willows` (515), `Dotty_Palms` (23). The next family is the
broadleaf one that replaces `Dotty_Oaks`. Sizes measured on the calibration grid
(builtin-sizes.json, area-equivalent at scale 1, drawn foot, sprite centre relative to the
click point): oak 353 x 301, foot 24, centre -130, height/width 0.74-1.12; hazel 214 x 233,
foot 26, centre -90, 0.83-1.71. The pre-swap copy of `Main` still tells which Dotty oak was
an oak and which a hazel (same positions), so a test could give each its own variants.

Built-in art in `Main` before the swap, by use (13,128 symbols):

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

A new family needs a `FAMILIES` entry: its subject prompt with shape variants, the folder of
`Main` it replaces, and its scale-1 size and anchor from builtin-sizes.json as above. The pack
can hold more variants than Wonderdraft's built-ins (it has 9 conifers; we install 40).
