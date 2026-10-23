"""Act 0: the present day (Hell Creek field camp, station, badlands).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_FIELD_CAMP", "HELL CREEK CAMP"),
    ("MAPSEC_STRATA_BADLANDS", "HELL CREEK BADLANDS"),
]

HEAL_LOCATIONS = [
    dict(id="HEAL_LOCATION_STRATA_FIELD_CAMP", map="MAP_STRATA_FIELD_CAMP", x=26, y=19,
         respawn_map="MAP_STRATA_FIELD_STATION", respawn_npc="LOCALID_STRATA_MENTOR"),
]

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
        ],
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_FIELD_CAMP",
        connections=[connection("down", "MAP_STRATA_BADLANDS")],
        warps=[warp(26, 18, "MAP_STRATA_FIELD_STATION", 0)],
        coords=[
            # The ranch road west to the prairie, open once the present is loaded.
            trigger(1, y, "VAR_TEMP_1", 0, "StrataFieldCamp_EventScript_PrairieRoad") for y in range(7, 11)
        ],
        objects=[
            obj("LOCALID_STRATA_CAMP_CREW", "OBJ_EVENT_GFX_HIKER", 18, 9,
                "StrataFieldCamp_EventScript_Crew", "MOVEMENT_TYPE_WANDER_AROUND"),
            obj("LOCALID_STRATA_CAMP_STUDENT", "OBJ_EVENT_GFX_PICNICKER", 22, 11,
                "StrataFieldCamp_EventScript_Student", "MOVEMENT_TYPE_LOOK_AROUND"),
            # The camp store: the quartermaster, parked beside the station door.
            obj("LOCALID_STRATA_CAMP_QUARTERMASTER", "OBJ_EVENT_GFX_WORKER_M", 29, 19,
                "StrataFieldCamp_EventScript_Quartermaster", "MOVEMENT_TYPE_FACE_LEFT"),
        ],
        bgs=[
            sign(13, 6, "StrataFieldCamp_EventScript_CampSign"),
            sign(25, 19, "StrataFieldCamp_EventScript_StationSign"),
        ],
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
        ],
    ),
    dict(
        id="MAP_STRATA_BADLANDS", name="StrataBadlands",
        crop=dict(**{"from": "LAYOUT_ROUTE111"}, rect=(0, 34, 40, 40)),
        patches=[
            dict(rect=(17, 17, 5, 9), like=(24, 49)),  # Mirage Tower -> sand
        ],
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_BADLANDS",
        connections=[connection("up", "MAP_STRATA_FIELD_CAMP")],
        objects=[
            obj("LOCALID_STRATA_BADLANDS_DIGGER", "OBJ_EVENT_GFX_HIKER", 24, 12,
                "StrataBadlands_EventScript_Digger", "MOVEMENT_TYPE_FACE_LEFT"),
        ],
        bgs=[
            sign(7, 32, "StrataBadlands_EventScript_BoundarySign"),
        ],
    ),
]
