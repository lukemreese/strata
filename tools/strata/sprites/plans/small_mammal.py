"""Small-mammal body plan: generalised small quadrupeds in side view
(multituberculates, cimolestids, condylarths, early marsupials), plus the
small-mammal engine that plans/rodent_lagomorph.py and plans/primate.py reuse.

Two templates live here; `side`/`overworld` dispatch on the spec:

1. The CLASSIC template (Mesodma, Taeniolabis): hand-placed ellipses, used
   when the spec has a `torso` list. Documented directly below.
2. The ENGINE (`quad_side`, everything else in this lane): the proportion-driven
   quadruped of plans/canid.py (same spec keys: body, leg, neck, head, ear, tail,
   eye, marks, action, teeth, whiskers, ow_end ...; see that docstring), forked
   here with the extras small mammals need. Documented at `ENGINE_DEFAULTS`.

CLASSIC template.
Ramps the template uses:
    outline   1 colour
    fur       main coat, 3-4 shades
    belly     underside, 2-3 shades (also the whisker colour)
    skin      nose, ears, paws, naked tail, 2-3 shades
    white     1 colour: incisors, eye highlight

Geometry (model units, head to the left, ground at y ~ 19):
    torso / head   lists of ellipses (cx, cy, rx, ry, angle), smooth-unioned
    ear, thigh     one ellipse each (thigh may be None)
    legs           list of dict(pts, radii, foot=(cx, cy, rx, ry), z, foot_z,
                   near=True|False, lift=<px raised in frame 2>, swing=+1|-1
                   (walk-cycle direction: +1 swings forward in step 1),
                   toes=(xs, y) or None). Far legs are listed first.
    tail           list of (x, y, curl_dx, curl_dy) + tail_radii; frame 2 adds
                   `curl` x (curl_dx, curl_dy)
    sniff          head rotation in frame 2 (degrees) about `neck`
    belly_line     (a, b): torso belly below y = a + b*x
    jaw            (x, y, slope): head belly (throat) below this line
Painted details: inner_ear, fur_dashes, nose, nostril, mouth, incisors, eye,
whiskers (see the mesodma spec). Each may be None.
"""

import math

from ..core.geom import Ellipse, Tube, Union, Part, Model, turn, rot, lerp, clamp
from ..core.plan import BodyPlan
# read-only reuse of the carnivore artist's quadruped engine (see ENGINE below)
from .canid import (Facet, Path, paint, _mark, _countershade, rig, head_shapes,
                    DEFAULTS as CANID_DEFAULTS, overworld as canid_overworld)

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

CLASSIC_DEFAULTS = dict(
    sniff=7, neck=(-10.0, 2.0), curl=2.0, head_k=0.10, torso_k=0.10,
    far_light=-0.25, walk_swing=16,
    thigh=None, inner_ear=None, fur_dashes=(3, 5), nostril=None, incisors=None, whiskers=None,
    ow=dict(tracks="TRACKS_FOOT"),
)


def _legs(p, phase, step):
    """Yields (leg dict, Tube, foot Ellipse, toe points) with the frame's pose."""
    for leg in p["legs"]:
        lift = leg.get("lift", 0.0) if phase else 0.0
        pts = list(leg["pts"])
        foot = leg["foot"]
        toes = leg.get("toes")
        toe_pts = [(x, toes[1] - lift) for x in toes[0]] if toes else []
        if lift:
            pts[-1] = (pts[-1][0], pts[-1][1] - lift)
            foot = (foot[0], foot[1] - lift, *foot[2:])
        if step:
            hip, deg = pts[0], p["walk_swing"] * leg.get("swing", 1)
            pts = [pts[0]] + [turn(q, hip, deg) for q in pts[1:]]
            fc = turn(foot[:2], hip, deg)
            foot = (fc[0], fc[1], *foot[2:])
            toe_pts = [turn(q, hip, deg) for q in toe_pts]
        yield leg, Tube(pts, leg["radii"]), Ellipse(*foot), toe_pts


