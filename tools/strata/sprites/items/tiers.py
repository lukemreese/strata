"""Capsule tiers: colours and marking per capsule item.

Every capsule shares the drawing (capsule.py); a tier is a body colour, a lid,
a marking and a status-light colour. A few tiers are designed (Specimen,
Great, Ultra, Master, Premier, Heal, Safari); the rest are recolours with a
band or label so the bag list stays readable. Keys are the stock ball names
used in file names (graphics/balls/<key>.png, items/icons/<key>_ball.png).
Field-equipment colours: khaki canvas, slate, graphite, ceramic white, olive.
"""

from ..core.color import ramp, shift_hue

LID_GUNMETAL = ("3c4248", "5c666c", "86929a")
LID_DARK = ("24262a", "383c42", "545a62")
METAL = ("a6aeb0", "e6eae6")
INTERIOR = ("1c2026", "e8f6d8")      # in, glow
LED_GREEN = "7ce060"


def body(*hexes):
    return hexes


def tier(body_, lid=LID_GUNMETAL, stripe=("5c5034", "e8e0c4"), led=LED_GREEN, marking="label", outline=None):
    return dict(body=body_, lid=lid, stripe=stripe, led=led, marking=marking, outline=outline)


def hue_body(base_hex, light=1.0):
    """Four body shades from one mid colour: shadows cooler, lights warmer."""
    c = ramp(base_hex)[0]
    shades = [shift_hue(c, 8, 1.05, 0.55), shift_hue(c, 4, 1.0, 0.78), c, shift_hue(c, -6, 0.75, 1.18 * light)]
    return tuple("%02x%02x%02x" % s for s in shades)


TIERS = {
    # designed tiers
    "poke":    tier(("5e5232", "8c7c4c", "b8a46a", "dccb94")),                      # Specimen: khaki canvas, sample label
    "great":   tier(("2a4664", "3e6488", "5a88b0", "8cb2d4"), stripe=("a85418", "f0943c"), marking="band"),
    "ultra":   tier(("26282c", "3c4046", "585e66", "7a8088"), lid=LID_DARK, stripe=("1c1e22", "f0c030"),
                    led="f0a020", marking="hazard"),
    "master":  tier(("948e82", "bcb6a8", "dcd6c8", "f6f4ec"), lid=("3a2656", "5c3a86", "8862b6"),
                    stripe=("a0801e", "e6c450"), led="c890ff", marking="double"),
    "premier": tier(("8e8e8a", "b8b8b2", "dadad4", "f6f6f0"), stripe=("a02c26", "d8504a"), led="f06050",
                    marking="band"),
    "heal":    tier(("98506a", "c4788e", "e2a2b4", "f6cad4"), lid=("6c6870", "98949c", "c8c4ca"),
                    stripe=("d04860", "fafaf6"), marking="cross"),
    "safari":  tier(("3a4824", "546834", "72864a", "98aa6c"), lid=("5e5034", "86744e", "ae9a6e"),
                    stripe=("3a4824", "d8cc9c")),
    # recolours
    "net":     tier(hue_body("3c8c8a"), stripe=("1e3a3a", "a8dcd0"), marking="hazard"),
    "nest":    tier(hue_body("5c8a34"), stripe=("5a3a1e", "a8784a"), marking="band"),
    "dive":    tier(hue_body("2c5ca0"), stripe=("1a3a6a", "8ad0f0"), marking="band"),
    "dusk":    tier(hue_body("2e4430"), lid=LID_DARK, stripe=("1a241a", "6cd070"), marking="band"),
    "timer":   tier(hue_body("c86030"), stripe=("c03828", "f6eee0"), marking="double"),   # shares repeat's icon palette
    "quick":   tier(hue_body("3460b0"), stripe=("b08a10", "f6d040"), marking="band"),
    "repeat":  tier(hue_body("c86030"), stripe=("c03828", "f6eee0"), marking="band"),
    "luxury":  tier(hue_body("34302c"), lid=LID_DARK, stripe=("a0801e", "e6c450"), led="f06050", marking="double"),
    "level":   tier(hue_body("b0402c")),
    "lure":    tier(hue_body("2c7a9c")),
    "moon":    tier(hue_body("3a3e6c"), stripe=("8a7a20", "f2e27a")),
    "friend":  tier(hue_body("4c8c40")),
    "love":    tier(hue_body("c8607c")),
    "fast":    tier(hue_body("c8a030")),
    "heavy":   tier(hue_body("5a6878")),
    "dream":   tier(hue_body("b07ab8"), stripe=("6c3a7a", "f4d8f2"), marking="band"),
    "sport":   tier(hue_body("c07a34"), stripe=("5a3a1e", "e8c890"), marking="band"),
    "park":    tier(hue_body("c8b040"), stripe=("2c4a8a", "6c94d8"), marking="band"),
    "beast":   tier(hue_body("2a3a7a"), stripe=("1a2040", "f0d040"), marking="hazard"),
    "cherish": tier(hue_body("a02c2c"), stripe=("a0801e", "e6c450"), marking="double"),
    "strange": tier(hue_body("6a7480"), stripe=("2a6a7a", "8ae0f0"), marking="band"),
}

# Item file stems (graphics/items/icons/<stem>.png) whose icon palette is
# another tier's (src/data/items.h: Timer uses gItemIconPalette_RepeatBall).
ICON_PALETTE_SHARED = {"timer": "repeat"}


def ramps(name):
    """The 15-colour sprite palette of a tier, in role order (core.color.Palette ramps)."""
    t = TIERS[name]
    b = ramp(*t["body"])
    outline = ramp(t["outline"])[0] if t["outline"] else shift_hue(b[0], 6, 1.1, 0.45)
    return {
        "o": [outline],
        "b": b,
        "l": ramp(*t["lid"]),
        "m": ramp(*METAL),
        "s": ramp(*t["stripe"]),
        "led": ramp(t["led"]),
        "in": ramp(INTERIOR[0]),
        "glow": ramp(INTERIOR[1]),
    }


def role_index(palette):
    """Role name -> index into a core.color.Palette built from ramps()."""
    m = {"o": palette.get("o"), "led": palette.get("led"), "in": palette.get("in"), "glow": palette.get("glow")}
    for key, n in (("b", 4), ("l", 3), ("m", 2), ("s", 2)):
        for i in range(n):
            m[f"{key}{i}"] = palette.get((key, i))
    return m
