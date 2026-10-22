"""Strata map definitions: the single source of truth for Strata map headers,
events and wild encounters.

Run tools/strata/gen_maps.py after editing. See docs/strata_design.md §3.
Map scripts live by hand in data/maps/<Name>/scripts.inc.

Layouts are cut (`crop`) from stock maps with matching terrain, then `patches`
fill rects to remove man-made features, with a block copied from the source map
at `like` (source coords), from the new map at `same_as` (new-map coords), or a
raw `metatile` (+ `collision`, `elevation`). `swap` maps one metatile ID to
another everywhere in the map (see gen_maps.py). Crops taken from adjacent rows
of one stock map join seamlessly, so they can be connected with offset 0.
"""

# Hoenn secret-base entrances in the General primary tileset. They are interactive
# ("make a SECRET BASE here?"), so every Strata map swaps them for the plain rock or
# tree they imitate: rock-mound cave mouths, and the hollow tree trunks.
SECRET_BASE_SWAPS = {0x1A0: 0x079, 0x1A8: 0x071, 0x026: 0x016, 0x027: 0x017}

# Fences, arrow-warp tiles, signposts, doors and the like become plain ground.
GROUND = lambda tile: (tile, 0)  # noqa: E731

MAP_SECTIONS = [
    ("MAPSEC_STRATA_FIELD_CAMP", "HELL CREEK CAMP"),
    ("MAPSEC_STRATA_BADLANDS", "HELL CREEK BADLANDS"),
    ("MAPSEC_STRATA_LEVEE", "LEVEE FOREST"),
    ("MAPSEC_STRATA_RIVER", "RIVER CHANNEL"),
    ("MAPSEC_STRATA_BACKSWAMP", "BACKSWAMP"),
    ("MAPSEC_STRATA_ASHEN_LEVEE", "ASHEN LEVEE"),
    ("MAPSEC_STRATA_ASHEN_RIVER", "ASHEN RIVER"),
    ("MAPSEC_STRATA_ASHEN_SWAMP", "ASHEN SWAMP"),
    ("MAPSEC_STRATA_CORRAL_BLUFFS", "CORRAL BLUFFS"),
    ("MAPSEC_STRATA_BIGHORN", "BIGHORN BASIN"),
    ("MAPSEC_STRATA_GREEN_RIVER", "LAKE GOSIUTE"),
    ("MAPSEC_STRATA_WHITE_RIVER", "WHITE RIVER"),
    ("MAPSEC_STRATA_ASHFALL", "ASHFALL"),
    ("MAPSEC_STRATA_ICE_AGE", "ICE AGE STEPPE"),
    ("MAPSEC_STRATA_TRAP_CAVE", "NATURAL TRAP CAVE"),
    ("MAPSEC_STRATA_PRAIRIE", "MONTANA PRAIRIE"),
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
    dict(rect=(28, 3, 4, 2), metatile=0x001, elevation=3),    # berry-soil plot -> grass
]
RIVER_SWAP = {0x271: 0x270}                                   # secret-base shrub -> plain shrub
BACKSWAMP_CROP = dict(**{"from": "LAYOUT_ROUTE120"}, rect=(0, 25, 40, 17))
IMPACT_WINTER_TILESETS = ("gTileset_GeneralWinter", "gTileset_FortreeWinter")


def winter(crop):
    return dict(**crop, tilesets=IMPACT_WINTER_TILESETS)


def return_edge():
    """The south edge of the Levee, where the player arrives from camp."""
    return [trigger(x, 32, "VAR_TEMP_1", 0, "StrataLevee_EventScript_ReconstructionEdge") for x in (17, 18, 19)]


def anchor(x, y):
    """The edge of a reconstruction: a marker that offers a return to camp."""
    return sign(x, y, "StrataFieldStation_EventScript_Anchor")


# enum StrataEra order (include/constants/strata.h). An act's number is its era.
ERAS = ["ERA_PRESENT_DIG", "ERA_HELL_CREEK", "ERA_IMPACT_WINTER", "ERA_CORRAL_BLUFFS", "ERA_BIGHORN_PETM",
        "ERA_GREEN_RIVER", "ERA_WHITE_RIVER", "ERA_ASHFALL", "ERA_TRAP_CAVE", "ERA_EPILOGUE"]


def story_in_act(era):
    """VAR_STRATA_STORY while the player is in an act (STORY_IN_ACT in C)."""
    return ERAS.index(era) * 2


