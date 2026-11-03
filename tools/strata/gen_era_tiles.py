#!/usr/bin/env python3
"""Era ground cover: tile art that replaces Hoenn grass in the eras before grasslands.

Grasses existed by the latest Cretaceous, but they were rare until the Oligocene and only
formed grasslands in the Miocene. So in Acts 1-5 the stock tall grass, long grass and lawn
are redrawn as each era's undergrowth and ground; the metatile *behaviours* stay, so wild
encounters, the grass field effects and battle environments work as before.

This module holds the art and is driven by gen_tilesets.py (run that, not this):

    python3 tools/strata/gen_tilesets.py                writes everything
    python3 tools/strata/gen_era_tiles.py --preview DIR  review sheets (after gen_tilesets.py)

Per ground (GROUNDS below) it makes:
  - General primary tiles: lawn (tiles 0x002/0x003), tall grass 0x00D (tiles 0x010/0x011/
    0x020/0x021) and long grass 0x015 (tiles 0x012/0x013/0x022/0x023), drawn in palette 2;
  - Fortree's long-grass south edge 0x208 (tiles 0x30A/0x30B/0x31A/0x31B) and, for the PETM,
    Fallarbor's ash grass 0x20A and the "normal grass" 0x212 it turns into when walked on;
  - a ground recolour: the three stock lawn colours become the era's ground ramp in every
    palette of the variant, so the ground under trees, signs and cliff edges matches;
  - field-effect sprites: the tall-grass and long-grass overlays drawn over the player;
  - battle backgrounds: the tall- and long-grass environments' platforms (tiles + palette)
    and their entry animation (the wall of plants that slides past at the start of a wild
    battle), and the plain environment's palette.
Everything is drawn from code (fronds, fans, leaves, stems) with a fixed random seed, so
the output is reproducible.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maprender import ROOT, read_pal, read_png, write_png  # noqa: E402
from sprites.core.image import write_indexed_png  # noqa: E402

# --- Roles -------------------------------------------------------------------
#
# Art is drawn in one-character roles; each target palette maps roles to indices.
#   ground:  '.' base   ',' dark   "'" light          (the recoloured lawn ramp)
#   plants:  'l' light  'm' mid    'd' dark   'o' darkest/outline   't' teal shade
#   browns:  'p' tan    'r' rust   'g' grey-brown     'b' dark brown  'y' peach  'a' red
# General palette 2 (stock): 1 (180,255,131) 2 (131,197,98) 3 (57,139,49) 4 (57,82,0)
# 5 (222,148,115) 6 (106,90,90) 7 (164,98,90) 8 (65,57,49) 9 (255,197,148) A (222,106,98)
# B (205,65,82) C/D/E lawn (164,213,197) (115,197,164) (65,180,131) F (24,164,106).
PAL2_ROLES = {".": 13, ",": 14, "'": 12, "l": 1, "m": 2, "d": 3, "o": 4, "t": 15,
              "p": 5, "g": 6, "r": 7, "b": 8, "y": 9, "a": 10}
GROUND_ROLES = (".", ",", "'")

# The stock lawn ramp (light, base, dark) as it appears in every Hoenn palette, and the
# teal of the ground shadow around trees (palette 2 index 15).
LAWN_RGB = ((164, 213, 197), (115, 197, 164), (65, 180, 131), (24, 164, 106))


class Ground:
    """One era's ground cover. `ramp` replaces LAWN_RGB (light, base, dark, tree shadow),
    before the era's colour transform. `accents` are the two brown roles the field-effect
    palette gets (its slots 10/11, otherwise only the ash puff's)."""

    def __init__(self, key, era, label, ramp, accents, tall, long, lawn, notes):
        self.key, self.era, self.label = key, era, label
        self.ramp, self.accents = ramp, accents
        self.tall, self.long, self.lawn, self.notes = tall, long, lawn, notes


# --- Canvas ---------------------------------------------------------------------


class Art:
    """A role canvas. wrap=True draws across the edges (art for tiles that repeat),
    wrap="x" only across the left and right edges (a strip)."""

    def __init__(self, w, h, fill=".", wrap=False):
        self.w, self.h = w, h
        self.wrap_x, self.wrap_y = bool(wrap), wrap is True
        self.px = [[fill] * w for _ in range(h)]

    def _xy(self, x, y):
        if self.wrap_x:
            x %= self.w
        if self.wrap_y:
            y %= self.h
        return (x, y) if 0 <= x < self.w and 0 <= y < self.h else None

    def get(self, x, y):
        p = self._xy(x, y)
        return self.px[p[1]][p[0]] if p else None

    def put(self, x, y, role):
        p = self._xy(int(math.floor(x + 0.5)), int(math.floor(y + 0.5)))
        if p:
            self.px[p[1]][p[0]] = role

    def line(self, x0, y0, x1, y1, role):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 1.5) + 1
        for i in range(n + 1):
            t = i / n
            self.put(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, role)

    def stamp(self, x, y, rows, keep=" "):
        """Pastes a small hand-drawn grid of roles; `keep` characters leave the canvas."""
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch != keep:
                    self.put(x + dx, y + dy, ch)

    def sub(self, x0, y0, w, h):
        return [[self.get(x0 + x, y0 + y) for x in range(w)] for y in range(h)]


