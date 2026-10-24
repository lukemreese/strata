"""turtle body plan: STUB. Covers turtles and tortoises: snappers, the tortoise Stylemys.

Species (taxonomy.py):
    emarginachel  Emarginachelys (Hell Creek Fm, MT, 8 kg)
    protochelyd   Protochelydra (Paleocene, ND, 25 kg)
    chelydra      Chelydra serpentina (Living; MT, 10 kg)
    stylemys      Stylemys nebrascensis (Brule Fm, SD, 15 kg)
    macrochelys   Macrochelys (Miocene Great Plains, NE, 80 kg)

Anatomy and colour notes for the artist:
Snapping turtles (Emarginachelys, Protochelydra, Chelydra serpentina,
Macrochelys: rough keeled carapace, big head, long tail with a saw-toothed crest,
Macrochelys' worm-like tongue lure is a frame-2 detail) and the tortoise Stylemys
(high-domed shell, elephantine legs). A Loft carapace plus scute lines as painted
details. Back sprite: a dedicated back() view showing the carapace from above-behind
is worth it here.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/turtle.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("turtle", "turtles and tortoises: snappers, the tortoise Stylemys")
