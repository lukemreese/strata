"""primate body plan: STUB. Covers arboreal primates and plesiadapiforms: grasping hands, long tails, big eyes.

Species (taxonomy.py):
    purgatorius   Purgatorius (Tullock Fm, MT, 0.04 kg)
    teilhardina   Teilhardina brandti (Willwood Fm, WY, 0.03 kg)
    notharctus    Notharctus tenebrosus (Bridger Fm, WY, 4 kg)
    omomys        Omomys carteri (Bridger Fm, WY, 0.25 kg)

Anatomy and colour notes for the artist:
Arboreal: long tail (not prehensile), grasping hands and feet with
nails, forward-facing big eyes (huge in nocturnal Teilhardina/Omomys), short snout.
Purgatorius is a plesiadapiform: more tree-shrew-like, eyes on the sides, claws.
Notharctus is lemur-like with a long bushy tail. Pose on a branch (a Poly branch part
is fine). Overworld: TRACKS_FOOT, walking quadrupedally.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/primate.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("primate", "arboreal primates and plesiadapiforms: grasping hands, long tails, big eyes")
