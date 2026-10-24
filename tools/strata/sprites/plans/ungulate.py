"""ungulate body plan: slender even-toed ungulates: early artiodactyls,
ruminants, pronghorns, camels, oreodonts, sheep.

Species (taxonomy.py):
    diacodexis    Diacodexis ilicis (Willwood Fm, WY, 2 kg)
    leptomeryx    Leptomeryx (Brule Fm, SD, 5 kg)
    cosoryx       Cosoryx furcatus (Miocene Great Plains, NE, 20 kg)
    antilocapra   Antilocapra americana (Living; MT, 50 kg)
    poebrothere   Poebrotherium (Brule Fm, SD, 30 kg)
    procamelus    Procamelus grandis (Ashfall, NE, 300 kg)
    camelops      Camelops (Wyoming, 800 kg)
    merycoidodon  Merycoidodon (Brule Fm, SD, 100 kg)
    ovis          Ovis canadensis (Natural Trap Cave, WY, 100 kg)

Drawn with the hoofed-mammal engine in plans/equid.py (`side`, `overworld`;
its docstring lists the spec keys). The sub-builds are proportions, foot type
(`leg.foot`: cloven hooves for the ruminants, sheep and oreodont, broad pads
for Procamelus and Camelops) and the `horns` list: forked bony horns for
Cosoryx, the pronged black sheaths of the pronghorn, the bighorn's curls
(`kind="curl"`, a tapering spiral with annulation rings), and Merycoidodon's
canine tusks (a short white `path` at the lip). Lineage looks:
    camel line   Poebrotherium -> Procamelus -> Camelops: tan coat, pale
                 muzzle and belly, small rounded ears, long neck growing
                 longer and more upright, cloven hooves turning into pads
    pronghorns   Cosoryx (a merycodont stand-in) -> Antilocapra: cinnamon
                 back, white belly and rump patch, horns on the brow
"""

from ..core.plan import BodyPlan
from .equid import side, overworld, DEFAULTS as HOOF_DEFAULTS

FOOTPRINT_CLOVEN = [  # two crescent halves of a cloven hoof
    "................",
    "................",
    "................",
    "......#..#......",
    ".....##..##.....",
    ".....##..##.....",
    "....###..###....",
    "....###..###....",
    "....###..###....",
    "....###..###....",
    ".....##..##.....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

FOOTPRINT_PAD = [  # camels: two toes on a broad soft pad
    "................",
    "................",
    "......#..#......",
    ".....##..##.....",
    "....#########...",
    "...###########..",
    "...###########..",
    "...###########..",
    "....#########...",
    ".....#######....",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

DEFAULTS = dict(HOOF_DEFAULTS)
DEFAULTS["leg"] = dict(HOOF_DEFAULTS["leg"], foot="cloven")

PLAN = BodyPlan(
    "ungulate", "slender even-toed ungulates: early artiodactyls, ruminants, pronghorns, camels, oreodonts, sheep",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINT_CLOVEN, tracks="TRACKS_FOOT",
)