def classic_side(p, phase=0, step=None):
    if step is not None:
        phase = 0
    sniff = p["sniff"] if phase else 0
    neck = p["neck"]
    H = lambda x, y: turn((x, y), neck, sniff)  # noqa: E731

    torso = Union([Ellipse(*e) for e in p["torso"]], k=p["torso_k"])
    head = Union([Ellipse(*H(cx, cy), rx, ry, a + sniff) for cx, cy, rx, ry, a in p["head"]], k=p["head_k"])
    ex, ey, erx, ery, ea = p["ear"]
    ear = Ellipse(*H(ex, ey), erx, ery, ea + sniff)
    curl = p["curl"] if phase else 0.0
    tail = Tube([(x + curl * cx, y + curl * cy) for x, y, cx, cy in p["tail"]], p["tail_radii"])

    def underside(base):
        def region(x, y):
            return "belly" if y > base(x) else "fur"
        return region

    ba, bb = p["belly_line"]
    torso_region = underside(lambda x: ba + bb * x)
    jx, jy, js = p["jaw"]
    jaw = H(jx, jy)
    jaw_slope = js + math.tan(math.radians(sniff))
    head_region = underside(lambda x: jaw[1] + (x - jaw[0]) * jaw_slope)

    far = dict(light=p["far_light"])
    legs = list(_legs(p, phase, step))
    parts = [Part(tail, "skin", z=-3, flat=0.5)]
    for leg, tube, foot, _ in legs:
        if not leg["near"]:
            parts += [Part(tube, "fur", z=leg["z"], **far), Part(foot, "skin", z=leg["foot_z"], **far)]
    parts.append(Part(torso, "fur", z=0, flat=0.5, region=torso_region))
    if p["thigh"]:
        parts.append(Part(Ellipse(*p["thigh"]), "fur", z=1, flat=0.5, inner=("fur", 0)))
    for leg, tube, foot, _ in legs:
        if leg["near"]:
            parts += [Part(tube, "fur", z=leg["z"], inner=("fur", 0)),
                      Part(foot, "skin", z=leg["foot_z"], inner=("skin", 0))]
    parts += [Part(ear, "fur", z=2.5), Part(head, "fur", z=3, flat=0.5, region=head_region)]

    def details(cv):
        big = cv.big
        if p["inner_ear"]:
            c, r_big, r_small = p["inner_ear"]
            cv.disc(H(*c), r_big if big else r_small, ("skin", 1), only_opaque=True)
        if big and p["fur_dashes"]:  # short darker dashes on the coat
            rows, diag = p["fur_dashes"]
            for py in range(cv.h):
                for px in range(cv.w):
                    v = cv.idx[py][px]
                    if v in cv.pal.index["fur"][1:] and py % rows == 0 and (px + py) % diag == 0:
                        cv.shade(px, py, -1)
        if big:  # toes: tiny darker gaps on the near feet
            for leg, _, _, toe_pts in legs:
                for q in toe_pts:
                    cv.shade(*cv.pt(*q), -1)
        c, r_big, r_small = p["nose"]
        cv.disc(H(*c), r_big if big else r_small, ("skin", 1))
        if big:
            if p["nostril"]:
                cv.set(*cv.pt(*H(*p["nostril"])), ("skin", 2))
            if p["mouth"]:
                cv.line(H(*p["mouth"][0]), H(*p["mouth"][1]), "outline")
            if p["incisors"]:
                for k, q in enumerate(p["incisors"]):
                    cv.set(*cv.pt(*H(*q)), "white", only_opaque=(k == 0))
        c, r_big, r_small = p["eye"]
        e = H(*c)
        if big:  # a beady black eye with a highlight
            cv.disc(e, r_big, "outline")
            px, py = cv.pt(*e)
            cv.set(px + (1 if cv.flip else -1), py - 1, "white")
        else:
            cv.disc(e, r_small, "outline")

    def post(cv):
        if not cv.big or not p["whiskers"]:
            return
        for a, b in p["whiskers"]:  # drawn over the outline, in the pale belly colour
            for px, py in cv.pixels_on_line(H(*a), H(*b)):
                if cv.inside(px, py) and not cv.idx[py][px]:
                    cv.idx[py][px] = cv.pal.get(("belly", 0))

    return Model(parts, p["ramps"], details, post)


def _dims(p):
    """End-on measurements derived from the side-view parameters."""
    tops = [cy - ry for cx, cy, rx, ry, a in p["torso"]]
    bots = [cy + ry for cx, cy, rx, ry, a in p["torso"]]
    t_top, t_bot = min(tops), max(bots)
    ground = max(leg["foot"][1] + leg["foot"][3] for leg in p["legs"])
    hx, hy, hrx, hry, _ = p["head"][0]
    return dict(t_cy=(t_top + t_bot) / 2, t_ry=(t_bot - t_top) / 2, ground=ground,
                h_cy=hy, h_r=hry, ear=p["ear"], eye=p["eye"], legs=p["legs"])


