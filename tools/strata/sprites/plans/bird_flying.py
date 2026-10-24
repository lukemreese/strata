"""bird_flying body plan: small flying/perching birds with the wings half-open
(enantiornithines). Template species: Avisaurus.

Species (taxonomy.py):
    avisaurus     Avisaurus archibaldi (Hell Creek Fm, MT, 1 kg)

Built on the shared bird template (plans/bird_ground.py `bird_model`; read its
docstring for the body, head, beak, legs, regions, extra and marks keys). Added
here:
    spread      the half-open near wing as a feathered polygon: dict(poly=[...] leading
                edge then the notched trailing edge, coverts=(cx, cy, rx, ry, angle),
                claw=dict(pts, radii) or None, far=(dx, dy) offset of the far wing,
                root=(x, y) the shoulder, about which frame 2 raises both wings by
                `wing_lift` degrees)
    perch       dict(pts, radii, ramp): the branch in the battle sprites (not in
                the overworld, where the bird hops and flutters)
    feather_lines  list of polylines on the near wing (shaded one step darker)
    leg_ramp    ramp of the tarsi and toes
Overworld: west = the side view with the wings flapping (step 1 = wings up, legs
tucked); south and north = the bird face-on/from behind with both wings spread,
flapping between steps. TRACKS_NONE (it flutters).
The back sprite is a dedicated view from behind with both wings half-spread.
"""

import math

from ..core.geom import Ellipse, Tube, Union, Poly, Part, Model, turn
from ..core.plan import BodyPlan
from .bird_ground import DEFAULTS as BIRD_DEFAULTS, bird_model, ramp_or

DEFAULTS = dict(BIRD_DEFAULTS, walk_swing=0, spread=None, perch=None, feather_lines=(),
                ow=dict(tracks="TRACKS_NONE"))

WING = dict(normal=(-0.25, -0.45, 0.86))


def _wings(p, lift, ramps_far=True):
    """Parts for the far and near spread wings, rotated `lift` degrees up about the shoulder."""
    sp = p["spread"]
    root = sp["root"]
    W = lambda q: turn(q, root, -lift)  # noqa: E731
    wr = ramp_or(p, p["wing_ramp"], "body")
    dx, dy = sp.get("far", (3.0, -3.0))
    far_poly = Poly([W((x + dx, y + dy)) for x, y in sp["poly"]])
    near_poly = Poly([W(q) for q in sp["poly"]])
    cx, cy, rx, ry, a = sp["coverts"]
    cov = Ellipse(*W((cx, cy)), rx, ry, a - lift)
    parts = [Part(far_poly, wr, z=-2.5, light=p["far_light"] - 0.05, **WING),
             Part(near_poly, wr, z=2, inner=(wr, 0), **WING),
             Part(cov, wr, z=2.2, flat=0.45, light=0.12, inner=(wr, 0))]
    if sp.get("claw"):
        c = sp["claw"]
        parts.append(Part(Tube([W(q) for q in c["pts"]], c["radii"]), ramp_or(p, p["leg_ramp"], "beak"), z=2.3))
    return parts, W


def side(p, phase=0, step=None):
    flying = step is not None
    q = dict(p)
    q["wing"] = dict(root=p["spread"]["root"], coverts=[])  # so marks on="wing" follow the spread wing
    if flying:  # flapping: wings up on step 1, legs tucked under the body
        lift = p["wing_lift"] if step else -6.0
        q["legs"] = [dict(leg, ankle=turn(leg["ankle"], leg["hip"], -50), foot=turn(leg["foot"], leg["hip"], -50),
                          toes=[turn(t, leg["hip"], -50) for t in leg.get("toes", [])],
                          hallux=turn(leg["hallux"], leg["hip"], -50) if leg.get("hallux") else None)
                     for leg in p["legs"]]
        q["wing_lift"] = 0.0
    else:
        lift = p["wing_lift"] if phase else 0.0
    holder = {}

    def wing_parts(pp, pose):
        parts, W = _wings(pp, lift)
        holder["W"] = W
        return parts

    def extra_details(cv, pose):
        W = holder["W"]
        if cv.big:
            for line in p["feather_lines"]:
                cv.polyline([W(pt) for pt in line], None, shade=-1)

    m = bird_model(q, 0 if flying else phase, None if flying else step,
                   wing_parts=wing_parts, extra_details=extra_details)
    if p["perch"] and not flying:
        pr = p["perch"]
        m.parts.append(Part(Tube(pr["pts"], pr["radii"]), pr.get("ramp", "leg"), z=0.5, flat=0.4))
    return m


