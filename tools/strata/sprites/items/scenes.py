"""Full-screen backgrounds: the starter choice's field case (replacing Birch's
bag) and the big capsule of the cave battle transition (B_TRANSITION_BIG_POKEBALL).
Both are drawn as role grids, cut into 8x8 tiles, deduplicated with flips and
written back as tileset PNG + tilemap .bin in the stock formats."""

import struct

from . import capsule as C
from .grid import Grid, read_indexed, write_png8
from .targets import TRANSITION, path, transition_palette
from ..core.image import write_indexed_png

SCREEN_W, SCREEN_H = 240, 160


def fill_poly(g, pts, role):
    ys = [p[1] for p in pts]
    for y in range(max(0, int(min(ys))), min(g.h, int(max(ys)) + 1)):
        py = y + 0.5
        xs = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            if (y1 <= py < y2) or (y2 <= py < y1):
                xs.append(x1 + (py - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            for x in range(max(0, int(round(a))), min(g.w, int(round(b)))):
                g.px[y][x] = role(x, y) if callable(role) else role


def fill_ellipse(g, cx, cy, rx, ry, role):
    for y in range(max(0, int(cy - ry - 1)), min(g.h, int(cy + ry + 2))):
        for x in range(max(0, int(cx - rx - 1)), min(g.w, int(cx + rx + 2))):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                g.px[y][x] = role(x, y) if callable(role) else role


def rect(g, x0, y0, x1, y1, role):
    fill_poly(g, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], role)


# --- tiles ------------------------------------------------------------------------

def tiles_of(rows, tw, th):
    """8x8 tiles of an index image, row-major; returns list of tuples-of-tuples."""
    out = []
    for ty in range(th):
        for tx in range(tw):
            out.append(tuple(tuple(rows[ty * 8 + y][tx * 8:tx * 8 + 8]) for y in range(8)))
    return out


def variants(t):
    """(tile, hflip, vflip) for the four flips of a tile."""
    h = tuple(tuple(reversed(r)) for r in t)
    return [(t, 0, 0), (h, 1, 0), (tuple(reversed(t)), 0, 1), (tuple(reversed(h)), 1, 1)]


def dedupe(tiles, reserved):
    """Assigns each tile a slot: 0 for blank, else a unique tile (matching
    flips). `reserved` is the iterator of free slot numbers.
    Returns (map entries without palette bits, {slot: tile})."""
    blank = tuple(tuple([0] * 8) for _ in range(8))
    seen, placed, entries = {}, {}, []
    for t in tiles:
        if t == blank:
            entries.append(0)
            continue
        hit = None
        for v, hf, vf in variants(t):
            if v in seen:
                hit = seen[v] | (hf << 10) | (vf << 11)
                break
        if hit is None:
            slot = next(reserved)
            seen[t] = slot
            placed[slot] = t
            hit = slot
        entries.append(hit)
    return entries, placed


# --- starter choice: the field case ----------------------------------------------

CASE_COLOURS = {      # bank 0 of starter_choose/tiles.png (index 0 is the backdrop)
    "o": (28, 32, 22), "sh0": (46, 56, 34), "sh1": (70, 84, 48), "sh2": (98, 114, 66), "sh3": (138, 152, 94),
    "f0": (34, 36, 40), "f1": (56, 60, 64), "f2": (80, 86, 90),
    "m0": (140, 148, 150), "m1": (214, 220, 214),
    "lab": (232, 224, 196), "tag": (180, 70, 46), "ink": (92, 84, 64), "shadow": (70, 122, 58),
}
CASE_INDEX = {k: i + 1 for i, k in enumerate(CASE_COLOURS)}


def case_grid():
    """An open olive field case, lid up, foam inside with three empty capsule
    wells: the three capsules (sprites at (60,64) (120,88) (180,64)) came out
    of it. Lit from the upper left like the creature sprites."""
    g = Grid(SCREEN_W, SCREEN_H)
    fill_ellipse(g, 120, 66, 58, 9, "shadow")
    # lid, opened back past upright: rim, then the foam lining
    lid = [(80, 8), (160, 8), (158, 38), (82, 38)]
    fill_poly(g, lid, lambda x, y: "sh2" if x < 120 else "sh1")
    fill_poly(g, [(84, 11), (156, 11), (154, 35), (86, 35)],
              lambda x, y: "f1" if ((x // 3) + (y // 3)) % 2 else "f2")
    # sample sheet clipped to the lid lining
    rect(g, 106, 14, 134, 29, "lab")
    rect(g, 106, 14, 134, 17, "tag")
    for ly in (20, 23, 26):
        rect(g, 109, ly, 128 if ly != 26 else 121, ly + 1, "ink")
    # base: top rim and the foam tray, front face
    fill_poly(g, [(78, 38), (162, 38), (166, 50), (74, 50)], "sh3")
    fill_poly(g, [(81, 40), (159, 40), (162, 48), (78, 48)], "f1")
    for wx in (98, 120, 142):                           # the three empty wells
        fill_ellipse(g, wx, 44.2, 7, 3, "f0")
        fill_ellipse(g, wx - 1, 43.6, 5, 1.6, "o")
    rect(g, 74, 50, 166, 64, lambda x, y: "sh2" if x < 92 else ("sh1" if x < 150 else "sh0"))
    rect(g, 74, 50, 166, 52, "sh3")                     # front lip catches the light
    rect(g, 74, 62, 166, 64, "sh0")
    # hardware: hinges, latches, handle
    for hx in (90, 146):
        rect(g, hx, 36, hx + 5, 40, "m0")
        rect(g, hx, 36, hx + 5, 37, "m1")
    for lx in (86, 150):
        rect(g, lx, 49, lx + 5, 57, "m0")
        rect(g, lx, 49, lx + 5, 51, "m1")
        rect(g, lx + 1, 56, lx + 4, 57, "o")
    rect(g, 110, 55, 131, 58, "m0")
    rect(g, 110, 55, 131, 56, "m1")
    rect(g, 108, 54, 110, 60, "m0")
    rect(g, 131, 54, 133, 60, "m0")
    # stencilled field number on the front
    for i, sx in enumerate((96, 100, 104)):
        rect(g, sx, 58 - (i == 1), sx + 2, 61, "sh3")
    out = Grid(SCREEN_W, SCREEN_H)
    out.px = [row[:] for row in g.px]
    # outline only the case, not its shadow
    for y in range(g.h):
        for x in range(g.w):
            if g.px[y][x] in (None, "shadow") and any(
                    g.get(x + dx, y + dy) not in (None, "shadow", "o")
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out.px[y][x] = "o"
    return out


def starter_case(written):
    tiles_rel = "graphics/starter_choose/tiles.png"
    bag_rel = "graphics/starter_choose/birch_bag.bin"
    grass_rel = "graphics/starter_choose/birch_grass.bin"
    rows, pal = read_indexed(path(tiles_rel))
    grass = open(path(grass_rel), "rb").read()
    grass_tiles = {e & 0x3FF for e in struct.unpack("<%dH" % (len(grass) // 2), grass)}
    nslots = (len(rows) // 8) * (len(rows[0]) // 8)
    ntx = len(rows[0]) // 8
    # clear every tile the grass does not use (the old bag)
    for slot in range(1, nslots):
        if slot not in grass_tiles:
            for y in range(8):
                for x in range(8):
                    rows[(slot // ntx) * 8 + y][(slot % ntx) * 8 + x] = 0
    g = case_grid()
    img = [[CASE_INDEX[v] if v else 0 for v in r] for r in g.px]
    free = iter([s for s in range(1, nslots) if s not in grass_tiles])
    entries, placed = dedupe(tiles_of(img, 30, 20), free)
    for slot, t in placed.items():
        for y in range(8):
            for x in range(8):
                rows[(slot // ntx) * 8 + y][(slot % ntx) * 8 + x] = t[y][x]
    tilemap = []
    for ty in range(20):
        tilemap += entries[ty * 30:(ty + 1) * 30] + [0, 0]
    with open(path(bag_rel), "wb") as f:
        f.write(struct.pack("<%dH" % len(tilemap), *tilemap))
    pal = list(pal)
    for k, i in CASE_INDEX.items():
        pal[i] = CASE_COLOURS[k]
    write_png8(path(tiles_rel), rows, pal)
    written += [tiles_rel, bag_rel]
    print(f"starter case: {len(placed)} tiles")


# --- cave battle transition --------------------------------------------------------

def big_emblem(written):
    """battle_transitions/big_pokeball.png (+ _map.bin, 30x20): one big capsule,
    in the shared transition palette (field_effects/palettes/pokeball.pal)."""
    cap = C.capsule(r=50, e=13, side=64, lid=16, handle=12, marking="label")
    x0, y0, x1, y1 = cap.bbox()
    g = Grid(SCREEN_W, SCREEN_H)
    ox = 120 - (x0 + x1 + 1) // 2
    oy = 80 - (y0 + y1 + 1) // 2
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if cap.px[y][x] is not None:
                g.set(x + ox, y + oy, cap.px[y][x])
    img = [[TRANSITION[v] if v else 0 for v in r] for r in g.px]
    entries, placed = dedupe(tiles_of(img, 30, 20), iter(range(1, 1024)))
    n = len(placed) + 1
    if n > 256:
        raise SystemExit(f"gen_item_art: big transition capsule needs {n} tiles (keep it under 256)")
    cols = 4
    sheet = [[0] * (cols * 8) for _ in range(((n + cols - 1) // cols) * 8)]
    for slot, t in placed.items():
        for y in range(8):
            for x in range(8):
                sheet[(slot // cols) * 8 + y][(slot % cols) * 8 + x] = t[y][x]
    rel = "graphics/battle_transitions/big_pokeball.png"
    write_indexed_png(path(rel), sheet, transition_palette())
    with open(path("graphics/battle_transitions/big_pokeball_map.bin"), "wb") as f:
        f.write(struct.pack("<%dH" % len(entries), *entries))
    written += [rel, "graphics/battle_transitions/big_pokeball_map.bin"]
    print(f"big transition capsule: {n} tiles")
