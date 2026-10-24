"""Species specs, one module per body plan (specs/<plan>.py defines SPECS).

SPECS maps art folder -> spec dict; PLAN_OF maps folder -> plan name. A spec
must live in the file of the plan taxonomy.py assigns to it."""

import importlib

from ..taxonomy import PLANS as _TAXONOMY, SPECIES_PLAN

SPECS, PLAN_OF = {}, {}
for _plan in _TAXONOMY:
    _mod = importlib.import_module(f"{__name__}.{_plan}")
    for _folder, _spec in _mod.SPECS.items():
        if SPECIES_PLAN.get(_folder) != _plan:
            raise SystemExit(f"gen_sprite: specs/{_plan}.py has '{_folder}', but taxonomy.py assigns it to "
                             f"{SPECIES_PLAN.get(_folder)!r}")
        SPECS[_folder] = _spec
        PLAN_OF[_folder] = _plan
