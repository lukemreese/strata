"""Act 5: Green River lakes and Bridger Basin, WY (~52-46 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

Four maps, one per habitat of the plan (docs/strata_outline.md section 2.6):

    Bridger Shore (StrataLakeForest)  the arrival; Route 104 whole. The boss line is on its
                                      south beach. North edge -> Fossil Lake, east gap -> Bridger Forest.
    Fossil Lake                       Route 103 (lake and shore): the Lagerstaette, mass-mortality scene.
    Bridger Forest                    Route 116 west half, lightly planted: canopy primates, rodents.
    Oil-Shale Cliffs                  Route 115's canyon below the ridge: varves, the Patriofelis set piece.

                 Fossil Lake
                     | (down / up)
    arrival -> Bridger Shore --(east gap)-- Bridger Forest -- Oil-Shale Cliffs
                     |
                (boss line, y = 61)
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_BRIDGER_SHORE", "BRIDGER SHORE"),
    ("MAPSEC_STRATA_FOSSIL_LAKE", "FOSSIL LAKE"),
    ("MAPSEC_STRATA_BRIDGER_FOREST", "BRIDGER FOREST"),
    ("MAPSEC_STRATA_OIL_SHALE", "OIL-SHALE CLIFFS"),
]

# Object flags. data/map_events.s doesn't see constants/strata.h, so map.json needs the numbers:
# these are FLAG_STRATA_A5_BULL_HIDDEN and FLAG_STRATA_A5_PATRIOFELIS in
# include/constants/strata_act_flags.h (FLAG_STRATA_ACT5_BASE = 0x284, + 0 and + 1).
BULL_FLAG = "0x284"
PATRIOFELIS_FLAG = "0x285"
ACT5_VAR = "0x40FB"   # VAR_STRATA_ACT5 (VAR_UNUSED_0x40FB in vars.h)

# General primary tileset: the wooden signpost. A field note on open ground gets this
# metatile so the player can see there is something to read (same as act 0).
SIGNPOST = 0x01B


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1, elevation=3), sign(x, y, script, facing)


def tree(x, y):
    """A big 2x2 tree (General tileset), top-left at (x, y)."""
    return dict(at=(x, y), tiles=[[0x1D4, 0x1D5], [0x1DC, 0x1DD]], collision=1, elevation=3)


# --- signposts -----------------------------------------------------------------------
_shore_signs = [
    signpost(7, 19, "StrataLakeForest_EventScript_NoteLake"),
    signpost(26, 4, "StrataLakeForest_EventScript_NoteClimate"),
    signpost(20, 23, "StrataLakeForest_EventScript_NoteShallows"),
    signpost(16, 57, "StrataLakeForest_EventScript_NoteUintatheres"),
]
_fossil_signs = [
    signpost(19, 8, "StrataFossilLake_EventScript_NoteFish"),
    signpost(9, 3, "StrataFossilLake_EventScript_NoteBats"),
    signpost(6, 14, "StrataFossilLake_EventScript_NoteBirds"),
]
_forest_signs = [
    signpost(5, 8, "StrataBridgerForest_EventScript_NotePrimates"),
    signpost(33, 10, "StrataBridgerForest_EventScript_NoteFlora"),
    signpost(18, 15, "StrataBridgerForest_EventScript_NoteRodents"),
]
_shale_signs = [
    signpost(10, 14, "StrataOilShale_EventScript_NoteVarves"),
    signpost(14, 31, "StrataOilShale_EventScript_NoteKerogen"),
    signpost(17, 20, "StrataOilShale_EventScript_NoteCreodonts"),
]

# The Bridger Forest is a meadow in the source; plant some canopy (top-left corners).
_forest_trees = [(7, 4), (11, 4), (14, 5), (18, 13), (20, 16), (24, 17), (34, 13), (37, 15), (36, 3), (37, 6)]

MAPS = [
    # ------------------------------------------------------------------
    # Act 5: Green River lakes and Bridger Basin, WY (~52-46 Ma): subtropical lake and forest
    # ------------------------------------------------------------------
    dict(
        # Bridger Shore: the arrival, and the boss on the south beach. (The id keeps its old
        # name: the rig's warp and the tests refer to MAP_STRATA_LAKE_FOREST.)
        id="MAP_STRATA_LAKE_FOREST", name="StrataLakeForest", era="ERA_GREEN_RIVER",
        habitat="forest", light="day",
        forage=[forage(3, 21, "PALM_FRUIT"), forage(30, 24, "LARVAE"), forage(20, 44, "LEGUME_POD"),
                forage(24, 5, "FERN_FROND"), forage(9, 26, "BROWSE"), forage(16, 59, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE104"}, rect=(0, 0, 40, 80)),
        patches=[
            dict(rect=(3, 14, 7, 5), like=(5, 21)),     # house -> grass
            dict(rect=(24, 9, 2, 8), like=(22, 12)),    # piers -> lake
            dict(rect=(26, 15, 6, 2), like=(22, 12)),
            dict(rect=(30, 17, 2, 5), like=(22, 12)),
            dict(rect=(10, 31, 2, 7), like=(10, 29)),   # path through the forest band
            dict(rect=(14, 46, 6, 5), metatile=0x001, elevation=3),   # cottage -> grass
            dict(rect=(11, 51, 5, 2), like=(9, 52)),    # dock -> lake
            dict(rect=(11, 53, 4, 1), metatile=0x170, elevation=1),
            dict(rect=(2, 22, 3, 5), metatile=0x001, elevation=3),    # berry-soil plots -> grass
            dict(rect=(33, 6, 5, 2), metatile=0x001, elevation=3),
            dict(rect=(21, 41, 5, 2), metatile=0x001, elevation=3),
            dict(rect=(10, 6, 4, 2), like=(5, 21)),     # a way from the arrival meadow to the north shore
            dict(rect=(27, 47, 3, 2), like=(5, 21)),    # a way through the trees to the east strip
            dict(rect=(34, 45, 6, 4), like=(5, 21)),    # a gap in the east forest: the way to Bridger Forest
        ] + [p for p, _ in _shore_signs],
        # fences, and the green mats at the ends of the path through the forest band
        swap={0x149: GROUND(0x001), 0x30E: 0x306, 0x30F: 0x306, 0x317: 0x306, 0x307: 0x306},
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_BRIDGER_SHORE",
        arrival=(5, 17),
        connections=[connection("up", "MAP_STRATA_FOSSIL_LAKE", 2), connection("right", "MAP_STRATA_BRIDGER_FOREST", 36)],
        objects=[
            # The bull, placeholder sprite borrowed from its battle sprite's species. Hidden
            # (flag set) until the boss line is crossed, see scripts.inc.
            obj("LOCALID_STRATA_A5_BULL", "OBJ_EVENT_GFX_SPECIES(RHYPERIOR)", 39, 62,
                "StrataLakeForest_EventScript_BullTalk", movement="MOVEMENT_TYPE_FACE_LEFT",
                flag=BULL_FLAG),
        ],
        bgs=[anchor(5, 16)] + [s for _, s in _shore_signs],
        # The bull charges along the shore: x 14-20 is the beach lane west of the cliff, x 22-39
        # the grass lane east of it. (22 and 23 are a dead end at y 62, so they don't trigger.)
        coords=boss_triggers("ERA_GREEN_RIVER", "StrataLakeForest_EventScript_UintatheriumWest", [(x, 61) for x in range(14, 21)])
        + boss_triggers("ERA_GREEN_RIVER", "StrataLakeForest_EventScript_Uintatherium", [(x, 61) for x in range(24, 40)]),
        encounters=dict(
            land_mons=mons(("EOHIPPUS", 28, 30), ("HYRACHYUS", 28, 31), ("HYOPSODUS", 28, 30), ("EOHIPPUS", 29, 31),
                           ("HYRACHYUS", 29, 32), ("PRESBYORNIS", 29, 31), ("DIACODEXIS", 29, 31), ("HYOPSODUS", 30, 32),
                           ("HYRACHYUS", 30, 33), ("BOREALOSUCH", 30, 32), ("CORYPHODON", 31, 33), ("UINTATHERIUM", 32, 33)),
            water_mons=mons(("KNIGHTIA", 28, 32), ("HELIOBATIS", 28, 32), ("PRESBYORNIS", 29, 33),
                            ("BOREALOSUCH", 30, 33), ("BOREALOSUCH", 31, 34)),
            fishing_mons=mons(("KNIGHTIA", 26, 29), ("KNIGHTIA", 26, 29), ("KNIGHTIA", 27, 30), ("LEPISOSTEUS", 27, 30),
                              ("HELIOBATIS", 28, 31), ("LEPISOSTEUS", 28, 31), ("HELIOBATIS", 29, 32), ("LEPISOSTEUS", 29, 32),
                              ("HELIOBATIS", 30, 33), ("BOREALOSUCH", 31, 34)),
        ),
    ),
    dict(
        id="MAP_STRATA_FOSSIL_LAKE", name="StrataFossilLake", era="ERA_GREEN_RIVER",
        habitat="water", light="day",
        forage=[forage(21, 8, "CARRION"), forage(23, 13, "CARRION"), forage(5, 4, "FERN_FROND"),
                forage(10, 10, "PALM_FRUIT"), forage(8, 20, "LARVAE")],
        crop=dict(**{"from": "LAYOUT_ROUTE103"}, rect=(0, 0, 49, 22)),
        patches=[dict(rect=(8, 18, 6, 4), like=(9, 20))] + [p for p, _ in _fossil_signs],   # widen the way out south
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_FOSSIL_LAKE",
        connections=[connection("down", "MAP_STRATA_LAKE_FOREST", -2)],
        bgs=[anchor(9, 17)] + [s for _, s in _fossil_signs],
        # Walking the east shore for the first time: the mass-mortality scene.
        coords=[trigger(21, y, ACT5_VAR, 0, "StrataFossilLake_EventScript_Turnover") for y in (9, 10, 11)],
        encounters=dict(
            land_mons=mons(("ONYCHONYCTER", 26, 28), ("GALLINULOID", 26, 28), ("PRESBYORNIS", 27, 29), ("ONYCHONYCTER", 27, 29),
                           ("GALLINULOID", 27, 30), ("PRESBYORNIS", 28, 30), ("ONYCHONYCTER", 28, 30), ("GALLINULOID", 28, 31),
                           ("PRESBYORNIS", 29, 31), ("BOREALOSUCH", 29, 31), ("ONYCHONYCTER", 30, 31), ("GALLINULOID", 30, 31)),
            water_mons=mons(("KNIGHTIA", 26, 30), ("KNIGHTIA", 27, 31), ("HELIOBATIS", 27, 31),
                            ("HELIOBATIS", 28, 31), ("BOREALOSUCH", 29, 31)),
            fishing_mons=mons(("KNIGHTIA", 26, 28), ("KNIGHTIA", 26, 28), ("KNIGHTIA", 27, 29), ("LEPISOSTEUS", 27, 29),
                              ("KNIGHTIA", 28, 30), ("LEPISOSTEUS", 28, 30), ("HELIOBATIS", 28, 30), ("KNIGHTIA", 29, 31),
                              ("LEPISOSTEUS", 29, 31), ("HELIOBATIS", 30, 32)),
        ),
    ),
    dict(
        id="MAP_STRATA_BRIDGER_FOREST", name="StrataBridgerForest", era="ERA_GREEN_RIVER",
        habitat="forest", light="day",
        forage=[forage(9, 4, "PALM_FRUIT"), forage(38, 5, "BROWSE"), forage(22, 14, "LEGUME_POD"),
                forage(15, 16, "FERN_FROND"), forage(17, 12, "LARVAE")],
        crop=dict(**{"from": "LAYOUT_ROUTE116"}, rect=(0, 0, 40, 20)),
        patches=[dict(rect=(35, 3, 5, 8), metatile=0x001, elevation=3)]     # house and yard -> grass
        + [tree(x, y) for x, y in _forest_trees] + [p for p, _ in _forest_signs],
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_BRIDGER_FOREST",
        connections=[connection("left", "MAP_STRATA_LAKE_FOREST", -36), connection("right", "MAP_STRATA_OIL_SHALE", 0)],
        bgs=[anchor(3, 10)] + [s for _, s in _forest_signs],
        encounters=dict(
            land_mons=mons(("OMOMYS", 26, 28), ("PARAMYS", 26, 28), ("NOTHARCTUS", 27, 29), ("HYOPSODUS", 26, 28),
                           ("EOHIPPUS", 27, 29), ("OMOMYS", 27, 30), ("MIACIS", 27, 29), ("PARAMYS", 28, 30),
                           ("NOTHARCTUS", 29, 31), ("MIACIS", 29, 31), ("OMOMYS", 29, 31), ("EOHIPPUS", 29, 31)),
        ),
    ),
    dict(
        id="MAP_STRATA_OIL_SHALE", name="StrataOilShale", era="ERA_GREEN_RIVER",
        habitat="open", light="day",
        forage=[forage(12, 28, "CARRION"), forage(17, 24, "BROWSE"), forage(2, 15, "FERN_FROND"),
                forage(11, 31, "LARVAE")],
        crop=dict(**{"from": "LAYOUT_ROUTE115"}, rect=(14, 36, 26, 34)),
        patches=[
            dict(rect=(10, 15, 2, 15), metatile=0x00D, elevation=3),    # tall grass beside the sand path
            dict(rect=(16, 14, 3, 17), metatile=0x00D, elevation=3),    # ...and along the east strip (over the mud patch)
        ] +[p for p, _ in _shale_signs],
        # fences, boulders
        swap={0x148: GROUND(0x001), 0x149: GROUND(0x001), 0x139: GROUND(0x001), 0x140: GROUND(0x001), 0x0E0: GROUND(0x001)},
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_OIL_SHALE",
        connections=[connection("left", "MAP_STRATA_BRIDGER_FOREST", 0)],
        objects=[
            # The Patriofelis set piece: a one-time wild battle (flag set once it's over).
            obj("LOCALID_STRATA_A5_PATRIOFELIS", "OBJ_EVENT_GFX_SPECIES(LITLEO)", 12, 26,
                "StrataOilShale_EventScript_Patriofelis", movement="MOVEMENT_TYPE_LOOK_AROUND",
                flag=PATRIOFELIS_FLAG),
        ],
        bgs=[anchor(2, 12)] + [s for _, s in _shale_signs],
        coords=[trigger(x, 20, "VAR_TEMP_1", 0, "StrataOilShale_EventScript_PatriofelisSight") for x in range(10, 15)],
        encounters=dict(
            land_mons=mons(("DIACODEXIS", 28, 30), ("DIACODEXIS", 28, 30), ("HYOPSODUS", 28, 30), ("DIACODEXIS", 29, 31),
                           ("EOHIPPUS", 29, 31), ("HYOPSODUS", 29, 31), ("MIACIS", 30, 32), ("EOHIPPUS", 30, 32),
                           ("DIACODEXIS", 30, 32), ("PARAMYS", 30, 32), ("HYRACHYUS", 31, 33), ("MIACIS", 31, 33)),
            water_mons=mons(("KNIGHTIA", 28, 31), ("KNIGHTIA", 28, 32), ("HELIOBATIS", 29, 32),
                            ("HELIOBATIS", 29, 32), ("BOREALOSUCH", 30, 33)),
            fishing_mons=mons(("KNIGHTIA", 27, 29), ("KNIGHTIA", 27, 29), ("KNIGHTIA", 28, 30), ("LEPISOSTEUS", 28, 30),
                              ("HELIOBATIS", 28, 31), ("LEPISOSTEUS", 29, 31), ("KNIGHTIA", 29, 31), ("HELIOBATIS", 30, 32),
                              ("LEPISOSTEUS", 30, 32), ("BOREALOSUCH", 31, 33)),
        ),
    ),
]
