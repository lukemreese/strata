#!/usr/bin/env python3
"""Generate original creature sprites ("Tier A reconstruction plates").

Usage (from the repo root):
    python3 tools/strata/gen_sprite.py                 all species in SPECS
    python3 tools/strata/gen_sprite.py knightia        one species
    python3 tools/strata/gen_sprite.py --preview DIR   also write enlarged previews to DIR

Each species is a small parametric body plan (ellipsoids, capsules, lofted
bodies and flat fin polygons, in sprite pixels, head to the left). The script
rasterises it directly at the target size with 4x4 supersampled coverage,
shades every part as a dome lit from the upper left into the species' colour
ramps, adds selective 1 px outlines and painted details (eye, mouth, rays), and
writes, in graphics/pokemon/strata/<name>/:

    anim_front.png  64x128, two frames      back.png    64x64
    normal.pal / shiny.pal  16 colours, index 0 transparent ("shiny" is a
                    pigment variant: a hue shift of chosen ramps)
    icon.png        32x64, two frames, in one of the 6 shared icon palettes
    footprint.png   16x16 1bpp
    CUSTOM          marker read by gen_species.py: it stops gen_species from
                    overwriting these files with the borrowed species' and
                    overrides the presentation fields listed in it.
"""

import colorsys
import math
import os
import struct
import sys
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from maprender import read_pal, write_png  # noqa: E402

TRANSPARENT = (152, 208, 160)
LIGHT = (-0.50, -0.70, 0.75)
_n = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _n for c in LIGHT)
AMBIENT, DIFFUSE = 0.10, 0.80  # a surface facing the viewer lands on the 2nd-lightest of 4 shades
SS = 4  # supersampling per axis for coverage


# --- maths -------------------------------------------------------------------

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


def lerp(a, b, t):
    return a + (b - a) * t


def curve(points, t):
    """Cosine interpolation through (t, value) control points."""
    if t <= points[0][0]:
        return points[0][1]
    for (t0, v0), (t1, v1) in zip(points, points[1:]):
        if t <= t1:
            u = (t - t0) / (t1 - t0)
            return lerp(v0, v1, (1 - math.cos(u * math.pi)) / 2)
    return points[-1][1]


def rot(x, y, deg):
    a = math.radians(deg)
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def shift_hue(rgb, deg, sat=1.0, val=1.0):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    r, g, b = colorsys.hsv_to_rgb((h + deg / 360) % 1, clamp(s * sat, 0, 1), clamp(v * val, 0, 1))
    return tuple(round(c * 255) for c in (r, g, b))


# --- shapes ------------------------------------------------------------------
# q(x, y) > 0 inside, rising to 1 on the shape's ridge; continuous outside so a
# numeric gradient gives the edge normal. bbox = (x0, y0, x1, y1) in model units.

class Ellipse:
    def __init__(self, cx, cy, rx, ry, angle=0.0):
        self.c, self.r, self.a = (cx, cy), (rx, ry), angle
        m = max(rx, ry)
        self.bbox = (cx - m, cy - m, cx + m, cy + m)

    def q(self, x, y):
        u, v = rot(x - self.c[0], y - self.c[1], -self.a)
        return 1 - (u / self.r[0]) ** 2 - (v / self.r[1]) ** 2