def boss_triggers(era, script, tiles):
    return [trigger(x, y, "VAR_STRATA_STORY", story_in_act(era), script) for x, y in tiles]


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

    # ------------------------------------------------------------------
    # Act 3: Corral Bluffs, CO (~65.7 Ma): recovering palm and legume forest
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_PALM_FOREST", name="StrataPalmForest", era="ERA_CORRAL_BLUFFS",
        crop=dict(**{"from": "LAYOUT_PETALBURG_WOODS"}, rect=(0, 0, 48, 44)),
        # Petalburg Woods' wooden fences, arrow-warp mats and ledge logs -> plain ground
        swap={0x149: GROUND(0x001), 0x203: GROUND(0x001), 0x204: GROUND(0x001),
              0x087: GROUND(0x001), 0x0D5: GROUND(0x001), 0x0D6: GROUND(0x001)},
        music="MUS_PETALBURG_WOODS", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_CORRAL_BLUFFS",
        arrival=(15, 33),
        bgs=[anchor(14, 32)],
        coords=boss_triggers("ERA_CORRAL_BLUFFS", "StrataPalmForest_EventScript_Eoconodon",
                             [(x, 7) for x in range(31, 37)] + [(x, 7) for x in range(41, 46)]),
        encounters=dict(
            land_mons=mons(("LOXOLOPHUS", 15, 17), ("CARSIOPTYCH", 15, 17), ("MESODMA", 15, 16), ("PURGATORIUS", 15, 17),
                           ("LOXOLOPHUS", 16, 18), ("CARSIOPTYCH", 16, 18), ("PROTICTIS", 16, 18), ("ASTERIORNIS", 16, 18),
                           ("TAENIOLABIS", 17, 19), ("PROTOCHELYD", 17, 19), ("TAENIOLABIS", 18, 20), ("EOCONODON", 18, 20)),
        ),
    ),

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

    # ------------------------------------------------------------------
    # Act 5: Green River lakes, WY (~52-46 Ma): subtropical lake and forest
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_LAKE_FOREST", name="StrataLakeForest", era="ERA_GREEN_RIVER",
        crop=dict(**{"from": "LAYOUT_ROUTE104"}, rect=(0, 0, 40, 80)),
        patches=[
            dict(rect=(3, 14, 7, 5), like=(5, 21)),     # house -> grass
            dict(rect=(24, 9, 2, 8), like=(22, 12)),    # piers -> lake
            dict(rect=(26, 15, 6, 2), like=(22, 12)),
            dict(rect=(30, 17, 2, 5), like=(22, 12)),
            dict(rect=(10, 31, 2, 7), like=(10, 29)),   # path through the forest band
            dict(rect=(14, 46, 6, 5), metatile=0x001, elevation=3),   # cottage -> grass
            dict(rect=(11, 51, 5, 2), like=(9, 52)),    # dock -> lake
            dict(rect=(11, 53, 4, 1), metatile=0x170, elevation=1),
            dict(rect=(2, 22, 3, 5), metatile=0x001, elevation=3),    # berry-soil plots -> grass
            dict(rect=(33, 6, 5, 2), metatile=0x001, elevation=3),
            dict(rect=(21, 41, 5, 2), metatile=0x001, elevation=3),
        ],
        # fences, and the green mats at the ends of the path through the forest band
        swap={0x149: GROUND(0x001), 0x30E: 0x306, 0x30F: 0x306, 0x317: 0x306, 0x307: 0x306},
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_GREEN_RIVER",
        arrival=(5, 17),
        bgs=[anchor(5, 16)],
        coords=boss_triggers("ERA_GREEN_RIVER", "StrataLakeForest_EventScript_Uintatherium", [(x, 61) for x in range(14, 40) if x != 21]),
        encounters=dict(
            land_mons=mons(("EOHIPPUS", 28, 30), ("NOTHARCTUS", 28, 30), ("ONYCHONYCTER", 28, 30), ("HYOPSODUS", 28, 30),
                           ("EOHIPPUS", 29, 31), ("MIACIS", 29, 31), ("GALLINULOID", 29, 31), ("DIACODEXIS", 29, 31),
                           ("NOTHARCTUS", 30, 32), ("PRESBYORNIS", 30, 32), ("CORYPHODON", 31, 33), ("UINTATHERIUM", 32, 33)),
            water_mons=mons(("KNIGHTIA", 28, 32), ("HELIOBATIS", 28, 32), ("PRESBYORNIS", 29, 33),
                            ("BOREALOSUCH", 30, 33), ("CHAMPSOSAUR", 30, 34)),
            fishing_mons=mons(("KNIGHTIA", 26, 29), ("KNIGHTIA", 26, 29), ("KNIGHTIA", 27, 30), ("LEPISOSTEUS", 27, 30),
                              ("HELIOBATIS", 28, 31), ("LEPISOSTEUS", 28, 31), ("HELIOBATIS", 29, 32), ("LEPISOSTEUS", 29, 32),
                              ("HELIOBATIS", 30, 33), ("BOREALOSUCH", 31, 34)),
        ),
    ),

    # ------------------------------------------------------------------
    # Act 6: White River badlands, SD/NE (~33 Ma): cooler, drier open woodland
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_WHITE_RIVER", name="StrataWhiteRiver", era="ERA_WHITE_RIVER",
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 37, 40, 43), tilesets=("gTileset_GeneralOligocene", "gTileset_FallarborOligocene")),
        patches=[
            dict(rect=(31, 5, 2, 5), metatile=0x001, elevation=3),    # berry-soil plot -> grass
        ],
        # secret-base rock spots and a cave door -> plain rock
        swap={0x208: 0x241, 0x259: 0x265, 0x261: (0x265, 1)},
        music="MUS_ROUTE110", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_WHITE_RIVER",
        arrival=(17, 3),
        bgs=[anchor(17, 4)],
        coords=boss_triggers("ERA_WHITE_RIVER", "StrataWhiteRiver_EventScript_Archaeotherium",
                             [(13, 32), (14, 32), (24, 34), (25, 34)]),
        encounters=dict(
            land_mons=mons(("MESOHIPPUS", 34, 36), ("MERYCOIDODON", 34, 36), ("LEPTOMERYX", 34, 36), ("ISCHYROMYS", 34, 36),
                           ("MERYCOIDODON", 35, 37), ("STYLEMYS", 35, 37), ("POEBROTHERE", 35, 37), ("HESPEROCYON", 35, 37),
                           ("MESOHIPPUS", 36, 38), ("SUBHYRACODON", 36, 38), ("HOPLOPHONEUS", 37, 39), ("ARCHAEOTHERE", 38, 39)),
        ),
    ),

    # ------------------------------------------------------------------
    # Act 7: Ashfall, NE (~11.9 Ma): a grassland waterhole under volcanic ash
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_GRASSLAND", name="StrataGrassland", era="ERA_ASHFALL",
        crop=dict(**{"from": "LAYOUT_ROUTE113"}, rect=(15, 0, 85, 20)),
        patches=[
            dict(rect=(16, 1, 6, 5), like=(37, 6)),     # house -> ash plain
        ],
        music="MUS_ROUTE113", weather="WEATHER_VOLCANIC_ASH", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_ASHFALL",
        arrival=(5, 11),
        bgs=[anchor(5, 12)],
        coords=boss_triggers("ERA_ASHFALL", "StrataGrassland_EventScript_Teleoceras", [(70, y) for y in range(7, 12)]),
        encounters=dict(
            land_mons=mons(("PROTOHIPPUS", 40, 42), ("PROCAMELUS", 40, 42), ("LEPTOCYON", 40, 42), ("BALEARICA", 40, 42),
                           ("PROTOHIPPUS", 41, 43), ("GALLINULOID", 41, 43), ("PROCAMELUS", 41, 43), ("ANCHIGYPS", 41, 43),
                           ("TELEOCERAS", 42, 44), ("CHELYDRA", 42, 44), ("EPICYON", 43, 45), ("TELEOCERAS", 43, 45)),
        ),
    ),

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

    # ------------------------------------------------------------------
    # Epilogue: the Montana prairie today, open only once the present is loaded
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_PRAIRIE", name="StrataPrairie", era="ERA_EPILOGUE",
        crop=dict(**{"from": "LAYOUT_ROUTE102"}, rect=(0, 0, 50, 20)),
        patches=[
            dict(rect=(23, 2, 4, 2), metatile=0x001, elevation=3),    # berry-soil plot -> grass
        ],
        music="MUS_ROUTE101", weather="WEATHER_SUNNY", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_PRAIRIE",
        arrival=(2, 9),
        bgs=[sign(2, 10, "StrataPrairie_EventScript_TrailToCamp")],
        encounters=dict(
            land_mons=mons(("CYNOMYS", 48, 50), ("ANTILOCAPRA", 48, 50), ("CYNOMYS", 48, 50), ("CANIS", 48, 50),
                           ("MELEAGRIS", 49, 51), ("ANTILOCAPRA", 49, 51), ("BISON", 49, 51), ("OVIS", 49, 51),
                           ("CANIS", 50, 52), ("BISON", 50, 52), ("EQUUS", 50, 52), ("OVIBOS", 50, 52)),
            water_mons=mons(("CHELYDRA", 48, 52), ("LEPISOSTEUS", 48, 52), ("CHELYDRA", 49, 52),
                            ("LEPISOSTEUS", 50, 53), ("CHELYDRA", 51, 53)),
            fishing_mons=mons(("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 46, 49), ("LEPISOSTEUS", 47, 50), ("CHELYDRA", 47, 50),
                              ("LEPISOSTEUS", 48, 51), ("CHELYDRA", 48, 51), ("LEPISOSTEUS", 49, 52), ("CHELYDRA", 49, 52),
                              ("CHELYDRA", 50, 53), ("CHELYDRA", 51, 54)),
        ),
    ),
]
