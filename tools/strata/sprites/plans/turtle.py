"""Turtle body plan: snapping turtles and a tortoise, in side view, plus a
top-down shell view for the back sprite and the overworld end-on frames.

Species (taxonomy.py):
    emarginachel  Emarginachelys (Hell Creek Fm, MT, 8 kg)       the turtle starter
    protochelyd   Protochelydra (Paleocene, ND, 25 kg)           high-domed snapper
    chelydra      Chelydra serpentina (Living; MT, 10 kg)        common snapper
    macrochelys   Macrochelys (Miocene Great Plains, NE, 80 kg)  alligator snapper
    stylemys      Stylemys nebrascensis (Brule Fm, SD, 15 kg)    land tortoise

The four snappers are one lineage (the 'stasis' line), so they share one set of
proportions and differ by a few scalar knobs; the tortoise uses the same
machinery with `legs="tortoise"`. Everything is derived from the knobs, so the
specs stay short and the lineage stays visibly related.

Ramps the template uses:
    outline  1   very dark shell hue
    shell    4   carapace (seams use its darkest shade)
    skin     3   head, neck, legs, tail
    belly    3   throat, jaw, the skin under the shell; lightest = eye highlight
    beak     2   horny beak and claws
    eye      1   iris
    mouth    1   mouth lining (Macrochelys: the pink lure)

Knobs (see DEFAULTS): dome (carapace height), dome_shape (exponent: < 0.7 is
boxier), peak (where the dome is highest, 0 = front), front_lift, keel (height of
the vertebral knobs; lateral keels follow), keel_w (knob width), serr / serr_len
(rear marginal serrations), wid (shell width/length from above), head (head
size), hook (beak hook), neck (neck length), tail (tail length), crest (tail
saw-crest height), legs ("snapper" | "tortoise"), eye_k, gape (frame 2 jaw angle),
lure (Macrochelys' tongue lure), rings (tortoise growth annuli on the scutes),
tubercles (skin texture), algae (sparse lighter flecks on the carapace).

Views:
    side()       profile, head left; frame 2 lunges and gapes (tortoise: lifts its head)
    back()       the carapace from above and behind, head away and to the right
    overworld()  the same top-down model, head towards (south) or away from (north)
                 the camera; step 1 moves the diagonal leg pairs

Model units: carapace from x = -16 to 16, ground at y = 12.

New primitive (plan-local, worth promoting to core): `Ground(shape, yaw, fs, h)`
evaluates any shape on a tilted ground plane: the shape is drawn in plan
coordinates (u right, v forward), turned by `yaw` about the vertical, viewed
from above with foreshortening `fs` and lifted `h` units. Shading, outline and
contours all work unchanged, so a top-down animal is built like a side one.
"""

import math

from ..core.geom import Ellipse, Tube, Union, Loft, Poly, Part, Model, turn, clamp, lerp
from ..core.plan import BodyPlan

FOOTPRINT_TURTLE = [
    "................",
    "................",
    "...#........#...",
    "..###......###..",
    "...#........#...",
    "................",
    "................",
    "......####......",
    "......####......",
    "................",
    "................",
    "...#........#...",
    "..###......###..",
    "...#........#...",
    "................",
    "................",
]

DEFAULTS = dict(
    dome=9.0, dome_shape=0.75, peak=0.45, front_lift=1.2,
    keel=1.0, keel_w=0.07, serr=3, serr_len=2.4, wid=0.80,
    head=1.0, hook=1.0, neck=1.0, neck_up=4, tail=1.0, crest=1.0,
    legs="snapper", eye_k=1.0, gape=24, lunge=8, lure=False,
    rings=False, tubercles=True, algae=False,
    far_light=-0.25, walk_swing=14,
    ow=dict(tracks="TRACKS_FOOT", end_zoom=1.3),
)

GROUND = 12.0
X0, X1 = -16.0, 16.0
HEAD_SCALE = 1.15   # heads a little larger than life, for readability at 1x

