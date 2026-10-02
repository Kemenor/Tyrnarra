"""What to generate: art families, styles and the numbers that make them fit Wonderdraft.

Each family becomes one folder of Fuchsbau, Kartofuchs' own pack (art/Fuchsbau in a Kartofuchs
checkout). How the pack is tried on a real map: import it into Kartofuchs with the Fuchsbau art
mapping, which comes with Kartofuchs (README: Reviewing). The prompt lessons behind
these strings are in README.md ("Prompting").
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
    "icon": "bold black ink outlines, cream white walls, flat red roofs, hand-drawn fantasy cartography",
    # Terrain symbols: the watercolour styles drew detailed engravings and whole landscapes, and
    # "hand-drawn fantasy cartography" brought the hatching back; the bare wording (in the
    # subject) drew clean single mountains.
    "line": "",
}
LINE_FRAME = ", sketch, isolated on a plain white background"
# Mountains keep their ridge lines and shaded side: no inner fade, a thin ring.
TERRAIN_FINISH = {"OUTLINE": 2, "INNER_LIGHTEN": 0.0, "BASE_FADE": 0.15, "SKIRT_TRIM": 0.2}
# Mountains measured against Wonderdraft's jagged peaks (peaks round 7): a heavy ring and calm
# insides read like the built-ins' bold outlines; the thin-ringed line art read busy and small.
BOLD_TERRAIN = {"OUTLINE": 6, "INNER_LIGHTEN": 0.7, "BASE_FADE": 0.15, "SKIRT_TRIM": 0.2}
# Hills: Wonderdraft's are an upper arc only; many drawings closed their base into a loop, so
# the lower half fades out (hills round 4).
HILL_FINISH = {"OUTLINE": 4, "INNER_LIGHTEN": 0.0, "BASE_FADE": 0.5, "SKIRT_TRIM": 0.2}
# FLUX trees in the "bold" style (tree review): the drawing's own few thick strokes are the
# texture, so nothing fades them.
BOLD_TREE = {"INNER_LIGHTEN": 0.0}
LINE_NEGATIVE = ("photo, realistic, 3d render, text, letters, caption, watermark, signature, landscape, scene, "
                 "panorama, horizon, sky, clouds, sun, birds, trees, forest, several mountains, mountain range, "
                 "background, parchment, paper texture, border, frame, cropped, blurry, detailed, shading, hatching")

# The settlement kinds, shared by the raised (2.5D) and the flat (2D) icon families. Kartofuchs
# guesses each icon's role from these item names (README: Families): keep them.
SETTLEMENT_ITEMS = [("hamlet", "hamlet of two small cottages with thatched roofs"),
                    ("village", "village of five cottages around a small chapel"),
                    ("town", "small town of tall houses around a church tower"),
                    ("walled_town", "town behind a low round stone wall with a gate"),
                    ("city", "large city of many tightly packed houses, towers and a cathedral"),
                    ("walled_city", "large city inside a ring of stone walls with towers"),
                    ("capital", "grand capital city behind high walls, with a domed palace and tall towers"),
                    ("castle", "castle with a keep and four corner towers"),
                    ("fortress", "massive stone fortress with thick walls and a gatehouse"),
                    ("tower", "lone tall stone watchtower"),
                    ("port", "harbour town with houses, a lighthouse and a jetty with a small ship"),
                    ("temple", "temple with columns and a dome"),
                    ("monastery", "walled monastery with a bell tower"),
                    ("ruins", "ruined castle with broken walls and a collapsed tower"),
                    ("mine", "mine entrance in a rock face with a wooden headframe"),
                    ("farmstead", "farmstead with a barn, a windmill and a fenced field"),
                    ("camp", "camp of several canvas tents around a campfire, only tents, no buildings"),
                    ("inn", "roadside inn with a hanging sign and a stable")]

# Flat (2D) icon wordings where the shared one failed: "a town behind a round wall" drew the wall
# in perspective; the camp's wide scene ran off the image.
FLAT_ITEMS = {
    "walled_town": ("small town behind a low stone wall seen straight from the front: the wall one flat band across "
                    "the bottom with a gate in the middle, the houses and a church tower rising behind it"),
    "walled_city": ("large city behind a high stone wall seen straight from the front: the wall one flat band across "
                    "the bottom with square towers and a gate, many roofs, towers and a cathedral rising behind it"),
    # Seeds 106+: "tents around a campfire" drew red-domed stone houses behind the tents (the style
    # asks for red roofs and domes).
    "camp": "small compact camp of three canvas tents close around a campfire, only tents, no buildings",
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
        "kind": "trees",           # Wonderdraft sprite folder: trees | mountains | symbols
        "size": (185, 330),        # px at Wonderdraft scale 1, matched by area (built-in tree_xmas ~170-210 x 300-415)
        "radius": 51, "offset_y": -73,   # built-in tree_xmas footprint and anchor
        "aspect": (1.3, 2.6),      # height / width a usable cut-out must have
        "pack_folder": "Fuchsbau_Conifers",
        # Round 13: the 0.7 inner fade left the densest drawings as blank pale shapes without their
        # branch tiers; half the fade and 2 px bolder strokes keep the tiers, like Wonderdraft's own.
        "finish": {"INNER_LIGHTEN": 0.35, "INK_THIN": -2},
        # Round 17 (the user: "some less textured ones jump out"): only drawings whose finished
        # inside keeps its dark branch tiers (13% of it strokes at map scale; the flat ones had
        # 4-9%, at 12% they still looked soft) and whose edge is clean (the hazy sepia ones had
        # 0.064-0.09 soft alpha per opaque pixel). 77 of 279 pass.
        "min_texture": 0.13, "max_haze": 0.06,
        "file": "conifer_{n:02d}",
    },
    "broadleaf": {
        # SDXL Turbo would not draw a short trunk or a wide crown (tall naturalistic trees,
        # tree-of-life roots, circle frames); FLUX.2 does as asked (README: Prompting).
        "engine": "flux", "canvas": (1024, 1024), "styles": ["bold"], "finish": BOLD_TREE,
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No roots, no visible branches, no ground.",
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading, short visible trunk"),
        # Oaks and hazels were Main's two big broadleaf families; the rest adds temperate variety.
        "variants": ["oak tree: one big round puffy crown of scalloped leafy bumps, wider than it is tall, on a very short stubby trunk",
                     "old oak tree: a broad spreading crown of billowing lobes, much wider than tall, on a short thick trunk",
                     "hazel: a bushy round crown on several thin short stems",
                     "beech tree: a dense smooth domed crown on a short straight trunk",
                     "linden tree: a tall rounded egg-shaped crown on a short trunk",
                     "young tree: a small round crown on a thin short trunk",
                     "maple tree: a full round leafy crown on a short trunk",   # "lobed" drew a maple leaf
                     "ash tree: an open airy crown of a few rounded leaf clusters on a short trunk"],
        # Main's broadleaves since the pack swap (built-in oak, hazel and leafy tree became Dotty's oaks).
        "kind": "trees",
        "size": (350, 300),        # built-in _hd_oak, area-equivalent at scale 1 (builtin-sizes.json)
        "radius": 118, "offset_y": -130,  # built-in _hd_oak footprint and anchor
        "aspect": (0.65, 1.6),     # built-in oaks 0.74-1.12, hazels 0.83-1.71
        # ink 14, 23, 47 drew a giant maple leaf; bold 37 a blob with a flat cut-off bottom.
        "exclude": {"ink": [14, 23, 47], "bold": [37]},
        "pack_folder": "Fuchsbau_Broadleaves",
        "file": "broadleaf_{n:02d}",
    },
    "willow": {
        # SDXL drew mostly upright trees for "weeping willow" (1 in 6 wept); FLUX follows the shape.
        "engine": "flux", "canvas": (1024, 1024), "styles": ["bold"], "finish": BOLD_TREE,
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading, short visible trunk"),
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No roots, no ground.",
        "variants": ["weeping willow: a round dome of long drooping curtains of leaves hanging almost to the ground, short trunk",
                     "old weeping willow: a wide crown whose long branches hang straight down like a curtain",
                     "young weeping willow: a small dome of hanging leafy strands on a thin trunk",
                     "leaning weeping willow: the trunk tilted to one side, long strands of leaves drooping down"],
        "kind": "trees", "size": (260, 264), "radius": 128, "offset_y": -110, "aspect": (0.75, 1.5),
        "pack_folder": "Fuchsbau_Willows", "file": "willow_{n:02d}",
    },
    "pine": {
        # Mediterranean and mountain pines: Main's built-in cedars and umbrella pines, both
        # Dotty's pines since the swap. Round 7's "drooping boughs" conifers drew these unasked.
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading, visible trunk"),
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No roots, no ground.",
        "variants": ["umbrella pine, flat wide canopy on a tall bare trunk",
                     "cedar tree with flat layered horizontal tiers of foliage",
                     "old gnarled pine with a few cloud-like foliage pads",
                     "Scots pine, tall trunk with a rounded irregular crown",
                     "windswept mountain pine, crown blown to one side"],
        "kind": "trees", "size": (272, 300), "radius": 90, "offset_y": -130, "aspect": (0.6, 1.8),
        "pack_folder": "Fuchsbau_Pines", "file": "pine_{n:02d}",
        "exclude": {"ink": [13]},   # a watercolour stain cut out with the tree
    },
    "jungle": {
        # Rainforest canopy trees: Main's jungles are Dotty's kapoks (no built-in counterpart).
        "engine": "flux", "canvas": (1024, 1024), "styles": ["bold"], "finish": BOLD_TREE,
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No ground.",
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading"),
        "variants": ["tropical rainforest tree: a huge wide flat canopy of leafy clumps on a tall straight trunk",
                     "kapok tree: a broad layered canopy over a trunk with wide buttress roots",
                     "jungle tree: a dense round crown hung with a few vines",
                     "young jungle tree: big glossy leaves in a round crown on a slim trunk",
                     "strangler fig: a tangled trunk under a broad dense crown"],
        "exclude": {"ink": [8], "bold": [23]},   # a giant leaf bush without a trunk
        "kind": "trees", "size": (340, 320), "radius": 100, "offset_y": -140, "aspect": (0.6, 1.6),
        "pack_folder": "Fuchsbau_Jungle", "file": "jungle_{n:02d}",
    },
    "palm": {
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale leaves drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading"),
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No ground.",
        "variants": ["coconut palm tree, curved trunk, crown of long feathery fronds",
                     "date palm, straight ringed trunk, dense round crown of fronds",
                     "short fan palm with a bushy crown",
                     "pair of leaning palm trees"],
        # Alpha from the ink, a thin ring: the mask and a 4 px ring made the fronds a round disc.
        "ink_alpha": True, "finish": {"OUTLINE": 1, "INNER_LIGHTEN": 0.0},
        "kind": "trees", "size": (160, 240), "radius": 36, "offset_y": -100, "aspect": (1.0, 2.6),
        "pack_folder": "Fuchsbau_Palms", "file": "palm_{n:02d}",
    },
    "bamboo": {
        # A clump is many stalks: kept as several pieces, no ground trim (1 of 48 passed as a tree).
        "shape": "clump", "fill": (0.12, 0.8),
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale leaves drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading"),
        "flux": "A {variant}, drawn as a symbol for a hand-drawn fantasy map. No ground.",
        "variants": ["clump of tall bamboo stalks with leafy tops",
                     "small grove of bamboo, stalks of different heights",
                     "single tall bamboo cluster bending slightly"],
        "kind": "trees", "size": (170, 300), "radius": 40, "offset_y": -130, "aspect": (1.2, 3.0),
        "pack_folder": "Fuchsbau_Bamboo", "file": "bamboo_{n:02d}",
        "exclude": {"ink": [16, 19, 46]},   # bamboo forest scenes, cut into loose stalks
    },
    "deadtree": {
        # Blighted lands, swamps and winter; not in Main yet, compared with Dotty's dead trees.
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, drawn with confident ink lines, lots of white paper showing, minimal shading"),
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No ground.",
        "variants": ["dead leafless tree with gnarled bare branches",
                     "broken dead tree stump with a few crooked branches",
                     "twisted dead tree leaning to one side",
                     "bare winter tree with a round crown of thin branches"],
        # Gnarled roots flare as wide as the crown and bare branches fill little: 0 of 48 passed.
        # Alpha from the ink, a thin ring, no fade: the mask and a thick ring filled the crowns in.
        "base_max": 0.95, "fill": (0.12, 0.8), "ink_alpha": True,
        "finish": {"OUTLINE": 1, "INNER_LIGHTEN": 0.0},
        "kind": "trees", "size": (250, 300), "radius": 70, "offset_y": -130, "aspect": (0.7, 2.0),
        "pack_folder": "Fuchsbau_Dead_Trees", "file": "deadtree_{n:02d}",
        "exclude": {"ink": [21, 41]},   # hollow stumps drawn in 3D, unlike the flat others
    },
    "savanna": {
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading"),
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No ground.",
        # Seeds 49+ (round 3): the first wording drew ordinary round trees for "acacia".
        "variants": ["acacia tree with a very flat wide umbrella-shaped crown, much wider than tall, on a thin trunk "
                     "forking into a few bare branches",
                     "wide acacia tree with a flat layered crown like a table top",
                     "baobab tree, huge thick bottle-shaped trunk with a small crown of stubby branches",
                     "small thorny acacia bush with a flat top"],
        "kind": "trees", "size": (340, 250), "radius": 90, "offset_y": -105, "aspect": (0.45, 1.5),
        "pack_folder": "Fuchsbau_Savanna", "file": "savanna_{n:02d}",
    },
    "desert": {
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, drawn with a few confident ink lines, lots of white paper showing, minimal shading"),
        "flux": "A single {variant}, drawn as a symbol for a hand-drawn fantasy map. No ground.",
        # Seeds 49+ (round 3): six shapes; the barrel cactus came out as a near-identical oval every
        # time, so the old barrel seeds (seed % 4 == 2) are left out.
        "variants": ["saguaro cactus with two raised arms",
                     "tall saguaro cactus with one arm",
                     "saguaro cactus with three arms",
                     "prickly pear cactus with a few flat paddle pads",
                     "young saguaro cactus, a single tall column",
                     "group of three small column cacti"],
        "exclude": {"ink": [s for s in range(1, 49) if s % 4 == 2]},
        "base_max": 1.0,           # a barrel cactus is widest at the ground
        "kind": "trees", "size": (150, 240), "radius": 40, "offset_y": -100, "aspect": (0.7, 2.6),
        "pack_folder": "Fuchsbau_Cactuses", "file": "cactus_{n:02d}",
    },
    "fungal": {
        # Giant-mushroom forests for strange and underground lands; clusters are several pieces.
        "shape": "clump",
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, drawn with a few confident ink lines, lots of white paper showing, minimal shading"),
        "flux": "A single {variant}, drawn as a symbol for a hand-drawn fantasy map. No ground.",
        "variants": ["giant mushroom with a wide round cap on a tall stem",
                     "cluster of three giant mushrooms of different heights",
                     "giant toadstool with a spotted domed cap",
                     "tall thin giant mushroom with a small conical cap"],
        "kind": "trees", "size": (240, 260), "radius": 70, "offset_y": -110, "aspect": (0.6, 2.2),
        "pack_folder": "Fuchsbau_Mushrooms", "file": "mushroom_{n:02d}",
        # Round 3: half the inner fade and 1 px bolder strokes bring back the caps' dots and gills.
        "finish": {"INNER_LIGHTEN": 0.35, "INK_THIN": -1},
    },
    "swamp": {
        # Swamps and marshes (night of 2026-09-28, "any yet missing assets"). Stilt roots and flared
        # bases are as wide as the crown, so no ground trim: kept whole as a clump.
        "engine": "flux", "canvas": (1024, 1024), "styles": ["bold"], "finish": BOLD_TREE, "shape": "clump",
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No ground, no water.",
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines"),
        "variants": ["bald cypress: a tall narrow crown of drooping feathery foliage on a trunk flaring wide at the base, "
                     "with a few knobby knees beside it",
                     "mangrove: a round bushy crown held up on a tangle of arching stilt roots",
                     "swamp tree hung with long curtains of moss from a broad crooked crown",
                     "gnarled swamp tree: a twisted leaning trunk with a small ragged crown",
                     "young mangrove: a small round crown on a few arching roots"],
        # The young mangroves (seed % 5 == 4) drew big single leaves across the crown, like the maples.
        "exclude": {"bold": [4, 9, 14, 19, 24, 29]},
        "kind": "trees", "size": (260, 300), "radius": 90, "offset_y": -120, "aspect": (0.7, 1.9), "fill": (0.2, 0.9),
        "pack_folder": "Fuchsbau_Swamp_Trees", "file": "swamp_{n:02d}",
    },
    "shrubs": {
        # Bushes and scrub to scatter over open land (night of 2026-09-28).
        "engine": "flux", "canvas": (1024, 1024), "styles": ["bold"], "finish": BOLD_TREE, "shape": "clump",
        "flux": "A single {variant}, drawn as a small plant symbol for a hand-drawn fantasy map. No ground.",
        "subject": "a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at small size",
        "variants": ["round leafy bush", "low wide shrub of a few rounded leafy clumps",
                     "thorny scrub bush of bare twigs with a few small leaves", "heather bush: a low mound of tiny flowers"],
        "kind": "trees", "size": (140, 110), "radius": 45, "offset_y": -40, "aspect": (0.35, 1.4), "fill": (0.25, 0.95),
        "pack_folder": "Fuchsbau_Shrubs", "file": "shrub_{n:02d}",
    },

    # --- mountains, hills, dunes: greyscale like the trees, centred on the click point -------
    "peaks": {
        "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME, "finish": BOLD_TERRAIN, "negative": LINE_NEGATIVE,
        # Round 4 wording: "flat bottom edge" drew base lines that stacked into stripes across a range.
        "subject": ("minimalist black line drawing of one single {variant}, simple clean outline with two or three "
                    "inner ridge lines, white inside, steep sides, fantasy map symbol"),
        "flux": "A single {variant}, drawn as a mountain symbol for a hand-drawn fantasy map: flat base line, nothing around it.",
        "variants": ["tall jagged mountain", "mountain with two sharp peaks", "craggy mountain with a snowy top",
                     "broad mountain with two summits", "steep rocky spire", "mountain with a long ridge sloping to one side"],
        # Sized by area, not width: ours are wider than the built-ins' tall peaks, so width made them low.
        "kind": "mountains",
        "size": (400, 280),        # 3x the built-in's area-equivalent 131 x 92: sharp at Main's big scales
        "radius": 45, "offset_y": 0, "aspect": (0.3, 1.1), "fill": (0.2, 0.9),
        "drop_thin": 14,   # base strokes under 28 px that stick out of the body dropped (sprites.drop_thin)
        "pack_folder": "Fuchsbau_Peaks", "file": "peak_{n:02d}",
    },
    "fells": {
        "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME, "finish": BOLD_TERRAIN, "negative": LINE_NEGATIVE,
        "subject": ("minimalist black line drawing of one single {variant}, simple clean outline with one or two "
                    "soft inner lines, white inside, flat bottom edge, fantasy map symbol"),
        "flux": "A single {variant}, drawn as a mountain symbol for a hand-drawn fantasy map: flat base line, nothing around it.",
        "variants": ["rounded old mountain with a soft dome top", "worn mountain with two gentle rounded humps",
                     "broad rounded mountain with a shallow saddle", "low rounded mountain with a rocky shoulder"],
        "kind": "mountains", "size": (330, 190), "radius": 33, "offset_y": 0, "aspect": (0.2, 1.0), "fill": (0.2, 0.9),
        "drop_thin": 14,   # base strokes under 28 px that stick out of the body dropped (sprites.drop_thin)
        "pack_folder": "Fuchsbau_Fells", "file": "fell_{n:02d}",
    },
    "hills": {
        "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME, "finish": HILL_FINISH, "negative": LINE_NEGATIVE + ", houses, buildings, road, path, fence",
        # Round 2 wording: the first drew landscapes, hills with houses and trees, and wavy lines.
        "subject": ("minimalist black line drawing of one single {variant}, one smooth curved outline like a gentle "
                    "dome, one or two short inner strokes, white inside, nothing on top, fantasy map symbol"),
        "flux": "A single {variant}, drawn as a hill symbol for a hand-drawn fantasy map: flat base line, nothing around it.",
        "variants": ["low rounded hill", "gentle wide hill", "small rounded knoll", "long low hill"],
        # A scribble in a circle (118), a volcano from above (122), an empty ellipse (134): all
        # three showed as black circles in a range; 113 and 147 stand on a full ellipse base.
        "exclude": {"line": [113, 118, 122, 134, 147]},
        # Sparse outlines are fine: Wonderdraft's own hills are little more than an arc.
        "kind": "mountains", "size": (300, 115), "radius": 30, "offset_y": 0, "aspect": (0.15, 0.7), "fill": (0.04, 0.9),
        "fill_under": True,   # solid body under the top contour (sprites.fill_under)
        "pack_folder": "Fuchsbau_Hills", "file": "hill_{n:02d}",
    },
    "dunes": {
        # SDXL drew desert photos and abstract swooshes for any single-dune wording: FLUX.
        "engine": "flux", "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME, "finish": TERRAIN_FINISH, "negative": LINE_NEGATIVE + ", desert, sand texture, photo of dunes",
        "subject": ("minimalist black line drawing of one single {variant} shape, a simple curved outline with a sharp "
                    "crest line, white inside, flat bottom edge, fantasy map symbol, like an icon"),
        "flux": "A single {variant}, drawn as a symbol for a hand-drawn fantasy map: flat base line, nothing around it.",
        # Seeds 25+ (round 3): the short names drew curls and swooshes; the shape spelled out.
        "variants": ["sand dune seen from the side: a smooth crescent-shaped mound, much wider than tall, with one sharp "
                     "curved crest line and soft shading on the steep side",
                     "long low sand dune seen from the side: a gentle wave-shaped mound with one crest line",
                     "pair of overlapping sand dunes seen from the side, the back one taller",
                     "tall sand dune seen from the side with a sharp crest and a steep shaded face"],
        "kind": "mountains", "size": (320, 90), "radius": 30, "offset_y": 0, "aspect": (0.1, 0.55), "fill": (0.2, 0.95),
        "pack_folder": "Fuchsbau_Dunes", "file": "dune_{n:02d}",
    },
    "mesas": {
        # Desert mesas, buttes and arches (night of 2026-09-28), in the peaks' bold finish.
        # Round 2: the peaks' 0.7 inner fade washed out the rock layers that make a mesa; 0.3 keeps them.
        "engine": "flux", "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME,
        "finish": dict(BOLD_TERRAIN, INNER_LIGHTEN=0.3), "negative": LINE_NEGATIVE,
        "exclude": {"line": [21]},   # a butte whose two feet left a notch in its base
        "flux": "A single {variant}, drawn as a mountain symbol for a hand-drawn fantasy map, seen from the side, nothing around it.",
        "subject": ("minimalist black line drawing of one single {variant}, simple clean outline with a few inner lines, "
                    "white inside, fantasy map symbol"),
        "variants": ["mesa: a wide flat-topped rock plateau with steep cliff sides striped by horizontal rock layers",
                     "butte: a tall narrow flat-topped rock tower with sheer sides",
                     "pair of mesas, a big flat-topped one behind a smaller one",
                     "natural rock arch bridging two stone pillars",
                     "cluster of three tall rock spires of different heights"],
        "kind": "mountains", "size": (380, 220), "radius": 60, "offset_y": 0, "aspect": (0.25, 1.3), "fill": (0.2, 0.95),
        "drop_thin": 14,
        "pack_folder": "Fuchsbau_Mesas", "file": "mesa_{n:02d}",
    },
    "pillars": {
        # Tall karst pillars (2026-09-29): Main's Tang Dynasty mountains (141, e.g. the ring around the
        # Air Monastery) are tall narrow crags; the peaks in their place spread into one wide mass.
        "engine": "flux", "shape": "mountain", "canvas": (832, 1216), "styles": ["line"], "frame": LINE_FRAME,
        "finish": dict(BOLD_TERRAIN, INNER_LIGHTEN=0.3, BASE_FADE=0.25), "negative": LINE_NEGATIVE,
        # Many pillars are open at the base (hollow without a fill), but fill_under built
        # straight-sided boxes under a pine's crown or a faint background peak: fill_enclosed.
        "fill_enclosed": True,
        # 12, 16, 24, 28: a faint background peak filled into a flat tab beside the pillar; the rest
        # are the two pine variants the user removed.
        "exclude": {"line": [12, 16, 24, 28] + [s for s in range(1, 31) if s % 6 in (0, 5)]},
        "flux": ("A single {variant}, drawn as a mountain symbol for a hand-drawn fantasy map in the manner of a "
                 "Chinese ink painting, seen from the side, much taller than wide, nothing around it."),
        "subject": ("minimalist black line drawing of one single {variant}, tall and narrow, sheer sides with a few "
                    "vertical crack lines, white inside, fantasy map symbol"),
        # Round 1 had six variants (seed % 6); the user dropped the two with a pine (a rounded
        # pillar with a pine near the top, a leaning needle with a pine crown: seeds % 6 == 0, 5).
        # New seeds (31+) cycle through these four.
        "variants": ["pair of tall karst pillars side by side, one taller than the other",
                     "tall craggy rock tower with a slanted top and a smaller crag at its foot",
                     "cluster of three narrow rock spires of different heights",
                     "massive rounded karst peak, taller than wide, with steep grooved sides"],
        # About 2x the area of the Tang pillars' area-equivalent 222 x 314, like the peaks: sharp at big scales.
        "kind": "mountains", "size": (300, 430), "radius": 50, "offset_y": 0, "aspect": (1.0, 3.0), "fill": (0.25, 0.95),
        "pack_folder": "Fuchsbau_Pillars", "file": "pillar_{n:02d}",
    },
    "volcanoes": {
        # "Volcanic was missing" (the user, 2026-09-28). Recolourable like the icons: R ink, G rock and
        # smoke, B lava and glow, so each volcano's lava colour is picked on the map.
        # The extinct cones need style "quiet": "lava" names lava and smoke, and FLUX drew them anyway
        # (seeds 35-59 in "lava" came out active and are left out).
        "shape": "icon", "draw": "custom_colors", "engine": "flux", "canvas": (1024, 1024), "styles": ["lava", "quiet"],
        "exclude": {"lava": [35, 41, 47, 53, 59]},
        "flux": "A single {variant}, drawn as a mountain symbol for a hand-drawn fantasy map, seen from the side.",
        "subject": "a single {variant}, fantasy map symbol, bold black outlines",
        "variants": ["active volcano: a tall cone with a crater at the top and a thick plume of smoke rising from it",
                     "erupting volcano: a steep cone with glowing lava streams running down its sides and fire at the top",
                     "broad volcano: a wide low cone with a large crater rim and a thin wisp of smoke",
                     "small volcanic cone: a short steep cone with a smoking crater",
                     "volcano with a lava lake: a broken crater rim around a glowing pool of lava",
                     # Seeds 35+: "dormant" still drew smoke and fire (round 1: 5, 11, 17, 23, 29).
                     "extinct volcano: a quiet grey cone with a wide empty crater, no smoke, no fire, no lava"],
        "kind": "symbols", "size": (340, 280), "radius": 90, "offset_y": 0, "aspect": (0.4, 1.6), "fill": (0.2, 0.97),
        "pack_folder": "Fuchsbau_Volcanoes", "file": "volcano_{n:02d}",
    },

    # --- icons: recolourable (Wonderdraft custom colours: R lines, G walls, B roofs) -------------
    "settlements": {
        "shape": "icon", "draw": "custom_colors", "engine": "flux", "canvas": (1024, 1024), "styles": ["icon"],
        "flux": "A {variant}, drawn as a settlement symbol for a hand-drawn fantasy map, seen from a slightly raised side view.",
        "items": SETTLEMENT_ITEMS,
        "per_item": 3,
        # Kartofuchs guesses each icon's role from these item names (README: Families): keep them.
        "kind": "symbols", "size": (260, 200), "radius": 60, "offset_y": 0, "aspect": (0.35, 2.8), "fill": (0.3, 0.97),
        # The raised view reads as 2.5D; the user filed these under it once flat 2D icons were asked for.
        "pack_folder": "Fuchsbau_2.5D_Settlements", "file": "{item}_{n}",
    },
    "settlements_2d": {
        # "Can we generate some true 2D ones? Just to see" (the user, 2026-09-27): the same kinds as
        # flat, straight-on map symbols, beside the raised view of "settlements". A flat village
        # is a row of separate houses: kept as several pieces (shape "clump"), not rejected.
        "shape": "clump", "draw": "custom_colors", "engine": "flux", "canvas": (1024, 1024), "styles": ["icon"],
        "flux": ("A {variant}, drawn as a flat 2D symbol for a hand-drawn fantasy map: seen straight from the front, "
                 "no perspective and no depth, the buildings standing side by side like a skyline, as on old maps."),
        # Round 2 (seeds 20+): the walled ones came out raised; their wall spelled out as a flat band.
        "items": [(k, FLAT_ITEMS.get(k, d)) for k, d in SETTLEMENT_ITEMS],
        "exclude": {"icon": [3, 5]},   # the raised walled town and walled city of round 1
        "per_item": 2,
        "kind": "symbols", "size": (260, 200), "radius": 60, "offset_y": 0, "aspect": (0.25, 2.8), "fill": (0.3, 0.97),
        "pack_folder": "Fuchsbau_2D_Settlements", "file": "{item}_{n}",
    },
    "landmarks": {
        # Single structures a world map marks (night of 2026-09-28), in the settlements' raised view
        # and colours. Not settlements: Kartofuchs' role guessing ignores these item names.
        # Round 1 ("icon" style): the lighthouses, shrines and beacons came out right; the style's
        # "roofs and domes" put red-domed houses around the stones, the obelisk, the statue (on a
        # whole castle), the bridge and the arch, and the statue looked like a real religious figure.
        # Those five are redrawn in style "landmark" (seeds 104+).
        "shape": "icon", "draw": "custom_colors", "engine": "flux", "canvas": (1024, 1024), "styles": ["icon", "landmark"],
        "exclude": {"icon": [8, 16, 24, 1, 9, 17, 4, 12, 20, 5, 13, 21, 7, 15, 23]},
        "flux": "A {variant}, drawn as a landmark symbol for a hand-drawn fantasy map, seen from a slightly raised side view.",
        "items": [("standing_stones", "ring of tall rough standing stones"),
                  ("obelisk", "tall stone obelisk on a stepped base"),
                  ("lighthouse", "tall lighthouse on a small rocky point"),
                  ("shrine", "small roadside shrine with a little roof and an offering stone"),
                  ("statue", "giant stone statue of a hooded, faceless robed guardian holding a staff, on a plain square plinth"),
                  ("bridge", "old stone bridge of three arches"),
                  ("beacon", "hilltop beacon: a squat stone tower with a big fire burning on top"),
                  ("portal", "ancient stone archway carved with runes, standing alone")],
        "per_item": 2,
        "kind": "symbols", "size": (220, 220), "radius": 60, "offset_y": 0, "aspect": (0.35, 2.8), "fill": (0.2, 0.97),
        "pack_folder": "Fuchsbau_2.5D_Landmarks", "file": "{item}_{n}",
    },
    "god_cities": {
        # One themed icon per Bound god-city, from docs/god-city-seeds.md (open, chronicler-tier
        # features only: what a traveller sees).
        "shape": "icon", "draw": "custom_colors", "engine": "flux", "canvas": (1024, 1024), "styles": ["icon"],
        "flux": "A {variant}, drawn as a city symbol for a hand-drawn fantasy map, seen from a slightly raised side view.",
        "items": [("merkavar", "lakeside trade city of domed market halls and awnings, a ring of market boats and barges moored along its shore"),
                  ("myrria", "dark hillside city of narrow towers, its long winding stairways lit by lanterns"),
                  ("eldara", "city carved into a smoking volcano, with stone halls, forge chimneys and wild wooden scaffolding"),
                  ("uravel", "scatter of small islets with houses, linked by ropes and hanging bells, glass domes half-sunk in the water beneath"),
                  ("haizava", "city of sails, wind vanes and windmills, its towers linked by rope bridges"),
                  ("lurrath", "massive round ring of stone walls enclosing a solid squat stone city with ramps and a great central keep"),
                  ("ljosarn", "lakeside city of lanterns around a tall beacon tower shining rays of light"),
                  ("thekkavar", "great academy of domes, towers and libraries above stairs descending deep into the ground"),
                  # Lograth seeds 203+: the first wording drew the aerial lines as a tent-like sheet.
                  ("lograth", "judgment city: a royal throne-hall and a tall temple crowned with a great pair of scales, facing each other across one wide paved square, joined in the middle by a bridge-like hall of courts, many small courthouses around them, and a few thin straight cables strung between slender towers with small gondolas hanging from them"),
                  ("veidrath", "ancient stone temple core ringed by newer stone districts with an airship mooring tower, circles of tents around it"),
                  ("nahaskel", "jumble of mismatched crooked buildings and impossible twisting towers stacked on top of each other"),
                  ("valreka", "city with a palace and a temple built on the back of a giant whale swimming in the sea, smaller whales carrying houses beside it"),
                  ("frae_city", "city on a great rock floating above a lake, held down by seven huge chains")],
        "per_item": 2,
        "kind": "symbols", "size": (320, 260), "radius": 80, "offset_y": 0, "aspect": (0.35, 1.8), "fill": (0.3, 0.97),
        "pack_folder": "Fuchsbau_2.5D_God_Cities", "file": "{item}_{n}",
    },
}

# FLUX.2 styles (comfy.flux_images; natural sentences, no negative prompt). Greyscale families
# become greyscale anyway; "icon" asks for flat colours that sprites.finish_cc sorts into its
# three colour masks (ink lines, pale walls, coloured roofs).
FLUX_STYLES = {
    "ink": ("Black ink with a light grey wash: a bold clean outline, a pale fill with only a few confident strokes "
            "inside, soft shading on one side. Simple and readable at small size. Isolated on a plain white "
            "background, nothing else in the image."),
    "sepia": ("Sepia-brown ink with a pale warm wash: a bold clean outline, a light fill with a few fine hatching "
              "strokes, shading on one side. Simple and readable at small size. Isolated on a plain white "
              "background, nothing else in the image."),
    # Wonderdraft's own trees: a flat pale fill and a few thick black strokes where the clumps
    # overlap. "ink" drew grey wash and many small leaf marks that blur to speckle at map size.
    # "Like a sticker" drew a sticker: a white die-cut border and a drop shadow.
    "bold": ("Bold black brush-pen drawing: a thick black outline, the foliage drawn as a few big simple rounded "
             "shapes, with a few thick black curved strokes inside where the shapes overlap. Flat very pale fill, no "
             "grey wash, no small leaf marks, no hatching. Simple and readable at small size. Drawn directly on a "
             "plain white background: no border around it, no shadow, nothing else in the image."),
    # Volcanoes (custom colours): lava in the accent channel, rock and smoke in the body.
    "lava": ("Bold black ink outlines; rock left plain pale grey with light shading; lava, glow and fire painted in "
             "flat red-orange; smoke plain light grey. Simple, clean and readable at small size. Isolated on a plain "
             "white background, nothing else in the image, no ground, no text."),
    # Landmarks: one structure alone; "roofs and domes painted red" (icon) built a town around each.
    "landmark": ("Bold black ink outlines; stone left plain cream-white with light grey shading; red only on a roof "
                 "if it has one. A single structure standing alone: no houses, towers, domes or walls around it; no "
                 "flags or banners. Simple, clean and readable at small size. Isolated on a plain white background, "
                 "nothing else in the image, no text."),
    "quiet": ("Bold black ink outlines; rock left plain pale grey with light shading; a still, cold mountain. Simple, "
              "clean and readable at small size. Isolated on a plain white background, nothing else in the image, no "
              "ground, no text."),
    "line": ("Clean black ink line drawing: a bold clean outline, a few inner lines, white inside, a little grey "
             "shading on one side. Simple and readable at small size. Isolated on a plain white background, nothing "
             "else in the image."),
    # Seeds 101+ (round 2 of the icons): "roofs, flags and domes painted in flat red" put red
    # flags on every icon, even the mine and the camp.
    "icon": ("Bold black ink outlines; walls left plain cream-white with light grey shading; roofs and domes "
             "painted in flat red; no flags or banners. Simple, clean and readable at small size. Isolated on a "
             "plain white background, nothing else in the image, no ground, no text."),
}
FLUX_BATCH = 1        # images per FLUX graph: a 4-image graph wedged the tower (2026-09-27)
SDXL_BATCH = 8        # images per SDXL graph: the tower's --cache-none server reloads models per graph


def variants(fam):
    """The subject variants of a family: its items' descriptions, or its variants."""
    return [d for _, d in fam["items"]] if "items" in fam else (fam.get("variants") or [""])


