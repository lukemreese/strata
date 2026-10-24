"""canid body plan: dogs and foxes (the dog starter lines), plus the shared
quadruped-carnivore engine that plans/carnivoran.py reuses.

Species (taxonomy.py):
    hesperocyon   Hesperocyon (White River Gp, SD/NE, 2 kg)
    leptocyon     Leptocyon (Ogallala Gp, NE, 2 kg)
    epicyon       Epicyon (Ogallala Gp, NE, 120 kg)
    aenocyon      Aenocyon dirus (Natural Trap Cave, WY, 65 kg)
    canis         Canis latrans (Living; WY, 13 kg)
    vulpes        Vulpes velox (Living; MT, 2.2 kg)

The dog line runs Cimolestes -> Protictis -> Miacis -> Hesperocyon -> Leptocyon
(-> Canis, Aenocyon, Vulpes) and Hesperocyon -> Epicyon. Protictis and Miacis
live in the carnivoran plan but are drawn with this engine and the same family
marks, so the line reads as one lineage: pointed ears with dark backs, a pale
muzzle, throat and chest, a dark streak from the eye's front corner, dark lower
legs and a dark tail tip; forest spots and tail rings fade out from Protictis to
Hesperocyon, and the open-country dogs are plain.

The engine (`side`, `overworld`) builds a quadruped from proportions instead of
hand-placed ellipses, so one set of numbers per species gives all views.
Model units are sprite pixels at scale 1, head to the LEFT, y down.

Spec keys (every length in model px; see DEFAULTS for the full set):
    body   L (shoulder-to-hip distance), top_s / top_h (back height at the
           shoulder / hip), chest / waist / hip (depths), sag (back dip),
           chest_w / rump_w (ellipse width factors), hump (withers ellipse
           (dx, dy, rx, ry) relative to the shoulder top, or None)
    leg    h (chest bottom to ground), fr / hr (fore / hind radii: upper, lower,
           wrist), digi (0 plantigrade .. 1 digitigrade), paw (length, radius),
           thigh (size factor of the near haunch), arm (near shoulder muscle factor),
           far (fore dx, hind dx of the far legs), stride (walk swing, degrees)
    neck   r0, r1 (radii at the body and the head), base (dx, dy from the shoulder top)
    head   dx, dy (cranium centre from the shoulder top), cr (cranium radius),
           cw (cranium width factor), ml / md (muzzle length / depth), mdrop,
           mtilt, jd (lower-jaw depth), cheek (zygomatic/jaw-muscle factor), stop
    ear    kind point|round, h, w, lean (deg back), dx, dy, inner (pale inner fur)
    tail   len, a0 (deg below horizontal at the root), bend (deg per segment),
           r (root, widest, tip), widest (fraction), dy (root height offset)
    eye    dx, dy (from the cranium centre), r, iris (ramp or None), line (tear
           streak to the muzzle: ((dx, dy), (dx, dy)) or None), mask (ramp)
    marks  list of colour rules, first match wins (see _mark)
    action phase-2 pose: tilt (head deg, + raises the snout), gape (jaw deg),
           tail (deg added to the tail angles), ear (deg)
    teeth  canine (gape only), sabre (length, x frac along the muzzle), flange
    claws  paint pale claws on the near paws (bears)
    whiskers  list of whisker strokes (head-relative) drawn over the outline

Ramps the engine uses: outline (1), fur (3-4), pale (2-3), dark (1-2), skin
(1-2: nose leather, mouth), white (1), optional eye (1) and any extra coat ramp
named in `marks`.
"""

import math

from ..core.geom import Ellipse, Tube, Union, Part, Model, turn, lerp, clamp
from ..core.plan import BodyPlan

FOOTPRINT_CANID = [
    "................",
    "................",
    "................",
    "......#..#......",
    ".....##..##.....",
    "...#........#...",
    "...##......##...",
    "......####......",
    ".....######.....",
    ".....######.....",
    "......####......",
    "................",
    "................",
    "................",
    "................",
    "................",
]


class Facet:
    """A convex polygon with a central ridge (ears, sabres, claws): q is the
    distance to the nearest edge over the inradius, so it shades like a
    low pyramid instead of a flat plate."""
    def __init__(self, pts):
        self.p = pts
        area = sum(ax * by - bx * ay for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]))
        sgn = 1 if area > 0 else -1
        self.edges = []
        for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
            dx, dy = bx - ax, by - ay
            ln = math.hypot(dx, dy) or 1
            self.edges.append((ax, ay, -dy / ln * sgn, dx / ln * sgn))
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        self.r = max(0.3, min((cx - ax) * nx + (cy - ay) * ny for ax, ay, nx, ny in self.edges))
        self.bbox = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

    def q(self, x, y):
        return min((x - ax) * nx + (y - ay) * ny for ax, ay, nx, ny in self.edges) / self.r


