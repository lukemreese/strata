#!/usr/bin/env python3
"""Check that a Strata map's events can be reached on foot from its arrival point
and connected edges.

Usage: python3 tools/strata/mapcheck.py [MapName ...]   (default: every Strata map)

Walks the layout from the arrival tile (include/constants/strata_maps.h, or the
first warp, or the first connected edge) the way the player can: no surfing, elevation rules as in
field_player_avatar.c, ledges one way. Then reports every coord event, sign and
map edge that can't be reached, and every hidden item (forage) and item ball that
can't be picked up.
"""

import json
import os
import re
import struct
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(__file__))
import maprender  # noqa: E402
from mapascii import WATER  # noqa: E402

ROOT = maprender.ROOT
DIRS = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}


def arrivals():
    text = open(os.path.join(ROOT, "include/constants/strata_maps.h")).read()
    return {m.group(1): (int(m.group(2)), int(m.group(3)))
            for m in re.finditer(r"STRATA_ARRIVAL_(\w+) (\d+), (\d+)", text)}


def can_move(e_from, e_to):
    return e_from in (0, 15) or e_to in (0, 15) or e_from == e_to


def reachable(layout, starts):
    tiles = maprender.TilesetPair(maprender.tileset_dir_from_symbol(layout["primary_tileset"]),
                                  maprender.tileset_dir_from_symbol(layout["secondary_tileset"]))
    names = maprender.behavior_names()
    w, h = layout["width"], layout["height"]
    blocks = struct.unpack(f"<{w * h}H", open(os.path.join(ROOT, layout["blockdata_filepath"]), "rb").read())

    def info(x, y):
        b = blocks[y * w + x]
        return (b >> 10) & 3, b >> 12, names.get(tiles.behavior(b & 0x3FF), "")

    # The arrival tile itself may be a door; edge tiles must be walkable.
    starts = [starts[0]] + [(x, y) for x, y in starts[1:] if not info(x, y)[0] and info(x, y)[2] not in WATER]
    seen = set(starts)
    queue = deque(starts)
    while queue:
        x, y = queue.popleft()
        _, elev, _ = info(x, y)
        for name, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            coll, nelev, beh = info(nx, ny)
            if beh == f"JUMP_{name}":
                nx, ny = nx + dx, ny + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                coll, nelev, beh = info(nx, ny)
            elif beh.startswith("JUMP_"):
                continue
            if coll or beh in WATER or not can_move(elev, nelev):
                continue
            if (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    walkable = {(x, y) for y in range(h) for x in range(w)
                if not info(x, y)[0] and info(x, y)[2] not in WATER}
    return seen, walkable


def check(name):
    m = json.load(open(os.path.join(ROOT, f"data/maps/{name}/map.json")))
    layouts = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    layout = next(l for l in layouts if l.get("id") == m["layout"])
    key = m["id"].removeprefix("MAP_STRATA_")
    start = arrivals().get(key)
    if start is None and m["warp_events"]:
        start = (m["warp_events"][0]["x"], m["warp_events"][0]["y"])
    w, h = layout["width"], layout["height"]
    edges = {"up": [(x, 0) for x in range(w)], "down": [(x, h - 1) for x in range(w)],
             "left": [(0, y) for y in range(h)], "right": [(w - 1, y) for y in range(h)]}
    starts = [start] if start is not None else []
    for c in m["connections"] or []:
        starts += edges[c["direction"]]
    if not starts:
        print(f"{name}: no arrival point, skipped")
        return True
    seen, walkable = reachable(layout, starts)
    ok = True
    for e in m["coord_events"]:
        # A trigger on a blocked tile can never fire, and needn't.
        if (e["x"], e["y"]) in walkable and (e["x"], e["y"]) not in seen:
            print(f"{name}: trigger ({e['x']}, {e['y']}) {e.get('script')} unreachable")
            ok = False
    for e in m["bg_events"]:
        x, y = e["x"], e["y"]
        if not any((x + dx, y + dy) in seen for dx, dy in DIRS.values()):
            what = f"hidden {e['item']}" if e.get("type") == "hidden_item" else f"sign {e.get('script')}"
            print(f"{name}: {what} at ({x}, {y}) can't be stood next to")
            ok = False
    # Item balls (forage with visible=True, see maps/common.py) are picked up from beside.
    for e in m["object_events"]:
        x, y = e["x"], e["y"]
        if e.get("graphics_id") == "OBJ_EVENT_GFX_ITEM_BALL" \
           and not any((x + dx, y + dy) in seen for dx, dy in DIRS.values()):
            print(f"{name}: item ball {e.get('trainer_sight_or_berry_tree_id')} at ({x}, {y}) can't be reached")
            ok = False
    for c in m["connections"] or []:
        if not any(t in seen for t in edges[c["direction"]]):
            print(f"{name}: {c['direction']} edge to {c['map']} unreachable")
            ok = False
    print(f"{name}: {len(seen)} tiles reachable" + ("" if ok else "  <-- problems"))
    return ok


def main(names):
    if not names:
        names = sorted(d for d in os.listdir(os.path.join(ROOT, "data/maps")) if d.startswith("Strata"))
    ok = all([check(n) for n in names])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