def _end_view(p, view, flap, scale=1.0, zoom_head=1.25):
    """The bird from the front (south) or behind (north/back) with both wings spread.
    flap: wing angle in degrees above horizontal."""
    body_r = ramp_or(p, "body")
    belly_r = ramp_or(p, "belly", "body")
    wing_r = ramp_or(p, p["wing_ramp"], "body")
    beak_r = ramp_or(p, "beak")
    leg_r = ramp_or(p, p["leg_ramp"], "leg")
    hx, hy, hrx, hry, *_ = p["head"][0]
    s = scale
    T = 7.0 * s
    body_cy = 2.0 * s
    h_r = hry * zoom_head * s
    h_cy = body_cy - T - h_r * 0.45
    span = 15.0 * s
    parts, lines, bars = [], [], []
    for side_ in (-1, 1):
        a = math.radians(flap)
        sx = lambda r, up: (side_ * (T * 0.5 + r * math.cos(a)), body_cy - T * 0.4 - r * math.sin(a) + up)  # noqa: E731
        # leading edge out to the tip, then a notched trailing edge back to the body
        poly = [(side_ * T * 0.3, body_cy - T * 0.7), sx(span * 0.45, -1.5 * s), sx(span, 0.0),
                sx(span * 0.92, 2.2 * s), sx(span * 0.8, 1.8 * s), sx(span * 0.7, 3.2 * s), sx(span * 0.55, 2.8 * s),
                sx(span * 0.4, 4.0 * s), (side_ * T * 0.4, body_cy + T * 0.2)]
        z = -1 if view == "south" else 1
        inner_r = body_r if view != "south" else wing_r   # from behind: paler coverts, dark primaries
        parts.append(Part(Poly(poly), wing_r, z=z, light=-0.1 if view == "south" else 0.0, inner=(wing_r, 0),
                          region=lambda x, y, ir=inner_r: ir if abs(x) < T * 0.5 + span * 0.42 else wing_r, **WING))
        if view != "south":  # coverts: a rounded band along the leading edge
            c = sx(span * 0.32, 1.0 * s)
            parts.append(Part(Ellipse(c[0], c[1], span * 0.3, 2.6 * s, -side_ * flap), wing_r, z=z + 0.1,
                              flat=0.45, light=0.12, inner=(wing_r, 0)))
        for r0, r1, u0, u1 in ((0.66, 0.9, 0.5, 1.6), (0.56, 0.74, 1.2, 2.8), (0.46, 0.6, 1.8, 3.4),
                               (0.36, 0.44, 2.4, 3.8)):  # flight feathers fanning to the notches
            lines.append([sx(span * r0, u0 * s), sx(span * r1, u1 * s)])
        bars.append([sx(span * 0.08, 2.0 * s), sx(span * 0.5, 0.9 * s)])   # pale bar on the coverts
    if view == "south":
        tail = Poly([(-2.2 * s, body_cy + T * 0.5), (2.2 * s, body_cy + T * 0.5), (3.6 * s, body_cy + T + 4 * s),
                     (-3.6 * s, body_cy + T + 4 * s)])
        parts.append(Part(tail, wing_r, z=-1.5, light=-0.15, **WING))
        parts.append(Part(Ellipse(0, body_cy, T * 0.85, T), body_r, z=0,
                          region=lambda x, y: belly_r if abs(x) < T * 0.55 and y > body_cy - T * 0.6 else body_r))
        for k in (-1, 1):  # tucked feet
            parts.append(Part(Tube([(k * 2.0 * s, body_cy + T * 0.8), (k * 2.2 * s, body_cy + T + 1.5 * s)],
                                   [0.9 * s, 0.8 * s]), leg_r, z=0.5))
        parts.append(Part(Ellipse(0, h_cy, h_r, h_r * 0.95), body_r, z=1, inner=(body_r, 0)))
        parts.append(Part(Poly([(-1.3 * s, h_cy + h_r * 0.15), (1.3 * s, h_cy + h_r * 0.15), (0, h_cy + h_r * 0.15 + 4 * s)]),
                          beak_r, z=1.5, normal=(-0.2, -0.3, 0.93)))

        def details(cv):
            for k in (-1, 1):
                cv.disc((k * h_r * 0.5, h_cy - h_r * 0.15), 0.7 / cv.scale, "outline")
        return Model(parts, p["ramps"], details)

    def details_back(cv):
        if cv.big:
            for line in lines:
                cv.polyline(line, None, shade=-1)
            for line in bars:
                cv.polyline(line, (belly_r, 1))
    # from behind: an egg-shaped back (broad shoulders), a short tail fan, the head beyond
    parts.append(Part(Union([Ellipse(0, body_cy - T * 0.25, T * 0.95, T * 0.8), Ellipse(0, body_cy + T * 0.3, T * 0.6, T * 0.7)],
                            k=0.2), body_r, z=0))
    tail = Poly([(-2.0 * s, body_cy + T * 0.6), (2.0 * s, body_cy + T * 0.6), (4.0 * s, body_cy + T + 3.0 * s),
                 (1.5 * s, body_cy + T + 2.4 * s), (0, body_cy + T + 3.4 * s), (-1.5 * s, body_cy + T + 2.4 * s),
                 (-4.0 * s, body_cy + T + 3.0 * s)])
    parts.append(Part(tail, wing_r, z=1.5, inner=(wing_r, 0), **WING))
    parts.append(Part(Ellipse(0, h_cy + h_r * 0.3, h_r, h_r * 0.95), body_r, z=-0.5, light=-0.1))
    return Model(parts, p["ramps"], details_back)


def overworld(p, view, step):
    return _end_view(p, view, 35 if step else -5, scale=1.0)


def back(p, phase=0):
    """Seen from behind and above: back, both wings half-spread, tail fan."""
    return _end_view(p, "north", 28 if phase else 18, scale=1.55, zoom_head=1.0)


PLAN = BodyPlan(
    "bird_flying", "small flying/perching birds, wings folded or spread: enantiornithines",
    side=side, back=back, overworld=overworld, defaults=DEFAULTS, footprint=None, tracks="TRACKS_NONE",
)
