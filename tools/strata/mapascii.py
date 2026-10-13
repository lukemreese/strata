#!/usr/bin/env python3
"""Print a generated layout's collision and elevation as text, for placing events.

Usage: python3 tools/strata/mapascii.py <LayoutName>   (e.g. StrataPalmForest)
  '#' blocked, '~' surfable water, digits: walkable tile's elevation (hex).
"""

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import maprender  # noqa: E402

ROOT = maprender.ROOT
WATER = {"POND_WATER", "DEEP_WATER", "OCEAN_WATER", "SEMI_DEEP_WATER", "WATERFALL", "NO_SURFACING",
         "INTERIOR_DEEP_WATER", "SOOTOPOLIS_DEEP_WATER"}


def main(name):
    layouts = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    layout = next(l for l in layouts if l.get("name") == f"{name}_Layout")
    tiles = maprender.TilesetPair(maprender.tileset_dir_from_symbol(layout["primary_tileset"]),
                                  maprender.tileset_dir_from_symbol(layout["secondary_tileset"]))
    names = maprender.behavior_names()
    w, h = layout["width"], layout["height"]
    blocks = struct.unpack(f"<{w * h}H", open(os.path.join(ROOT, layout["blockdata_filepath"]), "rb").read())
    print("    " + "".join(str(x // 10) for x in range(w)))
    print("    " + "".join(str(x % 10) for x in range(w)))
    for y in range(h):
        row = []
        for x in range(w):
            b = blocks[y * w + x]
            beh = names.get(tiles.behavior(b & 0x3FF), "")
            if beh in WATER:
                row.append("~")
            elif (b >> 10) & 3:
                row.append("#")
            else:
                row.append(f"{b >> 12:X}")
        print(f"{y:3} " + "".join(row))


if __name__ == "__main__":
    main(sys.argv[1])
