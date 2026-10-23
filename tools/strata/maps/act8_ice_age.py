"""Act 8: Ice Age Wyoming (~20 ka), the steppe and Natural Trap Cave.

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_ICE_AGE", "ICE AGE STEPPE"),
    ("MAPSEC_STRATA_TRAP_CAVE", "NATURAL TRAP CAVE"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Act 8: Ice Age Wyoming (~20 ka): cold steppe, and Natural Trap Cave
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_STEPPE", name="StrataSteppe", era="ERA_TRAP_CAVE",
        crop=dict(**{"from": "LAYOUT_ROUTE118"}, rect=(0, 0, 80, 20), tilesets=("gTileset_GeneralIceAge", "gTileset_MauvilleIceAge")),
        patches=[
            dict(rect=(0, 13, 5, 5), like=(2, 8)),      # house -> steppe
            dict(rect=(34, 5, 5, 2), metatile=0x001, elevation=3),    # berry-soil plot -> steppe
            # The sinkhole's mouth, south of its trigger row (65..71, 14): a rock lip
            # (the stock rock mound) around a black opening, replacing the tree belt.
            dict(at=(67, 15), collision=1, elevation=0,
                 tiles=[[0x080, 0x081, 0x082], [0x088, 0x071, 0x08A], [0x090, 0x1A2, 0x092]]),
        ],
        music="MUS_ROUTE120", weather="WEATHER_SNOW", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_ICE_AGE",
        arrival=(56, 9),
        bgs=[anchor(56, 8)],
        coords=[
            # The mouth of Natural Trap Cave: a sinkhole hidden in the snow.
            trigger(x, 14, "VAR_TEMP_1", 0, "StrataSteppe_EventScript_Sinkhole") for x in range(65, 72)
        ],
        encounters=dict(
            land_mons=mons(("EQUUS", 46, 48), ("OVIS", 46, 48), ("CANIS", 46, 48), ("ANTILOCAPRA", 46, 48),
                           ("EQUUS", 47, 49), ("CAMELOPS", 47, 49), ("MELEAGRIS", 47, 49), ("OVIBOS", 47, 49),
                           ("AENOCYON", 48, 50), ("MIRACINONYX", 48, 50), ("PANTHERA", 49, 51), ("MAMMUTHUS", 50, 51)),
            water_mons=mons(("CHELYDRA", 46, 50), ("CHELYDRA", 46, 50), ("CHELYDRA", 47, 50),
                            ("CHELYDRA", 48, 51), ("CHELYDRA", 49, 51)),
        ),
    ),
    dict(
        id="MAP_STRATA_TRAP_CAVE", name="StrataTrapCave", era="ERA_TRAP_CAVE",
        crop=dict(**{"from": "LAYOUT_GRANITE_CAVE_1F"}, rect=(0, 0, 42, 15)),
        patches=[
            # The rope down from the surface, over the arrival point (14, 3).
            dict(at=(14, 1), tiles=[[0x217], [0x216]], collision=1, elevation=0),
        ],
        # Granite Cave's ladders and exit glows lead nowhere here -> plain floor
        swap={0x23F: 0x211, 0x207: 0x211, 0x23C: 0x211,
              0x258: 0x209, 0x259: 0x209, 0x25A: 0x209},   # (the last three: lit cave-mouth slabs)
        music="MUS_CAVE_OF_ORIGIN", map_type="MAP_TYPE_UNDERGROUND", mapsec="MAPSEC_STRATA_TRAP_CAVE",
        arrival=(14, 3),
        bgs=[sign(14, 2, "StrataTrapCave_EventScript_Rope")],
        coords=boss_triggers("ERA_TRAP_CAVE", "StrataTrapCave_EventScript_Arctodus",
                             [(x, 7) for x in range(17, 35)] + [(x, 6) for x in range(5, 10)]),
    ),
]