def classic_overworld(p, view, step):
    """South: face, ears, chest and forepaws in front of the body. North: the
    back, ears behind, hind feet and the tail. Shapes are derived from the side
    parameters, so a new spec gets usable end-on views automatically; override
    with an `ow_end` dict (t_rx, h_rx scale factors) if needed."""
    d = _dims(p)
    o = dict(head_w=1.12, body_w=0.7, **p.get("ow_end", {}))
    T, ground = d["t_ry"], d["ground"]
    h_r = d["h_r"]
    h_rx, h_ry = h_r * o["head_w"], h_r * 0.95
    h_cy = d["t_cy"] - 1.6
    c_cy, c_rx, c_ry = d["t_cy"] + T * 0.65, T * o["body_w"], T * 0.65   # chest / rump
    _, _, erx, ery, _ = d["ear"]
    erx, ery = erx * 1.1, ery * 1.1
    fore = next((leg for leg in d["legs"] if leg["near"] and leg.get("fore")), d["legs"][-1])
    leg_r = fore["radii"]
    paw_rx, paw_ry = fore["foot"][3] * 1.35, fore["foot"][3] * 1.15
    far = dict(light=p["far_light"])
    lift = [1.5, 0.0] if step else [0.0, 0.0]  # step 1 raises one paw
    haunch_r = T * 0.45
    parts = []
    for s in (-1, 1):  # haunches and hind feet stick out at the sides: a pear shape
        parts.append(Part(Ellipse(s * T * 0.7, ground - haunch_r - 0.6, haunch_r, haunch_r), "fur",
                          z=-1 if view == "south" else 0.5, **(far if view == "south" else {})))
        parts.append(Part(Ellipse(s * T * 0.8, ground - paw_ry - (lift[0 if s > 0 else 1] if view == "north" else 0),
                                  paw_rx * 1.2, paw_ry), "skin", z=-0.9 if view == "south" else 1,
                          **(far if view == "south" else dict(inner=("skin", 0)))))
    if view == "south":
        parts.append(Part(Ellipse(0, c_cy, c_rx, c_ry), "fur", z=0,
                          region=lambda x, y: "belly" if abs(x) < c_rx * 0.55 else "fur"))
        for k, s in enumerate((-1, 1)):
            x = s * T * 0.35
            foot_y = ground - paw_ry - lift[k]
            parts.append(Part(Tube([(x, c_cy - 1), (x, foot_y)], [leg_r[0], leg_r[-1]]), "fur", z=2, inner=("fur", 0)))
            parts.append(Part(Ellipse(x, foot_y, paw_rx, paw_ry), "skin", z=2.1, inner=("skin", 0)))
            parts.append(Part(Ellipse(s * h_rx * 0.75, h_cy - h_ry * 0.85, erx, ery, s * 30), "fur", z=2.5))
        parts.append(Part(Ellipse(0, h_cy, h_rx, h_ry), "fur", z=3))
        muzzle = (0, h_cy + h_ry * 0.45)
        parts.append(Part(Ellipse(*muzzle, h_r * 0.5, h_r * 0.38), "belly", z=3.2, inner=("fur", 0)))

        def details(cv):
            for s in (-1, 1):
                cv.disc((s * h_rx * 0.75, h_cy - h_ry * 0.8), erx * 0.5, ("skin", 1), only_opaque=True)
                cv.disc((s * h_rx * 0.42, h_cy - h_ry * 0.1), 0.75 / cv.scale, "outline")
            cv.disc((muzzle[0], muzzle[1] - h_r * 0.15), 0.6 / cv.scale, ("skin", 0))
            if p["incisors"]:
                cv.set(*cv.pt(0, muzzle[1] + h_r * 0.3), "white")
        return Model(parts, p["ramps"], details)

    # north: seen from behind; the head is farther away, above the back
    tail_r = p["tail_radii"]
    sway = 2.0 if step else -1.0
    parts.append(Part(Ellipse(0, c_cy - T * 0.25, c_rx * 1.1, c_ry * 1.3), "fur", z=0))
    parts.append(Part(Ellipse(0, h_cy - 1.0, h_rx * 0.9, h_ry * 0.85), "fur", z=-0.5, light=-0.1))
    for s in (-1, 1):
        parts.append(Part(Ellipse(s * h_rx * 0.7, h_cy - h_ry * 0.85, erx, ery, s * 30), "fur", z=-1, **far))
    tail = Tube([(0, c_cy + c_ry * 0.6), (1.0 + sway * 0.5, ground - 1.0), (6.0 + sway, ground - 0.5),
                 (11.0 + sway, ground - 3.0)], tail_r[:4])
    parts.append(Part(tail, "skin", z=2))
    return Model(parts, p["ramps"])


