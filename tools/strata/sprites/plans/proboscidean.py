"""proboscidean body plan: STUB. Covers mammoths and mastodons: trunk, tusks, domed head.

Species (taxonomy.py):
    mammuthus     Mammuthus columbi (Natural Trap Cave, WY, 9000 kg)

Anatomy and colour notes for the artist:
Mammuthus columbi: 4 m at the shoulder, high domed head, sloping back,
long spiralled tusks, sparse hair (Columbian mammoths were less woolly than M.
primigenius). Front sprite fills 64x64; overworld 64x64.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/proboscidean.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("proboscidean", "mammoths and mastodons: trunk, tusks, domed head")
