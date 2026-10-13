#!/usr/bin/env python3
"""Generate palette variants of stock tilesets for Strata's eras.

Usage (from the repo root):  python3 tools/strata/gen_tilesets.py

A variant reuses its base tileset's tiles and metatiles and only swaps the
palettes, so one map layout can show the same place in a different era (e.g.
Hell Creek a year after the impact). Writes data/tilesets/<kind>/<variant>/
palettes/*.pal; the Tileset structs are in src/data/tilesets/headers.h.
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# variant dir -> (kind, base dir, transform)
VARIANTS = {
    "general_winter": ("primary", "general", "impact_winter"),
    "fortree_winter": ("secondary", "fortree", "impact_winter"),
}


def impact_winter(r, g, b):
    """Soot-darkened, ash-covered world: mostly desaturated, dimmed, with a
    faint warm ash tint. Greens lose almost all of their colour."""
    lum = 0.30 * r + 0.59 * g + 0.11 * b
    keep = 0.25 if g > r and g > b else 0.35  # vegetation fades the most
    r, g, b = (lum + (c - lum) * keep for c in (r, g, b))
    r, g, b = r * 0.72 + 10, g * 0.70 + 6, b * 0.70 + 4
    return tuple(max(0, min(255, round(c))) for c in (r, g, b))


TRANSFORMS = {"impact_winter": impact_winter}


def read_pal(path):
    lines = open(path).read().split()
    count = int(lines[2])
    return [tuple(int(v) for v in lines[3 + i * 3:6 + i * 3]) for i in range(count)]


def write_pal(path, colors):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(colors))
        f.write("".join("%d %d %d\n" % c for c in colors))


def variant_base(name):
    """(kind, base dir) for a variant tileset dir name, or None."""
    if name in VARIANTS:
        kind, base, _ = VARIANTS[name]
        return kind, base
    return None


def main():
    for variant, (kind, base, transform) in VARIANTS.items():
        src = os.path.join(ROOT, "data/tilesets", kind, base, "palettes")
        dst = os.path.join(ROOT, "data/tilesets", kind, variant, "palettes")
        os.makedirs(dst, exist_ok=True)
        for fname in sorted(os.listdir(src)):
            if fname.endswith(".pal"):
                colors = read_pal(os.path.join(src, fname))
                # Color 0 is transparent; keep it so nothing else changes.
                out = colors[:1] + [TRANSFORMS[transform](*c) for c in colors[1:]]
                write_pal(os.path.join(dst, fname), out)
        print("wrote", variant)


if __name__ == "__main__":
    main()
