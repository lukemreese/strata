"""Every place the game draws a capsule: one writer per asset family.

Each writer keeps the stock file's size, frame layout and, where the palette
is shared with other graphics, the stock palette (drawing with a role ->
index map instead). Free palettes are built from the tier (tiers.py).
`TARGETS` lists (name, function, files written); run them all with build().
"""

import os

from ..core.color import Palette
from ..core.image import write_indexed_png, write_pal
from ..core.paths import ROOT
from . import capsule as C
from .grid import Grid, place, to_index, stack, side, blank, read_indexed
from .tiers import TIERS, ICON_PALETTE_SHARED, ramps, role_index

BALLS = list(TIERS)          # every capsule item (stock ball keys)


def path(rel):
    return os.path.join(ROOT, rel)


def tier_palette(name):
    pal = Palette(ramps(name))
    return pal, role_index(pal)


def fixed(mapping, **extra):
    """Role -> index map for a stock palette; missing shades fall back to a
    neighbour so every role resolves."""
    m = dict(mapping)
    m.update(extra)
    fallbacks = {"b0": "b1", "b1": "b2", "b3": "b2", "b2": "b1", "l0": "l1", "l2": "l1", "l1": "l0",
                 "m0": "m1", "m1": "m0", "s0": "s1", "s1": "s0", "in": "o", "glow": "m1"}
    for _ in range(3):
        for role, alt in fallbacks.items():
            if role not in m and alt in m:
                m[role] = m[alt]
    return m


def keep_palette(rel):
    """The stock PNG's own PLTE (16 entries), for files whose palette is shared."""
    _, pal = read_indexed(path(rel))
    return (pal + [(0, 0, 0)] * 16)[:16]


def save(rel, rows, colors, written):
    write_indexed_png(path(rel), rows, colors)
    written.append(rel)


# --- battle: thrown / summary / release capsule --------------------------------

def balls(written):
    """graphics/balls/<key>.png: 16x48, frames closed / open / wide open
    (pokeball.c uses tiles 0, 4, 8). Open = lid raised over the glowing interior."""
    for key in BALLS:
        pal, m = tier_palette(key)
        mk = TIERS[key]["marking"]
        closed = place(C.capsule(marking=mk, **C.SIZE_16), 16, 16, bottom=14)
        opened = place(C.capsule(marking=mk, lift=2, **dict(C.SIZE_16, handle=1)), 16, 16, bottom=15)
        wide = place(C.capsule(marking=mk, lift=3, **dict(C.SIZE_16, handle=0)), 16, 16, bottom=15)
        save(f"graphics/balls/{key}.png", stack(to_index(closed, m), to_index(opened, m), to_index(wide, m)),
             pal.colors, written)
    # balls/open.png: LoadBallGfx() copies it over frame 2 of the Poke..Master,
    # Net..Nest, Repeat and Safari sheets, so it is drawn with indices that mean
    # the same role in every tier palette (no marking: it is shared).
    maps = {tuple(sorted(tier_palette(k)[1].items())) for k in BALLS}
    if len(maps) != 1:
        raise SystemExit("gen_item_art: tier palettes must share one role -> index layout (balls/open.png)")
    pal, m = tier_palette("poke")
    wide = place(C.capsule(marking="plain", lift=3, **dict(C.SIZE_16, handle=0)), 16, 16, bottom=15)
    save("graphics/balls/open.png", to_index(wide, m), pal.colors, written)


def item_icons(written):
    """graphics/items/icons/<key>_ball.png (24x24) and icon_palettes/<key>_ball.pal."""
    for key in BALLS:
        pal_key = ICON_PALETTE_SHARED.get(key, key)
        pal, m = tier_palette(pal_key)
        if pal_key != key and ramps(key) != ramps(pal_key):
            raise SystemExit(f"gen_item_art: {key} shares {pal_key}'s icon palette, so their colours must match")
        g = place(C.capsule(marking=TIERS[key]["marking"], **C.SIZE_24), 24, 24, bottom=22)
        save(f"graphics/items/icons/{key}_ball.png", to_index(g, m), pal.colors, written)
        if pal_key == key:
            rel = f"graphics/items/icon_palettes/{key}_ball.pal"
            write_pal(path(rel), pal.colors)
            written.append(rel)


