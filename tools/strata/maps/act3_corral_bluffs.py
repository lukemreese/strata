"""Act 3: Corral Bluffs, CO (~65.7-65.4 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

Four maps (outline 2.4), joined at the Palm Forest hub:

    Palm Forest (48x44)  --up-->     Front Range Creek (40x25, Route 119 upper river)
                         --left-->   Legume Thicket    (25x33, Route 120 thicket) + the boss
                         --right-->  Concretion Bluffs (60x20, Route 116)
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_CORRAL_BLUFFS", "CORRAL BLUFFS"),
    ("MAPSEC_STRATA_LEGUME_THICKET", "LEGUME THICKET"),
    ("MAPSEC_STRATA_CONCRETION_BLUFFS", "CONCRETION BLUFFS"),
    ("MAPSEC_STRATA_FRONT_RANGE_CREEK", "FRONT RANGE CREEK"),
]

# Map events are assembled in data/maps.s, which does not see constants/strata.h, so the
# act's flags are numbers here: FLAG_STRATA_ACT3_BASE + n (include/constants/strata_act_flags.h,
# 0 CONCRETION_1, 1 CONCRETION_2, 2 CONCRETION_3, 3 TAENIOLABIS_DONE, 4 EOCONODON_GONE).
def a3_flag(n):
    return f"0x{0x274 + n:X}"


# A wooden signpost (General tileset 0x01B, impassable) for a field note. The generator
# draws every other stock signpost as plain ground, so a note's tile is patched in.
def signpost(x, y):
    return dict(rect=(x, y, 1, 1), metatile=0x01B, collision=1)


MAPS = [
    # ------------------------------------------------------------------
    # Act 3: Corral Bluffs, CO (~65.7-65.4 Ma, 300-700 kyr after the impact): recovering palm and legume forest
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_PALM_FOREST", name="StrataPalmForest", era="ERA_CORRAL_BLUFFS",
        habitat="forest", light="day",
        forage=[forage(6, 10, "PALM_FRUIT"), forage(20, 18, "PALM_FRUIT"),
                forage(44, 6, "PALM_FRUIT"), forage(8, 30, "FERN_FROND"), forage(40, 34, "LARVAE")],
        crop=dict(**{"from": "LAYOUT_PETALBURG_WOODS"}, rect=(0, 0, 48, 44)),
        patches=[
            dict(rect=(13, 0, 3, 5), same_as=(13, 6)),    # north opening: up to the creek
            dict(rect=(0, 16, 4, 2), same_as=(4, 16)),    # west opening: the thicket
            dict(rect=(46, 24, 2, 2), same_as=(45, 24)),  # east opening: the bluffs
            signpost(20, 26), signpost(40, 12),
        ],
        # Petalburg Woods' wooden fences, arrow-warp mats and ledge logs -> plain ground
        swap={0x149: GROUND(0x001), 0x203: GROUND(0x001), 0x204: GROUND(0x001),
              0x087: GROUND(0x001), 0x0D5: GROUND(0x001), 0x0D6: GROUND(0x001)},
        music="MUS_PETALBURG_WOODS", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_CORRAL_BLUFFS",
        arrival=(15, 33),
        connections=[connection("up", "MAP_STRATA_FRONT_RANGE_CREEK", 8),
                     connection("left", "MAP_STRATA_LEGUME_THICKET", -10),
                     connection("right", "MAP_STRATA_CONCRETION_BLUFFS", 15)],
        bgs=[anchor(14, 32),
             sign(11, 8, "StrataPalmForest_EventScript_NotePalms"),
             sign(20, 26, "StrataPalmForest_EventScript_NoteDating"),
             sign(40, 12, "StrataPalmForest_EventScript_NoteFruit")],
        encounters=dict(
            land_mons=mons(("LOXOLOPHUS", 14, 15), ("CARSIOPTYCH", 14, 15), ("MESODMA", 14, 15), ("PURGATORIUS", 14, 16),
                           ("LOXOLOPHUS", 15, 16), ("CARSIOPTYCH", 15, 16), ("PROTICTIS", 15, 17), ("ASTERIORNIS", 15, 17),
                           ("PURGATORIUS", 16, 17), ("MESODMA", 16, 17), ("PROTICTIS", 16, 17), ("LOXOLOPHUS", 16, 17)),
        ),
    ),
    # The thicket: the marsh at its north end is where the Eoconodon feeds (boss).
    dict(
        id="MAP_STRATA_LEGUME_THICKET", name="StrataLegumeThicket", era="ERA_CORRAL_BLUFFS",
        habitat="forest", light="day",
        forage=[forage(8, 20, "LEGUME_POD"), forage(16, 26, "LEGUME_POD"), forage(5, 30, "LEGUME_POD"),
                forage(20, 15, "LARVAE"), forage(3, 8, "FERN_FROND"), forage(12, 9, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE120"}, rect=(15, 26, 25, 33)),
        patches=[signpost(21, 24), signpost(14, 11), signpost(8, 10)],
        music="MUS_ROUTE120", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_LEGUME_THICKET",
        connections=[connection("right", "MAP_STRATA_PALM_FOREST", 10)],
        objects=[
            obj("LOCALID_STRATA_THICKET_EOCONODON", "OBJ_EVENT_GFX_SPECIES(EOCONODON)", 10, 9,
                "StrataLegumeThicket_EventScript_EoconodonLook", "MOVEMENT_TYPE_FACE_DOWN",
                flag=a3_flag(4)),
        ],
        bgs=[sign(21, 24, "StrataLegumeThicket_EventScript_NoteLegumes"),
             sign(14, 11, "StrataLegumeThicket_EventScript_NoteMarsh"),
             sign(8, 10, "StrataLegumeThicket_EventScript_NoteCarcass")],
        # Every way north into the marsh crosses row 13 (the boss only waits there in Act 3).
        coords=boss_triggers("ERA_CORRAL_BLUFFS", "StrataLegumeThicket_EventScript_Eoconodon",
                             [(x, 13) for x in (0, 1, 2) + tuple(range(4, 20))]),
        encounters=dict(
            land_mons=mons(("TAENIOLABIS", 18, 19), ("CARSIOPTYCH", 18, 19), ("LOXOLOPHUS", 18, 19), ("TAENIOLABIS", 19, 20),
                           ("PURGATORIUS", 18, 20), ("CARSIOPTYCH", 19, 20), ("LOXOLOPHUS", 19, 21), ("MESODMA", 18, 19),
                           ("TAENIOLABIS", 20, 21), ("PROTICTIS", 19, 21), ("EOCONODON", 20, 21), ("TAENIOLABIS", 20, 21)),
        ),
    ),
    # The real site: fossils sit in carbonate concretions that weather out of the bluffs.
    dict(
        id="MAP_STRATA_CONCRETION_BLUFFS", name="StrataConcretionBluffs", era="ERA_CORRAL_BLUFFS",
        habitat="open", light="day",
        forage=[forage(10, 6, "LEGUME_POD"), forage(5, 15, "BROWSE"), forage(24, 17, "LARVAE"), forage(44, 10, "CARRION"),
                forage(30, 12, "LEGUME_POD")],
        crop=dict(**{"from": "LAYOUT_ROUTE116"}, rect=(0, 0, 60, 20)),
        patches=[
            dict(rect=(36, 5, 5, 4), same_as=(38, 11)),    # the house -> bare ground
            dict(rect=(37, 9, 3, 2), same_as=(38, 11)),    # its flower beds
            signpost(4, 11), signpost(30, 16), signpost(47, 12),
        ],
        # Cave mouths in the cliff face and the secret-base cave spot -> plain rock
        swap={0x0A7: (0x091, 1), 0x0AF: (0x07C, 1), 0x1B0: (0x0A9, 1)},
        music="MUS_ROUTE104", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_CONCRETION_BLUFFS",
        connections=[connection("left", "MAP_STRATA_PALM_FOREST", -15)],
        objects=[
            # The mini-boss: a Taeniolabis cracking seeds on the flats.
            obj("LOCALID_STRATA_BLUFFS_TAENIOLABIS", "OBJ_EVENT_GFX_SPECIES(TAENIOLABIS)", 28, 15,
                "StrataConcretionBluffs_EventScript_Taeniolabis", "MOVEMENT_TYPE_FACE_DOWN",
                flag=a3_flag(3)),
            # Concretions: round rocks to crack (one-time finds).
            obj("LOCALID_STRATA_BLUFFS_CONCRETION_1", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 45, 11,
                "StrataConcretionBluffs_EventScript_Concretion1", "MOVEMENT_TYPE_NONE", flag=a3_flag(0)),
            obj("LOCALID_STRATA_BLUFFS_CONCRETION_2", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 48, 9,
                "StrataConcretionBluffs_EventScript_Concretion2", "MOVEMENT_TYPE_NONE", flag=a3_flag(1)),
            obj("LOCALID_STRATA_BLUFFS_CONCRETION_3", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 51, 16,
                "StrataConcretionBluffs_EventScript_Concretion3", "MOVEMENT_TYPE_NONE", flag=a3_flag(2)),
        ],
        bgs=[sign(4, 11, "StrataConcretionBluffs_EventScript_NoteSite"),
             sign(30, 16, "StrataConcretionBluffs_EventScript_NoteTaeniolabis"),
             sign(47, 12, "StrataConcretionBluffs_EventScript_NoteConcretions")],
        encounters=dict(
            land_mons=mons(("TAENIOLABIS", 17, 19), ("LOXOLOPHUS", 17, 18), ("CARSIOPTYCH", 17, 18), ("PURGATORIUS", 17, 19),
                           ("ASTERIORNIS", 17, 19), ("PROTICTIS", 17, 19), ("TAENIOLABIS", 18, 20), ("MESODMA", 17, 18),
                           ("LOXOLOPHUS", 18, 20), ("CARSIOPTYCH", 18, 20), ("TAENIOLABIS", 19, 20), ("ASTERIORNIS", 19, 20)),
        ),
    ),
    # The creek: the rising Laramide Rockies shed the sediment that became the Denver Fm.
    dict(
        id="MAP_STRATA_FRONT_RANGE_CREEK", name="StrataFrontRangeCreek", era="ERA_CORRAL_BLUFFS",
        habitat="water", light="day",
        forage=[forage(5, 6, "FERN_FROND"), forage(14, 3, "PALM_FRUIT"), forage(14, 9, "BROWSE"),
                forage(10, 18, "LARVAE"), forage(21, 13, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE119"}, rect=(0, 54, 40, 25)),
        patches=[
            dict(rect=(16, 12, 6, 2), same_as=(10, 12)),   # a path down to the water
            signpost(8, 21), signpost(12, 12), signpost(19, 12),
        ],
        music="MUS_ROUTE119", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_FRONT_RANGE_CREEK",
        connections=[connection("down", "MAP_STRATA_PALM_FOREST", -8)],
        bgs=[sign(8, 21, "StrataFrontRangeCreek_EventScript_NoteRockies"),
             sign(12, 12, "StrataFrontRangeCreek_EventScript_NoteTurtles"),
             sign(19, 12, "StrataFrontRangeCreek_EventScript_NoteChampsosaur")],
        encounters=dict(
            land_mons=mons(("MESODMA", 15, 16), ("LOXOLOPHUS", 15, 16), ("PROTOCHELYD", 15, 17), ("CARSIOPTYCH", 15, 17),
                           ("PURGATORIUS", 16, 17), ("PROTOCHELYD", 16, 18), ("PROTICTIS", 16, 18), ("ASTERIORNIS", 16, 18),
                           ("LOXOLOPHUS", 17, 18), ("MESODMA", 17, 18), ("CHAMPSOSAUR", 17, 19), ("BOREALOSUCH", 18, 19)),
            water_mons=mons(("LEPISOSTEUS", 15, 18), ("CHAMPSOSAUR", 15, 18), ("PROTOCHELYD", 16, 19),
                            ("BOREALOSUCH", 17, 19), ("BOREALOSUCH", 18, 20)),
            fishing_mons=mons(("LEPISOSTEUS", 15, 17), ("LEPISOSTEUS", 15, 17), ("LEPISOSTEUS", 16, 18), ("CHAMPSOSAUR", 16, 18),
                              ("PROTOCHELYD", 16, 18), ("CHAMPSOSAUR", 17, 19), ("PROTOCHELYD", 17, 19), ("LEPISOSTEUS", 17, 19),
                              ("BOREALOSUCH", 18, 20), ("BOREALOSUCH", 18, 20)),
        ),
    ),
]
