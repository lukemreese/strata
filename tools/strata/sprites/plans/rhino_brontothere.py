"""rhino_brontothere body plan: STUB. Covers rhinocerotoids (hornless and horned) and brontotheres.

Species (taxonomy.py):
    hyrachyus     Hyrachyus modestus (Bridger Fm, WY, 70 kg)
    subhyracodon  Subhyracodon (Brule Fm, SD, 500 kg)
    teleoceras    Teleoceras major (Ashfall, NE, 1800 kg)
    aphelops      Aphelops (Ashfall, NE, 1500 kg)

Anatomy and colour notes for the artist:
Hyrachyus (hornless, tapir-like stem rhino), Subhyracodon (hornless,
two small nasal ridges), Teleoceras (barrel body, very short legs, small nasal horn),
Aphelops (hornless, long legs). Skin wrinkles as darker lines; greys and browns.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/rhino_brontothere.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("rhino_brontothere", "rhinocerotoids (hornless and horned) and brontotheres")