class Turned:
    """Any shape rotated by deg about pivot (turn() convention)."""
    def __init__(self, shape, pivot, deg):
        self.s, self.pv, self.deg = shape, pivot, deg
        x0, y0, x1, y1 = shape.bbox
        cs = [turn(c, pivot, deg) for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
        self.bbox = (min(c[0] for c in cs), min(c[1] for c in cs), max(c[0] for c in cs), max(c[1] for c in cs))

    def q(self, x, y):
        if not self.deg:
            return self.s.q(x, y)
        return self.s.q(*turn((x, y), self.pv, -self.deg))


class Path:
    """A Tube that also knows how far along it a point lies (tail tips, rings)."""
    def __init__(self, pts, radii):
        self.tube = Tube(pts, radii)
        self.p = pts
        self.bbox = self.tube.bbox
        segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
        self.total = sum(segs) or 1
        self.cum = [0]
        for s in segs:
            self.cum.append(self.cum[-1] + s)

    def q(self, x, y):
        return self.tube.q(x, y)

    def frac(self, x, y):
        best, f = 1e9, 0.0
        for k, (a, b) in enumerate(zip(self.p, self.p[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ll = dx * dx + dy * dy
            t = clamp(((x - a[0]) * dx + (y - a[1]) * dy) / ll, 0, 1) if ll else 0
            d = math.hypot(x - a[0] - dx * t, y - a[1] - dy * t)
            if d < best:
                best, f = d, (self.cum[k] + t * (self.cum[k + 1] - self.cum[k])) / self.total
        return f


DEFAULTS = dict(
    front=0.95, back=1.05, icon=0.5,
    body=dict(L=22.0, top_s=-7.0, top_h=-7.0, chest=11.0, waist=8.5, hip=9.5, sag=0.5,
              chest_w=1.0, rump_w=1.0, hump=None, k=0.14),
    leg=dict(h=8.0, fr=(2.4, 1.6, 1.3), hr=(2.4, 1.7, 1.3), digi=1.0, paw=(3.6, 1.3),
             thigh=1.0, arm=0.0, far=(3.0, -2.5), stride=18.0, elbow=0.6, knee=3.0, hock=2.0),
    neck=dict(r0=4.0, r1=3.2, base=(1.5, 3.5)),
    head=dict(dx=-9.0, dy=-3.0, cr=4.6, cw=1.0, ml=6.0, md=4.0, mdrop=0.6, mtilt=4.0, jd=2.2,
              cheek=0.0, stop=0.0, k=0.12),
    ear=dict(kind="point", h=5.0, w=4.0, lean=12.0, dx=1.0, dy=0.0, inner=True, tip=None),
    tail=dict(len=22.0, a0=40.0, bend=-6.0, r=(1.8, 2.6, 1.0), widest=0.5, dy=1.0),
    eye=dict(dx=-2.4, dy=-0.8, r=1.25, iris=None, line=None),
    marks=[],
    belly=None, throat=None,     # override the countershading lines (see _countershade)
    action=dict(tilt=5.0, gape=-16.0, tail=-14.0, ear=0.0),
    teeth=dict(canine=1.6, sabre=None, flange=None),
    claws=False, whiskers=None, fur_dashes=(3, 5), nostril=True,
    ow=dict(tracks="TRACKS_FOOT"),
    ow_end={},
)


# ---------------------------------------------------------------------------
# geometry


def rig(p):
    """Key points and shapes in rest pose, derived from the proportions."""
    b, lg, hd, nk = p["body"], p["leg"], p["head"], p["neck"]
    L = b["L"]
    xs, xh = -L / 2, L / 2
    ts, th = b["top_s"], b["top_h"]
    ch, wa, hp = b["chest"], b["waist"], b["hip"]
    G = ts + ch + lg["h"]
    r = dict(L=L, xs=xs, xh=xh, ts=ts, th=th, ch=ch, wa=wa, hp=hp, G=G)
    r["torso"] = [
        (xs + 1.0, ts + ch / 2, ch * 0.62 * b["chest_w"], ch / 2, -6),
        (0.0, (ts + th) / 2 + b["sag"] + wa / 2, L * 0.42, wa / 2, 0),
        (xh - 0.5, th + hp / 2, hp * 0.58 * b["rump_w"], hp / 2, 8),
    ]
    if b["hump"]:
        dx, dy, rx, ry = b["hump"]
        r["torso"].append((xs + dx, ts + dy, rx, ry, -10))
    # head (cranium centre) and neck
    hx, hy = xs + hd["dx"], ts + hd["dy"]
    r["hx"], r["hy"] = hx, hy
    r["neck"] = ((xs + nk["base"][0], ts + nk["base"][1]), (hx + hd["cr"] * 0.35, hy + hd["cr"] * 0.35))
    r["pivot"] = r["neck"][1]
    return r


def head_shapes(p, r):
    """Unrotated head shapes, relative to nothing (absolute rest coordinates)."""
    hd = p["head"]
    hx, hy, cr = r["hx"], r["hy"], hd["cr"]
    ml, md = hd["ml"], hd["md"]
    # the muzzle is a tapered tube from its root (under the eye) to the nose
    root = (hx - cr * 0.45, hy + cr * 0.22 + hd["mdrop"] * 0.3)
    a = math.radians(hd["mtilt"])
    reach = ml + cr * 0.45
    tipc = (root[0] - reach * math.cos(a), root[1] + reach * math.sin(a) + hd["mdrop"])
    taper = hd.get("taper", 0.72)
    cran = (hx, hy, cr * hd["cw"], cr * 0.86, 0)
    shapes = [Ellipse(*cran), Tube([root, tipc], [md * 0.62, md * 0.5 * taper / 0.72])]
    if hd["stop"]:  # forehead bulge between eyes and muzzle
        shapes.append(Ellipse(hx - cr * 0.55, hy - cr * 0.2, cr * 0.6, cr * 0.5 * hd["stop"], -15))
    if hd["cheek"]:
        shapes.append(Ellipse(hx - cr * 0.1, hy + cr * 0.45, cr * 0.8 * hd["cheek"], cr * 0.6 * hd["cheek"], -8))
    tip_r = md * 0.5 * taper / 0.72
    tip_x = tipc[0] - tip_r
    mouth_y = tipc[1] + tip_r * 0.75
    hinge = (hx + cr * 0.1, hy + cr * 0.55)
    jd = hd["jd"]
    chin = (tip_x + 1.4 + jd * 0.2, mouth_y + jd * 0.3)
    return dict(cran=cran, shapes=shapes, tip=(tip_x, tipc[1] - tip_r * 0.3), mouth_y=mouth_y,
                hinge=hinge, chin=chin, jd=jd, root=root, tipc=tipc)


def legs(p, r, step, phase):
    """Four legs (far fore, far hind, near hind, near fore) as dicts with the
    tube points, radii and paw ellipse, posed for the walk step."""
    lg = p["leg"]
    G, xs, xh, ts, th, ch, hp = r["G"], r["xs"], r["xh"], r["ts"], r["th"], r["ch"], r["hp"]
    digi = lg["digi"]
    pl, pr = lg["paw"]
    out = []
    for near in (False, True):
        for fore in (True, False):
            if fore:
                x0 = xs + 1.5 + (0 if near else lg["far"][0])
                top = (x0, ts + ch * 0.45)
                elbow = (x0 + lg["elbow"], ts + ch - 0.8)
                wh = pr + digi * lg["h"] * 0.20 + 0.5
                wrist = (x0 - 0.2, G - wh)
                paw = (wrist[0] - pl * 0.35 - (1 - digi) * pl * 0.2, G - pr)
                pts, radii = [top, elbow, wrist], list(lg["fr"])
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
            if step:
                # diagonal pairs: near fore + far hind forward, the others back
                sgn = 1 if (near == fore) else -1
                swing = lg["stride"] * sgn
            if swing:
                piv = pts[0]
                pts = [pts[0]] + [turn(q, piv, swing) for q in pts[1:]]
                pc = turn(paw, piv, swing)
                lift = max(0.0, (pc[1] + pr) - G)  # keep paws on the ground
                pts = [pts[0]] + [(x, y - lift * (k / 3)) for k, (x, y) in enumerate(pts[1:], 1)]
                paw = (pc[0], pc[1] - lift)
            out.append(dict(near=near, fore=fore, pts=pts, radii=radii,
                            paw=(paw[0], paw[1], pl / 2, pr, 0)))
    return out


def tail_points(p, r, extra=0.0):
    t = p["tail"]
    x, y = r["xh"] + r["hp"] * 0.3, r["th"] + 1.6 + t["dy"]
    seg = t["len"] / 5
    pts = [(x, y)]
    a = t["a0"] + extra
    for k in range(5):
        x += seg * math.cos(math.radians(a))
        y += seg * math.sin(math.radians(a))
        pts.append((x, y))
        a += t["bend"] + extra * 0.15
    r0, rm, rt = t["r"]
    w = t["widest"]
    radii = []
    for k in range(6):
        f = k / 5
        radii.append(lerp(r0, rm, f / w) if f <= w else lerp(rm, rt, (f - w) / (1 - w)))
    return pts, radii


# ---------------------------------------------------------------------------
# colour rules


def _mark(m, group, x, y, ctx):
    """True if mark m colours point (x, y) of a part in `group`.
    Mark kinds (m["kind"]), coordinates as noted:
        ell      (cx, cy, rx, ry[, deg]); head marks are relative to the cranium
                 centre in head space, other groups absolute
        below    (x0, y0, slope): y > y0 + slope*(x - x0) (head marks head-relative)
        above    same, y < line
        spots    step (sx, sy), r, below (y limit, absolute) / above: lattice spots
        stripes  period, width, x0, x1, lean: vertical bands
        rings    list of (f0, f1) tail fractions
        tip      f: tail fraction beyond f
        socks    h: legs below G - h (fore/hind via m["legs"] = "fore"|"hind"|"all")
        front    legs: a stripe down the front of the near forelegs (w)
    m["on"]: a group name or a tuple of group names (head, jaw, neck, torso,
    legs, tail, ear, all)."""
    on = m["on"]
    if on != "all" and group != on and (not isinstance(on, tuple) or group not in on):
        return False
    k = m["kind"]
    # generic filters: an x range, and (torso) only above the pale belly line
    if "x" in m and k not in ("spots", "stripes") and not (m["x"][0] <= x <= m["x"][1]):
        return False
    if "above" in m and k not in ("spots", "stripes") and group == "torso" and y > ctx["belly"](x) + m["above"]:
        return False
    if k == "ell":
        cx, cy, rx, ry = m["e"][:4]
        deg = m["e"][4] if len(m["e"]) > 4 else 0
        u, v = x - cx, y - cy
        if deg:
            a = math.radians(-deg)
            u, v = u * math.cos(a) - v * math.sin(a), u * math.sin(a) + v * math.cos(a)
        return (u / rx) ** 2 + (v / ry) ** 2 <= 1
    if k in ("below", "above"):
        x0, y0, s = m["line"]
        yl = y0 + s * (x - x0)
        hit = y > yl if k == "below" else y < yl
        if hit and "x" in m:
            hit = m["x"][0] <= x <= m["x"][1]
        return hit
    if k == "spots":
        sx, sy = m["step"]
        if "below" in m and y < m["below"]:
            return False
        if "above" in m and y > ctx["belly"](x) + m["above"]:
            return False
        if "x" in m and not (m["x"][0] <= x <= m["x"][1]):
            return False
        row = math.floor(y / sy)
        off = (row % 2) * sx / 2
        cx = math.floor((x - off) / sx) * sx + off + sx / 2
        cy = row * sy + sy / 2
        return (x - cx) ** 2 + ((y - cy) * m.get("squash", 1.0)) ** 2 <= m["r"] ** 2
    if k == "stripes":
        if not (m["x"][0] <= x <= m["x"][1]):
            return False
        if "above" in m and y > ctx["belly"](x) + m["above"]:
            return False
        ph = (x + m.get("lean", 0) * y) % m["period"]
        return ph < m["width"]
    if k in ("rings", "tip"):
        f = ctx.get("tail_frac")
        if f is None:
            return False
        f = f(x, y)
        if k == "tip":
            return f >= m["f"]
        return any(a <= f < b for a, b in m["bands"])
    if k == "socks":
        which = m.get("legs", "all")
        if which != "all" and ctx.get("leg") != which:
            return False
        return y > ctx["G"] - m["h"]
    return False


def _countershade(p, r):
    """Default pale underside: below a line from the chest to the flank."""
    if p["belly"]:
        a, s = p["belly"]
        return lambda x: a + s * x
    y0 = r["ts"] + r["ch"] * 0.74
    y1 = r["th"] + r["hp"] * 0.9
    return lambda x: lerp(y0, y1, clamp((x - r["xs"]) / (r["xh"] - r["xs"]), 0, 1))


# ---------------------------------------------------------------------------
# side view


def side(p, phase=0, step=None):
    if step is not None:
        phase = 0
    act = p["action"] if phase else dict(tilt=0.0, gape=0.0, tail=0.0, ear=0.0)
    r = rig(p)
    hd = p["head"]
    hs = head_shapes(p, r)
    pivot = r["pivot"]
    tilt = act.get("tilt", 0.0)
    H = lambda pt: turn(pt, pivot, tilt)  # noqa: E731
    Hinv = lambda x, y: turn((x, y), pivot, -tilt)  # noqa: E731
    hx, hy = r["hx"], r["hy"]
    marks = p["marks"]
    belly = _countershade(p, r)
    far = dict(light=-0.28)

    def ctx(**kw):
        c = dict(G=r["G"], belly=belly)
        c.update(kw)
        return c

    def region(group, default, local=None, **kw):
        c = ctx(**kw)

        def f(x, y):
            lx, ly = local(x, y) if local else (x, y)
            for m in marks:
                if _mark(m, group, lx, ly, c):
                    return m["ramp"]
            return default(lx, ly)
        return f

    # torso
    torso = Union([Ellipse(*e) for e in r["torso"]], k=p["body"]["k"])
    torso_reg = region("torso", lambda x, y: "pale" if y > belly(x) else "fur")
    # neck: throat pale
    (n0, n1) = r["neck"]
    n1r = H(n1)
    neck = Tube([n0, n1r], [p["neck"]["r0"], p["neck"]["r1"]])
    if p["throat"]:
        ta, tsl = p["throat"]
    else:
        ta, tsl = None, None

    def neck_default(x, y):
        # pale below the line from the jaw hinge to the chest front
        ax, ay = hs["hinge"][0], hs["hinge"][1] + 0.6
        bx, by = r["xs"] - 1.0, belly(r["xs"]) - 0.5
        if ta is not None:
            return "pale" if y > ta + tsl * x else "fur"
        t = clamp((x - ax) / ((bx - ax) or 1), 0, 1)
        return "pale" if y > lerp(ay, by, t) else "fur"
    neck_reg = region("neck", neck_default, local=None)

    # head (rotated by tilt about the neck pivot); head-relative coordinates for marks
    def head_local(x, y):
        u, v = Hinv(x, y)
        return u - hx, v - hy

    mouth_rel = hs["mouth_y"] - hy
    jaw_rel_slope = 0.12

    def head_default(u, v):
        # muzzle sides and lips pale below a line from the muzzle top to below the eye
        cr = hd["cr"]
        tipx = hs["tip"][0] - hx
        y_line = lerp(mouth_rel - hd["md"] * 0.45, cr * 0.5, clamp((u - tipx) / (cr * 0.8 - tipx), 0, 1))
        return "pale" if v > y_line else "fur"
    head_reg = region("head", head_default, local=head_local)
    head = Turned(Union(hs["shapes"], k=hd["k"]), pivot, tilt)

    # lower jaw, opened about the hinge
    gape = act.get("gape", 0.0)
    hinge = hs["hinge"]
    J = lambda pt: H(turn(pt, hinge, gape))  # noqa: E731
    jd = hs["jd"]
    jaw_pts = [J((hinge[0] - 0.5, hinge[1] + 0.2)), J(((hinge[0] + hs["chin"][0]) / 2, hs["mouth_y"] + jd * 0.45)),
               J(hs["chin"])]
    jaw = Tube(jaw_pts, [jd * 0.75, jd * 0.62, jd * 0.48])
    jaw_reg = region("jaw", lambda x, y: "pale", local=head_local)

    # ears
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

    # tail
    tpts, trad = tail_points(p, r, act.get("tail", 0.0))
    tail = Path(tpts, trad)
    tail_reg = region("tail", lambda x, y: "fur", tail_frac=tail.frac)

    # legs
    L4 = legs(p, r, step, phase)
    parts = [Part(tail, "fur", z=-3, region=tail_reg, inner=("fur", 0)),
             Part(far_ear, "fur", z=-0.5, region=ear_reg, **far)]
    for lg_ in L4:
        if not lg_["near"]:
            reg = region("legs", lambda x, y: "fur", leg="fore" if lg_["fore"] else "hind")
            parts += [Part(Tube(lg_["pts"], lg_["radii"]), "fur", z=-2, region=reg, **far),
                      Part(Ellipse(*lg_["paw"]), "fur", z=-1.9, region=reg, **far)]
    parts.append(Part(torso, "fur", z=0, flat=0.55, region=torso_reg))
    lg = p["leg"]
    for lg_ in L4:
        if lg_["near"]:
            reg = region("legs", lambda x, y: "fur", leg="fore" if lg_["fore"] else "hind")
            z = 2 if lg_["fore"] else 1.5
            parts += [Part(Tube(lg_["pts"], lg_["radii"]), "fur", z=z, region=reg, inner=("fur", 0)),
                      Part(Ellipse(*lg_["paw"]), "fur", z=z + 0.1, region=reg, inner=("fur", 0))]
            if not lg_["fore"] and lg["thigh"]:
                (x0, y0), (x1, y1) = lg_["pts"][0], lg_["pts"][1]
                s = lg["thigh"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.6, (y0 + y1) / 2 - 0.6, r["hp"] * 0.42 * s,
                                          r["hp"] * 0.55 * s, 25), "fur", z=1.6, region=torso_reg,
                                  inner=("fur", 0)))
            if lg_["fore"] and lg["arm"]:
                (x0, y0), (x1, y1) = lg_["pts"][0], lg_["pts"][1]
                s = lg["arm"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.3, (y0 + y1) / 2 - 0.4, r["ch"] * 0.3 * s,
                                          r["ch"] * 0.42 * s, -10), "fur", z=2.05, region=torso_reg,
                                  inner=("fur", 0)))
    parts += [Part(neck, "fur", z=2.5, region=neck_reg, inner=("fur", 0)),
              Part(jaw, "pale", z=2.9, region=jaw_reg, inner=("fur", 0)),
              Part(head, "fur", z=3, flat=0.5, region=head_reg, inner=("fur", 0)),
              Part(near_ear, "fur", z=3.2, region=ear_reg, inner=("fur", 0))]
    tt = p["teeth"]
    if gape:  # mouth interior, only visible in the gap
        mi = [H(hinge), H((hs["tip"][0] + 1.5, hs["mouth_y"] - 0.2)), J((hs["chin"][0] + 0.5, hs["chin"][1] - 0.6))]
        parts.append(Part(Facet(mi), "skin", z=2.8, line=False, shadow=False))
    if tt["sabre"]:
        ln, fx = tt["sabre"]
        sx = lerp(hs["tip"][0], hx, fx)
        top_y = hs["mouth_y"] - 0.8
        sab = Facet([H((sx - 0.9, top_y)), H((sx + 1.2, top_y)), H((sx + 0.2, top_y + ln * 0.6)),
                     H((sx - 0.6, top_y + ln))])
        parts.append(Part(sab, "white", z=3.05, outline="outline", inner=("fur", 0), shadow=False))
    if tt["flange"]:
        fx, fl = tt["flange"]
        cx = lerp(hs["chin"][0], hinge[0], fx)
        parts.append(Part(Ellipse(*J((cx, hs["chin"][1] + fl * 0.5)), 1.6, fl * 0.7, gape + tilt), "pale",
                          z=2.95, inner=("fur", 0)))

    eye = p["eye"]
    ec = H((hx + eye["dx"], hy + eye["dy"]))
    nose_c = H((hs["tip"][0] + 0.9, hs["tip"][1] - 0.1))

    def details(cv):
        big = cv.big
        # inner ear fur
        if inner_ear is not None and ear["inner"] and big:
            paint(cv, inner_ear, ("pale", -1), owner_part=parts.index(next(q for q in parts if q.shape is near_ear)))
        # fur dashes
        if big and p["fur_dashes"]:
            rows, diag = p["fur_dashes"]
            fur = set(cv.pal.index["fur"][1:])
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in fur and py % rows == 0 and (px + py) % diag == 0:
                        cv.shade(px, py, -1)
        # claws on near paws
        if big and p["claws"]:
            for lg_ in L4:
                if lg_["near"]:
                    x, y = lg_["paw"][0] - lg_["paw"][2], lg_["paw"][1] + lg_["paw"][3] * 0.3
                    for k in range(2):
                        cv.set(*cv.pt(x + k * 0.9, y), "white" if "claw" not in cv.pal.index else "claw")
        # tear streak from the eye's front corner towards the muzzle
        if eye["line"] and big:
            a, b = eye["line"]
            cv.line(H((hx + a[0], hy + a[1])), H((hx + b[0], hy + b[1])), eye.get("line_ramp", ("dark", 0)))
        # nose leather
        cv.disc(nose_c, 1.25 if big else 0.8, ("dark", 0), only_opaque=True)
        if big and p["nostril"]:
            px, py = cv.pt(*nose_c)
            cv.set(px, py - 1 if cv.flip else py - 1, ("dark", -1))
        # teeth in the open mouth
        if big and gape and tt["canine"]:
            ux = hs["tip"][0] + 1.6
            top = H((ux, hs["mouth_y"] + 0.1))
            cv.line(top, H((ux + 0.2, hs["mouth_y"] + tt["canine"])), "white", only_opaque=False)
            lo = J((hs["chin"][0] + 0.6, hs["chin"][1] - jd * 0.5))
            cv.line(lo, (lo[0] + 0.3, lo[1] - tt["canine"] * 0.8), "white", only_opaque=False)
        # eye
        r_ = eye["r"]
        if big:
            cv.disc(ec, r_, "outline", only_opaque=True)
            px, py = cv.pt(*ec)
            fwd = 1 if cv.flip else -1
            if eye["iris"]:  # a coloured iris behind the pupil (big cats, wolves)
                cv.set(px - fwd, py, eye["iris"])
            cv.set(px + fwd, py - 1, "white")
        else:
            cv.disc(ec, max(0.6, r_ * 0.6), "outline", only_opaque=True)

    def post(cv):
        if not cv.big or not p["whiskers"]:
            return
        for a, b in p["whiskers"]:
            for px, py in cv.pixels_on_line(H((hx + a[0], hy + a[1])), H((hx + b[0], hy + b[1]))):
                if cv.inside(px, py) and not cv.idx[py][px]:
                    cv.idx[py][px] = cv.pal.get(("pale", -1))

    return Model(parts, p["ramps"], details, post)


