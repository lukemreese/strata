"""Maths and shape primitives for the sprite rasteriser.

Shapes live in model units (sprite pixels at scale 1), centred on the origin,
head to the LEFT. Every shape has q(x, y): > 0 inside, rising to 1 on its ridge,
continuous outside so a numeric gradient gives the edge normal, and a bbox
(x0, y0, x1, y1) in model units.
"""

import math


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


def turn(p, pivot, deg):
    """Rotates point p about pivot by deg (positive = clockwise on screen, i.e.
    a point below the pivot swings to the left/forward)."""
    x, y = rot(p[0] - pivot[0], p[1] - pivot[1], deg)
    return (pivot[0] + x, pivot[1] + y)


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
    """A flat polygon (fins, ears, frills). Give its Part a `normal`."""
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


class Model:
    """What a body plan returns for one view and pose: parts, palette ramps,
    and optional painters. `details(cv)` runs after shading and contours,
    before the outer outline; `post(cv)` runs after the outline."""
    def __init__(self, parts, ramps, details=None, post=None):
        self.parts, self.ramps, self.details, self.post = parts, ramps, details, post
