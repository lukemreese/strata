"""ornithischian body plan: STUB. Covers ceratopsians, hadrosaurs, ankylosaurs, pachycephalosaurs, small ornithopods.

Species (taxonomy.py):
    triceratops   Triceratops horridus (Hell Creek Fm, MT, 9000 kg)
    edmontosaur   Edmontosaurus annectens (Hell Creek Fm, MT, 4000 kg)
    ankylosaurus  Ankylosaurus magniventris (Hell Creek Fm, MT, 5000 kg)
    pachycephalo  Pachycephalosaurus (Hell Creek Fm, MT, 400 kg)
    thescelosaur  Thescelosaurus neglectus (Hell Creek Fm, MT, 300 kg)

Anatomy and colour notes for the artist:
Triceratops (frill, three horns, beak, possible bristles on the tail),
Edmontosaurus (duck bill, fleshy head crest known from a mummy, pebbly scales,
hoof-like hands), Ankylosaurus (wide low body, osteoderm rows as a texture, tail club),
Pachycephalosaurus (domed skull with knobs, biped), Thescelosaurus (small biped,
long tail). Herd species appear as map objects (Edmontosaur glade herd).

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/ornithischian.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("ornithischian", "ceratopsians, hadrosaurs, ankylosaurs, pachycephalosaurs, small ornithopods")