def paint(cv, shape, color, owner_part=None):
    """Fills the pixels whose centres lie inside `shape` (model coordinates),
    optionally only those owned by part index `owner_part`."""
    x0, y0, x1, y1 = shape.bbox
    a, b = cv.pt(x0, y0), cv.pt(x1, y1)
    for py in range(min(a[1], b[1]) - 1, max(a[1], b[1]) + 2):
        for px in range(min(a[0], b[0]) - 1, max(a[0], b[0]) + 2):
            if not cv.inside(px, py) or not cv.idx[py][px]:
                continue
            if owner_part is not None and cv.owner[py][px] != owner_part:
                continue
            if shape.q(*cv.to_model(px + 0.5, py + 0.5)) > 0:
                cv.set(px, py, color)


# ---------------------------------------------------------------------------
# overworld end-on views


def _ow_ramp(p, group):
    """The colour of a whole group in the end views: the spec's ow_ramps, else
    a mark that colours the whole group (a leg or ear colour), else fur."""
    if group in p.get("ow_ramps", {}):
        return p["ow_ramps"][group]
    for m in p["marks"]:
        if m["on"] == group and m["kind"] == "below" and m["line"][1] <= -50:
            return m["ramp"]
    return "fur"


def overworld(p, view, step):
    """South: a big face (chibi) over the chest, forelegs in front, hind feet
    at the sides. North: rump, hind legs and the tail, the back of the head and
    ears above. Sizes are in U, the end-view head radius (side cranium radius x
    ow_end["head"]); legs are shortened (chibi). `ow_end` keys: head, body
    (chest width), legs (visible leg length), muzzle, ear, hind, tail_up."""
    hd, lg, ear, eye = p["head"], p["leg"], p["ear"], p["eye"]
    o = {**dict(head=1.9, body=1.0, legs=1.0, muzzle=1.0, ear=1.0, hind=1.0), **p["ow_end"]}
    U = hd["cr"] * o["head"]
    b = p["body"]
    depth = b["chest"] / hd["cr"]          # chest depth in head radii: bulk
    legv = U * (0.35 + 0.45 * lg["h"] / b["chest"]) * o["legs"]
    bw = U * (0.42 + 0.22 * depth) * o["body"]   # half chest width
    far = dict(light=-0.28)
    lift = (0.25 * U, 0.0) if step else (0.0, 0.0)
    pr = lg["paw"][1] * o["head"] * 0.55
    fr = lg["fr"][0] * o["head"] * 0.5
    hr = lg["hr"][0] * o["head"] * 0.5
    marks = p["marks"]
    leg_ramp, ear_ramp = _ow_ramp(p, "legs"), _ow_ramp(p, "ear")
    hy = 0.0
    cy = hy + U * 1.0                       # chest / rump centre
    G = cy + U * 0.35 + legv                # ground

    def mreg(group, default, **kw):
        c = dict(G=G, belly=lambda x: 99.0)
        c.update(kw)
        socks_scale = U / hd["cr"] * 0.5

        def f(x, y):
            for m in marks:
                if m["kind"] == "socks":
                    if group == "legs" and y > G - m["h"] * socks_scale:
                        return m["ramp"]
                elif m["kind"] in ("rings", "tip") and _mark(m, group, x, y, c):
                    return m["ramp"]
            return default(x, y)
        return f
    leg_reg = mreg("legs", lambda x, y: leg_ramp)
    parts = []
    er = ear["h"] / hd["cr"]
    eh, ew = U * er * 0.8 * o["ear"], U * ear["w"] / hd["cr"] * 0.62 * o["ear"]

    def ears(hcy, z, light=0.0):
        out = []
        for s in (-1, 1):
            bx, by = s * U * 0.5, hcy - U * 0.55
            a = math.radians(s * (16 + ear["lean"] * 0.5))
            tip = (bx + eh * math.sin(a), by - eh * math.cos(a))
            if ear["kind"] == "round":
                shp = Ellipse((bx + tip[0]) / 2, (by + tip[1]) / 2 + U * 0.08, ew / 2, eh / 2 + U * 0.08, s * 20)
            else:
                shp = Facet([(bx - ew * 0.5, by + U * 0.2), tip, (bx + ew * 0.5, by + U * 0.2)])
            out.append((Part(shp, ear_ramp, z=z, light=light, inner=("fur", 0),
                             region=mreg("ear", lambda x, y: ear_ramp)), shp, (bx, by), tip))
        return out

    hind_x = (bw + hr * 0.6) * o["hind"]
    if view == "south":
        for s in (-1, 1):  # hind feet at the sides, behind
            parts.append(Part(Ellipse(s * hind_x, cy + U * 0.15, hr * 1.3, U * 0.45), "fur", z=-1, **far))
            parts.append(Part(Tube([(s * hind_x, cy + U * 0.3), (s * hind_x, G - pr - U * 0.12)],
                                   [hr * 0.8, hr * 0.6]), leg_ramp, z=-0.9, region=leg_reg, **far))
            parts.append(Part(Ellipse(s * hind_x, G - pr - U * 0.12, pr * 1.3, pr), leg_ramp, z=-0.8,
                              region=leg_reg, **far))
        parts.append(Part(Ellipse(0, cy, bw, U * 0.62), "fur", z=0,
                          region=lambda x, y: "pale" if abs(x) < bw * 0.5 else "fur"))
        for k, s in enumerate((-1, 1)):
            x = s * bw * 0.5
            fy = G - pr - lift[k]
            parts.append(Part(Tube([(x, cy), (x, fy)], [fr, fr * 0.85]), leg_ramp,
                              z=2, region=leg_reg, inner=("fur", 0)))
            parts.append(Part(Ellipse(x, fy, pr * 1.25, pr), leg_ramp, z=2.1, region=leg_reg,
                              inner=("fur", 0)))
        eparts = ears(hy, 2.6)
        parts += [e[0] for e in eparts]
        cran = Ellipse(0, hy, U, U * 0.86)
        mry = U * 0.3 * o["muzzle"]
        mrx = U * 0.36 * o["muzzle"]
        mcy = hy + U * 0.46
        parts.append(Part(cran, "fur", z=3, inner=("fur", 0),
                          region=lambda x, y: "pale" if y > hy + U * 0.55 else "fur"))
        if hd["cheek"]:
            for s in (-1, 1):
                parts.append(Part(Ellipse(s * U * 0.62, hy + U * 0.3, U * 0.42 * hd["cheek"],
                                          U * 0.4 * hd["cheek"]), "fur", z=3.1, inner=("fur", 0),
                                  region=lambda x, y: "pale" if y > hy + U * 0.3 else "fur"))
        mramp = p.get("ow_ramps", {}).get("muzzle", "pale")
        parts.append(Part(Ellipse(0, mcy, mrx, mry), mramp, z=3.3, inner=("fur", 0)))

        def details(cv):
            for prt, shp, (bx, by), tip in eparts:  # inner ears
                if ear["kind"] != "round" and ear["inner"]:
                    inner = Facet([(bx - ew * 0.2, by + U * 0.2), (tip[0] * 0.85 + bx * 0.15, tip[1] + eh * 0.3),
                                   (bx + ew * 0.2, by + U * 0.2)])
                    paint(cv, inner, ("pale", -1), owner_part=parts.index(prt))
            for s in (-1, 1):
                px, py = cv.pt(s * U * 0.45, hy + U * 0.02)
                cv.set(px, py, "outline")
                cv.set(px, py - 1, "outline")
                if eye["line"]:
                    cv.set(px + (1 if s < 0 else -1), py + 1, ("dark", 0))
            nx, ny = cv.pt(0, mcy - mry * 0.55)
            for dx, dy in ((0, 0), (-1, 0)):
                cv.set(nx + dx, ny + dy, ("dark", 0))
            if cv.scale * U > 7:
                cv.set(nx, ny + 1, ("dark", 0))
            for fx, fy, c in p.get("ow_face", []):  # extra face pixels, in U
                cv.set(*cv.pt(fx * U, hy + fy * U), c)
        return Model(parts, p["ramps"], details)

    # north: from behind
    hcy = hy - U * 0.05
    parts.append(Part(Ellipse(0, cy, bw * 1.1, U * 0.7), "fur", z=0))
    for k, s in enumerate((-1, 1)):
        x = s * bw * 0.72
        fy = G - pr - lift[k]
        parts.append(Part(Ellipse(x, cy + U * 0.2, hr * 1.4, U * 0.45), "fur", z=0.5, inner=("fur", 0)))
        parts.append(Part(Tube([(x, cy + U * 0.4), (x, fy)], [hr * 0.9, hr * 0.7]), leg_ramp, z=1,
                          region=leg_reg, inner=("fur", 0)))
        parts.append(Part(Ellipse(x, fy, pr * 1.2, pr), leg_ramp, z=1.1, region=leg_reg, inner=("fur", 0)))
    parts.append(Part(Ellipse(0, hcy, U * 0.92, U * 0.8), "fur", z=-0.5, light=-0.05))
    parts += [e[0] for e in ears(hcy, -0.4, light=-0.1)]
    t = p["tail"]
    sway = U * (0.15 if step else -0.1)
    k = o["head"] * 0.55
    r0, rm, rt = (v * k for v in t["r"])
    tl = min(t["len"] * k, G - cy)
    if t["a0"] < 30 or o.get("tail_up"):  # a tail held level or up: a stub with the tip above the back
        tpts = [(0, cy - U * 0.1), (sway * 0.5, cy - U * 0.55), (sway, cy - U * 0.9)]
        trad = [r0, rm, rt * 1.2]
    else:
        tpts = [(0, cy - U * 0.2), (sway * 0.3, cy + tl * 0.3), (sway * 0.8, cy + tl * 0.65),
                (sway * 1.2, cy + tl * 0.95)]
        trad = [r0, rm, (rm + rt) / 2, rt]
    tail = Path(tpts, trad)
    parts.append(Part(tail, "fur", z=2, region=mreg("tail", lambda x, y: "fur", tail_frac=tail.frac),
                      inner=("fur", 0)))
    return Model(parts, p["ramps"])


PLAN = BodyPlan(
    "canid", "dogs and foxes (the dog starter lines)",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_CANID, tracks="TRACKS_FOOT",
)
