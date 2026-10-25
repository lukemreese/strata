"""Strata item art: the specimen capsule (Poke Ball replacement) everywhere the
game draws one. CLI: tools/strata/gen_item_art.py; docs: docs/strata_art.md,
section "Item art".

    capsule.py  the capsule drawing at any size (role grids) + the 7x7 tile version
    tiers.py    per-capsule colours and markings, tier palettes
    grid.py     role grids, placement, indexed PNG read/write helpers
    targets.py  one writer per asset family (balls, icons, HUD, menus, field, ...)
    scenes.py   full-screen BGs: starter field case, cave transition capsule
    review.py   stock-vs-new review sheet
"""
