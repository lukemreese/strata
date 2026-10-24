"""primate body plan: arboreal primates and plesiadapiforms.

Species (taxonomy.py):
    purgatorius   Purgatorius (Tullock Fm, MT, 0.04 kg)
    teilhardina   Teilhardina brandti (Willwood Fm, WY, 0.03 kg)
    notharctus    Notharctus tenebrosus (Bridger Fm, WY, 4 kg)
    omomys        Omomys carteri (Bridger Fm, WY, 0.25 kg)

Drawn with the small-mammal engine (plans/small_mammal.py, `quad_side`; keys
there and in plans/canid.py), crouched on a branch in the battle views
(`branch`, ramp "bark"; the overworld walk frames drop it and carry the tail
level via `ow_side`). Primate identity is in the head: a short snout and big
forward-facing eyes, drawn as a large iris eye (`eye.big`) plus the far eye
peeking past the snout (`eye.far`), so the head reads as turned towards the
viewer while the body stays in profile (style guide). Purgatorius, a
plesiadapiform, keeps a longer snout, side eyes and claws. Grasping hands and
feet: plantigrade paws wrapped over the branch, no claws.
Lineage: Teilhardina -> Omomys share the omomyid face (huge amber eyes, pale
eye ring, dark muzzle) and the dark tail end.
"""

from ..core.plan import BodyPlan
from .small_mammal import side, overworld, ENGINE_DEFAULTS

FOOTPRINT_PRIMATE = [  # a hand: four fingers and a thumb set apart
    "................",
    "................",
    "......#.#.......",
    ".....#.#.#......",
    ".....#.#.#.#....",
    ".....#.#.#.#....",
    "....########....",
    "..#.########....",
    "..##########....",
    "...#########....",
    "....#######.....",
    ".....#####......",
    "................",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(ENGINE_DEFAULTS)

PLAN = BodyPlan(
    "primate", "arboreal primates and plesiadapiforms: grasping hands, long tails, big eyes",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_PRIMATE, tracks="TRACKS_FOOT",
)
