"""ray body plan: STUB. Covers stingrays, seen from above / banking.

Species (taxonomy.py):
    heliobatis    Heliobatis radians (Green River Fm, WY, 2 kg)

Anatomy and colour notes for the artist:
Heliobatis radians (Green River): a small freshwater stingray, disc about
as wide as long, long whip tail with a serrated spine, eyes and spiracles on top.
Show it banking (disc tilted ~30 deg) so the side-view battle sprite reads as a ray;
dorsal disc colour sandy brown with darker mottling (fossils preserve no colour;
living potamotrygonids are spotted, so sparse spots are plausible). Overworld: flat
disc seen from above in every direction; TRACKS_NONE.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/ray.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("ray", "stingrays, seen from above / banking")
