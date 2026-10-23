"""Act 6: White River badlands, SD/NE (~34-30 Ma).

Maps of this act only. Add a map by appending a dict to MAPS (order within an act
is its map-id order), and its MAPSEC to MAP_SECTIONS. Shared helpers are in
common.py; see maps/__init__.py for how the acts are assembled.

The act, north to south and west to east:

    Gallery Forest ---- Badlands Wall ---- Toadstool Trackways
          |
    White River  (arrival from camp: the valley's north end; the bone stash
                  and the Archaeotherium boss are on the plateau to the south)

All four maps use the Oligocene palettes of the General and Fallarbor tilesets, the only
ones gen_tilesets.py makes, so the crops come from the Fallarbor routes (113, 114).
The Gallery Forest is the north half of Route 114 (the White River map is its south half,
so they join with offset 0); the Badlands Wall and the Toadstool Trackways are the left and
right of Route 113 (they also join with offset 0).

Map events are assembled without include/constants/strata.h, so they name the act flags by
their stock FLAG_UNUSED_0x... / VAR_UNUSED_0x... names (include/constants/strata_act_flags.h):
FLAG_UNUSED_0x28C is FLAG_STRATA_A6_HYAENODON_GONE, 0x28D FLAG_STRATA_A6_STASH_CLEARED,
VAR_UNUSED_0x40FC VAR_STRATA_ACT6.
"""

from .common import *  # noqa: F401,F403

MAP_SECTIONS = [
    ("MAPSEC_STRATA_WHITE_RIVER", "WHITE RIVER"),
    ("MAPSEC_STRATA_GALLERY_FOREST", "GALLERY FOREST"),
    ("MAPSEC_STRATA_BADLANDS_WALL", "BADLANDS WALL"),
    ("MAPSEC_STRATA_TOADSTOOL", "TOADSTOOL TRACKS"),
]

OLIGOCENE = ("gTileset_GeneralOligocene", "gTileset_FallarborOligocene")

# General primary tileset: the wooden signpost (a field note on open ground).
SIGNPOST = 0x01B
GROUND = 0x279        # Fallarbor: plain dirt ground (Route 114's, and 113's red-soil corner)
ASH_GROUND = 0x218    # Fallarbor: plain pale ground (Route 113)
GRASS = 0x001         # General: plain grass
LONG_GRASS = 0x015    # General: long grass (forest encounters, FOREST pressure)
TALL_GRASS = 0x212    # Fallarbor: the tall grass that the ash-covered 0x20A imitates


