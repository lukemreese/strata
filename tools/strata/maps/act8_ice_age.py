"""Act 8: Ice Age Wyoming (~20 ka), the steppe and Natural Trap Cave, with the ~13 ka Colby coda.

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The act (Steppe is the hub; the Colby coda is reached by a marker, not a connection):

                 Ice Margin
                     |
    Meltwater -- Ice Age Steppe (arrival, anchor)  --- sinkhole ---> Natural Trap Cave (boss)
     River                   :
                             : sub-layer marker (after the boss) --> Colby Site, ~13 ka

All four 20 ka maps use the ice-age palettes (General + Mauville variants, gen_tilesets.py).
Colby uses the same set without snow: there is no late-glacial palette yet (outline §4.1).
The deposit-wide rule for every species list here: the encounter tables are the roster's
Trap Cave animals, and the field notes say where a placement is a stand-in.

Map events are assembled without include/constants/strata.h, so they name the act flags by
their stock FLAG_UNUSED_0x... / VAR_UNUSED_0x... names (include/constants/strata_act_flags.h):
FLAG_UNUSED_0x29C is FLAG_STRATA_A8_LIONS_GONE, VAR_UNUSED_0x40FE is VAR_STRATA_ACT8.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_ICE_AGE", "ICE AGE STEPPE"),
    ("MAPSEC_STRATA_TRAP_CAVE", "NATURAL TRAP CAVE"),
    ("MAPSEC_STRATA_MELTWATER", "MELTWATER RIVER"),
    ("MAPSEC_STRATA_ICE_MARGIN", "ICE MARGIN"),
    ("MAPSEC_STRATA_COLBY", "COLBY SITE"),
]

ICE_AGE_TILESETS = ("gTileset_GeneralIceAge", "gTileset_MauvilleIceAge")

# General primary tileset: the wooden signpost (field notes, and the anchor markers).
SIGNPOST = 0x01B


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), sign(x, y, script, facing)


def split(*notes):
    """([patches], [sign events]) of several signpost() results."""
    return [p for p, _ in notes], [s for _, s in notes]


# Where the American lion pair waits on the steppe, in the corridor to the sinkhole.
_LIONS = ((64, 10), (64, 11))

_STEPPE_NOTES = split(
    signpost(53, 9, "StrataSteppe_EventScript_NoteSteppe"),
    signpost(47, 10, "StrataSteppe_EventScript_NotePronghorn"),
    signpost(33, 10, "StrataSteppe_EventScript_NoteWolf"),
    signpost(68, 12, "StrataSteppe_EventScript_NoteSinkhole"),
    signpost(55, 8, "StrataSteppe_EventScript_SubLayer"),    # the sub-layer marker, beside the anchor
)
_CAVE_NOTES = split(
    signpost(16, 4, "StrataTrapCave_EventScript_NoteTrap"),
    signpost(22, 4, "StrataTrapCave_EventScript_NoteBlur"),
    signpost(30, 4, "StrataTrapCave_EventScript_NotePredators"),
)
_MELT_NOTES = split(
    signpost(2, 8, "StrataMeltwater_EventScript_NoteBraided"),
    signpost(33, 9, "StrataMeltwater_EventScript_NoteTurtle"),
    signpost(12, 8, "StrataMeltwater_EventScript_NoteMuskOx"),
    signpost(1, 7, "StrataFieldStation_EventScript_Anchor"),
)
_MARGIN_NOTES = split(
    signpost(26, 19, "StrataIceMargin_EventScript_NoteIce"),
    signpost(31, 12, "StrataIceMargin_EventScript_NoteSeaLevel"),
    signpost(23, 5, "StrataIceMargin_EventScript_NoteEdge"),
    signpost(27, 22, "StrataFieldStation_EventScript_Anchor"),
)
_COLBY_NOTES = split(
    signpost(8, 7, "StrataColby_EventScript_NoteSite"),
    signpost(16, 7, "StrataColby_EventScript_NoteEvidence"),
    signpost(5, 7, "StrataFieldStation_EventScript_Anchor"),
)

MAPS = [
    # ------------------------------------------------------------------
    # Act 8: Ice Age Wyoming (~20 ka): cold steppe, and Natural Trap Cave
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_STEPPE", name="StrataSteppe", era="ERA_TRAP_CAVE",
        habitat="open", light="day",
        forage=[forage(45, 10, "SEED_HEAD"), forage(40, 11, "CARRION"), forage(75, 10, "BROWSE"),
                forage(58, 5, "SEED_HEAD"), forage(34, 11, "BROWSE"), forage(52, 6, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE118"}, rect=(0, 0, 80, 20), tilesets=ICE_AGE_TILESETS),
        patches=[
            dict(rect=(0, 13, 5, 5), like=(2, 8)),      # house -> steppe
            dict(rect=(34, 5, 5, 2), metatile=0x001, elevation=3),    # berry-soil plot -> steppe
            # The sinkhole's mouth, south of its trigger row (65..71, 14): a rock lip
            # (the stock rock mound) around a black opening, replacing the tree belt.
            dict(at=(67, 15), collision=1, elevation=0,
                 tiles=[[0x080, 0x081, 0x082], [0x088, 0x071, 0x08A], [0x090, 0x1A2, 0x092]]),
        ] + _STEPPE_NOTES[0],
        music="MUS_ROUTE120", weather="WEATHER_SNOW", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_ICE_AGE",
        arrival=(56, 9),
        # Ice Margin up the pass at x 57..59 (its x 22..24), Meltwater River downstream, east.
        connections=[connection("right", "MAP_STRATA_MELTWATER"), connection("up", "MAP_STRATA_ICE_MARGIN", 35)],
        bgs=[anchor(56, 8)] + _STEPPE_NOTES[1],
        coords=[
            # The mouth of Natural Trap Cave: a sinkhole hidden in the snow.
            trigger(x, 14, "VAR_TEMP_1", 0, "StrataSteppe_EventScript_Sinkhole") for x in range(65, 72)
        ] + [
            # The American lion pair, in the only way through to the sinkhole (once).
            trigger(61, y, "VAR_UNUSED_0x40FE", 0, "StrataSteppe_EventScript_Lions") for y in range(9, 13)
        ],
        objects=[
            obj("LOCALID_STRATA_STEPPE_LION_A", "OBJ_EVENT_GFX_SPECIES(PYROAR)", _LIONS[0][0], _LIONS[0][1],
                "StrataSteppe_EventScript_Lions", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_UNUSED_0x29C"),
            obj("LOCALID_STRATA_STEPPE_LION_B", "OBJ_EVENT_GFX_SPECIES(PYROAR)", _LIONS[1][0], _LIONS[1][1],
                "StrataSteppe_EventScript_Lions", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_UNUSED_0x29C"),
        ],
        # Aenocyon is not wild here (H5: the dire wolf is not a secure record at the cave).
        encounters=dict(
            land_mons=mons(("EQUUS", 44, 46), ("OVIS", 44, 46), ("ANTILOCAPRA", 45, 47), ("CANIS", 45, 47),
                           ("EQUUS", 46, 48), ("CAMELOPS", 46, 48), ("MELEAGRIS", 46, 48), ("OVIBOS", 47, 49),
                           ("MIRACINONYX", 48, 50), ("OVIS", 48, 50), ("PANTHERA", 49, 51), ("MAMMUTHUS", 50, 51)),
            water_mons=mons(("CHELYDRA", 46, 50), ("CHELYDRA", 46, 50), ("CHELYDRA", 47, 50),
                            ("CHELYDRA", 48, 51), ("CHELYDRA", 49, 51)),
        ),
    ),
    dict(
        id="MAP_STRATA_TRAP_CAVE", name="StrataTrapCave", era="ERA_TRAP_CAVE",
        habitat=None, light="none", forage=[forage(26, 4, "CARRION"), forage(5, 9, "LARVAE")],
        crop=dict(**{"from": "LAYOUT_GRANITE_CAVE_1F"}, rect=(0, 0, 42, 15)),
        patches=[
            # The rope down from the surface, over the arrival point (14, 3).
            dict(at=(14, 1), tiles=[[0x217], [0x216]], collision=1, elevation=0),
        ] + _CAVE_NOTES[0],
        # Granite Cave's ladders and exit glows lead nowhere here -> plain floor
        swap={0x23F: 0x211, 0x207: 0x211, 0x23C: 0x211,
              0x258: 0x209, 0x259: 0x209, 0x25A: 0x209},   # (the last three: lit cave-mouth slabs)
        music="MUS_CAVE_OF_ORIGIN", map_type="MAP_TYPE_UNDERGROUND", mapsec="MAPSEC_STRATA_TRAP_CAVE",
        arrival=(14, 3),
        bgs=[sign(14, 2, "StrataTrapCave_EventScript_Rope")] + _CAVE_NOTES[1],
        coords=boss_triggers("ERA_TRAP_CAVE", "StrataTrapCave_EventScript_Arctodus",
                             [(x, 7) for x in range(17, 35)] + [(x, 6) for x in range(5, 10)]),
    ),
    # Braided glacial outwash: the Steppe's river, with a sand-bar ford across the channel so both
    # banks can be walked. Entered from the Steppe's east end (its x 79 -> this map's x 0).
    dict(
        id="MAP_STRATA_MELTWATER", name="StrataMeltwater", era="ERA_TRAP_CAVE",
        habitat="water", light="day",
        forage=[forage(14, 9, "SEED_HEAD"), forage(8, 7, "BROWSE"), forage(33, 11, "CARRION"), forage(30, 8, "BROWSE")],
        crop=dict(**{"from": "LAYOUT_ROUTE118"}, rect=(0, 0, 40, 20), tilesets=ICE_AGE_TILESETS),
        patches=[
            dict(rect=(0, 13, 5, 5), like=(2, 8)),                  # house -> steppe
            dict(rect=(34, 5, 5, 2), metatile=0x001, elevation=3),  # berry-soil plot -> steppe
            dict(rect=(18, 8, 10, 2), like=(16, 9)),                # a sand-bar ford across the main channel
        ] + _MELT_NOTES[0],
        music="MUS_ROUTE120", weather="WEATHER_SNOW", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_MELTWATER",
        connections=[connection("left", "MAP_STRATA_STEPPE")],
        bgs=_MELT_NOTES[1],
        encounters=dict(
            land_mons=mons(("EQUUS", 45, 47), ("OVIBOS", 45, 47), ("CAMELOPS", 46, 48), ("ANTILOCAPRA", 45, 47),
                           ("CANIS", 46, 48), ("OVIBOS", 47, 49), ("MELEAGRIS", 46, 48), ("EQUUS", 47, 49),
                           ("OVIS", 46, 48), ("PANTHERA", 48, 50), ("MIRACINONYX", 48, 50), ("MAMMUTHUS", 49, 51)),
            water_mons=mons(("CHELYDRA", 45, 49), ("CHELYDRA", 45, 49), ("CHELYDRA", 46, 50),
                            ("CHELYDRA", 47, 51), ("CHELYDRA", 48, 51)),
            fishing_mons=mons(("CHELYDRA", 44, 46), ("CHELYDRA", 44, 46), ("CHELYDRA", 45, 47), ("CHELYDRA", 45, 47),
                              ("CHELYDRA", 46, 48), ("CHELYDRA", 46, 48), ("CHELYDRA", 46, 49), ("CHELYDRA", 47, 49),
                              ("CHELYDRA", 47, 50), ("CHELYDRA", 48, 50)),
        ),
    ),
    # The edge of the glaciers: a pale basin of outwash silt under rock ridges (a Route 111 desert
    # cut, ice palettes). Reached up the pass at the north of the Steppe.
    dict(
        id="MAP_STRATA_ICE_MARGIN", name="StrataIceMargin", era="ERA_TRAP_CAVE",
        habitat="open", light="day",
        forage=[forage(30, 7, "SEED_HEAD"), forage(5, 8, "BROWSE"), forage(33, 17, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE111"}, rect=(0, 60, 40, 24), tilesets=ICE_AGE_TILESETS),
        patches=_MARGIN_NOTES[0],
        music="MUS_ROUTE120", weather="WEATHER_SNOW", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_ICE_MARGIN",
        connections=[connection("down", "MAP_STRATA_STEPPE", -35)],
        bgs=_MARGIN_NOTES[1],
        encounters=dict(
            land_mons=mons(("OVIBOS", 46, 48), ("OVIS", 46, 48), ("OVIBOS", 47, 49), ("CANIS", 47, 49),
                           ("OVIS", 47, 49), ("MAMMUTHUS", 48, 50), ("EQUUS", 47, 49), ("PANTHERA", 48, 50),
                           ("CAMELOPS", 48, 50), ("MAMMUTHUS", 49, 51), ("PANTHERA", 49, 51), ("OVIBOS", 50, 51)),
        ),
    ),
    # Coda: the Colby mammoth site, ~13 ka, the Bighorn Basin. A thin late-glacial sub-layer of
    # the same era (no lineage changes), entered through the marker beside the Steppe's anchor.
    # No encounters: the rig can build the bones and the stone, not the people (rule R-g).
    dict(
        id="MAP_STRATA_COLBY", name="StrataColby", era="ERA_TRAP_CAVE",
        habitat=None, light="day",
        forage=[forage(10, 6, "SEED_HEAD"), forage(22, 8, "BROWSE")],
        crop=dict(**{"from": "LAYOUT_ROUTE118"}, rect=(50, 3, 30, 17), tilesets=ICE_AGE_TILESETS),
        patches=_COLBY_NOTES[0],
        music="MUS_ROUTE120", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_COLBY",
        arrival=(4, 8),
        bgs=_COLBY_NOTES[1],
        coords=[trigger(10, y, "VAR_TEMP_1", 0, "StrataColby_EventScript_Intro") for y in (6, 7, 8, 9)],
        objects=[
            # The bone pile (stand-in boulders) and, among the bones, the point.
            obj("LOCALID_STRATA_COLBY_BONES_A", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 13, 7,
                "StrataColby_EventScript_Bones", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_COLBY_BONES_B", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 15, 8,
                "StrataColby_EventScript_Bones", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_COLBY_BONES_C", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 12, 9,
                "StrataColby_EventScript_Bones", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_COLBY_POINT", "OBJ_EVENT_GFX_ITEM_BALL", 14, 8,
                "StrataColby_EventScript_Point", "MOVEMENT_TYPE_FACE_DOWN"),
        ],
    ),
]
