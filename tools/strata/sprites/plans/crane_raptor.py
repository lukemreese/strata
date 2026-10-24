"""crane_raptor body plan: STUB. Covers long-legged waders and raptorial birds: cranes, presbyornithid ducks, vultures.

Species (taxonomy.py):
    presbyornis   Presbyornis (Green River Fm, WY, 2.5 kg)
    balearica     Balearica exigua (Ashfall, NE, 3.5 kg)
    anchigyps     Anchigyps voorhiesi (Ashfall, NE, 5 kg)

Anatomy and colour notes for the artist:
Tall birds: Presbyornis (long-legged duck with a duck bill on a
flamingo/stilt body), Balearica exigua (crowned crane relative: a crest is a
plausible guess), Anchigyps (Old-World-style vulture: bare head is plausible for a
scavenger, hooked beak, broad wings). Long legs as Tubes, neck as a Tube.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/crane_raptor.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("crane_raptor", "long-legged waders and raptorial birds: cranes, presbyornithid ducks, vultures")
