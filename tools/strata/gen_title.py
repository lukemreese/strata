#!/usr/bin/env python3
"""Generate Strata's title screen art in place of Emerald's.

Usage (from the repo root):  python3 tools/strata/gen_title.py

Redraws graphics/title_screen/ assets in their original sizes and formats, so
src/title_screen.c needs no changes:
  pokemon_logo.png / .pal   "STRATA" logo, letters filled with rock-layer bands
  emerald_version.png       "DEEP TIME" banner (was "EMERALD VERSION")
  press_start.png           keeps PRESS START, blanks the copyright line
  rayquaza.png, clouds.png  blanked
The logo's tilemap (pokemon_logo.bin) maps tile row*32+col, so it is unchanged.
"""

import os
import struct
import sys
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from maprender import read_png  # noqa: E402

TITLE = os.path.join(ROOT, "graphics/title_screen")

FONT_5X7 = {
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    " ": ["00000"] * 7,
}


def read_palette(path):
    data = open(path, "rb").read()
    pos = 8
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if ctype == b"PLTE":
            raw = data[pos + 8:pos + 8 + length]
            return [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
        pos += 12 + length
    sys.exit(f"{path} has no palette")


def write_indexed_png(path, rows, palette, depth):
    width, height = len(rows[0]), len(rows)
    per_byte = 8 // depth
    raw = bytearray()
    for row in rows:
        raw.append(0)
        for x in range(0, width, per_byte):
            byte = 0
            for i in range(per_byte):
                byte |= (row[x + i] & ((1 << depth) - 1)) << (8 - depth * (i + 1))
            raw.append(byte)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    plte = b"".join(bytes(c) for c in palette)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, depth, 3, 0, 0, 0)))
        f.write(chunk(b"PLTE", plte))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def text_mask(text, scale, gap):
    """Returns a 2D list of booleans for `text` drawn in the 5x7 font."""
    width = len(text) * 5 * scale + (len(text) - 1) * gap
    mask = [[False] * width for _ in range(7 * scale)]
    for i, ch in enumerate(text):
        ox = i * (5 * scale + gap)
        for gy, line in enumerate(FONT_5X7[ch]):
            for gx, bit in enumerate(line):
                if bit == "1":
                    for y in range(scale):
                        for x in range(scale):
                            mask[gy * scale + y][ox + gx * scale + x] = True
    return mask


def stamp(canvas, mask, ox, oy, fill, outline, shadow=None):
    """Draws mask at (ox, oy) with a 1px outline and optional 2px drop shadow.
    `fill(x, y)` gives the palette index for a filled pixel (mask coords)."""
    h, w = len(mask), len(mask[0])

    def on(x, y):
        return 0 <= y < h and 0 <= x < w and mask[y][x]

    if shadow is not None:
        for y in range(-1, h + 1):
            for x in range(-1, w + 1):
                if any(on(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                    canvas[oy + y + 2][ox + x + 2] = shadow
    for y in range(-1, h + 1):
        for x in range(-1, w + 1):
            if on(x, y):
                canvas[oy + y][ox + x] = fill(x, y)
            elif any(on(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                canvas[oy + y][ox + x] = outline


# Logo palette (BG palette 0, 8bpp logo). Index 0 is the title screen backdrop.
LOGO_COLORS = [
    (32, 24, 56),     # 0 backdrop: dusk sky
    (40, 24, 16),     # 1 outline
    (200, 150, 64),   # 2 ochre
    (236, 220, 170),  # 3 cream sandstone
    (248, 244, 232),  # 4 pale boundary clay
    (176, 96, 56),    # 5 rust mudstone
    (210, 170, 110),  # 6 tan siltstone
    (150, 140, 130),  # 7 grey shale
    (120, 64, 48),    # 8 dark red-brown
    (16, 12, 28),     # 9 shadow
]

# Rock bands down the letters, (first row, palette index); the thin pale line
# is the K-Pg boundary clay.
BANDS = [(0, 2), (6, 3), (10, 4), (12, 5), (18, 6), (23, 7), (27, 8), (31, 5)]

# title_screen.c scrolls the logo BG 29 px right (BG2X = -29), and the screen is
# 240 px wide, so content is centered at image x = 120 - 29.
LOGO_SCREEN_SHIFT = 29


def band_color(y):
    color = BANDS[0][1]
    for start, idx in BANDS:
        if y >= start:
            color = idx
    return color


def make_logo():
    w, h = 256, 64
    canvas = [[0] * w for _ in range(h)]
    mask = text_mask("STRATA", 5, 5)
    ox = (240 - len(mask[0])) // 2 - LOGO_SCREEN_SHIFT
    # Keep clear of tile (0,0), which the tilemap uses for empty space.
    stamp(canvas, mask, ox, 16, lambda x, y: band_color(y), 1, shadow=9)
    assert all(canvas[y][x] == 0 for y in range(8) for x in range(8))

    pal_path = os.path.join(TITLE, "pokemon_logo.pal")
    lines = open(pal_path).read().split("\n")
    count = int(lines[2])
    colors = [tuple(int(v) for v in lines[3 + i].split()) for i in range(count)]
    colors[:len(LOGO_COLORS)] = LOGO_COLORS
    with open(pal_path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % count)
        f.write("".join("%d %d %d\n" % c for c in colors))
    palette = (colors + [(0, 0, 0)] * 256)[:256]
    write_indexed_png(os.path.join(TITLE, "pokemon_logo.png"), canvas, palette, 8)


def make_banner():
    w, h = 128, 32
    canvas = [[0] * w for _ in range(h)]
    mask = text_mask("DEEP TIME", 2, 2)
    ox = (w - len(mask[0])) // 2
    stamp(canvas, mask, ox, 9, lambda x, y: 3 if y < 6 else 2, 1)
    palette = [(255, 0, 255), (32, 20, 40), (240, 176, 72), (255, 236, 168)]
    palette = (palette + [(0, 0, 0)] * 256)[:256]
    write_indexed_png(os.path.join(TITLE, "emerald_version.png"), canvas, palette, 8)


def blank_copyright():
    path = os.path.join(TITLE, "press_start.png")
    palette = read_palette(path)
    _, _, rows = read_png(path)
    for y in range(8, len(rows)):  # row 0-7 is PRESS START, below is the copyright
        rows[y] = [0] * len(rows[y])
    write_indexed_png(path, rows, palette, 4)


def blank(name):
    path = os.path.join(TITLE, name)
    palette = read_palette(path)
    _, _, rows = read_png(path)
    write_indexed_png(path, [[0] * len(r) for r in rows], palette, 4)


if __name__ == "__main__":
    make_logo()
    make_banner()
    blank_copyright()
    blank("rayquaza.png")
    blank("clouds.png")
    print("title screen art written")
