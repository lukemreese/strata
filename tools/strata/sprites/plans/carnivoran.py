"""carnivoran body plan: cats, bears, mustelids, miacids/viverravids, creodonts
(oxyaenids, hyaenodonts) and the triisodont Eoconodon.

Species (taxonomy.py):
    protictis     Protictis (Paleocene, MT/WY, 1.5 kg)       dog line
    miacis        Miacis (Bridger Fm, WY, 1.5 kg)            dog line
    mustela       Mustela nigripes (Living; MT, 0.9 kg)
    hoplophoneus  Hoplophoneus (Brule Fm, SD, 50 kg)
    miracinonyx   Miracinonyx trumani (Natural Trap Cave, WY, 70 kg)
    panthera      Panthera atrox (Natural Trap Cave, WY, 350 kg)
    arctodus      Arctodus simus (Natural Trap Cave, WY, 900 kg)
    oxyaena       Oxyaena (Willwood Fm, WY, 20 kg)
    patriofelis   Patriofelis ferox (Bridger Fm, WY, 70 kg)
    hyaenodon     Hyaenodon horridus (Brule Fm, SD, 40 kg)
    eoconodon     Eoconodon (Denver Fm, CO, 30 kg)

All of them use the parametric quadruped engine in plans/canid.py (`side`,
`overworld`); the sub-builds are just different proportions and head shapes,
set per spec (see the spec comments):
    weasel-long   Protictis, Miacis, Mustela: long body, short legs, small head
    cat           Hoplophoneus (sabres + chin flange, short legs), Miracinonyx
                  (cheetah build), Panthera atrox (maneless lion): short muzzle,
                  round ears, whiskers, coloured iris
    bear          Arctodus: long legs, short body, short broad face, plantigrade
    creodont      Oxyaena, Patriofelis (low, plantigrade, long tail, short
                  broad head), Hyaenodon (long narrow skull, digitigrade)
    triisodont    Eoconodon: heavy, plantigrade, big blunt-toothed head
Protictis and Miacis are on the dog starter line and wear the dog-line family
marks (specs/canid.py).
"""

from ..core.plan import BodyPlan
from .canid import side, overworld, DEFAULTS as CANID_DEFAULTS, FOOTPRINT_CANID

FOOTPRINT_CAT = [  # retractile claws: no claw marks, a broad lobed pad
    "................",
    "................",
    "................",
    ".....#....#.....",
    "...#..#..#..#...",
    "....#......#....",
    "................",
    "......####......",
    ".....######.....",
    "....########....",
    ".....######.....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINT_PLANTIGRADE = [  # five toes and a long sole: bears, creodonts
    "................",
    "...#.#..#..#.#..",
    "...#.#..#..#.#..",
    "................",
    "....#########...",
    "...###########..",
    "...###########..",
    "....#########...",
    "....########....",
    ".....#######....",
    ".....######.....",
    "......####......",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINTS = dict(canid=FOOTPRINT_CANID, cat=FOOTPRINT_CAT, plantigrade=FOOTPRINT_PLANTIGRADE)

DEFAULTS = dict(CANID_DEFAULTS)

PLAN = BodyPlan(
    "carnivoran", "cats, bears, mustelids, miacids/viverravids, creodonts (oxyaenids, hyaenodonts), triisodonts",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_CANID, tracks="TRACKS_FOOT",
)
