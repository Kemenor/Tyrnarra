"""What to generate: art families, styles and the numbers that make them fit Wonderdraft.

A family replaces one art folder of Main (the "replaces" texture prefix: since the 2026-09-26
pack swap a bought pack's folder, which stands where Wonderdraft's built-ins stood). Its size and
anchor at scale 1 are the built-in art's, measured (builtin-sizes.json), so hand-placed symbols
come out as big as Wonderdraft's own; the test fits each swapped symbol to the art it replaces.
The prompt lessons behind these strings are in README.md ("Prompting").
"""

# Shared prompt tail and negative prompt. One subject per image, portrait: see README.
FRAME = ", centered, whole subject in frame, isolated on a plain white background, no ground"
NEGATIVE = ("photo, realistic, 3d render, text, letters, caption, watermark, signature, ground, soil, rocks, grass, "
            "shadow, landscape, scene, forest, several trees, parchment, paper texture, border, frame, cropped, blurry")

# Prompt styles. All of them feed the same pack folder: greyscaled and levelled they look alike
# on the map, and mixing them adds variety to a forest.
STYLES = {
    "ink": "black ink outlines with soft watercolor wash shading, hand-drawn fantasy cartography",
    "sepia": "sepia brown ink linework with light wash shading, antique map illustration",
}

FAMILIES = {
    "conifer": {
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading, short visible trunk"),
        # One per seed, in turn (seed % len): variety inside the family.
        "variants": ["conifer tree, full rounded fir silhouette",
                     "tall narrow spruce tree, slender pointed silhouette",
                     "broad old fir tree, wide layered branches",
                     "young small fir tree, compact cone shape",
                     "pine tree with drooping layered boughs",
                     "lopsided windswept fir tree, slightly irregular silhouette"],
        # Main's conifers since the pack swap (built-in _hd_christmas, inked, hatch, _hd_pine,
        # larix and cedar all became Dotty's pines).
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Pines/",
        "kind": "trees",           # Wonderdraft sprite folder: trees | mountains | symbols
        "size": (185, 330),        # px at Wonderdraft scale 1, matched by area (built-in tree_xmas ~170-210 x 300-415)
        "radius": 51, "offset_y": -73,   # built-in tree_xmas footprint and anchor
        "aspect": (1.3, 2.6),      # height / width a usable cut-out must have
        "pack_folder": "Tyrnarra_Conifers",
        "file": "conifer_{n:02d}",
    },
}

# Sprite finishing (sprites.py). Wonderdraft multiplies greyscale tree art by the ground colour,
# so the grey values decide how much ground shows through: its own conifers are near-white
# fill with black strokes.
TARGET_MEAN = 195     # average grey of the opaque tree pixels after levels (0-255)
INK_THIN = 0          # px narrower per side for dark lines (sprites.thin_ink); 3+ blobs the lines
OUTLINE = 1           # solid ring around the drawn edge, px; it is what separates trees at map scale
OUTLINE_GREY = 28
DEFRINGE = 0          # px eaten from the soft edge under the ring (the cut edge is colour-cleaned already)

# Generation (generate.py): SDXL Turbo on the tower's ComfyUI, ~5 s per image.
CHECKPOINT = "DreamShaperXL_Turbo_v2.1.safetensors"
STEPS, CFG, SAMPLER, SCHEDULER = 7, 2.0, "dpmpp_sde", "karras"
WIDTH, HEIGHT = 832, 1216
BG_MODEL = "birefnet.safetensors"
