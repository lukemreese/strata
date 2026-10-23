"""Act 4: Bighorn Basin, WY (~56 Ma, PETM).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_BIGHORN", "BIGHORN BASIN"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Act 4: Bighorn Basin, WY (~56 Ma): PETM hothouse, red floodplain soils
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_RED_BEDS", name="StrataRedBeds", era="ERA_BIGHORN_PETM",
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 0, 40, 34), tilesets=("gTileset_GeneralPetm", "gTileset_FallarborPetm")),
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
        ],
        swap={0x2F4: 0x279},   # the ground with a pond's edge line, also the striped 'bridge'
        music="MUS_ROUTE110", weather="WEATHER_DROUGHT", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_BIGHORN",
        arrival=(31, 8),
        bgs=[anchor(31, 7)],
        coords=boss_triggers("ERA_BIGHORN_PETM", "StrataRedBeds_EventScript_Coryphodon", [(x, 26) for x in range(19, 23)]),
        encounters=dict(
            land_mons=mons(("SIFRHIPPUS", 22, 24), ("HYOPSODUS", 22, 24), ("DIACODEXIS", 22, 24), ("TEILHARDINA", 22, 24),
                           ("SIFRHIPPUS", 23, 25), ("HYOPSODUS", 23, 25), ("PROTICTIS", 23, 25), ("MESODMA", 23, 25),
                           ("DIACODEXIS", 24, 26), ("GASTORNIS", 24, 26), ("PROTOCHELYD", 24, 26), ("CORYPHODON", 25, 27)),
            water_mons=mons(("LEPISOSTEUS", 22, 26), ("CHAMPSOSAUR", 22, 26), ("LEPISOSTEUS", 23, 27),
                            ("BOREALOSUCH", 24, 27), ("CORYPHODON", 25, 28)),
            fishing_mons=mons(("LEPISOSTEUS", 20, 23), ("LEPISOSTEUS", 20, 23), ("LEPISOSTEUS", 21, 24), ("CHAMPSOSAUR", 21, 24),
                              ("LEPISOSTEUS", 22, 25), ("CHAMPSOSAUR", 22, 25), ("PROTOCHELYD", 23, 26), ("CHAMPSOSAUR", 23, 26),
                              ("BOREALOSUCH", 24, 27), ("BOREALOSUCH", 25, 28)),
        ),
    ),
]
