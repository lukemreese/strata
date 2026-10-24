"""hoofed_giant body plan: heavy-bodied large herbivores and omnivores
(pantodonts, uintatheres, entelodonts, bovines), plus the shared "giant"
quadruped engine that plans/rhino_brontothere.py and plans/proboscidean.py reuse.

Species (taxonomy.py):
    coryphodon    Coryphodon (Willwood Fm, WY, 500 kg)          Act 4 boss
    uintatherium  Uintatherium anceps (Bridger Fm, WY, 2000 kg) Act 5 boss
    archaeothere  Archaeotherium (Brule Fm, SD, 270 kg)         Act 6 boss
    bison         Bison bison (Living; MT, 700 kg)
    ovibos        Ovibos moschatus (Natural Trap Cave, WY, 300 kg)

The engine follows the proportion-driven quadruped of plans/canid.py (and
imports its Facet, Turned, Path, paint and colour-mark rules read-only) but is
built for graviportal and unguligrade animals: pillar legs ending in hooves or
nailed pads, long low heads with ungulate ears, and generic data-driven
`extras` for everything that makes a giant distinct (horns, knobs, tusks,
flanges, trunks, hair skirts, beards), so a new species is mostly data.
Model units are sprite pixels at scale 1, head to the LEFT, y down.

Spec keys (see DEFAULTS):
    body   L (shoulder-to-hip), top_s / top_h (back height at shoulder / hip),
           chest / waist / hip (depths), sag (back dip), chest_w / rump_w,
           hump (dx, dy, rx, ry) withers ellipse from the shoulder top or None,
           paunch (extra belly drop: hippo/rhino barrels)
    leg    h (chest bottom to ground), fr / hr (fore / hind radii: upper, lower,
           foot), fx / hx (fore / hind x offsets), far (far-leg dx), elbow,
           knee (stifle forward), hock (back), wrist / hockh (joint heights as a
           fraction of h), stride (walk swing deg), thigh / arm (near haunch and
           shoulder muscle factors), foot = dict(kind hoof|pad, l, h)
    neck   r0, r1, base (dx, dy from the shoulder top)
    head   dx, dy (cranium centre from the shoulder top), cr, cw, chh (cranium
           width / height factors), cdeg (cranium tilt), ml / md (muzzle length /
           depth), mdrop, mtilt, taper, jd (lower-jaw depth), hinge (u, v) and
           chin (du, dv) overrides, lumps (extra ellipses (u, v, rx, ry, deg)
           in head space merged into the head: brows, bosses, domes)
    ear    kind leaf|round, h, w, lean (deg from vertical, + = back), dx, dy
           (base from the cranium top), inner (pale inner ear), far (far-ear dx)
    tail   len, a0, bend, r (root, widest, tip), widest, dy
    eye    dx, dy (head space), r
    nose   r (nostril disc at the muzzle tip) or None
    marks  canid colour rules (plans/canid.py `_mark`); groups head, jaw, neck,
           torso, legs, tail, ear, plus "extra" for extras without their own ramp rule
    extras list of extra parts, each a dict:
             kind  ell (e=(cx, cy, rx, ry, deg)) | tube (pts, radii) |
                   facet (pts, convex) | pillow (pts, r: any polygon) |
                   fringe (top, bottom, teeth, depth, r: hanging hair)
             on    head (head space, follows tilt) | jaw (also follows the gape) |
                   body (absolute)
             ramp, z, plus optional flat, light, outline, inner, line, shadow,
             tip=(frac, ramp) for tubes (horn tips), far=(du, dv) adds a darker
             far-side copy behind (far_z), phase=0|1 (only in that frame),
             alt=dict(...) keys replaced in frame 2 (a raised trunk)
    wrinkles  polylines painted one shade darker: dict(on=head|body, pts)
    hair   dict(ramps=(...), period, run) vertical strand texture or None
    action frame-2 pose: tilt (head deg, + raises the snout), gape (jaw deg,
           negative opens), tail (deg), ear (deg)
    ow_end end-view sizes in U (= cranium radius x head): head, body, legs,
           muzzle, muzzle_dy, ear, ear_angle (deg from vertical; default
           sideways), eyes / eye_dy (eye spacing / height), hump, hump_w,
           head_dy, hind, tail_up, head_inner (contour colour of the face)
    ow_ramps  end-view ramps per group: body, head, muzzle, legs
    ow_chest_pale  pale chest patch in the south view (default True)
    ow_extras  {"south": [...], "north": [...]} extras in U units (head
           centre at the origin), mirror=True adds the x-mirrored copy

Ramps the engine uses: outline (1), fur (3-4), pale (2-3), dark (1-2), hoof
(1-2), skin (1, mouth), plus any ramp named by marks or extras (horn, tusk, hair).
"""

import math

