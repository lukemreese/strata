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
"""

from . import (  # noqa: F401
    act0_present, act1_hell_creek, act2_impact, act3_corral_bluffs, act4_bighorn,
    act5_green_river, act6_white_river, act7_ashfall, act8_ice_age, epilogue,
)
from .common import ERAS, SECRET_BASE_SWAPS  # noqa: F401

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


_check()
