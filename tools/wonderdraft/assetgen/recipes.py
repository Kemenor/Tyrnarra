"""What to generate: art families, styles and the numbers that make them fit Wonderdraft.

A family is measured against Wonderdraft's built-in art ("builtin": the texture prefix of its
counterpart in Main before the 2026-09-26 pack swap) and replaces one art folder of Main today
("replaces": the bought pack's folder that took the built-ins' place). Its size and anchor at
scale 1 are the built-in art's, so the test puts it exactly where and as big as the built-ins
stood. A family without a built-in counterpart leaves out "builtin" and is fitted to the art it
replaces. The prompt lessons behind these strings are in README.md ("Prompting").
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
        "builtin": "res://sprites/trees/_hd_christmas/",
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
    "broadleaf": {
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading, short visible trunk"),
        # Oaks and hazels were Main's two big broadleaf families; the rest adds temperate variety.
        "variants": ["oak tree, broad rounded billowing crown",
                     "old oak tree, wide spreading crown, gnarled trunk",
                     "hazel tree, several thin stems, bushy round crown",
                     "beech tree, smooth trunk, dense domed crown",
                     "linden tree, tall rounded crown",
                     "young deciduous tree, small round crown",
                     "maple tree, full round lobed crown",
                     "ash tree, open airy crown"],
        "builtin": "res://sprites/trees/_hd_oak/",
        # Main's broadleaves since the pack swap (built-in oak, hazel and leafy tree became Dotty's oaks).
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Oaks/",
        "kind": "trees",
        "size": (350, 300),        # built-in _hd_oak, area-equivalent at scale 1 (builtin-sizes.json)
        "radius": 118, "offset_y": -130,  # built-in _hd_oak footprint and anchor
        "aspect": (0.65, 1.6),     # built-in oaks 0.74-1.12, hazels 0.83-1.71
        "pack_folder": "Tyrnarra_Broadleaves",
        "file": "broadleaf_{n:02d}",
    },
}

# Sprite finishing (sprites.py). Wonderdraft multiplies greyscale tree art by the ground colour,
# so the grey values decide how much ground shows through: its own conifers are near-white
# fill with black strokes.
TARGET_MEAN = 195     # average grey of the opaque tree pixels after levels (0-255)
INK_THIN = 0          # px narrower per side for dark lines (sprites.thin_ink); 3+ blobs the lines
OUTLINE = 4           # solid ring around the drawn edge, px; with INNER_LIGHTEN it separates trees at map scale
OUTLINE_GREY = 28
DEFRINGE = 0          # px eaten from the soft edge under the ring (the cut edge is colour-cleaned already)
INNER_LIGHTEN = 0.7   # 0-1: how far strokes inside the shape fade toward white (sprites.finish)
INNER_EDGE = 6        # px from the edge where that fading starts (full at twice this)

# Generation (generate.py): SDXL Turbo on the tower's ComfyUI, ~5 s per image.
CHECKPOINT = "DreamShaperXL_Turbo_v2.1.safetensors"
STEPS, CFG, SAMPLER, SCHEDULER = 7, 2.0, "dpmpp_sde", "karras"
WIDTH, HEIGHT = 832, 1216
BG_MODEL = "birefnet.safetensors"
