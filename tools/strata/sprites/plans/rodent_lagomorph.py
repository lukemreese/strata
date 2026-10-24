"""rodent_lagomorph body plan: STUB. Covers rodents and rabbits: gnawing incisors, big hind feet, squirrels, prairie dogs.

Species (taxonomy.py):
    ischyromys    Ischyromys (Brule Fm, SD, 0.8 kg)
    paramys       Paramys (Willwood Fm, WY, 2 kg)
    palaeolagus   Palaeolagus haydeni (Brule Fm, SD, 0.8 kg)
    douglassciur  Douglassciurus jeffersoni (Chadron Fm, Flagstaff Rim, WY, 0.3 kg)
    cynomys       Cynomys ludovicianus (Living; MT, 1 kg)

Anatomy and colour notes for the artist:
Start from small_mammal. Add: rodent incisors (orange enamel on the
front is real), large hind feet and a sitting/hopping pose for Palaeolagus (no long ears
like modern jackrabbits: Palaeolagus ears were shorter), bushy tail for Douglassciurus
(the oldest squirrel; tail the length of the body), Cynomys upright sentinel pose and
short tail. Agouti browns/greys.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/rodent_lagomorph.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("rodent_lagomorph", "rodents and rabbits: gnawing incisors, big hind feet, squirrels, prairie dogs")
