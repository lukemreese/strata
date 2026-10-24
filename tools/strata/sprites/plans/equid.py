"""equid body plan: the horse series, plus the shared hoofed-mammal engine that
plans/ungulate.py reuses.

Species (taxonomy.py):
    sifrhippus    Sifrhippus sandrae (Willwood Fm, WY, 4 kg)
    eohippus      Eohippus angustidens (Wind River Fm, WY, 10 kg)
    mesohippus    Mesohippus bairdi (Brule Fm, SD, 40 kg)
    protohippus   Protohippus simus (Ashfall, NE, 100 kg)
    hypohippus    Hypohippus (Miocene Great Plains, NE, 200 kg)
    cormohippari  Cormohipparion occidentale (Ashfall, NE, 100 kg)
    equus         Equus (Natural Trap Cave, WY, 300 kg)

The horse series is one parameter set evolving along the line (specs/equid.py):
size and leg length up, back from arched (duiker-like) to straight, toes from
4 front / 3 hind to 3 and then 1, the face from short and low to long and deep
(high-crowned grinding teeth need a deep jaw), the mane from a short crest to
the upright Equus brush. Family marks on every horse: pale belly and mealy
muzzle, dark mane, tail hair and lower legs; forest dapples fade out from
Sifrhippus to Mesohippus, the open-country grazers are plain or dun.

The engine (`side`, `overworld`) builds a hoofed quadruped from proportions,
in the spirit of the carnivore engine in plans/canid.py (whose Facet, Path,
paint, tail_points and colour-mark rules it imports read-only), but with
ungulate legs (elbow, knee/carpus, cannon, fetlock, pastern, hoof; hind leg
with stifle and a high hock), side toes, a multi-point neck (camels), a head
in its own rigid frame (long faces carried nose-down), manes and horns.
Model units are sprite pixels at scale 1, head to the LEFT, y down.

Spec keys (lengths in model px; see DEFAULTS):
    body   L (shoulder-to-hip x), top_s / top_h (back height at withers / hip),
           chest / waist / hip (depths), sag (back dip; negative arches the
           back), chest_w / rump_w, hump (dx, dy, rx, ry from the withers or
           None), k (blend)
    leg    h (chest bottom to ground), fr (fore radii: arm, forearm, cannon,
           fetlock), hr (hind: thigh, gaskin, cannon, fetlock), kn (carpus
           height as a fraction of h above the ground), hk (hock height,
           same), pas (fetlock height), slope (pastern lean, px), hoof (length,
           height), toes (fore, hind) 1..4, side (side-toe size, lift above
           the ground), foot "hoof"|"cloven"|"pad", fx / hx (x offsets of the
           near legs), far (fore dx, hind dx of the far legs), stifle (px the
           stifle sits ahead of the hip joint), hock (px the hock sits behind),
           thigh (near haunch size factor), arm (shoulder muscle factor),
           stride (walk swing, degrees)
    neck   pts (list of (dx, dy) from the withers top; first = base, last =
           where the head attaches), r (radii per point)
    mane   None or dict(r=radius, off=offset beyond the neck top in neck
           radii, up=standing brush, ramp, x0/x1 fractions along the neck)
    head   dx, dy (cranium centre from the neck end), face (deg nose-down),
           cr, cw (cranium radius, width factor), ml (forehead-to-nose length),
           md / mt (muzzle depth at root / tip), drop (nose top below the
           forehead line), jaw (cheek/jaw-muscle size), jx, jy (its centre,
           cranium radii), chin (lip bulge radius or 0), k (blend)
    ear    h, w, lean (deg back from vertical, world), dx, dy (base offset in
           head units), far (dx of the far ear), inner (pale inner fur)
    horns  list of dict(kind="path", base=(x, y) head-local, pts=[...] world-
           oriented offsets, r=[...]) or kind="curl" (base, R=(r0, r1),
           a=(a0, a1) deg, thick=(t0, t1), n): far copy drawn behind, darker
           (far=(dx, dy) head-local offset), rings=annulation spacing
    tail   as the carnivore engine (len, a0, bend, r, widest, dy)
    eye    dx, dy (head-local), r, ring (ramp for a pale eye ring or None)
    nose   (dx, dy) head-local nostril offset from the nose tip, or None
    mouth  length of the mouth line from the lips (px), or 0
    marks  colour rules (canid.py `_mark` kinds plus `dorsal` (w: stripe
           along the back top), `bars` (period, width, top: leg barring
           below G - top), `rump` (e: ellipse, absolute)), first match wins
    action phase-2 pose: tilt (head deg, + raises the nose), neck (deg the
           neck swings about its base, + lifts), tail (deg), ear (deg),
           paw (upper, lower deg: near foreleg raised) or None
    fur_dashes (rows, diag) or None, ow_end (end-view proportions),
    ow_ramps (end-view group colours: legs, hoof, muzzle, rump, chest, face,
    tail, mane, belly), ow_face (extra end-view pixels in U)

Ramps the engine uses: outline (1), fur (3-4), pale (2-3), dark (1-2),
hoof (1-2), white (1); optional mane, horn, skin and any ramp named in marks.
"""

import math

from ..core.geom import Ellipse, Tube, Union, Part, Model, turn, lerp, clamp, rot
from ..core.plan import BodyPlan
from .canid import Facet, Path, paint, _mark, tail_points

