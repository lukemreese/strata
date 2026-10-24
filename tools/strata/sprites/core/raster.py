"""The rasteriser: coverage, dome shading, cast shadows, contours, painted
details and the 1-px outline, straight into palette indices.

render(model, size, scale, flip, origin, palette) -> rows of palette indices.
"""

import math

from .geom import clamp

LIGHT = (-0.50, -0.70, 0.75)  # from the upper left, towards the viewer
_n = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _n for c in LIGHT)
AMBIENT, DIFFUSE = 0.10, 0.80  # a surface facing the viewer lands on the 2nd-lightest of 4 shades
SS = 4  # supersampling per axis for coverage


class Canvas:
    """Index image + per-pixel owning part; model -> screen transform.
    Painters (Model.details / Model.post) draw on it in model coordinates."""
    def __init__(self, size, scale, flip, palette, origin):
        self.w = self.h = size
        self.scale, self.flip, self.pal = scale, flip, palette
        self.ox, self.oy = origin
        self.idx = [[0] * size for _ in range(size)]
        self.owner = [[-1] * size for _ in range(size)]

    @property
    def big(self):
        """True at battle-sprite scale: draw fine details. Icons and overworld
        sprites render below 0.8 and should drop them."""
        return self.scale >= 0.8

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

    def texture(self, ramp, rule, delta=-1, min_level=1, max_level=None):
        """Darkens (delta < 0) pixels of `ramp` whose levels are in
        [min_level, max_level) where rule(px, py) is true: fur dashes, scale
        lattices, mottling. Pixel coordinates, so the pattern is screen-aligned."""
        idxs = self.pal.index[ramp]
        hi = len(idxs) if max_level is None else max_level
        allowed = set(idxs[min_level:hi])
        for py in range(self.h):
            for px in range(self.w):
                if self.idx[py][px] in allowed and rule(px, py):
                    self.shade(px, py, delta)


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
