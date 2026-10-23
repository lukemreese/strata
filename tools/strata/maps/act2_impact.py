"""Act 2: Hell Creek about a year after the Chicxulub impact (impact winter).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_ASHEN_LEVEE", "ASHEN LEVEE"),
    ("MAPSEC_STRATA_ASHEN_RIVER", "ASHEN RIVER"),
    ("MAPSEC_STRATA_ASHEN_SWAMP", "ASHEN SWAMP"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Hell Creek, ~1 year after the Chicxulub impact (Act 2): the same
    # place, soot-darkened and ash-covered. Only the survivors remain.
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LEVEE_WINTER", name="StrataLeveeWinter", era="ERA_IMPACT_WINTER",
        crop=winter(LEVEE_CROP), patches=LEVEE_PATCHES,
        music="MUS_ABANDONED_SHIP", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_ASHEN_LEVEE",
        connections=[connection("up", "MAP_STRATA_RIVER_WINTER")],
        coords=return_edge(),
        encounters=dict(
            land_mons=mons(("MESODMA", 10, 11), ("MESODMA", 10, 12), ("MESODMA", 11, 12), ("CIMOLESTES", 10, 12),
                           ("MESODMA", 11, 13), ("CHAMPSOSAUR", 11, 13), ("ASTERIORNIS", 11, 13), ("CIMOLESTES", 12, 13),
                           ("EMARGINACHEL", 12, 13), ("ASTERIORNIS", 12, 14), ("CHAMPSOSAUR", 12, 14), ("BOREALOSUCH", 13, 14)),
            water_mons=mons(("LEPISOSTEUS", 10, 13), ("LEPISOSTEUS", 10, 13), ("CHAMPSOSAUR", 11, 13),
                            ("EMARGINACHEL", 11, 13), ("BOREALOSUCH", 12, 14)),
        ),
    ),
    dict(
        id="MAP_STRATA_RIVER_WINTER", name="StrataRiverWinter", era="ERA_IMPACT_WINTER",
        crop=winter(RIVER_CROP), patches=RIVER_PATCHES, swap=RIVER_SWAP,
        music="MUS_ABANDONED_SHIP", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_ASHEN_RIVER",
        connections=[connection("down", "MAP_STRATA_LEVEE_WINTER"), connection("up", "MAP_STRATA_BACKSWAMP_WINTER")],
        bgs=[
            sign(29, 12, "StrataRiverWinter_EventScript_Bluff"),
        ],
        encounters=dict(
            land_mons=mons(("MESODMA", 11, 12), ("MESODMA", 11, 13), ("CIMOLESTES", 11, 13), ("CHAMPSOSAUR", 12, 13),
                           ("MESODMA", 12, 13), ("ASTERIORNIS", 12, 14), ("CHAMPSOSAUR", 12, 14), ("EMARGINACHEL", 12, 14),
                           ("CIMOLESTES", 13, 14), ("ASTERIORNIS", 13, 14), ("BOREALOSUCH", 13, 15), ("BOREALOSUCH", 14, 15)),
            water_mons=mons(("LEPISOSTEUS", 11, 14), ("CHAMPSOSAUR", 11, 14), ("LEPISOSTEUS", 12, 14),
                            ("EMARGINACHEL", 12, 15), ("BOREALOSUCH", 13, 15)),
            fishing_mons=mons(("LEPISOSTEUS", 10, 12), ("LEPISOSTEUS", 10, 12), ("LEPISOSTEUS", 11, 13), ("CHAMPSOSAUR", 11, 13),
                              ("LEPISOSTEUS", 11, 13), ("CHAMPSOSAUR", 12, 14), ("EMARGINACHEL", 12, 14), ("LEPISOSTEUS", 12, 14),
                              ("BOREALOSUCH", 13, 15), ("BOREALOSUCH", 13, 15)),
        ),
    ),
    dict(
        id="MAP_STRATA_BACKSWAMP_WINTER", name="StrataBackswampWinter", era="ERA_IMPACT_WINTER",
        crop=winter(BACKSWAMP_CROP),
        music="MUS_ABANDONED_SHIP", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_ASHEN_SWAMP",
        connections=[connection("down", "MAP_STRATA_RIVER_WINTER")],
        coords=[
            # The starving season: the survivors guard the last open water.
            trigger(x, 13, "VAR_STRATA_STORY", 4, "StrataBackswampWinter_EventScript_Gauntlet")
            for x in range(23, 38)
        ],
        encounters=dict(
            land_mons=mons(("MESODMA", 12, 13), ("CHAMPSOSAUR", 12, 14), ("MESODMA", 12, 14), ("CIMOLESTES", 12, 14),
                           ("CHAMPSOSAUR", 13, 14), ("EMARGINACHEL", 13, 14), ("ASTERIORNIS", 13, 15), ("BOREALOSUCH", 13, 15),
                           ("MESODMA", 13, 15), ("CHAMPSOSAUR", 14, 15), ("BOREALOSUCH", 14, 16), ("BOREALOSUCH", 15, 16)),
            water_mons=mons(("LEPISOSTEUS", 12, 15), ("CHAMPSOSAUR", 12, 15), ("BOREALOSUCH", 13, 15),
                            ("EMARGINACHEL", 13, 16), ("BOREALOSUCH", 14, 16)),
            fishing_mons=mons(("LEPISOSTEUS", 11, 13), ("LEPISOSTEUS", 11, 13), ("LEPISOSTEUS", 12, 14), ("CHAMPSOSAUR", 12, 14),
                              ("LEPISOSTEUS", 12, 14), ("CHAMPSOSAUR", 13, 15), ("EMARGINACHEL", 13, 15), ("BOREALOSUCH", 13, 15),
                              ("BOREALOSUCH", 14, 16), ("BOREALOSUCH", 14, 16)),
        ),
    ),
]
