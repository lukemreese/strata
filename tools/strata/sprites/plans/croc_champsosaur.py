"""croc_champsosaur body plan: low-slung aquatic reptiles in side view, plus a
top-down view for the back sprite and the overworld end-on frames.

Species (taxonomy.py):
    champsosaur   Champsosaurus (Hell Creek Fm, MT, 20 kg)  choristodere: gharial-like snout
    borealosuch   Borealosuchus (Hell Creek Fm, MT, 150 kg) generalised crocodylian

Both are built from the same knobs, so a spec is mostly numbers:
    snout, snout_h, snout_w   snout length ahead of the eyes, half-height, half-width (top view)
    skull, skull_h, skull_w   skull length behind the eyes, height at the back, half-width
    body, body_h, body_w      torso length, half-height (side), half-width (top)
    stance                    gap between belly and ground (high walk vs. belly sprawl)
    legs                      limb thickness factor
    tail, tail_r, tail_arc    tail length, base radius, upward arc (side view)
    crest                     height of the tail's saw crest (crocodylian caudal scutes; 0 = none)
    scutes                    osteoderm rows on the back (True for crocodylians)
    bands                     list of (x0, x1) model-x intervals with darker crossbands
    teeth                     "croc" (big interlocking teeth) | "fine" (many small ones)
    gape                      frame 2 jaw angle; tail_flick: frame 2 tail lift
Ramps: outline 1, hide 4 (dorsal), band 2 (crossbands, scute shadows), belly 3,
eye 1, teeth 1, mouth 2.

Model units: torso centred on x = 0 (head left), mid-torso at y = 0, ground at
y = body_h * 0.9 + stance.

Plan-local primitives (worth promoting to core): `Rotated(shape, pivot, deg)`
turns any shape about a pivot (the jaw drop), and the `Ground` projection from
plans/turtle.py for the top-down views.
"""

import math

from ..core.geom import Ellipse, Tube, Loft, Poly, Part, Model, turn, lerp, clamp
from ..core.plan import BodyPlan
from .turtle import Ground

FOOTPRINT_CROC = [
    "................",
    "................",
    "..#.#.......#.#.",
    "...###.....###..",
    "....#.......#...",
    "................",
    "................",
    "................",
    "................",
    "...#.#.....#.#..",
    "..#####...#####.",
    "...###.....###..",
    "....#.......#...",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(
    snout=15.0, snout_h=1.6, snout_w=2.8, skull=9.0, skull_h=4.4, skull_w=5.0,
    body=26.0, body_h=6.0, body_w=7.0, stance=5.0, legs=1.0,
    tail=40.0, tail_r=5.2, tail_arc=3.0, crest=1.4, scutes=True, bands=(),
    teeth="croc", gape=26, tail_flick=3.0, head_up=3.0, tail_wrap=True, tail_bands=(),
    far_light=-0.25, walk_swing=16,
    ow=dict(tracks="TRACKS_SLITHER", end_zoom=1.25),
)


class Rotated:
    """`shape` turned by `deg` about `pivot` (positive = clockwise on screen,
    as core.geom.turn)."""
    def __init__(self, shape, pivot, deg):
        self.s, self.pv, self.d = shape, pivot, deg
        x0, y0, x1, y1 = shape.bbox
        pts = [turn((x, y), pivot, deg) for x in (x0, x1) for y in (y0, y1)]
        self.bbox = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))

    def q(self, x, y):
        return self.s.q(*turn((x, y), self.pv, -self.d))


def _layout(p):
    """Key x/y positions shared by the views."""
    B, bh = p["body"], p["body_h"]
    ground = bh * 0.9 + p["stance"]
    head_back = -B / 2 - 1.0
    x_eye = head_back - p["skull"]
    tip = x_eye - p["snout"]
    y_m = -bh * 0.15 + p["stance"] * 0.12     # mouth line
    return dict(B=B, bh=bh, ground=ground, head_back=head_back, x_eye=x_eye, tip=tip, y_m=y_m)


# ---------------------------------------------------------------- side view

