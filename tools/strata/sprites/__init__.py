"""Strata creature sprite pipeline.

    core/       rasteriser, shading/outline, palettes, writers, previews
    plans/      one parametric template per body plan (BodyPlan or stub)
    specs/      one SPECS dict per body plan: the species data
    taxonomy.py species -> body plan, the one table
    check.py    art status: borrowed sprites, missing specs, side-only overworld

CLI: tools/strata/gen_sprite.py. Docs and style guide: docs/strata_art.md.
"""

import re

from .core import paths  # noqa: F401  (puts tools/strata on sys.path)
from .core.build import Species, build  # noqa: F401
from .plans import PLANS
from .specs import SPECS, PLAN_OF  # noqa: F401
from .taxonomy import PLANS as TAXONOMY, SPECIES_PLAN, LANES  # noqa: F401


def folder_name(name):
    """Same rule as gen_species.folder_name."""
    return re.sub(r"[^a-z0-9]", "_", name.lower())


def roster():
    """Roster species with their art folder, in species-ID order."""
    from roster import SPECIES as ROSTER
    return [dict(sp, folder=folder_name(sp["name"])) for sp in ROSTER]


def check_taxonomy(species=None):
    """Every roster species is in exactly one plan, and nothing else is."""
    species = species or roster()
    folders = [sp["folder"] for sp in species]
    listed = [f for _, fs in TAXONOMY.values() for f in fs]
    errors = []
    dup = sorted({f for f in listed if listed.count(f) > 1})
    if dup:
        errors.append(f"in more than one plan: {', '.join(dup)}")
    missing = [f for f in folders if f not in SPECIES_PLAN]
    if missing:
        errors.append(f"roster species with no body plan in taxonomy.py: {', '.join(missing)}")
    extra = [f for f in listed if f not in folders]
    if extra:
        errors.append(f"taxonomy.py names species not in the roster: {', '.join(extra)}")
    return errors


def species(folder):
    sp = next((s for s in roster() if s["folder"] == folder), None)
    if sp is None:
        raise SystemExit(f"gen_sprite: {folder} is not a roster species")
    if folder not in SPECS:
        plan = SPECIES_PLAN[folder]
        raise SystemExit(f"gen_sprite: no spec for {folder} yet (add it to tools/strata/sprites/specs/{plan}.py)")
    plan = PLANS[PLAN_OF[folder]]
    if not plan.ready:
        raise SystemExit(f"gen_sprite: {folder}'s body plan '{plan.name}' is still a stub")
    return Species(folder, plan, SPECS[folder], sp["mass"])
