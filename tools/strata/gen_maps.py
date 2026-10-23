#!/usr/bin/env python3
"""Generate Strata map layouts and map headers from the package tools/strata/maps/.

Usage (from the repo root):
  python3 tools/strata/gen_maps.py [--render DIR]

Each Strata map's layout is cut from a hand-made stock map with a matching
terrain and tileset (a placeholder until Strata has its own tilesets), then
patched to remove anything man-made. Writes, for every map in the maps package:
  data/layouts/<Name>/map.bin, border.bin   (if the map has a `crop`)
  data/layouts/layouts.json                 layout entry
  data/maps/<Name>/map.json                 header, connections and events
  data/maps/map_groups.json                 membership of gMapGroup_Strata
  src/data/region_map/region_map_sections.json   MAPSEC entries
  src/data/heal_locations.json              HEAL_LOCATION entries
  src/data/wild_encounters.json             wild encounters of maps with `encounters`
Map scripts (data/maps/<Name>/scripts.inc) are written by hand and never touched.
With --render, also draws every generated layout to DIR/<Name>.png.
"""

import json
import os
import struct
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from maps import HEAL_LOCATIONS, MAPS, MAP_SECTIONS, SECRET_BASE_SWAPS  # noqa: E402
import maprender  # noqa: E402

GROUP = "gMapGroup_Strata"
SIGNPOST_METATILES = (0x003, 0x01B)   # General: the blue route sign and the wooden signpost


def path(*parts):
    return os.path.join(ROOT, *parts)


def load_json(rel):
    with open(path(rel)) as f:
        return json.load(f)


def save_json(rel, data):
    with open(path(rel), "w") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def read_blocks(layout):
    w, h = layout["width"], layout["height"]
    data = open(path(layout["blockdata_filepath"]), "rb").read()
    blocks = list(struct.unpack(f"<{w * h}H", data))
    return [blocks[y * w:(y + 1) * w] for y in range(h)]


