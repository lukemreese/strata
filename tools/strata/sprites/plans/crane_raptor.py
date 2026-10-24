"""crane_raptor body plan: long-legged waders and raptorial birds in side view
(presbyornithid ducks, cranes, vultures).

Species (taxonomy.py):
    presbyornis   Presbyornis (Green River Fm, WY, 2.5 kg)
    balearica     Balearica exigua (Ashfall, NE, 3.5 kg)
    anchigyps     Anchigyps voorhiesi (Ashfall, NE, 5 kg)

The geometry is the shared bird template of plans/bird_ground.py (`bird_model`,
`overworld`; read its docstring for every key). What differs here is in the
specs: long necks as multi-point Tubes (`neck.bend` makes the middle of an
S-neck follow a head turn only partly), bare lower tibiae (`tibia_ramp="leg"`),
crests and bare faces as `extra` parts, and wing `regions` (on="wing") for the
crane's white coverts and the vulture's dark primaries. Long legs swing less in
the walk cycle (walk_swing 14).
"""

from ..core.plan import BodyPlan
from .bird_ground import DEFAULTS as BIRD_DEFAULTS, FOOTPRINT_BIRD, bird_model, overworld as bird_overworld

DEFAULTS = dict(BIRD_DEFAULTS, walk_swing=14, body_k=0.2)


def side(p, phase=0, step=None):
    return bird_model(p, phase, step)


def overworld(p, view, step):
    return bird_overworld(p, view, step)


PLAN = BodyPlan(
    "crane_raptor", "long-legged waders and raptorial birds: cranes, presbyornithid ducks, vultures",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_BIRD, tracks="TRACKS_FOOT",
)