class Tube:
    """Capsules through points with per-point radii (limbs, tails, necks)."""
    def __init__(self, points, radii):
        self.p, self.rad = points, radii
        m = max(radii)
        self.bbox = (min(p[0] for p in points) - m, min(p[1] for p in points) - m,
                     max(p[0] for p in points) + m, max(p[1] for p in points) + m)

    def q(self, x, y):
        best = -9.0
        for (a, ra), (b, rb) in zip(zip(self.p, self.rad), zip(self.p[1:], self.rad[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ll = dx * dx + dy * dy
            t = clamp(((x - a[0]) * dx + (y - a[1]) * dy) / ll, 0, 1) if ll else 0
            d = math.hypot(x - a[0] - dx * t, y - a[1] - dy * t)
            r = lerp(ra, rb, t)
            best = max(best, 1 - (d / r) ** 2)
        return best


class Loft:
    """A body lofted along x: between x0 and x1 the outline runs from
    mid(t) - up(t) to mid(t) + dn(t), t = 0..1 (fish bodies, torsos)."""
    def __init__(self, x0, x1, up, dn, mid=None):
        self.x0, self.x1, self.up, self.dn = x0, x1, up, dn
        self.mid = mid or (lambda t: 0.0)
        ts = [i / 40 for i in range(41)]
        self.bbox = (x0, min(self.mid(t) - curve(up, t) for t in ts),
                     x1, max(self.mid(t) + curve(dn, t) for t in ts))

    def t(self, x):
        return (x - self.x0) / (self.x1 - self.x0)

    def top(self, x):
        t = clamp(self.t(x), 0, 1)
        return self.mid(t) - curve(self.up, t)

    def bottom(self, x):
        t = clamp(self.t(x), 0, 1)
        return self.mid(t) + curve(self.dn, t)

    def s(self, x, y):
        """-1 at the top outline, +1 at the bottom."""
        top, bot = self.top(x), self.bottom(x)
        return (y - (top + bot) / 2) / max(0.01, (bot - top) / 2)

    def q(self, x, y):
        t = self.t(x)
        if t < 0 or t > 1:
            return -1 - abs(t - clamp(t, 0, 1)) * 10
        top, bot = self.top(x), self.bottom(x)
        if bot - top < 0.05:
            return -1
        return 1 - self.s(x, y) ** 2


class Union:
    """Smooth union of shapes (k = blend width in q units), shaded as one dome."""
    def __init__(self, shapes, k=0.12):
        self.shapes, self.k = shapes, k
        self.bbox = (min(s.bbox[0] for s in shapes), min(s.bbox[1] for s in shapes),
                     max(s.bbox[2] for s in shapes), max(s.bbox[3] for s in shapes))

    def q(self, x, y):
        qs = [s.q(x, y) for s in self.shapes]
        m = max(qs)
        return m + self.k * math.log(sum(math.exp((v - m) / self.k) for v in qs))


class Poly:
    """A flat polygon (fins, ears). Lit as a plane facing `tilt`."""
    def __init__(self, points):
        self.p = points
        self.bbox = (min(p[0] for p in points), min(p[1] for p in points),
                     max(p[0] for p in points), max(p[1] for p in points))

    def q(self, x, y):
        inside = False
        for (ax, ay), (bx, by) in zip(self.p, self.p[1:] + self.p[:1]):
            if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
                inside = not inside
        return 1.0 if inside else -1.0


class Part:
    """shape + colour ramp. z orders parts (higher is nearer). `flat` is the
    dome exponent (0.5 = round, smaller = flatter); `normal` overrides shading
    for flat parts. `region(x, y)` may return another ramp name for this point
    (countershading). `outline` is the colour used to outline this part against
    the background, `inner` (default: outline) where it overlaps farther parts;
    `line=False` draws no such contour. `light` brightens (+) or darkens (-)."""
    def __init__(self, shape, ramp, z=0, flat=0.5, normal=None, region=None,
                 outline="outline", inner=None, line=True, shadow=True, light=0.0):
        self.shape, self.ramp, self.z, self.flat = shape, ramp, z, flat
        self.normal, self.region, self.outline = normal, region, outline
        self.inner = inner if inner is not None else outline
        self.line, self.shadow, self.light = line, shadow, light


# --- rendering ---------------------------------------------------------------

class Model:
    """What a species function returns: parts, palette ramps, painted details."""
    def __init__(self, parts, ramps, details=None, post=None):
        self.parts, self.ramps, self.details, self.post = parts, ramps, details, post


class Palette:
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
        if len(self.colors) > 16:
            sys.exit(f"gen_sprite: {len(self.colors)} colours (max 16 with transparent)")
        self.colors += [(0, 0, 0)] * (16 - len(self.colors))

    def get(self, color):
        """'name' (level 0 of a 1-colour ramp, else darkest), ('name', level), or an index."""
        if isinstance(color, int):
            return color
        if isinstance(color, tuple):
            name, lvl = color
            ramp = self.index[name]
            return ramp[clamp(lvl if lvl >= 0 else len(ramp) + lvl, 0, len(ramp) - 1)]
        return self.index[color][0]

    def step(self, idx, delta):
        if idx not in self.ramp_of:
            return idx
        name, lvl = self.ramp_of[idx]
        ramp = self.index[name]
        return ramp[clamp(lvl + delta, 0, len(ramp) - 1)]


class Canvas:
    """Index image + per-pixel owning part; model -> screen transform."""
    def __init__(self, size, scale, flip, palette, origin):
        self.w = self.h = size
        self.scale, self.flip, self.pal = scale, flip, palette
        self.ox, self.oy = origin
        self.idx = [[0] * size for _ in range(size)]
        self.owner = [[-1] * size for _ in range(size)]

    def to_model(self, px, py):
        return (px - self.ox) / self.scale * (-1 if self.flip else 1), (py - self.oy) / self.scale

    def pt(self, x, y):
        return (math.floor(self.ox + x * self.scale * (-1 if self.flip else 1)),
                math.floor(self.oy + y * self.scale))

    def inside(self, px, py):
        return 0 <= px < self.w and 0 <= py < self.h

    def set(self, px, py, color, only_opaque=True):
        if self.inside(px, py) and (self.idx[py][px] or not only_opaque):
            self.idx[py][px] = self.pal.get(color)

    def shade(self, px, py, delta):
        if self.inside(px, py) and self.idx[py][px]:
            self.idx[py][px] = self.pal.step(self.idx[py][px], delta)

    def pixels_on_line(self, a, b):
        (x0, y0), (x1, y1) = self.pt(*a), self.pt(*b)
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            yield x0, y0
            if (x0, y0) == (x1, y1):
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def line(self, a, b, color, only_opaque=True):
        for px, py in self.pixels_on_line(a, b):
            self.set(px, py, color, only_opaque)

    def polyline(self, pts, color, only_opaque=True, shade=None):
        for a, b in zip(pts, pts[1:]):
            for px, py in self.pixels_on_line(a, b):
                if shade is not None:
                    self.shade(px, py, shade)
                else:
                    self.set(px, py, color, only_opaque)

    def disc(self, c, r, color, only_opaque=False):
        """Pixels whose centres are within r model units of c."""
        rs = r * self.scale
        cx, cy = self.ox + c[0] * self.scale * (-1 if self.flip else 1), self.oy + c[1] * self.scale
        for py in range(math.floor(cy - rs) - 1, math.ceil(cy + rs) + 2):
            for px in range(math.floor(cx - rs) - 1, math.ceil(cx + rs) + 2):
                if (px + 0.5 - cx) ** 2 + (py + 0.5 - cy) ** 2 <= rs * rs:
                    self.set(px, py, color, only_opaque)


def shade_normal(part, x, y, eps):
    if part.normal is not None:
        return part.normal
    q = part.shape.q(x, y)
    gx = (part.shape.q(x + eps, y) - part.shape.q(x - eps, y)) / (2 * eps)
    gy = (part.shape.q(x, y + eps) - part.shape.q(x, y - eps)) / (2 * eps)
    g = math.hypot(gx, gy)
    z = clamp(q, 0.0, 1.0) ** part.flat
    if g < 1e-6:
        return (0.0, 0.0, 1.0)
    k = math.sqrt(max(0.0, 1 - z * z)) / g
    return (-gx * k, -gy * k, z)


def render(model, size, scale, flip, origin, palette):
    cv = Canvas(size, scale, flip, palette, origin)
    parts = sorted(enumerate(model.parts), key=lambda p: -p[1].z)
    fs = -1 if flip else 1
    level = [[0] * size for _ in range(size)]
    # 1. coverage: each subsample belongs to the nearest part containing it. A pixel
    #    that is at least half covered goes to the nearest part owning half of it,
    #    else to the part owning most of its samples.
    half = SS * SS / 2
    for py in range(size):
        for px in range(size):
            mx0, my0 = cv.to_model(px, py)
            m1x, m1y = cv.to_model(px + 1, py + 1)
            lo_x, hi_x = min(mx0, m1x), max(mx0, m1x)
            near = [(i, p) for i, p in parts
                    if not (hi_x < p.shape.bbox[0] or lo_x > p.shape.bbox[2]
                            or m1y < p.shape.bbox[1] or my0 > p.shape.bbox[3])]
            if not near:
                continue
            hits = {}
            for sy in range(SS):
                for sx in range(SS):
                    x, y = cv.to_model(px + (sx + 0.5) / SS, py + (sy + 0.5) / SS)
                    for i, part in near:
                        if part.shape.q(x, y) > 0:
                            hits[i] = hits.get(i, 0) + 1
                            break
            if sum(hits.values()) < half:
                continue
            owner = next((i for i, _ in near if hits.get(i, 0) >= half), None)
            if owner is None:
                owner = max(hits, key=lambda i: (hits[i], model.parts[i].z))
            cv.owner[py][px] = owner
    # 2. shading
    for py in range(size):
        for px in range(size):
            i = cv.owner[py][px]
            if i < 0:
                continue
            part = model.parts[i]
            x, y = cv.to_model(px + 0.5, py + 0.5)
            nx, ny, nz = shade_normal(part, x, y, 0.35 / scale)
            nx *= fs
            light = AMBIENT + DIFFUSE * max(0.0, nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]) + part.light
            ramp = part.region(x, y) if part.region else part.ramp
            n = len(palette.index[ramp])
            lvl = clamp(int(light * n), 0, n - 1)
            # cast shadow from a nearer part towards the upper left (light side)
            for dx, dy in ((0, -1), (-1, 0), (-1, -1), (0, -2)):
                qx, qy = px + dx, py + dy
                if cv.inside(qx, qy) and cv.owner[qy][qx] >= 0:
                    other = model.parts[cv.owner[qy][qx]]
                    if other.z > part.z and other.shadow:
                        lvl = max(0, lvl - 1)
                        break
            level[py][px] = lvl
            cv.idx[py][px] = palette.index[ramp][lvl]
    # 3. contour lines where a nearer part overlaps a farther one
    lines = []
    for py in range(size):
        for px in range(size):
            i = cv.owner[py][px]
            if i < 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                qx, qy = px + dx, py + dy
                if cv.inside(qx, qy) and cv.owner[qy][qx] >= 0:
                    other = model.parts[cv.owner[qy][qx]]
                    if other.z > model.parts[i].z and other.line:
                        lines.append((px, py, palette.get(other.inner)))
                        break
    for px, py, c in lines:
        cv.idx[py][px] = c
    # 4. painted details
    if model.details:
        model.details(cv)
    # 5. outer outline
    outline = []
    for py in range(size):
        for px in range(size):
            if cv.idx[py][px]:
                continue
            best = None
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                qx, qy = px + dx, py + dy
                if cv.inside(qx, qy) and cv.owner[qy][qx] >= 0:
                    p = model.parts[cv.owner[qy][qx]]
                    if best is None or p.z > best.z:
                        best = p
            if best is not None:
                outline.append((px, py, palette.get(best.outline)))
    for px, py, c in outline:
        cv.idx[py][px] = c
    if model.post:
        model.post(cv)
    return cv.idx


# --- image helpers -----------------------------------------------------------

def bbox(img):
    pts = [(x, y) for y, row in enumerate(img) for x, v in enumerate(row) if v]
    if not pts:
        return (0, 0, 0, 0)
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def crop(img, x0, y0, w, h):
    return [[img[y][x] if 0 <= y < len(img) and 0 <= x < len(img[0]) else 0
             for x in range(x0, x0 + w)] for y in range(y0, y0 + h)]


def place(frames, size, out, bottom=None):
    """Crops same-size frames to out x out with the union bbox centred
    horizontally and either centred vertically or with its bottom at `bottom`."""
    boxes = [bbox(f) for f in frames]
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    if x1 - x0 + 1 > out or y1 - y0 + 1 > out:
        sys.exit(f"gen_sprite: art is {x1 - x0 + 1}x{y1 - y0 + 1}, larger than {out}")
    left = x0 - (out - (x1 - x0 + 1)) // 2
    top = y0 - (out - (y1 - y0 + 1)) // 2 if bottom is None else y1 - bottom
    return [crop(f, left, top, out, out) for f in frames]


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


# --- species -----------------------------------------------------------------

def ramp(*hexes):
    return [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in hexes]


def knightia(phase=0):
    """Knightia eocaena, Green River Fm (~51 Ma): a ~15 cm herring (Clupeidae).
    Fusiform, laterally compressed; terminal, slightly upturned mouth; big eye;
    one short triangular dorsal fin over the pelvic fins; small anal fin far back;
    deeply forked caudal; a keel of ventral scutes; no lateral line on the flank
    (clupeids lack one). Dark dorsum over silver flanks, as in living herrings."""
    ramps = {
        "outline": ramp("1c243c"),
        "dorsal": ramp("24466a", "346888", "508ca4", "78b4c4"),
        "silver": ramp("6e7c98", "9eacc4", "ccd6e6", "f4f8fc"),
        "fin": ramp("7a8896", "aab8bc", "d6dedc"),
        "cheek": ramp("dcc890"),
    }
    body = Loft(-24, 14,
                up=[(0, 0.5), (0.04, 2.0), (0.12, 4.4), (0.25, 6.9), (0.42, 7.9), (0.62, 6.6), (0.85, 3.8), (1.0, 2.6)],
                dn=[(0, 0.5), (0.04, 1.6), (0.12, 4.2), (0.27, 8.2), (0.44, 9.2), (0.64, 7.2), (0.86, 4.0), (1.0, 2.6)],
                mid=lambda t: 0.6 * (1 - t) - 0.3)

    def countershade(x, y):
        return "dorsal" if body.s(x, y) < -0.22 else "silver"

    tail = 0.82 if phase else 1.0  # tail sweeping towards the viewer foreshortens the fin
    top, bot = body.top, body.bottom
    tx = lambda x: 14 + (x - 14) * tail  # noqa: E731
    caudal = Poly([(13.5, -2.4), (tx(20.5), -6.8), (tx(28), -11.5), (tx(25.5), -6.5), (tx(22.5), -1.0),
                   (tx(22.5), 1.0), (tx(25.5), 6.5), (tx(28), 11.5), (tx(20.5), 6.8), (13.5, 2.4)])
    dorsal_fin = Poly([(-6.5, top(-6.5) + 1.2), (-4.5, top(-4.5) - 8.0), (-2.5, top(-2.5) - 6.0),
                       (2.5, top(2.5) - 1.6), (3.0, top(3.0) + 1.2)])
    anal_fin = Poly([(6.0, bot(6.0) - 1.0), (8.0, bot(8.0) + 4.0), (14.0, bot(14) + 2.2), (13.5, bot(13.5) - 1.0)])
    pa = 12 if phase else 0
    pelvic = Poly([(-4.0, bot(-4.0) - 1.0), *(( -4 + u, bot(-4.0) + v) for u, v in (rot(7.5, 3.5, pa), rot(6.0, 5.0, pa))),
                   (-1.0, bot(-1.0) - 1.0)])
    pectoral = Poly([(-14.0, 3.2), *((-14 + u, 4.0 + v) for u, v in (rot(9.0, 3.2, pa), rot(8.0, 5.0, pa))), (-13.0, 6.0)])

    fin = dict(normal=(0, 0, 1), outline=("fin", 0), light=0.2)  # hyaline fins: pale, outlined in grey
    parts = [
        Part(body, "silver", z=0, flat=0.45, region=countershade),
        Part(caudal, "fin", z=-1, **fin),
        Part(dorsal_fin, "fin", z=-1, **fin),
        Part(anal_fin, "fin", z=-1, **fin),
        Part(pelvic, "fin", z=-1, **fin),
        Part(pectoral, "fin", z=1, shadow=False, **fin),
    ]

    def details(cv):
        big = cv.scale >= 0.8
        # fin rays (every other ray, darker)
        if big:
            for v in (-8.5, -4.0, 4.0, 8.5):
                cv.line((15.0, v * 0.2), (tx(15 + abs(v) * 1.15), v), ("fin", 1))
            for k in range(1, 3):
                x = lerp(-5.5, 1.5, k / 3)
                cv.line((x, top(x)), (x + 1.5 - k, top(x) - 6 + k * 1.6), ("fin", 1))
        # operculum (gill cover): a darker arc with a hint of red gill behind it
        arc = [(-14.5 + 4.5 * math.cos(a), 1.2 + 7.0 * math.sin(a)) for a in
               (math.radians(d) for d in range(-75, 76, 15))]
        if big:  # the brassy sheen of a herring's cheek
            cv.disc((-15.2, 3.4), 1.1, "cheek", only_opaque=True)
        cv.polyline(arc, None, shade=-3)
        # scale rows on the dark back: a sparse lattice of darker pixels
        if big:
            for py in range(cv.h):
                for px in range(cv.w):
                    v = cv.idx[py][px]
                    if (v in cv.pal.index["dorsal"][1:] and py % 2 == 0 and (px + py) % 4 == 0
                            and cv.pal.ramp_of[v][1] < 3):
                        cv.shade(px, py, -1)
        # mouth: lower jaw slightly upturned; frame 2 gapes
        if phase and big:
            cv.line((-24.0, 0.3), (-20.0, 1.6), "outline")
            cv.line((-23.5, 1.4), (-20.5, 2.2), "outline")
            cv.set(*cv.pt(-23.0, 1.0), ("silver", 0))
        else:
            cv.line((-24.0, 0.6), (-20.0, 1.8), "outline")
        # ventral scutes: a serrated keel between the pectoral and anal fins
        if big:
            for x in range(-15, 6, 2):
                px, py = cv.pt(x, bot(x) - 0.6)
                cv.shade(px, py, -1)
        # eye
        e, r = (-16.8, -1.4), 3.0
        if big:
            cv.disc(e, r + 0.6, "outline")
            cv.disc(e, r - 0.2, ("silver", 2))
            cv.disc((e[0] - 0.5, e[1] + 0.3), r * 0.55, "outline")
            px, py = cv.pt(e[0] - 1.4, e[1] - 1.4)
            cv.set(px, py, ("silver", 3))
            cv.set(px + (1 if cv.flip else -1), py + 2, ("silver", 1))
        else:
            cv.disc(e, 1.6, "outline")
            px, py = cv.pt(e[0] - 0.8, e[1] - 0.8)
            cv.set(px, py, ("silver", 3))

    return Model(parts, ramps, details)


def turn(p, pivot, deg):
    x, y = rot(p[0] - pivot[0], p[1] - pivot[1], deg)
    return (pivot[0] + x, pivot[1] + y)


def mesodma(phase=0):
    """Mesodma, Hell Creek Fm (latest Cretaceous): a ~30 g multituberculate.
    Mouse-sized and rodent-like by convergence: short deep snout, procumbent
    lower incisors, a long tail (ptilodontoids had reversible hind feet and are
    reconstructed as climbers). Fur colour is unknown; a muted agouti brown with
    a pale belly is the conservative choice."""
    ramps = {
        "outline": ramp("2a1c16"),
        "fur": ramp("5a3a28", "82583c", "a87c56", "cca476"),
        "belly": ramp("b4967a", "d8c2a0", "f0e2c8"),
        "skin": ramp("8c5e5c", "bc8880", "e2b2a6"),
        "white": ramp("fcfcf4"),
    }
    sniff = 7 if phase else 0                   # frame 2: head up, sniffing
    neck = (-10.0, 2.0)
    H = lambda x, y: turn((x, y), neck, sniff)  # noqa: E731

    torso = Union([Ellipse(7.0, 2.5, 11.5, 9.8, -8), Ellipse(-4.0, 5.0, 9.0, 7.6, 5)], k=0.10)
    head = Union([Ellipse(*H(-16.0, -0.8), 8.8, 7.6, -12 + sniff),
                  Ellipse(*H(-22.8, 2.0), 5.2, 4.2, 10 + sniff)], k=0.10)
    ear = Ellipse(*H(-11.0, -7.6), 3.6, 4.2, 20 + sniff)
    thigh = Ellipse(10.0, 7.0, 6.2, 6.8, 20)

    lift = 1.8 if phase else 0.0
    near_fore = Tube([(-7.0, 8.5), (-8.5, 13.0), (-10.5, 16.0 - lift)], [3.0, 2.2, 1.7])
    near_fore_paw = Ellipse(-11.8, 16.8 - lift, 2.6, 1.4)
    far_fore = Tube([(-2.5, 9.0), (-3.0, 13.5), (-4.5, 16.5)], [2.6, 2.0, 1.6])
    far_fore_paw = Ellipse(-5.6, 17.2, 2.4, 1.3)
    near_hind = Tube([(10.0, 11.0), (8.0, 15.5), (6.5, 16.8)], [2.6, 2.0, 1.6])
    near_hind_foot = Ellipse(4.2, 17.6, 4.4, 1.5)
    far_hind = Tube([(15.0, 10.0), (14.5, 15.5), (13.0, 16.8)], [2.4, 1.8, 1.5])
    far_hind_foot = Ellipse(11.0, 17.6, 3.8, 1.4)
    curl = 2.0 if phase else 0.0
    tail = Tube([(16.0, 5.0), (22.0, 3.5), (26.5, -1.0), (28.5 - curl * 0.5, -7.0), (27.0 - curl, -12.0 + curl * 0.5),
                 (23.5 - curl, -14.5 + curl)], [2.6, 2.1, 1.8, 1.5, 1.3, 1.1])

    def underside(base):
        def region(x, y):
            return "belly" if y > base(x) else "fur"
        return region

    torso_region = underside(lambda x: 7.0 + 0.10 * x)
    jaw = H(-16.0, 2.6)
    jaw_slope = -0.10 + math.tan(math.radians(sniff))
    head_region = underside(lambda x: jaw[1] + (x - jaw[0]) * jaw_slope)

    far = dict(light=-0.25)
    parts = [
        Part(tail, "skin", z=-3, flat=0.5),
        Part(far_hind, "fur", z=-2, **far),
        Part(far_hind_foot, "skin", z=-1.9, **far),
        Part(far_fore, "fur", z=-2, **far),
        Part(far_fore_paw, "skin", z=-1.9, **far),
        Part(torso, "fur", z=0, flat=0.5, region=torso_region),
        Part(thigh, "fur", z=1, flat=0.5, inner=("fur", 0)),
        Part(near_hind, "fur", z=2, inner=("fur", 0)),
        Part(near_hind_foot, "skin", z=2.1, inner=("skin", 0)),
        Part(ear, "fur", z=2.5),
        Part(head, "fur", z=3, flat=0.5, region=head_region),
        Part(near_fore, "fur", z=4, inner=("fur", 0)),
        Part(near_fore_paw, "skin", z=4.1, inner=("skin", 0)),
    ]

    def details(cv):
        big = cv.scale >= 0.8
        # inner ear
        cv.disc(H(-10.8, -7.0), 2.1 if big else 1.2, ("skin", 1), only_opaque=True)
        # fur texture: short darker dashes on the back
        if big:
            for py in range(cv.h):
                for px in range(cv.w):
                    v = cv.idx[py][px]
                    if v in cv.pal.index["fur"][1:] and py % 3 == 0 and (px + py) % 5 == 0:
                        cv.shade(px, py, -1)
        # toes: tiny darker gaps on the near feet
        if big:
            for x in (-12.5, -11.0):
                cv.shade(*cv.pt(x, 17.6 - lift), -1)
            for x in (2.0, 3.6, 5.2):
                cv.shade(*cv.pt(x, 18.4), -1)
        # nose, mouth, incisor
        nose = H(-27.0, 0.6)
        cv.disc(nose, 1.3 if big else 0.8, ("skin", 1))
        if big:
            cv.set(*cv.pt(*H(-27.3, 0.0)), ("skin", 2))
            cv.line(H(-26.0, 3.2), H(-22.5, 4.4), "outline")
            cv.set(*cv.pt(*H(-25.0, 4.6)), "white")
            cv.set(*cv.pt(*H(-25.0, 5.6)), "white", only_opaque=False)
        # eye: a beady black eye with a highlight
        e = H(-18.2, -2.0)
        if big:
            cv.disc(e, 2.6, "outline")
            px, py = cv.pt(*e)
            cv.set(px + (1 if cv.flip else -1), py - 1, "white")
        else:
            cv.disc(e, 1.2, "outline")

    def post(cv):
        if cv.scale < 0.8:
            return
        # whiskers drawn over the outline, in the pale belly colour
        for a, b in (((-24.0, 1.5), (-31.0, -1.0)), ((-24.0, 2.5), (-31.5, 3.5))):
            for px, py in cv.pixels_on_line(H(*a), H(*b)):
                if cv.inside(px, py) and not cv.idx[py][px]:
                    cv.idx[py][px] = cv.pal.get(("belly", 0))

    return Model(parts, ramps, details, post)


FOOTPRINT_MAMMAL = [
    "................",
    "................",
    "................",
    "................",
    "......#.#.......",
    "....#.....#.....",
    "......###.......",
    "....#.###.#.....",
    ".....#####......",
    "......###.......",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]


SPECS = {
    # folder name: model function, render scales (front, back, icon), the pigment
    # variant (hue shift in degrees, saturation and value factors per ramp), footprint
    "knightia": dict(model=knightia, front=1.0, back=1.08, icon=0.58,
                     shiny={"dorsal": dict(deg=-165, sat=1.15, val=1.05),
                            "fin": dict(deg=-180, sat=2.2, val=1.0)},
                     footprint=None),
    "mesodma": dict(model=mesodma, front=0.9, back=0.95, icon=0.46,
                    shiny={"fur": dict(deg=-12, sat=0.45, val=1.12)},
                    footprint=FOOTPRINT_MAMMAL),
}


# --- output ------------------------------------------------------------------

def pigment_variant(palette, shiny):
    colors = list(palette.colors)
    for name, k in shiny.items():
        for idx in palette.index[name]:
            colors[idx] = shift_hue(colors[idx], k["deg"], k.get("sat", 1.0), k.get("val", 1.0))
    return colors


def build(name, preview_dir=None):
    spec = SPECS[name]
    make = spec["model"]
    pal = Palette(make(0).ramps)
    size = 96

    def frames(scale, flip, out, bottom=None):
        imgs = [render(make(ph), size, scale, flip, (size / 2, size / 2), pal) for ph in (0, 1)]
        return place(imgs, size, out, bottom)

    front = frames(spec["front"], False, 64)
    back = frames(spec["back"], True, 64)[0]
    icon = frames(spec["icon"], False, 32, bottom=29)
    icon[1] = icon[1][1:] + [[0] * 32]  # frame 2 bobs up a pixel

    dst = os.path.join(ROOT, "graphics/pokemon/strata", name)
    os.makedirs(dst, exist_ok=True)
    shiny = pigment_variant(pal, spec["shiny"])
    write_indexed_png(os.path.join(dst, "anim_front.png"), front[0] + front[1], pal.colors)
    write_indexed_png(os.path.join(dst, "back.png"), back, pal.colors)
    write_pal(os.path.join(dst, "normal.pal"), pal.colors)
    write_pal(os.path.join(dst, "shiny.pal"), shiny)
    icon_pal, remap, icon_colors = icon_palette_fit(icon, pal)
    icon = [[[remap[v] for v in row] for row in f] for f in icon]
    write_indexed_png(os.path.join(dst, "icon.png"), icon[0] + icon[1], icon_colors)
    fp = spec["footprint"] or ["." * 16] * 16
    write_indexed_png(os.path.join(dst, "footprint.png"), [[1 if c == "#" else 0 for c in row] for row in fp],
                      [(255, 255, 255), (98, 98, 98)], depth=1)
    for old in ("front.png",):
        if os.path.exists(os.path.join(dst, old)):
            os.remove(os.path.join(dst, old))

    fb, bb = bbox(front[0]), bbox(back)
    fields = [
        f".frontPicSize = {coords_size(fb[2] - fb[0] + 1, fb[3] - fb[1] + 1)},",
        f".frontPicYOffset = {63 - fb[3]},",
        f".backPicSize = {coords_size(bb[2] - bb[0] + 1, bb[3] - bb[1] + 1)},",
        f".backPicYOffset = {63 - bb[3]},",
        f".iconPalIndex = {icon_pal},",
    ]
    with open(os.path.join(dst, "CUSTOM"), "w") as f:
        f.write("# Generated by tools/strata/gen_sprite.py. While this file exists, gen_species.py\n"
                "# keeps the sprites in this folder and uses these presentation fields.\n")
        f.write("\n".join(fields) + "\n")
    print(f"{name}: front {fb}, back {bb}, icon palette {icon_pal}, {sum(1 for c in pal.colors if c)} colours")

    if preview_dir:
        write_preview(preview_dir, name, front, back, icon, pal.colors, shiny, icon_colors)


def write_preview(outdir, name, front, back, icon, normal, shiny, icon_colors):
    """<name>_sheet.png: 1x row (front frames, back, shiny front, icons), then the same at 3x."""
    os.makedirs(outdir, exist_ok=True)
    bg = (232, 232, 224)
    tiles = [(front[0], normal), (front[1], normal), (back, normal), (front[0], shiny), (back, shiny),
             (icon[0], icon_colors), (icon[1], icon_colors)]

    def sheet(scale):
        w = sum(len(t[0][0]) * scale + 4 for t in tiles)
        h = 64 * scale
        img = [[bg] * w for _ in range(h)]
        x = 0
        for pic, cols in tiles:
            for y, row in enumerate(pic):
                for xx, v in enumerate(row):
                    if v:
                        for dy in range(scale):
                            for dx in range(scale):
                                img[y * scale + dy][x + xx * scale + dx] = cols[v]
            x += len(pic[0]) * scale + 4
        return img

    one, three = sheet(1), sheet(3)
    w = max(len(one[0]), len(three[0]))
    rows = [r + [bg] * (w - len(r)) for r in one] + [[(255, 255, 255)] * w] * 4 + [r + [bg] * (w - len(r)) for r in three]
    path = os.path.join(outdir, f"{name}_sheet.png")
    write_png(path, w, len(rows), rows)
    print("wrote", path)
    big = [[normal[v] if v else bg for v in row0 + row1 for _ in range(6)]
           for row0, row1 in zip(front[0], front[1]) for _ in range(6)]
    write_png(os.path.join(outdir, f"{name}_front_x6.png"), len(big[0]), len(big), big)
    write_battle_mock(outdir, name, front[0], back, normal)


def write_battle_mock(outdir, name, front, back, colors):
    """<name>_battle.png: the creature as foe and as your mon on the tall-grass
    battle background, stock (top) and impact-winter palette (bottom), at 2x.
    Positions follow Emerald's battler coords: foe (176, 40), player (72, 80),
    plus the pic Y offsets that gen_sprite writes to CUSTOM."""
    import gen_tilesets
    from maprender import read_pal as rp
    fb, bb = bbox(front), bbox(back)
    stock = rp(os.path.join(ROOT, "graphics/battle_environment/tall_grass/palette.pal"))
    panels = []
    for pal in (stock, gen_tilesets.transform_pal(stock, "impact_winter")):
        img = [r[:240] for r in gen_tilesets.render_battle_bg("tall_grass", pal)[:160]]
        for y in range(112, 160):
            img[y] = [(40, 48, 64)] * 240
        for pic, (cx, cy) in ((front, (176, 40 + 63 - fb[3])), (back, (72, 80 + 63 - bb[3]))):
            for y, row in enumerate(pic):
                for x, v in enumerate(row):
                    sx, sy = cx - 32 + x, cy - 32 + y
                    if v and 0 <= sx < 240 and 0 <= sy < 112:
                        img[sy][sx] = colors[v]
        panels += [r for r in img for _ in range(2)]
        panels += [[(255, 255, 255)] * 240] * 4
    rows = [[c for c in r for _ in range(2)] for r in panels]
    path = os.path.join(outdir, f"{name}_battle.png")
    write_png(path, len(rows[0]), len(rows), rows)
    print("wrote", path)


def main():
    args = sys.argv[1:]
    preview = None
    if "--preview" in args:
        i = args.index("--preview")
        preview = args[i + 1]
        del args[i:i + 2]
    for name in args or list(SPECS):
        if name not in SPECS:
            sys.exit(f"gen_sprite: no spec for {name} (have: {', '.join(SPECS)})")
        build(name, preview)


if __name__ == "__main__":
    main()
