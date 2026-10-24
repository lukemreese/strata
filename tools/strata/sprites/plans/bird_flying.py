"""bird_flying body plan: STUB. Covers small flying/perching birds, wings folded or spread: enantiornithines.

Species (taxonomy.py):
    avisaurus     Avisaurus archibaldi (Hell Creek Fm, MT, 1 kg)

Anatomy and colour notes for the artist:
Avisaurus: an enantiornithine (opposite bird): teeth possible, clawed
wing fingers, perching feet. Front: perched with wings half-open; frame 2 wings up.
Overworld: hopping/fluttering, TRACKS_NONE.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/bird_flying.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("bird_flying", "small flying/perching birds, wings folded or spread: enantiornithines")
