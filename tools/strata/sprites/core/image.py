"""Index-image helpers and the exact output writers (4bpp/1bpp PNG, JASC pal)."""

import struct
import sys
import zlib


def bbox(img):
    pts = [(x, y) for y, row in enumerate(img) for x, v in enumerate(row) if v]
    if not pts:
        return (0, 0, 0, 0)
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def crop(img, x0, y0, w, h):
    return [[img[y][x] if 0 <= y < len(img) and 0 <= x < len(img[0]) else 0
             for x in range(x0, x0 + w)] for y in range(y0, y0 + h)]


def place(frames, out, bottom=None, what="art"):
    """Crops same-size frames to out x out with the union bbox centred
    horizontally and either centred vertically or with its bottom row at `bottom`."""
    boxes = [bbox(f) for f in frames]
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    if x1 - x0 + 1 > out or y1 - y0 + 1 > out:
        sys.exit(f"gen_sprite: {what} is {x1 - x0 + 1}x{y1 - y0 + 1}, larger than {out}x{out}")
    left = x0 - (out - (x1 - x0 + 1)) // 2
    top = y0 - (out - (y1 - y0 + 1)) // 2 if bottom is None else y1 - bottom
    return [crop(f, left, top, out, out) for f in frames]


def hcat(*imgs):
    """Joins same-height index images left to right."""
    return [sum((img[y] for img in imgs), []) for y in range(len(imgs[0]))]


def write_indexed_png(path, rows, palette, depth=4):
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

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, depth, 3, 0, 0, 0)))
        f.write(chunk(b"PLTE", b"".join(bytes(c) for c in palette)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def write_pal(path, colors):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(colors))
        f.write("".join("%d %d %d\n" % tuple(c) for c in colors))


def coords_size(w, h):
    return f"MON_COORDS_SIZE({min(64, (w + 7) // 8 * 8)}, {min(64, (h + 7) // 8 * 8)})"
