"""Small-mammal body plan: generalised small quadrupeds in side view
(multituberculates, cimolestids, condylarths, early marsupials).
Template species: Mesodma.

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

from ..core.geom import Ellipse, Tube, Union, Part, Model, turn
from ..core.plan import BodyPlan

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

DEFAULTS = dict(
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


def side(p, phase=0, step=None):
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


def overworld(p, view, step):
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


PLAN = BodyPlan(
    "small_mammal", "generalised small quadrupeds: multituberculates, cimolestids, condylarths, early marsupials",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_MAMMAL, tracks="TRACKS_FOOT",
)
