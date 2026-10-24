"""Act 7: Ashfall, NE (~11.9 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The act opens BEFORE the ash. Four places, each built twice from one footprint (a
spec below, turned into a map by build()): the clear version (Oligocene palettes, a
distant haze, WEATHER_SHADE) and its ash version (the stock Fallarbor ash tiles and
WEATHER_VOLCANIC_ASH). The boss at the Waterhole starts the ashfall, and winning it
warps the player into the ash version of the Waterhole. The ash maps connect to each
other only, and have no new species: survivors at higher levels.

        Niobrara River
              |
    Grassland (arrival from camp) ---- Waterhole (boss)
              |
        Savanna Woodland

    each also as <Name> Ash (MAP_STRATA_*_ASH)
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_ASHFALL", "ASHFALL"),
    ("MAPSEC_STRATA_SAVANNA", "SAVANNA WOODLAND"),
    ("MAPSEC_STRATA_NIOBRARA", "NIOBRARA RIVER"),
    ("MAPSEC_STRATA_WATERHOLE", "THE WATERHOLE"),
    ("MAPSEC_STRATA_ASHFALL_ASH", "ASHFALL (ASH)"),
]

# General primary tileset: the wooden signpost (a field note on open ground).
SIGNPOST = 0x01B
TREE = 0x26E            # Fallarbor: a round tree (blocked)
CLEAR_TILESETS = ("gTileset_GeneralOligocene", "gTileset_FallarborOligocene")

# Map events are assembled without include/constants/strata.h, so they name the act flags by
# their stock FLAG_UNUSED_0x... / VAR_UNUSED_0x... names: FLAG_UNUSED_0x294 is
# FLAG_STRATA_A7_EPICYON_GONE, VAR_UNUSED_0x40FD is VAR_STRATA_ACT7 (1 once the haze has been
# seen; include/constants/strata_act_flags.h).

R113 = "LAYOUT_ROUTE113"
R114 = "LAYOUT_ROUTE114"
# Route 113's ground and grass are ash tiles; the clear version swaps them for plain grass.
ASH_TO_GRASS = {0x20A: 0x00D, 0x218: 0x001}
# Route 114's grass is plain; the ash version swaps in the ash tiles.
GRASS_TO_ASH = {0x00D: 0x20A, 0x001: 0x218, 0x002: 0x218}

# Water in General (as in the ponds of Route 114): top edge, middle rows, shore row.
WATER_TOP = (0x180, 0x189, 0x181)
WATER_MID = (0x190, 0x170, 0x192)
WATER_SHORE = 0x2F4


def pond(x, y, w, h):
    """Patches for a pond with its top-left corner at (x, y): w wide, h tall counting the
    top edge row and the walkable shore row beneath."""
    top = [WATER_TOP[0]] + [WATER_TOP[1]] * (w - 2) + [WATER_TOP[2]]
    mid = [WATER_MID[0]] + [WATER_MID[1]] * (w - 2) + [WATER_MID[2]]
    return [
        dict(at=(x, y), tiles=[top], collision=0, elevation=1),
        dict(at=(x, y + 1), tiles=[mid] * (h - 2), collision=0, elevation=1),
        dict(at=(x, y + h - 1), tiles=[[WATER_SHORE] * w], collision=0, elevation=3),
    ]


def signpost(x, y):
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1)


def trees(*spots):
    return [dict(rect=(x, y, 1, 1), metatile=TREE, collision=1, elevation=0) for x, y in spots]


def build(spec, ash):
    """One map of a pair, from its spec: shared `patches`, `notes` [(x, y, clear script,
    ash script)], the `anchor` post, and per-version `clear`/`ash` dicts."""
    m = dict(spec)
    version = dict(m.pop("ash") if ash else m.pop("clear"))
    m.pop("clear", None)
    m.pop("ash", None)
    notes = m.pop("notes")
    anchor_at = m.pop("anchor")
    links = m.pop("links")
    swap = m.pop("swap_ash") if ash else m.pop("swap_clear")
    m.pop("swap_ash", None)
    m.pop("swap_clear", None)
    key = m.pop("key")
    m["id"] = f"MAP_STRATA_{key}" + ("_ASH" if ash else "")
    m["name"] = "Strata" + spec["name"] + ("Ash" if ash else "")
    m["era"] = "ERA_ASHFALL"
    m["swap"] = swap
    m["crop"] = dict(m["crop"])
    if ash:
        m["crop"].pop("tilesets")
    shown = [(x, y, ash_script if ash else clear_script) for x, y, clear_script, ash_script in notes]
    shown = [(x, y, s) for x, y, s in shown if s]
    m["patches"] = list(m.get("patches", [])) + [signpost(x, y) for x, y, _ in shown] + [signpost(*anchor_at)]
    m["bgs"] = [sign(x, y, s) for x, y, s in shown] + [anchor(*anchor_at)] + version.pop("bgs", [])
    m["connections"] = [connection(d, f"MAP_STRATA_{k}" + ("_ASH" if ash else ""), off) for d, k, off in links]
    m.update(version)
    m.pop("name_suffix", None)
    return m


def pair(spec):
    return [build(spec, False), build(spec, True)]


# ----------------------------------------------------------------------
# Grassland: where the rig arrives. Open grass, the haze on the horizon.
# ----------------------------------------------------------------------
GRASSLAND = dict(
    key="GRASSLAND", name="Grassland",
    habitat="open",
    crop=dict(**{"from": R113}, rect=(15, 0, 55, 20), tilesets=CLEAR_TILESETS),
    swap_clear=ASH_TO_GRASS, swap_ash=GRASS_TO_ASH,
    patches=[
        dict(rect=(16, 1, 6, 5), like=(37, 6)),     # house -> plain
        dict(rect=(19, 0, 8, 2), like=(37, 6)),     # the way north, to the river (tall grass)
        dict(rect=(33, 15, 10, 5), like=(37, 6)),   # the way south, to the savanna
    ],
    notes=[
        (4, 10, "StrataGrassland_EventScript_NoteTeeth", "StrataGrassland_EventScript_NoteAshDepth"),
        (36, 11, "StrataGrassland_EventScript_NoteSeeds", None),
        (23, 8, None, "StrataGrassland_EventScript_NoteOrder"),
        (50, 12, "StrataGrassland_EventScript_NoteCranes", None),
    ],
    anchor=(5, 12),
    links=[("right", "WATERHOLE", 0), ("up", "NIOBRARA", 10), ("down", "SAVANNA", 29)],
    music="MUS_ROUTE113", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_ASHFALL",
    clear=dict(
        light="day", weather="WEATHER_SHADE", music="MUS_ROUTE104",
        forage=[forage(20, 3, "SEED_HEAD"), forage(45, 6, "BROWSE"), forage(11, 13, "SEED_HEAD"), forage(48, 13, "LARVAE")],
        arrival=(5, 11),
        coords=[trigger(7, y, "VAR_UNUSED_0x40FD", 0, "StrataGrassland_EventScript_Haze") for y in range(10, 15)],
        encounters=dict(
            land_mons=mons(("PROTOHIPPUS", 40, 42), ("CORMOHIPPARI", 38, 40), ("PROCAMELUS", 40, 42), ("CORMOHIPPARI", 40, 42),
                           ("LEPTOCYON", 40, 42), ("COSORYX", 38, 40), ("BALEARICA", 41, 43), ("COSORYX", 40, 42),
                           ("PROCAMELUS", 41, 43), ("CORMOHIPPARI", 41, 43), ("ANCHIGYPS", 42, 44), ("EPICYON", 43, 45)),
        ),
    ),
    ash=dict(
        light="ash", weather="WEATHER_VOLCANIC_ASH",
        forage=[forage(45, 6, "CARRION"), forage(11, 13, "CARRION"), forage(48, 13, "CARRION")],
        encounters=dict(
            land_mons=mons(("ANCHIGYPS", 43, 45), ("LEPTOCYON", 43, 45), ("TELEOCERAS", 43, 45), ("ANCHIGYPS", 43, 45),
                           ("EPICYON", 44, 46), ("APHELOPS", 43, 45), ("LEPTOCYON", 44, 46), ("TELEOCERAS", 44, 46),
                           ("ANCHIGYPS", 44, 46), ("EPICYON", 44, 46), ("APHELOPS", 44, 46), ("TELEOCERAS", 45, 46)),
        ),
    ),
)

# ----------------------------------------------------------------------
# The Waterhole: east of the Grassland (Route 113's east end). The boss arena.
# ----------------------------------------------------------------------
_WATERHOLE_POND = (17, 13, 11, 5)
WATERHOLE = dict(
    key="WATERHOLE", name="Waterhole",
    habitat="water",
    crop=dict(**{"from": R113}, rect=(70, 0, 30, 20), tilesets=CLEAR_TILESETS),
    swap_clear=ASH_TO_GRASS, swap_ash=GRASS_TO_ASH,
    patches=[dict(rect=(14, 11, 16, 9), like=(32, 8))] + pond(*_WATERHOLE_POND),   # the south plateau -> plain, with the pond
    notes=[
        (18, 9, "StrataWaterhole_EventScript_NoteWaterhole", None),
        (22, 10, None, "StrataWaterhole_EventScript_NoteBarn"),
        (19, 7, None, "StrataWaterhole_EventScript_NoteGlass"),
    ],
    anchor=(2, 12),
    links=[("left", "GRASSLAND", 0)],
    music="MUS_ROUTE113", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_WATERHOLE",
    clear=dict(
        light="day", weather="WEATHER_SHADE", music="MUS_ROUTE104",
        forage=[forage(26, 11, "SEED_HEAD"), forage(16, 18, "CARRION"), forage(28, 18, "BROWSE")],
        coords=boss_triggers("ERA_ASHFALL", "StrataWaterhole_EventScript_Teleoceras", [(16, y) for y in range(7, 20)]),
        objects=[
            # The bull and the cow at the water: talking to either starts the boss battle.
            obj("LOCALID_STRATA_WATERHOLE_BULL", "OBJ_EVENT_GFX_SPECIES(TELEOCERAS)", 22, 12,
                "StrataWaterhole_EventScript_Teleoceras", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_WATERHOLE_COW", "OBJ_EVENT_GFX_SPECIES(TELEOCERAS)", 24, 12,
                "StrataWaterhole_EventScript_Teleoceras", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_WATERHOLE_HERD_A", "OBJ_EVENT_GFX_SPECIES(TELEOCERAS)", 20, 18,
                "StrataWaterhole_EventScript_Herd", "MOVEMENT_TYPE_FACE_UP"),
            obj("LOCALID_STRATA_WATERHOLE_HERD_B", "OBJ_EVENT_GFX_SPECIES(TELEOCERAS)", 26, 18,
                "StrataWaterhole_EventScript_Herd", "MOVEMENT_TYPE_FACE_LEFT"),
            obj("LOCALID_STRATA_WATERHOLE_CAMEL", "OBJ_EVENT_GFX_SPECIES(PROCAMELUS)", 19, 11,
                "StrataWaterhole_EventScript_Camel", "MOVEMENT_TYPE_FACE_DOWN"),
        ],
        encounters=dict(
            land_mons=mons(("PROTOHIPPUS", 41, 43), ("PROCAMELUS", 41, 43), ("TELEOCERAS", 42, 44), ("CORMOHIPPARI", 41, 43),
                           ("BALEARICA", 41, 43), ("TELEOCERAS", 43, 45), ("PROCAMELUS", 42, 44), ("ANCHIGYPS", 42, 44),
                           ("COSORYX", 41, 43), ("CHELYDRA", 42, 44), ("TELEOCERAS", 42, 44), ("APHELOPS", 43, 45)),
            water_mons=mons(("CHELYDRA", 39, 42), ("LEPISOSTEUS", 38, 42), ("MACROCHELYS", 38, 41),
                            ("CHELYDRA", 40, 43), ("MACROCHELYS", 40, 42)),
            fishing_mons=mons(("LEPISOSTEUS", 38, 40), ("LEPISOSTEUS", 38, 40), ("LEPISOSTEUS", 39, 41), ("CHELYDRA", 39, 41),
                              ("LEPISOSTEUS", 39, 41), ("MACROCHELYS", 39, 41), ("CHELYDRA", 40, 42), ("MACROCHELYS", 40, 42),
                              ("CHELYDRA", 41, 43), ("MACROCHELYS", 41, 42)),
        ),
    ),
    ash=dict(
        light="ash", weather="WEATHER_VOLCANIC_ASH",
        arrival=(15, 9),
        forage=[forage(26, 11, "CARRION"), forage(16, 18, "CARRION")],
        objects=[
            # The skeletons-to-be: the herd, still standing at the water.
            obj("LOCALID_STRATA_WATERHOLE_ASH_A", "OBJ_EVENT_GFX_SPECIES(TELEOCERAS)", 21, 12,
                "StrataWaterhole_EventScript_AshRhino", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_WATERHOLE_ASH_B", "OBJ_EVENT_GFX_SPECIES(TELEOCERAS)", 25, 12,
                "StrataWaterhole_EventScript_AshRhino", "MOVEMENT_TYPE_FACE_DOWN"),
        ],
        encounters=dict(
            land_mons=mons(("TELEOCERAS", 43, 45), ("ANCHIGYPS", 43, 45), ("TELEOCERAS", 44, 46), ("EPICYON", 44, 46),
                           ("APHELOPS", 43, 45), ("ANCHIGYPS", 44, 46), ("TELEOCERAS", 44, 46), ("CHELYDRA", 43, 45),
                           ("TELEOCERAS", 45, 46), ("EPICYON", 45, 46), ("APHELOPS", 44, 46), ("TELEOCERAS", 45, 46)),
            water_mons=mons(("CHELYDRA", 41, 44), ("MACROCHELYS", 41, 44), ("CHELYDRA", 42, 45),
                            ("MACROCHELYS", 42, 45), ("MACROCHELYS", 43, 45)),
            fishing_mons=mons(("CHELYDRA", 41, 43), ("CHELYDRA", 41, 43), ("MACROCHELYS", 41, 43), ("MACROCHELYS", 42, 44),
                              ("CHELYDRA", 42, 44), ("MACROCHELYS", 42, 44), ("CHELYDRA", 43, 45), ("MACROCHELYS", 43, 45),
                              ("CHELYDRA", 43, 45), ("MACROCHELYS", 44, 45)),
        ),
    ),
)

# ----------------------------------------------------------------------
# Savanna Woodland: south of the Grassland, the meadow of Route 114 with trees added.
# ----------------------------------------------------------------------
SAVANNA = dict(
    key="SAVANNA", name="Savanna",
    habitat="forest",
    crop=dict(**{"from": R114}, rect=(6, 34, 28, 28), tilesets=CLEAR_TILESETS),
    swap_clear={}, swap_ash=GRASS_TO_ASH,
    patches=[
        dict(rect=(19, 0, 6, 3), like=(15, 35)),        # house -> meadow
        dict(rect=(24, 8, 3, 5), like=(15, 35)),        # the berry-soil plot -> meadow
    ] + trees((10, 5), (13, 3), (17, 4), (10, 8), (19, 6), (18, 10), (13, 14), (18, 14), (9, 19), (12, 22), (16, 25), (12, 25)),
    notes=[
        (10, 1, "StrataSavanna_EventScript_NoteBrowsers", None),
        (13, 13, "StrataSavanna_EventScript_NoteDogs", None),
        (16, 13, None, "StrataSavanna_EventScript_NoteScavengers"),
    ],
    anchor=(7, 1),
    links=[("up", "GRASSLAND", -29)],
    music="MUS_ROUTE113", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_SAVANNA",
    clear=dict(
        light="day", weather="WEATHER_SHADE", music="MUS_ROUTE104",
        forage=[forage(12, 11, "BROWSE"), forage(16, 19, "BROWSE"), forage(18, 13, "LARVAE"), forage(9, 20, "SEED_HEAD")],
        objects=[
            # The Epicyon mini-boss (Lv 44), once: a bone-cracking dog at a carcass.
            obj("LOCALID_STRATA_SAVANNA_EPICYON", "OBJ_EVENT_GFX_SPECIES(EPICYON)", 15, 14,
                "StrataSavanna_EventScript_Epicyon", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_UNUSED_0x294"),
        ],
        encounters=dict(
            land_mons=mons(("HYPOHIPPUS", 39, 41), ("PROCAMELUS", 40, 42), ("LEPTOCYON", 40, 42), ("HYPOHIPPUS", 40, 42),
                           ("COSORYX", 38, 40), ("ANCHIGYPS", 41, 43), ("PROCAMELUS", 41, 43), ("HYPOHIPPUS", 41, 43),
                           ("COSORYX", 40, 42), ("BALEARICA", 41, 43), ("PROTOHIPPUS", 41, 43), ("ANCHIGYPS", 42, 44)),
        ),
    ),
    ash=dict(
        light="ash", weather="WEATHER_VOLCANIC_ASH",
        forage=[forage(12, 11, "CARRION"), forage(18, 13, "CARRION"), forage(16, 19, "CARRION")],
        encounters=dict(
            land_mons=mons(("ANCHIGYPS", 43, 45), ("LEPTOCYON", 43, 45), ("EPICYON", 44, 46), ("APHELOPS", 43, 45),
                           ("LEPTOCYON", 44, 46), ("ANCHIGYPS", 43, 45), ("TELEOCERAS", 44, 46), ("EPICYON", 44, 46),
                           ("ANCHIGYPS", 44, 46), ("LEPTOCYON", 44, 46), ("APHELOPS", 44, 46), ("TELEOCERAS", 45, 46)),
        ),
    ),
)

# ----------------------------------------------------------------------
# Niobrara River: north of the Grassland, the lake and river of Route 114.
# ----------------------------------------------------------------------
NIOBRARA = dict(
    key="NIOBRARA", name="Niobrara",
    habitat="water",
    crop=dict(**{"from": R114}, rect=(0, 4, 32, 32), tilesets=CLEAR_TILESETS),
    swap_clear={}, swap_ash=GRASS_TO_ASH,
    patches=[
        # The wooden bridge becomes a gravel bar across the river.
        dict(rect=(18, 17, 1, 13), metatile=0x192, collision=0, elevation=1),
        dict(rect=(23, 17, 1, 13), metatile=0x190, collision=0, elevation=1),
        dict(rect=(19, 17, 4, 13), metatile=0x279, collision=0, elevation=3),
        dict(rect=(26, 0, 6, 3), metatile=0x279, collision=0, elevation=3),    # the house at the edge
        dict(rect=(25, 30, 6, 2), like=(15, 35)),                              # the house at the south shore
        # Tall grass on the banks and the bar.
        dict(rect=(24, 5, 4, 3), metatile=0x00D, collision=0, elevation=3),
        dict(rect=(10, 29, 6, 2), metatile=0x00D, collision=0, elevation=3),
        dict(rect=(19, 21, 4, 3), metatile=0x00D, collision=0, elevation=3),
        # The waterfall becomes a run of rapids (plain water).
        dict(rect=(9, 6, 4, 4), metatile=0x170, collision=0, elevation=1),
    ],
    notes=[
        (21, 12, "StrataNiobrara_EventScript_NoteRiver", None),
        (9, 29, "StrataNiobrara_EventScript_NoteTurtles", None),
        (22, 15, None, "StrataNiobrara_EventScript_NoteSilt"),
        (29, 8, "StrataNiobrara_EventScript_NoteRhinos", None),
    ],
    anchor=(14, 30),
    links=[("down", "GRASSLAND", -10)],
    music="MUS_ROUTE113", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_NIOBRARA",
    clear=dict(
        light="day", weather="WEATHER_SHADE", music="MUS_ROUTE104",
        forage=[forage(28, 3, "SEED_HEAD"), forage(28, 14, "LARVAE"), forage(11, 29, "BROWSE"), forage(20, 6, "CARRION")],
        encounters=dict(
            land_mons=mons(("CHELYDRA", 40, 42), ("BALEARICA", 40, 42), ("APHELOPS", 40, 42), ("PROCAMELUS", 40, 42),
                           ("CHELYDRA", 41, 43), ("APHELOPS", 41, 43), ("BALEARICA", 41, 43), ("TELEOCERAS", 42, 44),
                           ("APHELOPS", 42, 44), ("CHELYDRA", 42, 44), ("TELEOCERAS", 43, 45), ("APHELOPS", 43, 44)),
            water_mons=mons(("LEPISOSTEUS", 38, 42), ("MACROCHELYS", 38, 40), ("CHELYDRA", 39, 42),
                            ("MACROCHELYS", 40, 42), ("LEPISOSTEUS", 40, 43)),
            fishing_mons=mons(("LEPISOSTEUS", 38, 40), ("LEPISOSTEUS", 38, 40), ("LEPISOSTEUS", 39, 41), ("CHELYDRA", 39, 41),
                              ("LEPISOSTEUS", 39, 41), ("MACROCHELYS", 39, 41), ("CHELYDRA", 40, 42), ("MACROCHELYS", 40, 42),
                              ("MACROCHELYS", 41, 42), ("MACROCHELYS", 41, 42)),
        ),
    ),
    ash=dict(
        light="ash", weather="WEATHER_VOLCANIC_ASH",
        forage=[forage(28, 14, "CARRION"), forage(20, 6, "CARRION"), forage(11, 29, "CARRION")],
        encounters=dict(
            land_mons=mons(("CHELYDRA", 43, 45), ("ANCHIGYPS", 43, 45), ("APHELOPS", 43, 45), ("CHELYDRA", 43, 45),
                           ("TELEOCERAS", 43, 45), ("APHELOPS", 44, 46), ("ANCHIGYPS", 44, 46), ("TELEOCERAS", 44, 46),
                           ("CHELYDRA", 44, 46), ("APHELOPS", 44, 46), ("TELEOCERAS", 45, 46), ("EPICYON", 44, 46)),
            water_mons=mons(("LEPISOSTEUS", 41, 44), ("MACROCHELYS", 41, 44), ("CHELYDRA", 42, 45),
                            ("MACROCHELYS", 42, 45), ("MACROCHELYS", 43, 45)),
            fishing_mons=mons(("LEPISOSTEUS", 41, 43), ("LEPISOSTEUS", 41, 43), ("MACROCHELYS", 41, 43), ("CHELYDRA", 42, 44),
                              ("LEPISOSTEUS", 42, 44), ("MACROCHELYS", 42, 44), ("CHELYDRA", 43, 45), ("MACROCHELYS", 43, 45),
                              ("MACROCHELYS", 44, 45), ("CHELYDRA", 44, 45)),
        ),
    ),
)

MAPS = [m for spec in (GRASSLAND, NIOBRARA, SAVANNA, WATERHOLE) for m in pair(spec)]