from ..core.geom import Ellipse, Tube, Union, Part, Model, turn, lerp, clamp
from ..core.plan import BodyPlan
from .canid import Facet, Turned, Path, paint, _mark

FOOTPRINT_CLOVEN = [
    "................",
    "................",
    "................",
    ".....##..##.....",
    "....###..###....",
    "....###..###....",
    "....###..###....",
    "....###..###....",
    "....###..###....",
    ".....##..##.....",
    ".....##..##.....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINT_PAD = [  # a broad round sole with nail marks: uintatheres, pantodonts, proboscideans
    "................",
    "....#..##..#....",
    "................",
    "....########....",
    "...##########...",
    "..############..",
    "..############..",
    "..############..",
    "..############..",
    "...##########...",
    "....########....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINT_RHINO = [  # three toes, the middle one largest
    "................",
    "................",
    "...##......##...",
    "..###.####.###..",
    "..##.######.##..",
    ".....######.....",
    "....########....",
    "....########....",
    "....########....",
    ".....######.....",
    "......####......",
    "................",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINTS = dict(cloven=FOOTPRINT_CLOVEN, pad=FOOTPRINT_PAD, rhino=FOOTPRINT_RHINO)


# ---------------------------------------------------------------------------
# shapes


class Pillow:
    """Any simple polygon (convex or not) shaded like a cushion: q is the
    signed distance to the outline over r, capped at 1 (hair skirts, beards,
    flanges, horn bosses)."""
    def __init__(self, pts, r=2.0):
        self.p, self.r = pts, r
        self.bbox = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
        self.edges = list(zip(pts, pts[1:] + pts[:1]))

    def q(self, x, y):
        inside, best = False, 1e9
        for (ax, ay), (bx, by) in self.edges:
            if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
                inside = not inside
            dx, dy = bx - ax, by - ay
            ll = dx * dx + dy * dy
            t = clamp(((x - ax) * dx + (y - ay) * dy) / ll, 0, 1) if ll else 0
            best = min(best, math.hypot(x - ax - dx * t, y - ay - dy * t))
        return min(1.0, best / self.r) if inside else -best / self.r


def along(pts, f):
    """The point at fraction f of the polyline's length."""
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    d = clamp(f, 0, 1) * sum(segs)
    for (a, b), s in zip(zip(pts, pts[1:]), segs):
        if d <= s:
            t = d / s if s else 0
            return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))
        d -= s
    return pts[-1]


def fringe_points(top, bottom, teeth, depth):
    """A hanging hair fringe: the upper edge `top` (left to right), then the
    lower edge `bottom` (left to right) walked back with `teeth` points of
    length `depth` (ragged locks)."""
    n = max(1, int(teeth)) * 2
    lower = []
    for k in range(n + 1):
        x, y = along(bottom, 1 - k / n)
        if k % 2 == 1:
            y += depth
        lower.append((x, y))
    return list(top) + lower


# ---------------------------------------------------------------------------
# defaults

DEFAULTS = dict(
    front=1.0, back=1.06, icon=0.5,
    body=dict(L=26.0, top_s=-12.0, top_h=-11.0, chest=16.0, waist=14.0, hip=14.0, sag=0.5,
              chest_w=1.0, rump_w=1.0, hump=None, paunch=0.0, k=0.14),
    leg=dict(h=10.0, fr=(4.0, 3.0, 2.8), hr=(4.4, 3.0, 2.8), fx=2.0, hx=0.0, far=(3.0, -2.5),
             elbow=0.8, knee=2.0, hock=2.0, wrist=0.25, hockh=0.35, stride=14.0, thigh=1.0, arm=0.0,
             foot=dict(kind="hoof", l=4.0, h=2.2)),
    neck=dict(r0=6.0, r1=5.0, base=(0.0, 4.0)),
    head=dict(dx=-10.0, dy=-1.0, cr=6.0, cw=1.1, chh=0.86, cdeg=0.0, ml=6.0, md=5.0, mdrop=1.0, mtilt=10.0,
              taper=0.72, jd=2.6, hinge=None, chin=(0.0, 0.0), lumps=[], k=0.12),
    ear=dict(kind="leaf", h=4.0, w=2.4, lean=50.0, dx=1.5, dy=0.4, inner=True, far=0.6),
    tail=dict(len=8.0, a0=70.0, bend=4.0, r=(1.6, 1.4, 1.0), widest=0.2, dy=0.0),
    eye=dict(dx=-2.0, dy=-1.0, r=1.1),
    nose=dict(r=0.9),
    marks=[], belly=None, throat=None,
    extras=[], wrinkles=[], hair=None, teeth=None,
    action=dict(tilt=0.0, gape=0.0, tail=0.0, ear=0.0),
    ow=dict(tracks="TRACKS_FOOT"), ow_end={}, ow_extras={},
)