def _tail_pts(p, L, phase, step=None):
    """The tail runs back from the hips, drops to the ground and, with
    `tail_wrap`, curls forward along the ground on the near side of the body
    (towards the viewer, so lower on screen): this keeps a long reptile wide
    enough to read at 64 px. Returns (points, radii, index where the near
    part starts)."""
    B, bh, G = L["B"], L["bh"], L["ground"]
    x0, y0 = B / 2 - 2.0, -bh * 0.15
    T = p["tail"]
    flick = p["tail_flick"] if phase else 0.0
    if not p["tail_wrap"]:
        arc = p["tail_arc"] + flick
        pts, radii = [], []
        for i in range(8):
            s = i / 7
            pts.append((x0 + T * s, lerp(y0, G - 1.2, s ** 1.5) - arc * math.sin(math.pi * s) * (1 - 0.3 * s)))
            radii.append(lerp(p["tail_r"], 0.8, s ** 0.85))
        return pts, radii, len(pts)
    # path lengths along a hand-shaped curve, scaled to the tail length
    R = T * 0.17                                       # radius of the turn
    ctrl = [(x0, y0), (x0 + T * 0.18, y0 + bh * 0.25 - p["tail_arc"] * 0.3),
            (x0 + T * 0.30, G - R * 0.9), (x0 + T * 0.33 + R * 0.25, G + R * 0.25),
            (x0 + T * 0.22, G + R * 0.75), (x0 + T * 0.02, G + R * 0.82),
            (x0 - T * 0.18, G + R * 0.7 - flick * 0.4), (x0 - T * 0.36, G + R * 0.35 - flick)]
    radii = [lerp(p["tail_r"], 0.8, (i / (len(ctrl) - 1)) ** 0.8) for i in range(len(ctrl))]
    return ctrl, radii, 3


def _legs(p, L, phase, step):
    B, bh, G = L["B"], L["bh"], L["ground"]
    lk = p["legs"]
    sx, hx = -B / 2 + 4.5, B / 2 - 3.5
    defs = [  # (near, fore, swing, pts, radii, foot)
        (False, True, -1, [(sx + 2.5, bh * 0.1), (sx + 0.8, lerp(bh * 0.1, G, 0.55) - 0.6), (sx - 0.4, G - 1.6)],
         [3.0, 2.3, 1.8], (sx - 2.2, G - 1.0, 2.4, 0.9)),
        (False, False, 1, [(hx + 2.5, bh * 0.05), (hx + 5.5, lerp(bh * 0.1, G, 0.5) - 0.6), (hx + 3.0, G - 1.6)],
         [3.8, 2.7, 2.0], (hx + 1.4, G - 1.0, 3.2, 0.9)),
        (True, False, -1, [(hx, bh * 0.25), (hx + 3.2, lerp(bh * 0.25, G, 0.5)), (hx + 0.6, G - 1.2)],
         [4.2, 3.0, 2.2], (hx - 1.4, G - 0.5, 3.6, 1.0)),
        (True, True, 1, [(sx, bh * 0.3), (sx - 2.0, lerp(bh * 0.3, G, 0.55)), (sx - 3.4, G - 1.2)],
         [3.4, 2.6, 2.0], (sx - 5.2, G - 0.5, 2.8, 1.0)),
    ]
    for near, fore, swing, pts, radii, foot in defs:
        if step:
            hip, deg = pts[0], p["walk_swing"] * swing
            pts = [pts[0]] + [turn(q, hip, deg) for q in pts[1:]]
            fc = turn(foot[:2], hip, deg)
            lift = 1.0 if swing > 0 else 0.0
            pts[-1] = (pts[-1][0], pts[-1][1] - lift)
            foot = (fc[0], fc[1] - lift, *foot[2:])
        yield near, fore, Tube(pts, [r * lk for r in radii]), foot