SIZE_OW = dict(r=4.5, e=1.5, side=6, lid=2, handle=2)
NPC_3 = fixed({"o": 13, "b0": 4, "b1": 3, "b2": 2, "b3": 1, "l0": 7, "l1": 6, "l2": 5, "m0": 5, "m1": 14,
               "s0": 12, "s1": 14, "led": 8, "in": 15, "glow": 14})


def overworld(written):
    """graphics/object_events/pics/misc/ball_<key>.png: 5 frames of 16x32
    (closed, closed, opening, open, open + beam), bottom row 30. ball_poke is
    the field item (OBJ_EVENT_GFX_ITEM_BALL) and is drawn with the shared
    NPC_3 palette; the others are follower-release sheets with own palettes."""
    for key in BALLS:
        rel = f"graphics/object_events/pics/misc/ball_{key}.png"
        if key == "poke":
            colors, m = keep_palette(rel), NPC_3
        else:
            pal, m = tier_palette(key)
            colors = pal.colors
        mk = TIERS[key]["marking"]
        frames = [C.capsule(marking=mk, **SIZE_OW), C.capsule(marking=mk, **SIZE_OW),
                  C.capsule(marking=mk, lift=1, **SIZE_OW), C.capsule(marking=mk, lift=2, **SIZE_OW),
                  C.capsule(marking=mk, lift=2, beam=True, **SIZE_OW)]
        save(rel, side(*[to_index(place(f, 16, 32, bottom=30), m) for f in frames]), colors, written)


# --- battle HUD ---------------------------------------------------------------

# ball_display.png's own palette is also the health-bar palette: keep it.
STATUS_ROW = {
    "normal":   fixed({"o": 5, "l2": 3, "l1": 4, "m1": 2, "led": 10, "b2": 12, "b1": 13}),
    "fainted":  fixed({"o": 5, "l2": 6, "l1": 6, "m1": 6, "led": 6, "b2": 6, "b1": 6}),
    "statused": fixed({"o": 5, "l2": 3, "l1": 4, "m1": 2, "led": 14, "b2": 3, "b1": 4}),
}
# the caught indicator is drawn into the healthbox, i.e. with its palette
CAUGHT_HEALTHBOX = fixed({"o": 1, "l2": 3, "l1": 5, "m1": 2, "led": 9, "b2": 4, "b1": 5})


def tile8(g):
    return place(g, 8, 8, cx=3.5, cy=3.5)


def battle_hud(written):
    rel = "graphics/battle_interface/ball_display.png"
    colors = keep_palette(rel)
    frames = [to_index(tile8(C.tiny("closed")), STATUS_ROW["normal"]),
              to_index(tile8(C.tiny("empty")), STATUS_ROW["normal"]),
              to_index(tile8(C.tiny("closed")), STATUS_ROW["fainted"]),
              to_index(tile8(C.tiny("closed")), STATUS_ROW["statused"])]
    save(rel, side(*frames), colors, written)
    rel = "graphics/battle_interface/ball_caught_indicator.png"
    save(rel, to_index(tile8(C.tiny("closed")), CAUGHT_HEALTHBOX), keep_palette(rel), written)


def baton_pass(written):
    """graphics/battle_anims/sprites/pokeball.png: Baton Pass's capsule (16x16)."""
    pal, m = tier_palette("poke")
    g = place(C.capsule(marking="label", **C.SIZE_16), 16, 16)
    save("graphics/battle_anims/sprites/pokeball.png", to_index(g, m), pal.colors, written)


