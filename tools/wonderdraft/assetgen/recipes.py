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
LINE_NEGATIVE = ("photo, realistic, 3d render, text, letters, caption, watermark, signature, landscape, scene, "
                 "panorama, horizon, sky, clouds, sun, birds, trees, forest, several mountains, mountain range, "
                 "background, parchment, paper texture, border, frame, cropped, blurry, detailed, shading, hatching")

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
        # SDXL Turbo would not draw a short trunk or a wide crown (tall naturalistic trees,
        # tree-of-life roots, circle frames); FLUX.2 does as asked (README: Prompting).
        "engine": "flux", "canvas": (1024, 1024), "styles": ["ink"],
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
        "builtin": "res://sprites/trees/_hd_oak/", "place": "fit",
        # Main's broadleaves since the pack swap (built-in oak, hazel and leafy tree became Dotty's oaks).
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Oaks/",
        "kind": "trees",
        "size": (350, 300),        # built-in _hd_oak, area-equivalent at scale 1 (builtin-sizes.json)
        "radius": 118, "offset_y": -130,  # built-in _hd_oak footprint and anchor
        "aspect": (0.65, 1.6),     # built-in oaks 0.74-1.12, hazels 0.83-1.71
        "exclude": {"ink": [14, 23, 47]},  # these drew a giant maple leaf
        "pack_folder": "Tyrnarra_Broadleaves",
        "file": "broadleaf_{n:02d}",
    },
    "willow": {
        # SDXL drew mostly upright trees for "weeping willow" (1 in 6 wept); FLUX follows the shape.
        "engine": "flux", "canvas": (1024, 1024), "styles": ["ink"],
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading, short visible trunk"),
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No roots, no ground.",
        "variants": ["weeping willow: a round dome of long drooping curtains of leaves hanging almost to the ground, short trunk",
                     "old weeping willow: a wide crown whose long branches hang straight down like a curtain",
                     "young weeping willow: a small dome of hanging leafy strands on a thin trunk",
                     "leaning weeping willow: the trunk tilted to one side, long strands of leaves drooping down"],
        "builtin": "res://sprites/trees/_hd_willow/", "place": "fit",
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Willows/",
        "kind": "trees", "size": (260, 264), "radius": 128, "offset_y": -110, "aspect": (0.75, 1.5),
        "pack_folder": "Tyrnarra_Willows", "file": "willow_{n:02d}",
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
        "builtin": "res://sprites/trees/_hd_cedar/", "place": "fit",
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Pines/",
        "kind": "trees", "size": (272, 300), "radius": 90, "offset_y": -130, "aspect": (0.6, 1.8),
        "pack_folder": "Tyrnarra_Pines", "file": "pine_{n:02d}",
    },
    "jungle": {
        # Rainforest canopy trees: Main's jungles are Dotty's kapoks (no built-in counterpart).
        "engine": "flux", "canvas": (1024, 1024), "styles": ["ink"],
        "flux": "A single {variant}, drawn as a tree symbol for a hand-drawn fantasy map. No ground.",
        "subject": ("a single chunky {variant} icon for a fantasy map, stylized, bold simple shape readable at "
                    "small size, pale foliage drawn with a few confident ink lines, lots of white paper showing, "
                    "minimal shading"),
        "variants": ["tropical rainforest tree: a huge wide flat canopy of leafy clumps on a tall straight trunk",
                     "kapok tree: a broad layered canopy over a trunk with wide buttress roots",
                     "jungle tree: a dense round crown hung with a few vines",
                     "young jungle tree: big glossy leaves in a round crown on a slim trunk",
                     "strangler fig: a tangled trunk under a broad dense crown"],
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Kapoks/",
        "exclude": {"ink": [8]},   # a giant leaf bush
        "kind": "trees", "size": (340, 320), "radius": 100, "offset_y": -140, "aspect": (0.6, 1.6),
        "pack_folder": "Tyrnarra_Jungle", "file": "jungle_{n:02d}",
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
        "builtin": "res://sprites/trees/toon_palm/", "place": "fit",
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Palms/",
        "kind": "trees", "size": (160, 240), "radius": 36, "offset_y": -100, "aspect": (1.0, 2.6),
        "pack_folder": "Tyrnarra_Palms", "file": "palm_{n:02d}",
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
        "replaces": "user://assets/Nibroc's Bamboo Forest/sprites/trees/Bamboo Trees/",
        "kind": "trees", "size": (170, 300), "radius": 40, "offset_y": -130, "aspect": (1.2, 3.0),
        "pack_folder": "Tyrnarra_Bamboo", "file": "bamboo_{n:02d}",
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
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Dead_Trees/",
        # Gnarled roots flare as wide as the crown and bare branches fill little: 0 of 48 passed.
        # Alpha from the ink, a thin ring, no fade: the mask and a thick ring filled the crowns in.
        "base_max": 0.95, "fill": (0.12, 0.8), "ink_alpha": True,
        "finish": {"OUTLINE": 1, "INNER_LIGHTEN": 0.0},
        "kind": "trees", "size": (250, 300), "radius": 70, "offset_y": -130, "aspect": (0.7, 2.0),
        "pack_folder": "Tyrnarra_Dead_Trees", "file": "deadtree_{n:02d}",
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
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Acacias/",
        "compare": ["user://assets/Dotty_Assets/sprites/trees/Dotty_Acacias/",
                    "user://assets/Dotty_Assets/sprites/trees/Dotty_Baobabs/"],
        "kind": "trees", "size": (340, 250), "radius": 90, "offset_y": -105, "aspect": (0.45, 1.5),
        "pack_folder": "Tyrnarra_Savanna", "file": "savanna_{n:02d}",
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
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Cactuses/",
        "base_max": 1.0,           # a barrel cactus is widest at the ground
        "kind": "trees", "size": (150, 240), "radius": 40, "offset_y": -100, "aspect": (0.7, 2.6),
        "pack_folder": "Tyrnarra_Cactuses", "file": "cactus_{n:02d}",
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
        "replaces": "user://assets/Dotty_Assets/sprites/trees/Dotty_Mushrooms/",
        "kind": "trees", "size": (240, 260), "radius": 70, "offset_y": -110, "aspect": (0.6, 2.2),
        "pack_folder": "Tyrnarra_Mushrooms", "file": "mushroom_{n:02d}",
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
        "builtin": "res://sprites/mountains/playful_jagged_peaks/", "place": "fit", "match": "area",
        "replaces": "user://assets/Moulk's AI Fantasy Cartography Megapack/sprites/mountains/mountains sample 1/",
        "kind": "mountains",
        "size": (400, 280),        # 3x the built-in's area-equivalent 131 x 92: sharp at Main's big scales
        "radius": 45, "offset_y": 0, "aspect": (0.3, 1.1), "fill": (0.2, 0.9),
        "pack_folder": "Tyrnarra_Peaks", "file": "peak_{n:02d}",
    },
    "fells": {
        "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME, "finish": BOLD_TERRAIN, "negative": LINE_NEGATIVE,
        "subject": ("minimalist black line drawing of one single {variant}, simple clean outline with one or two "
                    "soft inner lines, white inside, flat bottom edge, fantasy map symbol"),
        "flux": "A single {variant}, drawn as a mountain symbol for a hand-drawn fantasy map: flat base line, nothing around it.",
        "variants": ["rounded old mountain with a soft dome top", "worn mountain with two gentle rounded humps",
                     "broad rounded mountain with a shallow saddle", "low rounded mountain with a rocky shoulder"],
        "builtin": "res://sprites/mountains/playful_rounded_mountains/", "place": "fit", "match": "area",
        "replaces": "user://assets/Moulk's AI Fantasy Cartography Megapack/sprites/mountains/high hills 2/",
        "kind": "mountains", "size": (330, 190), "radius": 33, "offset_y": 0, "aspect": (0.2, 1.0), "fill": (0.2, 0.9),
        "pack_folder": "Tyrnarra_Fells", "file": "fell_{n:02d}",
    },
    "hills": {
        "shape": "mountain", "canvas": (1216, 832), "styles": ["line"], "frame": LINE_FRAME, "finish": HILL_FINISH, "negative": LINE_NEGATIVE + ", houses, buildings, road, path, fence",
        # Round 2 wording: the first drew landscapes, hills with houses and trees, and wavy lines.
        "subject": ("minimalist black line drawing of one single {variant}, one smooth curved outline like a gentle "
                    "dome, one or two short inner strokes, white inside, nothing on top, fantasy map symbol"),
        "flux": "A single {variant}, drawn as a hill symbol for a hand-drawn fantasy map: flat base line, nothing around it.",
        "variants": ["low rounded hill", "gentle wide hill", "small rounded knoll", "long low hill"],
        "builtin": "res://sprites/mountains/playful_hiils/", "place": "fit", "match": "width",
        "replaces": "user://assets/Moulk's AI Fantasy Cartography Megapack/sprites/mountains/medium hills 1/",
        "exclude": {"line": [118, 124, 137]},   # a scribble in a circle, a volcano from above, an ellipse
        # Sparse outlines are fine: Wonderdraft's own hills are little more than an arc.
        "kind": "mountains", "size": (300, 115), "radius": 30, "offset_y": 0, "aspect": (0.15, 0.7), "fill": (0.04, 0.9),
        "pack_folder": "Tyrnarra_Hills", "file": "hill_{n:02d}",
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
        "builtin": "res://packs/Arabia by Chan/sprites/mountains/sand_dunes_small/", "place": "fit", "match": "width",
        "replaces": "user://assets/Dotty_Assets/sprites/mountains/Dotty_Dunes/",
        "kind": "mountains", "size": (320, 90), "radius": 30, "offset_y": 0, "aspect": (0.1, 0.55), "fill": (0.2, 0.95),
        "pack_folder": "Tyrnarra_Dunes", "file": "dune_{n:02d}",
    },

    # --- icons: recolourable (Wonderdraft custom colours: R lines, G walls, B roofs) -------------
    "settlements": {
        "shape": "icon", "draw": "custom_colors", "engine": "flux", "canvas": (1024, 1024), "styles": ["icon"],
        "flux": "A {variant}, drawn as a settlement symbol for a hand-drawn fantasy map, seen from a slightly raised side view.",
        "items": [("hamlet", "hamlet of two small cottages with thatched roofs"),
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
                  ("camp", "camp of several tents around a campfire"),
                  ("inn", "roadside inn with a hanging sign and a stable")],
        "per_item": 3,
        # Kartofuchs guesses each icon's role from these item names (README: Families): keep them.
        "compare": ["user://assets/BSG_elvanos_mapIcons/sprites/symbols/BSG & Elvanos - Map Icons Custom Colors Textured/"],
        "kind": "symbols", "size": (260, 200), "radius": 60, "offset_y": 0, "aspect": (0.35, 2.8), "fill": (0.3, 0.97),
        "pack_folder": "Tyrnarra_Settlements", "file": "{item}_{n}",
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
                  ("lograth", "two great buildings facing across one square, a royal palace and a temple crowned with scales, tall towers linked by aerial lines"),
                  ("veidrath", "ancient stone temple core ringed by newer stone districts with an airship mooring tower, circles of tents around it"),
                  ("nahaskel", "jumble of mismatched crooked buildings and impossible twisting towers stacked on top of each other"),
                  ("valreka", "city with a palace and a temple built on the back of a giant whale swimming in the sea, smaller whales carrying houses beside it"),
                  ("frae_city", "city on a great rock floating above a lake, held down by seven huge chains")],
        "per_item": 2,
        "compare": ["user://assets/BSG_elvanos_mapIcons/sprites/symbols/BSG & Elvanos - Map Icons Custom Colors Textured/"],
        "kind": "symbols", "size": (320, 260), "radius": 80, "offset_y": 0, "aspect": (0.35, 1.8), "fill": (0.3, 0.97),
        "pack_folder": "Tyrnarra_God_Cities", "file": "{item}_{n}",
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
