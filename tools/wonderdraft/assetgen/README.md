# assetgen: the Tyrnarra art pack for Wonderdraft

Generates our own symbol art (trees first, then mountains) to replace the Wonderdraft built-in
art in `Main`, which cannot come along to a future editor of our own (the EULA forbids
extracting it). The art is made in Wonderdraft's own pack format, so it works in Wonderdraft
today and in any later tool that reads Wonderdraft packs.

```
assetgen.sh generate conifer --seeds 1-40      # tower ComfyUI -> ~/.local/share/wdmap/assetgen/conifer/<style>/raw/
assetgen.sh build conifer --keep 32            # cut, check, finish, install into the Tyrnarra pack
assetgen.sh test conifer                       # real Wonderdraft export vs the built-in art (hands off ~3 min)
```

All prompt styles in `recipes.STYLES` feed **one pack folder per family**: once greyscaled and
levelled they look alike on the map, and mixing them adds variety. `--style ink` limits
`generate` or `build` to some of them. `build` writes into `~/.local/share/wdmap/assetgen/<family>/`:
`sheet.jpg` (the installed sprites tinted grass-green), `chosen.txt` (which style and seed became
which file) and `rejects.txt` (why each other image was dropped); every raw image has a `.txt`
with its exact prompt and settings. `test` writes `compare-*.jpg` there too.

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
- `test` needs Wonderdraft installed as for `wd-regions --export`, and closed.

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
  sprite must be as big as the built-in art at scale 1. Measure it from an export: find an
  isolated instance at a known scale and measure it (the built-in `tree_xmas` is about
  180-210 x 300-415 px at scale 1, centred 73 px above the click point, radius 51). In `Main`
  conifers are used at scale 0.1-0.6, so they end up 30-250 px tall.

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
- Outline: `OUTLINE` px solid dark ring. The cut-out's soft edge still carries the white
  background; `DEFRINGE` px of it are eaten and covered by the ring, otherwise a light halo
  shows between outline and tree at full size. A thick ring (6 px) on every tree made dense
  forests a dark scale pattern; 3 px only covers the seam and leaves the drawn line to read.
- Rejected before finishing: proportions outside the family's `aspect`, cut-outs smaller than
  0.8x the delivery height (they would be enlarged), a base (bottom 4%) wider than 55% of the
  crown (ground or bushes left), fill ratio outside 0.3-0.8, anything touching the image edge.

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

## Families still to do

Built-in art in `Main` by use (13,128 symbols; the next candidates after conifers):

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

A new family needs a `FAMILIES` entry: its subject prompt, the built-in texture prefix it
replaces, and its scale-1 size and anchor, measured as above. The pack can hold more variants
than Wonderdraft's built-ins (it has 9 conifers; we install 20+).