def side(p, phase=0, step=None):
    if step is not None:
        phase = 0
    L = _layout(p)
    B, bh, G = L["B"], L["bh"], L["ground"]
    hb, xe, tip, ym = L["head_back"], L["x_eye"], L["tip"], L["y_m"]
    far = dict(light=p["far_light"])
    sh, kh = p["snout_h"], p["skull_h"]

    # the whole head pivots up a little about the neck
    pivot = (hb + 2.0, ym)
    up = p["head_up"] + (2.0 if phase else 0.0)
    Hd = lambda s: Rotated(s, pivot, up)  # noqa: E731
    Hp = lambda x, y: turn((x, y), pivot, up)  # noqa: E731

    te = (xe - tip) / (hb + 3.0 - tip)
    upper = Loft(tip, hb + 3.0,
                 up=[(0, sh * 1.0), (0.12, sh * 1.05), (te * 0.7, sh * 1.25), (te, sh * 1.6 + 0.6),
                     (min(0.97, te + 0.12), kh * 0.85), (1, kh)],
                 dn=[(0, 0.5), (1, 0.6)], mid=lambda t: ym)
    lower = Loft(tip + 0.5, hb + 2.0,
                 up=[(0, 0.4), (1, 0.6)],
                 dn=[(0, sh * 0.75), (te, sh * 1.0 + 0.3), (1, kh * 0.75)], mid=lambda t: ym)
    hinge = (hb + 1.5, ym)
    gape = -p["gape"] if phase else 0.0
    jaw = Rotated(lower, hinge, gape)
    eye_top = upper.top(xe)
    bump = Ellipse(xe + 0.3, eye_top + 0.2, 2.3, 1.5)
    nost = Ellipse(tip + 1.6, ym - sh * 0.75, 1.4, 0.9 + sh * 0.25)

    torso = Loft(-B / 2 - 1.5, B / 2 + 3.0,
                 up=[(0, bh * 0.62), (0.3, bh * 0.98), (0.7, bh * 0.95), (1, bh * 0.7)],
                 dn=[(0, bh * 0.55), (0.4, bh * 0.92), (0.8, bh * 0.88), (1, bh * 0.55)])
    neck = Tube([(hb + 1.0, ym - kh * 0.35), (-B / 2 + 2.0, -bh * 0.2)], [kh * 0.95, bh * 0.85])
    tp, tr, kn = _tail_pts(p, L, phase)
    tail_far = Tube(tp[:kn + 1], tr[:kn + 1])
    tail_near = Tube(tp[kn:], tr[kn:]) if kn < len(tp) - 1 else None

    def along(s):
        """Point, tangent and radius at path fraction s of the tail."""
        seg = clamp(s, 0, 0.999) * (len(tp) - 1)
        j = int(seg)
        u = seg - j
        (ax, ay), (bx, by) = tp[j], tp[j + 1]
        ln = math.hypot(bx - ax, by - ay)
        return (lerp(ax, bx, u), lerp(ay, by, u)), ((bx - ax) / ln, (by - ay) / ln), lerp(tr[j], tr[j + 1], u)

    band_at = [along(s) for s in p["tail_bands"]]

    def bands(x, y):
        if any(a <= x <= b for a, b in p["bands"]):
            return True
        for (cx, cy), (tx, ty), r in band_at:
            if abs((x - cx) * tx + (y - cy) * ty) < 1.3 and math.hypot(x - cx, y - cy) < r + 1.5:
                return True
        return False

    def body_region(belly_y):
        def region(x, y):
            if y > belly_y(x):
                return "belly"
            return "band" if bands(x, y) else "hide"
        return region

    def tail_region(x, y):
        return "band" if bands(x, y) else "hide"

    legs = list(_legs(p, L, phase, step))
    parts = []
    for near, fore, tube, foot in legs:
        if not near:
            parts += [Part(tube, "hide", z=-3, **far), Part(Ellipse(*foot), "hide", z=-2.9, **far)]
    parts.append(Part(tail_far, "hide", z=-1, flat=0.5, region=tail_region))
    if tail_near:
        parts.append(Part(tail_near, "hide", z=1.6, flat=0.5, region=tail_region, inner=("hide", 0)))
    if p["crest"] > 0:  # caudal scute crest: a saw edge along the tail's top
        n = 13
        for i in range(n):
            s = 0.03 + 0.85 * i / n
            (cx, cy), (tx, ty), r = along(s)
            h = p["crest"] * (1.0 - 0.55 * s)
            w = 0.85
            top = cy - r + 0.6
            near_part = tail_near is not None and s * (len(tp) - 1) >= kn
            poly = Poly([(cx - w, top), (cx - 0.2, top - h), (cx + w, top)])
            parts.append(Part(poly, "hide", z=1.55 if near_part else -1.1, normal=(-0.3, -0.6, 0.75),
                              region=tail_region))
    parts.append(Part(torso, "hide", z=0, flat=0.5, region=body_region(lambda x: bh * 0.38)))
    parts.append(Part(neck, "hide", z=0.2, region=body_region(lambda x: ym + kh * 0.2)))
    for near, fore, tube, foot in legs:
        if near:
            parts += [Part(tube, "hide", z=1 if not fore else 1.2, inner=("hide", 0)),
                      Part(Ellipse(*foot), "hide", z=1.1 if not fore else 1.3, inner=("hide", 0))]
    up_tip = Hp(tip + 0.3, ym)
    lo_tip = Hp(*turn((tip + 0.8, ym + 0.2), hinge, gape))
    if phase:
        parts.append(Part(Poly([Hp(*hinge), up_tip, lo_tip]), "mouth", z=1.9, normal=(0.1, 0.3, 0.95)))
    parts += [Part(Hd(jaw), "belly", z=2.0, inner=("hide", 0)),
              Part(Hd(upper), "hide", z=2.2, flat=0.5),
              Part(Hd(bump), "hide", z=2.3, line=False),
              Part(Hd(nost), "hide", z=2.25, line=False)]

    def details(cv):
        big = cv.big
        if big and p["scutes"]:  # osteoderm rows: a lit pixel over a shadow, along the back and tail
            for row, dy in enumerate((1.3, 3.4)):
                x = -B / 2 + 1.0 + row * 1.2
                while x < B / 2 + 2.0:
                    y = torso.top(x) + dy
                    px, py = cv.pt(x, y)
                    cv.shade(px, py, +1)
                    cv.shade(px, py + 1, -1)
                    x += 2.6
        if big:  # teeth along the jaw line
            if p["teeth"] == "croc":
                xs = [tip + 1.8 + k * 2.2 for k in range(int((xe - tip + 2.0) / 2.2))]
                for k, x in enumerate(xs):
                    if phase:
                        cv.set(*cv.pt(*Hp(x, ym + 0.9)), "teeth")
                        q = turn((x + 0.6, ym - 0.2), hinge, gape)
                        cv.set(*cv.pt(*Hp(*q)), "teeth")
                    else:
                        cv.set(*cv.pt(*Hp(x, ym + (0.9 if k % 2 else -0.4))), "teeth")
            else:
                xs = [tip + 1.4 + k * 1.6 for k in range(int((xe - tip) / 1.6))]
                for k, x in enumerate(xs):
                    if phase:
                        cv.set(*cv.pt(*Hp(x, ym + 0.8)), "teeth")
                    elif k % 2 == 0:
                        cv.set(*cv.pt(*Hp(x, ym + 0.8)), "teeth")
            # mouth line (closed): darker along the lip
            if not phase:
                cv.line(Hp(tip + 0.6, ym + 0.2), Hp(hb + 0.5, ym + 0.4), "outline")
        # nostril and eye
        cv.set(*cv.pt(*Hp(tip + 1.0, ym - sh * 1.2)), "outline")
        e = Hp(xe - 0.2, eye_top + 0.5)
        if big:
            px, py = cv.pt(*e)
            f = 1 if cv.flip else -1
            for dx, dy, c in ((0, 0, "eye"), (f, 0, "eye"), (0, 1, "outline"), (f, 1, "outline"),
                              (-f, 0, "outline"), (2 * f, 0, "outline"), (0, -1, "outline"), (f, -1, "outline")):
                cv.set(px + dx, py + dy, c)
            cv.set(px + f, py, "outline")    # vertical slit pupil
        else:
            cv.set(*cv.pt(*e), "outline")
        if big:  # claws: pale points at the front of the near feet
            for near, fore, tube, foot in legs:
                if near:
                    fx, fy, frx, fry = foot
                    for k in range(3):
                        cv.set(*cv.pt(fx - frx + 0.5 + k * 1.1, fy + fry * 0.6), ("belly", 0))

    return Model(parts, p["ramps"], details)


