"""Theropod body plan: bipedal theropods in side view, plus the shared
dinosaur kit that plans/ornithischian.py imports.

Species (taxonomy.py):
    tyrannosaur   Tyrannosaurus rex (Hell Creek Fm, MT, 8000 kg)
    acheroraptor  Acheroraptor temertyorum (Hell Creek Fm, MT, 40 kg)
    anzu          Anzu wyliei (Hell Creek Fm, ND/SD, 250 kg)

Anatomy: Tyrannosaurus (deep skull, lipped jaws, tiny two-fingered arms,
horizontal back, scaly with a few optional filaments; earth tones),
Acheroraptor (dromaeosaur: fully feathered, wing feathers on the arms, frond
tail, sickle claw on toe II), Anzu (oviraptorosaur: tall casque, toothless
beak, long neck and legs, feathered, wing feathers).

Ramps the template uses (a spec may add more for its own parts):
    outline   1 colour
    skin      main colour (scales or plumage), 4 shades
    belly     underside, 2-3 shades
    mouth     gape and gums, 2 shades (any species that opens its mouth)
    eye       1 colour (iris)
    white     1 colour: teeth, eye highlight
    claw      1 colour (claws, beak tip)
    + whatever `extras`, `wings`, `head_ramps` name (plume, crest, beak, ...)

------------------------------------------------------------------- the kit
Shapes are given as data so they can be posed:
    ("E", cx, cy, rx, ry[, angle])     Ellipse
    ("T", [points], [radii])           Tube
    ("P", [points])                    Poly (flat: give the part a normal)
    ("L", x0, x1, up, dn, a, c)        Loft along x, mid line a*(1-t)+c (skulls)
    ("U", [shapes][, k])               smooth Union
    ("R", shape, amp, freq)            Ragged edge (feathers, shag)
Pose groups: "body" (fixed), "head" (rotates about `neck` by the frame's head
angle), "jaw" (about `jaw_pivot`, inside the head), "tail" (a progressive bend
from `tail_base`), "crest" (inside the head), legs and arms (rigid about hip /
shoulder; the walk cycle swings them).

Spec keys used by side():
    body       list of shape data (torso ellipses, neck tube, tail tube) unioned
               into one smooth body; body_k blend width
    belly      [(x, y), ...]: body points below this curve use the belly ramp
    head       shape data (skull) in the head group; head_belly: [(x, y)] (head
               coordinates) below which the skull is belly-coloured
    jaw        shape data (lower jaw), jaw group; jaw_belly likewise
    mouth      shape data (gape interior, behind skull and jaw) or None
    legs/arms  list of dict(near, pts, radii, z, foot=shape data, thigh=shape
               data, swing=+1|-1, claws=[pts], wing=shape data, ramp=...)
               far ones first
    extras     list of dict(s=shape data, ramp, z, group, normal, flat, light,
               outline, inner, line, region=(ramp, [(x, y)])): crests, frills,
               horns, tail fans, osteoderm spikes, ...
    eye        dict(c=(x, y), r, brow=[pts] or None) in head coordinates
    nostril    (x, y) head coordinates or None
    lip        [pts] head coordinates: the closed mouth line, or None
    teeth      dict(upper=[pts head], lower=[pts jaw]) shown when gaping
    action     frame 2: dict(head=deg, jaw=deg, tail=deg, arms=deg, crest=deg)
    walk       leg swing in degrees for the overworld step
    texture    list of dict(kind="scales"|"dashes"|"bands", ramp, ...) painters
"""

import math

from ..core.geom import Ellipse, Tube, Union, Poly, Loft, Part, Model, curve, clamp, rot
from ..core.plan import BodyPlan
from ..core.raster import Canvas

# ======================================================================= kit
# Primitives added by the dinosaur lane (candidates for core/geom.py).


def pose(deg=0.0, pivot=(0.0, 0.0), then=None):
    """A rigid pose (deg, b): p -> rot(p, deg) + b, rotating about `pivot`;
    `then` is a parent pose applied afterwards."""
    r = rot(*pivot, deg)
    b = (pivot[0] - r[0], pivot[1] - r[1])
    if then:
        d2, b2 = then
        rb = rot(*b, d2)
        return (deg + d2, (rb[0] + b2[0], rb[1] + b2[1]))
    return (deg, b)


IDENT = (0.0, (0.0, 0.0))


