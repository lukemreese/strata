"""bat body plan: bats in flight.

Species (taxonomy.py):
    onychonycter  Onychonycteris finneyi (Green River Fm, WY, 0.04 kg)

Onychonycteris finneyi (Green River, ~52.5 Ma): claws on all five fingers,
relatively short, broad wings and long hind legs (a climber that flew); a
small cochlea, so probably no laryngeal echolocation: big eyes, moderate ears.

Views
    side      flying in profile, head left, wings raised (frame 1) and in the
              downstroke (frame 2, also the overworld west step); the far wing
              peeks out in front of the near one, darker.
    back      from behind and above, wings spread (frame 2: raised)
    overworld south: face, belly and both wings spread towards the camera;
              north: the back view. Steps alternate wings up and down.
The wing is a hand: arm and forearm (a Tube leading edge) to the wrist, a
clawed thumb, and fingers 2-5 radiating to the trailing edge; the membrane is
one flat Poly panel per finger gap, each at a slightly different z and normal,
so the rasteriser's contour lines draw the finger bones and the panels shade
like a pleated sail. A claw (tiny Tube, ramp "claw") tips every finger.

Spec keys (model px, head left, y down):
    wing      dict(S, E, W, thumb, tips=[D2, D3, D4, D5], ankle, hip, scallop):
              the near wing in the raised pose (side view)
    spread    the same for the back/end views (right wing; mirrored)
    flap      downstroke rotation (deg) about the shoulder
    body, head, snout, ear, eye, legs, tail: shapes (see the spec)
Ramps: outline, fur (3), pale (2), wing (3), skin (1: face, ears, feet),
claw (1), white (1).
"""

from ..core.geom import Ellipse, Tube, Union, Poly, Part, Model, turn, lerp
from ..core.plan import BodyPlan

DEFAULTS = dict(front=1.2, back=1.0, icon=0.55, flap=26.0, ow=dict(tracks="TRACKS_NONE", end_zoom=0.95))

PANEL_NORMALS = [(-0.35, -0.45, 0.82), (0.15, -0.15, 0.97), (-0.25, -0.35, 0.9), (0.1, 0.05, 0.99)]


def _pull(a, b, c, k):
    """Midpoint of a-b pulled towards c by k (the scalloped trailing edge)."""
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return (lerp(m[0], c[0], k), lerp(m[1], c[1], k))


def wing_parts(w, T, z0, light=0.0, mirror=1, claws=True, normals=PANEL_NORMALS):
    """Parts of one wing. T maps rest points to the pose; mirror=-1 flips the
    x of the normals (for the left wing of the spread views)."""
    S, E, W, thumb = (T(w[k]) for k in ("S", "E", "W", "thumb"))
    tips = [T(q) for q in w["tips"]]
    ankle, hip = T(w["ankle"]) if w.get("move_ankle") else w["ankle"], w["hip"]
    k = w.get("scallop", 0.22)
    parts = []
    panels = []
    for i in range(3):
        a, b = tips[i], tips[i + 1]
        panels.append([W, a, _pull(a, b, W, k), b])
    panels.append([E, W, tips[3], _pull(tips[3], ankle, S, k * 0.8), ankle, hip, S])
    order = [3, 2, 1, 0]  # the arm panel farthest, the leading hand panel nearest
    for rank, i in enumerate(order):
        n = normals[i]
        parts.append(Part(Poly(panels[i]), "wing", z=z0 + rank * 0.02, normal=(n[0] * mirror, n[1], n[2]),
                          inner=("wing", 0), outline="outline", light=light, shadow=False))
    parts.append(Part(Tube([S, E, W], [1.2, 0.9, 0.75]), "wing", z=z0 + 0.1, inner=("wing", 0), light=light,
                      shadow=False))
    if claws:
        for tip, base in [(thumb, W)] + [(t, W) for t in tips]:
            dx, dy = tip[0] - base[0], tip[1] - base[1]
            ln = max(0.01, (dx * dx + dy * dy) ** 0.5)
            end = (tip[0] + dx / ln * 1.3, tip[1] + dy / ln * 1.3)
            parts.append(Part(Tube([tip, end], [0.55, 0.4]), "claw", z=z0 + 0.12, light=light, shadow=False))
        parts.append(Part(Tube([W, thumb], [0.6, 0.5]), "wing", z=z0 + 0.11, inner=("wing", 0), light=light,
                          shadow=False))
    return parts