FAR = -0.28  # far-side darkening


# ---------------------------------------------------------------------------
# rig


def rig(p):
    b, lg, hd, nk = p["body"], p["leg"], p["head"], p["neck"]
    L = b["L"]
    xs, xh = -L / 2, L / 2
    ts, th = b["top_s"], b["top_h"]
    ch, wa, hp = b["chest"], b["waist"], b["hip"]
    G = ts + ch + lg["h"]
    r = dict(L=L, xs=xs, xh=xh, ts=ts, th=th, ch=ch, wa=wa, hp=hp, G=G)
    r["torso"] = [
        (xs + 1.0, ts + ch / 2, ch * 0.62 * b["chest_w"], ch / 2, -6),
        (0.0, (ts + th) / 2 + b["sag"] + wa / 2 + b["paunch"] * 0.5, L * 0.44, wa / 2 + b["paunch"] * 0.5, 0),
        (xh - 0.5, th + hp / 2, hp * 0.58 * b["rump_w"], hp / 2, 8),
    ]
    if b["hump"]:
        dx, dy, rx, ry = b["hump"]
        r["torso"].append((xs + dx, ts + dy, rx, ry, -10))
    hx, hy = xs + hd["dx"], ts + hd["dy"]
    r["hx"], r["hy"] = hx, hy
    r["neck"] = ((xs + nk["base"][0], ts + nk["base"][1]), (hx + hd["cr"] * 0.35, hy + hd["cr"] * 0.3))
    r["pivot"] = r["neck"][1]
    return r


def head_shapes(p, r):
    hd = p["head"]
    hx, hy, cr = r["hx"], r["hy"], hd["cr"]
    ml, md = hd["ml"], hd["md"]
    root = (hx - cr * 0.45, hy + cr * 0.18 + hd["mdrop"] * 0.3)
    a = math.radians(hd["mtilt"])
    reach = ml + cr * 0.45
    tipc = (root[0] - reach * math.cos(a), root[1] + reach * math.sin(a) + hd["mdrop"])
    taper = hd["taper"]
    r0, r1 = md * 0.62, md * 0.5 * taper / 0.72
    shapes = [Ellipse(hx, hy, cr * hd["cw"], cr * hd["chh"], hd["cdeg"]), Tube([root, tipc], [r0, r1])]
    for u, v, rx, ry, deg in hd["lumps"]:
        shapes.append(Ellipse(hx + u, hy + v, rx, ry, deg))
    tip_x = tipc[0] - r1
    mouth_y = tipc[1] + r1 * 0.75
    hinge = (hx + hd["hinge"][0], hy + hd["hinge"][1]) if hd["hinge"] else (hx + cr * 0.15, hy + cr * 0.6)
    jd = hd["jd"]
    chin = (tip_x + 1.4 + jd * 0.3 + hd["chin"][0], mouth_y + jd * 0.3 + hd["chin"][1])
    return dict(shapes=shapes, tip=(tip_x, tipc[1] - r1 * 0.3), mouth_y=mouth_y, hinge=hinge, chin=chin,
                jd=jd, root=root, tipc=tipc, r1=r1)


def legs(p, r, step):
    """Far fore, far hind, near fore, near hind: tube points, radii and the foot."""
    lg = p["leg"]
    G, xs, xh, ts, th, ch, hp = r["G"], r["xs"], r["xh"], r["ts"], r["th"], r["ch"], r["hp"]
    ft = lg["foot"]
    fl, fh = ft["l"], ft["h"]
    out = []
    for near in (False, True):
        for fore in (True, False):
            if fore:
                x0 = xs + lg["fx"] + (0 if near else lg["far"][0])
                top = (x0, ts + ch * 0.42)
                mid = (x0 + lg["elbow"], ts + ch - 0.5)
                joint = (x0 - 0.1, G - fh - lg["h"] * lg["wrist"])
                radii = list(lg["fr"])
            else:
                x0 = xh + lg["hx"] + (0 if near else lg["far"][1])
                top = (x0, th + hp * 0.38)
                mid = (x0 - lg["knee"], th + hp + lg["h"] * 0.05)
                joint = (x0 + lg["hock"], G - fh - lg["h"] * lg["hockh"])
                radii = list(lg["hr"])
            foot_top = (joint[0] - 0.3 - (0.3 if fore else 0.6), G - fh * 0.9)
            pts = [top, mid, joint, foot_top]
            radii = radii + [radii[-1] * 0.98]
            foot_c = (foot_top[0] - fl * 0.08, G - fh * 0.5)
            if step:
                sgn = 1 if (near == fore) else -1
                piv = pts[0]
                sw = lg["stride"] * sgn
                pts = [pts[0]] + [turn(q, piv, sw) for q in pts[1:]]
                fc = turn(foot_c, piv, sw)
                lift = max(0.0, fc[1] + fh * 0.5 - G)
                pts = [pts[0]] + [(x, y - lift * (k / 3)) for k, (x, y) in enumerate(pts[1:], 1)]
                foot_c = (fc[0], fc[1] - lift)
            out.append(dict(near=near, fore=fore, pts=pts, radii=radii, foot=foot_c))
    return out


