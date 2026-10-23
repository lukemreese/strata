"""Helpers and constants shared by every act module of the Strata map package."""

# Hoenn secret-base entrances in the General primary tileset. They are interactive
# ("make a SECRET BASE here?"), so every Strata map swaps them for the plain rock or
# tree they imitate: rock-mound cave mouths, and the hollow tree trunks.
SECRET_BASE_SWAPS = {0x1A0: 0x079, 0x1A8: 0x071, 0x026: 0x016, 0x027: 0x017}

# Fences, arrow-warp tiles, signposts, doors and the like become plain ground.
GROUND = lambda tile: (tile, 0)  # noqa: E731

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