# Head geometry in head units (scaled by `head`), relative to the back of the
# skull; x forward is negative. cran: (cx, cy, rx, ry, angle) ellipses.
# beak: upper-beak polygon, its 4th point is the hook tip (lowered by `hook`).
HEAD_SNAP = dict(
    cran=[(-3.8, -1.2, 5.2, 3.3, -6), (-8.4, 0.2, 3.0, 2.1, -16)],
    jaw=((-5.0, 2.4), (5.0, 2.1)), hinge=(-0.8, 1.5),
    tip_up=(-10.9, 2.0), tip_lo=(-9.4, 2.9),
    beak=[(-8.8, -1.0), (-10.4, -0.4), (-11.5, 0.9), (-11.0, 1.8), (-9.6, 1.8)],
    lbeak=[(-7.0, 2.1), (-9.8, 2.2), (-9.4, 3.4), (-7.0, 3.8)],
    eye=(-6.4, -1.6), nostril=(-10.6, -0.2),
)
HEAD_TORT = dict(
    cran=[(-3.6, -0.6, 4.2, 3.3, -4), (-6.6, 0.4, 2.6, 2.4, -12)],
    jaw=((-4.4, 2.1), (3.8, 1.7)), hinge=(-0.8, 1.4),
    tip_up=(-8.8, 1.4), tip_lo=(-8.2, 2.4),
    beak=[(-7.0, 0.6), (-8.9, 0.3), (-9.2, 1.2), (-8.6, 1.8), (-7.4, 2.0)],
    lbeak=[(-6.0, 2.4), (-8.0, 2.3), (-7.8, 3.2), (-6.0, 3.4)],
    eye=(-4.9, -0.9), nostril=(-8.4, -0.1),
)


# ---------------------------------------------------------------- the carapace

def _vert_t(k):
    """Centre (t along the shell) of vertebral scute k (0..4)."""
    return 0.15 + 0.175 * k


def _shell(p):
    dome, shape, pk = p["dome"], p["dome_shape"], p["peak"]
    keel, kw = p["keel"], p["keel_w"]

    def prof(t):
        s = 0.5 * t / pk if t < pk else 0.5 + 0.5 * (t - pk) / (1 - pk)
        return math.sin(math.pi * clamp(s, 0, 1)) ** shape

    def knobs(t):
        k = 0.0
        for i in range(5):
            d = (t - _vert_t(i) - 0.03) / kw   # knobs sit on the rear half of each scute
            if abs(d) < 1:
                k = max(k, (math.cos(d * math.pi / 2)) ** 1.5)
        return keel * k * prof(t) ** 0.3

    ts = [i / 48 for i in range(49)]
    up = [(t, 0.6 + dome * prof(t) + knobs(t)) for t in ts]
    dn = [(t, 1.0 + 1.3 * math.sin(math.pi * t) ** 0.5) for t in ts]
    fl = p["front_lift"]
    return Loft(X0, X1, up=up, dn=dn, mid=lambda t: -fl * (1 - t))


def _serrations(p, shell, phase=0):
    """Rear marginal teeth, pointing back and down."""
    n, ln = p["serr"], p["serr_len"]
    polys = []
    for i in range(n):
        x = X1 - 0.6 - i * 3.2
        b = shell.bottom(x)
        polys.append(Poly([(x - 2.6, b - 1.6), (x + ln * 0.75, b + ln * 0.55 - 0.3), (x - 0.4, b - 0.3)]))
    return polys


# ---------------------------------------------------------------- side view

