"""Act 1: Hell Creek, 66.04 Ma.

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_LEVEE", "LEVEE FOREST"),
    ("MAPSEC_STRATA_RIVER", "RIVER CHANNEL"),
    ("MAPSEC_STRATA_BACKSWAMP", "BACKSWAMP"),
]

MAPS = [
    # ------------------------------------------------------------------
    # Hell Creek, 66.04 Ma (Act 1)
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LEVEE", name="StrataLevee", era="ERA_HELL_CREEK",
        crop=LEVEE_CROP, patches=LEVEE_PATCHES,
        music="MUS_ROUTE119", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_LEVEE",
        connections=[connection("up", "MAP_STRATA_RIVER")],
        coords=return_edge(),
        encounters=dict(
            land_mons=mons(("MESODMA", 3, 4), ("MESODMA", 3, 5), ("DIDELPHODON", 3, 5), ("THESCELOSAUR", 4, 5),
                           ("MESODMA", 4, 5), ("DIDELPHODON", 4, 6), ("THESCELOSAUR", 4, 6), ("ACHERORAPTOR", 5, 6),
                           ("ANZU", 5, 6), ("PACHYCEPHALO", 5, 7), ("EDMONTOSAUR", 6, 7), ("TRICERATOPS", 6, 7)),
            water_mons=mons(("LEPISOSTEUS", 4, 8), ("LEPISOSTEUS", 4, 8), ("CHAMPSOSAUR", 5, 8),
                            ("CHAMPSOSAUR", 5, 8), ("BOREALOSUCH", 6, 9)),
        ),
    ),
    dict(
        id="MAP_STRATA_RIVER", name="StrataRiver", era="ERA_HELL_CREEK",
        crop=RIVER_CROP, patches=RIVER_PATCHES, swap=RIVER_SWAP,
        music="MUS_ROUTE119", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_RIVER",
        connections=[connection("down", "MAP_STRATA_LEVEE"), connection("up", "MAP_STRATA_BACKSWAMP")],
        coords=[
            # Both ways up onto the bluff where the tyrannosaur waits.
            trigger(x, y, "VAR_STRATA_STORY", 2, "StrataRiver_EventScript_Tyrannosaur")
            for x, y in ((30, 10), (31, 10), (35, 4), (36, 4))
        ],
        bgs=[
            sign(29, 12, "StrataRiver_EventScript_Tracks"),
        ],
        encounters=dict(
            land_mons=mons(("MESODMA", 5, 6), ("DIDELPHODON", 5, 7), ("THESCELOSAUR", 5, 7), ("ACHERORAPTOR", 6, 7),
                           ("DIDELPHODON", 6, 7), ("ANZU", 6, 8), ("THESCELOSAUR", 6, 8), ("PACHYCEPHALO", 7, 8),
                           ("ACHERORAPTOR", 7, 8), ("EDMONTOSAUR", 7, 9), ("TRICERATOPS", 8, 9), ("ANKYLOSAURUS", 8, 9)),
            water_mons=mons(("LEPISOSTEUS", 5, 9), ("CHAMPSOSAUR", 5, 9), ("LEPISOSTEUS", 6, 9),
                            ("CHAMPSOSAUR", 6, 10), ("BOREALOSUCH", 8, 10)),
            fishing_mons=mons(("LEPISOSTEUS", 5, 7), ("LEPISOSTEUS", 5, 7), ("LEPISOSTEUS", 6, 8), ("CHAMPSOSAUR", 6, 8),
                              ("LEPISOSTEUS", 6, 8), ("CHAMPSOSAUR", 7, 9), ("CHAMPSOSAUR", 7, 9), ("LEPISOSTEUS", 7, 9),
                              ("BOREALOSUCH", 8, 10), ("BOREALOSUCH", 8, 10)),
        ),
    ),
    dict(
        id="MAP_STRATA_BACKSWAMP", name="StrataBackswamp", era="ERA_HELL_CREEK",
        crop=BACKSWAMP_CROP,
        music="MUS_ROUTE120", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_BACKSWAMP",
        connections=[connection("down", "MAP_STRATA_RIVER")],
        encounters=dict(
            land_mons=mons(("MESODMA", 6, 7), ("DIDELPHODON", 6, 8), ("CHAMPSOSAUR", 6, 8), ("MESODMA", 7, 8),
                           ("DIDELPHODON", 7, 8), ("THESCELOSAUR", 7, 8), ("CHAMPSOSAUR", 7, 9), ("EDMONTOSAUR", 7, 9),
                           ("ANZU", 8, 9), ("EDMONTOSAUR", 8, 10), ("ANKYLOSAURUS", 9, 10), ("BOREALOSUCH", 9, 10)),
            water_mons=mons(("LEPISOSTEUS", 6, 10), ("CHAMPSOSAUR", 6, 10), ("LEPISOSTEUS", 7, 10),
                            ("BOREALOSUCH", 8, 11), ("BOREALOSUCH", 9, 11)),
            fishing_mons=mons(("LEPISOSTEUS", 6, 8), ("LEPISOSTEUS", 6, 8), ("LEPISOSTEUS", 7, 9), ("CHAMPSOSAUR", 7, 9),
                              ("LEPISOSTEUS", 7, 9), ("CHAMPSOSAUR", 8, 10), ("BOREALOSUCH", 8, 10), ("CHAMPSOSAUR", 8, 10),
                              ("BOREALOSUCH", 9, 11), ("BOREALOSUCH", 9, 11)),
        ),
    ),
]