FOOTPRINT_HORSE = [  # a one-toed hoof print: a rounded U with the frog
    "................",
    "................",
    "................",
    ".....######.....",
    "....########....",
    "...###....###...",
    "...##......##...",
    "...##..##..##...",
    "...##.####.##...",
    "...##.####.##...",
    "....#.####.#....",
    "....#..##..#....",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINT_THREE_TOED = [  # a big central hoof and two small side toes
    "................",
    "................",
    "................",
    "......####......",
    ".....######.....",
    "..#..######..#..",
    ".###.######.###.",
    ".###..####..###.",
    "..#....##....#..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]


class Xf:
    """A shape placed by a transform: fwd(local) -> world, inv(world) -> local.
    The bbox is the box around the transformed local bbox corners."""
    def __init__(self, shape, fwd, inv):
        self.s, self.fwd, self.inv = shape, fwd, inv
        x0, y0, x1, y1 = shape.bbox
        cs = [fwd(c) for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
        self.bbox = (min(c[0] for c in cs), min(c[1] for c in cs), max(c[0] for c in cs), max(c[1] for c in cs))

    def q(self, x, y):
        return self.s.q(*self.inv(x, y))


class XfPath(Xf):
    """An Xf of a Path that keeps its fraction lookup (horn rings, tail tips)."""
    def frac(self, x, y):
        return self.s.frac(*self.inv(x, y))


DEFAULTS = dict(
    front=0.9, back=0.95, icon=0.46,
    body=dict(L=24.0, top_s=-8.0, top_h=-8.0, chest=12.0, waist=10.0, hip=11.0, sag=0.6,
              chest_w=1.0, rump_w=1.0, hump=None, k=0.14),
    leg=dict(h=16.0, fr=(2.8, 1.9, 1.15, 1.3), hr=(3.0, 2.0, 1.15, 1.3), kn=0.48, hk=0.42, pas=2.6, slope=1.0,
             hoof=(2.8, 2.0), toes=(1, 1), side=(0.55, 1.4), foot="hoof", fx=1.8, hx=0.0, far=(3.2, -2.8),
             stifle=3.0, hock=2.4, thigh=1.0, arm=0.8, stride=16.0),
    neck=dict(pts=[(0.5, 4.0), (-3.0, -3.0), (-5.0, -7.5)], r=[5.0, 3.8, 3.0]),
    mane=None,
    head=dict(dx=-1.0, dy=-1.5, face=38.0, cr=3.6, cw=1.0, ml=11.0, md=5.0, mt=3.4, drop=0.6, jaw=1.0,
              jx=0.15, jy=0.55, chin=0.0, k=0.14),
    ear=dict(h=4.0, w=2.6, lean=5.0, dx=0.25, dy=-0.7, far=-0.9, inner=True),
    horns=[],
    tail=dict(len=14.0, a0=70.0, bend=4.0, r=(1.4, 2.4, 1.0), widest=0.6, dy=0.5),
    eye=dict(dx=-1.1, dy=-0.8, r=1.2, ring=None),
    nose=(1.3, -0.4),
    mouth=2.6,
    marks=[],
    belly=None,
    action=dict(tilt=12.0, neck=4.0, tail=-14.0, ear=-12.0, paw=None),
    fur_dashes=None,
    ow=dict(tracks="TRACKS_FOOT"),
    ow_end={},
    ow_ramps={},
    ow_face=[],
)


# ---------------------------------------------------------------------------
# geometry


def rig(p, neck_deg=0.0):
    b, lg = p["body"], p["leg"]
    L = b["L"]
    xs, xh = -L / 2, L / 2
    ts, th = b["top_s"], b["top_h"]
    ch, wa, hp = b["chest"], b["waist"], b["hip"]
    G = ts + ch + lg["h"]
    r = dict(L=L, xs=xs, xh=xh, ts=ts, th=th, ch=ch, wa=wa, hp=hp, G=G)
    r["torso"] = [
        (xs + 1.0, ts + ch / 2, ch * 0.62 * b["chest_w"], ch / 2, -6),
        (0.0, (ts + th) / 2 + b["sag"] + wa / 2, L * 0.42, wa / 2, 0),
        (xh - 0.5, th + hp / 2, hp * 0.6 * b["rump_w"], hp / 2, 8),
    ]
    if b["hump"]:
        dx, dy, rx, ry = b["hump"]
        r["torso"].append((xs + dx, ts + dy, rx, ry, -10))
    nk = p["neck"]
    base = (xs + nk["pts"][0][0], ts + nk["pts"][0][1])
    pts = [base] + [turn((xs + dx, ts + dy), base, neck_deg) for dx, dy in nk["pts"][1:]]
    r["neck"] = pts
    end = pts[-1]
    hd = p["head"]
    r["C"] = (end[0] + hd["dx"], end[1] + hd["dy"])
    r["pivot"] = end
    return r


def head_frame(p, r, tilt):
    """fwd(local) -> world and inv(world) -> local for the head. Local frame:
    cranium centre at the origin, face pointing left, before the face angle."""
    face = p["head"]["face"]
    C, pv = r["C"], r["pivot"]

    def fwd(pt):
        x, y = rot(pt[0], pt[1], -face)
        return turn((C[0] + x, C[1] + y), pv, tilt)

    def inv(x, y):
        wx, wy = turn((x, y), pv, -tilt)
        return rot(wx - C[0], wy - C[1], face)
    return fwd, inv


def head_local_shapes(p):
    hd = p["head"]
    cr, ml = hd["cr"], hd["ml"]
    md, mt = hd["md"], hd["mt"]
    cran = Ellipse(0, 0, cr * hd["cw"], cr * 0.85)
    top0 = -cr * 0.62
    root = (-cr * 0.25, top0 + md / 2)
    tip = (-ml + mt / 2, top0 + hd["drop"] + mt / 2)
    shapes = [cran, Tube([root, tip], [md / 2, mt / 2])]
    if hd["jaw"]:
        j = hd["jaw"]
        shapes.append(Ellipse(cr * hd["jx"], cr * hd["jy"], cr * 0.82 * j, cr * 0.66 * j, -12))
    if hd["chin"]:
        c = hd["chin"]
        shapes.append(Ellipse(tip[0] + c * 0.4, tip[1] + mt * 0.42, c * 1.2, c * 0.8, 10))
    return shapes, dict(tip=tip, root=root, top0=top0)


def _local_vec(v, face):
    """A world-oriented offset expressed in the head-local frame."""
    return rot(v[0], v[1], face)


def horn_paths(p, h):
    """Head-local Path of one horn spec (and its far copy)."""
    face = p["head"]["face"]
    bx, by = h["base"]
    if h.get("kind") == "curl":
        r0, r1 = h["R"]
        a0, a1 = h["a"]
        t0, t1 = h["thick"]
        n = h.get("n", 9)
        a0r = math.radians(a0)
        c = (-r0 * math.cos(a0r), -r0 * math.sin(a0r))  # spiral centre (world-oriented, from the base)
        pts, rad = [], []
        for k in range(n):
            f = k / (n - 1)
            a = math.radians(lerp(a0, a1, f))
            R = lerp(r0, r1, f)
            pts.append((c[0] + R * math.cos(a), c[1] + R * math.sin(a)))
            rad.append(lerp(t0, t1, f ** 0.9))
    else:
        pts, rad = h["pts"], h["r"]
    loc = [(bx + u, by + v) for u, v in (_local_vec(q, face) for q in pts)]
    return loc, list(rad)


def legs(p, r, step, paw=None):
    """Four legs (far fore, far hind, near fore, near hind): tube points/radii,
    pastern and hoof shapes, posed for the walk step or the pawing action."""
    lg = p["leg"]
    G, xs, xh, ts, th, ch, hp = r["G"], r["xs"], r["xh"], r["ts"], r["th"], r["ch"], r["hp"]
    h = lg["h"]
    hl, hh = lg["hoof"]
    pas, slope = lg["pas"], lg["slope"]
    out = []
    for near in (False, True):
        for fore in (True, False):
            if fore:
                x0 = xs + lg["fx"] + (0 if near else lg["far"][0])
                top = (x0 + 0.8, ts + ch * 0.4)
                elbow = (x0 + 1.4, ts + ch * 0.92)
                knee = (x0 + 0.3, G - h * lg["kn"])
                fet = (x0 + 0.3, G - pas)
                pts, radii = [top, elbow, knee, fet], list(lg["fr"])
            else:
                x0 = xh + lg["hx"] + (0 if near else lg["far"][1])
                top = (x0, th + hp * 0.35)
                stifle = (x0 - lg["stifle"], th + hp * 0.98)
                hock = (x0 + lg["hock"], G - h * lg["hk"])
                fet = (hock[0] - 0.4, G - pas)
                pts, radii = [top, stifle, hock, fet], list(lg["hr"])
            hc = (fet[0] - slope - hl * 0.15, G - hh)   # hoof top centre
            pastern = [fet, (hc[0] + 0.2, hc[1] + 0.3)]
            foot = lg["foot"]
            if foot == "pad":   # camels: a broad flat pad with a small nail in front
                hoof = [(hc[0] - hl * 0.55, G - hh * 0.9), (hc[0] + hl * 0.55, G - hh * 0.9),
                        (hc[0] + hl * 0.62, G), (hc[0] - hl * 0.7, G)]
            else:
                hoof = [(hc[0] - hl * 0.32, G - hh), (hc[0] + hl * 0.42, G - hh * 0.9),
                        (hc[0] + hl * 0.45, G), (hc[0] - hl * 0.6, G)]
            toes = lg["toes"][0 if fore else 1]
            ss, slift = lg["side"]
            sides = []
            if toes >= 3:   # side toes behind the main hoof (one visible per side)
                sw, sh = hl * ss, hh * ss * 1.1
                sx = hc[0] + hl * 0.72
                sy = G - slift
                sides.append([(sx - sw * 0.35, sy - sh), (sx + sw * 0.5, sy - sh * 0.85), (sx + sw * 0.55, sy),
                              (sx - sw * 0.55, sy)])
                if toes == 4:
                    sx2 = hc[0] + hl * 0.05
                    sy2 = G - slift * 0.6
                    sides.append([(sx2 - sw * 0.3, sy2 - sh * 0.9), (sx2 + sw * 0.45, sy2 - sh * 0.8),
                                  (sx2 + sw * 0.5, sy2), (sx2 - sw * 0.5, sy2)])
            leg = dict(near=near, fore=fore, pts=pts, radii=radii, pastern=pastern, hoof=hoof, sides=sides)
            # posing: walk swing about the top, or the raised near foreleg
            swing = 0.0
            if step:
                sgn = 1 if (near == fore) else -1
                swing = lg["stride"] * sgn
            if swing:
                _swing(leg, pts[0], swing, G)
            if paw and near and fore:
                up, lo = paw
                _rotate(leg, 1, pts[1], up)        # from the elbow
                _rotate(leg, 2, leg["pts"][2], lo)  # from the knee
            out.append(leg)
    return out


def _all_points(leg, frm):
    return leg["pts"][frm:], leg["pastern"], leg["hoof"], leg["sides"]


def _rotate(leg, frm, piv, deg):
    leg["pts"] = leg["pts"][:frm] + [turn(q, piv, deg) for q in leg["pts"][frm:]]
    leg["pastern"] = [turn(q, piv, deg) for q in leg["pastern"]]
    leg["hoof"] = [turn(q, piv, deg) for q in leg["hoof"]]
    leg["sides"] = [[turn(q, piv, deg) for q in s] for s in leg["sides"]]


def _swing(leg, piv, deg, G):
    _rotate(leg, 1, piv, deg)
    low = max(q[1] for q in leg["hoof"])
    lift = max(0.0, low - G)
    if lift:
        f = lambda q: (q[0], q[1] - lift)  # noqa: E731
        leg["pts"] = leg["pts"][:1] + [f(q) for q in leg["pts"][1:]]
        leg["pastern"] = [f(q) for q in leg["pastern"]]
        leg["hoof"] = [f(q) for q in leg["hoof"]]
        leg["sides"] = [[f(q) for q in s] for s in leg["sides"]]


# ---------------------------------------------------------------------------
# colour rules


def _countershade(p, r):
    if p["belly"]:
        a, s = p["belly"]
        return lambda x: a + s * x
    y0 = r["ts"] + r["ch"] * 0.78
    y1 = r["th"] + r["hp"] * 0.88
    return lambda x: lerp(y0, y1, clamp((x - r["xs"]) / (r["xh"] - r["xs"]), 0, 1))


def _topline(shape, x0, x1, y0, y1):
    """The top outline of a shape sampled per 0.5 px column: x -> y."""
    xs, tops = [], []
    x = x0
    while x <= x1:
        y = y0
        while y < y1 and shape.q(x, y) <= 0:
            y += 0.25
        xs.append(x)
        tops.append(y)
        x += 0.5

    def f(x):
        i = int(clamp((x - x0) / 0.5, 0, len(tops) - 1))
        return tops[i]
    return f


def hmark(m, group, x, y, ctx):
    """canid `_mark` plus the hoof-engine kinds dorsal, bars and rump."""
    k = m["kind"]
    if k in ("dorsal", "bars", "rump"):
        on = m["on"]
        if on != "all" and group != on and (not isinstance(on, tuple) or group not in on):
            return False
        if k == "dorsal":
            top = ctx.get("top")
            if top is None:
                return False
            if "x" in m and not (m["x"][0] <= x <= m["x"][1]):
                return False
            return y < top(x) + m["w"]
        if k == "bars":
            if y < ctx["G"] - m["top"]:
                return False
            return (y % m["period"]) < m["width"]
        if k == "rump":
            cx, cy, rx, ry = m["e"]
            return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    return _mark(m, group, x, y, ctx)


# ---------------------------------------------------------------------------
# side view


def side(p, phase=0, step=None):
    if step is not None:
        phase = 0
    act = p["action"] if phase else dict(tilt=0.0, neck=0.0, tail=0.0, ear=0.0, paw=None)
    r = rig(p, act.get("neck", 0.0))
    hd = p["head"]
    tilt = act.get("tilt", 0.0)
    fwd, inv = head_frame(p, r, tilt)
    marks = p["marks"]
    belly = _countershade(p, r)
    far = dict(light=-0.28)
    torso = Union([Ellipse(*e) for e in r["torso"]], k=p["body"]["k"])
    top = _topline(torso, r["xs"] - 8, r["xh"] + 8, min(r["ts"], r["th"]) - 6, r["G"])

    def ctx(**kw):
        c = dict(G=r["G"], belly=belly, top=top)
        c.update(kw)
        return c

    def region(group, default, local=None, **kw):
        c = ctx(**kw)

        def f(x, y):
            lx, ly = local(x, y) if local else (x, y)
            for m in marks:
                if hmark(m, group, lx, ly, c):
                    return m["ramp"]
            return default(lx, ly)
        return f

    torso_reg = region("torso", lambda x, y: "pale" if y > belly(x) else "fur")

    # neck (throat pale below a line from the jaw to the chest front)
    npts = r["neck"]
    nrad = p["neck"]["r"]
    neck = Tube(npts, nrad)
    jaw_w = fwd((hd["cr"] * 0.3, hd["cr"] * 0.9))
    chest_front = (r["xs"] - 2.0, belly(r["xs"]) - 1.0)

    def neck_default(x, y):
        ax, ay = jaw_w
        bx, by = chest_front
        t = clamp((x - ax) / ((bx - ax) or 1), 0, 1)
        return "pale" if y > lerp(ay, by, t) + p.get("throat", 0.6) else "fur"
    neck_reg = region("neck", neck_default)

    # mane along the top of the neck
    mane_part = None
    mn = p["mane"]
    if mn:
        mpts = []
        for i, q in enumerate(npts):
            a = npts[max(0, i - 1)]
            b = npts[min(len(npts) - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = -dy / ln, dx / ln       # dorsal side of a neck running from body to head
            off = nrad[i] * mn.get("off", 0.75)
            mpts.append((q[0] + nx * off, q[1] + ny * off))
        # trim to [x0, x1] fraction along the neck and run it on to the poll
        poll = fwd((hd["cr"] * 0.35, -hd["cr"] * 0.75))
        mpts = mpts[1:] if mn.get("skip_base") else mpts
        mpts.append(poll)
        mr = mn["r"]
        rad = [mr * 0.8] + [mr] * (len(mpts) - 2) + [mr * 0.75]
        mane_shape = Path(mpts, rad)
        mane_part = Part(mane_shape, mn.get("ramp", "mane"), z=2.6, inner=(mn.get("ramp", "mane"), 0),
                         region=region("mane", lambda x, y: mn.get("ramp", "mane")))

    # head
    lshapes, hinfo = head_local_shapes(p)
    head = Xf(Union(lshapes, k=hd["k"]), fwd, inv)
    head_reg = region("head", lambda x, y: "fur", local=inv)

    # ears (world-oriented lean)
    ear = p["ear"]
    cr = hd["cr"]
    ebase = (cr * ear["dx"], cr * ear["dy"])
    elean = ear["lean"] + act.get("ear", 0.0)

    def ear_local(base, scale=1.0):
        bx, by = base
        h, w = ear["h"] * scale, ear["w"] * scale
        a = math.radians(elean)
        tv = _local_vec((h * math.sin(a), -h * math.cos(a)), hd["face"] - tilt * 0)
        pv = _local_vec((math.cos(a), math.sin(a)), hd["face"])
        tip = (bx + tv[0], by + tv[1])
        pts = [(bx - pv[0] * w * 0.5, by - pv[1] * w * 0.5), tip, (bx + pv[0] * w * 0.5, by + pv[1] * w * 0.5)]
        mid = ((pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2)
        pts = [(q[0] + (q[0] - mid[0]) * 0.0, q[1]) for q in pts]
        inner = [lerp_pt(pts[0], tip, 0.15), lerp_pt(mid, tip, 0.8), lerp_pt(pts[2], tip, 0.3)]
        inner = [lerp_pt(q, mid, 0.25) for q in inner]
        return Facet(pts), Facet(inner)
    near_ear_l, inner_ear_l = ear_local(ebase)
    far_ear_l, _ = ear_local((ebase[0] + cr * ear["far"], ebase[1] + 0.2), 0.92)
    near_ear = Xf(near_ear_l, fwd, inv)
    inner_ear = Xf(inner_ear_l, fwd, inv)
    far_ear = Xf(far_ear_l, fwd, inv)
    ear_reg = region("ear", lambda x, y: "fur", local=inv)

    # horns
    horn_parts = []
    for hspec in p["horns"]:
        loc, rad = horn_paths(p, hspec)
        hr = hspec.get("ramp", "horn")
        near_h = XfPath(Path(loc, rad), fwd, inv)
        fdx, fdy = hspec.get("far", (cr * -0.7, 0.3))
        far_h = XfPath(Path([(x + fdx, y + fdy) for x, y in loc], [v * 0.95 for v in rad]), fwd, inv)
        hreg = region("horn", lambda x, y, hr=hr: hr, local=inv)
        horn_parts.append((Part(far_h, hr, z=-0.4 if hspec.get("behind") else 2.95, inner=(hr, 0), region=hreg,
                                **far), hspec))
        horn_parts.append((Part(near_h, hr, z=3.4, inner=(hr, 0), region=hreg,
                                outline=hspec.get("outline", "outline")), hspec))

    # tail
    tpts, trad = tail_points(p, r, act.get("tail", 0.0))
    tail = Path(tpts, trad)
    tail_reg = region("tail", lambda x, y: "fur", tail_frac=tail.frac)

    # legs
    L4 = legs(p, r, step, act.get("paw"))
    lg = p["leg"]
    parts = [Part(tail, "fur", z=-3, region=tail_reg, inner=("fur", 0)),
             Part(far_ear, "fur", z=-0.5, region=ear_reg, **far)]
    hoof_ramp = "hoof"
    pad = lg["foot"] == "pad"

    def leg_parts(lg_, z, extra):
        reg = region("legs", lambda x, y: "fur", leg="fore" if lg_["fore"] else "hind")
        hreg = region("hoof", lambda x, y: hoof_ramp if not pad else "fur")
        out = [Part(Tube(lg_["pts"], lg_["radii"]), "fur", z=z, region=reg, **extra),
               Part(Tube(lg_["pastern"], [lg_["radii"][-1], lg_["radii"][-1] * 0.85]), "fur", z=z + 0.05,
                    region=reg, **extra),
               Part(Facet(lg_["hoof"]), hoof_ramp, z=z + 0.1, region=hreg, flat=0.8, **extra)]
        for s in lg_["sides"]:
            out.append(Part(Facet(s), hoof_ramp, z=z - 0.05, flat=0.8, **extra))
        return out
    for lg_ in L4:
        if not lg_["near"]:
            parts += leg_parts(lg_, -2, far)
    parts.append(Part(torso, "fur", z=0, flat=0.55, region=torso_reg))
    for lg_ in L4:
        if lg_["near"]:
            z = 2 if lg_["fore"] else 1.5
            parts += leg_parts(lg_, z, dict(inner=("fur", 0)))
            if not lg_["fore"] and lg["thigh"]:
                (x0, y0), (x1, y1) = lg_["pts"][0], lg_["pts"][1]
                s = lg["thigh"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.8, (y0 + y1) / 2 - 0.8, r["hp"] * 0.42 * s,
                                          r["hp"] * 0.58 * s, 22), "fur", z=1.6, region=torso_reg,
                                  inner=("fur", 0)))
            if lg_["fore"] and lg["arm"] and not (act.get("paw") and lg_["near"] and False):
                (x0, y0), (x1, y1) = lg_["pts"][0], lg_["pts"][1]
                s = lg["arm"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.3, (y0 + y1) / 2 - 0.6, r["ch"] * 0.3 * s,
                                          r["ch"] * 0.44 * s, -10), "fur", z=2.05, region=torso_reg,
                                  inner=("fur", 0)))
    parts.append(Part(neck, "fur", z=2.5, region=neck_reg, inner=("fur", 0)))
    if mane_part:
        parts.append(mane_part)
    head_part = Part(head, "fur", z=3, flat=0.5, region=head_reg, inner=("fur", 0))
    parts += [head_part, Part(near_ear, "fur", z=3.2, region=ear_reg, inner=("fur", 0))]
    parts += [hp_ for hp_, _ in horn_parts]

    eye = p["eye"]
    ec = fwd((eye["dx"] * cr, eye["dy"] * cr))
    tip = hinfo["tip"]
    mt = hd["mt"]

    def details(cv):
        big = cv.big
        if ear["inner"] and big:
            paint(cv, inner_ear, ("pale", 0), owner_part=parts.index(next(q for q in parts if q.shape is near_ear)))
        if big and p["fur_dashes"]:
            rows, diag = p["fur_dashes"]
            fur = set(cv.pal.index["fur"][1:])
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in fur and py % rows == 0 and (px + py) % diag == 0:
                        cv.shade(px, py, -1)
        # horn annulations: darker bands across the horn
        if big:
            for hp_, hs in horn_parts:
                if not hs.get("rings"):
                    continue
                pi = parts.index(hp_)
                n = hs["rings"]
                for py in range(cv.h):
                    for px in range(cv.w):
                        if cv.owner[py][px] == pi and cv.idx[py][px]:
                            f = hp_.shape.frac(*cv.to_model(px + 0.5, py + 0.5))
                            if (f * n) % 1 < 0.34 and f > 0.08:
                                cv.shade(px, py, -1)
        # cloven hooves: a split line
        if big and lg["foot"] == "cloven":
            for lg_ in L4:
                h_ = lg_["hoof"]
                a = ((h_[0][0] + h_[1][0]) / 2, (h_[0][1] + h_[1][1]) / 2 + 0.4)
                b = ((h_[2][0] + h_[3][0]) / 2 - 0.2, (h_[2][1] + h_[3][1]) / 2 - 0.2)
                cv.line(a, b, ("hoof", 0) if len(cv.pal.index["hoof"]) > 1 else "outline")
        # nostril, mouth
        if p["nose"]:
            nx, ny = p["nose"]
            n = fwd((tip[0] - mt / 2 + nx, tip[1] + ny))
            cv.set(*cv.pt(*n), ("dark", 0))
            if big and mt > 3.0:
                n2 = fwd((tip[0] - mt / 2 + nx + 0.7, tip[1] + ny - 0.3))
                cv.set(*cv.pt(*n2), ("dark", 0))
        if big and p["mouth"]:
            a = fwd((tip[0] - mt / 2 + 0.5, tip[1] + mt * 0.3))
            b = fwd((tip[0] - mt / 2 + p["mouth"], tip[1] + mt * 0.36))
            cv.line(a, b, ("dark", 0))
        # eye
        r_ = eye["r"]
        if big:
            if eye.get("ring"):
                cv.disc(ec, r_ + 0.75, eye["ring"], only_opaque=True)
            cv.disc(ec, r_, "outline", only_opaque=True)
            px, py = cv.pt(*ec)
            fwdx = 1 if cv.flip else -1
            cv.set(px + fwdx, py - 1, "white" if "white" in cv.pal.index else ("pale", -1))
        else:
            cv.disc(ec, max(0.6, r_ * 0.6), "outline", only_opaque=True)

    return Model(parts, p["ramps"], details)


def lerp_pt(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


# ---------------------------------------------------------------------------
# overworld end-on views


def overworld(p, view, step):
    """South: the long face over the chest, ears and horns on top, forelegs in
    front, hind legs at the sides. North: rump and tail, hind legs, the neck
    and the back of the head above. Sizes in U = cranium radius x
    ow_end["head"]. ow_end keys: head, body (half width factor), legs (visible
    leg length factor), neck (head height above the chest, U), face (face
    length, U), muzzle (muzzle width factor), ear, tail (hanging tail length,
    U, north view), horn (scale of end-view horns)."""
    hd, lg, ear, eye = p["head"], p["leg"], p["ear"], p["eye"]
    o = {**dict(head=1.8, body=1.0, legs=1.0, neck=1.0, face=1.0, muzzle=1.0, ear=1.0, tail=1.0, horn=1.0),
         **p["ow_end"]}
    R = p.get("ow_ramps", {})
    cr = hd["cr"]
    U = cr * o["head"]
    b = p["body"]
    depth = b["chest"] / cr
    bw = U * (0.75 + 0.14 * depth) * o["body"]
    legv = lg["h"] * o["head"] * 0.5 * o["legs"]
    far = dict(light=-0.28)
    lift = (0.3 * U, 0.0) if step else (0.0, 0.0)
    fr = max(0.55, lg["fr"][2]) * o["head"] * 0.55
    hr = max(0.55, lg["hr"][2]) * o["head"] * 0.55
    hoof_w, hoof_h = fr * 1.25, max(0.6, lg["hoof"][1] * o["head"] * 0.3)
    hy = 0.0
    cy = hy + U * (0.9 + 0.7 * o["neck"])
    G = cy + U * 0.55 + legv
    leg_r, hoof_r = R.get("legs", "fur"), R.get("hoof", "hoof")
    lower_r = R.get("lower")
    sock = next((m for m in p["marks"] if m["kind"] == "socks" and m["on"] == "legs"), None)
    if lower_r is None and sock is not None:
        lower_r = sock["ramp"]
    pad = lg["foot"] == "pad"

    sock_h = sock["h"] if sock else 0

    def leg_reg(x, y):
        if lower_r and y > G - legv * (0.18 + 0.045 * sock_h):
            return lower_r
        return leg_r
    parts = []
    eh, ew = U * ear["h"] / cr * 0.62 * o["ear"], U * ear["w"] / cr * 0.5 * o["ear"]

    def ears(hcy, z, light=0.0, spread=0.62):
        out = []
        for s in (-1, 1):
            bx, by = s * U * spread, hcy - U * 0.5
            a = math.radians(s * (30 + ear["lean"] * 0.4))
            tip = (bx + eh * math.sin(a), by - eh * math.cos(a))
            shp = Facet([(bx - ew * 0.55, by + U * 0.15), tip, (bx + ew * 0.55, by + U * 0.15)])
            out.append((Part(shp, R.get("ear", "fur"), z=z, light=light, inner=("fur", 0)), shp, (bx, by), tip))
        return out

    def horns(hcy, z, light=0.0):
        out = []
        hs = o["horn"] * U / cr
        for hspec in p["horns"]:
            hr_ = hspec.get("ramp", "horn")
            for s in (-1, 1):
                if hspec.get("kind") == "curl":   # a thick C each side: up and out, down by the cheek, tip forward
                    c = [(0.22, -0.72), (0.7, -0.92), (1.12, -0.7), (1.3, -0.25), (1.18, 0.2), (0.92, 0.4),
                         (0.78, 0.18)]
                    t0, t1 = hspec["thick"]
                    k_ = o["horn"] * U / 1.8 / cr
                    pts = [(s * x * U * o["horn"], hcy + y * U * o["horn"]) for x, y in c]
                    rad = [lerp(t0, t1, i / (len(c) - 1)) * k_ * 1.1 for i in range(len(c))]
                else:
                    ep = hspec.get("end", [(0, 0), (0, -4)])
                    er = hspec.get("end_r", hspec["r"][:len(ep)])
                    bx = s * U * hspec.get("spread", 0.4)
                    pts = [(bx + s * u * hs, hcy - U * 0.6 + v * hs) for u, v in ep]
                    rad = [v * hs * 0.8 for v in er]
                shp = Path(pts, rad)
                out.append((Part(shp, hr_, z=z, light=light, inner=(hr_, 0)), hspec, shp))
        return out

    def hoof_parts(x, fy, z, extra):
        if pad:
            return [Part(Ellipse(x, fy + hoof_h * 0.3, hoof_w * 1.3, hoof_h * 0.8), leg_r, z=z, **extra)]
        return [Part(Ellipse(x, fy + hoof_h * 0.2, hoof_w, hoof_h * 0.9), hoof_r, z=z, flat=0.8, **extra)]

    if view == "south":
        for k, s in enumerate((-1, 1)):  # hind legs seen between the forelegs, farther away
            x = s * bw * 0.22
            fy = G - hoof_h - U * 0.3 - lift[1 - k] * 0.6
            parts.append(Part(Tube([(x, cy + U * 0.2), (x, fy)], [hr * 1.2, hr * 0.9]), leg_r, z=-1,
                              region=leg_reg, light=-0.38))
            parts += hoof_parts(x, fy, -0.9, dict(light=-0.38))
        body_r = R.get("body", "fur")
        chest_r = R.get("chest", "fur")
        parts.append(Part(Ellipse(0, cy, bw, U * 0.75), body_r, z=0,
                          region=lambda x, y: chest_r if abs(x) < bw * 0.4 and y > cy - U * 0.1 else body_r))
        for k, s in enumerate((-1, 1)):
            x = s * bw * 0.6
            fy = G - hoof_h - lift[k]
            parts.append(Part(Ellipse(x, cy + U * 0.05, bw * 0.42, U * 0.6), body_r, z=1.5, inner=("fur", 0)))
            parts.append(Part(Tube([(x, cy + U * 0.3), (x - s * U * 0.04, cy + U * 0.85), (x, fy)],
                                   [fr * 1.7, fr * 1.25, fr]),
                              leg_r, z=2, region=leg_reg, inner=("fur", 0)))
            parts += hoof_parts(x, fy, 2.1, dict(inner=("fur", 0)))
        # neck (a column between chest and head; shows for long necks)
        parts.append(Part(Tube([(0, cy - U * 0.2), (0, hy + U * 0.4)], [U * 0.62, U * 0.55]), "fur", z=0.5,
                          inner=("fur", 0),
                          region=lambda x, y: R.get("throat", "pale") if abs(x) < U * 0.28 else "fur"))
        eparts = ears(hy, 2.6)
        hparts = horns(hy, 3.4)
        parts += [e[0] for e in eparts] + [h[0] for h in hparts]
        fl = U * 0.26 * hd["ml"] / cr * o["face"]
        cran = Ellipse(0, hy, U * 0.78, U * 0.7)
        face_ = Ellipse(0, hy + fl * 0.75, U * 0.5 * o["muzzle"], fl * 0.9)
        mcy = hy + fl * 1.45
        mrx, mry = U * 0.46 * o["muzzle"], U * 0.34
        face_r = R.get("face", "fur")
        head_u = Union([cran, face_], k=0.15)
        parts.append(Part(head_u, "fur", z=3, inner=("fur", 0), region=lambda x, y: face_r if y > hy else "fur"))
        if p["mane"] and p["mane"].get("up"):
            parts.append(Part(Ellipse(0, hy - U * 0.72, U * 0.22, U * 0.3), p["mane"].get("ramp", "mane"),
                              z=3.05, inner=("fur", 0)))
        parts.append(Part(Ellipse(0, mcy, mrx, mry), R.get("muzzle", "pale"), z=3.3, inner=("fur", 0)))

        def details(cv):
            for prt, shp, (bx, by), tip in eparts:
                if ear["inner"]:
                    inner = Facet([(bx - ew * 0.25, by + U * 0.1), (tip[0] * 0.8 + bx * 0.2, tip[1] + eh * 0.3),
                                   (bx + ew * 0.25, by + U * 0.1)])
                    paint(cv, inner, ("pale", 0), owner_part=parts.index(prt))
            for s in (-1, 1):  # eyes on the sides of the head
                px, py = cv.pt(s * U * 0.62, hy + U * 0.12)
                cv.set(px, py, "outline")
                cv.set(px, py + 1, "outline")
                if eye.get("ring"):
                    cv.set(px + (1 if s < 0 else -1), py, eye["ring"])
            for s in (-1, 1):  # nostrils
                nx, ny = cv.pt(s * mrx * 0.45, mcy - mry * 0.1)
                cv.set(nx, ny, ("dark", 0))
            for fx, fy, c in p.get("ow_face", []):
                cv.set(*cv.pt(fx * U, hy + fy * U), c)
        return Model(parts, p["ramps"], details)

    # north: from behind
    hcy = hy
    rump_r = R.get("rump", "fur")
    rump_w = U * R.get("rump_w", 0.5) if "rump" in R else 0
    parts.append(Part(Ellipse(0, cy, bw * 1.05, U * 0.8), "fur", z=0,
                      region=lambda x, y: rump_r if rump_w and abs(x) < rump_w and y > cy - U * 0.5 else "fur"))
    for k, s in enumerate((-1, 1)):  # forelegs seen between the hind legs, farther away
        x = s * bw * 0.22
        fy = G - hoof_h - U * 0.3 - lift[1 - k] * 0.6
        parts.append(Part(Tube([(x, cy + U * 0.3), (x, fy)], [fr * 1.2, fr * 0.9]), leg_r, z=-1,
                          region=leg_reg, light=-0.38))
        parts += hoof_parts(x, fy, -0.9, dict(light=-0.38))
    for k, s in enumerate((-1, 1)):
        x = s * bw * 0.6
        fy = G - hoof_h - lift[k]
        parts.append(Part(Ellipse(x, cy + U * 0.15, bw * 0.45, U * 0.68), "fur", z=0.5, inner=("fur", 0),
                          region=lambda x, y: rump_r if rump_w and abs(x) < rump_w and y > cy - U * 0.5 else "fur"))
        parts.append(Part(Tube([(x, cy + U * 0.45), (x + s * U * 0.06, G - legv * 0.55), (x, fy)],
                               [hr * 1.8, hr * 1.1, hr]), leg_r, z=1, region=leg_reg, inner=("fur", 0)))
        parts += hoof_parts(x, fy, 1.1, dict(inner=("fur", 0)))
    parts.append(Part(Tube([(0, cy - U * 0.3), (0, hcy + U * 0.3)], [U * 0.6, U * 0.5]), "fur", z=-0.6,
                      light=-0.05))
    if p["mane"]:
        parts.append(Part(Tube([(0, cy - U * 0.45), (0, hcy - U * 0.2)], [U * 0.2, U * 0.24]),
                          p["mane"].get("ramp", "mane"), z=-0.55, inner=("fur", 0)))
    parts.append(Part(Ellipse(0, hcy, U * 0.74, U * 0.66), "fur", z=-0.5, light=-0.05))
    parts += [e[0] for e in ears(hcy, -0.4, light=-0.1)]
    parts += [h[0] for h in horns(hcy, -0.3, light=-0.1)]
    t = p["tail"]
    sway = U * (0.15 if step else -0.1)
    k = o["head"] * 0.55
    r0, rm, rt = (v * k for v in t["r"])
    tl = min(t["len"] * k * o["tail"], G - cy - U * 0.2)
    tpts = [(0, cy - U * 0.35), (sway * 0.3, cy + tl * 0.3), (sway * 0.8, cy + tl * 0.65), (sway * 1.2, cy + tl)]
    tail = Path(tpts, [r0, rm, (rm + rt) / 2, rt])
    tail_marks = [m for m in p["marks"] if m["kind"] in ("tip", "rings")]

    def tail_reg(x, y):
        for m in tail_marks:
            if _mark(m, "tail", x, y, dict(tail_frac=tail.frac)):
                return m["ramp"]
        return R.get("tail", "fur")
    parts.append(Part(tail, "fur", z=2, region=tail_reg, inner=("fur", 0)))
    return Model(parts, p["ramps"])


PLAN = BodyPlan(
    "equid", "horses, from dawn horses to Equus: toe count, muzzle length and mane change along the line",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_HORSE, tracks="TRACKS_FOOT",
)
