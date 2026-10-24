"""hoofed_giant body plan: STUB. Covers heavy-bodied large herbivores/omnivores: pantodonts, uintatheres, entelodonts, bovines.

Species (taxonomy.py):
    coryphodon    Coryphodon (Willwood Fm, WY, 500 kg)
    uintatherium  Uintatherium anceps (Bridger Fm, WY, 2000 kg)
    archaeothere  Archaeotherium (Brule Fm, SD, 270 kg)
    bison         Bison bison (Living; MT, 700 kg)
    ovibos        Ovibos moschatus (Natural Trap Cave, WY, 300 kg)

Anatomy and colour notes for the artist:
Heavy and barrel-bodied: Coryphodon (pantodont: hippo-like, tusks,
short legs), Uintatherium (three pairs of knobs, sabre tusks in males), Archaeotherium
(entelodont: huge head with jaw flanges), Bison bison and Ovibos (living: colours and
coats known: shaggy forequarters, musk ox skirt). Low camera, big silhouette. Overworld
64x64 for the >1 t ones (size is chosen from mass).

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/hoofed_giant.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("hoofed_giant", "heavy-bodied large herbivores/omnivores: pantodonts, uintatheres, entelodonts, bovines")
