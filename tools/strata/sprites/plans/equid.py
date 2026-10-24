"""equid body plan: STUB. Covers horses, from dawn horses to Equus: toe count, muzzle length and mane change along the line.

Species (taxonomy.py):
    sifrhippus    Sifrhippus sandrae (Willwood Fm, WY, 4 kg)
    eohippus      Eohippus angustidens (Wind River Fm, WY, 10 kg)
    mesohippus    Mesohippus bairdi (Brule Fm, SD, 40 kg)
    protohippus   Protohippus simus (Ashfall, NE, 100 kg)
    hypohippus    Hypohippus (Miocene Great Plains, NE, 200 kg)
    cormohippari  Cormohipparion occidentale (Ashfall, NE, 100 kg)
    equus         Equus (Natural Trap Cave, WY, 300 kg)

Anatomy and colour notes for the artist:
One template, parameterised along the line: shoulder height, leg length,
toe count (Sifrhippus/Eohippus 4 front/3 hind, small and arched-backed like a duiker;
Mesohippus 3 toes; Protohippus/Cormohipparion high-crowned grazers with longer faces,
side toes reduced; Hypohippus a forest browser, 3 toes; Equus one toe, upright mane).
Colours are reconstruction: dappled/striped forest horses, dun steppe horses.

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/equid.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("equid", "horses, from dawn horses to Equus: toe count, muzzle length and mane change along the line")
