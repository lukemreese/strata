"""Ray body plan: freshwater stingrays seen from above. Every view is the same
3D model (a flat disc, pelvic fins, eye bumps and a whip tail) drawn on a
tilted ground plane with the `Ground` projection from plans/turtle.py:

    side()       battle front: banking, head to the left and a little towards
                 the viewer, the pale underside showing as a lip along the near
                 edge. Frame 2 banks harder and flicks the tail.
    back()       from above and behind, tail towards the viewer
    overworld()  from above, head towards (south) or away from (north) the camera;
                 the west frames are the side view. Step 1 ripples the disc.

Species (taxonomy.py):
    heliobatis    Heliobatis radians (Green River Fm, WY, 2 kg)

Ramps: outline 1, disc 4 (dorsal), belly 3 (underside), spot 1 (dark spots),
eye 1.

Knobs: disc_w, disc_l (half-width, half-length of the disc), snout (how far the
snout protrudes), pelvic (pelvic-fin size), tail (length behind the disc),
tail_r (base radius), spine (serrated spine: (position 0..1 along the tail,
length)), spots [(u, v)] dark spots in plan units (u right, v forward), bank
(view yaw, degrees from head-left), tilt (foreshortening of the side view).
"""

import math

from ..core.geom import Ellipse, Tube, Union, Poly, Part, Model, lerp
from ..core.plan import BodyPlan
from .turtle import Ground

DEFAULTS = dict(
    disc_w=14.0, disc_l=13.0, snout=1.5, pelvic=1.0, tail=24.0, tail_r=1.6,
    spine=(0.32, 4.0), spots=(), bank=-100, tilt=0.86, eye_k=1.0,
    ow=dict(tracks="TRACKS_NONE", end_zoom=1.0),
)