def build_layout(m, layouts_by_id):
    """Crops and patches the source layout. Returns (layout entry, rows)."""
    src = layouts_by_id[m["crop"]["from"]]
    rows = read_blocks(src)
    x0, y0, w, h = m["crop"]["rect"]
    out = [row[x0:x0 + w] for row in rows[y0:y0 + h]]
    for patch in m.get("patches", []):
        # Fill a rect (in the new map's coordinates) with a block. Where it comes from:
        #   like=(sx, sy)      the block of the SOURCE layout at (sx, sy): metatile,
        #                      collision and elevation (no metatile IDs hard-coded);
        #   same_as=(x, y)     the block of the map being built, at (x, y), as patched so
        #                      far (nicer than `like` when the source has a good tile nearby);
        #   metatile=0x2A3     a raw metatile ID, with `collision` (default 0, passable) and
        #                      `elevation` (default: keep each target block's elevation).
        #   tiles=[[a, b], [c, d]] with at=(x, y) instead of rect: a grid of raw metatiles
        #                      (same `collision` and `elevation` options).
        if "tiles" in patch:
            px, py = patch["at"]
            for dy, trow in enumerate(patch["tiles"]):
                for dx, tile in enumerate(trow):
                    elev = patch["elevation"] if "elevation" in patch else out[py + dy][px + dx] >> 12
                    out[py + dy][px + dx] = tile | (patch.get("collision", 0) << 10) | (elev << 12)
            continue
        px, py, pw, ph = patch["rect"]
        if "like" in patch:
            sx, sy = patch["like"]
            block = rows[sy][sx]
        elif "same_as" in patch:
            sx, sy = patch["same_as"]
            block = out[sy][sx]
        else:
            block = None
        for y in range(py, py + ph):
            for x in range(px, px + pw):
                if block is not None:
                    out[y][x] = block
                else:
                    elev = patch["elevation"] if "elevation" in patch else out[y][x] >> 12
                    out[y][x] = patch["metatile"] | (patch.get("collision", 0) << 10) | (elev << 12)
    # Metatile swaps: every block showing metatile `old` shows `new` instead, keeping its
    # collision and elevation; a (new, collision) tuple sets the collision too. The global
    # table removes Hoenn secret-base entrances, which are interactive.
    swaps = dict(SECRET_BASE_SWAPS)
    swaps.update(m.get("swap", {}))
    if swaps:
        for row in out:
            for x, block in enumerate(row):
                new = swaps.get(block & 0x3FF)
                if new is None:
                    continue
                collision = (block >> 10) & 3
                if isinstance(new, tuple):
                    new, collision = new
                row[x] = new | (collision << 10) | (block & 0xF000)
    # Stock signposts that carry no sign event are dead props: draw the ground instead,
    # copied from the first walkable neighbour.
    signs = {(e["x"], e["y"]) for e in m.get("bgs", [])}
    for y, row in enumerate(out):
        for x, block in enumerate(row):
            if (block & 0x3FF) not in SIGNPOST_METATILES or (x, y) in signs:
                continue
            around = [out[ny][nx] for ny in range(y - 1, y + 2) for nx in range(x - 1, x + 2)
                      if 0 <= ny < len(out) and 0 <= nx < len(row) and (nx, ny) != (x, y)]
            ground = [b for b in around if not (b >> 10) & 3 and (b & 0x3FF) not in SIGNPOST_METATILES]
            if ground:
                row[x] = max(ground, key=ground.count)
    name = m["name"]
    os.makedirs(path("data/layouts", name), exist_ok=True)
    with open(path("data/layouts", name, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{w * h}H", *[b for row in out for b in row]))
    with open(path(src["border_filepath"]), "rb") as f:
        border = f.read()
    with open(path("data/layouts", name, "border.bin"), "wb") as f:
        f.write(border)
    # Era variants reuse a crop with palette-variant tilesets (gen_tilesets.py).
    primary, secondary = m["crop"].get("tilesets", (src["primary_tileset"], src["secondary_tileset"]))
    entry = {
        "id": layout_id(m),
        "name": f"{name}_Layout",
        "width": w,
        "height": h,
        "primary_tileset": primary,
        "secondary_tileset": secondary,
        "border_filepath": f"data/layouts/{name}/border.bin",
        "blockdata_filepath": f"data/layouts/{name}/map.bin",
        "layout_version": "emerald",
    }
    return entry, out


def layout_id(m):
    return m.get("layout") or "LAYOUT_" + map_const(m)[len("MAP_"):]


def map_const(m):
    return m["id"]


def resolve_elevations(m, rows):
    """Coord triggers only fire when their elevation matches the tile's, so a
    trigger with elevation None takes the elevation of the block under it."""
    for event in m.get("coords", []):
        if event["elevation"] is None:
            event["elevation"] = rows[event["y"]][event["x"]] >> 12


def build_header(m):
    header = {
        "id": m["id"],
        "name": m["name"],
        "layout": layout_id(m),
        "music": m["music"],
        "region": "REGION_HOENN",
        "region_map_section": m["mapsec"],
        "requires_flash": False,
        "weather": m.get("weather", "WEATHER_NONE"),
        "map_type": m["map_type"],
        "allow_cycling": m["map_type"] != "MAP_TYPE_INDOOR",
        "allow_escaping": False,
        "allow_running": m["map_type"] != "MAP_TYPE_INDOOR",
        "show_map_name": m["map_type"] != "MAP_TYPE_INDOOR",
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
        "connections": m.get("connections") or None,
        "object_events": m.get("objects", []),
        "warp_events": m.get("warps", []),
        "coord_events": m.get("coords", []),
        "bg_events": m.get("bgs", []),
    }
    return header


ENCOUNTER_RATES = {"land_mons": 20, "water_mons": 4, "rock_smash_mons": 20, "fishing_mons": 30}


def update_encounters():
    data = load_json("src/data/wild_encounters.json")
    group = next(g for g in data["wild_encounter_groups"] if g["label"] == "gWildMonHeaders")
    strata_maps = {m["id"] for m in MAPS}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in strata_maps]
    for m in MAPS:
        if "encounters" not in m:
            continue
        entry = {"map": m["id"], "base_label": "g" + m["name"]}
        for kind, slots in m["encounters"].items():
            entry[kind] = {"encounter_rate": ENCOUNTER_RATES[kind], "mons": slots}
        group["encounters"].append(entry)
    save_json("src/data/wild_encounters.json", data)


def update_heal_locations():
    data = load_json("src/data/heal_locations.json")
    ours = {h["id"] for h in HEAL_LOCATIONS}
    data["heal_locations"] = [h for h in data["heal_locations"] if h["id"] not in ours] + HEAL_LOCATIONS
    save_json("src/data/heal_locations.json", data)


GENERATED = "// DO NOT MODIFY: generated by tools/strata/gen_maps.py from tools/strata/maps.py\n"


def write_arrivals():
    """Where the rig drops the player in each act's map, for `warp` in scripts."""
    lines = [GENERATED, "#ifndef GUARD_CONSTANTS_STRATA_MAPS_H", "#define GUARD_CONSTANTS_STRATA_MAPS_H", ""]
    for m in MAPS:
        if "arrival" in m:
            name = m["id"][len("MAP_STRATA_"):]
            lines.append(f"#define STRATA_ARRIVAL_{name} {m['arrival'][0]}, {m['arrival'][1]}")
    lines += ["", "#endif // GUARD_CONSTANTS_STRATA_MAPS_H"]
    with open(path("include/constants/strata_maps.h"), "w") as f:
        f.write("\n".join(lines) + "\n")


def write_map_eras():
    """Which era each deep-time map belongs to (for tests and era-aware code)."""
    lines = [GENERATED, "static const struct { u16 map; u8 era; } sStrataMapEras[] =", "{"]
    for m in MAPS:
        if "era" in m:
            lines.append(f"    {{ {m['id']}, {m['era']} }},")
    lines.append("};")
    with open(path("src/data/strata_map_eras.h"), "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    render_dir = sys.argv[sys.argv.index("--render") + 1] if "--render" in sys.argv else None

    layouts = load_json("data/layouts/layouts.json")
    by_id = {l["id"]: l for l in layouts["layouts"] if "id" in l}
    for m in MAPS:
        if "crop" not in m:
            continue
        entry, rows = build_layout(m, by_id)
        resolve_elevations(m, rows)
        if entry["id"] in by_id:
            idx = layouts["layouts"].index(by_id[entry["id"]])
            layouts["layouts"][idx] = entry
        else:
            layouts["layouts"].append(entry)
        by_id[entry["id"]] = entry
    save_json("data/layouts/layouts.json", layouts)

    groups = load_json("data/maps/map_groups.json")
    if GROUP not in groups:
        groups["group_order"].append(GROUP)
    groups[GROUP] = [m["name"] for m in MAPS]
    save_json("data/maps/map_groups.json", groups)

    for m in MAPS:
        os.makedirs(path("data/maps", m["name"]), exist_ok=True)
        save_json(f"data/maps/{m['name']}/map.json", build_header(m))
        scripts = path("data/maps", m["name"], "scripts.inc")
        if not os.path.exists(scripts):
            with open(scripts, "w") as f:
                f.write(f"{m['name']}_MapScripts::\n\t.byte 0\n")

    sections = load_json("src/data/region_map/region_map_sections.json")
    existing = {s["id"] for s in sections["map_sections"]}
    for sid, name in MAP_SECTIONS:
        if sid not in existing:
            sections["map_sections"].append({"id": sid, "name": name})
    save_json("src/data/region_map/region_map_sections.json", sections)

    update_encounters()
    update_heal_locations()
    write_arrivals()
    write_map_eras()

    if render_dir:
        os.makedirs(render_dir, exist_ok=True)
        for m in MAPS:
            if "crop" in m:
                maprender.render_map(layout_id(m), os.path.join(render_dir, f"{m['name']}.png"),
                                     show_collision="--collision" in sys.argv)
                print("rendered", m["name"])


if __name__ == "__main__":
    main()