def prompt(fam, style, seed, engine):
    """The prompt for one seed: the family's variant seed % len, in the engine's wording."""
    v = variants(fam)[seed % len(variants(fam))]
    if engine == "flux":
        return fam["flux"].format(variant=v) + " " + FLUX_STYLES[style]
    tail = STYLES[style]
    return fam["subject"].format(variant=v) + fam.get("frame", FRAME) + (", " + tail if tail else "")


def styles(fam):
    return fam.get("styles", ["ink", "sepia"])


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
BASE_FADE = 0.0       # share of the height over which the bottom fades out (mountains' open base)
SKIRT_TRIM = 0.0      # mountains: cut the flanks where the shape is lower than this share of its peak
# Custom-colour art (icons; sprites.finish_cc): R = ink lines, G = body, B = accents.
OUTLINE_CC = 3        # solid ink ring, px
CC_INK_LUM = 0.42     # luminance below which a pixel turns into ink (fully by 0.17)
CC_ACCENT_SAT = 0.28  # saturation above which a pixel is an accent (roof, banner) rather than body

# Generation (generate.py): SDXL Turbo on the tower's ComfyUI, ~5 s per image.
CHECKPOINT = "DreamShaperXL_Turbo_v2.1.safetensors"
STEPS, CFG, SAMPLER, SCHEDULER = 7, 2.0, "dpmpp_sde", "karras"
WIDTH, HEIGHT = 832, 1216
BG_MODEL = "birefnet.safetensors"
