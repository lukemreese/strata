"""canid body plan: STUB. Covers dogs and foxes (the dog starter lines).

Species (taxonomy.py):
    hesperocyon   Hesperocyon (White River Gp, SD/NE, 2 kg)
    leptocyon     Leptocyon (Ogallala Gp, NE, 2 kg)
    epicyon       Epicyon (Ogallala Gp, NE, 120 kg)
    aenocyon      Aenocyon dirus (Natural Trap Cave, WY, 65 kg)
    canis         Canis latrans (Living; WY, 13 kg)
    vulpes        Vulpes velox (Living; MT, 2.2 kg)

Anatomy and colour notes for the artist:
The dog starter lines (focal: they carry the game). Hesperocyon/Leptocyon:
small, long-bodied, short-legged, long tail, plantigrade-to-digitigrade; Epicyon: huge
borophagine, deep short muzzle with bone-cracking jaws, heavy forequarters; Aenocyon
(dire wolf): wolf build, broad head; Canis latrans and Vulpes velox: modern coyote and
swift fox colours are known (use them). Keep one recognisable family look (ear shape,
eye markings) across the line so evolution reads.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/canid.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("canid", "dogs and foxes (the dog starter lines)")
