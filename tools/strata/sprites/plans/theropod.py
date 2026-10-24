"""theropod body plan: STUB. Covers bipedal theropods: tyrannosaurs, dromaeosaurs (feathered), oviraptorosaurs.

Species (taxonomy.py):
    tyrannosaur   Tyrannosaurus rex (Hell Creek Fm, MT, 8000 kg)
    acheroraptor  Acheroraptor temertyorum (Hell Creek Fm, MT, 40 kg)
    anzu          Anzu wyliei (Hell Creek Fm, ND/SD, 250 kg)

Anatomy and colour notes for the artist:
Tyrannosaurus (adult: deep skull, tiny arms, horizontal back, scaly with
possible sparse filaments on the back; earth tones, not green), Acheroraptor
(dromaeosaur: fully feathered with wing feathers on the arms - no naked raptors),
Anzu (oviraptorosaur: crested toothless beak, feathered, long legs, wing feathers).
Lips over the teeth are now the favoured reconstruction for T. rex. Overworld 64x64
for Tyrannosaurus (it is a boss map object).

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/theropod.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("theropod", "bipedal theropods: tyrannosaurs, dromaeosaurs (feathered), oviraptorosaurs")