def foot_shape(p, c, near):
    """The hoof or nailed pad around centre c = (x, y)."""
    ft = p["leg"]["foot"]
    fl, fh = ft["l"], ft["h"]
    x, y = c
    if ft["kind"] == "hoof":  # a wedge, toe forward (left), slanted front
        return Facet([(x - fl * 0.55, y + fh * 0.5), (x - fl * 0.25, y - fh * 0.5), (x + fl * 0.45, y - fh * 0.5),
                      (x + fl * 0.5, y + fh * 0.5)])
    return Ellipse(x, y, fl / 2, fh / 2 + 0.2)


def tail_points(p, r, extra=0.0):
    t = p["tail"]
    x, y = r["xh"] + r["hp"] * 0.35, r["th"] + 1.5 + t["dy"]
    seg = t["len"] / 5
    pts = [(x, y)]
    a = t["a0"] + extra
    for _ in range(5):
        x += seg * math.cos(math.radians(a))
        y += seg * math.sin(math.radians(a))
        pts.append((x, y))
        a += t["bend"]
    r0, rm, rt = t["r"]
    w = t["widest"]
    radii = [lerp(r0, rm, (k / 5) / w) if k / 5 <= w else lerp(rm, rt, (k / 5 - w) / (1 - w)) for k in range(6)]
    return pts, radii


def _countershade(p, r):
    if p["belly"]:
        a, s = p["belly"]
        return lambda x: a + s * x
    y0 = r["ts"] + r["ch"] * 0.78
    y1 = r["th"] + r["hp"] * 0.92
    return lambda x: lerp(y0, y1, clamp((x - r["xs"]) / (r["xh"] - r["xs"]), 0, 1))


# ---------------------------------------------------------------------------
# extras


def phase_extras(extras, phase):
    out = []
    for e in extras:
        if "phase" in e and e["phase"] != phase:
            continue
        if phase and "alt" in e:
            e = {**e, **e["alt"]}
        out.append(e)
    return out


def extra_shape(e, f, rot, k=1.0):
    """Builds the shape of extra e; f maps a point to model space, rot is the
    rotation of that space in degrees, k scales radii (end views: U)."""
    kind = e["kind"]
    if kind == "ell":
        cx, cy, rx, ry = e["e"][:4]
        deg = e["e"][4] if len(e["e"]) > 4 else 0.0
        return Ellipse(*f((cx, cy)), rx * k, ry * k, deg + rot)
    if kind == "tube":
        return Path([f(q) for q in e["pts"]], [v * k for v in e["radii"]])
    if kind == "facet":
        return Facet([f(q) for q in e["pts"]])
    if kind == "pillow":
        return Pillow([f(q) for q in e["pts"]], e.get("r", 2.0) * k)
    if kind == "fringe":
        pts = fringe_points(e["top"], e["bottom"], e["teeth"], e["depth"])
        return Pillow([f(q) for q in pts], e.get("r", 2.0) * k)
    raise ValueError(f"unknown extra kind {kind}")


def extra_parts(e, f, rot, region=None, k=1.0, far_f=None):
    """Part(s) for one extra: the far copy (if any) and the near one."""
    out = []
    kw = dict(flat=e.get("flat", 0.5), outline=e.get("outline", "outline"), line=e.get("line", True),
              shadow=e.get("shadow", True))
    if "inner" in e:
        kw["inner"] = e["inner"]
    if e.get("far") is not None and far_f is not None:
        du, dv = e["far"]
        sh = extra_shape(e, lambda q: far_f((q[0] + du, q[1] + dv)), rot, k)
        out.append(Part(sh, e["ramp"], z=e.get("far_z", -0.5), light=FAR + e.get("light", 0.0),
                        region=_tip_region(e, sh), **kw))
    sh = extra_shape(e, f, rot, k)
    out.append(Part(sh, e["ramp"], z=e.get("z", 3.4), light=e.get("light", 0.0),
                    region=_tip_region(e, sh) or region, **kw))
    return out


