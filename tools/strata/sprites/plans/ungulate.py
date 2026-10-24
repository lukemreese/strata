"""ungulate body plan: STUB. Covers slender even-toed ungulates: early artiodactyls, ruminants, pronghorns, camels, oreodonts, sheep.

Species (taxonomy.py):
    diacodexis    Diacodexis ilicis (Willwood Fm, WY, 2 kg)
    leptomeryx    Leptomeryx (Brule Fm, SD, 5 kg)
    cosoryx       Cosoryx furcatus (Miocene Great Plains, NE, 20 kg)
    antilocapra   Antilocapra americana (Living; MT, 50 kg)
    poebrothere   Poebrotherium (Brule Fm, SD, 30 kg)
    procamelus    Procamelus grandis (Ashfall, NE, 300 kg)
    camelops      Camelops (Wyoming, 800 kg)
    merycoidodon  Merycoidodon (Brule Fm, SD, 100 kg)
    ovis          Ovis canadensis (Natural Trap Cave, WY, 100 kg)

Anatomy and colour notes for the artist:
Slender even-toed: Diacodexis (rabbit-sized, long hind legs), Leptomeryx
(chevrotain-like, no antlers), Cosoryx (merycodont: forked antler-like horns),
Antilocapra (pronghorn: real colours known, white rump and throat bands), camels
(Poebrotherium small and gazelle-like; Procamelus and Camelops long-necked, NO hump is
the cautious choice), Merycoidodon (oreodont: pig-like head on a sheep-like body),
Ovis canadensis (bighorn: curled horns, real colours).

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/ungulate.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("ungulate", "slender even-toed ungulates: early artiodactyls, ruminants, pronghorns, camels, oreodonts, sheep")
