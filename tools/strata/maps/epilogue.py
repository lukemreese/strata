"""Epilogue: Montana today.

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The epilogue, west to east and north to south:

    Jordan (Act 0 hub: its west highway opens at story 18) --> Montana Prairie
                                                              |   \\
                                                  Interpretive      Missouri Breaks
                                                  Center (door)     (east edge)
                                                       |
                                                 Pryor Mountains (south edge)

    Interpretive Center 1F: the Pair on display, Halvorsen (the final peer review:
                            hook for C13), staff and visitors.
    Hall of Lost Lineages (2F): one plaque per extinction filter of src/data/lineages.h.
                            Hook for F4/S3: per-lineage plaques from the fossil flags.

There is no boss and no epilogue var. Act state lives in the flags below
(FLAG_STRATA_EPI_*, include/constants/strata_act_flags.h; map events name them by
their stock FLAG_UNUSED_0x... names since they are assembled without strata.h:
0x2A4 FERRET_MET, 0x2A5 PAIR_SEEN, 0x2A6 HALL_SEEN, 0x2A7 PEER_REVIEW_DONE).

Present-day maps use the real clock (light="dns") and the stock Hoenn tilesets.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_PRAIRIE", "MONTANA PRAIRIE"),
    ("MAPSEC_STRATA_MISSOURI_BREAKS", "MISSOURI BREAKS"),
    ("MAPSEC_STRATA_PRYOR", "PRYOR MOUNTAINS"),
    ("MAPSEC_STRATA_INTERPRETIVE", "INTERPRETIVE CENTER"),
]

# General primary tileset: the wooden signpost (a blocked metatile) for field notes.
SIGNPOST = 0x01B


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), sign(x, y, script, facing)


# A small brown-roofed building (4 x 4) copied from Oldale Town (same tilesets as
# Route 102): the Interpretive Center. The door is the second tile of the bottom row.
# Roof top: walkable-under (elevation 3); the rest blocks, the door warps when entered.
CENTER_AT = (36, 8)
CENTER_DOOR = (37, 11)
_CENTER_PATCHES = [
    dict(at=CENTER_AT, tiles=[[0x26C, 0x26D, 0x26D, 0x26E]], collision=0, elevation=3),
    dict(at=(CENTER_AT[0], CENTER_AT[1] + 1), tiles=[[0x274, 0x275, 0x275, 0x276], [0x27C, 0x27F, 0x27D, 0x27E],
                                                       [0x284, 0x287, 0x28F, 0x286]], collision=1, elevation=0),
]

_PRAIRIE_NOTES = [signpost(7, 13, "StrataPrairie_EventScript_NoteGrouse"),
                  signpost(21, 15, "StrataPrairie_EventScript_NoteFox"),
                  signpost(30, 16, "StrataPrairie_EventScript_NoteBison"),
                  signpost(39, 12, "StrataPrairie_EventScript_CenterSign")]
_BREAKS_NOTES = [signpost(10, 7, "StrataMissouriBreaks_EventScript_NoteRocks"),
                 signpost(4, 12, "StrataMissouriBreaks_EventScript_NoteGar"),
                 signpost(20, 6, "StrataMissouriBreaks_EventScript_NoteSheep")]
_PRYOR_NOTES = [signpost(8, 2, "StrataPryor_EventScript_NoteLimestone"),
                signpost(14, 10, "StrataPryor_EventScript_NoteHorses"),
                signpost(24, 14, "StrataPryor_EventScript_NotePronghorn")]

# Map events are assembled without include/constants/strata.h: act flags by stock name.
_FERRET_MET = "FLAG_UNUSED_0x2A4"

MAPS = [
    # ------------------------------------------------------------------
    # Epilogue: the Montana prairie today, open only once the present is loaded
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_PRAIRIE", name="StrataPrairie", era="ERA_EPILOGUE",
        habitat="open", light="dns",
        forage=[forage(20, 9, "SEED_HEAD"), forage(10, 4, "LEGUME_POD"), forage(33, 17, "SEED_HEAD"),
                forage(46, 9, "LARVAE"), forage(8, 16, "BROWSE")],
        crop=dict(**{"from": "LAYOUT_ROUTE102"}, rect=(0, 0, 50, 20)),
        patches=[
            dict(rect=(23, 2, 4, 2), metatile=0x001, elevation=3),    # berry-soil plot -> grass
        ] + _CENTER_PATCHES + [p for p, _ in _PRAIRIE_NOTES],
        music="MUS_ROUTE101", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_PRAIRIE",
        arrival=(2, 9),
        # East: the river breaks, through the gap in the trees (rows 10-11). South: the
        # Pryor Mountains, through the open throat of the south edge (columns 24-31).
        connections=[connection("right", "MAP_STRATA_MISSOURI_BREAKS", 3),
                     connection("down", "MAP_STRATA_PRYOR", 18)],
        warps=[warp(CENTER_DOOR[0], CENTER_DOOR[1], "MAP_STRATA_INTERPRETIVE_1F", 0)],     # 0: the Interpretive Center
        objects=[
            # The prairie-dog town: three black-tailed prairie dogs, and the ferret that hunts them.
            obj("LOCALID_STRATA_PRAIRIE_DOG_A", "OBJ_EVENT_GFX_SPECIES(CYNOMYS)", 42, 8,
                "StrataPrairie_EventScript_Dog", "MOVEMENT_TYPE_LOOK_AROUND"),
            obj("LOCALID_STRATA_PRAIRIE_DOG_B", "OBJ_EVENT_GFX_SPECIES(CYNOMYS)", 45, 12,
                "StrataPrairie_EventScript_Dog", "MOVEMENT_TYPE_FACE_LEFT"),
            obj("LOCALID_STRATA_PRAIRIE_DOG_C", "OBJ_EVENT_GFX_SPECIES(CYNOMYS)", 41, 14,
                "StrataPrairie_EventScript_Dog", "MOVEMENT_TYPE_FACE_UP"),
            obj("LOCALID_STRATA_PRAIRIE_FERRET", "OBJ_EVENT_GFX_SPECIES(MUSTELA)", 44, 10,
                "StrataPrairie_EventScript_Ferret", "MOVEMENT_TYPE_FACE_DOWN", flag=_FERRET_MET),
        ],
        bgs=[sign(2, 10, "StrataPrairie_EventScript_TrailToCamp"),
             # The stock route sign beside the town (a blue sign tile): the prairie-dog note.
             sign(40, 9, "StrataPrairie_EventScript_NoteDogs")] + [s for _, s in _PRAIRIE_NOTES],
        encounters=dict(
            # The ferret is rare (the town's two 4% slots); levels follow outline 3.1 (46-54).
            land_mons=mons(("CYNOMYS", 46, 49), ("ANTILOCAPRA", 47, 50), ("CENTROCERCUS", 46, 50), ("VULPES", 46, 50),
                           ("CYNOMYS", 48, 51), ("CANIS", 48, 51), ("MELEAGRIS", 48, 52), ("BISON", 49, 52),
                           ("MUSTELA", 46, 50), ("MUSTELA", 47, 50), ("BISON", 51, 53), ("OVIS", 51, 53)),
            water_mons=mons(("CHELYDRA", 48, 52), ("LEPISOSTEUS", 48, 52), ("CHELYDRA", 49, 52),
                            ("LEPISOSTEUS", 50, 53), ("CHELYDRA", 51, 53)),
            fishing_mons=mons(("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 47, 50), ("CHELYDRA", 47, 50),
                              ("LEPISOSTEUS", 48, 51), ("CHELYDRA", 48, 51), ("LEPISOSTEUS", 49, 52), ("CHELYDRA", 49, 52),
                              ("CHELYDRA", 50, 53), ("CHELYDRA", 51, 54)),
        ),
    ),
    # The river badlands of central Montana: the same Hell Creek rocks as Act 1, eroding today.
    dict(
        id="MAP_STRATA_MISSOURI_BREAKS", name="StrataMissouriBreaks", era="ERA_EPILOGUE",
        habitat="water", light="dns",
        forage=[forage(14, 4, "LARVAE"), forage(20, 10, "BROWSE"), forage(5, 14, "CARRION"),
                forage(22, 3, "SEED_HEAD"), forage(16, 7, "FERN_FROND")],
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(16, 4, 24, 29)),
        patches=[
            dict(rect=(12, 0, 4, 3), same_as=(14, 9)),                # the house -> bare ground
            dict(rect=(16, 0, 8, 5), same_as=(14, 9)),                # berry-soil plots -> bare ground
            dict(rect=(16, 7, 8, 4), same_as=(14, 9)),
            dict(rect=(3, 17, 4, 12), same_as=(10, 22)),              # the bridge -> open river
        ] + [p for p, _ in _BREAKS_NOTES],
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_MISSOURI_BREAKS",
        connections=[connection("left", "MAP_STRATA_PRAIRIE", -3)],
        bgs=[s for _, s in _BREAKS_NOTES],
        encounters=dict(
            land_mons=mons(("OVIS", 47, 51), ("MELEAGRIS", 47, 50), ("OVIS", 48, 52), ("MELEAGRIS", 48, 51),
                           ("CANIS", 48, 51), ("OVIS", 49, 52), ("CHELYDRA", 48, 52), ("MELEAGRIS", 49, 52),
                           ("CHELYDRA", 49, 53), ("OVIS", 50, 53), ("CANIS", 50, 53), ("OVIS", 51, 54)),
            water_mons=mons(("CHELYDRA", 48, 53), ("LEPISOSTEUS", 48, 53), ("CHELYDRA", 49, 53),
                            ("LEPISOSTEUS", 50, 54), ("CHELYDRA", 51, 54)),
            fishing_mons=mons(("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 47, 50), ("CHELYDRA", 47, 50),
                              ("LEPISOSTEUS", 48, 51), ("CHELYDRA", 48, 51), ("LEPISOSTEUS", 49, 52), ("CHELYDRA", 49, 52),
                              ("CHELYDRA", 50, 53), ("LEPISOSTEUS", 51, 54)),
        ),
    ),
    # Optional: the red limestone foothills where feral horses run.
    dict(
        id="MAP_STRATA_PRYOR", name="StrataPryor", era="ERA_EPILOGUE",
        habitat="open", light="dns",
        forage=[forage(10, 8, "SEED_HEAD"), forage(4, 2, "BROWSE"), forage(25, 13, "SEED_HEAD"),
                forage(20, 9, "LARVAE"), forage(28, 15, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE112"}, rect=(9, 36, 31, 17)),
        patches=[dict(rect=(2, 0, 1, 1), same_as=(3, 0))] + [p for p, _ in _PRYOR_NOTES],   # the stray cave door -> rock
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_PRYOR",
        connections=[connection("up", "MAP_STRATA_PRAIRIE", -18)],
        objects=[
            # Feral horses: Equus came back with the Spanish, in the 1500s.
            obj("LOCALID_STRATA_PRYOR_HORSE_A", "OBJ_EVENT_GFX_SPECIES(EQUUS)", 14, 12,
                "StrataPryor_EventScript_Horse", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_PRYOR_HORSE_B", "OBJ_EVENT_GFX_SPECIES(EQUUS)", 18, 13,
                "StrataPryor_EventScript_Horse", "MOVEMENT_TYPE_FACE_LEFT"),
            obj("LOCALID_STRATA_PRYOR_HORSE_C", "OBJ_EVENT_GFX_SPECIES(EQUUS)", 26, 10,
                "StrataPryor_EventScript_Horse", "MOVEMENT_TYPE_FACE_DOWN"),
        ],
        bgs=[s for _, s in _PRYOR_NOTES],
        encounters=dict(
            land_mons=mons(("EQUUS", 50, 53), ("EQUUS", 51, 54), ("ANTILOCAPRA", 50, 53), ("EQUUS", 51, 54),
                           ("OVIS", 51, 54), ("CENTROCERCUS", 50, 53), ("CANIS", 50, 53), ("EQUUS", 52, 54),
                           ("ANTILOCAPRA", 52, 54), ("OVIS", 52, 54), ("CENTROCERCUS", 52, 54), ("EQUUS", 53, 54)),
        ),
    ),
    # ------------------------------------------------------------------
    # The Interpretive Center: the Pair on display, and the Hall of Lost Lineages upstairs
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_INTERPRETIVE_1F", name="StrataInterpretive1F", era="ERA_EPILOGUE",
        layout="LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_1F",
        habitat=None, light="dns",
        music="MUS_LILYCOVE_MUSEUM", map_type="MAP_TYPE_INDOOR", mapsec="MAPSEC_STRATA_INTERPRETIVE",
        warps=[
            warp(9, 13, "MAP_STRATA_PRAIRIE", 0), warp(10, 13, "MAP_STRATA_PRAIRIE", 0),   # 0, 1: out to the prairie
            warp(16, 1, "MAP_STRATA_INTERPRETIVE_2F", 0),                                 # 2: the stairs up
        ],
        objects=[
            # Dr. Halvorsen beside the Pair: the final peer review (Lv 55, C13).
            obj("LOCALID_STRATA_CENTER_HALVORSEN", "OBJ_EVENT_GFX_SCIENTIST_1", 14, 8,
                "StrataInterpretive1F_EventScript_Halvorsen", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_CENTER_JOSIE", "OBJ_EVENT_GFX_PICNICKER", 11, 4,
                "StrataInterpretive1F_EventScript_Josie", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_CENTER_BEA", "OBJ_EVENT_GFX_EXPERT_F", 12, 6,
                "StrataInterpretive1F_EventScript_Bea", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_CENTER_DALE", "OBJ_EVENT_GFX_HIKER", 18, 5,
                "StrataInterpretive1F_EventScript_Dale", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_CENTER_THEO", "OBJ_EVENT_GFX_SCIENTIST_2", 3, 8,
                "StrataInterpretive1F_EventScript_Theo", "MOVEMENT_TYPE_FACE_UP"),
        ],
        bgs=[
            # Paleoart murals along the north wall (the stock painting spots), one per layer.
            sign(1, 1, "StrataInterpretive1F_EventScript_MuralHellCreek", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(2, 1, "StrataInterpretive1F_EventScript_MuralHellCreek", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(5, 1, "StrataInterpretive1F_EventScript_MuralGreenRiver", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(6, 1, "StrataInterpretive1F_EventScript_MuralGreenRiver", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(9, 1, "StrataInterpretive1F_EventScript_MuralWhiteRiver", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(11, 1, "StrataInterpretive1F_EventScript_MuralAshfall", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(19, 1, "StrataInterpretive1F_EventScript_MuralIceAge", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(20, 1, "StrataInterpretive1F_EventScript_MuralIceAge", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(2, 6, "StrataInterpretive1F_EventScript_MuralPetm", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(3, 6, "StrataInterpretive1F_EventScript_MuralPetm", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(6, 6, "StrataInterpretive1F_EventScript_MuralCorral", "BG_EVENT_PLAYER_FACING_NORTH"),
            # The Pair, in the round case (the stock "stone tablet" spots).
            sign(16, 9, "StrataInterpretive1F_EventScript_Pair", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(17, 9, "StrataInterpretive1F_EventScript_Pair", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(18, 9, "StrataInterpretive1F_EventScript_PairLabel", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(15, 12, "StrataInterpretive1F_EventScript_Cast"),
            sign(18, 11, "StrataInterpretive1F_EventScript_RigModel"),
        ],
    ),
    dict(
        id="MAP_STRATA_INTERPRETIVE_2F", name="StrataInterpretive2F", era="ERA_EPILOGUE",
        layout="LAYOUT_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F",
        habitat=None, light="dns",
        music="MUS_LILYCOVE_MUSEUM", map_type="MAP_TYPE_INDOOR", mapsec="MAPSEC_STRATA_INTERPRETIVE",
        warps=[warp(13, 1, "MAP_STRATA_INTERPRETIVE_1F", 2)],
        objects=[
            obj("LOCALID_STRATA_HALL_DOCENT", "OBJ_EVENT_GFX_GENTLEMAN", 10, 8,
                "StrataInterpretive2F_EventScript_Docent", "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_HALL_STUDENT", "OBJ_EVENT_GFX_SCHOOL_KID_M", 3, 8,
                "StrataInterpretive2F_EventScript_Student", "MOVEMENT_TYPE_FACE_UP"),
        ],
        bgs=[
            # Five cases, one per extinction filter of the rig, oldest first; the two statues
            # at the door carry the last filter and the one still open.
            sign(2, 6, "StrataInterpretive2F_EventScript_CaseKPg", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(3, 6, "StrataInterpretive2F_EventScript_CaseKPg", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(10, 6, "StrataInterpretive2F_EventScript_CasePaleocene", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(11, 6, "StrataInterpretive2F_EventScript_CasePaleocene", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(18, 6, "StrataInterpretive2F_EventScript_CaseEocene", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(19, 6, "StrataInterpretive2F_EventScript_CaseEocene", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(6, 10, "StrataInterpretive2F_EventScript_CaseMiocene", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(7, 10, "StrataInterpretive2F_EventScript_CaseMiocene", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(14, 10, "StrataInterpretive2F_EventScript_CaseIceAge", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(15, 10, "StrataInterpretive2F_EventScript_CaseIceAge", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(11, 2, "StrataInterpretive2F_EventScript_StatueLast", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(15, 2, "StrataInterpretive2F_EventScript_StatueNow", "BG_EVENT_PLAYER_FACING_NORTH"),
        ],
    ),
]