# ---------------------------------------------------------------- top-down views

def topdown(p, yaw, fs, phase=0, step=None):
    """From above; plan shapes use (u, -v) with v forward (head)."""
    L = _layout(p)
    B, bw = L["B"], p["body_w"]
    G = lambda s, h=0.0: Ground(s, yaw, fs, h)  # noqa: E731
    toward = math.cos(math.radians(yaw)) < 0
    far = dict(light=p["far_light"])
    v_hb = B / 2 + 1.0                         # back of the skull
    v_eye = v_hb + p["skull"]
    v_tip = v_eye + p["snout"]
    sw, kw = p["snout_w"], p["skull_w"]
    lk = p["legs"]
    parts = []
    # legs, sprawled; diagonal pairs swap on the walk step
    sweep = (2.5 if step else -1.0) if step is not None else 0.0
    for su in (-1, 1):
        f = sweep * su
        fore = Tube([(su * bw * 0.75, -(B / 2 - 4)), (su * (bw + 3.5), -(B / 2 - 3 + f)),
                     (su * (bw + 4.5), -(B / 2 + 0.5 + f))], [3.0 * lk, 2.4 * lk, 2.0 * lk])
        hind = Tube([(su * bw * 0.75, B / 2 - 4), (su * (bw + 4.0), B / 2 - 3 - f),
                     (su * (bw + 5.0), B / 2 - 6.5 - f)], [3.6 * lk, 2.8 * lk, 2.2 * lk])
        for kind, tube, foot in (("fore", fore, (su * (bw + 4.8), -(B / 2 + 1.6 + f))),
                                 ("hind", hind, (su * (bw + 5.4), B / 2 - 7.8 - f))):
            nearer = (kind == "fore") == toward
            parts.append(Part(G(tube, 0.5), "hide", z=-1 if not nearer else 0.5, **({} if nearer else far)))
            parts.append(Part(G(Ellipse(foot[0], foot[1], 2.4 * lk, 2.0 * lk), 0.2), "hide",
                              z=-0.9 if not nearer else 0.55, **({} if nearer else far)))
    # tail: an S-curve sideways so the animal fits the frame
    sway = (1.0 if step else -1.0) if step is not None else 0.6
    tl = p["tail"] * 0.82
    tpts, trad = [], []
    for i in range(8):
        s = i / 7
        tpts.append((sway * 4.5 * math.sin(math.pi * s * 1.4) * s, B / 2 - 2 + tl * s))
        trad.append(lerp(p["tail_r"] * 0.95, 0.8, s ** 0.85))
    parts.append(Part(G(Tube(tpts, trad), 1.0), "hide", z=0.6 if not toward else -1.5,
                      region=lambda x, y: "hide"))
    body = Ellipse(0, 0, bw, B / 2 + 1.5)
    parts.append(Part(G(body, 2.0), "hide", z=0, flat=0.55))
    # head: skull and snout, one shade dome each
    skull = Ellipse(0, -(v_hb + p["skull"] * 0.55), kw, p["skull"] * 0.75 + 1.0)
    snout = Tube([(0, -(v_eye - 1.0)), (0, -(v_tip - sw * 0.6))], [sw * 1.15, sw * 0.75])
    hz = 1.5 if toward else -0.5
    parts.append(Part(G(snout, 1.6), "hide", z=hz + 0.1, **({} if toward else dict(light=-0.1))))
    parts.append(Part(G(skull, 1.8), "hide", z=hz, **({} if toward else dict(light=-0.1))))
    for su in (-1, 1):
        parts.append(Part(G(Ellipse(su * kw * 0.5, -(v_eye + 0.2), 1.5, 1.3), 2.6), "hide", z=hz + 0.2, line=False))

    def details(cv):
        big = cv.big
        if p["scutes"]:  # osteoderm rows down the back (and the doubled tail crest)
            hs = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 2.0)
            for u in (-0.55, -0.2, 0.2, 0.55):
                v = B / 2 - 1.0
                while v > -B / 2 - 3:
                    x, y = cv.pt(*hs.to_screen(u * bw, v))
                    cv.shade(x, y, +1)
                    if big:
                        cv.shade(x, y + 1, -1)
                    v -= 2.8 if big else 3.6
        if not p["scutes"] and big:  # fine scales: a sparse darker lattice
            cv.texture("hide", lambda px, py: (px + 2 * py) % 5 == 0 and py % 2 == 0, -1, 1, 3)
        es = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 2.8)
        for su in (-1, 1):
            e = es.to_screen(su * kw * 0.5, v_eye + 0.2)
            if big:
                px, py = cv.pt(*e)
                cv.set(px, py, "eye")
                cv.set(px, py + 1, "outline")
            else:
                cv.set(*cv.pt(*e), "outline")
        if toward:
            ns = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 1.8)
            cv.set(*cv.pt(*ns.to_screen(0, v_tip - sw * 0.5)), "outline")

    return Model(parts, p["ramps"], details)


def back(p, phase=0):
    return topdown(p, yaw=24, fs=0.62, phase=phase)


def overworld(p, view, step):
    return topdown(p, yaw=180 if view == "south" else 0, fs=0.72, step=step)


PLAN = BodyPlan(
    "croc_champsosaur", "low-slung aquatic reptiles: crocodylians, choristoderes",
    side=side, back=back, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_CROC,
    tracks="TRACKS_SLITHER",
)
