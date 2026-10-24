"""Fish body plan: ray-finned fish in side view (Knightia; next: Lepisosteus).

Ramps the template uses (a spec may add more for its own painters):
    outline   1 colour
    back      dorsal colour, 3-4 shades (countershading above `dorsal_line`)
    flank     belly/flank, 3-4 shades (silver: pale top shade)
    fin       hyaline fins, 2-3 shades
    accent    1 colour (cheek sheen)

Geometry is in model units at scale 1, head to the left, origin mid-body.
Fins are given relative to the body outline: (x, dy) with dy added to the
top (dorsal) or bottom (anal) of the body at x, so fins stay attached when the
body profile changes. Caudal points behind the body's x1 sweep with the tail.

To add a species: copy the knightia spec, set `body` from the real proportions,
place the fins, then iterate with --preview. New anatomy (a gar's long snout and
ganoid scale rows, a long-based dorsal) goes in here as a new optional feature
with a default that leaves existing species unchanged.
"""

import math

from ..core.geom import Loft, Poly, Part, Model, lerp, rot
from ..core.plan import BodyPlan

FIN = dict(normal=(0, 0, 1), outline=("fin", 0), light=0.2)  # hyaline fins: pale, outlined in grey

DEFAULTS = dict(
    dorsal_line=-0.22,     # body.s() below which the back colour starts (-1 top .. 1 bottom)
    tail_sweep=0.82,       # frame 2: the caudal fin foreshortens as it sweeps towards the viewer
    fin_flap=12,           # frame 2: paired fins rotate by this many degrees
    cheek=None,            # ((x, y), r): brassy cheek sheen in `accent`
    scale_lattice=False,   # sparse darker pixels on the back
    scutes=None,           # dict(x0, x1, step, inset): ventral keel scutes
    caudal_rays=None,      # dict(x, v, root, reach)
    dorsal_rays=None,      # dict(x0, x1, n, lean, h, dh)
    ganoid=None,           # dict(period, min_level): diamond lattice of ganoid scales (gars)
    spots=None,            # [(x, y)]: dark spots in the `spot` ramp (body and fins)
    teeth=None,            # dict(x0, x1, step, y, open_y): pale teeth along a long jaw, in `accent`
    ow=dict(tracks="TRACKS_NONE"),
)


def _body(p):
    b = p["body"]
    a, c = b["tilt"]
    return Loft(b["x0"], b["x1"], up=b["up"], dn=b["dn"], mid=lambda t: a * (1 - t) + c)


def side(p, phase=0, step=None):
    if step is not None:  # swimming: the walk cycle is the tail beat
        phase = step
    ramps = p["ramps"]
    body = _body(p)
    x1 = p["body"]["x1"]

    def countershade(x, y):
        return "back" if body.s(x, y) < p["dorsal_line"] else "flank"

    tail = p["tail_sweep"] if phase else 1.0
    top, bot = body.top, body.bottom
    tx = lambda x: x1 + (x - x1) * tail  # noqa: E731
    caudal = Poly([(tx(x) if x > x1 else x, y) for x, y in p["caudal"]])
    dorsal_fin = Poly([(x, top(x) + dy) for x, dy in p["dorsal"]])
    anal_fin = Poly([(x, bot(x) + dy) for x, dy in p["anal"]])
    pa = p["fin_flap"] if phase else 0
    pv = p["pelvic"]
    px0, inset = pv["x"], pv["inset"]
    pelvic = Poly([(px0, bot(px0) + inset), *((px0 + u, bot(px0) + v) for u, v in (rot(*r, pa) for r in pv["rays"])),
                   (pv["end"], bot(pv["end"]) + inset)])
    pc = p["pectoral"]
    pectoral = Poly([pc["root"], *((pc["pivot"][0] + u, pc["pivot"][1] + v) for u, v in (rot(*r, pa) for r in pc["rays"])),
                     pc["end"]])

    parts = [
        Part(body, "flank", z=0, flat=0.45, region=countershade),
        Part(caudal, "fin", z=-1, **FIN),
        Part(dorsal_fin, "fin", z=-1, **FIN),
        Part(anal_fin, "fin", z=-1, **FIN),
        Part(pelvic, "fin", z=-1, **FIN),
        Part(pectoral, "fin", z=1, shadow=False, **FIN),
    ]

    def details(cv):
        big = cv.big
        if big and p["caudal_rays"]:  # every other ray, darker
            cr = p["caudal_rays"]
            for v in cr["v"]:
                cv.line((cr["x"], v * cr["root"]), (tx(cr["x"] + abs(v) * cr["reach"]), v), ("fin", 1))
        if big and p["dorsal_rays"]:
            dr = p["dorsal_rays"]
            for k in range(1, dr["n"] + 1):
                x = lerp(dr["x0"], dr["x1"], k / (dr["n"] + 1))
                cv.line((x, top(x)), (x + dr["lean"] - k, top(x) - dr["h"] + k * dr["dh"]), ("fin", 1))
        # operculum (gill cover): a darker arc
        ox, oy, orx, ory = p["operculum"]
        arc = [(ox + orx * math.cos(a), oy + ory * math.sin(a)) for a in
               (math.radians(d) for d in range(-75, 76, 15))]
        if big and p["cheek"]:
            cv.disc(p["cheek"][0], p["cheek"][1], "accent", only_opaque=True)
        cv.polyline(arc, None, shade=-3)
        if big and p["scale_lattice"]:
            for py in range(cv.h):
                for px in range(cv.w):
                    v = cv.idx[py][px]
                    if (v in cv.pal.index["back"][1:] and py % 2 == 0 and (px + py) % 4 == 0
                            and cv.pal.ramp_of[v][1] < 3):
                        cv.shade(px, py, -1)
        if big and p["ganoid"]:  # rhombic ganoid scales: a diagonal lattice on the lit shades
            g = p["ganoid"]
            n, lo = g["period"], g.get("min_level", 2)
            for py in range(cv.h):
                for px in range(cv.w):
                    v = cv.idx[py][px]
                    rl = cv.pal.ramp_of.get(v)
                    if rl and rl[0] in ("back", "flank") and rl[1] >= lo and \
                            ((px + py) % n == 0 or (px - py) % n == 0):
                        cv.shade(px, py, -1)
        if big and p["spots"]:
            for q in p["spots"]:
                cv.set(*cv.pt(*q), "spot")
        if big and p["teeth"]:
            t = p["teeth"]
            x = t["x0"]
            while x < t["x1"]:
                if phase:
                    cv.set(*cv.pt(x, t["open_y"][0] + (x - t["x0"]) * t["open_y"][2]), "accent")
                    cv.set(*cv.pt(x + t["step"] / 2, t["open_y"][1] - (x - t["x0"]) * t["open_y"][3]), "accent")
                else:
                    cv.set(*cv.pt(x, t["y"] + (x - t["x0"]) * t.get("slope", 0.0)), "accent")
                x += t["step"]
        m = p["mouth"]
        if phase and big:  # frame 2 gapes
            for a, b in m["open"]:
                cv.line(a, b, "outline")
            cv.set(*cv.pt(*m["gap"]), ("flank", 0))
        else:
            cv.line(*m["closed"], "outline")
        if big and p["scutes"]:
            s = p["scutes"]
            for x in range(s["x0"], s["x1"], s["step"]):
                qx, qy = cv.pt(x, bot(x) - s["inset"])
                cv.shade(qx, qy, -1)
        _eye(cv, *p["eye"])

    return Model(parts, ramps, details)


