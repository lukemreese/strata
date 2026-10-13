"""Strata map definitions: the single source of truth for Strata map headers,
events and wild encounters.

Run tools/strata/gen_maps.py after editing. See docs/strata_design.md §3.
Map scripts live by hand in data/maps/<Name>/scripts.inc.

Layouts are cut (`crop`) from stock maps with matching terrain, then `patches`
fill rects with a block copied from the source map at `like` (source coords) to
remove man-made features. Crops taken from adjacent rows of one stock map join
seamlessly, so they can be connected with offset 0.
"""

MAP_SECTIONS = [
    ("MAPSEC_STRATA_FIELD_CAMP", "HELL CREEK CAMP"),
    ("MAPSEC_STRATA_BADLANDS", "HELL CREEK BADLANDS"),
    ("MAPSEC_STRATA_LEVEE", "LEVEE FOREST"),
    ("MAPSEC_STRATA_RIVER", "RIVER CHANNEL"),
    ("MAPSEC_STRATA_BACKSWAMP", "BACKSWAMP"),
    ("MAPSEC_STRATA_ASHEN_LEVEE", "ASHEN LEVEE"),
    ("MAPSEC_STRATA_ASHEN_RIVER", "ASHEN RIVER"),
    ("MAPSEC_STRATA_ASHEN_SWAMP", "ASHEN SWAMP"),
]

HEAL_LOCATIONS = [
    dict(id="HEAL_LOCATION_STRATA_FIELD_CAMP", map="MAP_STRATA_FIELD_CAMP", x=26, y=19,
         respawn_map="MAP_STRATA_FIELD_STATION", respawn_npc="LOCALID_STRATA_MENTOR"),
]


def obj(local_id, gfx, x, y, script, movement="MOVEMENT_TYPE_FACE_DOWN", flag="0", elevation=3):
    return {
        "local_id": local_id, "graphics_id": gfx, "x": x, "y": y, "elevation": elevation,
        "movement_type": movement, "movement_range_x": 1, "movement_range_y": 1,
        "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
        "script": script, "flag": flag,
    }


def warp(x, y, dest_map, dest_warp_id, elevation=0):
    return {"x": x, "y": y, "elevation": elevation, "dest_map": dest_map, "dest_warp_id": str(dest_warp_id)}


def sign(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": facing, "script": script}


def trigger(x, y, var, value, script, elevation=None):
    """elevation None takes the elevation of the tile, see gen_maps.py."""
    return {"type": "trigger", "x": x, "y": y, "elevation": elevation, "var": var,
            "var_value": str(value), "script": script}


def connection(direction, dest, offset=0):
    return {"map": dest, "offset": offset, "direction": direction}


# Hell Creek's footprint, shared by every era built on it. Same layout, different
# tilesets: the place stays put while time moves on.
LEVEE_CROP = dict(**{"from": "LAYOUT_ROUTE119"}, rect=(0, 107, 40, 33))
LEVEE_PATCHES = [dict(rect=(31, 0, 6, 3), like=(36, 111))]   # house -> grass
RIVER_CROP = dict(**{"from": "LAYOUT_ROUTE119"}, rect=(0, 86, 40, 21))
RIVER_PATCHES = [
    dict(rect=(17, 4, 9, 6), like=(20, 100)),                 # wooden docks -> river
    dict(rect=(31, 18, 6, 3), like=(36, 111)),                # house -> grass
]
BACKSWAMP_CROP = dict(**{"from": "LAYOUT_ROUTE120"}, rect=(0, 25, 40, 17))
IMPACT_WINTER_TILESETS = ("gTileset_GeneralWinter", "gTileset_FortreeWinter")


def winter(crop):
    return dict(**crop, tilesets=IMPACT_WINTER_TILESETS)


def return_edge():
    """The south edge of the Levee, where the player arrives from camp."""
    return [trigger(x, 32, "VAR_TEMP_1", 0, "StrataLevee_EventScript_ReconstructionEdge") for x in (17, 18, 19)]


def mons(*entries):
    """(species, min_level, max_level) per encounter slot."""
    return [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s} for s, lo, hi in entries]


MAPS = [
    # ------------------------------------------------------------------
    # Present day (Act 0): Hell Creek, Garfield County, Montana
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_FIELD_CAMP", name="StrataFieldCamp",
        crop=dict(**{"from": "LAYOUT_ROUTE111"}, rect=(0, 0, 40, 34)),
        music="MUS_ROUTE113", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE",
        mapsec="MAPSEC_STRATA_FIELD_CAMP",
        connections=[connection("down", "MAP_STRATA_BADLANDS")],
        warps=[warp(26, 18, "MAP_STRATA_FIELD_STATION", 0)],
        objects=[
            obj("LOCALID_STRATA_CAMP_CREW", "OBJ_EVENT_GFX_HIKER", 18, 9,
                "StrataFieldCamp_EventScript_Crew", "MOVEMENT_TYPE_WANDER_AROUND"),
            obj("LOCALID_STRATA_CAMP_STUDENT", "OBJ_EVENT_GFX_PICNICKER", 22, 11,
                "StrataFieldCamp_EventScript_Student", "MOVEMENT_TYPE_LOOK_AROUND"),
        ],
        bgs=[
            sign(13, 6, "StrataFieldCamp_EventScript_CampSign"),
            sign(25, 19, "StrataFieldCamp_EventScript_StationSign"),
        ],
    ),
    dict(
        id="MAP_STRATA_FIELD_STATION", name="StrataFieldStation",
        layout="LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB",
        music="MUS_BIRCH_LAB", map_type="MAP_TYPE_INDOOR",
        mapsec="MAPSEC_STRATA_FIELD_CAMP",
        warps=[warp(6, 12, "MAP_STRATA_FIELD_CAMP", 0), warp(7, 12, "MAP_STRATA_FIELD_CAMP", 0)],
        objects=[
            obj("LOCALID_STRATA_MENTOR", "OBJ_EVENT_GFX_SCIENTIST_1", 6, 5,
                "StrataFieldStation_EventScript_Mentor"),
        ],
        bgs=[
            sign(10, 7, "StrataFieldStation_EventScript_Rig", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(11, 7, "StrataFieldStation_EventScript_Rig", "BG_EVENT_PLAYER_FACING_NORTH"),
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

    # ------------------------------------------------------------------
    # Hell Creek, 66.04 Ma (Act 1)
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LEVEE", name="StrataLevee",
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
        id="MAP_STRATA_RIVER", name="StrataRiver",
        crop=RIVER_CROP, patches=RIVER_PATCHES,
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
        id="MAP_STRATA_BACKSWAMP", name="StrataBackswamp",
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

    # ------------------------------------------------------------------
    # Hell Creek, ~1 year after the Chicxulub impact (Act 2): the same
    # place, soot-darkened and ash-covered. Only the survivors remain.
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LEVEE_WINTER", name="StrataLeveeWinter",
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
        id="MAP_STRATA_RIVER_WINTER", name="StrataRiverWinter",
        crop=winter(RIVER_CROP), patches=RIVER_PATCHES,
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
        id="MAP_STRATA_BACKSWAMP_WINTER", name="StrataBackswampWinter",
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