def model(p, yaw, fs, flap=0.0, tail_bend=0.0, big_eyes=True):
    """The ray on a ground plane. Plan shapes use (u, -v): u right, v forward."""
    W, Ln = p["disc_w"], p["disc_l"]
    G = lambda s, h=0.0: Ground(s, yaw, fs, h)  # noqa: E731
    parts = []
    # disc: a broad ellipse with a slightly pointed snout; the margin can ripple
    disc = Union([Ellipse(0, 0, W, Ln), Ellipse(0, -(Ln - 2.0 + p["snout"]), W * 0.28, 2.6)], k=0.10)
    lip = Union([Ellipse(0, 0, W + 0.2, Ln + 0.2), Ellipse(0, -(Ln - 2.0 + p["snout"]), W * 0.29, 2.7)], k=0.10)
    parts.append(Part(G(lip, -1.8 - flap * 0.3), "belly", z=-1, light=0.1, outline=("belly", 0)))
    parts.append(Part(G(disc, 0.0 + flap * 0.4), "disc", z=0, flat=0.2))
    # central body hump: shaded as its own dome, no contour
    parts.append(Part(G(Ellipse(0, 1.0, W * 0.40, Ln * 0.70), 1.0 + flap * 0.4), "disc", z=0.1, flat=0.35,
                      inner=("disc", 1), shadow=False))
    for su in (-1, 1):  # raised eye sockets
        parts.append(Part(G(Ellipse(su * 3.0, -Ln * 0.42, 1.7, 1.6), 1.9 + flap * 0.4), "disc", z=0.2,
                          flat=0.5, line=False))
    # pelvic fins behind the disc
    pk = p["pelvic"]
    for su in (-1, 1):
        parts.append(Part(G(Ellipse(su * 3.8 * pk, Ln - 0.5, 3.0 * pk, 2.6 * pk, su * 25), -0.2), "disc",
                          z=-0.5, light=-0.1))
    # the tail: a whip with a gentle bend, serrated spine part-way along
    T = p["tail"]
    pts, rad = [], []
    for i in range(7):
        s = i / 6
        pts.append((tail_bend * math.sin(s * math.pi * 0.9) * s, Ln - 1.0 + T * s))
        rad.append(lerp(p["tail_r"], 0.7, s ** 0.7))
    parts.append(Part(G(Tube(pts, rad), 0.3), "disc", z=-0.3))
    sp, sl = p["spine"]
    if sl:
        j = sp * 6
        k = int(j)
        u = j - k
        cx = lerp(pts[k][0], pts[k + 1][0], u)
        cy = lerp(pts[k][1], pts[k + 1][1], u)
        spine = Poly([(cx - 0.5, cy - 0.5), (cx + 0.5, cy - 0.5), (cx + 0.15, cy + sl), (cx - 0.15, cy + sl)])
        parts.append(Part(G(spine, 1.1), "belly", z=-0.25, normal=(0, -0.3, 0.95), outline=("disc", 0)))

    def details(cv):
        big = cv.big
        top = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 0.4)
        for u, v in p["spots"]:  # sparse dark spots (as in living potamotrygonids)
            x, y = cv.pt(*top.to_screen(u, v))
            if big or (abs(u) + abs(v)) % 2 < 1:
                cv.set(x, y, "spot")
                if big:
                    cv.set(x + 1, y, "spot")
                    if (u * 3 + v) % 3 == 0:
                        cv.set(x, y + 1, "spot")
                        cv.set(x + 1, y + 1, "spot")
        eyes = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 1.6)
        for su in (-1, 1):
            e = eyes.to_screen(su * 3.0, Ln * 0.42)
            s = eyes.to_screen(su * 3.4, Ln * 0.42 - 2.6)  # spiracle behind the eye
            x, y = cv.pt(*e)
            if big and big_eyes:  # dark 2x2 eye in a pale socket rim, a gold glint
                for dx, dy in ((-1, 0), (-1, 1), (2, 0), (2, 1), (0, -1), (1, -1), (0, 2), (1, 2)):
                    if cv.inside(x + dx, y + dy) and cv.idx[y + dy][x + dx]:
                        cv.set(x + dx, y + dy, ("disc", 3))
                for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    cv.set(x + dx, y + dy, "outline")
                cv.set(x, y, "eye")
                cv.set(*cv.pt(*s), ("disc", 0))
            else:
                cv.set(x, y, "outline")
        if big:  # radiating fin rays on the pectoral disc (what gives H. radians its name)
            r0 = Ground(Ellipse(0, 0, 1, 1), yaw, fs, 0.2)
            for k in range(0, 360, 14):
                a = math.radians(k + 7)
                if math.cos(a) > 0.82 or math.cos(a) < -0.85:  # not across the snout or the tail root
                    continue
                a0 = r0.to_screen(W * 0.52 * math.sin(a), Ln * 0.62 * math.cos(a))
                a1 = r0.to_screen(W * 0.93 * math.sin(a), Ln * 0.93 * math.cos(a))
                for px, py in cv.pixels_on_line(a0, a1):
                    v = cv.idx[py][px] if cv.inside(px, py) else 0
                    if v in cv.pal.index["disc"][1:]:
                        cv.shade(px, py, -1)
    return Model(parts, p["ramps"], details)


def side(p, phase=0, step=None):
    if step is not None:  # west overworld frames: the same banking view, rippling
        return model(p, p["bank"], p["tilt"], flap=0.6 if step else 0.0, tail_bend=1.5 if step else -1.0)
    if phase:
        return model(p, p["bank"] - 8, p["tilt"] - 0.08, flap=0.8, tail_bend=3.0)
    return model(p, p["bank"], p["tilt"], tail_bend=-1.5)


def back(p, phase=0):
    return model(p, 22, 0.7, tail_bend=2.0)


def overworld(p, view, step):
    flap = 0.6 if step else 0.0
    bend = (2.5 if step else -2.0)
    return model(p, 180 if view == "south" else 0, 0.75, flap=flap, tail_bend=bend)


PLAN = BodyPlan(
    "ray", "stingrays, seen from above / banking",
    side=side, back=back, overworld=overworld, defaults=DEFAULTS, footprint=None, tracks="TRACKS_NONE",
)
