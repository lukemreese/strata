"""bird_ground body plan: STUB. Covers ground fowl and terror-bird-sized galloanserans: galliforms, Gastornis.

Species (taxonomy.py):
    asteriornis   Asteriornis (Maastricht Fm, Belgium (stand-in), 0.4 kg)
    gallinuloid   Gallinuloides (Green River Fm, WY, 0.3 kg)
    meleagris     Meleagris gallopavo (Natural Trap Cave, WY, 8 kg)
    centrocercus  Centrocercus urophasianus (Living; MT, 2.5 kg)
    gastornis     Gastornis (Willwood Fm, WY, 160 kg)

Anatomy and colour notes for the artist:
Galliform/galloanseran fowl: Asteriornis (tiny, quail-like, the
'Wonderchicken'), Gallinuloides (stem galliform), Meleagris (wild turkey: real
colours), Centrocercus (sage-grouse: real colours, male display with air sacs and
spiky tail is a good frame-2 pose), Gastornis (2 m flightless, huge deep beak:
herbivore; feathers likely hair-like). Feather texture: scalloped rows of darker
pixels. Overworld TRACKS_FOOT (no bird tracks constant).

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/bird_ground.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("bird_ground", "ground fowl and terror-bird-sized galloanserans: galliforms, Gastornis")
