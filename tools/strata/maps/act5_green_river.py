"""Act 5: Green River lakes, WY (~52-46 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_GREEN_RIVER", "LAKE GOSIUTE"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Act 5: Green River lakes, WY (~52-46 Ma): subtropical lake and forest
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LAKE_FOREST", name="StrataLakeForest", era="ERA_GREEN_RIVER",
        habitat="forest", light="day", forage=[forage(3, 21, "PALM_FRUIT"), forage(30, 24, "LARVAE"), forage(20, 44, "LEGUME_POD")],
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
        ],
        # fences, and the green mats at the ends of the path through the forest band
        swap={0x149: GROUND(0x001), 0x30E: 0x306, 0x30F: 0x306, 0x317: 0x306, 0x307: 0x306},
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_GREEN_RIVER",
        arrival=(5, 17),
        bgs=[anchor(5, 16)],
        coords=boss_triggers("ERA_GREEN_RIVER", "StrataLakeForest_EventScript_Uintatherium", [(x, 61) for x in range(14, 40) if x != 21]),
        encounters=dict(
            land_mons=mons(("EOHIPPUS", 28, 30), ("NOTHARCTUS", 28, 30), ("ONYCHONYCTER", 28, 30), ("HYOPSODUS", 28, 30),
                           ("EOHIPPUS", 29, 31), ("MIACIS", 29, 31), ("GALLINULOID", 29, 31), ("DIACODEXIS", 29, 31),
                           ("NOTHARCTUS", 30, 32), ("PRESBYORNIS", 30, 32), ("CORYPHODON", 31, 33), ("UINTATHERIUM", 32, 33)),
            water_mons=mons(("KNIGHTIA", 28, 32), ("HELIOBATIS", 28, 32), ("PRESBYORNIS", 29, 33),
                            ("BOREALOSUCH", 30, 33), ("CHAMPSOSAUR", 30, 34)),
            fishing_mons=mons(("KNIGHTIA", 26, 29), ("KNIGHTIA", 26, 29), ("KNIGHTIA", 27, 30), ("LEPISOSTEUS", 27, 30),
                              ("HELIOBATIS", 28, 31), ("LEPISOSTEUS", 28, 31), ("HELIOBATIS", 29, 32), ("LEPISOSTEUS", 29, 32),
                              ("HELIOBATIS", 30, 33), ("BOREALOSUCH", 31, 34)),
        ),
    ),
]
