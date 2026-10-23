"""Strata species roster: the single source of truth for every Strata species.

Run tools/strata/gen_species.py after editing to regenerate the C data.

Every species is a real, fossil-documented (or living) animal. Fields:
  name      In-game name, max 12 chars. Genus where it fits, else the informal
            anglicized form (Tyrannosaurus -> Tyrannosaur), else the genus cut
            at a morpheme boundary. `genus` always holds the full name.
  genus     Full scientific name shown in the Codex.
  site      Fossil occurrence used for the game (formation / locality).
  age       Approximate age of that occurrence.
  mass      Body mass in kg. Drives the base stat total (see gen_species.py).
  length    Body length in m (stored as the dex "height").
  mass_est  True when no published estimate exists and the mass is our own
            estimate from size comparisons. Shown as such in the Codex.
  focal     True for the starter lineages (every species a starter can descend
            into). Adds a flat +40 to the base stat total: a game concession so
            the lineage the player carries stays usable (gen_species.py).
  weights   Relative stat split {hp, atk, def, spa, spd, spe}, from anatomy:
            atk = bite/weapon, def = armour/shell, spe = locomotion,
            spa = senses/brain, spd = hardiness, hp = bulk.
  types     Ecological types; see docs/strata_design.md §7.6.
  borrow    Stock Pokémon whose sprites/cry are used as placeholders.
  notes     Caveats for the Codex: stand-ins, debated placements.

=============================================================================
ORDER RULE: NEW SPECIES ARE ALWAYS APPENDED AT THE END OF THE GLOBAL LIST.
=============================================================================
A species' position in SPECIES is its species ID and its National Dex number,
and every generated splice (species.h, pokedex.h, cries) follows it. The list is
the concatenation of the modules in PARTS, in that order. The existing modules
hold the species that already exist, grouped by act, but their order is frozen:
do not insert, remove or reorder species in them (editing a species' fields in
place is fine). A new species belongs in PART3 (roster/part3.py, appended at the
end), even when it belongs to an early act; its `site`/`age`/`first_era` fields
say where it lives, not its position in the file. If several agents add species
in parallel, give each their own file (part4.py, part5.py, ...) and append it to
PARTS below, so they never touch the same file; land them in a fixed order.

Modules:
  starters.py           the dog, bird and snapping-turtle starter lines
  act1_2_hell_creek.py  Hell Creek (Act 1) and impact-winter survivors (Act 2)
  act3_corral_bluffs.py ... act8_ice_age.py, epilogue.py   Cenozoic acts, present day
  part3.py              new species, append-only
"""

from . import (
    starters, act1_2_hell_creek, act3_corral_bluffs, act4_bighorn, act5_green_river,
    act6_white_river, act7_ashfall, act8_ice_age, epilogue, part3,
)

# Do not reorder. Append new parts at the END.
PARTS = [
    starters, act1_2_hell_creek, act3_corral_bluffs, act4_bighorn, act5_green_river,
    act6_white_river, act7_ashfall, act8_ice_age, epilogue,
    part3,
]

SPECIES = [sp for part in PARTS for sp in part.SPECIES]
