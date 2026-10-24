"""Body-plan templates, one module per plan (names from taxonomy.PLANS).
Each module defines PLAN = BodyPlan(...) (core/plan.py) or a stub()."""

import importlib

from ..taxonomy import PLANS as _TAXONOMY

PLANS = {}
for _name in _TAXONOMY:
    _mod = importlib.import_module(f"{__name__}.{_name}")
    if _mod.PLAN.name != _name:
        raise SystemExit(f"gen_sprite: plans/{_name}.py defines PLAN '{_mod.PLAN.name}'")
    PLANS[_name] = _mod.PLAN
