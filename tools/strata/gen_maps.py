#!/usr/bin/env python3
"""Generate Strata map layouts and map headers from tools/strata/maps.py.

Usage (from the repo root):
  python3 tools/strata/gen_maps.py [--render DIR]

Each Strata map's layout is cut from a hand-made stock map with a matching
terrain and tileset (a placeholder until Strata has its own tilesets), then
patched to remove anything man-made. Writes, for every map in maps.py:
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
from maps import HEAL_LOCATIONS, MAPS, MAP_SECTIONS  # noqa: E402
import maprender  # noqa: E402

GROUP = "gMapGroup_Strata"


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
        # Fill a rect (in the new map's coordinates) with a block taken from the
        # source map at `like`, so no metatile IDs are hard-coded.
        sx, sy = patch["like"]
        block = rows[sy][sx]
        px, py, pw, ph = patch["rect"]
        for y in range(py, py + ph):
            for x in range(px, px + pw):
                out[y][x] = block
    name = m["name"]
    os.makedirs(path("data/layouts", name), exist_ok=True)
    with open(path("data/layouts", name, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{w * h}H", *[b for row in out for b in row]))
    with open(path(src["border_filepath"]), "rb") as f:
        border = f.read()
    with open(path("data/layouts", name, "border.bin"), "wb") as f:
        f.write(border)
    entry = {
        "id": layout_id(m),
        "name": f"{name}_Layout",
        "width": w,
        "height": h,
        "primary_tileset": src["primary_tileset"],
        "secondary_tileset": src["secondary_tileset"],
        "border_filepath": f"data/layouts/{name}/border.bin",
        "blockdata_filepath": f"data/layouts/{name}/map.bin",
        "layout_version": "emerald",
    }
    return entry


def layout_id(m):
    return m.get("layout") or "LAYOUT_" + map_const(m)[len("MAP_"):]


def map_const(m):
    return m["id"]


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


def main():
    render_dir = sys.argv[sys.argv.index("--render") + 1] if "--render" in sys.argv else None

    layouts = load_json("data/layouts/layouts.json")
    by_id = {l["id"]: l for l in layouts["layouts"] if "id" in l}
    for m in MAPS:
        if "crop" not in m:
            continue
        entry = build_layout(m, by_id)
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

    if render_dir:
        os.makedirs(render_dir, exist_ok=True)
        for m in MAPS:
            if "crop" in m:
                maprender.render_map(layout_id(m), os.path.join(render_dir, f"{m['name']}.png"),
                                     show_collision="--collision" in sys.argv)
                print("rendered", m["name"])


if __name__ == "__main__":
    main()
