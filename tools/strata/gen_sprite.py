#!/usr/bin/env python3
"""Generate original creature sprites. Thin CLI over tools/strata/sprites/.

Usage (from the repo root):
    python3 tools/strata/gen_sprite.py <species> [...]     those species (art folder names)
    python3 tools/strata/gen_sprite.py --all               every species with a spec (also: no arguments)
    python3 tools/strata/gen_sprite.py --plan NAME         every species with a spec in one body plan
      add --preview DIR to write review images (sheet, 6x front, battle and overworld mock-ups)
    python3 tools/strata/gen_sprite.py --contact OUT.png [--scale N]
                                                           every roster species' front sprite on one PNG
    python3 tools/strata/gen_sprite.py --borrowed [--strict]
                                                           art status; --strict exits 1 if any species
                                                           still uses borrowed stock sprites
    python3 tools/strata/gen_sprite.py --plans             the body-plan table (species per plan, lanes)

Writes graphics/pokemon/strata/<folder>/ (anim_front, back, normal/shiny pal, icon,
footprint, overworld, CUSTOM); see tools/strata/sprites/core/build.py and
docs/strata_art.md. Run gen_species.py afterwards, then make.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sprites  # noqa: E402
from sprites import check  # noqa: E402


def take(args, flag, value=False):
    if flag not in args:
        return None
    i = args.index(flag)
    if value:
        if i + 1 >= len(args):
            sys.exit(f"gen_sprite: {flag} needs a value")
        v = args[i + 1]
        del args[i:i + 2]
        return v
    del args[i]
    return True


def main():
    args = sys.argv[1:]
    roster = sprites.roster()
    errors = sprites.check_taxonomy(roster)
    if errors:
        sys.exit("gen_sprite: " + "\n  ".join(errors))

    preview = take(args, "--preview", value=True)
    contact = take(args, "--contact", value=True)
    scale = take(args, "--scale", value=True)
    plan = take(args, "--plan", value=True)
    every = take(args, "--all")
    borrowed = take(args, "--borrowed")
    strict = take(args, "--strict")
    plans_table = take(args, "--plans")
    unknown = [a for a in args if a.startswith("--")]
    if unknown:
        sys.exit(f"gen_sprite: unknown option {unknown[0]} (see the docstring)")

    if plans_table:
        for name, (covers, folders) in sprites.TAXONOMY.items():
            state = "template" if sprites.PLANS[name].ready else "stub"
            print(f"{name:<18} {len(folders):>2} {state:<8} {', '.join(folders)}")
        print("lanes:", " | ".join(" + ".join(lane) for lane in sprites.LANES))
        return
    if borrowed or strict:
        status = check.art_status(roster, sprites.SPECS, sprites.SPECIES_PLAN, sprites.PLANS)
        n = check.report(status, list(sprites.TAXONOMY), strict=bool(strict))
        sys.exit(1 if strict and n else 0)
    if contact:
        from sprites.core import preview as pv
        status = check.art_status(roster, sprites.SPECS, sprites.SPECIES_PLAN, sprites.PLANS)
        pv.contact_sheet(contact, status, sprites.SPECIES_PLAN, list(sprites.TAXONOMY), int(scale or 2))
        return

    if plan:
        if plan not in sprites.PLANS:
            sys.exit(f"gen_sprite: no body plan {plan} (have: {', '.join(sprites.PLANS)})")
        names = [f for f in sprites.TAXONOMY[plan][1] if f in sprites.SPECS]
        if not names:
            print(f"gen_sprite: no specs in plan {plan} yet")
    elif every or not args:
        names = [sp["folder"] for sp in roster if sp["folder"] in sprites.SPECS]
    else:
        names = args
    for name in names:
        sprites.build(sprites.species(name), preview)


if __name__ == "__main__":
    main()
