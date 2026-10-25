"""Role grids: item art is drawn as a grid of role names ("o" outline, "b2" body
shade 2, "led", ...) and only turned into palette indices per target, so one
drawing serves targets with free palettes and targets that must reuse a shared
palette. Plus the indexed-PNG reader (with its PLTE) the writers need."""

import struct
import zlib

from ..core.paths import read_png


class Grid:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[None] * w for _ in range(h)]

    def get(self, x, y):
        return self.px[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def set(self, x, y, v):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = v

    def bbox(self):
        pts = [(x, y) for y in range(self.h) for x in range(self.w) if self.px[y][x] is not None]
        if not pts:
            return (0, 0, -1, -1)
        return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

    def outline(self, role="o", thicken=False):
        """1-px outer outline (4-neighbourhood) around everything drawn."""
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.px[y][x] is None and any(
                        self.get(x + dx, y + dy) not in ((None,) if thicken else (None, role))
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for x, y in add:
            self.px[y][x] = role
        return self

    def shear(self, k):
        """Leans the drawing: the top row moves k px (sign = direction), the
        bottom row stays. Integer steps keep the pixel clusters clean."""
        x0, y0, x1, y1 = self.bbox()
        out = Grid(self.w, self.h)
        span = max(1, y1 - y0)
        for y in range(self.h):
            dx = round(k * (y1 - y) / span)
            for x in range(self.w):
                if self.px[y][x] is not None:
                    out.set(x + dx, y, self.px[y][x])
        return out

    def flip(self):
        out = Grid(self.w, self.h)
        out.px = [list(reversed(r)) for r in self.px]
        return out


def place(grid, w, h, cx=None, bottom=None, cy=None):
    """A w x h grid with `grid`'s drawing centred at column cx (default: centre)
    and either its bottom row at `bottom` or its centre row at cy (default)."""
    x0, y0, x1, y1 = grid.bbox()
    gw, gh = x1 - x0 + 1, y1 - y0 + 1
    if gw > w or gh > h:
        raise SystemExit(f"gen_item_art: drawing {gw}x{gh} does not fit {w}x{h}")
    cx = w / 2 if cx is None else cx
    left = int(round(cx - gw / 2))
    if bottom is not None:
        top = bottom - gh + 1
    else:
        top = int(round((h if cy is None else 2 * cy) / 2 - gh / 2))
    left, top = max(0, min(w - gw, left)), max(0, min(h - gh, top))
    out = Grid(w, h)
    for y in range(gh):
        for x in range(gw):
            out.px[top + y][left + x] = grid.px[y0 + y][x0 + x]
    return out


def to_index(grid, mapping):
    """Role grid -> rows of palette indices (None -> 0)."""
    rows = []
    for row in grid.px:
        out = []
        for v in row:
            if v is None:
                out.append(0)
            elif v not in mapping:
                raise SystemExit(f"gen_item_art: role {v!r} has no palette index")
            else:
                out.append(mapping[v])
        rows.append(out)
    return rows


def stack(*frames):
    """Index frames (same width) top to bottom."""
    return [r for f in frames for r in f]


def side(*frames):
    """Index frames (same height) left to right."""
    return [sum((f[y] for f in frames), []) for y in range(len(frames[0]))]


def blank(w, h):
    return [[0] * w for _ in range(h)]


def read_indexed(path):
    """(rows, palette) of an indexed PNG; palette is the PLTE as RGB tuples."""
    _, _, rows = read_png(path)
    data = open(path, "rb").read()
    pos, pal = 8, None
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if ctype == b"PLTE":
            chunk = data[pos + 8:pos + 8 + length]
            pal = [tuple(chunk[i:i + 3]) for i in range(0, len(chunk), 3)]
        pos += 12 + length
    return rows, pal


def write_png8(path, rows, palette):
    """8-bit indexed PNG (for 8bpp sources such as starter_choose/tiles.png)."""
    width, height = len(rows[0]), len(rows)
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)))
        f.write(chunk(b"PLTE", b"".join(bytes(c) for c in palette)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        f.write(chunk(b"IEND", b""))
