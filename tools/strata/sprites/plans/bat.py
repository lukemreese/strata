"""bat body plan: STUB. Covers bats: wing membranes, perched or in flight.

Species (taxonomy.py):
    onychonycter  Onychonycteris finneyi (Green River Fm, WY, 0.04 kg)

Anatomy and colour notes for the artist:
Onychonycteris finneyi (Green River): claws on all five fingers, relatively
short wings and long hind legs: a climber that flew; lacked the echolocation
specialisations of modern bats (small cochlea), so big eyes rather than huge ears.
Front sprite: wings half-spread (membranes as Polys with finger bones as lines); back
sprite from behind. Overworld: hanging or fluttering; TRACKS_NONE.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/bat.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("bat", "bats: wing membranes, perched or in flight")