def bezier(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def walk(p0, p1, p2, step=0.5):
    """Points every ~step px along a quadratic Bezier, with unit tangents and t."""
    pts = [bezier(p0, p1, p2, i / 200) for i in range(201)]
    out, acc = [], 0.0
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        d = math.hypot(x1 - x0, y1 - y0)
        acc += d
        if acc >= step or i == 1:
            acc = 0.0
            tx, ty = (x1 - x0) / (d or 1), (y1 - y0) / (d or 1)
            out.append((x1, y1, tx, ty, i / 200))
    return out


# --- Plant primitives ---------------------------------------------------------------


def frond(a, base, ctrl, tip, pinna=2.5, rachis="d", upper="l", lower="m", gap=1.5, start=0.15):
    """A pinnate fern frond along a curve: alternating leaflets angled toward the tip,
    shortening to the tip. Leaflets on the lit (upper) side get `upper`."""
    pts = walk(base, ctrl, tip, 0.5)
    dist = 0.0
    side = 0
    for i, (x, y, tx, ty, t) in enumerate(pts):
        dist += 0.5
        if t < start or dist < gap:
            continue
        dist = 0.0
        side ^= 1
        length = pinna * (1 - t) ** 0.6 + 0.7
        nx, ny = (-ty, tx) if side else (ty, -tx)
        dx, dy = nx + tx * 0.7, ny + ty * 0.7
        norm = math.hypot(dx, dy) or 1
        dx, dy = dx / norm, dy / norm
        a.line(x, y, x + dx * length, y + dy * length, upper if ny < 0 or (ny == 0 and side) else lower)
    for x, y, _, _, t in pts:
        a.put(x, y, rachis)


def blade(a, base, ctrl, tip, width=1.5, body="m", rib="d", edge="l"):
    """A broad leaf (lanceolate): widest at the middle, a midrib, a lit upper edge."""
    pts = walk(base, ctrl, tip, 0.35)
    for x, y, tx, ty, t in pts:
        w = width * math.sin(math.pi * min(1.0, t * 1.1)) + 0.3
        nx, ny = -ty, tx
        if ny > 0:
            nx, ny = -nx, -ny          # (nx, ny) points up: the lit side
        k = -w
        while k <= w:
            a.put(x + nx * k, y + ny * k, edge if k > w - 0.8 else body)
            k += 0.4
    for x, y, _, _, t in pts:
        if 0.1 < t < 0.9:
            a.put(x, y, rib)


def fiddlehead(a, x, y, body="m", lit="l"):
    """A young fern frond still curled: the first green after the impact (the fern spike)."""
    a.stamp(x, y, [" ml", "m m", " m ", " m "], keep=" ")
    a.put(x + 2, y, lit)


def shadow(a, plant_roles, below=","):
    """Ground pixels right under a plant pixel get a soft shadow."""
    marks = []
    for y in range(a.h):
        for x in range(a.w):
            if a.px[y][x] in GROUND_ROLES:
                above = a.get(x, y - 1)
                if above is not None and above in plant_roles:
                    marks.append((x, y))
    for x, y in marks:
        a.put(x, y, below)


GREENS = set("lmdot")
PLANT = set("lmdotpgrbya")


def speckle(a, rng, n, roles, area=None):
    x0, y0, x1, y1 = area or (0, 0, a.w, a.h)
    for _ in range(n):
        x, y = rng.randrange(x0, x1), rng.randrange(y0, y1)
        if a.get(x, y) in GROUND_ROLES:
            a.put(x, y, rng.choice(roles))


# --- Lawn (ground) textures: two 8x8 tiles, self-contained so any arrangement or flip
# of them tiles (other metatiles reuse them under trees, signs and edges). -------------

LAWNS = {
    # moss and fallen leaves (forest floor)
    "litter": (["........", ".,...'..", "....gb..", "...b....", "'.......", ".....m,.", "..,..d..", "........"],
               ["........", "..'.....", ".....,..", ".m......", ".d..,...", "......r.", "..,..gb.", "........"]),
    # ash over mud; a dead leaf, a twig
    "ash": (["........", ".'..,...", "......'.", "..gb....", "........", ".,...'..", "....,...", "'......."],
            ["........", "...,..'.", ".'......", "........", "....bbg.", "..,.....", "......,.", ".'......"]),
    # bare soil, a pebble, a little litter, a seedling
    "soil": (["........", ".'......", ".,...,..", "........", "...pr...", "......'.", "..,...,.", "........"],
             ["........", "....,...", "........", ".m...'..", ".d...,..", "........", ",...gr..", "........"]),
    # reddened, cracked soil (PETM)
    "redsoil": (["........", ".,,.....", "...,....", "....,'..", "........", ".'....,.", "......,.", "........"],
                ["........", "....'...", ".m.d....", "..d...,.", "......,,", ".,......", "...'....", "........"]),
    # damp moss cushions and litter by the lake
    "moss": (["........", ".''.....", ".',..,..", "........", "....r...", "......'.", "..,..''.", "......,."],
             ["........", ".....,..", ".m.''...", ".d.',...", "........", "..,.....", "....gr..", "........"]),
}


def lawn_tiles(kind, seed):
    return [[list(row) for row in tile] for tile in LAWNS[kind]]


# --- Tall undergrowth (tall-grass metatile 0x00D): one 16x16 clump on the ground. -----

FRONT = dict(rachis="m", upper="l", lower="m")      # a lit frond
MIDDLE = dict(rachis="d", upper="m", lower="d")
BACK = dict(rachis="o", upper="d", lower="o")       # a frond in shade


def tall_hell_creek(rng):
    """A fern clump: fronds arching out of one crown."""
    a = Art(16, 16)
    frond(a, (8, 14), (1, 8), (0, 12), pinna=2.0, gap=2.0, **BACK)
    frond(a, (8, 14), (15, 8), (16, 12), pinna=2.0, gap=2.0, **BACK)
    frond(a, (8, 14), (3, 2), (1, 6), pinna=2.4, gap=2.0, **MIDDLE)
    frond(a, (8, 14), (13, 2), (15, 6), pinna=2.4, gap=2.0, **MIDDLE)
    frond(a, (8, 14), (6, 3), (5, 1), pinna=2.2, gap=2.0, **FRONT)
    frond(a, (8, 14), (10, 4), (12, 2), pinna=2.2, gap=2.0, **FRONT)
    shadow(a, PLANT)
    return a


DEAD = dict(rachis="b", upper="p", lower="r")
DEAD_BACK = dict(rachis="b", upper="g", lower="b")


def tall_winter(rng):
    """Dead, ash-grey fern fronds slumped over, and the first fiddleheads: after the
    impact, ferns came back first (the "fern spike" in the pollen record)."""
    a = Art(16, 16)
    frond(a, (8, 13), (1, 4), (0, 12), pinna=2.0, gap=2.0, **DEAD_BACK)
    frond(a, (8, 13), (15, 4), (16, 12), pinna=2.0, gap=2.0, **DEAD_BACK)
    frond(a, (8, 13), (5, 2), (2, 6), pinna=2.2, gap=2.0, **DEAD)
    frond(a, (8, 13), (12, 3), (14, 8), pinna=2.0, gap=2.0, **DEAD)
    fiddlehead(a, 7, 8)
    shadow(a, PLANT)
    return a


def fan(a, base, radius, angles, lit="l", mid="m", gap="d", stalk=None):
    """A fan-palm leaf (Sabalites-like): stiff leaflets radiating from the top of the
    stalk, alternately lit, with dark folds between them and ragged tips."""
    if stalk:
        a.line(stalk[0], stalk[1], base[0], base[1], gap)
    angles = list(angles)
    for i, ang in enumerate(angles[:-1]):        # dark folds first
        r = math.radians((ang + angles[i + 1]) / 2)
        a.line(base[0], base[1], base[0] + math.cos(r) * radius * 0.85, base[1] + math.sin(r) * radius * 0.85, gap)
    for i, ang in enumerate(angles):
        r = math.radians(ang)
        length = radius - (i % 2)
        a.line(base[0], base[1], base[0] + math.cos(r) * length, base[1] + math.sin(r) * length, lit if i % 2 == 0 else mid)


def tall_corral(rng):
    """A fan-palm seedling with two stiff cycad-like leaves at its feet."""
    a = Art(16, 16)
    frond(a, (8, 14), (4, 12), (0, 11), pinna=1.8, gap=2.0, rachis="d", upper="m", lower="o")
    frond(a, (8, 14), (12, 12), (16, 11), pinna=1.8, gap=2.0, rachis="d", upper="m", lower="o")
    fan(a, (8, 9), 7.5, range(190, 352, 18), stalk=(8, 14))
    shadow(a, PLANT)
    return a


def tall_petm(rng):
    """Broad, glossy leaves of a ginger-like herb (Zingiberopsis) with a red flower spike."""
    a = Art(16, 16)
    blade(a, (8, 14), (1, 11), (0, 6), 1.8, body="d", rib="o", edge="m")
    blade(a, (8, 14), (15, 11), (16, 6), 1.8, body="d", rib="o", edge="m")
    blade(a, (8, 14), (4, 6), (5, 1), 2.0, body="m", rib="d", edge="l")
    blade(a, (8, 14), (13, 7), (12, 2), 1.8, body="m", rib="d", edge="l")
    a.stamp(8, 5, ["a", "a", "y", "d"])
    shadow(a, PLANT)
    return a


def horsetail(a, x, y0, y1, node=3, stem="m", lit="l", node_role="o", whorl=None, cone=None):
    """An Equisetum stem from y0 (bottom) up to y1: jointed, with dark node bands, short
    whorled branches if `whorl`, and a spore cone (strobilus) on top if `cone`."""
    for y in range(y1, y0 + 1):
        a.put(x, y, stem)
        a.put(x + 1, y, lit)
    for y in range(y0 - node, y1, -node):
        a.put(x, y, node_role)
        a.put(x + 1, y, node_role)
        if whorl:
            a.put(x - 1, y - 1, whorl)
            a.put(x + 2, y - 1, whorl)
    if cone:
        a.stamp(x, y1 - 2, [cone[1] + cone[1], cone[0] + cone[0]])


def tall_green_river(rng):
    """A fern clump between horsetails (Equisetum, with spore cones) at the lake shore."""
    a = Art(16, 16)
    horsetail(a, 1, 13, 3, stem="m", lit="l", whorl="d", cone=("b", "g"))
    horsetail(a, 13, 13, 2, stem="m", lit="l", whorl="d", cone=("b", "g"))
    frond(a, (8, 14), (2, 6), (0, 11), pinna=2.0, gap=2.0, **BACK)
    frond(a, (8, 14), (14, 6), (16, 11), pinna=2.0, gap=2.0, **BACK)
    frond(a, (8, 14), (5, 0), (3, 4), pinna=2.2, gap=2.0, **FRONT)
    frond(a, (8, 14), (11, 0), (13, 4), pinna=2.2, gap=2.0, **FRONT)
    shadow(a, PLANT)
    return a


# --- Long undergrowth (long-grass metatile 0x015): dense, seamless 16x16 cover. -------


def dense(fill_dark="d", fill_deep="o", rng=None, holes=10):
    a = Art(16, 16, fill=fill_dark, wrap=True)
    for _ in range(holes):
        a.put(rng.randrange(16), rng.randrange(16), fill_deep)
    return a


def crowns(a, centres, height, spread, styles, pinna=2.2):
    """Fern crowns (wrapping): from each centre, one frond arching left and one right."""
    for (cx, cy), style in zip(centres, styles):
        for side in (-1, 1):
            frond(a, (cx, cy), (cx + side * spread * 0.3, cy - height), (cx + side * spread, cy - height * 0.6),
                  pinna=pinna, gap=2.0, start=0.05, **style)


def long_hell_creek(rng):
    """A fern brake: overlapping crowns of arching fronds, deep shade between them."""
    a = dense("d", "o", rng, 40)
    crowns(a, [(0, 12), (8, 4)], 8, 7, [BACK, BACK])
    crowns(a, [(4, 16), (12, 8)], 9, 7, [FRONT, FRONT], pinna=2.4)
    return a


def long_winter(rng):
    """Dead fern fronds collapsed over ash-covered mud, a fiddlehead pushing through."""
    a = Art(16, 16, fill=".", wrap=True)
    for _ in range(12):
        a.put(rng.randrange(16), rng.randrange(16), rng.choice("g,b,"))
    for (cx, cy), style in (((0, 12), DEAD_BACK), ((8, 4), DEAD_BACK), ((4, 15), DEAD), ((12, 8), DEAD)):
        for side in (-1, 1):
            frond(a, (cx, cy), (cx + side * 2, cy - 7), (cx + side * 7, cy - 2), pinna=2.0, gap=2.0, start=0.05, **style)
    fiddlehead(a, 10, 11)
    return a


def long_corral(rng):
    """A legume thicket: pinnate leaves of round leaflets in pairs, and hanging pods."""
    a = dense("d", "o", rng, 30)
    shoots = [((1, 15), (3, 9), (7, 7)), ((9, 7), (11, 1), (15, -1)), ((9, 15), (8, 10), (4, 9)),
              ((1, 7), (0, 2), (-4, 1)), ((13, 13), (15, 11), (19, 11))]
    for n, (p0, p1, p2) in enumerate(shoots):
        pts = walk(p0, p1, p2, 0.5)
        for k, (x, y, tx, ty, t) in enumerate(pts):
            a.put(x, y, "o")
            if k % 4 == 2 and t > 0.1:
                a.put(x - ty * 1.3, y + tx * 1.3, "l" if n % 2 == 0 else "m")
                a.put(x + ty * 1.3, y - tx * 1.3, "m" if n % 2 == 0 else "l")
                a.put(x - ty * 2.0 + tx, y + tx * 2.0 + ty, "m")
    for x, y in ((6, 9), (13, 2), (3, 2)):
        a.stamp(x, y, ["b", "p", "p", "r"])
    return a


def long_petm(rng):
    """A thicket of broad herb leaves."""
    a = dense("d", "o", rng, 20)
    for (bx, by, lean), lit in (((2, 18, 1), False), ((10, 10, -1), False), ((6, 14, -1), True), ((14, 22, 1), True)):
        blade(a, (bx, by), (bx + lean * 1, by - 6), (bx + lean * 5, by - 11), 2.0,
              body="m" if lit else "d", rib="o" if lit else "o", edge="l" if lit else "m")
    return a


def long_green_river(rng):
    """A horsetail stand: jointed stems with dark node bands."""
    a = dense("d", "o", rng, 24)
    for i, (x, top) in enumerate(((0, 2), (4, 6), (8, 0), (12, 4))):
        horsetail(a, x, top + 18, top, stem="m", lit="l", node_role="o", whorl="m" if i % 2 else None)
    return a


def root_tile(long_art, rng):
    """The south edge of a long-undergrowth patch (Fortree 0x208): the plants above,
    their dark base and shadow, then open ground."""
    a = Art(16, 16)
    for y in range(11):
        for x in range(16):
            a.px[y][x] = long_art.px[y][x]
    for x in range(16):
        a.px[11][x] = "o" if long_art.px[11][x] in GREENS else long_art.px[11][x]
        a.px[12][x] = "o" if x % 3 else "d"
        a.px[13][x] = ","
    return a


GROUNDS = {
    "hell_creek": Ground(
        "hell_creek", "ERA_HELL_CREEK", "Hell Creek (66 Ma)",
        ramp=((176, 178, 124), (138, 142, 92), (104, 110, 66), (78, 88, 50)), accents=("r", "b"),
        tall=tall_hell_creek, long=long_hell_creek, lawn="litter",
        notes="fern brakes and fern clumps; mossy leaf litter"),
    "impact_winter": Ground(
        "impact_winter", "ERA_IMPACT_WINTER", "impact winter (66 Ma)",
        ramp=((184, 176, 160), (146, 138, 124), (110, 102, 92), (84, 78, 70)), accents=("p", "g"),
        tall=tall_winter, long=long_winter, lawn="ash",
        notes="dead ash-grey ferns with the first fiddleheads (the fern spike); ash over mud"),
    "corral_bluffs": Ground(
        "corral_bluffs", "ERA_CORRAL_BLUFFS", "Corral Bluffs (65.5 Ma)",
        ramp=((204, 184, 138), (172, 150, 106), (136, 114, 80), (108, 90, 62)), accents=("p", "r"),
        tall=tall_corral, long=long_corral, lawn="soil",
        notes="fan-palm and cycad-like seedlings; early legume shrubs with pods; bare soil"),
    "petm": Ground(
        "petm", "ERA_BIGHORN_PETM", "PETM (56 Ma)",
        ramp=((208, 160, 120), (178, 126, 92), (144, 94, 68), (114, 74, 54)), accents=("y", "a"),
        tall=tall_petm, long=long_petm, lawn="redsoil",
        notes="broad-leaved ginger-like herbs and low shrubs; reddened, cracked soil"),
    "green_river": Ground(
        "green_river", "ERA_GREEN_RIVER", "Green River (50 Ma)",
        ramp=((166, 184, 128), (128, 148, 94), (94, 116, 70), (70, 92, 54)), accents=("r", "p"),
        tall=tall_green_river, long=long_green_river, lawn="moss",
        notes="ferns between horsetails at the lake shore; damp moss and litter"),
}

SEED = 66


def designs(key):
    """The role art of one ground: dict of lawn (2 x 8x8), tall, long, root."""
    g = GROUNDS[key]
    rng = random.Random(f"{SEED}-{key}")
    long_art = g.long(rng)
    return {
        "lawn": lawn_tiles(g.lawn, f"{SEED}-{key}-lawn"),
        "tall": g.tall(rng),
        "long": long_art,
        "root": root_tile(long_art, rng),
    }


# --- Palettes ---------------------------------------------------------------------------


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def remap_ground(colors, ground, keep0=True):
    """The stock lawn ramp -> the ground's ramp, in a list of colours."""
    table = dict(zip(LAWN_RGB, GROUNDS[ground].ramp))
    return [c if (keep0 and i % 16 == 0) else table.get(tuple(c), tuple(c)) for i, c in enumerate(colors)]


def tint_to(c, target, strength=1.0):
    """Keeps c's lightness and colourfulness but takes target's hue: turns Hoenn's pale
    greens (sky stripes, plain floors) into the era's ground or haze colour."""
    l, lt = lum(c), lum(target)
    sat = max(c) - min(c)
    sat_t = (max(target) - min(target)) or 1
    k = min(1.5, sat / sat_t) * strength
    out = [l + (t - lt) * k for t in target]
    mixed = [c[i] + (out[i] - c[i]) * strength for i in range(3)]
    return tuple(max(0, min(255, round(v))) for v in mixed)


def role_rgb(ground):
    """Role -> RGB for a ground, from General palette 2 with the ground ramp applied."""
    pal = remap_ground(read_pal(os.path.join(ROOT, "data/tilesets/primary/general/palettes/02.pal")), ground, keep0=False)
    return {r: pal[i] for r, i in PAL2_ROLES.items()}


# --- Field-effect palette and overlays --------------------------------------------------

FE_PAL = "graphics/field_effects/palettes/general_1.pal"
# GENERAL_1 slots the overlays may use (6-9 are the ripples' blues).
FE_ROLE_SLOTS = {".": 13, ",": 14, "'": 12, "l": 1, "m": 2, "d": 3, "o": 4, "t": 15}


def field_effect_palette(ground):
    """GENERAL_1 with the ground ramp and the two accent browns (slots 10/11, the ash
    puff's), before the era transform."""
    pal = remap_ground(read_pal(os.path.join(ROOT, FE_PAL)), ground)
    rgb = role_rgb(ground)
    a, b = GROUNDS[ground].accents
    pal[10], pal[11] = rgb[a], rgb[b]
    return pal


def overlay_index(role, ground, pal):
    if role in FE_ROLE_SLOTS:
        return FE_ROLE_SLOTS[role]
    target = role_rgb(ground)[role]
    cands = [1, 2, 3, 4, 5, 10, 11, 15]
    return min(cands, key=lambda i: sum((pal[i][k] - target[k]) ** 2 for k in range(3)))


def overlay_frames(art, ground, kind, rng):
    """The sprite drawn over a walker's legs, as 16x16 role frames.

    tall (5 frames, anim 1,2,3,4 then 0 stays): 0 is the plants' lower half (rows 8-15),
    1 the whole clump pushed apart, 2-4 the lower half with a few loose leaflets settling.
    long (4 frames, anim 1,2,0,3,0,3,0): the whole patch below the head, swaying."""
    def plants_only(rows):
        return [[r if r is not None and r in PLANT else None for r in row] for row in rows]

    full = plants_only(art.px)
    frames = []
    if kind == "tall":
        low = [[None] * 16 for _ in range(8)] + [row[:] for row in full[8:]]
        frames.append(low)
        pushed = [[None] * 16 for _ in range(16)]
        for y in range(4, 16):
            shift = -1 if y < 10 else 0
            for x in range(16):
                v = full[y][x]
                if v is not None:
                    nx = x + (shift if x < 8 else -shift)
                    if 0 <= nx < 16:
                        pushed[y][nx] = v
        frames.append(pushed)
        lit = [r for r in "lmp" if any(r in row for row in art.px)] or ["m"]
        for n, height in enumerate((3, 5, 7)):
            f = [row[:] for row in low]
            for k in range(3 - n // 2):
                x, y = rng.randrange(2, 14), height + rng.randrange(3)
                f[y][x] = rng.choice(lit)
                if k == 0:
                    f[y + 1][x + 1] = "d"
            frames.append(f)
    else:
        base = [[None] * 16 for _ in range(4)] + [row[:] for row in full[4:]]
        frames.append(base)
        for dx in (1, -1, 1):
            f = [[None] * 16 for _ in range(16)]
            for y in range(16):
                s = dx if y < 9 else 0
                for x in range(16):
                    v = base[y][x]
                    if v is not None and 0 <= x + s < 16:
                        f[y][x + s] = v
            frames.append(f)
    return frames


def write_overlay(path, frames, ground, pal):
    rows = []
    for y in range(16):
        row = []
        for f in frames:
            row += [0 if v is None else overlay_index(v, ground, pal) for v in f[y]]
        rows.append(row)
    write_indexed_png(path, rows, [tuple(c) for c in pal])


# --- Battle backgrounds ----------------------------------------------------------------
#
# Bank-0 slots of the tall/long-grass background palette: 2 platform, 3 platform rim (and
# the stock blade tops), 5/7 (and 8 on long grass) blades, 1/4/6/11-15 sky stripes;
# 8-10 are free on tall grass. The era version uses 2 ground, 3 ground light, 8 ground
# dark, 5 plant dark, 9 plant mid, 7 plant light, 10 accent, and tints the stripes.
BG_SLOTS = {".": 2, "'": 3, ",": 8, "o": 5, "d": 5, "m": 9, "l": 7, "t": 5}
BG_ACCENT = 10

SPRIGS = {
    "hell_creek": [["l l l", " mdm ", "  d  "], [" l l ", "lmdml", " d d "]],
    "impact_winter": [["a a  ", " ama ", "  m  "], ["  a  ", "amama", " m m "]],
    "corral_bluffs": [["l m l", " lml ", "  d  "], ["m l m", " mlm ", "  d  "]],
    "petm": [[" ll ", "lmmd", " dd "], ["ll  ", "mmd ", " d  "]],
    "green_river": [[" l ", "dmd", " m ", "dmd"], [" a ", " m ", "dmd", " m "]],
}


def bg_palette(env, ground):
    """The 48-colour background palette for a grass environment, before the transform."""
    pal = read_pal(os.path.join(ROOT, "graphics/battle_environment", env, "palette.pal"))
    rgb = role_rgb(ground)
    g = GROUNDS[ground]
    haze = rgb["'"]
    out = list(pal)
    for bank in (0, 1):
        o = bank * 16
        for i in (1, 4, 6, 11, 12, 13, 14, 15):
            if pal[o + i] != (0, 0, 0):
                out[o + i] = tint_to(pal[o + i], haze, 0.55)
        out[o + 2], out[o + 3], out[o + 8] = rgb["."], rgb["'"], rgb[","]
        out[o + 5], out[o + 9], out[o + 7] = rgb["d"], rgb["m"], rgb["l"]
        out[o + 10] = rgb[g.accents[0]]
    # bank 2: the entry animation's plants (1 back, 3 front, 2 highlight)
    out[32 + 1], out[32 + 3], out[32 + 2] = rgb["d"], rgb["m"], rgb["l"]
    return out


def plain_palette(ground):
    """The plain environment (boss and trainer battles on open ground): its green floor
    and stripes take the ground's colours."""
    pal = read_pal(os.path.join(ROOT, "graphics/battle_environment/plain/palette.pal"))
    rgb = role_rgb(ground)
    out = []
    for i, c in enumerate(pal):
        if i % 16 == 0 or c == (0, 0, 0):
            out.append(c)
        elif i >= 32:
            out.append(tint_to(c, rgb["m"], 0.9))
        elif c[2] > c[1] or (c[0] > 200 and c[1] > 200 and c[2] > 200 and i % 16 >= 11):
            out.append(c)                       # the sky's blues stay
        else:
            out.append(tint_to(c, rgb["."], 0.85))
    return out


def _interior(idx, x, y, base=2, blades=(3, 5, 7, 8)):
    """True if (x, y) is inside the platform: walking out in all four directions over
    blade pixels reaches the platform colour first."""
    h, w = len(idx), len(idx[0])
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        cx, cy = x + dx, y + dy
        while 0 <= cx < w and 0 <= cy < h and idx[cy][cx] in blades:
            cx, cy = cx + dx, cy + dy
        if not (0 <= cx < w and 0 <= cy < h) or idx[cy][cx] != base:
            return False
    return True


def bg_tiles(env, ground):
    """The background tiles with the grass blades on the platforms replaced by the era's
    sprigs (and a little litter), at the same scattered spots."""
    w, h, idx = read_png(os.path.join(ROOT, "graphics/battle_environment", env, "tiles.png"))
    idx = [row[:] for row in idx]
    rng = random.Random(f"{SEED}-bg-{env}-{ground}")
    interior = [(x, y) for y in range(h) for x in range(w) if idx[y][x] in (3, 5, 7, 8) and _interior(idx, x, y)]
    inside = set(interior)
    for x, y in interior:
        idx[y][x] = 2
    # one sprig per stock blade (a blade is a vertical run; take its top pixel)
    tops = [(x, y) for x, y in interior if (x, y - 1) not in inside]
    sprigs = SPRIGS[ground]
    taken = set()
    for x, y in tops:
        if any(abs(x - tx) < 4 and abs(y - ty) < 3 for tx, ty in taken):
            continue
        rows = rng.choice(sprigs)
        ok = all(idx[y + dy][x - 2 + dx] == 2 for dy in range(len(rows)) for dx, ch in enumerate(rows)
                 if ch != " " and 0 <= y + dy < h and 0 <= x - 2 + dx < w)
        if not ok:
            continue
        taken.add((x, y))
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                px, py = x - 2 + dx, y + dy
                if ch != " " and 0 <= py < h and 0 <= px < w and idx[py][px] == 2:
                    idx[py][px] = BG_ACCENT if ch == "a" else BG_SLOTS[ch]
        # its shadow
        sy = y + len(rows)
        if sy < h and idx[sy][x] == 2:
            idx[sy][x] = 8
    # litter specks between the plants
    for x, y in rng.sample(interior, min(len(interior), 60)):
        if idx[y][x] == 2 and all(idx[y + dy][x + dx] == 2 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                                  if 0 <= y + dy < h and 0 <= x + dx < w):
            idx[y][x] = rng.choice((8, 8, 3, BG_ACCENT))
    return w, h, idx


def bg_anim_tiles(env, ground):
    """The entry animation: a wall of the era's plants, 128 px wide and seamless."""
    w, h, stock = read_png(os.path.join(ROOT, "graphics/battle_environment", env, "anim_tiles.png"))
    rows = 6 if env == "tall_grass" else 10
    hh = rows * 8
    rng = random.Random(f"{SEED}-anim-{env}-{ground}")
    big = Art(128, hh, fill=" ", wrap="x")
    for y in range(hh - 6, hh):
        for x in range(128):
            big.px[y][x] = "1"
    n = 9 if env == "tall_grass" else 11
    for layer, (body, lit, under) in enumerate((("1", "1", "1"), ("3", "2", "3"))):
        for i in range(n):
            bx = (i + 0.5 * layer + rng.uniform(-0.3, 0.3)) * 128 / n
            by = hh + 2
            height = rng.uniform(0.55, 0.95) * hh * (0.85 if layer else 1.0)
            lean = rng.choice((-1, 1)) * rng.uniform(0.15, 0.45) * height
            plant_shape(big, ground, (bx, by), lean, height, body, lit, under, rng)
    # keep tile 0 (top-left 8x8) empty: the tilemap uses it for blank space
    for y in range(8):
        for x in range(8):
            big.px[y][x] = " "
    out = [row[:] for row in stock]
    for y in range(h):
        for x in range(w):
            if y < hh:
                v = big.px[y][x]
                out[y][x] = 0 if v == " " else int(v)
    return w, h, out


def plant_shape(a, ground, base, lean, height, body, lit, under, rng):
    """One plant of the entry wall, in silhouette roles."""
    bx, by = base
    tip = (bx + lean, by - height)
    ctrl = (bx + lean * 0.2, by - height * 0.8)
    if ground in ("hell_creek", "impact_winter"):
        if ground == "impact_winter":     # slumped dead fronds
            tip = (bx + lean * 1.6, by - height * 0.55)
            ctrl = (bx + lean * 0.5, by - height * 1.0)
        frond(a, base, ctrl, tip, pinna=height * 0.16, rachis=body, upper=lit, lower=under, gap=2.0, start=0.1)
        frond(a, (bx + 1, by), ctrl, tip, pinna=height * 0.12, rachis=body, upper=under, lower=under, gap=2.0, start=0.1)
    elif ground == "corral_bluffs" and body == lit:
        # the back row: stiff, cycad-like pinnate leaves
        frond(a, base, (bx + lean * 0.3, by - height * 0.7), (bx + lean * 0.8, by - height * 0.85),
              pinna=height * 0.14, rachis=body, upper=body, lower=body, gap=2.5, start=0.15)
    elif ground == "corral_bluffs":
        cx, cy = bx + lean * 0.3, by - height * 0.55
        a.line(bx, by, cx, cy, body)
        a.line(bx + 1, by, cx + 1, cy, body)
        fan(a, (cx, cy), height * 0.48, range(190, 352, 9), lit=lit, mid=body, gap=under)
    elif ground == "petm":
        blade(a, base, ctrl, tip, height * 0.11, body=body, rib=under, edge=lit)
    elif body == lit:
        # Green River, back row: ferns
        frond(a, base, ctrl, (bx + lean * 1.3, by - height * 0.6), pinna=height * 0.15, rachis=body,
              upper=body, lower=body, gap=2.0, start=0.1)
    else:
        # Green River, front row: horsetails (jointed, whorled, a cone on top)
        for k in range(2):
            x = int(bx + (k * 2 - 1) * 3)
            top = int(by - height * (0.7 + 0.25 * k))
            for y in range(top, int(by) + 1):
                a.put(x, y, body)
                a.put(x + 1, y, lit)
            for y in range(int(by) - 6, top + 2, -6):
                a.put(x, y, lit)
                for d in range(1, 4):
                    a.put(x - d, y - d, body)
                    a.put(x + 1 + d, y - d, body)
            a.stamp(x, top - 4, ["22", "33", "22", "33"])


# --- Tileset writers ---------------------------------------------------------------------


def put_tile(idx, tile, rows8, roles=PAL2_ROLES):
    """Writes an 8x8 role grid at tile number `tile` of an index image (16 tiles a row)."""
    tx, ty = (tile % 16) * 8, (tile // 16) * 8
    for y in range(8):
        for x in range(8):
            idx[ty + y][tx + x] = roles[rows8[y][x]]


def put_metatile(idx, tiles, art_rows, roles=PAL2_ROLES):
    """tiles = (TL, TR, BL, BR) tile numbers; art_rows a 16x16 role grid."""
    for n, t in enumerate(tiles):
        ox, oy = (n % 2) * 8, (n // 2) * 8
        put_tile(idx, t, [row[ox:ox + 8] for row in art_rows[oy:oy + 8]], roles)


def tileset_image(kind, base):
    path = os.path.join(ROOT, "data/tilesets", kind, base, "tiles.png")
    w, h, idx = read_png(path)
    pal = _png_palette(path)
    return w, h, [row[:] for row in idx], pal


def _png_palette(path):
    import struct
    data = open(path, "rb").read()
    pos = 8
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if ctype == b"PLTE":
            chunk = data[pos + 8:pos + 8 + length]
            pal = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
            return (pal + [(0, 0, 0)] * 16)[:16]
        pos += 12 + length
    return [(i * 17,) * 3 for i in range(16)]


# Fallarbor (PETM): ash grass 0x20A (tiles 0x201/0x202/0x211/0x212, palette 11) and the
# grass it becomes when walked on, 0x212 (tiles 0x203/0x204/0x213/0x214, palette 10), on
# the bench's dusty ground (the ash-field tile 0x210, palette 11: B base, A light, C dark).
# These palettes have no greens: the shrub is olive-drab, dusty before it is brushed.
ASH_FIELD_TILE = 0x010
ASH_ROLES = {"l": 10, "m": 13, "d": 14, "o": 14, "p": 9, ",": 12}
SHAKEN_ROLES = {"l": 5, "m": 6, "d": 11, "o": 11, "p": 5, ",": 4}
ASH_TO_SHAKEN = {0xB: 3, 0xA: 2, 0xC: 4, 0x9: 1, 0xD: 5, 0xE: 6}


def petm_scrub(dusty):
    """A dry-season shrub (roles; ' ' shows the ground)."""
    rng = random.Random(f"{SEED}-scrub-{dusty}")
    a = Art(16, 16, fill=" ")
    blade(a, (8, 14), (3, 12), (1, 8), 1.9, body="d", rib="o", edge="m")
    blade(a, (8, 14), (13, 12), (15, 8), 1.9, body="d", rib="o", edge="m")
    blade(a, (8, 14), (5, 8), (4, 3), 2.1, body="m", rib="d", edge="l")
    blade(a, (8, 14), (11, 8), (12, 3), 2.1, body="m", rib="d", edge="l")
    if dusty:
        for _ in range(8):
            x, y = rng.randrange(2, 14), rng.randrange(2, 12)
            if a.px[y][x] != " ":
                a.px[y][x] = "p"
    for y in range(15, 0, -1):          # shadow on the ground under the leaves
        for x in range(16):
            if a.px[y][x] == " " and a.px[y - 1][x] not in (" ", ","):
                a.px[y][x] = ","
    return a


def scrub_metatile(idx, tiles, dusty):
    """Composes the shrub over the ash-field ground into four tiles of `idx`."""
    gx, gy = (ASH_FIELD_TILE % 16) * 8, (ASH_FIELD_TILE // 16) * 8
    ground = [[idx[gy + y][gx + x] for x in range(8)] for y in range(8)]
    art = petm_scrub(dusty)
    roles = ASH_ROLES if dusty else SHAKEN_ROLES
    for n, t in enumerate(tiles):
        ox, oy = (n % 2) * 8, (n // 2) * 8
        tx, ty = (t % 16) * 8, (t // 16) * 8
        for y in range(8):
            for x in range(8):
                r = art.px[oy + y][ox + x]
                g = ground[y][x] if dusty else ASH_TO_SHAKEN.get(ground[y][x], 3)
                idx[ty + y][tx + x] = g if r == " " else roles[r]


def write_variant_tiles(kind, base, ground, out_path):
    """Writes the variant's tiles.png: the base tileset's tiles with the era's ground
    cover. Returns False if this base has no ground-cover tiles (palette-only variant)."""
    if base not in ("general", "fortree") and not (base == "fallarbor" and ground == "petm"):
        return False
    w, h, idx, png_pal = tileset_image(kind, base)
    d = designs(ground)
    if base == "general":
        put_tile(idx, 0x002, d["lawn"][0])
        put_tile(idx, 0x003, d["lawn"][1])
        put_metatile(idx, (0x010, 0x011, 0x020, 0x021), d["tall"].px)
        put_metatile(idx, (0x012, 0x013, 0x022, 0x023), d["long"].px)
    elif base == "fortree":
        put_metatile(idx, (0x10A, 0x10B, 0x11A, 0x11B), d["root"].px)
    else:
        scrub_metatile(idx, (0x001, 0x002, 0x011, 0x012), True)
        scrub_metatile(idx, (0x003, 0x004, 0x013, 0x014), False)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    write_indexed_png(out_path, idx, png_pal)
    return True


# --- Era art (battle backgrounds and field effects) -----------------------------------------


def write_era_art(ground, transform_pal, out_bg, out_fe):
    """Writes this ground's battle-background tiles/anim/palettes and field-effect pics
    and palette. transform_pal(colors) applies the era's colour transform (or nothing).
    Returns a dict of the files written, for the C tables."""
    files = {}
    os.makedirs(out_bg, exist_ok=True)
    os.makedirs(out_fe, exist_ok=True)
    stock_pal = _png_palette(os.path.join(ROOT, "graphics/battle_environment/tall_grass/tiles.png"))
    for env in ("tall_grass", "long_grass"):
        w, h, idx = bg_tiles(env, ground)
        p = os.path.join(out_bg, f"{env}_tiles.png")
        write_indexed_png(p, idx, stock_pal)
        files[f"{env}_tiles"] = p
        w, h, idx = bg_anim_tiles(env, ground)
        p = os.path.join(out_bg, f"{env}_anim_tiles.png")
        write_indexed_png(p, idx, stock_pal)
        files[f"{env}_anim"] = p
        files[f"{env}_pal"] = transform_pal(bg_palette(env, ground))
    files["plain_pal"] = transform_pal(plain_palette(ground))
    fe_pal = field_effect_palette(ground)
    d = designs(ground)
    rng = random.Random(f"{SEED}-fe-{ground}")
    for kind in ("tall", "long"):
        p = os.path.join(out_fe, f"{kind}_grass_{ground}.png")
        write_overlay(p, overlay_frames(d[kind], ground, kind, rng), ground, fe_pal)
        files[f"fe_{kind}"] = p
    files["fe_pal"] = transform_pal(fe_pal)
    return files


# --- Preview -----------------------------------------------------------------------------


def preview(outdir):
    """Per ground: a patch of map (lawn, tall and long undergrowth, the south edge) from the
    generated variant tilesets, the overlay frames, and the grass battle background with its
    entry wall. Run gen_tilesets.py first."""
    import maprender as mr
    import gen_tilesets as gt
    os.makedirs(outdir, exist_ok=True)
    s = 4
    layout = [[0x001, 0x001, 0x00D, 0x00D, 0x001, 0x0C6, 0x001, 0x001],
              [0x001, 0x00D, 0x00D, 0x00D, 0x001, 0x0C7, 0x015, 0x015],
              [0x015, 0x015, 0x015, 0x001, 0x001, 0x001, 0x015, 0x015],
              [0x015, 0x015, 0x015, 0x00D, 0x001, 0x00E, 0x208, 0x208],
              [0x208, 0x208, 0x208, 0x001, 0x001, 0x001, 0x001, 0x001]]
    sheets = []
    for key in list(GROUNDS) + ["stock"]:
        if key == "stock":
            prim, sec = "general", "fortree"
        else:
            prim = next(v for v, spec in gt.VARIANTS.items() if spec[0] == "primary" and spec[4] == key)
            sec = next((v for v, spec in gt.VARIANTS.items() if spec[1] == "fortree" and spec[4] == key), "fortree")
        tp = mr.TilesetPair(mr.tileset_dir(prim), mr.tileset_dir(sec))
        img = [[(0, 0, 0)] * (8 * 16 * s) for _ in range(5 * 16 * s)]
        for r, row in enumerate(layout):
            for c, mid in enumerate(row):
                px = tp.render(mid)
                for y in range(16 * s):
                    for x in range(16 * s):
                        img[r * 16 * s + y][c * 16 * s + x] = px[y // s][x // s]
        mr.draw_text(img, 2, 2, key)
        sheets.append(img)
        path = os.path.join(outdir, f"ground_{key}.png")
        write_png(path, len(img[0]), len(img), img)
        print("wrote", path)
    # overlays and battle backgrounds
    for key in GROUNDS:
        transform = gt.GROUND_ERAS[key][1]
        fe = os.path.join(ROOT, f"graphics/field_effects/pics/strata/tall_grass_{key}.png")
        fe_long = os.path.join(ROOT, f"graphics/field_effects/pics/strata/long_grass_{key}.png")
        pal = read_pal(os.path.join(ROOT, f"graphics/field_effects/palettes/strata/general_1_{gt.era_suffix(key)}.pal"))
        rows = []
        for path in (fe, fe_long):
            w, h, idx = read_png(path)
            for y in range(h * 6):
                rows.append([pal[idx[y // 6][x // 6]] if idx[y // 6][x // 6] else (96, 96, 96) for x in range(w * 6)])
        wmax = max(len(r) for r in rows)
        rows = [r + [(96, 96, 96)] * (wmax - len(r)) for r in rows]
        path = os.path.join(outdir, f"overlay_{key}.png")
        write_png(path, wmax, len(rows), rows)
        print("wrote", path)
        bgdir = os.path.join(ROOT, "graphics/battle_environment/strata", key)
        panels = []
        for env in ("tall_grass", "long_grass"):
            bpal = read_pal(os.path.join(bgdir, f"{env}.pal"))
            img = gt.render_battle_bg(env, bpal, 1, tiles=os.path.join(bgdir, f"{env}_tiles.png"))[:112]
            panels += [r[:240] for r in img] + [[(255, 255, 255)] * 240] * 2
            # the entry wall over it, where the battle intro shows it
            w, h, anim = read_png(os.path.join(bgdir, f"{env}_anim_tiles.png"))
            rows_n = 6 if env == "tall_grass" else 10
            for y in range(rows_n * 8):
                for x in range(240):
                    v = anim[y][x % 128]
                    if v:
                        img[112 - rows_n * 8 + y][x] = bpal[32 + v]
            panels += [r[:240] for r in img] + [[(255, 255, 255)] * 240] * 2
        plain = read_pal(os.path.join(bgdir, "plain.pal"))
        img = gt.render_battle_bg("building", plain, 1)[:112]
        panels += [r[:240] for r in img]
        big = [[c for c in r for _ in range(2)] for r in panels for _ in range(2)]
        path = os.path.join(outdir, f"battle_{key}.png")
        write_png(path, len(big[0]), len(big), big)
        print("wrote", path)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--preview":
        preview(sys.argv[2])
    else:
        sys.exit(__doc__)
