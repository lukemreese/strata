"""Static knowledge of Strata's maps for scenarios: which act a map belongs to,
its events, creature objects, edges, warps, and which tiles can be walked on
(the same walk rules as tools/strata/mapcheck.py)."""

import json
import os
import re
import struct
import sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
STRATA = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(STRATA, "..", ".."))
sys.path.insert(0, STRATA)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import mapcheck  # noqa: E402
import maprender  # noqa: E402

STARTERS = ["SPECIES_CIMOLESTES", "SPECIES_ASTERIORNIS", "SPECIES_EMARGINACHEL"]  # src/starter_choose.c
# A party level that suits each act (era floors and boss levels in docs/strata_design.md).
ACT_LEVEL = [5, 12, 15, 22, 28, 34, 40, 46, 52, 55]
DIR_STEP = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


@lru_cache(None)
def acts():
    """{map id: act number} from the act modules (act0 ... act8, epilogue = 9)."""
    from maps import ACT_MODULES
    return {m["id"]: i for i, mod in enumerate(ACT_MODULES) for m in mod.MAPS}


def story_for_act(act):
    return 1 if act == 0 else 2 * act


@lru_cache(None)
def arrivals():
    return mapcheck.arrivals()


class MapInfo:
    def __init__(self, name):
        self.name = name
        self.json = json.load(open(os.path.join(ROOT, f"data/maps/{name}/map.json")))
        self.id = self.json["id"]
        self.act = acts().get(self.id, 0)
        layouts = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
        self.layout = next(l for l in layouts if l.get("id") == self.json["layout"])
        self.w, self.h = self.layout["width"], self.layout["height"]
        tiles = maprender.TilesetPair(maprender.tileset_dir_from_symbol(self.layout["primary_tileset"]),
                                      maprender.tileset_dir_from_symbol(self.layout["secondary_tileset"]))
        names = maprender.behavior_names()
        blocks = struct.unpack(f"<{self.w * self.h}H",
                               open(os.path.join(ROOT, self.layout["blockdata_filepath"]), "rb").read())
        self.behavior = {}
        self.collision = {}
        self.elevation = {}
        for y in range(self.h):
            for x in range(self.w):
                b = blocks[y * self.w + x]
                self.collision[(x, y)] = (b >> 10) & 3
                self.elevation[(x, y)] = b >> 12
                self.behavior[(x, y)] = names.get(tiles.behavior(b & 0x3FF), "")
        key = self.id.removeprefix("MAP_STRATA_")
        self.arrival = arrivals().get(key)
        starts = []
        if self.arrival:
            starts.append(self.arrival)
        starts += [(w["x"], w["y"]) for w in self.warps]
        edges = {"up": [(x, 0) for x in range(self.w)], "down": [(x, self.h - 1) for x in range(self.w)],
                 "left": [(0, y) for y in range(self.h)], "right": [(self.w - 1, y) for y in range(self.h)]}
        self.edges = edges
        for c in self.connections:
            starts += edges[c["direction"]]
        if not starts:
            starts = [(x, y) for (x, y), c in self.collision.items() if not c][:1]
        self.reachable, self.walkable = mapcheck.reachable(self.layout, starts)
        self.reachable = {t for t in self.reachable if t in self.walkable}
        self.objects = self.json["object_events"]
        self.blocked_by_objects = {(o["x"], o["y"]) for o in self.objects}
        self.trigger_tiles = {(e["x"], e["y"]): e for e in self.json["coord_events"] if e.get("type") == "trigger"}

    @property
    def warps(self):
        return self.json["warp_events"]

    @property
    def connections(self):
        return self.json.get("connections") or []

    def free(self, t):
        """A tile the player can stand on without starting anything."""
        return t in self.reachable and t not in self.blocked_by_objects and t not in self.trigger_tiles \
            and self.behavior.get(t, "") not in ("TALL_GRASS", "LONG_GRASS")

    def walk_set(self):
        """Tiles a walk may cross (triggers excluded so tours don't start set pieces)."""
        return {t for t in self.reachable if t not in self.blocked_by_objects and t not in self.trigger_tiles}

    def start_tile(self):
        if self.arrival and self.free(self.arrival):
            return self.arrival
        for c in [self.arrival] + [(w["x"], w["y"]) for w in self.warps]:
            if c:
                n = self.near(c, 1, 4)
                if n:
                    return n
        tiles = sorted(t for t in self.reachable if self.free(t))
        return tiles[len(tiles) // 2] if tiles else None

    def near(self, target, min_d=1, max_d=4, prefer="below"):
        """A free tile near target (Manhattan distance), preferring one below it so
        the target is on screen and the player faces it."""
        tx, ty = target
        best = None
        for (x, y) in self.reachable:
            d = abs(x - tx) + abs(y - ty)
            if not (min_d <= d <= max_d) or not self.free((x, y)):
                continue
            score = d + (0 if (prefer == "below" and y > ty and x == tx) else 0.5 if y >= ty else 1)
            if best is None or score < best[0]:
                best = (score, (x, y))
        return best[1] if best else None

    def species_objects(self):
        out = []
        for o in self.objects:
            m = re.match(r"OBJ_EVENT_GFX_SPECIES\((\w+)\)", o["graphics_id"])
            if m:
                out.append(dict(species=m.group(1), x=o["x"], y=o["y"], flag=o.get("flag"), script=o.get("script")))
        return out

    def tall_grass(self):
        return [t for t in sorted(self.reachable) if self.behavior[t] in ("TALL_GRASS", "LONG_GRASS")
                and t not in self.trigger_tiles and t not in self.blocked_by_objects]

    def story_triggers(self):
        """Coord triggers on VAR_STRATA_STORY: the act's boss line."""
        groups = {}
        for (x, y), e in self.trigger_tiles.items():
            if e["var"] == "VAR_STRATA_STORY":
                groups.setdefault((e["script"], int(e["var_value"])), []).append((x, y))
        return groups


@lru_cache(None)
def map_info(name_or_id):
    """MapInfo by folder name (StrataLevee) or id (MAP_STRATA_LEVEE)."""
    if name_or_id.startswith("MAP_"):
        for n in strata_maps():
            if json.load(open(os.path.join(ROOT, f"data/maps/{n}/map.json")))["id"] == name_or_id:
                return MapInfo(n)
        raise KeyError(name_or_id)
    return MapInfo(name_or_id)


def edge_pairs(mi, c):
    """Edge tiles of mi on connection c whose matching tile across the seam is walkable too:
    [(tile here, tile there)]."""
    other = map_info(c["map"])
    off = int(c.get("offset", 0))
    d = c["direction"]
    out = []
    for (x, y) in mi.edges[d]:
        there = {"down": (x - off, 0), "up": (x - off, other.h - 1),
                 "left": (other.w - 1, y - off), "right": (0, y - off)}[d]
        if (x, y) in mi.reachable and (x, y) not in mi.blocked_by_objects and there in other.walkable \
                and mapcheck.can_move(mi.elevation[(x, y)], other.elevation[there]):
            out.append(((x, y), there))
    return out


def strata_maps():
    return sorted(d for d in os.listdir(os.path.join(ROOT, "data/maps")) if d.startswith("Strata"))


def maps_by_act():
    by = {}
    for name in strata_maps():
        mi = MapInfo(name)
        by.setdefault(mi.act, []).append(mi)
    return by