def _legs(p, phase, step):
    tort = p["legs"] == "tortoise"
    R = 1.3 if tort else 1.0
    if tort:  # columnar, elephantine, short; round stumpy feet (the shell rides low)
        legs = [
            dict(near=False, swing=1, pts=[(-8.0, 1.0), (-9.0, 4.5), (-9.0, 7.5)], radii=[3.4, 3.4, 3.2],
                 foot=(-9.5, 8.6, 3.4, 1.4)),
            dict(near=False, swing=-1, pts=[(10.5, 1.5), (12.0, 4.5), (12.0, 7.5)], radii=[3.4, 3.2, 3.0],
                 foot=(12.4, 8.6, 3.2, 1.4)),
            dict(near=True, swing=-1, pts=[(7.5, 2.0), (8.2, 5.0), (8.2, 7.6)], radii=[4.0, 3.8, 3.5],
                 foot=(8.6, 8.5, 3.8, 1.6)),
            dict(near=True, swing=1, fore=True, pts=[(-11.0, 1.5), (-12.6, 4.5), (-12.8, 7.6)],
                 radii=[3.8, 3.8, 3.6], foot=(-13.2, 8.5, 3.9, 1.6)),
        ]
    else:  # stout, splayed; long-clawed feet
        legs = [
            dict(near=False, swing=1, pts=[(-8.0, 1.5), (-10.0, 6.0), (-10.5, 9.8)], radii=[2.8, 2.4, 2.1],
                 foot=(-12.0, 10.9, 3.0, 1.2)),
            dict(near=False, swing=-1, pts=[(10.0, 2.0), (12.5, 6.0), (13.2, 9.8)], radii=[3.0, 2.6, 2.2],
                 foot=(14.6, 10.9, 3.0, 1.2)),
            dict(near=True, swing=-1, pts=[(7.0, 2.5), (8.6, 6.5), (8.8, 9.8)], radii=[3.4, 2.9, 2.5],
                 foot=(10.4, 10.8, 3.6, 1.4)),
            dict(near=True, swing=1, fore=True, pts=[(-11.0, 2.0), (-13.4, 6.0), (-14.0, 9.8)],
                 radii=[3.2, 2.7, 2.4], foot=(-15.6, 10.8, 3.4, 1.4)),
        ]
    for leg in legs:
        pts, foot = leg["pts"], leg["foot"]
        if step:
            hip, deg = pts[0], p["walk_swing"] * leg["swing"]
            pts = [pts[0]] + [turn(q, hip, deg) for q in pts[1:]]
            fc = turn(foot[:2], hip, deg)
            foot = (fc[0], fc[1] - (1.0 if leg["swing"] > 0 else 0.0), *foot[2:])
        yield leg, Tube(pts, [r * (1.0 if tort else R) for r in leg["radii"]]), foot


def _head_geom(p, phase):
    """Neck tube, head anchor and the transform for head-local points."""
    hk, nk = p["head"] * HEAD_SCALE, p["neck"]
    base = (-11.0, 1.4)
    lunge = p["lunge"] if phase else 0
    up = p["neck_up"] + (lunge if p["legs"] == "tortoise" else 0)
    A0 = (-11.0 - 8.5 * nk, -1.2 - 1.0 * nk)          # back of the skull at rest
    A = turn(A0, base, up)
    if phase and p["legs"] != "tortoise":             # the snap: neck shoots forward
        A = (A[0] - 2.5 * nk, A[1] - 0.5)
    tilt = up * 0.5 - (6 if phase and p["legs"] != "tortoise" else 0)

    def H(dx, dy):
        x, y = turn((A[0] + dx * hk, A[1] + dy * hk), A, tilt)
        return (x, y)
    mid = ((base[0] + A[0]) / 2, (base[1] + A[1]) / 2 + 0.6)
    neck = Tube([base, mid, H(-1.0, 0.6)], [3.4 * hk ** 0.5, 3.0 * hk ** 0.6, 2.9 * hk])
    return neck, H, tilt