# --- menus ----------------------------------------------------------------------

def party_menu(written):
    """party_menu/pokeball.png (32x64: closed, open = selected slot) and
    pokeball_small.png (16x96: closed, open, 4 blank), one shared palette."""
    pal, m = tier_palette("poke")
    big = C.capsule(marking="label", **C.SIZE_24)
    big_open = C.capsule(marking="label", lift=3, **C.SIZE_24)
    frames = [place(big, 32, 32, cx=12, bottom=22), place(big_open, 32, 32, cx=12, bottom=22)]
    save("graphics/party_menu/pokeball.png", stack(*[to_index(f, m) for f in frames]), pal.colors, written)
    small = place(C.capsule(marking="label", **C.SIZE_16), 16, 16, bottom=14)
    small_open = place(C.capsule(marking="label", lift=2, **dict(C.SIZE_16, handle=1)), 16, 16, bottom=15)
    save("graphics/party_menu/pokeball_small.png",
         stack(to_index(small, m), to_index(small_open, m), *[blank(16, 16)] * 4), pal.colors, written)


def bag(written):
    """bag/rotating_ball.png (the pocket-switch spinner) and the pocket badge in
    bag/menu.png, which had a Poke Ball drawn in line art."""
    pal, m = tier_palette("poke")
    g = place(C.capsule(marking="label", **C.SIZE_16), 16, 16)
    save("graphics/bag/rotating_ball.png", to_index(g, m), pal.colors, written)
    bag_badge(written)


BADGE = [            # line-art capsule for the bag's pocket badge, colour E on A
    "...EEEE...",
    "...E..E...",
    ".EEEEEEEE.",
    "E........E",
    "EEEEEEEEEE",
    "E...EE...E",
    "E........E",
    "E........E",
    "E........E",
    ".E......E.",
    "..EEEEEE..",
]


