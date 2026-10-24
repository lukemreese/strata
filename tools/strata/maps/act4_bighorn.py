"""Act 4: Bighorn Basin, WY (~56 Ma, PETM).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

Four maps in a ring (geometry: Red Beds north-west, Polecat Bench north-east, Clarks
Fork south-east, Willwood Swamp south-west):

    Red Beds --east--> Polecat Bench --south--> Clarks Fork Crossing
       |                                             |
     south (the land bridge, Coryphodon)           west (a gravel-bar ford, Oxyaena)
       v                                             v
    Willwood Swamp <-------------------------------- +

The Coryphodon boss waits on the land bridge, so it is met whichever way the player
comes: from Red Beds (north end) or from Willwood Swamp (south end).
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_BIGHORN", "BIGHORN BASIN"),
    ("MAPSEC_STRATA_POLECAT", "POLECAT BENCH"),
    ("MAPSEC_STRATA_WILLWOOD", "WILLWOOD SWAMP"),
    ("MAPSEC_STRATA_CLARKS_FORK", "CLARKS FORK"),
]

PETM_TILESETS = ("gTileset_GeneralPetm", "gTileset_FallarborPetm")

# General primary tileset: the wooden signpost (field notes) and the blue route sign
# (the anchor back to the field station). A sign on open ground gets one of these
# metatiles so the player can see there is something to read.
SIGNPOST = 0x01B
ANCHOR_SIGN = 0x003

# General primary tileset: tall grass (land encounters), plain grass, and the pond
# parts of Route 114 (edges, interior, and the ground tile with a shore line).
TALL_GRASS = 0x00D


def signpost(x, y, script, tile=SIGNPOST):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[tile]], collision=1), sign(x, y, script)


def anchor_post(x, y):
    patch, _ = signpost(x, y, "", ANCHOR_SIGN)
    return patch, anchor(x, y)


def pond(x, y, w, n):
    """Two patches that draw a pond with Route 114's own edge tiles: n rows of water
    (the first is the top edge) and a shore row below them, `w` wide."""
    top = [0x180] + [0x189] * (w - 2) + [0x181]
    mid = [0x190] + [0x170] * (w - 2) + [0x192]
    return [dict(at=(x, y), tiles=[top] + [mid] * (n - 1), elevation=1),
            dict(at=(x, y + n), tiles=[[0x2F4] * w], elevation=3)]


def split(*pairs):
    """[(patch, event), ...] -> (patches, events)."""
    return [p for p, _ in pairs], [e for _, e in pairs]


# The map events are assembled by data/map_events.s, which doesn't know
# include/constants/strata_act_flags.h, so map.json names this act's persistent var and
# flag by their stock names (scripts use the VAR_STRATA_ACT4 / FLAG_STRATA_ACT4_* names).
VAR_ACT4 = "VAR_UNUSED_0x40FA"               # VAR_STRATA_ACT4
FLAG_ACT4_OXYAENA = "FLAG_UNUSED_0x27C"      # FLAG_STRATA_ACT4_OXYAENA (FLAG_STRATA_ACT4_BASE + 0)

# Oxyaena's gravel bar across the Clarks Fork (the set piece), see the maps below: it
# stalks the player from either side of the bar while VAR_STRATA_ACT4 is 0.
OXYAENA_TRIGGERS = (
    [trigger(6, y, VAR_ACT4, 0, "StrataClarksFork_EventScript_OxyaenaStalksWest") for y in (8, 9, 10)]    # from Willwood
    + [trigger(12, y, VAR_ACT4, 0, "StrataClarksFork_EventScript_OxyaenaStalksEast") for y in (8, 9, 10)]  # from the bank
)

# ----------------------------------------------------------------------
# Red Beds
# ----------------------------------------------------------------------
_RED_POSTS, _RED_SIGNS = split(
    signpost(29, 10, "StrataRedBeds_EventScript_RedBedsNote"),
    signpost(33, 9, "StrataRedBeds_EventScript_HeatNote"),
    signpost(36, 13, "StrataRedBeds_EventScript_DwarfingNote"),
    signpost(24, 19, "StrataRedBeds_EventScript_LandBridgeNote"),
)

# ----------------------------------------------------------------------
# Polecat Bench: Route 113 (ash flats) east of x=52
# ----------------------------------------------------------------------
_POLECAT_POSTS, _POLECAT_SIGNS = split(
    signpost(20, 10, "StrataPolecatBench_EventScript_ReleaseRateNote"),
    anchor_post(3, 10),
)

# ----------------------------------------------------------------------
# Willwood Swamp: Route 114 basin south of the land bridge
# ----------------------------------------------------------------------
_WILLWOOD_POSTS, _WILLWOOD_SIGNS = split(
    signpost(20, 2, "StrataWillwoodSwamp_EventScript_WallowNote"),
    signpost(16, 9, "StrataWillwoodSwamp_EventScript_LeafDamageNote"),
    signpost(25, 14, "StrataWillwoodSwamp_EventScript_WarmWaterNote"),
    anchor_post(22, 2),
)

# ----------------------------------------------------------------------
# Clarks Fork Crossing: Route 115 river coast
# ----------------------------------------------------------------------
_CLARKS_POSTS, _CLARKS_SIGNS = split(
    signpost(17, 5, "StrataClarksFork_EventScript_BasinNote"),
    signpost(25, 8, "StrataClarksFork_EventScript_GastornisNote"),
    anchor_post(19, 3),
)

MAPS = [
    # ------------------------------------------------------------------
    # Act 4: Bighorn Basin, WY (~56 Ma): PETM hothouse, red floodplain soils
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_RED_BEDS", name="StrataRedBeds", era="ERA_BIGHORN_PETM",
        habitat="open", light="day",
        forage=[forage(16, 12, "PALM_FRUIT"), forage(24, 6, "BROWSE"), forage(36, 10, "LARVAE"),
                forage(27, 16, "FERN_FROND"), forage(37, 6, "LEGUME_POD")],
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 0, 40, 34), tilesets=PETM_TILESETS),
        patches=[
            dict(rect=(26, 0, 7, 6), like=(32, 9)),     # house -> ground
            dict(rect=(32, 5, 8, 9), like=(31, 10)),    # farm plots -> ground
            dict(rect=(19, 20, 4, 14), like=(26, 19)),  # wooden bridge -> natural land bridge
            dict(rect=(24, 33, 9, 1), like=(26, 19)),   # roof at the bottom edge -> ground
            dict(rect=(32, 14, 8, 1), metatile=0x279, elevation=3),   # bottom edge of the farm
            dict(rect=(24, 7, 4, 3), metatile=0x279, elevation=3),    # square ponds -> ground
            dict(rect=(17, 13, 3, 3), metatile=0x279, elevation=3),
            dict(rect=(23, 14, 5, 5), metatile=0x279, elevation=3),
            dict(rect=(9, 25, 6, 5), metatile=0x170, elevation=1),    # garden island -> lake
        ] + _RED_POSTS,
        swap={0x2F4: 0x279},   # the ground with a pond's edge line, also the striped 'bridge'
        music="MUS_ROUTE110", weather="WEATHER_DROUGHT", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_BIGHORN",
        arrival=(31, 8),
        connections=[connection("right", "MAP_STRATA_POLECAT_BENCH"), connection("down", "MAP_STRATA_WILLWOOD_SWAMP")],
        bgs=[anchor(31, 7)] + _RED_SIGNS,
        coords=boss_triggers("ERA_BIGHORN_PETM", "StrataRedBeds_EventScript_Coryphodon", [(x, 26) for x in range(19, 23)]),
        encounters=dict(
            land_mons=mons(("SIFRHIPPUS", 20, 22), ("HYOPSODUS", 20, 22), ("DIACODEXIS", 21, 23), ("PARAMYS", 21, 24),
                           ("TEILHARDINA", 23, 26), ("SIFRHIPPUS", 22, 25), ("HYOPSODUS", 23, 25), ("PROTOCHELYD", 23, 25),
                           ("GASTORNIS", 24, 26), ("MESODMA", 24, 27), ("CORYPHODON", 25, 27), ("GASTORNIS", 26, 27)),
            water_mons=mons(("LEPISOSTEUS", 22, 26), ("CHAMPSOSAUR", 22, 26), ("LEPISOSTEUS", 23, 27),
                            ("BOREALOSUCH", 24, 27), ("CORYPHODON", 25, 27)),
            fishing_mons=mons(("LEPISOSTEUS", 19, 22), ("LEPISOSTEUS", 19, 22), ("LEPISOSTEUS", 20, 23), ("CHAMPSOSAUR", 20, 23),
                              ("LEPISOSTEUS", 21, 24), ("CHAMPSOSAUR", 21, 24), ("PROTOCHELYD", 22, 25), ("CHAMPSOSAUR", 22, 25),
                              ("BOREALOSUCH", 23, 26), ("BOREALOSUCH", 24, 27)),
        ),
    ),
    # Polecat Bench: the real PETM section is on the bench east of the Clarks Fork
    # (Polecat Bench, Clarks Fork Basin). Open, dry badlands flats.
    dict(
        id="MAP_STRATA_POLECAT_BENCH", name="StrataPolecatBench", era="ERA_BIGHORN_PETM",
        habitat="open", light="day",
        forage=[forage(10, 5, "BROWSE"), forage(22, 8, "LEGUME_POD"), forage(40, 9, "FERN_FROND"),
                forage(31, 5, "LARVAE"), forage(2, 3, "BROWSE")],
        crop=dict(**{"from": "LAYOUT_ROUTE113"}, rect=(52, 0, 48, 18), tilesets=PETM_TILESETS),
        patches=[
            dict(rect=(11, 14, 3, 4), like=(62, 11)),   # a trail through the trees to the river
        ] + _POLECAT_POSTS,
        music="MUS_ROUTE110", weather="WEATHER_DROUGHT", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_POLECAT",
        connections=[connection("left", "MAP_STRATA_RED_BEDS"), connection("down", "MAP_STRATA_CLARKS_FORK", -6)],
        bgs=[sign(6, 4, "StrataPolecatBench_EventScript_CarbonNote"),
             sign(33, 7, "StrataPolecatBench_EventScript_ImmigrantsNote")] + _POLECAT_SIGNS,
        encounters=dict(
            land_mons=mons(("PARAMYS", 21, 23), ("SIFRHIPPUS", 21, 23), ("DIACODEXIS", 22, 24), ("PARAMYS", 22, 25),
                           ("HYOPSODUS", 22, 24), ("SIFRHIPPUS", 23, 26), ("DIACODEXIS", 24, 26), ("TEILHARDINA", 23, 27),
                           ("PARAMYS", 24, 26), ("GASTORNIS", 25, 27), ("DIACODEXIS", 25, 27), ("SIFRHIPPUS", 26, 27)),
        ),
    ),
    dict(
        id="MAP_STRATA_WILLWOOD_SWAMP", name="StrataWillwoodSwamp", era="ERA_BIGHORN_PETM",
        habitat="water", light="day",
        forage=[forage(18, 1, "LARVAE"), forage(23, 8, "FERN_FROND"), forage(17, 12, "PALM_FRUIT"),
                forage(22, 17, "LARVAE"), forage(20, 21, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 34, 40, 30), tilesets=PETM_TILESETS),
        patches=[
            dict(rect=(25, 0, 6, 4), like=(14, 35)),    # house -> grass
            dict(rect=(29, 4, 11, 3), like=(14, 35)),   # a cut through the east mesa, to the Clarks Fork
        ] + pond(15, 3, 5, 3) + pond(14, 16, 5, 2) + _WILLWOOD_POSTS,
        music="MUS_ROUTE110", weather="WEATHER_DROUGHT", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_WILLWOOD",
        connections=[connection("up", "MAP_STRATA_RED_BEDS"), connection("right", "MAP_STRATA_CLARKS_FORK", -4)],
        bgs=_WILLWOOD_SIGNS,
        encounters=dict(
            land_mons=mons(("CHAMPSOSAUR", 22, 24), ("PROTOCHELYD", 22, 24), ("HYOPSODUS", 23, 25), ("BOREALOSUCH", 23, 25),
                           ("DIACODEXIS", 23, 25), ("PARAMYS", 24, 26), ("CORYPHODON", 24, 26), ("TEILHARDINA", 24, 27),
                           ("BOREALOSUCH", 25, 27), ("OXYAENA", 23, 26), ("CORYPHODON", 26, 27), ("GASTORNIS", 26, 27)),
            water_mons=mons(("LEPISOSTEUS", 22, 26), ("CHAMPSOSAUR", 22, 26), ("LEPISOSTEUS", 23, 27),
                            ("BOREALOSUCH", 24, 27), ("CORYPHODON", 25, 27)),
            fishing_mons=mons(("LEPISOSTEUS", 19, 22), ("LEPISOSTEUS", 19, 22), ("LEPISOSTEUS", 20, 23), ("CHAMPSOSAUR", 20, 23),
                              ("LEPISOSTEUS", 21, 24), ("CHAMPSOSAUR", 21, 24), ("PROTOCHELYD", 22, 25), ("CHAMPSOSAUR", 22, 25),
                              ("BOREALOSUCH", 23, 26), ("BOREALOSUCH", 24, 27)),
        ),
    ),
    dict(
        id="MAP_STRATA_CLARKS_FORK", name="StrataClarksFork", era="ERA_BIGHORN_PETM",
        habitat="forest", light="day",
        forage=[forage(14, 6, "CARRION"), forage(30, 12, "FERN_FROND"), forage(24, 20, "LEGUME_POD"),
                forage(25, 15, "LARVAE")],
        crop=dict(**{"from": "LAYOUT_ROUTE115"}, rect=(0, 44, 40, 30), tilesets=PETM_TILESETS),
        patches=[
            dict(rect=(0, 8, 14, 3), like=(8, 66)),     # the gravel bar across the river
            dict(rect=(21, 0, 1, 4), like=(19, 49)),    # fences -> ground
            dict(rect=(21, 4, 3, 1), like=(19, 49)),
            dict(rect=(23, 5, 2, 1), like=(19, 49)),
            dict(rect=(29, 5, 3, 1), like=(19, 49)),
            dict(rect=(12, 18, 8, 6), metatile=TALL_GRASS),   # tall grass for the land encounters
            dict(rect=(24, 26, 7, 3), metatile=TALL_GRASS),
        ] + _CLARKS_POSTS,
        music="MUS_ROUTE110", weather="WEATHER_DROUGHT", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_CLARKS_FORK",
        connections=[connection("up", "MAP_STRATA_POLECAT_BENCH", 6), connection("left", "MAP_STRATA_WILLWOOD_SWAMP", 4)],
        objects=[
            obj("LOCALID_STRATA_CLARKS_OXYAENA", "OBJ_EVENT_GFX_SPECIES(OXYAENA)", 9, 9,
                "StrataClarksFork_EventScript_Oxyaena", movement="MOVEMENT_TYPE_FACE_LEFT",
                flag=FLAG_ACT4_OXYAENA),
        ],
        coords=OXYAENA_TRIGGERS,
        bgs=_CLARKS_SIGNS,
        encounters=dict(
            land_mons=mons(("GASTORNIS", 22, 24), ("SIFRHIPPUS", 22, 24), ("DIACODEXIS", 23, 25), ("HYOPSODUS", 23, 25),
                           ("PARAMYS", 23, 25), ("GASTORNIS", 24, 26), ("PROTOCHELYD", 24, 26), ("TEILHARDINA", 24, 27),
                           ("BOREALOSUCH", 25, 27), ("SIFRHIPPUS", 25, 27), ("CORYPHODON", 26, 27), ("GASTORNIS", 26, 27)),
            water_mons=mons(("LEPISOSTEUS", 22, 26), ("CHAMPSOSAUR", 22, 26), ("LEPISOSTEUS", 23, 27),
                            ("PROTOCHELYD", 24, 27), ("BOREALOSUCH", 25, 27)),
            fishing_mons=mons(("LEPISOSTEUS", 19, 22), ("LEPISOSTEUS", 19, 22), ("LEPISOSTEUS", 20, 23), ("CHAMPSOSAUR", 20, 23),
                              ("LEPISOSTEUS", 21, 24), ("CHAMPSOSAUR", 21, 24), ("PROTOCHELYD", 22, 25), ("CHAMPSOSAUR", 22, 25),
                              ("BOREALOSUCH", 23, 26), ("BOREALOSUCH", 24, 27)),
        ),
    ),
]