def _head(p, H, z, face=True):
    hd = p["head"]
    parts = []
    cran = Ellipse(*H(hd["c"]), hd["r"][0], hd["r"][1])
    sn = p["snout"]
    snout = Tube([H(sn["a"]), H(sn["b"])], sn["r"])
    parts.append(Part(Union([cran, snout], k=0.1), "fur", z=z,
                      region=lambda x, y: "pale" if y > H(hd["c"])[1] + hd["r"][1] * 0.35 else "fur"))
    return parts


def side(p, phase=0, step=None):
    flap = p["flap"] if (phase or step) else 0.0
    w = p["wing"]
    S = w["S"]
    Tn = lambda q: turn(q, S, flap)  # noqa: E731
    fw = p["far_wing"]
    Tf = lambda q: turn((q[0] + fw["dx"], q[1] + fw["dy"]), (S[0] + fw["dx"], S[1] + fw["dy"]),  # noqa: E731
                        flap * 0.9 + fw["deg"])
    b = p["body"]
    parts = []
    parts += wing_parts(w, Tf, -3.0, light=-0.3)
    # far leg and ear
    lg = p["legs"]
    parts.append(Part(Tube(lg["far"], lg["r"]), "fur", z=-1.5, light=-0.3))
    parts.append(Part(Ellipse(*p["ear"]["far"]), "skin", z=-1.4, light=-0.3))
    # tail and its membrane
    parts.append(Part(Poly(p["tail"]["membrane"]), "wing", z=-1.2, normal=(0.1, 0.2, 0.97), inner=("wing", 0),
                      shadow=False))
    parts.append(Part(Tube(p["tail"]["pts"], p["tail"]["r"]), "wing", z=-1.1, inner=("wing", 0)))
    torso = Ellipse(*b["e"])
    parts.append(Part(torso, "fur", z=0, region=lambda x, y: "pale" if y > b["belly"] + 0.08 * x else "fur"))
    parts.append(Part(Tube(lg["near"], lg["r"]), "fur", z=0.5, inner=("fur", 0)))
    fx, fy = lg["near"][-1]
    parts.append(Part(Ellipse(fx - 0.6, fy + 0.6, 1.6, 0.8, -10), "skin", z=0.6, inner=("skin", 0)))
    parts += wing_parts(w, Tn, 1.0)
    H = lambda q: q  # noqa: E731
    parts += _head(p, H, 2.0)
    parts.append(Part(Ellipse(*p["ear"]["near"]), "skin", z=2.1, inner=("skin", 0)))
    eye = p["eye"]

    def details(cv):
        big = cv.big
        # inner ear
        ex, ey, erx, ery, ea = p["ear"]["near"]
        if big:
            cv.disc((ex + 0.3, ey + 0.6), min(erx, ery) * 0.55, ("skin", 0), only_opaque=True)
        # fur texture on the body
        if big:
            fur = set(cv.pal.index["fur"][1:])
            for py in range(cv.h):
                for px in range(cv.w):
                    if cv.idx[py][px] in fur and py % 2 == 0 and (px + py) % 4 == 0:
                        cv.shade(px, py, -1)
        # nose and mouth
        sb = p["snout"]["b"]
        cv.disc((sb[0] + 0.4, sb[1] - 0.2), 0.9 if big else 0.6, ("skin", 0), only_opaque=True)
        if big:
            cv.line(p["mouth"][0], p["mouth"][1], "outline")
        c, r = eye["c"], eye["r"]
        if big:
            cv.disc(c, r, "outline", only_opaque=True)
            px, py = cv.pt(*c)
            cv.set(px + (1 if cv.flip else -1), py - 1, "white")
        else:
            cv.disc(c, max(0.6, r * 0.6), "outline", only_opaque=True)
        # toe claws
        if big:
            cv.set(*cv.pt(fx - 2.0, fy + 1.0), "claw")
    return Model(parts, p["ramps"], details)


