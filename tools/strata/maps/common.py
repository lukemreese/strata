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


# ----------------------------------------------------------------------
# Habitat, light and forage (R3/R4). Per-map keys, generated into the map table
# src/data/strata_map_eras.h (sStrataMapInfo, read by src/strata_map.c):
#
#   habitat="forest" | "open" | "water" | None
#       Every 32 steps on the map add that pressure to the party
#       (Selection_GetHabitat). Surfing and shores are water anyway. None (the
#       default): the grass underfoot decides (long grass forest, tall grass open).
#       Required on every deep-time map (one with `era`), even if None.
#   light="day" | "dusk" | "dark" | "ash" | "none" | "dns"
#       Fixed day/night tint, whatever the wall clock says (UpdateTimeOfDay).
#       "none" never tints (caves), "dns" follows the real clock (the default;
#       present day only). Required on every deep-time map.
#   forage=[forage(x, y, "FERN_FROND"), ...]
#       Food that regrows on every visit, see forage() below.
# ----------------------------------------------------------------------

HABITATS = {"forest": "PRESSURE_FOREST", "open": "PRESSURE_OPEN", "water": "PRESSURE_WATER", None: "PRESSURE_NONE"}
LIGHTS = {"dns": "STRATA_LIGHT_DNS", "day": "STRATA_LIGHT_DAY", "dusk": "STRATA_LIGHT_DUSK",
          "dark": "STRATA_LIGHT_DARK", "ash": "STRATA_LIGHT_ASH", "none": "STRATA_LIGHT_NONE"}

# Forage items (ITEM_<name>, src/data/items.h): the pressure each adds (+12, and 20 HP)
# and the eras it may be placed in, so the food fits the flora and fauna of the layer.
# "PRESENT" stands for both present-day eras (ERA_PRESENT_DIG, ERA_EPILOGUE) and
# for maps with no era.
_ALL_ERAS = ("ERA_HELL_CREEK", "ERA_IMPACT_WINTER", "ERA_CORRAL_BLUFFS", "ERA_BIGHORN_PETM", "ERA_GREEN_RIVER",
             "ERA_WHITE_RIVER", "ERA_ASHFALL", "ERA_TRAP_CAVE", "PRESENT")
FORAGE_ITEMS = {
    # Ferns: throughout, and the "fern spike" right after the impact.
    "FERN_FROND": ("plant", _ALL_ERAS),
    # Palms reached Montana-Wyoming in the warm Late Cretaceous to Eocene, then left
    # the northern interior with the Eocene-Oligocene cooling.
    "PALM_FRUIT": ("plant", ("ERA_HELL_CREEK", "ERA_CORRAL_BLUFFS", "ERA_BIGHORN_PETM", "ERA_GREEN_RIVER")),
    # The oldest legume pods are from Corral Bluffs (~65.35 Ma, Lyson et al. 2019).
    "LEGUME_POD": ("plant", _ALL_ERAS[_ALL_ERAS.index("ERA_CORRAL_BLUFFS"):]),
    # Grass seed heads: grasses spread over the Great Plains from the Oligocene
    # (White River) and dominate from the Miocene on.
    "SEED_HEAD": ("plant", ("ERA_WHITE_RIVER", "ERA_ASHFALL", "ERA_TRAP_CAVE", "PRESENT")),
    "BROWSE": ("plant", _ALL_ERAS),
    "LARVAE": ("animal", _ALL_ERAS),
    "CARRION": ("animal", _ALL_ERAS),
}

# Forage flags: temp flags, cleared on every map load (warp or edge crossing), so
# picked forage regrows each time the player comes back. Reserved for forage on
# Strata maps: map scripts must not use them (gen_maps.py checks scripts.inc).
# FLAG_TEMP_11..1F are otherwise used only by FRLG cut trees and rocks.
FORAGE_FLAGS = [f"FLAG_TEMP_{i:X}" for i in range(0x11, 0x20)]


def forage(x, y, item, visible=False):
    """A forage spot, for a map's `forage=[...]` list.

    item: a FORAGE_ITEMS name ("FERN_FROND", "CARRION", ...), which must suit the
    map's era. Hidden by default: the player finds it by facing the tile and pressing
    A (place it on or beside a walkable tile; mapcheck.py checks it can be reached).
    visible=True puts an item ball on the tile instead (it blocks the tile).
    Either way it takes one of the map's FORAGE_FLAGS (15 per map, given out in list
    order by gen_maps.py), so it regrows on every visit.
    """
    item = item.upper().removeprefix("ITEM_")
    if item not in FORAGE_ITEMS:
        raise ValueError(f"forage({x}, {y}): {item} is not a forage item ({', '.join(FORAGE_ITEMS)})")
    return {"x": x, "y": y, "item": item, "visible": visible}


def forage_events(m):
    """The bg events (hidden) and object events (visible) for a map's forage, with
    their flags. Used by gen_maps.py."""
    spots = m.get("forage", [])
    if len(spots) > len(FORAGE_FLAGS):
        raise ValueError(f"{m['id']}: {len(spots)} forage spots, at most {len(FORAGE_FLAGS)}")
    bgs, objects = [], []
    for spot, flag in zip(spots, FORAGE_FLAGS):
        item = "ITEM_" + spot["item"]
        if spot["visible"]:
            event = obj(None, "OBJ_EVENT_GFX_ITEM_BALL", spot["x"], spot["y"], "Common_EventScript_FindItem",
                        flag=flag, elevation=None)
            del event["local_id"]
            event["trainer_sight_or_berry_tree_id"] = item
            objects.append(event)
        else:
            bgs.append({"type": "hidden_item", "x": spot["x"], "y": spot["y"], "elevation": 0,
                        "item": item, "flag": flag, "quantity": 1, "underfoot": False})
    return bgs, objects


def check_tags(m):
    """Validates a map's habitat, light and forage. Raises ValueError."""
    if m.get("habitat") not in HABITATS:
        raise ValueError(f"{m['id']}: habitat={m.get('habitat')!r}, expected one of {list(HABITATS)}")
    if m.get("light", "dns") not in LIGHTS:
        raise ValueError(f"{m['id']}: light={m.get('light')!r}, expected one of {list(LIGHTS)}")
    era = m.get("era")
    if era not in (None, "ERA_PRESENT_DIG", "ERA_EPILOGUE"):
        for key in ("habitat", "light"):
            if key not in m:
                raise ValueError(f"{m['id']}: deep-time maps need an explicit {key}= (see common.py)")
    layer = "PRESENT" if era in (None, "ERA_PRESENT_DIG", "ERA_EPILOGUE") else era
    for spot in m.get("forage", []):
        if layer not in FORAGE_ITEMS[spot["item"]][1]:
            raise ValueError(f"{m['id']}: forage {spot['item']} at ({spot['x']}, {spot['y']}) doesn't "
                             f"belong in {layer} (FORAGE_ITEMS in common.py)")
