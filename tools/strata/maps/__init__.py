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

Layout of this package (one file per act, so content agents can work on
different acts without touching the same file):

    common.py               helpers (obj, warp, sign, trigger, anchor, boss_triggers,
                            mons, ...), ERAS, SECRET_BASE_SWAPS, and the crops shared
                            by several acts (the Hell Creek footprint)
    act0_present.py ...     one module per act: act0_present, act1_hell_creek,
    act8_ice_age.py         act2_impact, act3_corral_bluffs, act4_bighorn,
                            act5_green_river, act6_white_river, act7_ashfall,
                            act8_ice_age, epilogue

Each act module defines:
    MAPS            the act's maps (dicts, see common.py helpers)
    MAP_SECTIONS    (MAPSEC constant, display name) pairs for the act's maps
    HEAL_LOCATIONS  optional

ORDER MATTERS. The map's position in the global MAPS list is its map number in
the Strata map group, and MAP_SECTIONS order is the MAPSEC enum order. Both are
the concatenation of the act modules in ACT_MODULES order, and a map's order within
its act is its order in that act's MAPS. New maps are appended to the end of their
act's MAPS: that shifts the map numbers of later acts' maps, which is harmless
(nothing but the generated files refers to them by number; scripts and code use the
MAP_STRATA_* names). The same goes for MAP_SECTIONS.

To add a map: append a dict to MAPS in the act's module (and a MAPSEC to
MAP_SECTIONS if it needs a new area name), write data/maps/<Name>/scripts.inc,
and run gen_maps.py. Nothing outside the act's module has to change, except for
a new shared helper or constant (common.py) or a new act module (ACT_MODULES below).

Habitat, light and forage (details in common.py, next to HABITATS):

    dict(id="MAP_STRATA_FOO", name="StrataFoo", era="ERA_GREEN_RIVER",
         habitat="forest", light="day",
         forage=[forage(12, 5, "PALM_FRUIT"), forage(30, 18, "LARVAE"),
                 forage(8, 40, "BROWSE", visible=True)],
         ...)

  - habitat= forest / open / water / None: the pressure every 32 steps on the map
    add to the party (water and shores count as water anyway). None lets the grass
    underfoot decide. Pick what the reconstruction is mostly made of.
  - light= day / dusk / dark / ash / none (caves) / dns (real clock, present day).
    Fixed: deep time ignores the wall clock.
  - Every deep-time map (one with an era, other than the present day) must state
    both, even habitat=None.
  - forage=[forage(x, y, item), ...]: 3-6 spots per map, up to 15. Each heals a mon
    20 HP and adds +12 PLANT (fern frond, palm fruit, legume pod, seed head, browse)
    or ANIMAL (larvae, carrion) pressure when eaten; ~6 of one kind push a lineage
    past a branch threshold (64). Hidden by default (face the tile, press A);
    visible=True for an item ball. Spots get the temp flags FLAG_TEMP_11..1F
    (FORAGE_FLAGS) in list order, so forage regrows on every map load; map scripts
    of a map with forage must not use those flags. Items must suit the era
    (FORAGE_ITEMS: no palms after the Eocene, no legumes before Corral Bluffs, grass
    seeds from White River on). Put a field note sign near a spot to hint at it.
  - mapcheck.py checks that every forage spot can be reached.
"""

from . import (  # noqa: F401
    act0_present, act1_hell_creek, act2_impact, act3_corral_bluffs, act4_bighorn,
    act5_green_river, act6_white_river, act7_ashfall, act8_ice_age, epilogue,
)
from .common import ERAS, FORAGE_FLAGS, HABITATS, LIGHTS, SECRET_BASE_SWAPS, check_tags, forage_events  # noqa: F401

# Act order = map-id order. Do not reorder.
ACT_MODULES = [
    act0_present, act1_hell_creek, act2_impact, act3_corral_bluffs, act4_bighorn,
    act5_green_river, act6_white_river, act7_ashfall, act8_ice_age, epilogue,
]

MAPS = [m for mod in ACT_MODULES for m in mod.MAPS]
MAP_SECTIONS = [s for mod in ACT_MODULES for s in mod.MAP_SECTIONS]
HEAL_LOCATIONS = [h for mod in ACT_MODULES for h in getattr(mod, "HEAL_LOCATIONS", [])]


def _check():
    for what, items in (("map id", [m["id"] for m in MAPS]), ("map name", [m["name"] for m in MAPS]),
                        ("MAPSEC", [s for s, _ in MAP_SECTIONS])):
        dupes = sorted({i for i in items if items.count(i) > 1})
        if dupes:
            raise ValueError(f"duplicate {what}: {', '.join(dupes)}")
    known = {s for s, _ in MAP_SECTIONS}
    for m in MAPS:
        if m.get("mapsec") not in known:
            raise ValueError(f"{m['id']}: mapsec {m.get('mapsec')} is not in any act's MAP_SECTIONS")
        check_tags(m)


_check()
