"""bird_ground body plan: ground fowl and Gastornis-sized galloanserans in side
view. Template species: Asteriornis (the bird starter). This module is also the
shared bird template of the bird lane: plans/crane_raptor.py and
plans/bird_flying.py import `bird_model`, `overworld` and the helpers from here.

Species (taxonomy.py):
    asteriornis   Asteriornis (Maastricht Fm, Belgium (stand-in), 0.4 kg)
    gallinuloid   Gallinuloides (Green River Fm, WY, 0.3 kg)
    meleagris     Meleagris gallopavo (Natural Trap Cave, WY, 8 kg)
    centrocercus  Centrocercus urophasianus (Living; MT, 2.5 kg)
    gastornis     Gastornis (Willwood Fm, WY, 160 kg)

Ramps (a spec may add its own for `extra` parts and `marks`):
    outline   1 colour
    body      main plumage, 3-4 shades
    belly     underside / breast (optional, else body)
    wing      folded wing and tail (optional, else body)
    beak      2 shades        leg   tarsus and toes, 2 shades
Any ramp may be named in `regions`, `extra`, `marks`, `head_ramp`, `tail_ramp`.

Geometry (model units, head to the LEFT, ground at y ~ 24):
    body        list of ellipses (cx, cy, rx, ry, angle), smooth-unioned
    regions     list of rules colouring parts of the body/neck/head, first match wins:
                dict(ramp, below=(a, b))  y > a + b*x     dict(ramp, above=(a, b))
                dict(ramp, ellipse=(cx, cy, rx, ry))      dict(ramp, right=x) / left=x
                add on="head" to apply a rule to the head and neck only, on="body" for
                the body only (default: both)
    neck        dict(pts, radii): Tube from the body to the head
    head        list of ellipses; `head_ramp` (default body)
    beak        dict(upper=dict(pts, radii), lower=dict(pts, radii), hinge=(x, y))
    wing        dict(coverts=[ellipses], primaries=dict(pts, radii), root=(x, y)) or None
    tail        list of polygons (fans, spikes) or Tubes (dict(pts, radii)); `tail_root`
    legs        list of dict(near, hip, ankle, foot, toes=[tip...], hallux=tip or None,
                tibia_r=(r0, r1), tarsus_r=(r0, r1), toe_r, swing=+1|-1, tibia_ramp)
    eye         ((x, y), r_big, r_small); eye_ring = colour or None; iris = colour or None
    extra       list of dict(shape="ellipse"|"tube"|"poly", args, ramp, z, on="head"|"body"|
                "tail"|"wing"|None, phase=None|0|1, flat, light, normal, inner, line)
    marks       painted details: list of dict(pts, color | shade, on, big=True, r=None,
                phase=None|0|1, only_opaque=True). With r: discs at each point.
    scallops    dict(ramps=(...), rows, period, shift): sparse darker feather-edge pixels
    tarsus_scutes  True: alternate darker pixels down the near tarsus
Frame 2 (phase 1) actions, any combination: head_turn (deg about `neck_pivot`,
positive = head down/forward), gape (deg), tail_lift (deg, positive raises),
wing_lift (deg, positive raises the wing tip).
Walk step 1 swings the legs about the hips by walk_swing.
"""

import math

from ..core.geom import Ellipse, Tube, Union, Poly, Part, Model, turn
from ..core.plan import BodyPlan

