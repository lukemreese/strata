#!/usr/bin/env python3
"""Render maps and tileset catalogs to PNG, without external dependencies.

Usage (from the repo root):
  python3 tools/strata/maprender.py map <LAYOUT_ID> out.png
  python3 tools/strata/maprender.py catalog <primary> <secondary> out.png [scale]
      e.g. catalog general fallarbor /tmp/fallarbor.png
      Draws every metatile with its hex ID and, if notable, its behavior.

Formats (see include/fieldmap.h, include/global.fieldmap.h):
  map.bin           u16 per block: metatile 0-9, collision 10-11, elevation 12-15
  metatiles.bin     8 u16 tile refs per metatile: 4 bottom layer, 4 top layer
                    tile ref: tile 0-9, hflip 10, vflip 11, palette 12-15
  metatile_attributes.bin  u16 per metatile: behavior 0-7, layer type 12-15
  Primary tileset: metatiles/tiles 0-511, palettes 0-5. Secondary: from 512, palettes 6-12.
"""

import json
import os
import re
import struct
import sys
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6
NUM_PALS_TOTAL = 13


# --- PNG ------------------------------------------------------------------

def read_png(path):
    """Reads a non-interlaced indexed or greyscale PNG with bit depth <= 8.
    Returns (width, height, rows of palette indices)."""
    with open(path, "rb") as f:
        data = f.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    pos, idat = 8, b""
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            width, height, depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
            assert color_type in (0, 3) and interlace == 0 and depth <= 8, (path, color_type, depth)
        elif ctype == b"IDAT":
            idat += chunk
        pos += 12 + length
    raw = zlib.decompress(idat)
    stride = (width * depth + 7) // 8
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(height):
        ftype, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - 1] if x else 0
            b, c = prev[x], prev[x - 1] if x else 0
            if ftype == 1:
                line[x] = (line[x] + a) & 0xFF
            elif ftype == 2:
                line[x] = (line[x] + b) & 0xFF
            elif ftype == 3:
                line[x] = (line[x] + (a + b) // 2) & 0xFF
            elif ftype == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 0xFF
        prev = line
        per_byte, mask = 8 // depth, (1 << depth) - 1
        rows.append([(line[x // per_byte] >> (8 - depth * (x % per_byte + 1))) & mask for x in range(width)])
    return width, height, rows


def write_png(path, width, height, pixels):
    """pixels: list of rows of (r, g, b)."""
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 6)))
        f.write(chunk(b"IEND", b""))


def read_pal(path):
    lines = open(path).read().split()
    count = int(lines[2])
    return [tuple(int(v) for v in lines[3 + i * 3:6 + i * 3]) for i in range(count)]


# --- Tilesets --------------------------------------------------------------

def tileset_dir(name):
    for kind in ("primary", "secondary"):
        d = os.path.join(ROOT, "data/tilesets", kind, name)
        if os.path.isdir(d):
            return d
    sys.exit(f"tileset {name} not found")


def tileset_dir_from_symbol(symbol):
    # gTileset_FallarborFrlg -> fallarbor_frlg, gTileset_GeneralIceAge -> general_ice_age
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", symbol.replace("gTileset_", "")).lower()
    return tileset_dir(name)


class Tileset:
    def __init__(self, path):
        palettes_path = path
        # Palette-only variants (tools/strata/gen_tilesets.py) borrow their base's
        # tiles and metatiles.
        from gen_tilesets import variant_base
        base = variant_base(os.path.basename(path))
        if base is not None:
            path = os.path.join(ROOT, "data/tilesets", *base)
        _, _, rows = read_png(os.path.join(path, "tiles.png"))
        width = len(rows[0])
        self.tiles = []
        for ty in range(len(rows) // 8):
            for tx in range(width // 8):
                self.tiles.append([rows[ty * 8 + y][tx * 8:tx * 8 + 8] for y in range(8)])
        self.palettes = [read_pal(os.path.join(palettes_path, "palettes", f"{i:02}.pal")) for i in range(16)]
        mt = open(os.path.join(path, "metatiles.bin"), "rb").read()
        self.metatiles = [struct.unpack("<8H", mt[i:i + 16]) for i in range(0, len(mt), 16)]
        at = open(os.path.join(path, "metatile_attributes.bin"), "rb").read()
        self.attributes = list(struct.unpack(f"<{len(at) // 2}H", at))


class TilesetPair:
    def __init__(self, primary, secondary):
        self.primary, self.secondary = Tileset(primary), Tileset(secondary)
        self.palettes = self.primary.palettes[:NUM_PALS_IN_PRIMARY] + self.secondary.palettes[NUM_PALS_IN_PRIMARY:NUM_PALS_TOTAL]
        self.cache = {}

    def metatile(self, mid):
        if mid < NUM_METATILES_IN_PRIMARY:
            return self.primary.metatiles[mid] if mid < len(self.primary.metatiles) else None
        mid -= NUM_METATILES_IN_PRIMARY
        return self.secondary.metatiles[mid] if mid < len(self.secondary.metatiles) else None

    def behavior(self, mid):
        ts, i = (self.primary, mid) if mid < NUM_METATILES_IN_PRIMARY else (self.secondary, mid - NUM_METATILES_IN_PRIMARY)
        return ts.attributes[i] & 0xFF if i < len(ts.attributes) else 0

    def tile(self, tid):
        if tid < NUM_TILES_IN_PRIMARY:
            return self.primary.tiles[tid] if tid < len(self.primary.tiles) else None
        tid -= NUM_TILES_IN_PRIMARY
        return self.secondary.tiles[tid] if tid < len(self.secondary.tiles) else None

    def render(self, mid):
        """16x16 RGB pixels of a metatile."""
        if mid in self.cache:
            return self.cache[mid]
        refs = self.metatile(mid)
        out = [[(255, 0, 255)] * 16 for _ in range(16)]
        if refs is not None:
            for layer in range(2):
                for q in range(4):
                    ref = refs[layer * 4 + q]
                    tile = self.tile(ref & 0x3FF)
                    if tile is None:
                        continue
                    hflip, vflip, pal = ref & 0x400, ref & 0x800, (ref >> 12) & 0xF
                    colors = self.palettes[pal] if pal < len(self.palettes) else [(255, 0, 255)] * 16
                    ox, oy = (q % 2) * 8, (q // 2) * 8
                    for y in range(8):
                        for x in range(8):
                            c = tile[7 - y if vflip else y][7 - x if hflip else x]
                            if layer == 0 or c != 0:
                                out[oy + y][ox + x] = colors[c]
        self.cache[mid] = out
        return out


# --- Behavior names ---------------------------------------------------------

def behavior_names():
    names, n = {}, 0
    text = open(os.path.join(ROOT, "include/constants/metatile_behaviors.h")).read()
    body = text[text.index("{") + 1:text.index("}")]
    for line in body.split("\n"):
        m = re.match(r"\s*(MB_\w+)\s*(?:=\s*(\w+))?,", line)
        if m:
            if m.group(2):
                n = int(m.group(2), 0)
            names[n] = m.group(1)[3:]
            n += 1
    return names


# --- Tiny 3x5 font for labels ---------------------------------------------

FONT = {
    "0": "111101101101111", "1": "010110010010111", "2": "111001111100111", "3": "111001111001111",
    "4": "101101111001001", "5": "111100111001111", "6": "111100111101111", "7": "111001001001001",
    "8": "111101111101111", "9": "111101111001111", "A": "111101111101101", "B": "110101110101110",
    "C": "111100100100111", "D": "110101101101110", "E": "111100111100111", "F": "111100111100100",
    "G": "111100101101111", "H": "101101111101101", "I": "111010010010111", "J": "001001001101111",
    "K": "101101110101101", "L": "100100100100111", "M": "101111111101101", "N": "111101101101101",
    "O": "111101101101111", "P": "111101111100100", "Q": "111101101111001", "R": "111101110101101",
    "S": "111100111001111", "T": "111010010010010", "U": "101101101101111", "V": "101101101101010",
    "W": "101101111111101", "X": "101101010101101", "Y": "101101111010010", "Z": "111001010100111",
    "_": "000000000000111", " ": "000000000000000",
}


def draw_text(img, x, y, text, color=(255, 255, 255), bg=(0, 0, 0)):
    for i, ch in enumerate(text.upper()):
        glyph = FONT.get(ch, FONT[" "])
        for gy in range(5):
            for gx in range(3):
                px, py = x + i * 4 + gx, y + gy
                if 0 <= py < len(img) and 0 <= px < len(img[0]):
                    img[py][px] = color if glyph[gy * 3 + gx] == "1" else bg
        for gy in range(5):  # spacing column
            px = x + i * 4 + 3
            if 0 <= y + gy < len(img) and 0 <= px < len(img[0]):
                img[y + gy][px] = bg


# --- Commands ---------------------------------------------------------------

def load_layout(layout_id):
    layouts = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    layout = next((l for l in layouts if l.get("id") == layout_id), None)
    if layout is None:
        sys.exit(f"layout {layout_id} not found")
    return layout


def render_map(layout_id, out, show_collision=False):
    layout = load_layout(layout_id)
    tiles = TilesetPair(tileset_dir_from_symbol(layout["primary_tileset"]),
                        tileset_dir_from_symbol(layout["secondary_tileset"]))
    w, h = layout["width"], layout["height"]
    blocks = struct.unpack(f"<{w * h}H", open(os.path.join(ROOT, layout["blockdata_filepath"]), "rb").read())
    img = [[(0, 0, 0)] * (w * 16) for _ in range(h * 16)]
    for by in range(h):
        for bx in range(w):
            block = blocks[by * w + bx]
            px = tiles.render(block & 0x3FF)
            for y in range(16):
                img[by * 16 + y][bx * 16:bx * 16 + 16] = px[y]
            if show_collision and (block >> 10) & 3:
                for i in range(16):  # red X on impassable blocks
                    img[by * 16 + i][bx * 16 + i] = (255, 0, 0)
                    img[by * 16 + i][bx * 16 + 15 - i] = (255, 0, 0)
    for bx in range(0, w, 5):  # coordinate ruler every 5 blocks
        draw_text(img, bx * 16 + 1, 1, str(bx))
    for by in range(0, h, 5):
        draw_text(img, 1, by * 16 + 9, str(by))
    write_png(out, w * 16, h * 16, img)


def render_catalog(primary, secondary, out, scale=1):
    tiles = TilesetPair(tileset_dir(primary), tileset_dir(secondary))
    names = behavior_names()
    count_p = len(tiles.primary.metatiles)
    ids = list(range(count_p)) + [NUM_METATILES_IN_PRIMARY + i for i in range(len(tiles.secondary.metatiles))]
    cols, cell = 16, 16 * scale + 8
    rows = (len(ids) + cols - 1) // cols
    img = [[(40, 40, 40)] * (cols * cell) for _ in range(rows * cell)]
    for n, mid in enumerate(ids):
        cx, cy = (n % cols) * cell, (n // cols) * cell
        px = tiles.render(mid)
        for y in range(16 * scale):
            for x in range(16 * scale):
                img[cy + y][cx + x] = px[y // scale][x // scale]
        draw_text(img, cx, cy + 16 * scale + 1, f"{mid:X}", color=(255, 255, 0), bg=(40, 40, 40))
    write_png(out, cols * cell, rows * cell, img)
    # Behaviors aren't drawn (labels would overlap); list the notable ones instead.
    for mid in ids:
        b = tiles.behavior(mid)
        if b:
            print(f"{mid:03X} {names.get(b, b)}")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "map":
        render_map(sys.argv[2], sys.argv[3], show_collision="--collision" in sys.argv)
    elif len(sys.argv) >= 5 and sys.argv[1] == "catalog":
        render_catalog(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 1)
    else:
        sys.exit(__doc__)