def apply(ps, q):
    d, b = ps
    x, y = rot(q[0], q[1], d)
    return (x + b[0], y + b[1])


def inverse(ps, q):
    d, b = ps
    return rot(q[0] - b[0], q[1] - b[1], -d)


class Rigid:
    """Any shape moved by a rigid pose (lofts and unions posed as one piece)."""
    def __init__(self, shape, ps):
        self.s, self.ps = shape, ps
        x0, y0, x1, y1 = shape.bbox
        pts = [apply(ps, c) for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
        self.bbox = (min(p[0] for p in pts), min(p[1] for p in pts),
                     max(p[0] for p in pts), max(p[1] for p in pts))

    def q(self, x, y):
        return self.s.q(*inverse(self.ps, (x, y)))


class Ragged:
    """Roughens a shape's edge (feathered or shaggy outlines). The bumps only
    act within `band` of the edge, so the interior shading stays smooth."""
    def __init__(self, shape, amp=0.3, freq=1.4, band=0.45):
        self.s, self.amp, self.freq, self.band = shape, amp, freq, band
        x0, y0, x1, y1 = shape.bbox
        self.bbox = (x0 - 1.5, y0 - 1.5, x1 + 1.5, y1 + 1.5)

    def q(self, x, y):
        q = self.s.q(x, y)
        if q < -self.band or q > self.band:
            return q
        w = 1 - abs(q) / self.band
        return q + self.amp * w * math.sin(x * self.freq) * math.sin(y * self.freq * 1.17 + 0.6)


def mk(s, ps=None, bend=None):
    """Shape data -> shape, posed rigidly (ps) or through a point map (bend)."""
    kind = s[0]
    if kind == "U":
        return Union([mk(x, ps, bend) for x in s[1]], k=s[2] if len(s) > 2 else 0.12)
    if kind == "R":
        return Ragged(mk(s[1], ps, bend), *s[2:])
    if kind == "L":
        x0, x1, up, dn, a, c = s[1:7]
        loft = Loft(x0, x1, up, dn, mid=lambda t: a * (1 - t) + c)
        return Rigid(loft, ps) if ps and ps != IDENT else loft
    m = bend or (lambda q: apply(ps, q) if ps else q)
    deg = ps[0] if ps else 0.0
    if kind == "E":
        cx, cy, rx, ry = s[1:5]
        c = m((cx, cy))
        return Ellipse(c[0], c[1], rx, ry, (s[5] if len(s) > 5 else 0.0) + deg)
    if kind == "T":
        return Tube([m(q) for q in s[1]], list(s[2]))
    if kind == "P":
        return Poly([m(q) for q in s[1]])
    raise ValueError(f"unknown shape {kind}")


def below(curve_pts, ramp_lo, ramp_hi, local=None):
    """Region: points under the curve [(x, y)] use ramp_lo (belly), else ramp_hi."""
    def region(x, y):
        if local:
            x, y = local((x, y))
        return ramp_lo if y > curve(curve_pts, x) else ramp_hi
    return region


class Rig:
    """The pose of one frame: head, jaw, crest and tail groups, legs, arms."""
    def __init__(self, p, phase, step):
        act = p["action"] if phase else {}
        walk = p["walk"] if step else 0.0
        self.p, self.phase, self.step = p, phase, step
        self.head = pose(act.get("head", 0.0) + (p.get("walk_head", 0.0) if step else 0.0), p["neck"])
        self.jaw = pose(act.get("jaw", 0.0), p["jaw_pivot"], then=self.head)
        self.crest = pose(act.get("crest", 0.0), p.get("crest_pivot", (0.0, 0.0)), then=self.head)
        self.tail_deg = act.get("tail", 0.0) + (p.get("walk_tail", 0.0) if step else 0.0)
        self.arm_deg = act.get("arms", 0.0) - (p.get("walk_arms", 0.0) if step else 0.0)
        self.arm_lift = act.get("arm_lift", 0.0)
        self.walk = walk
        self.gaping = bool(act.get("jaw", 0.0))

    def group(self, name):
        return {"head": self.head, "jaw": self.jaw, "crest": self.crest}.get(name)

    def bend(self, q):
        """The tail: rotate about tail_base, more towards the tip."""
        if not self.tail_deg:
            return q
        bx, by = self.p["tail_base"]
        reach = self.p.get("tail_reach", 30.0)
        t = clamp((q[0] - bx) / reach, 0.0, 1.0)
        x, y = rot(q[0] - bx, q[1] - by, self.tail_deg * t)
        return (bx + x, by + y)

    def limb(self, limb, kind):
        """Rigid pose of a leg (walk swing about the hip) or arm (about the shoulder)."""
        piv = limb["pts"][0]
        if kind == "leg":
            deg = self.walk * limb.get("swing", 1)
        else:
            deg = self.arm_deg * (1 if limb.get("near", True) else 0.6)
            lift = self.arm_lift * (1 if limb.get("near", True) else 0.7)
            return pose(deg, piv, then=(0.0, (0.0, -lift)))
        return pose(deg, piv)

    def shape(self, s, group):
        if group == "tail":
            return mk(s, bend=self.bend)
        ps = self.group(group)
        return mk(s, ps) if ps else mk(s)

    def to_local(self, group):
        ps = self.group(group)
        return (lambda q: inverse(ps, q)) if ps else None

    def at(self, group, q):
        """A group-local point in model coordinates."""
        if group == "tail":
            return self.bend(q)
        ps = self.group(group)
        return apply(ps, q) if ps else q


class _FineCanvas(Canvas):
    """A canvas whose `big` follows the species' own battle scale."""
    big = property(lambda self: self._fine)


def fine_details(cv, p):
    """core's Canvas.big means scale >= 0.8, but giants render their battle
    sprites at 0.76-0.9, which would drop eye highlights, scales and claws.
    Fine details here follow the spec: on at the battle scales (front/back),
    off for icons and overworld frames. (Candidate for core: a per-render
    `detail` flag instead of a fixed scale threshold.)"""
    cv.__class__ = _FineCanvas
    cv._fine = cv.scale >= min(p["front"], p["back"]) * 0.97


FAR = dict(light=-0.25)


def limb_parts(rig, limbs, kind, base_ramp):
    """Parts of every leg or arm, posed. Returns (parts, [(limb, pose)])."""
    parts, posed = [], []
    for limb in limbs:
        ps = rig.limb(limb, kind)
        posed.append((limb, ps))
        near = limb.get("near", True)
        ramp = limb.get("ramp", base_ramp)
        z = limb.get("z", 2 if near else -2)
        opt = dict(inner=(ramp, 0)) if near else dict(FAR)
        parts.append(Part(mk(("T", limb["pts"], limb["radii"]), ps), ramp, z=z, **opt))
        if limb.get("thigh"):
            tr = limb.get("thigh_ramp", ramp)
            topt = dict(inner=(tr, 0)) if near else dict(FAR)
            thigh = mk(limb["thigh"], ps)
            if limb.get("thigh_ragged"):
                thigh = Ragged(thigh, *limb["thigh_ragged"])
            parts.append(Part(thigh, tr, z=z + 0.1, flat=limb.get("thigh_flat", 0.5), **topt))
        if limb.get("foot"):
            parts.append(Part(mk(limb["foot"], ps), limb.get("foot_ramp", ramp), z=z + 0.05, **opt))
        if limb.get("wing"):
            wr = limb.get("wing_ramp", "plume")
            wz = limb.get("wing_z", z + 0.2)
            wopt = dict(normal=limb.get("wing_normal", (0, -0.2, 1)), outline="outline", inner=(wr, 0),
                        light=limb.get("wing_light", 0.0))
            if not near:
                wopt["light"] = -0.25
            parts.append(Part(mk(limb["wing"], ps), wr, z=wz, **wopt))
        for x in limb.get("parts", ()):  # claws, scutes, spurs that move with the limb
            xr = x.get("ramp", ramp)
            xo = dict(FAR) if not near else {}
            for k in ("normal", "light", "outline", "inner", "line", "flat"):
                if k in x:
                    xo[k] = x[k]
            parts.append(Part(mk(x["s"], ps), xr, z=z + x.get("z", 0.3), **xo))
    return parts, posed


def extra_parts(rig, p):
    parts = []
    for e in p.get("extras", ()):
        if e.get("phase") is not None and e["phase"] != rig.phase:
            continue
        group = e.get("group", "body")
        kw = dict(z=e.get("z", 1), flat=e.get("flat", 0.5))
        for k in ("normal", "light", "outline", "inner", "line", "shadow"):
            if k in e:
                kw[k] = e[k]
        if e.get("region"):
            lo, pts = e["region"]
            kw["region"] = below(pts, lo, e["ramp"], rig.to_local(group))
        parts.append(Part(rig.shape(e["s"], group), e["ramp"], **kw))
    return parts


def dino_parts(p, rig, body_ramp="skin"):
    """Body, head, jaw, mouth, legs, arms and extras of a side view."""
    belly = p.get("belly_ramp", "belly")
    body = Union([rig.shape(s, "tail" if i in p.get("tail_shapes", ()) else "body")
                  for i, s in enumerate(p["body"])], k=p.get("body_k", 0.15))
    if p.get("body_ragged"):
        body = Ragged(body, *p["body_ragged"])
    parts = [Part(body, body_ramp, z=0, flat=p.get("body_flat", 0.5),
                  region=below(p["belly"], belly, body_ramp) if p.get("belly") else None)]
    lp, legs = limb_parts(rig, p.get("legs", ()), "leg", p.get("leg_ramp", body_ramp))
    ap, arms = limb_parts(rig, p.get("arms", ()), "arm", p.get("arm_ramp", body_ramp))
    parts += lp + ap
    head_ramp = p.get("head_ramp", body_ramp)
    hb = p.get("head_belly")
    parts.append(Part(rig.shape(p["head"], "head"), head_ramp, z=p.get("head_z", 4), flat=p.get("head_flat", 0.5),
                      region=below(hb, belly, head_ramp, rig.to_local("head")) if hb else None))
    if p.get("jaw"):
        jb = p.get("jaw_belly")
        parts.append(Part(rig.shape(p["jaw"], "jaw"), p.get("jaw_ramp", head_ramp), z=p.get("head_z", 4) - 0.1,
                          region=below(jb, belly, p.get("jaw_ramp", head_ramp), rig.to_local("jaw")) if jb else None))
    if p.get("mouth") and rig.gaping:
        parts.append(Part(rig.shape(p["mouth"], "head"), p.get("mouth_ramp", "mouth"), z=p.get("head_z", 4) - 0.2,
                          normal=(0, 0, 1), light=-0.3, line=False, shadow=False))
        if p.get("tongue"):
            parts.append(Part(rig.shape(p["tongue"], "jaw"), p.get("mouth_ramp", "mouth"), z=p.get("head_z", 4) - 0.15,
                              normal=(0, 0, 1), light=0.2, line=False, shadow=False))
    parts += extra_parts(rig, p)
    return parts, legs, arms


# --------------------------------------------------------------- painters

def paint_eye(cv, rig, eye, group="head"):
    c = rig.at(group, eye["c"])
    big = cv.big
    if eye.get("brow") and big:
        cv.polyline([rig.at(group, q) for q in eye["brow"]], None, shade=-2)
    if big:
        r = eye["r"]
        cv.disc(c, r, "outline", only_opaque=True)
        if r >= 1.3:
            cv.disc((c[0] + 0.25, c[1]), r * 0.55, "eye", only_opaque=True)
            px, py = cv.pt(*c)
            cv.set(px, py, "outline")
        px, py = cv.pt(*c)
        cv.set(px + (1 if cv.flip else -1), py - 1, "white")
    else:
        cv.disc(c, max(0.55 / cv.scale, eye.get("r_small", 1.0)), "outline", only_opaque=True)


def paint_textures(cv, rig, p):
    """Sparse screen-aligned patterns on given ramps: scales (lattice), dashes
    (feathers), bands (stripes across the back, in model x with a dorsal limit)."""
    if not cv.big:
        return
    for t in p.get("texture", ()):
        idxs = cv.pal.index[t["ramp"]]
        lo, hi = t.get("levels", (1, len(idxs) - 1))
        allowed = set(idxs[lo:hi + 1])
        kind = t["kind"]
        for py in range(cv.h):
            for px in range(cv.w):
                if cv.idx[py][px] not in allowed:
                    continue
                if kind == "scales":
                    hit = py % t.get("rows", 3) == 0 and (px + py * t.get("shift", 1)) % t.get("cols", 4) == 0
                elif kind == "dashes":
                    hit = py % t.get("rows", 3) == 0 and (px + py) % t.get("cols", 4) in (0, 1)
                elif kind == "bands":
                    x, y = cv.to_model(px + 0.5, py + 0.5)
                    if y > curve(t["top"], x):
                        continue
                    u = (x - t.get("x0", 0.0)) / t["period"]
                    hit = t.get("x0", -99) <= x <= t.get("x1", 99) and (u - math.floor(u)) < t.get("width", 0.35)
                else:
                    raise ValueError(kind)
                if hit:
                    cv.shade(px, py, t.get("delta", -1))


def paint_claws(cv, rig, posed, color="claw"):
    color = rig.p.get("claw_color", color)
    if not cv.big:
        return
    for limb, ps in posed:
        for q in limb.get("claws", ()):
            cv.set(*cv.pt(*apply(ps, q)), color)
        for pts in limb.get("claw_lines", ()):  # hooked claws (sickle claw on toe II)
            cv.polyline([apply(ps, q) for q in pts], color)
        for pts, col in limb.get("lines", ()):  # feather edges, scutes
            ptsm = [apply(ps, q) for q in pts]
            if isinstance(col, int):
                cv.polyline(ptsm, None, shade=col)
            else:
                cv.polyline(ptsm, col)


def paint_lines(cv, rig, lines):
    """[(group, [pts], colour or shade int)]: painted strokes (lip lines, feather
    edges, frill ribs)."""
    for group, pts, col, *only_big in lines:
        if only_big and only_big[0] and not cv.big:
            continue
        ptsm = [rig.at(group, q) for q in pts]
        if isinstance(col, int):
            cv.polyline(ptsm, None, shade=col)
        else:
            cv.polyline(ptsm, col)


def paint_head(cv, rig, p, parts=()):
    big = cv.big
    gaping = rig.gaping
    if big and p.get("lip") and not gaping:
        cv.polyline([rig.at("head", q) for q in p["lip"]], "outline")
    if big and gaping and p.get("teeth"):
        # teeth: 1-2 px spikes on the gape (pixels owned by the mouth part)
        mouth = {i for i, part in enumerate(parts) if part.ramp == p.get("mouth_ramp", "mouth") and part.line is False}
        for grp, key, dy in (("head", "upper", 1), ("jaw", "lower", -1)):
            for q in p["teeth"].get(key, ()):
                px, py = cv.pt(*rig.at(grp, q))
                for yy in (py, py + dy)[:p["teeth"].get("length", 2)]:
                    if cv.inside(px, yy) and cv.owner[yy][px] in mouth:
                        cv.set(px, yy, "white")
    if p.get("nostril"):
        n = p["nostril"]
        if big:
            cv.set(*cv.pt(*rig.at("head", n)), "outline")
    paint_eye(cv, rig, p["eye"])


def side_model(p, phase=0, step=None, body_ramp="skin", extra_details=None):
    if step is not None:
        phase = 0
    rig = Rig(p, phase, step)
    parts, legs, arms = dino_parts(p, rig, p.get("body_ramp", body_ramp))

    def details(cv):
        fine_details(cv, p)
        paint_textures(cv, rig, p)
        paint_lines(cv, rig, p.get("lines", ()))
        paint_claws(cv, rig, legs + arms)
        if extra_details:
            extra_details(cv, rig)
        paint_head(cv, rig, p, parts)

    return Model(parts, p["ramps"], details)


# ===================================================== theropod side view

FOOTPRINT_THEROPOD = [
    "................",
    "................",
    "................",
    ".......#........",
    ".......#........",
    "...#...#...#....",
    "...#...#...#....",
    "....#..#..#.....",
    "....#..#..#.....",
    ".....#.#.#......",
    "......###.......",
    "......###.......",
    ".......#........",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(
    action=dict(head=5.0, jaw=-20.0, tail=-4.0, arms=0.0),
    walk=16.0, walk_tail=3.0, walk_head=-2.0,
    tail_reach=30.0, crest_pivot=(0.0, 0.0), ground=27.0,
    ow=dict(tracks="TRACKS_FOOT"),
)


def side(p, phase=0, step=None):
    return side_model(p, phase, step)


# ================================================== end-on overworld views
# The overworld camera looks down at about 45 degrees, so an animal facing
# south has its head low on the screen in front of its chest and its tail
# rising behind it; facing north the tail comes towards the viewer. end_view()
# projects the side view's own shapes into that camera, so a new spec gets
# usable end-on views from its side geometry plus a few widths:
#   side point (u, y), lateral w  ->  X = w,  Y = ground - h*kh + d*kd,
#   h = ground - y (height), d = -u facing south (head nearer) or u (north).
# Spec `end` dict (all optional):
#   kh, kd           projection factors (default 0.8, 0.5)
#   body_w {i: rw}   lateral radius of body shape i (default ry * 0.85)
#   leg_w, arm_w     lateral offset of the legs / arms (default: 0.6 * torso rw)
#   head             3D shapes (head-local side coords + w) replacing the side
#                    head; default: the side head's bbox as one ellipsoid
#   eyes             (u, y, w) mirrored; eye_r; eye_views (default south only)
#   extras           list of dict(s=3D shape, ramp, z, mirror, view, group,
#                    normal, light, inner, line, outline, region=(ramp, y_below))
#   lines            list of (view, [3D pts], colour or shade int, mirror)
#   belly            south: torso pixels within this fraction of rw from the
#                    centre line and below its centre are belly-coloured
# 3D shapes: ("S", u, y, w, ru, ry, rw) ellipsoid; ("C", [(u, y, w)], radii)
# tube; ("D", u, y, w, rw, rh[, ru]) a disc facing along the body (frills);
# ("Q", [(u, y, w)]) flat polygon. `group` "head" applies the head pose.


class Cam:
    def __init__(self, p, view):
        e = p.get("end", {})
        self.kh, self.kd = e.get("kh", 0.8), e.get("kd", 0.5)
        self.g = p.get("ground", 27.0)
        self.south = view == "south"

    def pt(self, u, y, w=0.0):
        """(X, Y, depth): depth grows towards the viewer."""
        d = -u if self.south else u
        return (w if self.south else -w, self.g - (self.g - y) * self.kh + d * self.kd, d)

    def xy(self, u, y, w=0.0):
        return self.pt(u, y, w)[:2]

    def ell(self, u, y, w, ru, ry, rw):
        X, Y, d = self.pt(u, y, w)
        return Ellipse(X, Y, rw, math.hypot(ry * self.kh, ru * self.kd)), d

    def shape(self, s, ps=None, zoom=None):
        """3D shape data (posed by a side-view rigid pose ps, then scaled by
        zoom=(factor, (u, y) anchor) for chibi heads) -> (2D shape, depth)."""
        f, (au, ay) = zoom or (1.0, (0.0, 0.0))

        def P(u, y):
            u, y = apply(ps, (u, y)) if ps else (u, y)
            return au + (u - au) * f, ay + (y - ay) * f
        k = s[0]
        if k == "R":
            sub, d = self.shape(s[1], ps, zoom)
            return Ragged(sub, *s[2:]), d
        if k == "U":
            subs = [self.shape(x, ps, zoom) for x in s[1]]
            return Union([x[0] for x in subs], k=s[2] if len(s) > 2 else 0.12), max(x[1] for x in subs)
        if k == "S":
            u, y = P(s[1], s[2])
            return self.ell(u, y, s[3] * f, *(v * f for v in s[4:7]))
        if k == "C":
            pts = [self.pt(*P(q[0], q[1]), q[2] * f) for q in s[1]]
            return Tube([q[:2] for q in pts], [r * f for r in s[2]]), sum(q[2] for q in pts) / len(pts)
        if k == "D":
            u, y = P(s[1], s[2])
            X, Y, d = self.pt(u, y, s[3] * f)
            ru = s[6] if len(s) > 6 else 0.5
            return Ellipse(X, Y, s[4] * f, math.hypot(s[5] * self.kh, ru * self.kd) * f), d
        if k == "Q":
            pts = [self.pt(*P(q[0], q[1]), q[2] * f) for q in s[1]]
            return Poly([q[:2] for q in pts]), sum(q[2] for q in pts) / len(pts)
        raise ValueError(k)

    def point(self, q, ps=None, zoom=None):
        f, (au, ay) = zoom or (1.0, (0.0, 0.0))
        u, y = apply(ps, q[:2]) if ps else q[:2]
        return self.xy(au + (u - au) * f, ay + (y - ay) * f, q[2] * f)


def _mirror3(s):
    """The same 3D shape on the other side (w -> -w)."""
    k = s[0]
    if k in ("S", "D"):
        return (k, s[1], s[2], -s[3]) + tuple(s[4:])
    if k == "C":
        return (k, [(u, y, -w) for u, y, w in s[1]], s[2])
    if k == "Q":
        return (k, [(u, y, -w) for u, y, w in s[1]])
    raise ValueError(k)


def end_view(p, view, step, body_ramp="skin"):
    e = p.get("end", {})
    cam = Cam(p, view)
    south = cam.south
    belly = p.get("belly_ramp", "belly")
    rig = Rig(p, 0, step)
    # chibi stylisation: head_shift (du, dy) moves the head (and the end of the
    # neck) forward/down so a high-headed animal faces the camera in front of
    # its chest instead of above it; per view: head_shift_n for north
    hs = e.get("head_shift", (0.0, 0.0)) if south else e.get("head_shift_n", (0.0, 0.0))
    hs = tuple(hs)
    rig.head = (rig.head[0], (rig.head[1][0] + hs[0], rig.head[1][1] + hs[1]))
    items = []  # (depth, Part)
    torso, torso_d = [], []
    tail_idx = set(p.get("tail_shapes", ()))
    rws = e.get("body_w", {})
    for i, s in enumerate(p["body"]):
        if s[0] == "E":
            cx, cy, rx, ry = s[1:5]
            sh, d = cam.ell(cx, cy, 0.0, rx, ry, rws.get(i, ry * 0.85))
            torso.append(sh)
            torso_d.append(d)
        elif s[0] == "T":
            kind = "tail" if i in tail_idx else "neck"
            radii = [r * rws.get(i, 1.0) for r in s[2]]
            if kind == "tail":
                # a raised tail would point at the camera: flatten it towards the
                # base height (tail_flat), and curve it to one side (tail_side,
                # swaying with the step) so it shows beside the body
                y0 = s[1][0][1]
                flat = e.get("tail_flat", 0.3)
                side_w = e.get("tail_side", 6.0) * (1.0 if not step else 0.4)
                drop = 0.0 if south else e.get("tail_drop", 0.0)
                n = len(s[1]) - 1
                pts3 = [(u, y0 + (y - y0) * flat + drop * (k / n) ** 1.5, side_w * (k / n) ** 2)
                        for k, (u, y) in enumerate(s[1])]
            else:
                n = len(s[1]) - 1
                pts3 = [(u + hs[0] * (k / n), y + hs[1] * (k / n), 0.0) for k, (u, y) in enumerate(s[1])]
            sh, d = cam.shape(("C", pts3, radii))
            ramp = e.get(kind + "_ramp", body_ramp)
            items.append((d + e.get(kind + "_z", 0.0),
                          Part(sh, ramp, inner=(ramp, 0),
                               region=_end_belly(e, belly, ramp, sh) if kind == "neck" and south else None)))
    tb = Union(torso, k=p.get("body_k", 0.15))
    t_rw = max(s.r[0] for s in torso)
    t_cx = 0.0
    t_cy = sum(s.c[1] for s in torso) / len(torso)
    bf = e.get("belly", 0.45)
    reg = ((lambda x, y: belly if abs(x - t_cx) < t_rw * bf and y > t_cy else body_ramp) if south else None)
    tdepth = sum(torso_d) / len(torso_d)
    items.append((tdepth, Part(tb, body_ramp, region=reg)))

    # limbs: the near ones, mirrored; in the step pose the two sides swing apart
    for kind, limbs, key in (("leg", p.get("legs", ()), "leg_w"), ("arm", p.get("arms", ()), "arm_w")):
        for limb in limbs:
            if not limb.get("near", True):
                continue
            lw = limb.get("end_w", e.get(key, t_rw * 0.6))
            ramp = limb.get("ramp", p.get(kind + "_ramp", body_ramp))
            for side in (-1, 1):
                if kind == "leg":
                    deg = (p["walk"] * side * limb.get("swing", 1) if step else 0.0)
                else:
                    deg = 0.0
                ps = pose(deg, limb["pts"][0])
                ld = cam.pt(*limb["pts"][0])[2] if e.get("limb_depth", True) else tdepth
                bias = limb.get("end_z", 0.6 if kind == "leg" else 0.8)
                pts3 = [(u, y, side * lw) for u, y in limb["pts"]]
                sh, d = cam.shape(("C", pts3, limb["radii"]), ps)
                items.append((ld + bias + (d - tdepth) * 0.02, Part(sh, ramp, inner=(ramp, 0))))
                if limb.get("thigh"):
                    t = limb["thigh"]
                    tw = limb.get("end_thigh_w", t[3] * 0.75)
                    th, _ = cam.shape(("S", t[1], t[2], side * (lw + tw * 0.25), t[3], t[4], tw), ps)
                    items.append((ld + bias + 0.03, Part(th, ramp, inner=(ramp, 0))))
                if limb.get("foot"):
                    f = limb["foot"]
                    if f[0] == "T":
                        fs, _ = cam.shape(("C", [(u, y, side * lw) for u, y in f[1]], f[2]), ps)
                    else:
                        fs, _ = cam.shape(("S", f[1], f[2], side * lw, f[3], f[4], f[3] * 0.7), ps)
                    fr = limb.get("foot_ramp", ramp)
                    items.append((ld + bias + 0.05, Part(fs, fr, inner=(fr, 0))))
                if limb.get("end_wing"):
                    ws = limb["end_wing"] if side > 0 else _mirror3(limb["end_wing"])
                    sh, _ = cam.shape(ws, ps)
                    wr = limb.get("wing_ramp", "plume")
                    items.append((ld + bias + 0.1, Part(sh, wr, normal=(side * 0.3, -0.3, 1), inner=(wr, 0))))

    # head: 3D shapes in head-local coordinates
    head_ramp = p.get("head_ramp", body_ramp)
    head = e.get("head")
    if head is None:
        x0, y0, x1, y1 = mk(p["head"]).bbox
        head = [("S", (x0 + x1) / 2, (y0 + y1) / 2, 0.0, (x1 - x0) / 2, (y1 - y0) / 2, (y1 - y0) / 2)]
    hz = (e.get("head_zoom", 1.0) if south else e.get("head_zoom_n", 1.0), (p["neck"][0] + hs[0], p["neck"][1] + hs[1]))
    for s in head:
        ramp, kw = head_ramp, {}
        if isinstance(s, dict):
            ramp, kw = s.get("ramp", head_ramp), {k: s[k] for k in ("light", "normal", "flat") if k in s}
            s = s["s"]
        sh, d = cam.shape(s, rig.head, hz)
        items.append((d + 0.5, Part(sh, ramp, inner=(ramp, 0), **kw)))

    for x in e.get("extras", ()):
        if x.get("view", view) != view:
            continue
        shapes = [x["s"]] + ([_mirror3(x["s"])] if x.get("mirror") else [])
        for s in shapes:
            if x.get("group") == "head":
                sh, d = cam.shape(s, rig.head, hz)
                d += 0.5
            else:
                sh, d = cam.shape(s)
            kw = {k: x[k] for k in ("normal", "light", "outline", "inner", "line", "flat") if k in x}
            if x.get("region"):
                lo, yb = x["region"]
                kw["region"] = (lambda X, Y, lo=lo, yb=cam.xy(0, yb)[1], hi=x["ramp"]: lo if Y > yb else hi)
            items.append((d + x.get("z", 0.0), Part(sh, x["ramp"], **kw)))

    items.sort(key=lambda it: it[0])
    parts = []
    for k, (d, part) in enumerate(items):
        part.z = k
        parts.append(part)

    def details(cv):
        paint_textures(cv, rig, dict(texture=[t for t in p.get("texture", ()) if t["kind"] != "bands"]))
        eyes = e.get("eyes")
        if eyes and view in e.get("eye_views", ("south",)):
            r = e.get("eye_r", 1.0)
            for side in (-1, 1):
                c = cam.point((eyes[0], eyes[1], side * eyes[2]), rig.head, hz)
                cv.disc(c, max(0.55 / cv.scale, r), "outline", only_opaque=True)
                if r >= 1.2:
                    px, py = cv.pt(*c)
                    cv.set(px - side, py - 1, "white")
        for v, pts, col, *mir in e.get("lines", ()):
            if v != view:
                continue
            sets = [pts] + ([[(u, y, -w) for u, y, w in pts]] if mir and mir[0] else [])
            for ps_ in sets:
                q = [cam.point(t, rig.head, hz) for t in ps_]
                if isinstance(col, int):
                    cv.polyline(q, None, shade=col)
                else:
                    cv.polyline(q, col)

    return Model(parts, p["ramps"], details)


def _end_belly(e, belly, ramp, sh):
    """South view of the neck: pale throat down its centre line."""
    k = e.get("throat", 0.4)
    r = max(sh.rad)
    return lambda x, y: belly if abs(x) < r * k else ramp


def overworld(p, view, step):
    return end_view(p, view, step, p.get("body_ramp", "skin"))


PLAN = BodyPlan(
    "theropod", "bipedal theropods: tyrannosaurs, dromaeosaurs (feathered), oviraptorosaurs",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_THEROPOD, tracks="TRACKS_FOOT",
)