def signpost(x, y, script, facing="BG_EVENT_PLAYER_FACING_ANY"):
    """A patch that plants a (blocked) signpost at (x, y), and the sign event for it."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), sign(x, y, script, facing)


def anchor_post(x, y):
    """The anchor sign back to the field station, drawn as a signpost."""
    return dict(at=(x, y), tiles=[[SIGNPOST]], collision=1), anchor(x, y)


# Where the Archaeotherium waits on the stash plateau, and the Hyaenodon on the trackways.
_HELL_PIG_AT = (19, 26)
_HYAENODON_AT = (12, 8)

_WR_NOTES = [signpost(22, 2, "StrataWhiteRiver_EventScript_NoteCooling"),
             signpost(11, 12, "StrataWhiteRiver_EventScript_NoteDogs"),
             signpost(7, 29, "StrataWhiteRiver_EventScript_NoteStash")]
_GF_ANCHOR = anchor_post(24, 35)
_GF_NOTES = [signpost(22, 20, "StrataGalleryForest_EventScript_NoteGallery"),
             signpost(33, 15, "StrataGalleryForest_EventScript_NoteSquirrel"),
             signpost(12, 34, "StrataGalleryForest_EventScript_NoteHorse")]
_BW_ANCHOR = anchor_post(1, 13)
_BW_NOTES = [signpost(6, 7, "StrataBadlandsWall_EventScript_NoteContact"),
             signpost(30, 12, "StrataBadlandsWall_EventScript_NoteOreodonts"),
             signpost(40, 12, "StrataBadlandsWall_EventScript_NoteRabbit")]
_TT_ANCHOR = anchor_post(1, 12)
_TT_NOTES = [signpost(6, 12, "StrataToadstool_EventScript_NoteTrackway"),
             signpost(16, 12, "StrataToadstool_EventScript_NoteCreodont"),
             signpost(30, 10, "StrataToadstool_EventScript_NoteBurial")]

MAPS = [
    # ------------------------------------------------------------------
    # Act 6: White River badlands, SD/NE (~34-30 Ma): cooler, drier open woodland
    # ------------------------------------------------------------------
    dict(
        id="MAP_STRATA_WHITE_RIVER", name="StrataWhiteRiver", era="ERA_WHITE_RIVER",
        habitat="open", light="day",
        forage=[forage(20, 6, "SEED_HEAD"), forage(10, 13, "BROWSE"), forage(29, 22, "CARRION"),
                # The bone stash on the plateau: carrion, once the hell pig has been dealt with.
                forage(16, 27, "CARRION", visible=True), forage(24, 28, "CARRION", visible=True),
                forage(21, 26, "CARRION"), forage(14, 30, "CARRION")],
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 37, 40, 43), tilesets=OLIGOCENE),
        patches=[
            dict(rect=(31, 5, 2, 5), metatile=0x001, elevation=3),    # berry-soil plot -> grass
        ] + [p for p, _ in _WR_NOTES],
        # secret-base rock spots and a cave door -> plain rock
        swap={0x208: 0x241, 0x259: 0x265, 0x261: (0x265, 1)},
        music="MUS_ROUTE110", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_WHITE_RIVER",
        arrival=(17, 3),
        connections=[connection("up", "MAP_STRATA_GALLERY_FOREST")],
        bgs=[anchor(17, 4)] + [s for _, s in _WR_NOTES],
        coords=boss_triggers("ERA_WHITE_RIVER", "StrataWhiteRiver_EventScript_Archaeotherium",
                             [(13, 32), (14, 32), (24, 34), (25, 34)]),
        objects=[
            # The hell pig at its stash: talking to it starts the same fight as the triggers.
            obj("LOCALID_STRATA_WR_ARCHAEOTHERIUM", "OBJ_EVENT_GFX_SPECIES(PIGNITE)", _HELL_PIG_AT[0], _HELL_PIG_AT[1],
                "StrataWhiteRiver_EventScript_Archaeotherium", "MOVEMENT_TYPE_FACE_DOWN", flag="FLAG_UNUSED_0x28D",
                elevation=7),
        ],
        encounters=dict(
            land_mons=mons(("PALAEOLAGUS", 32, 34), ("MESOHIPPUS", 34, 36), ("MERYCOIDODON", 34, 36), ("LEPTOMERYX", 34, 36),
                           ("PALAEOLAGUS", 33, 35), ("ISCHYROMYS", 34, 36), ("STYLEMYS", 35, 37), ("POEBROTHERE", 35, 37),
                           ("HESPEROCYON", 35, 37), ("SUBHYRACODON", 36, 38), ("HOPLOPHONEUS", 37, 39), ("ARCHAEOTHERE", 38, 39)),
        ),
    ),
    # The forest strips along the river and its lake, the north half of Route 114: the horse
    # lineage's forest branch (Hypohippus) is steered here, and the first squirrels live here.
    dict(
        id="MAP_STRATA_GALLERY_FOREST", name="StrataGalleryForest", era="ERA_WHITE_RIVER",
        habitat="forest", light="day",
        forage=[forage(36, 12, "BROWSE"), forage(33, 7, "BROWSE"), forage(31, 14, "LARVAE"),
                forage(10, 34, "FERN_FROND"), forage(35, 10, "SEED_HEAD")],
        crop=dict(**{"from": "LAYOUT_ROUTE114"}, rect=(0, 0, 40, 37), tilesets=OLIGOCENE),
        patches=[
            dict(rect=(28, 2, 4, 4), metatile=GROUND, collision=0),           # house -> ground
            dict(rect=(32, 5, 8, 4), metatile=GROUND),                        # berry-soil plots -> ground
            dict(rect=(32, 11, 8, 4), metatile=GROUND),
            dict(rect=(25, 33, 5, 4), metatile=GRASS),                        # house -> grass
            dict(rect=(19, 21, 4, 13), metatile=GROUND, elevation=3),         # plank bridge -> a sandbar
            dict(rect=(32, 6, 7, 8), metatile=LONG_GRASS),                    # thicket in the clearing
            dict(rect=(13, 34, 5, 2), metatile=LONG_GRASS),                   # reeds south of the lake
        ] + [_GF_ANCHOR[0]] + [p for p, _ in _GF_NOTES],
        music="MUS_ROUTE110", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_GALLERY_FOREST",
        connections=[connection("down", "MAP_STRATA_WHITE_RIVER"), connection("right", "MAP_STRATA_BADLANDS_WALL")],
        bgs=[_GF_ANCHOR[1]] + [s for _, s in _GF_NOTES],
        encounters=dict(
            land_mons=mons(("MESOHIPPUS", 33, 35), ("DOUGLASSCIUR", 33, 35), ("LEPTOMERYX", 33, 35), ("HESPEROCYON", 33, 35),
                           ("DOUGLASSCIUR", 34, 36), ("MESOHIPPUS", 34, 36), ("LEPTOMERYX", 34, 36), ("HESPEROCYON", 34, 36),
                           ("DOUGLASSCIUR", 35, 37), ("MESOHIPPUS", 35, 37), ("HESPEROCYON", 36, 37), ("LEPTOMERYX", 36, 37)),
            water_mons=mons(("LEPISOSTEUS", 32, 35), ("LEPISOSTEUS", 32, 35), ("LEPISOSTEUS", 33, 36),
                            ("LEPISOSTEUS", 34, 37), ("LEPISOSTEUS", 35, 38)),
            fishing_mons=mons(("LEPISOSTEUS", 32, 34), ("LEPISOSTEUS", 32, 34), ("LEPISOSTEUS", 33, 35), ("LEPISOSTEUS", 33, 35),
                              ("LEPISOSTEUS", 34, 36), ("LEPISOSTEUS", 34, 36), ("LEPISOSTEUS", 35, 37), ("LEPISOSTEUS", 35, 37),
                              ("LEPISOSTEUS", 36, 38), ("LEPISOSTEUS", 36, 38)),
        ),
    ),
    # The cliffs and open red-soil flats: the Chadron / Brule contact is in the banded wall at
    # the north-west corner. Left half of Route 113 (the Toadstool Trackways is its right half).
    dict(
        id="MAP_STRATA_BADLANDS_WALL", name="StrataBadlandsWall", era="ERA_WHITE_RIVER",
        habitat="open", light="day",
        forage=[forage(18, 8, "SEED_HEAD"), forage(36, 7, "SEED_HEAD"), forage(23, 5, "BROWSE"),
                forage(28, 13, "CARRION"), forage(9, 10, "SEED_HEAD")],
        crop=dict(**{"from": "LAYOUT_ROUTE113"}, rect=(0, 0, 48, 20), tilesets=OLIGOCENE),
        patches=[
            dict(rect=(0, 7, 13, 7), metatile=GROUND),                        # berry-soil plots -> ground
            dict(at=(32, 2), tiles=[[0x26D, 0x26E, 0x26D, 0x26E], [0x20C, 0x20D, 0x20C, 0x20D]], collision=1),  # house -> trees
            dict(rect=(32, 4, 4, 2), metatile=ASH_GROUND),
        ] + [_BW_ANCHOR[0]] + [p for p, _ in _BW_NOTES],
        swap={0x20A: TALL_GRASS},                                             # ash-covered grass -> plain tall grass
        music="MUS_ROUTE110", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_BADLANDS_WALL",
        connections=[connection("left", "MAP_STRATA_GALLERY_FOREST"), connection("right", "MAP_STRATA_TOADSTOOL")],
        bgs=[_BW_ANCHOR[1]] + [s for _, s in _BW_NOTES],
        objects=[
            # Oreodonts grazing: a herd (talk for a note; they ignore you).
            obj("LOCALID_STRATA_BW_HERD_A", "OBJ_EVENT_GFX_SPECIES(MUDBRAY)", 24, 9, "StrataBadlandsWall_EventScript_Herd",
                "MOVEMENT_TYPE_FACE_DOWN"),
            obj("LOCALID_STRATA_BW_HERD_B", "OBJ_EVENT_GFX_SPECIES(MUDBRAY)", 26, 11, "StrataBadlandsWall_EventScript_Herd",
                "MOVEMENT_TYPE_FACE_LEFT"),
            obj("LOCALID_STRATA_BW_HERD_C", "OBJ_EVENT_GFX_SPECIES(MUDBRAY)", 22, 12, "StrataBadlandsWall_EventScript_Herd",
                "MOVEMENT_TYPE_FACE_RIGHT"),
        ],
        encounters=dict(
            land_mons=mons(("PALAEOLAGUS", 32, 34), ("MERYCOIDODON", 33, 35), ("PALAEOLAGUS", 33, 35), ("STYLEMYS", 33, 35),
                           ("MERYCOIDODON", 34, 36), ("ISCHYROMYS", 33, 35), ("MESOHIPPUS", 34, 36), ("LEPTOMERYX", 34, 36),
                           ("POEBROTHERE", 35, 37), ("HESPEROCYON", 34, 36), ("SUBHYRACODON", 36, 38), ("HOPLOPHONEUS", 36, 38)),
        ),
    ),
    # The trackway floodplain: right half of Route 113. The Hyaenodon (mini-boss) hunts here.
    dict(
        id="MAP_STRATA_TOADSTOOL", name="StrataToadstool", era="ERA_WHITE_RIVER",
        habitat="open", light="day",
        forage=[forage(14, 8, "CARRION"), forage(44, 9, "SEED_HEAD"), forage(46, 8, "SEED_HEAD"),
                forage(31, 6, "CARRION"), forage(20, 4, "BROWSE")],
        crop=dict(**{"from": "LAYOUT_ROUTE113"}, rect=(48, 0, 52, 20), tilesets=OLIGOCENE),
        patches=[] + [_TT_ANCHOR[0]] + [p for p, _ in _TT_NOTES],
        swap={0x20A: TALL_GRASS},
        music="MUS_ROUTE110", map_type="MAP_TYPE_ROUTE", mapsec="MAPSEC_STRATA_TOADSTOOL",
        connections=[connection("left", "MAP_STRATA_BADLANDS_WALL")],
        bgs=[_TT_ANCHOR[1]] + [s for _, s in _TT_NOTES],
        coords=[
            # The Hyaenodon's line of sight across the way east (once).
            trigger(10, y, "VAR_UNUSED_0x40FC", 0, "StrataToadstool_EventScript_Hyaenodon") for y in (9, 10, 11)
        ],
        objects=[
            obj("LOCALID_STRATA_TT_HYAENODON", "OBJ_EVENT_GFX_SPECIES(MIGHTYENA)", _HYAENODON_AT[0], _HYAENODON_AT[1],
                "StrataToadstool_EventScript_Hyaenodon", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_UNUSED_0x28C"),
        ],
        encounters=dict(
            land_mons=mons(("POEBROTHERE", 34, 36), ("SUBHYRACODON", 35, 37), ("MERYCOIDODON", 34, 36), ("LEPTOMERYX", 34, 36),
                           ("POEBROTHERE", 35, 37), ("STYLEMYS", 35, 37), ("SUBHYRACODON", 36, 38), ("HESPEROCYON", 35, 37),
                           ("PALAEOLAGUS", 33, 35), ("HYAENODON", 35, 37), ("HOPLOPHONEUS", 37, 39), ("HYAENODON", 36, 38)),
        ),
    ),
]