# ===========================================================================
# ENGINE: the proportion-driven small-mammal quadruped.
#
# A fork of the side view in plans/canid.py (whose helpers it imports
# read-only), with what small mammals need on top of the canid keys:
#   body.rear        degrees the front half is raised about a pivot near the
#                    bottom of the rump (sitting, sentinel posture); the head
#                    stays level except for body.head_follow x rear.
#   body.rear_pivot  (dx, frac): pivot x offset from the hip, y as a fraction
#                    of the hip depth below the hip top
#   leg.hpaw         (length, radius) of the hind paws (rabbits, squirrels);
#                    None = leg.paw
#   leg.arms         with rear: (elbow dx, dy, wrist dx, dy) from the shoulder:
#                    forearms held up in front of the chest instead of
#                    reaching the ground
#   leg.toes         paint toe gaps on the near paws
#   eye.big          iris ramp: a big eye drawn as outline ring, iris and pupil
#                    (primates, nocturnal species)
#   eye.ring         ramp of a 1-px pale ring around the eye
#   eye.far          (dx, dy, r): the far eye peeking past the snout (forward-
#                    facing eyes: the head reads as turned towards the viewer)
#   teeth.gnaw       dict(len, w, dx, rake, ramp): ever-growing upper incisors
#                    at the muzzle tip (rodents: orange enamel)
#   tail.bends       5 per-segment bends (deg) instead of the constant `bend`
#                    (S-curves, a squirrel's tail curled over the back)
#   branch           dict(x=(x0, x1), r, dy, tilt, z): a branch under the feet
#                    in the battle views (ramp "bark"); omitted in the overworld
#   extra            list of dict(on="head"|"body", e=(cx, cy, rx, ry, deg),
#                    ramp, z): extra ellipse parts (cheek pouches, a scut);
#                    head ones are relative to the cranium centre
#   ow_side          dict of spec overrides for the overworld walk frames
#                    (e.g. a primate's tail held level instead of hanging)
# ===========================================================================


def _merge(a, b):
    out = {k: dict(v) if isinstance(v, dict) else v for k, v in a.items()}
    for k, v in b.items():
        out[k] = {**out[k], **v} if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


ENGINE_DEFAULTS = _merge(CANID_DEFAULTS, dict(
    body=dict(rear=0.0, rear_pivot=(0.0, 0.75), head_follow=0.2),
    leg=dict(hpaw=None, arms=None, toes=True),
    eye=dict(big=None, ring=None, far=None),
    teeth=dict(canine=0.0, gnaw=None),
    action=dict(tilt=6.0, gape=0.0, tail=-10.0, ear=0.0),
    branch=None, extra=[], ow_side={},
))

# the classic template's keys stay available to classic specs; engine values win
DEFAULTS = {**CLASSIC_DEFAULTS, **ENGINE_DEFAULTS}


