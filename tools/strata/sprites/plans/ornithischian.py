"""Ornithischian body plan: ceratopsians, hadrosaurs, ankylosaurs,
pachycephalosaurs and small ornithopods in side view.

Species (taxonomy.py):
    triceratops   Triceratops horridus (Hell Creek Fm, MT, 9000 kg)
    edmontosaur   Edmontosaurus annectens (Hell Creek Fm, MT, 4000 kg)
    ankylosaurus  Ankylosaurus magniventris (Hell Creek Fm, MT, 5000 kg)
    pachycephalo  Pachycephalosaurus (Hell Creek Fm, MT, 400 kg)
    thescelosaur  Thescelosaurus neglectus (Hell Creek Fm, MT, 300 kg)

The template is the dinosaur kit in plans/theropod.py (shape data, pose
groups, limbs, extras, painters, the projected end-on overworld views); see
its docstring for every spec key. Quadrupeds list four legs (far hind, far
fore, near hind, near fore) with `swing` alternating diagonally; bipeds two
legs and two arms. Identity features are `extras` in the head group (horns,
frill, beak, crest, dome) or body group (osteoderm rows, side spikes), and the
tail club rides the tail group.

Ornithischian additions to the kit:
    knobs       list of dict(group, pts, r, ramp): small domed bumps painted as
                discs (pachycephalosaur squamosal knobs, epoccipitals,
                ankylosaur osteoderms) - drawn in `ramp` level 1 with a level-0
                lower rim so they read as raised
"""

from ..core.plan import BodyPlan
from . import theropod as kit

FOOTPRINT_ORNITHISCHIAN = [
    "................",
    "................",
    "................",
    "................",
    "....#.....#.....",
    "...###...###....",
    "...###...###....",
    "....#.....#.....",
    "......###.......",
    ".....#####......",
    ".....#####......",
    "......###.......",
    "................",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(
    action=dict(head=-6.0, jaw=0.0, tail=-4.0, arms=0.0),
    walk=12.0, walk_tail=3.0, walk_head=-1.0,
    tail_reach=24.0, crest_pivot=(0.0, 0.0), jaw_pivot=(0.0, 0.0), ground=22.0,
    ow=dict(tracks="TRACKS_FOOT"),
)


def paint_knobs(cv, rig, p):
    """Raised knobs: a lit disc with a dark rim pixel below (squamosal knobs,
    epoccipitals, osteoderms). Battle scale only."""
    if not cv.big:
        return
    for k in p.get("knobs", ()):
        ramp = k.get("ramp", "skin")
        top = k.get("level", 2)
        for q in k["pts"]:
            c = rig.at(k.get("group", "body"), q)
            px, py = cv.pt(*c)
            if not (cv.inside(px, py) and cv.idx[py][px]):
                continue
            r = k.get("r", 0.6)
            if r * cv.scale >= 0.7:  # a dark ring, then a lit cap offset to the upper left
                cv.disc(c, r, (ramp, max(0, top - 2)), only_opaque=True)
                cv.disc((c[0] - 0.25 / cv.scale, c[1] - 0.25 / cv.scale), r * 0.55, (ramp, top), only_opaque=True)
            else:
                cv.disc(c, r, (ramp, top), only_opaque=True)
            cv.set(px, py + 1, (ramp, 0))


def side(p, phase=0, step=None):
    return kit.side_model(p, phase, step, extra_details=lambda cv, rig: paint_knobs(cv, rig, p))


def overworld(p, view, step):
    return kit.end_view(p, view, step, p.get("body_ramp", "skin"))


PLAN = BodyPlan(
    "ornithischian", "ceratopsians, hadrosaurs, ankylosaurs, pachycephalosaurs, small ornithopods",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_ORNITHISCHIAN, tracks="TRACKS_FOOT",
)
