"""carnivoran body plan: STUB. Covers cats, bears, mustelids, miacids/viverravids, creodonts (oxyaenids, hyaenodonts), triisodonts.

Species (taxonomy.py):
    protictis     Protictis (Paleocene, MT/WY, 1.5 kg)
    miacis        Miacis (Bridger Fm, WY, 1.5 kg)
    mustela       Mustela nigripes (Living; MT, 0.9 kg)
    hoplophoneus  Hoplophoneus (Brule Fm, SD, 50 kg)
    miracinonyx   Miracinonyx trumani (Natural Trap Cave, WY, 70 kg)
    panthera      Panthera atrox (Natural Trap Cave, WY, 350 kg)
    arctodus      Arctodus simus (Natural Trap Cave, WY, 900 kg)
    oxyaena       Oxyaena (Willwood Fm, WY, 20 kg)
    patriofelis   Patriofelis ferox (Bridger Fm, WY, 70 kg)
    hyaenodon     Hyaenodon horridus (Brule Fm, SD, 40 kg)
    eoconodon     Eoconodon (Denver Fm, CO, 30 kg)

Anatomy and colour notes for the artist:
Several sub-builds: weasel-long (Protictis, Miacis, Mustela: black-footed
ferret mask and feet are real colours), cat (Hoplophoneus: sabre canines, short legs;
Miracinonyx: cheetah build; Panthera atrox: lion, maybe faint spots/no mane is debated),
bear (Arctodus: long legs, short face), creodont (Oxyaena, Patriofelis: low, heavy,
plantigrade, long tail; Hyaenodon: big head, long skull, dog-like legs), and
Eoconodon (triisodont: wolf-sized, heavy, blunt teeth). Consider sub-templates in
this module (weasel(), cat(), bear(), creodont()).

To implement: write side(p, phase=0, step=None) (and overworld(p, view, step),
optionally back(p, phase)) following plans/small_mammal.py and plans/fish.py, pass
them to BodyPlan below, and add specs to specs/carnivoran.py. Read the style guide in
docs/strata_art.md first.
"""

from ..core.plan import stub

PLAN = stub("carnivoran", "cats, bears, mustelids, miacids/viverravids, creodonts (oxyaenids, hyaenodonts), triisodonts")
