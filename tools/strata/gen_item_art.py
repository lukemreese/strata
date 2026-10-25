#!/usr/bin/env python3
"""Generate Strata's specimen-capsule art (the Poke Ball replacement) for every
place the game draws one. Thin CLI over tools/strata/sprites/items/.

Usage (from the repo root):
    python3 tools/strata/gen_item_art.py                  write every asset
    python3 tools/strata/gen_item_art.py balls bag ...    only these target groups
    python3 tools/strata/gen_item_art.py --list           the target groups
    python3 tools/strata/gen_item_art.py --review OUT.png [--before REF]
                                                          stock (git REF) vs new, side by side

Writes stock-format files in place (graphics/balls, items/icons + icon_palettes,
object_events ball_*, battle_interface, party_menu, bag, pokedex, field_effects,
battle_transitions, starter_choose). Then make. See docs/strata_art.md, "Item art".
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprites.items import targets  # noqa: E402


def main(args):
    if "--list" in args:
        for name, fn in targets.TARGETS:
            print(f"{name:20} {(fn.__doc__ or '').strip().splitlines()[0] if fn.__doc__ else ''}")
        return
    if "--review" in args:
        from sprites.items import review
        i = args.index("--review")
        out = args[i + 1]
        before = args[args.index("--before") + 1] if "--before" in args else None
        review.sheet(out, before)
        return
    names = {n for n, _ in targets.TARGETS}
    bad = [a for a in args if a not in names]
    if bad:
        sys.exit(f"gen_item_art: unknown target group(s) {', '.join(bad)} (see --list)")
    written = targets.build(set(args) or None)
    print(f"gen_item_art: wrote {len(written)} files")


if __name__ == "__main__":
    main(sys.argv[1:])
