"""Strata key-item icons that are not capsules (24x24 bag icons with their own palette).

FOSSIL_CASE: a glass-topped wooden specimen case with a fossil bone on a sandstone bed and a
brass latch (ITEM_FOSSIL_CASE, src/strata_fossils.c). Drawn as a letter grid; each letter is
a palette entry below.
"""

from ..core.color import TRANSPARENT
from ..core.image import write_indexed_png, write_pal

FOSSIL_CASE_COLORS = {
    "o": (44, 30, 22),     # outline
    "W": (98, 60, 36),     # wood, dark
    "w": (146, 96, 56),    # wood
    "l": (190, 136, 82),   # wood, lit edge
    "m": (150, 126, 96),   # sandstone bed, shadow
    "n": (196, 174, 134),  # sandstone bed
    "p": (226, 210, 174),  # sandstone bed through the lit glass
    "g": (214, 238, 244),  # glass glint
    "B": (122, 102, 82),   # bone, shadow
    "b": (206, 196, 172),  # bone
    "c": (246, 242, 228),  # bone, lit
    "y": (222, 182, 70),   # brass latch
    "Y": (150, 108, 34),   # brass, shadow
}

FOSSIL_CASE = [
    "........................",
    "........................",
    "........................",
    ".oooooooooooooooooooooo.",
    ".ollllllllllllllllllllo.",
    ".olWWWWWWWWWWWWWWWWWWwo.",
    ".olWgggpppppppppppppnwo.",
    ".olWgpnbbnnnnnnnnbbnnwo.",
    ".olWpbccbbbbbbbbbccbnwo.",
    ".olWnbcccccccccccccbnwo.",
    ".olWnbccBBBBBBBBBccBnwo.",
    ".olWnnBBnnnnnnnnnBBnnwo.",
    ".olWmmmmmmmmmmmmmmmmmwo.",
    ".oWWWWWWWWWWWWWWWWWWWWo.",
    ".oooooooooooooooooooooo.",
    ".owwwwwwwwyyyywwwwwwwwo.",
    ".owwwwwwwwyYYywwwwwwwwo.",
    ".oWwwwwwwwwyywwwwwwwwWo.",
    ".oWWWWWWWWWWWWWWWWWWWWo.",
    ".oooooooooooooooooooooo.",
    "..oo................oo..",
    "........................",
    "........................",
    "........................",
]


def _check_rows(rows, width=24):
    for r in rows:
        if len(r) != width:
            raise SystemExit(f"gen_item_art: fossil case row {r!r} is {len(r)} wide, not {width}")
    return rows


def fossil_case(written, path):
    letters = list(FOSSIL_CASE_COLORS)
    colors = [TRANSPARENT] + [FOSSIL_CASE_COLORS[k] for k in letters]
    colors += [(0, 0, 0)] * (16 - len(colors))
    index = {k: i + 1 for i, k in enumerate(letters)}
    rows = [[0 if ch == "." else index[ch] for ch in r] for r in _check_rows(FOSSIL_CASE)]
    png = "graphics/items/icons/fossil_case.png"
    pal = "graphics/items/icon_palettes/fossil_case.pal"
    write_indexed_png(path(png), rows, colors)
    write_pal(path(pal), colors)
    written += [png, pal]