FOOTPRINT_BIRD = [
    "................",
    "................",
    "................",
    ".......#........",
    ".......#........",
    "...#...#...#....",
    "....#..#..#.....",
    ".....#.#.#......",
    "......###.......",
    ".......#........",
    ".......#........",
    "................",
    "................",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(
    far_light=-0.25, walk_swing=20, head_k=0.10, body_k=0.2, wing_k=0.10,
    head_turn=0.0, gape=0.0, tail_lift=0.0, wing_lift=0.0, neck_pivot=None,
    head_ramp="body", neck_ramp=None, beak_ramp="beak", leg_ramp="leg", wing_ramp="wing", tail_ramp="wing",
    regions=(), extra=(), marks=(), scallops=None, tarsus_scutes=True,
    eye_ring=None, iris=None, eye_hi=None, claws=True, tail=(), tail_root=(14.0, 0.0),
    wing=None, ow=dict(tracks="TRACKS_FOOT"),
)


def ramp_or(p, name, *fallbacks):
    """`name` if the spec has that ramp, else the first fallback it has."""
    for n in (name,) + fallbacks:
        if n in p["ramps"]:
            return n
    return "body"


def make_shape(kind, args):
    if kind == "ellipse":
        return Ellipse(*args)
    if kind == "tube":
        return Tube(*args)
    if kind == "poly":
        return Poly(list(args))
    raise ValueError(f"bird plan: unknown shape {kind}")


def _move_shape(kind, args, f):
    """The shape args with every point mapped by f (rotation keeps radii)."""
    if kind == "ellipse":
        cx, cy, rx, ry, *a = args
        x, y = f((cx, cy))
        return (x, y, rx, ry, *a)
    if kind == "tube":
        pts, radii = args
        return ([f(q) for q in pts], radii)
    return [f(q) for q in args]


def _rule_hit(rule, x, y):
    if "below" in rule:
        a, b = rule["below"]
        return y > a + b * x
    if "above" in rule:
        a, b = rule["above"]
        return y < a + b * x
    if "ellipse" in rule:
        cx, cy, rx, ry = rule["ellipse"]
        return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1
    if "right" in rule:
        return x > rule["right"]
    if "left" in rule:
        return x < rule["left"]
    return False


def region_fn(p, base, where, inverse=None):
    """A Part.region: the first rule (of those for `where`) that matches the point."""
    rules = [r for r in p["regions"] if r.get("on", where) == where]
    if not rules:
        return None

    def region(x, y):
        if inverse:
            x, y = inverse((x, y))
        for r in rules:
            if _rule_hit(r, x, y):
                return r["ramp"]
        return base
    return region


class Pose:
    """The point transforms of one frame: head (H), wing (W), tail (T)."""
    def __init__(self, p, phase):
        on = bool(phase)
        self.head_deg = p["head_turn"] if on else 0.0
        self.gape = p["gape"] if on else 0.0
        self.wing_deg = p["wing_lift"] if on else 0.0
        self.tail_deg = p["tail_lift"] if on else 0.0
        neck = p["neck"]["pts"] if p.get("neck") else [(0.0, 0.0)]
        self.pivot = p["neck_pivot"] or neck[0]
        self.wing_root = (p["wing"] or {}).get("root", (0.0, 0.0))
        self.tail_root = p["tail_root"]
        self.hinge = p["beak"].get("hinge", (0.0, 0.0)) if p.get("beak") else (0.0, 0.0)

    def H(self, q):
        return turn(q, self.pivot, self.head_deg)

    def Hinv(self, q):
        return turn(q, self.pivot, -self.head_deg)

    def J(self, q):  # lower jaw: opens downward about the hinge, then follows the head
        return self.H(turn(q, self.hinge, -self.gape))

    def W(self, q):
        return turn(q, self.wing_root, -self.wing_deg)

    def T(self, q):
        return turn(q, self.tail_root, -self.tail_deg)

    def on(self, where):
        return {"head": self.H, "wing": self.W, "tail": self.T, "jaw": self.J}.get(where, lambda q: q)


def leg_parts(p, leg, phase, step, ramps_far):
    """Tibia (feathered or bare), tarsus, toes for one leg. Returns (parts, toe tips, tarsus pts)."""
    hip, ankle, foot = leg["hip"], leg["ankle"], leg["foot"]
    toes = list(leg.get("toes", []))
    hallux = leg.get("hallux")
    lift = leg.get("lift", 0.0) if phase else 0.0
    if lift:
        ankle = (ankle[0], ankle[1] - lift * 0.5)
        foot = (foot[0], foot[1] - lift)
        toes = [(x, y - lift) for x, y in toes]
        hallux = (hallux[0], hallux[1] - lift) if hallux else None
    if step:
        deg = p["walk_swing"] * leg.get("swing", 1)
        R = lambda q: turn(q, hip, deg)  # noqa: E731
        ankle, foot = R(ankle), R(foot)
        toes = [R(q) for q in toes]
        hallux = R(hallux) if hallux else None
    near = leg["near"]
    z = leg.get("z", 1.0 if near else -2.0)
    kw = {} if near else dict(light=p["far_light"])
    leg_ramp = ramp_or(p, p["leg_ramp"], "leg")
    tib_ramp = leg.get("tibia_ramp") or ramp_or(p, "thigh", "belly", "body")
    tr = leg.get("toe_r", 0.75)
    parts = [Part(Tube([hip, ankle], list(leg["tibia_r"])), tib_ramp, z=z,
                  inner=(tib_ramp, 0), **kw),
             Part(Tube([ankle, foot], list(leg["tarsus_r"])), leg_ramp, z=z + 0.1,
                  inner=(leg_ramp, 0), **kw)]
    toe_tubes = [Tube([foot, t], [tr * 1.15, tr * 0.8]) for t in toes]
    if hallux:
        toe_tubes.append(Tube([foot, hallux], [tr, tr * 0.7]))
    if toe_tubes:
        parts.append(Part(Union(toe_tubes, k=0.05) if len(toe_tubes) > 1 else toe_tubes[0],
                          leg_ramp, z=z + 0.2, inner=(leg_ramp, 0), **kw))
    tips = toes + ([hallux] if hallux else [])
    return parts, tips, (ankle, foot)


def bird_model(p, phase=0, step=None, wing_parts=None, extra_details=None):
    """The side view. `wing_parts(p, pose)` may replace the folded wing (bird_flying);
    `extra_details(cv, pose)` paints after the standard details."""
    if step is not None:
        phase = 0
    pose = Pose(p, phase)
    H = pose.H
    far = dict(light=p["far_light"])
    body_r = ramp_or(p, "body")
    parts = []

    # legs (far ones behind the body)
    near_legs = []
    for leg in p["legs"]:
        lp, tips, tars = leg_parts(p, leg, phase, step, far)
        parts += lp
        if leg["near"]:
            near_legs.append((tips, tars))

    # tail: fans/spikes behind the body
    tail_r = ramp_or(p, p["tail_ramp"], "wing", "body")
    frame = phase if step is None else 0
    for t in p["tail"]:
        if isinstance(t, dict):
            if t.get("phase") is not None and t["phase"] != frame:
                continue
            if "poly" in t:
                parts.append(Part(Poly([pose.T(q) for q in t["poly"]]), t.get("ramp", tail_r), z=t.get("z", -1),
                                  normal=t.get("normal", (-0.25, -0.35, 0.9)), light=t.get("light", 0.0)))
            else:
                shape = Tube([pose.T(q) for q in t["pts"]], t["radii"])
                parts.append(Part(shape, t.get("ramp", tail_r), z=t.get("z", -1), flat=0.4,
                                  light=t.get("light", 0.0)))
        else:
            parts.append(Part(Poly([pose.T(q) for q in t]), tail_r, z=-1, normal=(-0.25, -0.35, 0.9)))

    body = Union([Ellipse(*e) for e in p["body"]], k=p["body_k"])
    parts.append(Part(body, body_r, z=0, flat=0.5, region=region_fn(p, body_r, "body")))

    # wing (folded on the flank, nearer than the body and thigh)
    if wing_parts:
        parts += wing_parts(p, pose)
    elif p["wing"]:
        w = p["wing"]
        shapes = [Ellipse(*pose.W(e[:2]), *e[2:4], (e[4] if len(e) > 4 else 0) - pose.wing_deg)
                  for e in w["coverts"]]
        if w.get("primaries"):
            pr = w["primaries"]
            shapes.append(Tube([pose.W(q) for q in pr["pts"]], pr["radii"]))
        wr = ramp_or(p, p["wing_ramp"], "body")
        parts.append(Part(Union(shapes, k=p["wing_k"]), wr, z=2, flat=0.45, inner=(wr, 0),
                          region=region_fn(p, wr, "wing", pose.W) if any(r.get("on") == "wing" for r in p["regions"]) else None))

    # neck and head
    # head and neck are one smooth shape that blends into the breast (no collar line)
    head_r = ramp_or(p, p["head_ramp"], "body")
    shapes = [Ellipse(*H(e[:2]), e[2], e[3], (e[4] if len(e) > 4 else 0) + pose.head_deg) for e in p["head"]]
    if p.get("neck"):
        n = p["neck"]
        bend = n.get("bend", 1.0)  # how much of the head turn the neck's middle points follow
        pts = [n["pts"][0]] + [turn(q, pose.pivot, pose.head_deg * (1.0 if k == len(n["pts"]) - 2 else bend))
                               for k, q in enumerate(n["pts"][1:])]
        shapes.append(Tube(pts, n["radii"]))
    parts.append(Part(Union(shapes, k=p["head_k"]), head_r, z=3, flat=0.5, line=p.get("head_line", False),
                      region=region_fn(p, head_r, "head", pose.Hinv)))

    # beak: upper over lower, so the gape line is the upper's dark edge
    bk = p["beak"]
    beak_r = ramp_or(p, p["beak_ramp"], "beak")
    if bk.get("lower"):
        lo = bk["lower"]
        parts.append(Part(Tube([pose.J(q) for q in lo["pts"]], lo["radii"]), beak_r, z=3.4, flat=0.4,
                          inner=(beak_r, 0), light=-0.1))
    up = bk["upper"]
    parts.append(Part(Tube([H(q) for q in up["pts"]], up["radii"]), beak_r, z=3.5, flat=0.4, inner=(beak_r, 0)))

    # extra parts (wattles, ruffs, crests, air sacs, spikes ...)
    for e in p["extra"]:
        if e.get("phase") is not None and e["phase"] != (phase if step is None else 0):
            continue
        f = pose.on(e.get("on"))
        shape = make_shape(e["shape"], _move_shape(e["shape"], e["args"], f))
        kw = dict(z=e.get("z", 3.2), flat=e.get("flat", 0.5), light=e.get("light", 0.0),
                  line=e.get("line", True), shadow=e.get("shadow", True))
        if e.get("normal"):
            kw["normal"] = e["normal"]
        if e.get("inner"):
            kw["inner"] = e["inner"]
        if e.get("outline"):
            kw["outline"] = e["outline"]
        parts.append(Part(shape, e["ramp"], **kw))

    def details(cv):
        big = cv.big
        if big and p["scallops"]:
            sc = p["scallops"]
            allowed = set()
            for r in sc["ramps"]:
                idx = cv.pal.index[r]
                allowed |= set(idx[1:len(idx) - (0 if sc.get("light", False) else 1)])
            rows, period, shift = sc.get("rows", 3), sc.get("period", 4), sc.get("shift", 2)
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in allowed and py % rows == 0 and (px + (py // rows) * shift) % period == 0:
                        cv.shade(px, py, sc.get("delta", -1))
        if big and p["tarsus_scutes"]:
            for tips, (a, b) in near_legs:
                for px, py in cv.pixels_on_line(a, b):
                    if py % 2 == 0:
                        cv.shade(px, py, -1)
        for m in p["marks"]:
            if m.get("big", True) and not big:
                continue
            if m.get("small") and big:
                continue
            if m.get("phase") is not None and m["phase"] != (phase if step is None else 0):
                continue
            f = pose.on(m.get("on"))
            pts = [f(q) for q in m["pts"]]
            only = m.get("only_opaque", True)
            if m.get("r"):
                for q in pts:
                    cv.disc(q, m["r"], m.get("color"), only_opaque=only)
            elif "shade" in m:
                cv.polyline(pts, None, shade=m["shade"])
            elif len(pts) == 1:
                cv.set(*cv.pt(*pts[0]), m["color"], only)
            else:
                cv.polyline(pts, m["color"], only_opaque=only)
        if big and p["claws"]:
            for tips, _ in near_legs:
                for q in tips:
                    cv.set(*cv.pt(*q), "outline")
        _eye(cv, p, pose)
        if extra_details:
            extra_details(cv, pose)

    return Model(parts, p["ramps"], details)


def _eye(cv, p, pose):
    c, r_big, r_small = p["eye"]
    e = pose.H(c)
    hi = p["eye_hi"] or (ramp_or(p, "white", "belly", "body"), -1)
    if cv.big:
        if p["eye_ring"]:
            cv.disc(e, r_big + 0.9, p["eye_ring"], only_opaque=True)
        if p["iris"]:
            cv.disc(e, r_big, "outline")
            cv.disc(e, r_big - 0.55, p["iris"])
            cv.disc(e, max(0.5, r_big - 1.4), "outline")
        else:
            cv.disc(e, r_big, "outline")
        px, py = cv.pt(*e)
        cv.set(px + (1 if cv.flip else -1) * (1 if r_big > 1.6 else 0), py - (1 if r_big > 1.6 else 0), hi)
    else:
        if p["eye_ring"] and cv.scale > 0.6:
            cv.disc(e, r_small + 0.8, p["eye_ring"], only_opaque=True)
        cv.disc(e, r_small, "outline")


def side(p, phase=0, step=None):
    return bird_model(p, phase, step)


# ---------------------------------------------------------------------------
# Overworld end-on views, derived from the side parameters
# ---------------------------------------------------------------------------

def dims(p):
    tops = [cy - ry for cx, cy, rx, ry, *a in p["body"]]
    bots = [cy + ry for cx, cy, rx, ry, *a in p["body"]]
    t_top, t_bot = min(tops), max(bots)
    ground = max(max([leg["foot"][1]] + [t[1] for t in leg.get("toes", [])]) for leg in p["legs"])
    hx, hy, hrx, hry, *_ = p["head"][0]
    return dict(t_top=t_top, t_bot=t_bot, t_cy=(t_top + t_bot) / 2, t_ry=(t_bot - t_top) / 2,
                ground=ground, h_cy=hy, h_r=max(hrx, hry), h_ry=hry)


def overworld(p, view, step):
    """South: breast, head and beak towards the camera, legs below. North: the
    back with the folded wings, tail towards the camera, head behind. Shapes come
    from the side parameters; `ow_end` overrides: body_w, head_w, neck (bool),
    head_dy, tail (\"fan\" | \"wedge\" | \"spikes\" | None), beak_len, leg_x, crest
    (list of extra-style dicts drawn on the head in both views)."""
    d = dims(p)
    o = dict(body_w=1.3, head_w=1.35, head_dy=1.5, tail="wedge", beak_len=None, leg_x=0.3,
             wings=True, beak_w=None, foot_w=1.0, leg_top=0.35, leg_len=1.0, leg_w=1.1)
    o.update(p.get("ow_end", {}))
    T = d["t_ry"]
    body_cy = d["t_cy"]
    # long legs are shortened end-on (`leg_len`), so tall birds keep their necks in 32 px
    ground = d["t_bot"] + (d["ground"] - d["t_bot"]) * o["leg_len"]
    bw = T * o["body_w"]
    h_r = d["h_ry"] * o["head_w"]
    h_cy = d["h_cy"] + o["head_dy"]
    body_r = ramp_or(p, "body")
    belly_r = ramp_or(p, o.get("belly", "belly"), "belly", "body")
    wing_r = ramp_or(p, p["wing_ramp"], "body")
    tail_r = ramp_or(p, p["tail_ramp"], "wing", "body")
    head_r = ramp_or(p, p["head_ramp"], "body")
    neck_r = ramp_or(p, p["neck_ramp"] or p["head_ramp"], "body")
    leg_r = ramp_or(p, p["leg_ramp"], "leg")
    beak_r = ramp_or(p, p["beak_ramp"], "beak")
    far = dict(light=p["far_light"])
    lift = (1.6, 0.0) if step else (0.0, 0.0)
    bob = 0.5 if step else 0.0
    parts = []
    near_leg = next((lg for lg in p["legs"] if lg["near"]), p["legs"][-1])
    tr0, tr1 = near_leg["tarsus_r"]
    leg_top = d["t_bot"] - T * o["leg_top"]
    for k, s in enumerate((-1, 1)):
        x = s * bw * o["leg_x"]
        fy = ground - 0.8 - lift[k]
        parts.append(Part(Tube([(x, leg_top), (x, fy)], [tr0 * o["leg_w"], tr1 * o["leg_w"] / 1.1]), leg_r, z=-0.5 if view == "south" else 0.5,
                          inner=(leg_r, 0)))
        if view == "south":  # toes splay towards the camera
            toes = [Tube([(x, fy), (x + dx * o["foot_w"], fy + 1.2)], [0.85, 0.6]) for dx in (-2.0, 0.0, 2.0)]
            parts.append(Part(Union(toes, k=0.05), leg_r, z=-0.4, inner=(leg_r, 0)))
        else:
            parts.append(Part(Tube([(x, fy), (x, fy + 1.0)], [0.9, 0.7]), leg_r, z=0.6, inner=(leg_r, 0)))
    ends = list(p.get("ow_extra", ()))
    if view == "south":
        if o["tail"] == "fan":  # a raised fan shows behind the body
            fan = p.get("ow_fan", (T * 1.9, T * 1.25))
            parts.append(Part(Ellipse(0, body_cy - T * 0.55 - bob, fan[0], fan[1]), tail_r, z=-2, flat=0.35, **far))
        elif o["tail"] == "spikes":
            spikes = [Poly([(s * 0.9 * k, body_cy - T * 0.3), (s * (k * 2.8 + 1.2), body_cy - T * 1.9 + abs(k) * 1.3),
                            (s * (k * 2.8 + 2.4), body_cy - T * 0.2)]) for k in (0, 1, 2) for s in (-1, 1)]
            for sp in spikes:
                parts.append(Part(sp, tail_r, z=-2, normal=(0, -0.3, 0.95), **far))
        if o["wings"]:
            for s in (-1, 1):
                parts.append(Part(Ellipse(s * bw * 0.78, body_cy - 0.5 - bob, bw * 0.42, T * 0.9, s * 10), wing_r,
                                  z=-0.2, **far))
        parts.append(Part(Ellipse(0, body_cy - bob, bw, T), body_r, z=0,
                          region=lambda x, y: belly_r if abs(x) < bw * 0.62 and y > body_cy - T * 0.5 - bob else body_r))
        if o.get("neck", True) and h_cy + h_r < body_cy - T * 0.4:
            parts.append(Part(Tube([(0, body_cy - T * 0.6 - bob), (0, h_cy - bob)], [h_r * 0.62, h_r * 0.55]),
                              neck_r, z=0.5, inner=(neck_r, 0)))
        parts.append(Part(Ellipse(0, h_cy - bob, h_r * 0.92, h_r * 0.95), head_r, z=1, inner=(head_r, 0)))
        bl = o["beak_len"] or 3.0
        bwid = o["beak_w"] or h_r * 0.32
        beak_poly = Poly([(-bwid, h_cy - bob + h_r * 0.05), (bwid, h_cy - bob + h_r * 0.05),
                          (0, h_cy - bob + h_r * 0.05 + bl)])
        parts.append(Part(beak_poly, beak_r, z=1.5, normal=(-0.2, -0.3, 0.93), inner=(beak_r, 0)))
        for e in ends:
            if e.get("view", "south") != "south":
                continue
            args = _move_shape(e["shape"], e["args"], lambda q: (q[0], q[1] - bob))
            parts.append(Part(make_shape(e["shape"], args), e["ramp"], z=e.get("z", 1.2), flat=e.get("flat", 0.5),
                              normal=e.get("normal"), light=e.get("light", 0.0), inner=e.get("inner"),
                              line=e.get("line", True)))

        def details(cv):
            for s in (-1, 1):
                ex = s * h_r * 0.5
                if p["eye_ring"]:
                    cv.disc((ex, h_cy - bob - h_r * 0.2), 0.9 / cv.scale + 0.3, p["eye_ring"], only_opaque=True)
                cv.disc((ex, h_cy - bob - h_r * 0.2), 0.7 / cv.scale, "outline")
            for m in p.get("ow_marks", ()):
                if m.get("view", "south") == "south":
                    pts = [(x, y - bob) for x, y in m["pts"]]
                    if m.get("r"):
                        for q in pts:
                            cv.disc(q, m["r"], m["color"], only_opaque=True)
                    else:
                        cv.polyline(pts, m["color"])
        return Model(parts, p["ramps"], details)

    # north: from behind
    parts.append(Part(Ellipse(0, body_cy - bob, bw, T), wing_r if o["wings"] else body_r, z=0,
                      region=(lambda x, y: body_r if abs(x) < bw * 0.18 and y < body_cy - bob else wing_r)
                      if o["wings"] else None))
    if o["wings"]:
        for s in (-1, 1):  # folded wings meet over the rump
            parts.append(Part(Ellipse(s * bw * 0.45, body_cy + T * 0.15 - bob, bw * 0.55, T * 0.85, -s * 12), wing_r,
                              z=0.3, inner=(wing_r, 0)))
    if o["tail"] == "fan":
        fan = p.get("ow_fan", (T * 1.9, T * 1.25))
        parts.append(Part(Ellipse(0, body_cy - T * 0.55 - bob, fan[0], fan[1]), tail_r, z=1.2, flat=0.35))
    elif o["tail"] == "spikes":
        for k in (0, 1, 2):
            for s in (-1, 1):
                parts.append(Part(Poly([(s * 0.9 * k, body_cy - bob), (s * (k * 2.8 + 1.2), body_cy - T * 1.9 + abs(k) * 1.3),
                                        (s * (k * 2.8 + 2.4), body_cy + 0.5)]), tail_r, z=1.2,
                                  normal=(0, -0.3, 0.95)))
    elif o["tail"] == "wedge":
        sway = 0.8 if step else -0.4
        parts.append(Part(Poly([(-T * 0.38, body_cy + T * 0.25 - bob), (T * 0.38, body_cy + T * 0.25 - bob),
                                (sway + T * 0.18, body_cy + T * 1.05 - bob), (sway - T * 0.18, body_cy + T * 1.05 - bob)]),
                          tail_r, z=1.2, normal=(0, -0.2, 0.97)))
    if o.get("neck", True) and h_cy + h_r < body_cy - T * 0.4:
        parts.append(Part(Tube([(0, body_cy - T * 0.6 - bob), (0, h_cy - bob)], [h_r * 0.62, h_r * 0.55]),
                          neck_r, z=-0.5, light=-0.1))
    parts.append(Part(Ellipse(0, h_cy - bob, h_r * 0.92, h_r * 0.95), head_r, z=-0.4, light=-0.1))
    for e in ends:
        if e.get("view", "south") != "north":
            continue
        args = _move_shape(e["shape"], e["args"], lambda q: (q[0], q[1] - bob))
        parts.append(Part(make_shape(e["shape"], args), e["ramp"], z=e.get("z", -0.3), flat=e.get("flat", 0.5),
                          normal=e.get("normal"), light=e.get("light", 0.0), inner=e.get("inner"),
                          line=e.get("line", True)))

    def details_n(cv):
        for m in p.get("ow_marks", ()):
            if m.get("view") == "north":
                pts = [(x, y - bob) for x, y in m["pts"]]
                if m.get("r"):
                    for q in pts:
                        cv.disc(q, m["r"], m["color"], only_opaque=True)
                else:
                    cv.polyline(pts, m["color"])
    return Model(parts, p["ramps"], details_n)


PLAN = BodyPlan(
    "bird_ground", "ground fowl and terror-bird-sized galloanserans: galliforms, Gastornis",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_BIRD, tracks="TRACKS_FOOT",
)
