"""Act 0: the present day (Hell Creek field camp, station, badlands, and the hub
around them: Jordan, the Lindqvist Ranch and Sand Arroyo).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The hub, west to east and north to south:

    Jordan (town) -- Lindqvist Ranch -- Hell Creek Camp (field station inside)
                                              |
                                        Hell Creek Badlands (tutorial dig)
                                              |  BLM boundary: permit needed
                                        Sand Arroyo (BLM land, the poached pit)

Jordan's west edge is the highway out of town: it leads to the epilogue prairie once
the present layer is loaded.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_FIELD_CAMP", "HELL CREEK CAMP"),
    ("MAPSEC_STRATA_BADLANDS", "HELL CREEK BADLANDS"),
    ("MAPSEC_STRATA_JORDAN", "JORDAN"),
    ("MAPSEC_STRATA_LINDQVIST_RANCH", "LINDQVIST RANCH"),
    ("MAPSEC_STRATA_SAND_ARROYO", "SAND ARROYO"),
]

HEAL_LOCATIONS = [
    dict(id="HEAL_LOCATION_STRATA_FIELD_CAMP", map="MAP_STRATA_FIELD_CAMP", x=26, y=19,
         respawn_map="MAP_STRATA_FIELD_STATION", respawn_npc="LOCALID_STRATA_MENTOR"),
]

# General primary tileset: the wooden signpost. A field-note sign on open ground gets
# this metatile, so the player can see there is something to read.
SIGNPOST = 0x01B


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), sign(x, y, script, facing)


def edge_triggers(x, ys, script):
    """Coord triggers along a map edge (VAR_TEMP_1 == 0: the map's scripts set it to
    1 to open the way)."""
    return [trigger(x, y, "VAR_TEMP_1", 0, script) for y in ys]


# Field-note signposts placed on open ground (patch + sign pairs).
_CAMP_NOTES = [signpost(11, 7, "StrataFieldCamp_EventScript_SuperpositionNote"),
               signpost(19, 5, "StrataFieldCamp_EventScript_ResearcherBoard")]
_BADLANDS_NOTES = [signpost(12, 5, "StrataBadlands_EventScript_FormationNote"),
                   signpost(22, 37, "StrataBadlands_EventScript_BlmBoundary")]
# Tutorial dig: survey stakes at the three specimen sites.
_DIG_STAKES = [signpost(14, 20, "StrataBadlands_EventScript_StakeJaw"),
               signpost(30, 16, "StrataBadlands_EventScript_StakeBird"),
               signpost(25, 28, "StrataBadlands_EventScript_StakeShell")]

# The badlands' south edge is the BLM boundary: walkable tiles of the bottom row.
_BLM_EDGE = [(x, 39) for x in list(range(9, 16)) + list(range(22, 38))]

MAPS = [
    # ------------------------------------------------------------------
    # Present day (Act 0): Hell Creek, Garfield County, Montana
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_FIELD_CAMP", name="StrataFieldCamp",
        crop=dict(**{"from": "LAYOUT_ROUTE111"}, rect=(0, 0, 40, 34)),
        patches=[
            dict(rect=(17, 5, 8, 2), metatile=0x001, elevation=3),    # two berry-soil plots -> grass
            dict(rect=(29, 16, 3, 3), metatile=0x001, elevation=3),   # the house's pale lawn -> grass
        ] + [p for p, _ in _CAMP_NOTES],
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_FIELD_CAMP",
        # The ranch road west (rows 7-10) runs on to the Lindqvist Ranch.
        connections=[connection("down", "MAP_STRATA_BADLANDS"),
                     connection("left", "MAP_STRATA_LINDQVIST_RANCH", -1)],
        warps=[warp(26, 18, "MAP_STRATA_FIELD_STATION", 0)],
        objects=[
            # Theo Okafor, PhD student and the rival (peer review starts with C13).
            obj("LOCALID_STRATA_CAMP_THEO", "OBJ_EVENT_GFX_SCIENTIST_2", 18, 9,
                "StrataFieldCamp_EventScript_Theo", "MOVEMENT_TYPE_WANDER_AROUND"),
            # Josie Lindqvist, undergrad on the crew (the camp "Student").
            obj("LOCALID_STRATA_CAMP_STUDENT", "OBJ_EVENT_GFX_PICNICKER", 22, 11,
                "StrataFieldCamp_EventScript_Student", "MOVEMENT_TYPE_LOOK_AROUND"),
            # The camp store: the quartermaster, parked beside the station door.
            obj("LOCALID_STRATA_CAMP_QUARTERMASTER", "OBJ_EVENT_GFX_WORKER_M", 29, 19,
                "StrataFieldCamp_EventScript_Quartermaster", "MOVEMENT_TYPE_FACE_LEFT"),
        ],
        bgs=[
            sign(13, 6, "StrataFieldCamp_EventScript_CampSign"),
            sign(25, 19, "StrataFieldCamp_EventScript_StationSign"),
        ] + [s for _, s in _CAMP_NOTES],
    ),
    dict(
        id="MAP_STRATA_FIELD_STATION", name="StrataFieldStation",
        crop=dict(**{"from": "LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB"}, rect=(0, 0, 13, 13)),
        patches=[
            # The healing cot: a pair of the lab's orange-blanket couch tiles in the west aisle.
            dict(at=(1, 4), tiles=[[0x274, 0x275]], collision=1),
        ],
        music="MUS_BIRCH_LAB", map_type="MAP_TYPE_INDOOR",
        mapsec="MAPSEC_STRATA_FIELD_CAMP",
        warps=[warp(6, 12, "MAP_STRATA_FIELD_CAMP", 0), warp(7, 12, "MAP_STRATA_FIELD_CAMP", 0)],
        objects=[
            obj("LOCALID_STRATA_MENTOR", "OBJ_EVENT_GFX_SCIENTIST_1", 6, 5,
                "StrataFieldStation_EventScript_Mentor"),
            obj("LOCALID_STRATA_RELEARNER", "OBJ_EVENT_GFX_WORKER_F", 9, 3,
                "StrataFieldStation_EventScript_Relearner"),
        ],
        bgs=[
            sign(10, 7, "StrataFieldStation_EventScript_Rig", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(11, 7, "StrataFieldStation_EventScript_Rig", "BG_EVENT_PLAYER_FACING_NORTH"),
            # The specimen database: the lab's desk computers (the PC behind the desk at (3, 1) and (4, 1)).
            sign(3, 1, "StrataFieldStation_EventScript_PC", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(4, 1, "StrataFieldStation_EventScript_PC", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(1, 4, "StrataFieldStation_EventScript_Cot"),
            sign(2, 4, "StrataFieldStation_EventScript_Cot"),
            # The rig's rules, pinned up over the back desk (outline §1.2).
            sign(7, 1, "StrataFieldStation_EventScript_RigRules", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(8, 1, "StrataFieldStation_EventScript_RigRules", "BG_EVENT_PLAYER_FACING_NORTH"),
        ],
    ),
    dict(
        id="MAP_STRATA_BADLANDS", name="StrataBadlands",
        crop=dict(**{"from": "LAYOUT_ROUTE111"}, rect=(0, 34, 40, 40)),
        patches=[
            dict(rect=(17, 17, 5, 9), like=(24, 49)),  # Mirage Tower -> sand
        ] + [p for p, _ in _BADLANDS_NOTES + _DIG_STAKES],
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_BADLANDS",
        # Rows 74+ of Route 111 continue south as Sand Arroyo, so the join is seamless.
        connections=[connection("up", "MAP_STRATA_FIELD_CAMP"),
                     connection("down", "MAP_STRATA_SAND_ARROYO")],
        coords=[trigger(x, y, "VAR_TEMP_1", 0, "StrataBadlands_EventScript_BlmFence") for x, y in _BLM_EDGE],
        objects=[
            # Dale Brekke, crew chief: runs the tutorial dig.
            obj("LOCALID_STRATA_BADLANDS_DIGGER", "OBJ_EVENT_GFX_HIKER", 24, 12,
                "StrataBadlands_EventScript_Digger", "MOVEMENT_TYPE_FACE_LEFT"),
        ],
        bgs=[
            sign(7, 32, "StrataBadlands_EventScript_BoundarySign"),
        ] + [s for _, s in _BADLANDS_NOTES + _DIG_STAKES],
    ),
    # ------------------------------------------------------------------
    # Jordan, the county seat: general store, café, BLM field office
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_JORDAN", name="StrataJordan",
        crop=dict(**{"from": "LAYOUT_FALLARBOR_TOWN"}, rect=(0, 0, 20, 20)),
        patches=[
            # The Battle Tent: cliff behind, plain ground in front.
            dict(rect=(4, 3, 7, 2), like=(8, 2)),
            dict(rect=(4, 5, 8, 1), like=(11, 5)),
            dict(rect=(5, 6, 7, 2), like=(4, 6)),
            # The Pokémon Center, the same way.
            dict(rect=(13, 4, 4, 1), like=(14, 3)),
            dict(rect=(13, 5, 4, 1), like=(11, 5)),
            dict(rect=(13, 6, 4, 2), like=(12, 7)),
        ],
        music="MUS_FALLARBOR", weather="WEATHER_SUNNY", map_type="MAP_TYPE_TOWN",
        mapsec="MAPSEC_STRATA_JORDAN",
        connections=[connection("right", "MAP_STRATA_LINDQVIST_RANCH")],
        warps=[
            warp(15, 15, "MAP_STRATA_JORDAN_STORE", 0),   # 0: the mart -> general store
            warp(6, 17, "MAP_STRATA_JORDAN_CAFE", 0),     # 1: Cozmo's house -> café
            warp(1, 6, "MAP_STRATA_BLM_OFFICE", 0),       # 2: the tutor's house -> BLM field office
        ],
        # The highway west: to the prairie once the present layer is loaded.
        coords=edge_triggers(0, range(7, 18), "StrataJordan_EventScript_Highway"),
        objects=[
            obj("LOCALID_STRATA_JORDAN_RANCHER", "OBJ_EVENT_GFX_OLD_MAN", 11, 13,
                "StrataJordan_EventScript_Rancher", "MOVEMENT_TYPE_FACE_LEFT"),
            obj("LOCALID_STRATA_JORDAN_LOCAL", "OBJ_EVENT_GFX_WOMAN_2", 8, 11,
                "StrataJordan_EventScript_Local", "MOVEMENT_TYPE_WANDER_AROUND"),
        ],
        bgs=[
            sign(10, 11, "StrataJordan_EventScript_TownSign"),
            sign(3, 7, "StrataJordan_EventScript_OfficeSign"),
            sign(6, 8, "StrataJordan_EventScript_LawNote"),
        ],
    ),
    dict(
        id="MAP_STRATA_JORDAN_STORE", name="StrataJordanStore", layout="LAYOUT_MART",
        music="MUS_FALLARBOR", map_type="MAP_TYPE_INDOOR", mapsec="MAPSEC_STRATA_JORDAN",
        warps=[warp(3, 7, "MAP_STRATA_JORDAN", 0), warp(4, 7, "MAP_STRATA_JORDAN", 0)],
        objects=[
            obj("LOCALID_STRATA_STORE_CLERK", "OBJ_EVENT_GFX_MART_EMPLOYEE", 1, 3,
                "StrataJordanStore_EventScript_Clerk", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_STORE_SHOPPER", "OBJ_EVENT_GFX_POKEFAN_M", 9, 6,
                "StrataJordanStore_EventScript_Shopper", "MOVEMENT_TYPE_FACE_UP"),
        ],
    ),
    dict(
        id="MAP_STRATA_JORDAN_CAFE", name="StrataJordanCafe", layout="LAYOUT_HOUSE2",
        music="MUS_FALLARBOR", map_type="MAP_TYPE_INDOOR", mapsec="MAPSEC_STRATA_JORDAN",
        warps=[warp(3, 7, "MAP_STRATA_JORDAN", 1), warp(4, 7, "MAP_STRATA_JORDAN", 1)],
        objects=[
            obj("LOCALID_STRATA_CAFE_OWNER", "OBJ_EVENT_GFX_WOMAN_5", 8, 2,
                "StrataJordanCafe_EventScript_Owner"),
            obj("LOCALID_STRATA_CAFE_OLDTIMER", "OBJ_EVENT_GFX_MAN_4", 4, 4,
                "StrataJordanCafe_EventScript_OldTimer", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_CAFE_TOURIST", "OBJ_EVENT_GFX_FISHERMAN", 7, 4,
                "StrataJordanCafe_EventScript_Tourist", "MOVEMENT_TYPE_FACE_LEFT"),
        ],
    ),
    dict(
        id="MAP_STRATA_BLM_OFFICE", name="StrataBlmOffice", layout="LAYOUT_ROUTE114_LANETTES_HOUSE",
        music="MUS_FALLARBOR", map_type="MAP_TYPE_INDOOR", mapsec="MAPSEC_STRATA_JORDAN",
        warps=[warp(5, 7, "MAP_STRATA_JORDAN", 2), warp(6, 7, "MAP_STRATA_JORDAN", 2)],
        objects=[
            # Ranger Lucia Ortiz, BLM paleontology / law-enforcement ranger.
            obj("LOCALID_STRATA_RANGER", "OBJ_EVENT_GFX_POLICEMAN", 5, 4,
                "StrataBlmOffice_EventScript_Ranger"),
        ],
        bgs=[
            sign(5, 1, "StrataBlmOffice_EventScript_Binder", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(7, 1, "StrataBlmOffice_EventScript_Map", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(8, 1, "StrataBlmOffice_EventScript_Map", "BG_EVENT_PLAYER_FACING_NORTH"),
        ],
    ),
    # ------------------------------------------------------------------
    # The Lindqvist Ranch: Bea's land, where the Pair lies under a tarp
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LINDQVIST_RANCH", name="StrataLindqvistRanch",
        crop=dict(**{"from": "LAYOUT_ROUTE117"}, rect=(0, 0, 60, 20)),
        music="MUS_ROUTE110", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_LINDQVIST_RANCH",
        connections=[connection("left", "MAP_STRATA_JORDAN"),
                     connection("right", "MAP_STRATA_FIELD_CAMP", 1)],
        objects=[
            # Bea Lindqvist, who owns the land; Wade Kessler pitching her (until Act 1 is done).
            obj("LOCALID_STRATA_RANCH_BEA", "OBJ_EVENT_GFX_EXPERT_F", 46, 7,
                "StrataLindqvistRanch_EventScript_Bea", "MOVEMENT_TYPE_FACE_RIGHT"),
            obj("LOCALID_STRATA_RANCH_KESSLER", "OBJ_EVENT_GFX_GENTLEMAN", 47, 7,
                "StrataLindqvistRanch_EventScript_Kessler", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_TEMP_1F"),
            # One of Kessler's crew, waiting by the gate.
            obj("LOCALID_STRATA_RANCH_HAND", "OBJ_EVENT_GFX_MANIAC", 55, 8,
                "StrataLindqvistRanch_EventScript_KesslerHand", "MOVEMENT_TYPE_LOOK_AROUND", flag="FLAG_TEMP_1F"),
        ],
        bgs=[
            sign(49, 5, "StrataLindqvistRanch_EventScript_RanchSign"),
            sign(51, 5, "StrataLindqvistRanch_EventScript_HouseDoor", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(16, 6, "StrataLindqvistRanch_EventScript_SplitEstateNote"),
            sign(49, 12, "StrataLindqvistRanch_EventScript_DroughtNote"),
            # The Pair's quarry: the bare plot inside the cottonwood ring, under a tarp.
            sign(42, 13, "StrataLindqvistRanch_EventScript_Tarp", "BG_EVENT_PLAYER_FACING_NORTH"),
        ],
    ),
    # ------------------------------------------------------------------
    # Sand Arroyo: BLM land south of the badlands, where someone dug a pit
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_SAND_ARROYO", name="StrataSandArroyo",
        crop=dict(**{"from": "LAYOUT_ROUTE111"}, rect=(0, 74, 40, 27)),
        patches=[
            # The Desert Ruins door stays as the poached pit, but nothing walks into it.
            dict(at=(29, 13), tiles=[[0x0A7]], collision=1),
            # Close the two gaps in the bottom row (Route 111 runs on south).
            dict(rect=(18, 26, 2, 1), like=(14, 100)),
            dict(rect=(30, 26, 3, 1), like=(14, 100)),
            dict(at=(31, 15), tiles=[[0x24B, 0x24C]], collision=1),   # a rock: the pit's spoil heap
        ],
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_SAND_ARROYO",
        connections=[connection("up", "MAP_STRATA_BADLANDS")],
        objects=[
            # A plaster field jacket, cracked open and left behind.
            obj("LOCALID_STRATA_ARROYO_JACKET", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 27, 15,
                "StrataSandArroyo_EventScript_Jacket"),
        ],
        bgs=[
            sign(7, 10, "StrataSandArroyo_EventScript_ContextNote"),
            sign(29, 13, "StrataSandArroyo_EventScript_Pit", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(31, 15, "StrataSandArroyo_EventScript_Spoil"),
        ],
    ),
]