def side(p, phase=0, step=None):
    if step is not None:
        phase = 0
    tort = p["legs"] == "tortoise"
    shell = _shell(p)
    neck, H, tilt = _head_geom(p, phase)
    hk, hook = p["head"] * HEAD_SCALE, p["hook"]
    far = dict(light=p["far_light"])

    # head: cranium + snout (one dome); the lower jaw is a separate part so the
    # mouth line is a contour, and it can drop open in frame 2
    g = HEAD_TORT if tort else HEAD_SNAP
    head = Union([Ellipse(*H(cx, cy), rx * hk, ry * hk, tilt + a) for cx, cy, rx, ry, a in g["cran"]], k=0.10)
    hinge = H(*g["hinge"])
    gape = -p["gape"] if (phase and not tort) else 0
    J = lambda x, y: turn(H(x, y), hinge, gape)  # noqa: E731
    (jx, jy), (jrx, jry) = g["jaw"]
    jaw = Ellipse(*J(jx, jy), jrx * hk, jry * hk, tilt - 6 + gape)
    tip_up = H(*g["tip_up"])
    tip_lo = J(*g["tip_lo"])
    # upper beak: a horn sheath whose tip hooks down over the lower jaw
    ub = Poly([H(x, y + (hook * 0.9 if k == 3 else 0)) for k, (x, y) in enumerate(g["beak"])])
    lb = Poly([J(x, y) for x, y in g["lbeak"]])

    parts = []
    legs = list(_legs(p, phase, step))
    for leg, tube, foot in legs:
        if not leg["near"]:
            parts += [Part(tube, "skin", z=-3, **far), Part(Ellipse(*foot), "skin", z=-2.9, **far)]

    # tail with the saw crest (snappers) or a short cone (tortoise)
    tk = p["tail"]
    tbase = (12.0, 2.6)
    tp = [(12.0, 2.6), (18.0, 5.6), (23.0, 9.0), (27.0, 10.9), (30.5, 11.0)]
    if phase and not tort:
        tp = [tp[0], (18.0, 5.4), (23.2, 8.6), (27.6, 10.2), (31.0, 9.8)]
    tp = [(tbase[0] + (x - tbase[0]) * tk, tbase[1] + (y - tbase[1]) * min(1.0, tk ** 0.7)) for x, y in tp]
    tr = [3.2, 2.6, 1.9, 1.3, 0.8] if not tort else [3.0, 2.4, 1.8, 1.3, 0.9]
    tail = Tube(tp, tr)
    parts.append(Part(tail, "skin", z=-1.5))
    if p["crest"] > 0:
        n = 7
        for i in range(n):
            t = 0.08 + 0.8 * i / n
            seg = t * (len(tp) - 1)
            j = min(int(seg), len(tp) - 2)
            u = seg - j
            (ax, ay), (bx, by) = tp[j], tp[j + 1]
            cx, cy = lerp(ax, bx, u), lerp(ay, by, u)
            r = lerp(tr[j], tr[j + 1], u)
            dx, dy = bx - ax, by - ay
            L = math.hypot(dx, dy)
            tx, ty, nx, ny = dx / L, dy / L, dy / L, -dx / L
            h = p["crest"] * (2.2 - 1.4 * t)
            w = 0.95
            b0 = (cx + nx * (r - 0.5) - tx * w, cy + ny * (r - 0.5) - ty * w)
            b1 = (cx + nx * (r - 0.5) + tx * w, cy + ny * (r - 0.5) + ty * w)
            apex = (cx + nx * (r + h) + tx * 0.5, cy + ny * (r + h) + ty * 0.5)
            parts.append(Part(Poly([b0, apex, b1]), "skin", z=-1.6, normal=(-0.3, -0.6, 0.75)))

    # the soft body under the shell, between the legs
    parts.append(Part(Ellipse(0.0, 3.6, 13.0, 3.0), "belly", z=-1, light=-0.15))
    for leg, tube, foot in legs:
        if leg["near"]:
            parts += [Part(tube, "skin", z=0, inner=("skin", 0)),
                      Part(Ellipse(*foot), "skin", z=0.1, inner=("skin", 0))]
    for poly in _serrations(p, shell, phase):
        parts.append(Part(poly, "shell", z=0.9, normal=(0.1, 0.35, 0.93), inner=("shell", 0)))
    parts.append(Part(shell, "shell", z=1, flat=0.55))
    parts.append(Part(neck, "skin", z=0.8, region=lambda x, y: "belly" if y > neck_belly(x) else "skin"))
    if gape:  # mouth lining (Macrochelys: dark, so the pink lure shows)
        gap = Poly([hinge, tip_up, tip_lo])
        parts.append(Part(gap, "skin" if p["lure"] else "mouth", z=1.9, normal=(0.2, 0.3, 0.9),
                          light=-0.6 if p["lure"] else 0.0))
    parts += [Part(jaw, "belly", z=2.0, inner=("skin", 0)),
              Part(lb, "beak", z=2.05, normal=(0.0, 0.2, 1.0), inner=("beak", 0)),
              Part(head, "skin", z=2.2, flat=0.5),
              Part(ub, "beak", z=2.3, normal=(-0.2, -0.3, 0.93), inner=("beak", 0))]

    def neck_belly(x):
        # lower third of the neck is the pale throat
        bx, by = -11.0, 1.4
        ax, ay = H(-1.0, 0.6)
        t = clamp((x - bx) / (ax - bx), 0, 1) if ax != bx else 0
        return lerp(by, ay, t) + 0.8 * hk

    def details(cv):
        big = cv.big
        _shell_seams(cv, p, shell, big)
        if big and p["tubercles"]:  # sparse tubercles on the skin
            cv.texture("skin", lambda px, py: py % 2 == 0 and (px + py // 2 * 3) % 4 == 0, -1, 1, 3)
        if big and p["algae"]:
            cv.texture("shell", lambda px, py: (px * 7 + py * 13) % 23 == 0, +1, 1, 3)
        if big:  # claws on the near feet: pale beak-coloured points
            for leg, _, foot in legs:
                if leg["near"]:
                    fx, fy, frx, fry = foot
                    for k in range(3 if not tort else 2):
                        x = fx - frx + 0.6 + k * (1.3 if not tort else 2.0)
                        cv.set(*cv.pt(x - 0.6, fy + fry * 0.7), ("beak", 1))
        if big:
            cv.set(*cv.pt(*H(*g["nostril"])), "outline")
        if gape and big and p["lure"]:  # the worm lure on the tongue
            lx, ly = J(-5.6, 1.3)
            for d in (-1.0, -0.2, 0.6):
                cv.set(*cv.pt(lx + d, ly - abs(d + 0.2) * 0.5), "mouth")
        _eye(cv, H(*g["eye"]), 1.45 * hk * p["eye_k"])

    return Model(parts, p["ramps"], details)


def _eye(cv, e, r):
    if cv.big:  # a 2x2 gold iris in a dark ring, pupil in its front-lower pixel
        px, py = cv.pt(*e)
        f = 1 if cv.flip else -1
        n = 3 if r * cv.scale > 2.1 else 2 if r * cv.scale > 1.0 else 1
        for dy in range(-1, n + 1):
            for dx in range(-1, n + 1):
                corner = dx in (-1, n) and dy in (-1, n)
                if not corner:
                    inner = 0 <= dx < n and 0 <= dy < n
                    cv.set(px + f * dx, py + dy, "eye" if inner else "outline")
        cv.set(px + f * (n - 1), py + n - 1, "outline")  # f points to the front
    else:
        cv.disc(e, max(0.9 / cv.scale * 0.5, r * 0.7), "outline")


def _shell_seams(cv, p, shell, big):
    """Marginal row, costal and vertebral seams (and growth rings) in side view."""
    rim = 2.5
    dark = ("shell", 0)
    xs = [X0 + 1.2 + i * 0.5 for i in range(int((X1 - X0 - 2.4) / 0.5) + 1)]

    def ym(x):
        return max(shell.top(x) + 1.0, shell.bottom(x) - rim)

    def yv(x):  # the vertebral/costal seam runs a little below the crest
        return min(ym(x) - 1.0, shell.top(x) + 2.4 + 0.12 * p["dome"] + 0.4 * p["keel"])

    cv.polyline([(x, ym(x)) for x in xs], dark)
    if not big:
        return
    for i in range(10):  # marginal seams
        x = X0 + 2.0 + i * 3.1
        cv.line((x, ym(x)), (x + 0.2, shell.bottom(x) - 0.4), dark)
    vx = [x for x in xs if X0 + 3.2 <= x <= X1 - 2.4]
    cv.polyline([(x, yv(x)) for x in vx], dark)
    tb = [X0 + 32 * t for t in (0.34, 0.53, 0.72)]  # costal seams
    for x in tb:
        lean = x * 0.18
        cv.line((x + lean, ym(x + lean) - 0.2), (x, yv(x) + 0.3), dark)
    for k in range(4):  # vertebral seams, short, on the crest
        x = X0 + 32 * (_vert_t(k) + 0.0875)
        cv.line((x, yv(x) - 0.3), (x - 0.4, shell.top(x) + 0.9), dark)
    if p["rings"]:  # growth annuli: a paler areola in the middle of each costal
        edges = [X0 + 3.2] + tb + [X1 - 2.4]
        for a, b in zip(edges, edges[1:]):
            cx = (a + b) / 2
            cy = (ym(cx) + yv(cx)) / 2
            _shade_disc(cv, (cx, cy + 0.3), 1.5, +1)
        for k in range(5):
            x = X0 + 32 * _vert_t(k)
            if X0 + 4 < x < X1 - 3:
                _shade_disc(cv, (x, (shell.top(x) + yv(x)) / 2 + 0.2), 1.0, +1)


def _shade_disc(cv, c, r, delta):
    """Shifts the shade of the opaque pixels within r model units of c."""
    cx, cy = cv.pt(*c)
    rs = r * cv.scale
    for py in range(int(cy - rs) - 1, int(cy + rs) + 2):
        for px in range(int(cx - rs) - 1, int(cx + rs) + 2):
            if (px - cx) ** 2 + (py - cy) ** 2 <= rs * rs and cv.inside(px, py) \
                    and cv.pal.ramp_of.get(cv.idx[py][px], ("", 0))[1] > 0:  # keep seams
                cv.shade(px, py, delta)


# ---------------------------------------------------------------- top-down views

class Ground:
    """A shape drawn in plan coordinates (u right, v forward) on a ground plane:
    turned by `yaw` degrees about the vertical (0 = head away from the camera,
    positive turns the head to the right), foreshortened by `fs` (sin of the
    camera elevation) and lifted `h` units (screen up by h * `ch`)."""
    def __init__(self, shape, yaw, fs, h=0.0, ch=0.7):
        self.s, self.fs, self.h, self.ch = shape, fs, h, ch
        a = math.radians(yaw)
        self.c, self.sn = math.cos(a), math.sin(a)
        x0, y0, x1, y1 = shape.bbox
        pts = [self.to_screen(u, v) for u in (x0, x1) for v in (-y0, -y1)]
        # plan shapes are written with y = -v (forward is up), so bbox y is -v
        self.bbox = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))

    def to_screen(self, u, v):
        gx = u * self.c + v * self.sn
        gz = -u * self.sn + v * self.c
        return gx, -gz * self.fs - self.h * self.ch

    def to_plan(self, x, y):
        gx, gz = x, -(y + self.h * self.ch) / self.fs
        u = gx * self.c - gz * self.sn
        v = gx * self.sn + gz * self.c
        return u, v

    def q(self, x, y):
        u, v = self.to_plan(x, y)
        return self.s.q(u, -v)