def _eye(cv, e, r):
    """A fish eye: dark rim, pale iris, big pupil, two highlights."""
    if cv.big:
        cv.disc(e, r + 0.6, "outline")
        cv.disc(e, r - 0.2, ("flank", 2))
        cv.disc((e[0] - 0.5, e[1] + 0.3), r * 0.55, "outline")
        px, py = cv.pt(e[0] - 1.4, e[1] - 1.4)
        cv.set(px, py, ("flank", 3))
        cv.set(px + (1 if cv.flip else -1), py + 2, ("flank", 1))
    else:
        cv.disc(e, 1.6 if cv.scale > 0.45 else 1.1, "outline")
        px, py = cv.pt(e[0] - 0.8, e[1] - 0.8)
        cv.set(px, py, ("flank", 3))


def overworld(p, view, step):
    """Head-on (south) and tail-on (north) views of a laterally compressed
    fish: a tall narrow body, the dorsal fin as a sliver on top, paired fins
    to the sides, the caudal fin edge-on behind. step 1 beats the tail."""
    from ..core.geom import Ellipse
    body = _body(p)
    b = p["body"]
    xs = [lerp(b["x0"], b["x1"], i / 20) for i in range(21)]
    xm = max(xs, key=lambda x: body.bottom(x) - body.top(x))
    top, bot = body.top(xm), body.bottom(xm)
    cy, ry = (top + bot) / 2, (bot - top) / 2
    rx = ry * p.get("thickness", 0.38)
    beat = (1.5 if step else -1.5) if view == "north" else (0.8 if step else 0.0)
    fin_h = -min(dy for _, dy in p["dorsal"])
    parts = [
        Part(Ellipse(0, cy, rx, ry), "flank", z=0, flat=0.45,
             region=lambda x, y: "back" if (y - cy) / ry < p["dorsal_line"] else "flank"),
        Part(Poly([(-0.6, top + 1), (beat * 0.3, top - fin_h * 0.8), (0.6, top + 1)]), "fin", z=-1, **FIN),
    ]
    flap = 1.0 if step else 0.0
    for s in (-1, 1):
        parts.append(Part(Poly([(s * rx * 0.7, cy + ry * 0.25), (s * (rx + 3.5 + flap), cy + ry * 0.55),
                                (s * rx * 0.6, cy + ry * 0.55)]), "fin", z=1, **FIN))
    caudal_h = max(abs(y) for _, y in p["caudal"])
    tail = Poly([(beat - 0.7, cy - caudal_h), (beat + 0.7, cy - caudal_h), (beat + 0.5, cy + caudal_h),
                 (beat - 0.5, cy + caudal_h)])
    parts.append(Part(tail, "fin", z=-2 if view == "south" else 2, **FIN))

    def details(cv):
        if view == "south":
            e = p["eye"][0]
            for s in (-1, 1):
                cv.disc((s * (rx - 0.6), e[1]), 1.3, "outline")
            cv.line((-1.0, cy + ry * 0.05), (1.0, cy + ry * 0.05), "outline")

    return Model(parts, p["ramps"], details)


PLAN = BodyPlan(
    "fish", "ray-finned fish (clupeids, gars)",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=None, tracks="TRACKS_NONE",
)