def _tip_region(e, sh):
    if "tip" not in e or not isinstance(sh, Path):
        return None
    f0, tr = e["tip"]
    base = e["ramp"]
    return lambda x, y: tr if sh.frac(x, y) >= f0 else base


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
    G = r["G"]

    def region(group, default, local=None, **kw):
        c = dict(G=G, belly=belly)
        c.update(kw)

        def fn(x, y):
            lx, ly = local(x, y) if local else (x, y)
            for m in marks:
                if _mark(m, group, lx, ly, c):
                    return m["ramp"]
            return default(lx, ly)
        return fn

    def head_local(x, y):
        u, v = Hinv(x, y)
        return u - hx, v - hy

    torso = Union([Ellipse(*e) for e in r["torso"]], k=p["body"]["k"])
    torso_reg = region("torso", lambda x, y: "pale" if y > belly(x) else "fur")

    n0, n1 = r["neck"]
    neck = Tube([n0, H(n1)], [p["neck"]["r0"], p["neck"]["r1"]])

    def neck_default(x, y):
        if p["throat"]:
            ta, tsl = p["throat"]
            return "pale" if y > ta + tsl * x else "fur"
        ax, ay = hs["hinge"][0], hs["hinge"][1] + 1.0
        bx, by = r["xs"] - 1.0, belly(r["xs"])
        t = clamp((x - ax) / ((bx - ax) or 1), 0, 1)
        return "pale" if y > lerp(ay, by, t) else "fur"
    neck_reg = region("neck", neck_default)

    mouth_rel = hs["mouth_y"] - hy

    def head_default(u, v):
        return "pale" if v > mouth_rel - hd["md"] * 0.15 and u < -hd["cr"] * 0.6 else "fur"
    head_reg = region("head", head_default, local=head_local)
    head = Turned(Union(hs["shapes"], k=hd["k"]), pivot, tilt)

    gape = act.get("gape", 0.0)
    hinge = hs["hinge"]
    J = lambda pt: H(turn(pt, hinge, gape))  # noqa: E731
    jd = hs["jd"]
    jaw_pts = [J((hinge[0] - 0.5, hinge[1] + 0.2)), J(((hinge[0] + hs["chin"][0]) / 2, hs["mouth_y"] + jd * 0.45)),
               J(hs["chin"])]
    jaw = Tube(jaw_pts, [jd * 0.8, jd * 0.66, jd * 0.5])
    jaw_reg = region("jaw", lambda x, y: "pale", local=head_local)

    # ears
    ear = p["ear"]
    eb = (hx + hd["cr"] * 0.25 + ear["dx"], hy - hd["cr"] * hd["chh"] * 0.75 + ear["dy"])
    elean = ear["lean"] + act.get("ear", 0.0)

    def ear_shape(base, s=1.0):
        bx, by = base
        h, w = ear["h"] * s, ear["w"] * s
        a = math.radians(elean)
        c = (bx + h * 0.5 * math.sin(a), by - h * 0.5 * math.cos(a))
        if ear["kind"] == "round":  # a flap lying on the side of the head
            return Ellipse(*H(c), w / 2, h / 2, elean + tilt), Ellipse(*H(c), w * 0.28, h * 0.32, elean + tilt)
        return (Ellipse(*H(c), w / 2, h / 2, elean + tilt),
                Ellipse(*H((c[0] + 0.15, c[1] + 0.1)), w * 0.24, h * 0.32, elean + tilt))
    near_ear, inner_ear = ear_shape(eb)
    far_ear, _ = ear_shape((eb[0] - ear["far"], eb[1] + 0.2), 0.92)
    ear_reg = region("ear", lambda x, y: "fur", local=head_local)

    tpts, trad = tail_points(p, r, act.get("tail", 0.0))
    tail = Path(tpts, trad)
    tail_reg = region("tail", lambda x, y: "fur", tail_frac=tail.frac)

    L4 = legs(p, r, step)
    lg = p["leg"]
    hoof = "hoof" if "hoof" in p["ramps"] else "dark"
    parts = [Part(tail, "fur", z=-3, region=tail_reg, inner=("fur", 0))]
    if ear["kind"] != "round":
        parts.append(Part(far_ear, "fur", z=-0.6, region=ear_reg, light=FAR))
    for l_ in L4:
        if not l_["near"]:
            reg = region("legs", lambda x, y: "fur", leg="fore" if l_["fore"] else "hind")
            parts += [Part(Tube(l_["pts"], l_["radii"]), "fur", z=-2, region=reg, light=FAR),
                      Part(foot_shape(p, l_["foot"], False), hoof, z=-1.9, light=FAR)]
    parts.append(Part(torso, "fur", z=0, flat=0.55, region=torso_reg))
    for l_ in L4:
        if l_["near"]:
            reg = region("legs", lambda x, y: "fur", leg="fore" if l_["fore"] else "hind")
            z = 2 if l_["fore"] else 1.5
            parts += [Part(Tube(l_["pts"], l_["radii"]), "fur", z=z, region=reg, inner=("fur", 0)),
                      Part(foot_shape(p, l_["foot"], True), hoof, z=z + 0.1, inner=(hoof, 0))]
            (x0, y0), (x1, y1) = l_["pts"][0], l_["pts"][1]
            if not l_["fore"] and lg["thigh"]:
                s = lg["thigh"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.8, (y0 + y1) / 2 - 1.0, r["hp"] * 0.4 * s,
                                          r["hp"] * 0.55 * s, 20), "fur", z=1.6, region=torso_reg,
                                  inner=("fur", 0)))
            if l_["fore"] and lg["arm"]:
                s = lg["arm"]
                parts.append(Part(Ellipse((x0 + x1) / 2 + 0.4, (y0 + y1) / 2 - 1.0, r["ch"] * 0.3 * s,
                                          r["ch"] * 0.42 * s, -10), "fur", z=2.05, region=torso_reg,
                                  inner=("fur", 0)))
    parts += [Part(neck, "fur", z=2.5, region=neck_reg, inner=("fur", 0)),
              Part(jaw, "pale", z=2.9, region=jaw_reg, inner=("fur", 0)),
              Part(head, "fur", z=3, flat=0.5, region=head_reg, inner=("fur", 0)),
              Part(near_ear, "fur", z=3.2 if ear["kind"] != "round" else 3.15, region=ear_reg,
                   inner=("fur", 0))]
    if gape:
        mi = [H(hinge), H((hs["tip"][0] + 1.2, hs["mouth_y"] - 0.3)), J((hs["chin"][0] + 0.4, hs["chin"][1] - 0.6))]
        parts.append(Part(Facet(mi), "skin", z=2.8, line=False, shadow=False))

    # extras
    X = dict(head=(lambda q: H((hx + q[0], hy + q[1])), tilt),
             jaw=(lambda q: J((hx + q[0], hy + q[1])), tilt + gape),
             body=(lambda q: q, 0.0))
    for e in phase_extras(p["extras"], phase):
        f, rot = X[e.get("on", "head")]
        grp = e.get("group", "extra")
        reg = None
        if grp != "extra":
            loc = head_local if e.get("on", "head") != "body" else None
            reg = region(grp, lambda x, y, d=e["ramp"]: d, local=loc)
        parts += extra_parts(e, f, rot, region=reg, far_f=f)

    eye = p["eye"]
    ec = H((hx + eye["dx"], hy + eye["dy"]))
    nose_c = H((hs["tip"][0] + 1.0, hs["tip"][1]))
    near_ear_i = parts.index(next(q for q in parts if q.shape is near_ear))
    hair = p["hair"]

    def details(cv):
        big = cv.big
        if inner_ear is not None and ear["inner"] and big:
            paint(cv, inner_ear, ear.get("inner_ramp", ("pale", 0)), owner_part=near_ear_i)
        if hair and big:
            hr_ = set()
            for nm in hair["ramps"]:
                hr_ |= set(cv.pal.index[nm][1:])
            per, run = hair.get("period", 3), hair.get("run", 3)
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in hr_ and px % per == 0 and (py + (px // per) * 2) % (run + 2) < run:
                        cv.shade(px, py, -1)
        if big:
            for w in p["wrinkles"]:
                on = w.get("on", "body")
                pts = [H((hx + u, hy + v)) for u, v in w["pts"]] if on == "head" else w["pts"]
                cv.polyline(pts, None, shade=w.get("shade", -1))
        if big and p["leg"]["foot"]["kind"] == "pad":  # pale nails along the sole
            for l_ in L4:
                if l_["near"]:
                    x, y = l_["foot"]
                    fl = p["leg"]["foot"]["l"]
                    for k in range(p["leg"]["foot"].get("nails", 2)):
                        cv.set(*cv.pt(x - fl * 0.42 + k * 1.3, y + p["leg"]["foot"]["h"] * 0.25), ("hoof", -1)
                               if "hoof" in cv.pal.index else "pale")
        if p["nose"]:
            cv.disc(nose_c, p["nose"]["r"] if big else 0.6, ("dark", 0), only_opaque=True)
        if big and gape and p["teeth"]:
            for (u0, v0), (u1, v1), jawside in p["teeth"]:
                F = (lambda q: J((hx + q[0], hy + q[1]))) if jawside else (lambda q: H((hx + q[0], hy + q[1])))
                cv.line(F((u0, v0)), F((u1, v1)), "white" if "white" in cv.pal.index else ("pale", -1),
                        only_opaque=False)
        r_ = eye["r"]
        if big:
            cv.disc(ec, r_, "outline", only_opaque=True)
            px, py = cv.pt(*ec)
            fwd = 1 if cv.flip else -1
            cv.set(px + fwd, py - 1, eye.get("glint", ("pale", -1)))
        else:
            cv.disc(ec, max(0.6, r_ * 0.6), "outline", only_opaque=True)

    return Model(parts, p["ramps"], details)


# ---------------------------------------------------------------------------
# overworld end views


def overworld(p, view, step):
    """South: the face over the chest, pillar forelegs in front, hind feet at
    the sides, ears out sideways. North: rump, hind legs, the tail, the back
    of the head (and hump) above. Sizes in U = cranium radius x ow_end["head"].
    Species features come from `ow_extras` in U units (mirror=True pairs)."""
    hd, lg, ear, eye = p["head"], p["leg"], p["ear"], p["eye"]
    o = {**dict(head=1.6, body=1.0, legs=1.0, muzzle=1.0, ear=1.0, hump=0.0, head_dy=0.0, hind=1.0,
                hump_w=0.8, eyes=0.62, eye_dy=-0.1, muzzle_dy=0.5), **p["ow_end"]}
    U = hd["cr"] * o["head"]
    b = p["body"]
    depth = b["chest"] / hd["cr"]
    legv = U * (0.3 + 0.4 * lg["h"] / b["chest"]) * o["legs"]
    bw = U * (0.45 + 0.2 * depth) * o["body"]
    lift = (0.25 * U, 0.0) if step else (0.0, 0.0)
    fh = lg["foot"]["h"] * o["head"] * 0.5
    fr = lg["fr"][0] * o["head"] * 0.45
    hr = lg["hr"][0] * o["head"] * 0.45
    hoof = "hoof" if "hoof" in p["ramps"] else "dark"
    marks = p["marks"]
    hy = o["head_dy"] * U
    cy = U * 0.9
    G = cy + U * 0.45 + legv
    leg_ramp = p.get("ow_ramps", {}).get("legs", "fur")
    body_ramp = p.get("ow_ramps", {}).get("body", "fur")

    def mreg(group, default, **kw):
        c = dict(G=G, belly=lambda x: 99.0)
        c.update(kw)

        def f(x, y):
            for m in marks:
                if m["kind"] == "socks":
                    if group == "legs" and y > G - m["h"] * U / hd["cr"] * 0.5:
                        return m["ramp"]
                elif m["kind"] in ("rings", "tip") and _mark(m, group, x, y, c):
                    return m["ramp"]
            return default(x, y)
        return f
    leg_reg = mreg("legs", lambda x, y: leg_ramp)
    parts = []
    eh, ew = ear["h"] / hd["cr"] * U * 0.75 * o["ear"], ear["w"] / hd["cr"] * U * 0.75 * o["ear"]
    sc = lambda q: (q[0] * U, q[1] * U)  # noqa: E731

    def add_extras(lst):
        for e in phase_extras(lst, step or 0):
            for s in ((1, -1) if e.get("mirror") else (1,)):
                f = (lambda q, s=s: (s * q[0] * U, q[1] * U))
                e2 = dict(e)
                if e["kind"] == "ell" and s < 0:
                    cx, cy_, rx, ry = e["e"][:4]
                    deg = e["e"][4] if len(e["e"]) > 4 else 0.0
                    e2["e"] = (cx, cy_, rx, ry, -deg)
                parts.extend(extra_parts(e2, f, 0.0, k=U))

    if view == "south":
        hind_x = (bw * 0.9 + hr * 0.4) * o["hind"]
        for s in (-1, 1):
            parts.append(Part(Tube([(s * hind_x, cy + U * 0.3), (s * hind_x, G - fh)], [hr, hr * 0.85]),
                              leg_ramp, z=-0.9, region=leg_reg, light=FAR))
            parts.append(Part(Ellipse(s * hind_x, G - fh * 0.5, hr * 0.95, fh * 0.6), hoof, z=-0.8, light=FAR))
        if o["hump"]:
            parts.append(Part(Ellipse(0, cy - U * o["hump"], bw * o["hump_w"], U * 0.75), body_ramp, z=-0.5))
        parts.append(Part(Ellipse(0, cy, bw, U * 0.8), body_ramp, z=0,
                          region=lambda x, y: "pale" if (abs(x) < bw * 0.35 and y > cy + U * 0.3
                                                         and p.get("ow_chest_pale", True)) else body_ramp))
        for k, s in enumerate((-1, 1)):
            x = s * bw * 0.55
            fy = G - fh - lift[k]
            parts.append(Part(Tube([(x, cy + U * 0.1), (x, fy)], [fr, fr * 0.9]), leg_ramp, z=2,
                              region=leg_reg, inner=("fur", 0)))
            parts.append(Part(Ellipse(x, fy + fh * 0.5, fr * 1.05, fh * 0.65), hoof, z=2.1, inner=(hoof, 0)))
        # ears out to the sides
        eparts = []
        for s in (-1, 1):
            bx, by = s * U * 0.75, hy - U * 0.45
            a = math.radians(s * o.get("ear_angle", 90 - ear["lean"] * 0.4 if ear["kind"] != "round" else 70))
            c = (bx + eh * 0.5 * math.sin(a), by - eh * 0.5 * math.cos(a))
            shp = Ellipse(*c, ew / 2, eh / 2, math.degrees(a))
            pr = Part(shp, "fur", z=2.6, inner=("fur", 0), region=mreg("ear", lambda x, y: "fur"))
            parts.append(pr)
            eparts.append((pr, c, a))
        cran = Ellipse(0, hy, U * hd["cw"] * 0.9, U * hd["chh"])
        parts.append(Part(cran, p.get("ow_ramps", {}).get("head", "fur"), z=3, inner=o.get("head_inner", ("fur", 0)), region=p.get("ow_head_region")))
        mry, mrx = U * 0.42 * o["muzzle"], U * 0.5 * o["muzzle"]
        mcy = hy + U * o["muzzle_dy"]
        mramp = p.get("ow_ramps", {}).get("muzzle", "fur")
        parts.append(Part(Ellipse(0, mcy, mrx, mry), mramp, z=3.3, inner=("fur", 0)))
        add_extras(p["ow_extras"].get("south", []))

        def details(cv):
            for prt, c, a in eparts:
                if ear["inner"]:
                    paint(cv, Ellipse(c[0], c[1], ew * 0.22, eh * 0.3, math.degrees(a)), ("pale", 0),
                          owner_part=parts.index(prt))
            for s in (-1, 1):
                px, py = cv.pt(s * U * o["eyes"], hy + U * o["eye_dy"])
                cv.set(px, py, "outline")
                cv.set(px, py + 1, "outline")
            if p["nose"]:
                for s in (-1, 1):
                    cv.set(*cv.pt(s * mrx * 0.45, mcy + mry * 0.2), ("dark", 0))
        return Model(parts, p["ramps"], details)

    # north
    hcy = hy - U * 0.05
    if o["hump"]:
        parts.append(Part(Ellipse(0, cy - U * o["hump"], bw * o["hump_w"], U * 0.75), body_ramp, z=0.2))
    parts.append(Part(Ellipse(0, cy, bw * 1.05, U * 0.85), body_ramp, z=0))
    for k, s in enumerate((-1, 1)):
        x = s * bw * 0.62
        fy = G - fh - lift[k]
        parts.append(Part(Ellipse(x, cy + U * 0.25, hr * 1.5, U * 0.55), "fur", z=0.5, inner=("fur", 0),
                          region=mreg("torso", lambda x, y: "fur")))
        parts.append(Part(Tube([(x, cy + U * 0.5), (x, fy)], [hr, hr * 0.85]), leg_ramp, z=1,
                          region=leg_reg, inner=("fur", 0)))
        parts.append(Part(Ellipse(x, fy + fh * 0.5, hr * 1.0, fh * 0.65), hoof, z=1.1, inner=(hoof, 0)))
    parts.append(Part(Ellipse(0, hcy, U * hd["cw"] * 0.85, U * hd["chh"] * 0.9), "fur", z=-0.5, light=-0.05))
    for s in (-1, 1):
        bx, by = s * U * 0.7, hcy - U * 0.45
        a = math.radians(s * o.get("ear_angle", 90 - ear["lean"] * 0.4 if ear["kind"] != "round" else 70))
        c = (bx + eh * 0.5 * math.sin(a), by - eh * 0.5 * math.cos(a))
        parts.append(Part(Ellipse(*c, ew / 2, eh / 2, math.degrees(a)), "fur", z=-0.4, light=-0.1))
    t = p["tail"]
    sway = U * (0.12 if step else -0.08)
    kk = o["head"] * 0.5
    r0, rm, rt = (v * kk for v in t["r"])
    tl = min(t["len"] * kk, G - cy)
    if o.get("tail_up"):
        tpts = [(0, cy - U * 0.1), (sway * 0.5, cy - U * 0.5), (sway, cy - U * 0.8)]
        trad = [r0, rm, rt]
    else:
        tpts = [(0, cy - U * 0.3), (sway * 0.3, cy + tl * 0.3), (sway * 0.8, cy + tl * 0.65),
                (sway * 1.2, cy + tl * 0.95)]
        trad = [r0, rm, (rm + rt) / 2, rt]
    tail = Path(tpts, trad)
    parts.append(Part(tail, "fur", z=2, region=mreg("tail", lambda x, y: "fur", tail_frac=tail.frac),
                      inner=("fur", 0)))
    add_extras(p["ow_extras"].get("north", []))
    return Model(parts, p["ramps"])


PLAN = BodyPlan(
    "hoofed_giant", "heavy-bodied large herbivores/omnivores: pantodonts, uintatheres, entelodonts, bovines",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_CLOVEN, tracks="TRACKS_FOOT",
)
