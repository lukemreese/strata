"""croc_champsosaur body plan: STUB. Covers low-slung aquatic reptiles: crocodylians, choristoderes.

Species (taxonomy.py):
    champsosaur   Champsosaurus (Hell Creek Fm, MT, 20 kg)
    borealosuch   Borealosuchus (Hell Creek Fm, MT, 150 kg)

Anatomy and colour notes for the artist:
Champsosaurus (gharial-like long thin snout, eyes on top, wide
skull at the back, long tail; a choristodere, not a croc), Borealosuchus (generalised
crocodylian, broad snout). Low side view; the overworld view from above reads best
for south/north (head or tail end towards the camera). TRACKS_SLITHER suits the tail
drag.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/croc_champsosaur.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("croc_champsosaur", "low-slung aquatic reptiles: crocodylians, choristoderes")