def bag_badge(written):
    import struct
    rel = "graphics/bag/menu.png"
    rows, pal = read_indexed(path(rel))
    tm = open(path("graphics/bag/menu.bin"), "rb").read()
    ents = struct.unpack("<%dH" % (len(tm) // 2), tm)
    ntx = len(rows[0]) // 8
    # screen pixels (8..23, 8..23) are tiles (1,1) (2,1) (1,2) (2,2) of the map
    for sy in range(9, 23):
        for sx in range(9, 23):
            e = ents[(sy // 8) * 32 + sx // 8]
            t, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
            yy, xx = sy % 8, sx % 8
            yy, xx = (7 - yy) if vf else yy, (7 - xx) if hf else xx
            ty, tx = (t // ntx) * 8 + yy, (t % ntx) * 8 + xx
            if rows[ty][tx] == 0xE:
                rows[ty][tx] = 0xA                 # erase the stock emblem
            gy, gx = sy - 10, sx - 11
            if 0 <= gy < len(BADGE) and 0 <= gx < len(BADGE[0]) and BADGE[gy][gx] == "E":
                rows[ty][tx] = 0xE
    write_indexed_png(path(rel), rows, (pal + [(0, 0, 0)] * 16)[:16])
    written.append(rel)


# Codex list: the caught mark is blitted into a window using the Codex BG palette
CODEX_CAUGHT = fixed({"o": 15, "l2": 2, "l1": 4, "m1": 1, "led": 12, "b2": 14, "b1": 14})


def codex(written):
    rel = "graphics/pokedex/caught_ball.png"
    g = Grid(8, 16)
    t = C.tiny("closed")
    for y in range(7):
        for x in range(7):
            g.px[5 + y][x] = t.px[y][x]
    save(rel, to_index(g, CODEX_CAUGHT), keep_palette(rel), written)


# --- field ------------------------------------------------------------------------

GLOW_PAL = [(0, 0, 0), (255, 255, 255), (206, 176, 104), (150, 124, 72), (57, 57, 57), (84, 94, 102),
            (140, 150, 158), (124, 224, 96), (210, 216, 218), (82, 82, 106), (123, 123, 123),
            (255, 255, 255), (189, 230, 255), (164, 197, 230), (156, 189, 213), (90, 131, 180)]
# field_effect.c flashes indices 2, 3, 5, 6 and 8; the outline (4) and light (7) stay
GLOW = fixed({"o": 4, "l2": 8, "l1": 6, "l0": 5, "m1": 1, "led": 7, "b2": 2, "b1": 3})


def heal_machine(written):
    rel = "graphics/field_effects/pics/pokeball_glow.png"
    save(rel, to_index(tile8(C.tiny("closed")), GLOW), GLOW_PAL, written)
    rel = "graphics/field_effects/palettes/pokeball_glow.pal"
    write_pal(path(rel), GLOW_PAL)
    written.append(rel)


# battle_transitions: field_effects/palettes/pokeball.pal is BG palette 15 of
# several transitions. The reachable others (shrinking box, rectangular spiral,
# trail) only use index 15 (black), so indices 1-14 are the Specimen capsule's
# colours. (The Aqua/Magma logo transitions also draw with it; unreachable.)
TRANSITION = {"o": 1, "b0": 2, "b1": 3, "b2": 4, "b3": 5, "l0": 6, "l1": 7, "l2": 8,
              "m0": 9, "m1": 10, "s0": 11, "s1": 12, "led": 13, "glow": 14, "in": 15}
TRANSITION_PAL = "graphics/field_effects/palettes/pokeball.pal"


def transition_palette():
    rm = ramps("poke")
    cols = [(98, 172, 238)] + rm["o"] + rm["b"] + rm["l"] + rm["m"] + rm["s"] + rm["led"] + rm["glow"] + [(0, 0, 0)]
    assert len(cols) == 16
    return cols


def transition_capsule(written):
    """battle_transitions/pokeball.png: the capsule that rolls across the screen
    before trainer battles (B_TRANSITION_POKEBALLS_TRAIL), 32x32, and the shared
    transition palette."""
    cols = transition_palette()
    write_pal(path(TRANSITION_PAL), cols)
    written.append(TRANSITION_PAL)
    rel = "graphics/battle_transitions/pokeball.png"
    g = place(C.capsule(marking="label", **C.SIZE_32), 32, 32)
    save(rel, to_index(g, TRANSITION), cols, written)


def starter_selection(written):
    """starter_choose/pokeball_selection.png: frames still, lean left, lean right
    (the wobble when a capsule is highlighted), then the pointing hand, kept."""
    rel = "graphics/starter_choose/pokeball_selection.png"
    rows, old = read_indexed(path(rel))
    pal, m = tier_palette("poke")
    base = C.capsule(marking="label", **C.SIZE_32)
    frames = [place(base, 32, 32, cx=16, bottom=27),
              place(base.shear(-2), 32, 32, cx=15, bottom=27),
              place(base.shear(2), 32, 32, cx=17, bottom=27)]

    def nearest(c):
        return min(range(1, 16), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal.colors[i], c)))
    hand = [[nearest(old[v]) if v else 0 for v in row] for row in rows[96:128]]
    save(rel, stack(*[to_index(f, m) for f in frames], hand), pal.colors, written)


def scenes(written):
    from . import scenes as S
    S.starter_case(written)
    S.big_emblem(written)


TARGETS = [
    ("balls", balls), ("item_icons", item_icons), ("overworld", overworld), ("battle_hud", battle_hud),
    ("baton_pass", baton_pass), ("party_menu", party_menu), ("bag", bag), ("codex", codex),
    ("heal_machine", heal_machine), ("transition_capsule", transition_capsule),
    ("starter_selection", starter_selection), ("scenes", scenes),
]


def build(only=None):
    written = []
    for name, fn in TARGETS:
        if only and name not in only:
            continue
        fn(written)
    return written
