"""Act 1: Hell Creek, 66.04 Ma.

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The act, south to north and west to east:

    Backswamp
        |
    River Channel (the bluff: the tyrant waits on it)
        |
    Levee Forest -- Fern Glade        (arrival from camp: the Levee's south edge)

Act 2 (act2_impact.py) reuses the Levee, River and Backswamp footprints with winter
palettes; the Fern Glade is not rebuilt there (its herds and its perching birds are
gone by then).

Field notes are wooden signposts (a blocked metatile plus a sign event), as in Act 0.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_LEVEE", "LEVEE FOREST"),
    ("MAPSEC_STRATA_RIVER", "RIVER CHANNEL"),
    ("MAPSEC_STRATA_BACKSWAMP", "BACKSWAMP"),
    ("MAPSEC_STRATA_FERN_GLADE", "FERN GLADE"),
]

# General primary tileset: the wooden signpost.
SIGNPOST = 0x01B


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), sign(x, y, script, facing)


_LEVEE_NOTES = [signpost(21, 25, "StrataLevee_EventScript_NoteFlora"),
                signpost(12, 20, "StrataLevee_EventScript_NoteTriceratops"),
                signpost(30, 13, "StrataLevee_EventScript_NoteSmall")]
_RIVER_NOTES = [signpost(30, 18, "StrataRiver_EventScript_NoteChannel")]
_SWAMP_NOTES = [signpost(30, 12, "StrataBackswamp_EventScript_NoteDetritus"),
                signpost(23, 9, "StrataBackswamp_EventScript_NoteShallows")]
_GLADE_NOTES = [signpost(6, 4, "StrataFernGlade_EventScript_NoteBirds"),
                signpost(13, 15, "StrataFernGlade_EventScript_NoteHerd"),
                signpost(4, 12, "StrataFernGlade_EventScript_NoteFerns")]

# The Levee's east side opens into the glade, over rows 14-20 of the Levee (the glade's
# rows 2-8). The glade is cut from the open grassland of Route 120, east of its cliff.
GLADE_OFFSET = 12

# Map events are assembled without include/constants/strata.h, so they name the act flags by
# their stock FLAG_UNUSED_0x... / VAR_UNUSED_0x... names: FLAG_UNUSED_0x264 is
# FLAG_STRATA_A1_RAPTORS_GONE, 0x265 FLAG_STRATA_A1_TYRANT_GONE, VAR_UNUSED_0x40F7 VAR_STRATA_ACT1
# (include/constants/strata_act_flags.h).

# Where the tyrannosaur waits on the bluff, and the two ways up onto it.
_TYRANT_AT = (33, 6)

MAPS = [
    # ------------------------------------------------------------------
    # Hell Creek, 66.04 Ma (Act 1)
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LEVEE", name="StrataLevee", era="ERA_HELL_CREEK",
        habitat="forest", light="day", forage=[forage(6, 20, "FERN_FROND"), forage(34, 12, "LARVAE"), forage(28, 4, "PALM_FRUIT")],
        crop=LEVEE_CROP, patches=LEVEE_PATCHES + [p for p, _ in _LEVEE_NOTES],
        music="MUS_ROUTE119", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_LEVEE",
        connections=[connection("up", "MAP_STRATA_RIVER"), connection("right", "MAP_STRATA_FERN_GLADE", GLADE_OFFSET)],
        coords=return_edge(),
        bgs=[s for _, s in _LEVEE_NOTES],
        encounters=dict(
            land_mons=mons(("MESODMA", 3, 4), ("MESODMA", 3, 5), ("DIDELPHODON", 3, 5), ("THESCELOSAUR", 4, 5),
                           ("MESODMA", 4, 5), ("AVISAURUS", 5, 7), ("THESCELOSAUR", 4, 6), ("ACHERORAPTOR", 5, 6),
                           ("ANZU", 5, 6), ("PACHYCEPHALO", 5, 7), ("EDMONTOSAUR", 6, 7), ("TRICERATOPS", 6, 7)),
            water_mons=mons(("LEPISOSTEUS", 4, 8), ("LEPISOSTEUS", 4, 8), ("CHAMPSOSAUR", 5, 8),
                            ("CHAMPSOSAUR", 5, 8), ("BOREALOSUCH", 6, 9)),
        ),
    ),
    dict(
        id="MAP_STRATA_RIVER", name="StrataRiver", era="ERA_HELL_CREEK",
        habitat="water", light="day", forage=[forage(27, 15, "CARRION"), forage(34, 19, "FERN_FROND")],
        crop=RIVER_CROP, patches=RIVER_PATCHES + [p for p, _ in _RIVER_NOTES], swap=RIVER_SWAP,
        music="MUS_ROUTE119", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_RIVER",
        connections=[connection("down", "MAP_STRATA_LEVEE"), connection("up", "MAP_STRATA_BACKSWAMP")],
        coords=[
            # Both ways up onto the bluff where the tyrannosaur waits.
            trigger(x, y, "VAR_STRATA_STORY", 2, "StrataRiver_EventScript_Tyrannosaur")
            for x, y in ((30, 10), (31, 10), (35, 4), (36, 4))
        ],
        objects=[
            # The tyrant on the bluff: talking to it starts the same set piece as the triggers.
            obj("LOCALID_STRATA_RIVER_TYRANT", "OBJ_EVENT_GFX_SPECIES(TYRANTRUM)", _TYRANT_AT[0], _TYRANT_AT[1],
                "StrataRiver_EventScript_Tyrannosaur", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_UNUSED_0x265",
                elevation=4),
        ],
        bgs=[
            sign(29, 12, "StrataRiver_EventScript_Tracks"),
        ] + [s for _, s in _RIVER_NOTES],
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
        habitat="forest", light="day", forage=[forage(28, 12, "FERN_FROND"), forage(5, 2, "LARVAE"), forage(22, 4, "BROWSE")],
        crop=BACKSWAMP_CROP, patches=[p for p, _ in _SWAMP_NOTES],
        music="MUS_ROUTE120", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_BACKSWAMP",
        connections=[connection("down", "MAP_STRATA_RIVER")],
        bgs=[s for _, s in _SWAMP_NOTES],
        encounters=dict(
            land_mons=mons(("MESODMA", 6, 7), ("DIDELPHODON", 6, 8), ("EMARGINACHEL", 6, 8), ("MESODMA", 7, 8),
                           ("DIDELPHODON", 7, 8), ("THESCELOSAUR", 7, 8), ("CHAMPSOSAUR", 7, 9), ("EDMONTOSAUR", 7, 9),
                           ("ANZU", 8, 9), ("EDMONTOSAUR", 8, 10), ("ANKYLOSAURUS", 9, 10), ("BOREALOSUCH", 9, 10)),
            water_mons=mons(("LEPISOSTEUS", 6, 10), ("CHAMPSOSAUR", 6, 10), ("EMARGINACHEL", 7, 10),
                            ("BOREALOSUCH", 8, 11), ("BOREALOSUCH", 9, 11)),
            fishing_mons=mons(("LEPISOSTEUS", 6, 8), ("LEPISOSTEUS", 6, 8), ("LEPISOSTEUS", 7, 9), ("CHAMPSOSAUR", 7, 9),
                              ("LEPISOSTEUS", 7, 9), ("CHAMPSOSAUR", 8, 10), ("BOREALOSUCH", 8, 10), ("CHAMPSOSAUR", 8, 10),
                              ("BOREALOSUCH", 9, 11), ("BOREALOSUCH", 9, 11)),
        ),
    ),
    # The open glade east of the Levee: ferns and low flowering plants (no grass yet), a
    # herd of Edmontosaurus, and the last tree-perching birds.
    dict(
        id="MAP_STRATA_FERN_GLADE", name="StrataFernGlade", era="ERA_HELL_CREEK",
        habitat="open", light="day",
        forage=[forage(9, 3, "FERN_FROND"), forage(18, 12, "FERN_FROND"), forage(3, 16, "BROWSE"),
                forage(15, 8, "FERN_FROND"), forage(10, 17, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE120"}, rect=(18, 41, 22, 20)),
        patches=[p for p, _ in _GLADE_NOTES],
        music="MUS_ROUTE120", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_FERN_GLADE",
        connections=[connection("left", "MAP_STRATA_LEVEE", -GLADE_OFFSET)],
        coords=[
            # The raptor pair's ambush: a line across the glade (once).
            trigger(12, y, "VAR_UNUSED_0x40F7", 0, "StrataFernGlade_EventScript_RaptorAmbush") for y in range(0, 20)
        ],
        objects=[
            # Three Edmontosaurus grazing, and the Acheroraptor pair stalking them.
            obj("LOCALID_STRATA_GLADE_HERD_A", "OBJ_EVENT_GFX_SPECIES(TROPIUS)", 9, 9,
                "StrataFernGlade_EventScript_Herd", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_GLADE_HERD_B", "OBJ_EVENT_GFX_SPECIES(TROPIUS)", 11, 11,
                "StrataFernGlade_EventScript_Herd", "MOVEMENT_TYPE_FACE_LEFT"),
            obj("LOCALID_STRATA_GLADE_HERD_C", "OBJ_EVENT_GFX_SPECIES(TROPIUS)", 8, 13,
                "StrataFernGlade_EventScript_Herd", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_GLADE_RAPTOR_A", "OBJ_EVENT_GFX_SPECIES(ARCHEN)", 17, 4,
                "StrataFernGlade_EventScript_RaptorAmbush", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_UNUSED_0x264"),
            obj("LOCALID_STRATA_GLADE_RAPTOR_B", "OBJ_EVENT_GFX_SPECIES(ARCHEN)", 18, 6,
                "StrataFernGlade_EventScript_RaptorAmbush", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_UNUSED_0x264"),
        ],
        bgs=[s for _, s in _GLADE_NOTES],
        encounters=dict(
            land_mons=mons(("THESCELOSAUR", 5, 6), ("EDMONTOSAUR", 5, 7), ("MESODMA", 5, 6), ("EDMONTOSAUR", 6, 7),
                           ("THESCELOSAUR", 6, 7), ("AVISAURUS", 6, 8), ("PACHYCEPHALO", 6, 8), ("EDMONTOSAUR", 7, 8),
                           ("ANZU", 7, 8), ("AVISAURUS", 7, 9), ("ACHERORAPTOR", 7, 9), ("TRICERATOPS", 8, 9)),
        ),
    ),
]
