"""rodent_lagomorph body plan: rodents and rabbits.

Species (taxonomy.py):
    ischyromys    Ischyromys (Brule Fm, SD, 0.8 kg)
    paramys       Paramys (Willwood Fm, WY, 2 kg)
    palaeolagus   Palaeolagus haydeni (Brule Fm, SD, 0.8 kg)
    douglassciur  Douglassciurus jeffersoni (Chadron Fm, Flagstaff Rim, WY, 0.3 kg)
    cynomys       Cynomys ludovicianus (Living; MT, 1 kg)

Drawn with the small-mammal engine (plans/small_mammal.py, `quad_side`; keys
documented there and in plans/canid.py). What makes them rodents and rabbits
is all spec data:
    teeth.gnaw   the ever-growing upper incisors at the muzzle tip: orange
                 enamel for rodents (real: iron in the enamel), white for
                 rabbits (lagomorph enamel is unpigmented)
    leg.hpaw     long hind feet (rabbit, squirrels)
    body.rear    raised front: a hunched rabbit, a sitting squirrel, the
                 upright prairie-dog sentinel (with leg.arms: hands at the chest)
    tail.bends   the squirrel tail curled up over the back
Lineages: Paramys -> Ischyromys (ischyromyids) and Douglassciurus -> Cynomys
(squirrels) share their line's marks: a pale eye ring and orange incisors for
all rodents; the squirrel line adds a dark-tipped tail and pale flank line.
"""

from ..core.plan import BodyPlan
from .small_mammal import side, overworld, ENGINE_DEFAULTS

FOOTPRINT_RODENT = [  # four slender fingers in front, five toes behind
    "................",
    "................",
    "....#.#..#.#....",
    "....#.#..#.#....",
    ".....######.....",
    ".....######.....",
    "......####......",
    "................",
    "...#.#.#.#.#....",
    "...#.#.#.#.#....",
    "....#######.....",
    "....#######.....",
    ".....#####......",
    ".....#####......",
    "................",
    "................",
]

FOOTPRINT_RABBIT = [  # furred soles: long blurred hind prints, small round fore prints
    "................",
    "......###.......",
    ".....#####......",
    ".....#####......",
    "......###.......",
    "................",
    "....##....##....",
    "...####..####...",
    "...####..####...",
    "...####..####...",
    "...####..####...",
    "...####..####...",
    "....##....##....",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(ENGINE_DEFAULTS)

PLAN = BodyPlan(
    "rodent_lagomorph", "rodents and rabbits: gnawing incisors, big hind feet, squirrels, prairie dogs",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_RODENT, tracks="TRACKS_FOOT",
)