class Xf:
    """A shape under a rigid motion: rest point q -> to + rot(q - pivot, deg)."""
    def __init__(self, shape, pivot, deg, to=None):
        self.s, self.pv, self.deg = shape, pivot, deg
        self.to = to if to is not None else pivot
        x0, y0, x1, y1 = shape.bbox
        cs = [self.fwd(c) for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
        self.bbox = (min(c[0] for c in cs), min(c[1] for c in cs), max(c[0] for c in cs), max(c[1] for c in cs))

    def fwd(self, q):
        x, y = rot(q[0] - self.pv[0], q[1] - self.pv[1], self.deg)
        return (self.to[0] + x, self.to[1] + y)

    def inv(self, q):
        x, y = rot(q[0] - self.to[0], q[1] - self.to[1], -self.deg)
        return (self.pv[0] + x, self.pv[1] + y)

    def q(self, x, y):
        return self.s.q(*self.inv((x, y)))


class Motion(Xf):
    """Just the transform (no shape): call it on points, wrap shapes with it."""
    def __init__(self, pivot, deg, to=None):
        self.pv, self.deg = pivot, deg
        self.to = to if to is not None else pivot

    def __call__(self, q):
        return self.fwd(q)

    def wrap(self, shape):
        return Xf(shape, self.pv, self.deg, self.to)


def quad_legs(p, r, step, R):
    """Four legs (far fore, far hind, near hind, near fore) for the walk step.
    Like canid.legs, plus hind-paw size and the reared forelegs."""
    lg = p["leg"]
    G, xs, xh, ts, th, ch, hp = r["G"], r["xs"], r["xh"], r["ts"], r["th"], r["ch"], r["hp"]
    digi = lg["digi"]
    reared = abs(p["body"]["rear"]) > 0.01
    out = []
    for near in (False, True):
        for fore in (True, False):
            pl, pr = lg["paw"] if (fore or not lg["hpaw"]) else lg["hpaw"]
            arms = False
            if fore:
                x0 = xs + 1.5 + (0 if near else lg["far"][0])
                top = (x0, ts + ch * 0.45)
                elbow = (x0 + lg["elbow"], ts + ch - 0.8)
                wh = pr + digi * lg["h"] * 0.20 + 0.5
                wrist = (x0 - 0.2, G - wh)
                paw = (wrist[0] - pl * 0.35 - (1 - digi) * pl * 0.2, G - pr)
                pts, radii = [top, elbow, wrist], list(lg["fr"])
                if reared:
                    t2 = R(top)
                    if lg["arms"]:
                        ex, ey, wx, wy = lg["arms"]
                        if not near:
                            t2 = (t2[0] + lg["far"][0] * 0.5, t2[1] - 0.5)
                        e2 = (t2[0] + ex, t2[1] + ey)
                        w2 = (e2[0] + wx, e2[1] + wy)
                        pts, arms = [t2, e2, w2], True
                        paw = (w2[0] - pl * 0.3, w2[1] + pr * 0.2)
                    else:
                        dx = t2[0] - top[0]
                        f = (elbow[1] - top[1]) / max(0.1, wrist[1] - top[1])
                        e2 = (elbow[0] + dx, lerp(t2[1], wrist[1], f))
                        pts = [t2, e2, (wrist[0] + dx, wrist[1])]
                        paw = (paw[0] + dx, paw[1])
            else:
                x0 = xh + 0.5 + (0 if near else lg["far"][1])
                top = (x0, th + hp * 0.4)
                knee = (x0 - lg["knee"], th + hp + lg["h"] * 0.1)
                hh = pr + digi * lg["h"] * 0.38 + 0.4
                hock = (x0 + lg["hock"] * (0.4 + 0.6 * digi), G - hh)
                paw = (hock[0] - pl * 0.4 - (1 - digi) * pl * 0.25, G - pr)
                pts, radii = [top, knee, hock], list(lg["hr"])
            pts.append((paw[0] + pl * 0.15, paw[1] - pr * 0.2))
            radii.append(radii[-1] * 0.95)
            swing = 0.0
            if step and not arms:
                sgn = 1 if (near == fore) else -1
                swing = lg["stride"] * sgn
            if swing:
                piv = pts[0]
                pts = [pts[0]] + [turn(q, piv, swing) for q in pts[1:]]
                pc = turn(paw, piv, swing)
                lift = max(0.0, (pc[1] + pr) - G)
                pts = [pts[0]] + [(x, y - lift * (k / 3)) for k, (x, y) in enumerate(pts[1:], 1)]
                paw = (pc[0], pc[1] - lift)
            if arms and step:  # the held-up hands bob a little
                pts = pts[:1] + [(x, y - 0.6) for x, y in pts[1:]]
                paw = (paw[0], paw[1] - 0.6)
            out.append(dict(near=near, fore=fore, pts=pts, radii=radii, arms=arms,
                            paw=(paw[0], paw[1], pl / 2, pr, 0)))
    return out


def quad_tail(p, r, R, extra=0.0):
    t = p["tail"]
    x, y = R((r["xh"] + r["hp"] * 0.3, r["th"] + 1.6 + t["dy"]))
    seg = t["len"] / 5
    pts = [(x, y)]
    a = t["a0"] + extra
    bends = t.get("bends") or [t["bend"]] * 5
    for k in range(5):
        x += seg * math.cos(math.radians(a))
        y += seg * math.sin(math.radians(a))
        pts.append((x, y))
        a += bends[k] + extra * 0.15
    r0, rm, rt = t["r"]
    w = t["widest"]
    radii = []
    for k in range(6):
        f = k / 5
        radii.append(lerp(r0, rm, f / w) if f <= w else lerp(rm, rt, (f - w) / (1 - w)))
    return pts, radii


def quad_side(p, phase=0, step=None):
    if step is not None:
        phase = 0
        if p["ow_side"]:
            p = _merge(p, p["ow_side"])
    act = p["action"] if phase else dict(tilt=0.0, gape=0.0, tail=0.0, ear=0.0)
    r = rig(p)
    hd, b = p["head"], p["body"]
    hs = head_shapes(p, r)
    rear = b["rear"]
    rp = (r["xh"] + b["rear_pivot"][0], r["th"] + r["hp"] * b["rear_pivot"][1])
    R = Motion(rp, rear)
    Rinv = lambda x, y: R.inv((x, y))  # noqa: E731
    pivot = r["pivot"]
    tilt = act.get("tilt", 0.0) + rear * b["head_follow"]
    Hm = Motion(pivot, tilt, to=R(pivot))
    H = Hm
    Hinv = lambda x, y: Hm.inv((x, y))  # noqa: E731
    hx, hy = r["hx"], r["hy"]
    marks = p["marks"]
    belly = _countershade(p, r)
    far = dict(light=-0.28)

    def region(group, default, local=None, **kw):
        c = dict(G=r["G"], belly=belly)
        c.update(kw)

        def f(x, y):
            lx, ly = local(x, y) if local else (x, y)
            for m in marks:
                if _mark(m, group, lx, ly, c):
                    return m["ramp"]
            return default(lx, ly)
        return f

    torso = R.wrap(Union([Ellipse(*e) for e in r["torso"]], k=b["k"]))
    body_local = Rinv if rear else None
    torso_reg = region("torso", lambda x, y: "pale" if y > belly(x) else "fur", local=body_local)
    (n0, n1) = r["neck"]
    neck = Tube([R(n0), H(n1)], [p["neck"]["r0"], p["neck"]["r1"]])
    ta, tsl = p["throat"] if p["throat"] else (None, None)

    def neck_default(x, y):
        ax, ay = hs["hinge"][0], hs["hinge"][1] + 0.6
        bx, by = r["xs"] - 1.0, belly(r["xs"]) - 0.5
        if ta is not None:
            return "pale" if y > ta + tsl * x else "fur"
        t = clamp((x - ax) / ((bx - ax) or 1), 0, 1)
        return "pale" if y > lerp(ay, by, t) else "fur"
    neck_reg = region("neck", neck_default, local=body_local)

    def head_local(x, y):
        u, v = Hinv(x, y)
        return u - hx, v - hy

    mouth_rel = hs["mouth_y"] - hy

    def head_default(u, v):
        cr = hd["cr"]
        tipx = hs["tip"][0] - hx
        y_line = lerp(mouth_rel - hd["md"] * 0.45, cr * 0.5, clamp((u - tipx) / (cr * 0.8 - tipx), 0, 1))
        return "pale" if v > y_line else "fur"
    head_reg = region("head", head_default, local=head_local)
    head = Hm.wrap(Union(hs["shapes"], k=hd["k"]))

    gape = act.get("gape", 0.0)
    hinge = hs["hinge"]
    J = lambda pt: H(turn(pt, hinge, gape))  # noqa: E731
    jd = hs["jd"]
    jaw_pts = [J((hinge[0] - 0.5, hinge[1] + 0.2)), J(((hinge[0] + hs["chin"][0]) / 2, hs["mouth_y"] + jd * 0.45)),
               J(hs["chin"])]
    jaw = Tube(jaw_pts, [jd * 0.75, jd * 0.62, jd * 0.48])
    jaw_reg = region("jaw", lambda x, y: "pale", local=head_local)

    ear = p["ear"]
    eb = (hx + hd["cr"] * 0.2 + ear["dx"], hy - hd["cr"] * 0.62 + ear["dy"])
    elean = ear["lean"] + act.get("ear", 0.0)

    def ear_shape(base, scale=1.0):
        bx, by = base
        h, w = ear["h"] * scale, ear["w"] * scale
        a = math.radians(elean)
        tip = (bx + h * math.sin(a), by - h * math.cos(a))
        if ear["kind"] == "round":
            c = ((bx + tip[0]) / 2, (by + tip[1]) / 2 + 0.3)
            return Ellipse(*H(c), w / 2, h / 2 + 0.6, elean + tilt), None
        pts = [(bx - w * 0.55, by + 1.2), tip, (bx + w * 0.5, by + 1.4)]
        inner = [(bx - w * 0.3, by + 0.8), (tip[0] - 0.2 * math.sin(a) * h * 0.25, tip[1] + h * 0.3),
                 (bx + w * 0.12, by + 1.0)]
        return Facet([H(q) for q in pts]), Facet([H(q) for q in inner])
    near_ear, inner_ear = ear_shape(eb)
    far_ear, _ = ear_shape((eb[0] - ear["w"] * ear.get("far", 0.95), eb[1] + 0.2), 0.92)
    ear_reg = region("ear", lambda x, y: "fur", local=head_local)

    tpts, trad = quad_tail(p, r, R, act.get("tail", 0.0))
    tail = Path(tpts, trad)
    tail_reg = region("tail", lambda x, y: "fur", tail_frac=tail.frac)

    L4 = quad_legs(p, r, step, R)
    parts = [Part(tail, p.get("tail_ramp", "fur"), z=p["tail"].get("z", -3), region=tail_reg, inner=("fur", 0)),
             Part(far_ear, "fur", z=-0.5, region=ear_reg, **far)]
    for lg_ in L4:
        if not lg_["near"]:
            reg = region("legs", lambda x, y: "fur", leg="fore" if lg_["fore"] else "hind")
            parts += [Part(Tube(lg_["pts"], lg_["radii"]), "fur", z=-2, region=reg, **far),
                      Part(Ellipse(*lg_["paw"]), "fur", z=-1.9, region=reg, **far)]
    br = p["branch"]
    if br and step is None:
        y = r["G"] + br.get("dy", 0.0)
        bx0, bx1 = br["x"]
        brad, btl = br.get("r", 2.2), br.get("tilt", 0.0)
        bshape = Tube([(bx0, y + brad * 0.8 - btl / 2), (bx1, y + brad * 0.8 + btl / 2)], [brad, brad * 0.85])
        parts.append(Part(bshape, "bark", z=br.get("z", -1.95), flat=0.6, outline=("bark", 0) if br.get("soft") else "outline"))
    parts.append(Part(torso, "fur", z=0, flat=0.55, region=torso_reg))
    lg = p["leg"]
    for lg_ in L4:
        if lg_["near"]:
            reg = region("legs", lambda x, y: "fur", leg="fore" if lg_["fore"] else "hind")
            z = 2 if lg_["fore"] else 1.5
            if lg_["arms"]:
                z = 2.7
            parts += [Part(Tube(lg_["pts"], lg_["radii"]), "fur", z=z, region=reg, inner=("fur", 0)),
                      Part(Ellipse(*lg_["paw"]), "fur", z=z + 0.1, region=reg, inner=("fur", 0))]
            if not lg_["fore"] and lg["thigh"]:
                (x0, y0), (x1, y1) = lg_["pts"][0], lg_["pts"][1]
                s = lg["thigh"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.6, (y0 + y1) / 2 - 0.6, r["hp"] * 0.42 * s,
                                          r["hp"] * 0.55 * s, 25), "fur", z=1.6, region=torso_reg,
                                  inner=("fur", 0)))
    for ex in p["extra"]:
        cx, cy, rx, ry = ex["e"][:4]
        deg = ex["e"][4] if len(ex["e"]) > 4 else 0.0
        if ex.get("on", "head") == "head":
            c, deg = H((hx + cx, hy + cy)), deg + tilt
        else:
            c, deg = R((cx, cy)), deg + rear
        parts.append(Part(Ellipse(*c, rx, ry, deg), ex["ramp"], z=ex.get("z", 3.1), inner=("fur", 0),
                          light=ex.get("light", 0.0)))
    parts += [Part(neck, "fur", z=2.5, region=neck_reg, inner=("fur", 0)),
              Part(jaw, "pale", z=2.9, region=jaw_reg, inner=("fur", 0)),
              Part(head, "fur", z=3, flat=0.5, region=head_reg, inner=("fur", 0)),
              Part(near_ear, "fur", z=3.2, region=ear_reg, inner=("fur", 0))]
    head_part = len(parts) - 2
    tt = p["teeth"]
    if gape:
        mi = [H(hinge), H((hs["tip"][0] + 1.5, hs["mouth_y"] - 0.2)), J((hs["chin"][0] + 0.5, hs["chin"][1] - 0.6))]
        parts.append(Part(Facet(mi), "skin", z=2.8, line=False, shadow=False))
    g = tt.get("gnaw")
    if g:
        gx = hs["tip"][0] + g.get("dx", 1.3)
        a = (gx, hs["mouth_y"] - 0.6)
        bpt = (gx + g.get("rake", 0.3), hs["mouth_y"] + g["len"])
        w = g.get("w", 0.6)
        parts.append(Part(Tube([H(a), J(bpt) if g.get("lower") else H(bpt)], [w, w * 0.9]), g.get("ramp", "white"),
                          z=3.15, flat=0.8, shadow=False, inner=("fur", 0)))

    eye = p["eye"]
    ec = H((hx + eye["dx"], hy + eye["dy"]))
    nose_c = H((hs["tip"][0] + 0.9, hs["tip"][1] - 0.1))

    def details(cv):
        big = cv.big
        if inner_ear is not None and ear["inner"] and big:
            paint(cv, inner_ear, ("pale", -1), owner_part=parts.index(next(q for q in parts if q.shape is near_ear)))
        if big and p["fur_dashes"]:
            rows, diag = p["fur_dashes"]
            fur = set(cv.pal.index["fur"][1:])
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in fur and py % rows == 0 and (px + py) % diag == 0:
                        cv.shade(px, py, -1)
        if big and br and step is None and "bark" in cv.pal.index:  # bark: sparse darker dashes
            bk = set(cv.pal.index["bark"][1:])
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in bk and (px * 2 + py * 3) % 7 == 0 and px % 3:
                        cv.shade(px, py, -1)
        if big and lg["toes"]:
            for lg_ in L4:
                if lg_["near"] and not lg_["arms"]:
                    x, y, rx, ry, _ = lg_["paw"]
                    for k in (0.15, 0.55):
                        cv.shade(*cv.pt(x - rx + rx * k * 2, y + ry * 0.55), -1)
        if big and p["claws"]:
            for lg_ in L4:
                if lg_["near"]:
                    x, y = lg_["paw"][0] - lg_["paw"][2], lg_["paw"][1] + lg_["paw"][3] * 0.3
                    for k in range(2):
                        cv.set(*cv.pt(x + k * 0.9, y), "white" if "claw" not in cv.pal.index else "claw")
        if eye["line"] and big:
            a, b2 = eye["line"]
            cv.line(H((hx + a[0], hy + a[1])), H((hx + b2[0], hy + b2[1])), eye.get("line_ramp", ("dark", 0)))
        cv.disc(nose_c, 1.25 if big else 0.8, p.get("nose_ramp", ("dark", 0)), only_opaque=True)
        if big and p["nostril"]:
            px, py = cv.pt(*nose_c)
            cv.set(px, py - 1, ("dark", -1) if "nose_ramp" not in p else (p["nose_ramp"][0], -1))
        if big and gape and tt["canine"]:
            ux = hs["tip"][0] + 1.6
            top = H((ux, hs["mouth_y"] + 0.1))
            cv.line(top, H((ux + 0.2, hs["mouth_y"] + tt["canine"])), "white", only_opaque=False)
            lo = J((hs["chin"][0] + 0.6, hs["chin"][1] - jd * 0.5))
            cv.line(lo, (lo[0] + 0.3, lo[1] - tt["canine"] * 0.8), "white", only_opaque=False)
        # the far eye (forward-facing eyes), only on the head's own pixels
        if eye["far"]:
            fx, fy, fr = eye["far"]
            fc = H((hx + fx, hy + fy))
            rr = fr if big else max(0.6, fr * 0.6)
            paint(cv, Ellipse(*fc, rr, rr), "outline", owner_part=head_part)
            if big and eye["big"] and fr * cv.scale >= 2.0:
                paint(cv, Ellipse(fc[0] - 0.15, fc[1] + 0.1, rr * 0.5, rr * 0.5), eye["big"], owner_part=head_part)
        r_ = eye["r"]
        fwd = 1 if cv.flip else -1
        if big:
            if eye["ring"]:
                cv.disc(ec, r_ + 0.9 / cv.scale, eye["ring"], only_opaque=True)
            cv.disc(ec, r_, "outline", only_opaque=True)
            px, py = cv.pt(*ec)
            if eye["big"]:  # iris around a dark pupil
                cv.disc(ec, r_ - 0.95 / cv.scale, eye["big"], only_opaque=True)
                cv.disc(ec, max(0.55 / cv.scale, (r_ - 0.95 / cv.scale) * 0.5), "outline", only_opaque=True)
                cv.set(px + fwd, py - 1, "white")
            else:
                if eye["iris"]:
                    cv.set(px - fwd, py, eye["iris"])
                cv.set(px + fwd, py - 1, "white")
        else:
            if eye["ring"] and eye["big"]:
                cv.disc(ec, max(0.6, r_ * 0.6) + 0.9 / cv.scale, eye["ring"], only_opaque=True)
            cv.disc(ec, max(0.6, r_ * 0.6), "outline", only_opaque=True)

    def post(cv):
        if not cv.big or not p["whiskers"]:
            return
        for a, b2 in p["whiskers"]:
            for px, py in cv.pixels_on_line(H((hx + a[0], hy + a[1])), H((hx + b2[0], hy + b2[1]))):
                if cv.inside(px, py) and not cv.idx[py][px]:
                    cv.idx[py][px] = cv.pal.get(("pale", -1))

    return Model(parts, p["ramps"], details, post)


def side(p, phase=0, step=None):
    if "torso" in p:
        return classic_side(p, phase, step)
    return quad_side(p, phase, step)


def overworld(p, view, step):
    if "torso" in p:
        return classic_overworld(p, view, step)
    if p.get("ow_model"):
        return p["ow_model"](p, view, step)
    return canid_overworld(p, view, step)


PLAN = BodyPlan(
    "small_mammal", "generalised small quadrupeds: multituberculates, cimolestids, condylarths, early marsupials",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_MAMMAL, tracks="TRACKS_FOOT",
)