def topdown(p, yaw, fs, phase=0, step=None, ow=False):
    """The turtle from above. Plan shapes use (u, -v): u right, v forward."""
    tort = p["legs"] == "tortoise"
    a = 16.0
    b = a * p["wid"]
    hk = p["head"] * HEAD_SCALE
    dome = p["dome"]
    hs = dome * 0.55 + 1.0
    toward = math.cos(math.radians(yaw)) < 0       # head towards the camera (south)
    G = lambda shape, h=0.0: Ground(shape, yaw, fs, h)  # noqa: E731

    def S(u, v, h=hs):
        return G(Ellipse(0, 0, 1, 1), h).to_screen(u, v)

    far = dict(light=p["far_light"])
    parts = []
    # legs: diagonal pairs alternate on the walk step
    sw = (2.2 if step else -0.8) if step is not None else 0.0
    lr = 1.35 if tort else 1.0
    legs = []
    for su in (-1, 1):
        f = sw * su
        legs.append(("fore", su, Tube([(su * b * 0.70, -(a * 0.48)), (su * b * 1.10, -(a * 0.62 + f)),
                                      (su * b * 1.22, -(a * 0.80 + f))], [3.0 * lr, 2.6 * lr, 2.4 * lr]),
                     (su * b * 1.26, -(a * 0.86 + f))))
        legs.append(("hind", su, Tube([(su * b * 0.70, a * 0.50), (su * b * 1.05, a * (0.68) - f),
                                      (su * b * 1.12, a * 0.84 - f)], [3.2 * lr, 2.8 * lr, 2.5 * lr]),
                     (su * b * 1.14, a * 0.90 - f)))
    for kind, su, tube, foot in legs:
        nearer = (kind == "fore") == toward
        parts.append(Part(G(tube, 0.6), "skin", z=0.5 if nearer else -2, **({} if nearer else far)))
        parts.append(Part(G(Ellipse(foot[0], foot[1], 2.6 * lr, 2.0 * lr), 0.3), "skin",
                          z=0.55 if nearer else -1.9, **({} if nearer else far)))
    # tail
    tk = p["tail"]
    sway = (3.0 if step else -2.0) if step is not None else 1.5
    tl = 14.0 * tk
    tail = Tube([(0, a * 0.85), (sway * 0.4, a + tl * 0.45), (sway, a + tl)], [3.0, 2.0, 0.9])
    parts.append(Part(G(tail, 0.6), "skin", z=0.6 if not toward else -2.5))
    if p["crest"] > 0 and tk > 0.6:
        for i in range(4):
            t = 0.2 + 0.2 * i
            cy = a + tl * t
            cx = sway * t
            parts.append(Part(G(Ellipse(cx, cy, 0.9, 1.0), 1.6), "skin", z=0.65 if not toward else -2.4,
                              normal=(-0.3, -0.5, 0.8)))
    # neck and head
    hl = (5.2 if not tort else 4.0) * hk
    hw = (4.6 if not tort else 3.4) * hk
    nl = 6.0 * p["neck"]
    hv = a + nl * 0.6 + hl * 0.55
    if phase:
        hv += 2.0
    hz = 2.5 if toward else -1.5
    neck = Tube([(0, -(a * 0.75)), (0, -(a + nl * 0.4))], [3.4 * hk ** 0.5, 3.0 * hk ** 0.6])
    parts.append(Part(G(neck, 1.5), "skin", z=hz - 0.1, **({} if toward else far)))
    head = Union([Ellipse(0, -hv, hw, hl), Ellipse(0, -(hv + hl * 0.75), hw * 0.62, hl * 0.6)], k=0.1)
    parts.append(Part(G(head, 2.0), "skin", z=hz, **({} if toward else dict(light=-0.1))))
    # shell: the marginal rim (seen on the near side) under the domed carapace
    rim = Ellipse(0, 0, b + 0.3, a + 0.3)
    parts.append(Part(G(rim, 0.6), "shell", z=1, light=-0.32, inner=("shell", 0)))
    for k in range(p["serr"]):  # rear serrations from above
        for su in (-1, 1):
            ang = math.radians(20 + k * 15) * su
            ex, ey = math.sin(ang), math.cos(ang)
            cx, cy = ex * b, ey * a
            tx, ty = ey * a / math.hypot(ey * a, ex * b), -ex * b / math.hypot(ey * a, ex * b)
            L = p["serr_len"] * 0.9
            poly = Poly([(cx - tx * 1.4, cy - ty * 1.4), (cx + ex * L + tx * 0.6 * su, cy + ey * L - ty * 0.6 * su),
                         (cx + tx * 1.4, cy + ty * 1.4)])
            parts.append(Part(G(poly, 0.8), "shell", z=0.95, normal=(0, 0.2, 0.98), light=-0.1, inner=("shell", 0)))
    shell = Ellipse(0, 0, b, a)
    parts.append(Part(G(shell, hs), "shell", z=1.2, flat=0.6 if not tort else 0.45, light=0.1))

    def details(cv):
        big = cv.big
        dark = ("shell", 0)

        def P(u, v):
            return S(u, v)

        def ring(f, n=48):
            return [P(b * f * math.sin(2 * math.pi * i / n), a * f * math.cos(2 * math.pi * i / n)) for i in range(n + 1)]
        mf = 0.80
        if big or ow:
            cv.polyline(ring(mf), dark)
        wv = b * 0.30
        vs = [a * (0.80 - 0.32 * k) for k in range(6)]
        if big or ow:
            # vertebral row (hexagons) down the midline
            for k in range(5):
                v0, v1 = vs[k], vs[k + 1]
                vm = (v0 + v1) / 2
                w0 = wv * (0.75 if k == 0 else 1.0)
                pts = [(-w0 * 0.8, v0), (-w0, vm), (-w0 * 0.8, v1), (w0 * 0.8, v1), (w0, vm), (w0 * 0.8, v0)]
                cv.polyline([P(*q) for q in pts + pts[:1]], dark)
            # costal seams, radiating to the marginal ring
            for k in (1, 2, 3):
                for su in (-1, 1):
                    v = vs[k]
                    ang = math.atan2(su * 1.0, (v / a) * 1.15)
                    cv.line(P(su * wv * 0.8, v), P(b * mf * math.sin(ang), a * mf * math.cos(ang)), dark)
        if big:
            for i in range(18):  # marginal seams
                ang = 2 * math.pi * (i + 0.5) / 18
                cv.line(P(b * mf * math.sin(ang), a * mf * math.cos(ang)),
                        P(b * 0.98 * math.sin(ang), a * 0.98 * math.cos(ang)), dark)
            if p["keel"] > 0.3:  # keel knobs: a lit pixel over a dark one, on vertebrals and costals
                for k in range(5):
                    vm = (vs[k] + vs[k + 1]) / 2 - 1.0
                    for u in ([0.0] + ([-b * 0.55, b * 0.55] if p["keel"] > 0.6 else [])):
                        x, y = cv.pt(*P(u, vm))
                        cv.shade(x, y, +2)
                        cv.shade(x, y + 1, -1)
                        if p["keel"] > 2.0:
                            cv.shade(x, y - 1, +1)
            if p["rings"]:
                for k in range(5):
                    vm = (vs[k] + vs[k + 1]) / 2
                    x, y = cv.pt(*P(0, vm))
                    _shade_disc(cv, cv.to_model(x + 0.5, y + 0.5), 1.2, +1)
            if p["algae"]:
                cv.texture("shell", lambda px, py: (px * 7 + py * 13) % 23 == 0, +1, 1, 3)
            if p["tubercles"]:
                cv.texture("skin", lambda px, py: py % 2 == 0 and (px + py // 2 * 3) % 4 == 0, -1, 1, 3)
        # eyes on the head (visible from above in both directions; bigger when facing us)
        hsx = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 2.0)
        ey = -(hv + hl * 0.35)
        for su in (-1, 1):
            e = hsx.to_screen(su * hw * 0.62, -ey)
            if toward or big:
                if cv.big:
                    cv.disc(e, 1.3 * hk, "outline")
                    cv.disc(e, 0.7 * hk, "eye")
                else:
                    cv.set(*cv.pt(*e), "outline")
        if toward:
            m0, m1 = hsx.to_screen(-hw * 0.45, hv + hl * 1.05), hsx.to_screen(hw * 0.45, hv + hl * 1.05)
            if cv.big:
                cv.line(m0, m1, "outline")
            tip = hsx.to_screen(0, hv + hl * 1.25)
            cv.set(*cv.pt(*tip), ("beak", 1))
    return Model(parts, p["ramps"], details)


def back(p, phase=0):
    return topdown(p, yaw=28, fs=0.72, phase=phase)


def overworld(p, view, step):
    return topdown(p, yaw=180 if view == "south" else 0, fs=0.72, step=step, ow=True)


PLAN = BodyPlan(
    "turtle", "turtles and tortoises: snappers, the tortoise Stylemys",
    side=side, back=back, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_TURTLE,
    tracks="TRACKS_FOOT",
)
