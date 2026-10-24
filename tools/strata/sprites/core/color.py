"""Colour: ramps, the 16-colour sprite palette, pigment variants, icon fit."""

import colorsys
import os
import sys

from .geom import clamp
from .paths import ROOT, read_pal

TRANSPARENT = (152, 208, 160)  # index 0 of every sprite palette
MAX_COLOURS = 15               # plus the transparent index 0


def ramp(*hexes):
    """ramp("2a1c16", "5a3a28", ...) -> list of RGB tuples, darkest first."""
    return [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in hexes]


def shift_hue(rgb, deg, sat=1.0, val=1.0):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    r, g, b = colorsys.hsv_to_rgb((h + deg / 360) % 1, clamp(s * sat, 0, 1), clamp(v * val, 0, 1))
    return tuple(round(c * 255) for c in (r, g, b))


class Palette:
    """Index 0 transparent, then every ramp in order (darkest first)."""
    def __init__(self, ramps):
        self.colors = [TRANSPARENT]
        self.index = {}
        self.ramp_of = {}
        for name, cols in ramps.items():
            self.index[name] = []
            for lvl, c in enumerate(cols):
                self.ramp_of[len(self.colors)] = (name, lvl)
                self.index[name].append(len(self.colors))
                self.colors.append(tuple(c))
        if len(self.colors) > MAX_COLOURS + 1:
            sys.exit(f"gen_sprite: {len(self.colors) - 1} colours (max {MAX_COLOURS} plus transparent)")
        self.colors += [(0, 0, 0)] * (16 - len(self.colors))

    def get(self, color):
        """'name' (level 0 of a 1-colour ramp, else darkest), ('name', level), or an index."""
        if isinstance(color, int):
            return color
        if isinstance(color, tuple):
            name, lvl = color
            ramp_ = self.index[name]
            return ramp_[clamp(lvl if lvl >= 0 else len(ramp_) + lvl, 0, len(ramp_) - 1)]
        return self.index[color][0]

    def step(self, idx, delta):
        if idx not in self.ramp_of:
            return idx
        name, lvl = self.ramp_of[idx]
        ramp_ = self.index[name]
        return ramp_[clamp(lvl + delta, 0, len(ramp_) - 1)]


def pigment_variant(palette, shiny):
    """The 'shiny' palette: per-ramp hue/saturation/value shifts
    {ramp: dict(deg=, sat=, val=)}. Indices stay the same."""
    colors = list(palette.colors)
    for name, k in shiny.items():
        for idx in palette.index[name]:
            colors[idx] = shift_hue(colors[idx], k["deg"], k.get("sat", 1.0), k.get("val", 1.0))
    return colors


def lab(rgb):
    """sRGB -> CIE L*a*b* (D65)."""
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.9505
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.089

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return (116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z)))


def icon_palette_fit(img_frames, palette):
    """Maps sprite colours to the best of the 6 shared icon palettes (CIELAB
    distance; the outline always goes to the icon's dark grey, and collapsing
    two shades of one ramp into one icon colour costs extra).
    Returns (palette index, remap list, icon palette)."""
    counts = {}
    for f in img_frames:
        for row in f:
            for v in row:
                if v:
                    counts[v] = counts.get(v, 0) + 1

    def dist(a, b):
        la, lb = lab(a), lab(b)
        return (la[0] - lb[0]) ** 2 + 1.5 * ((la[1] - lb[1]) ** 2 + (la[2] - lb[2]) ** 2)

    outline = palette.get("outline")
    best = None
    for p in range(6):
        icon = read_pal(os.path.join(ROOT, f"graphics/pokemon/icon_palettes/pal{p}.pal"))
        remap, err = [0] * 16, 0
        for v, n in counts.items():
            j = 15 if v == outline else min(range(1, 16), key=lambda k: dist(palette.colors[v], icon[k]))
            remap[v] = j
            err += n * dist(palette.colors[v], icon[j])
        for name, idxs in palette.index.items():
            used = [i for i in idxs if i in counts]
            err += 400 * (len(used) - len({remap[i] for i in used})) * sum(counts[i] for i in used) / max(1, len(used))
        if best is None or err < best[0]:
            best = (err, p, remap, icon)
    return best[1], best[2], best[3]