def spread(p, view, up, chibi=1.0):
    """Both wings spread, seen from the front (south) or from behind (north /
    back sprite). up: wings raised (True) or lowered. chibi scales the head
    and ears (overworld frames)."""
    sw = p["spread"]
    deg = sw["up"] if up else sw["down"]
    parts = []
    b = p["spread_body"]
    front = view == "south"
    for m in (1, -1):
        S = (sw["S"][0] * m, sw["S"][1])

        def T(q, m=m, S=S):
            return turn((q[0] * m, q[1]), S, -deg * m)
        w = dict(sw, S=sw["S"], E=sw["E"], W=sw["W"], thumb=sw["thumb"], tips=sw["tips"],
                 ankle=(sw["ankle"][0] * m, sw["ankle"][1]), hip=(sw["hip"][0] * m, sw["hip"][1]))
        parts += wing_parts(w, T, -1.0, mirror=m, light=0.05 if front else 0.0)
    # legs and tail
    for m in (1, -1):
        parts.append(Part(Tube([(b["leg"][0][0] * m, b["leg"][0][1]), (b["leg"][1][0] * m, b["leg"][1][1])],
                               [1.3, 0.9]), "fur", z=-0.5 if front else 0.4, inner=("fur", 0)))
    if not front:
        parts.append(Part(Poly([(-b["leg"][1][0], b["leg"][1][1]), (0, b["tail"]), (b["leg"][1][0], b["leg"][1][1]),
                                (0, b["leg"][0][1])]), "wing", z=0.3, normal=(0.0, -0.2, 0.98), inner=("wing", 0)))
    torso = Ellipse(0, b["cy"], b["rx"], b["ry"])
    parts.append(Part(torso, "fur", z=0, region=(lambda x, y: "pale" if abs(x) < b["rx"] * 0.55 and y > b["cy"] - 1
                                                 else "fur") if front else None))
    hy, hr = b["head"]
    hy, hr = hy - (chibi - 1) * hr * 0.6, hr * chibi
    er = [v * chibi for v in b["ear"]]
    for m in (1, -1):
        parts.append(Part(Ellipse(er[0] * m, hy + er[1], er[2], er[3], 18 * m), "skin",
                          z=0.8 if front else 0.6, inner=("skin", 0)))
    parts.append(Part(Ellipse(0, hy, hr, hr * 0.9), "fur", z=1.0, inner=("fur", 0)))
    if front:
        parts.append(Part(Ellipse(0, hy + hr * 0.5, hr * 0.5, hr * 0.38), "skin", z=1.1, inner=("fur", 0)))

    def details(cv):
        if front:
            for m in (1, -1):
                q = cv.pt(m * hr * 0.42, hy - hr * 0.08)
                cv.set(*q, "outline")
                if cv.big:
                    cv.disc((m * hr * 0.42, hy - hr * 0.08), 0.9, "outline", only_opaque=True)
                    cv.set(q[0] + (-1 if m > 0 else 0), q[1] - 1, "white")
                else:  # overworld: a 1x2 eye with a glint, readable on dark fur
                    cv.set(q[0], q[1] + 1, "outline")
                    cv.set(q[0], q[1] - 1, ("pale", -1))
                cv.disc((m * er[0], hy + er[1] + 0.5), er[2] * 0.45, ("skin", 0), only_opaque=True)
            cv.set(*cv.pt(0, hy + hr * 0.42), "outline")
    return Model(parts, p["ramps"], details)


def back(p, phase=0):
    return spread(p, "north", up=bool(phase))


def overworld(p, view, step):
    return spread(p, view, up=not step, chibi=p.get("ow_head", 1.9))


PLAN = BodyPlan(
    "bat", "bats: wing membranes, perched or in flight",
    side=side, back=back, overworld=overworld, defaults=DEFAULTS, footprint=None, tracks="TRACKS_NONE",
)
