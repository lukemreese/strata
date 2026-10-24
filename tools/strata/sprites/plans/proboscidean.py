"""proboscidean body plan: mammoths and mastodons (trunk, tusks, domed head).

Species (taxonomy.py):
    mammuthus     Mammuthus columbi (Natural Trap Cave, WY, 9000 kg)   Act 8 giant

Uses the giant engine of plans/hoofed_giant.py (`side`, `overworld`; keys
documented there). The proboscidean features are data in the spec: the high
single dome is a head `lump`, the muzzle is a short downward stub that the
trunk (a tube extra hanging from it, raised in frame 2 via `alt`) continues,
the tusks are tube extras with a far copy, the ears are small `round` flaps on
the side of the head, and the feet are nailed pads.
"""

from ..core.plan import BodyPlan
from .hoofed_giant import side, overworld, DEFAULTS as GIANT_DEFAULTS, FOOTPRINTS

DEFAULTS = {k: (dict(v) if isinstance(v, dict) else v) for k, v in GIANT_DEFAULTS.items()}
DEFAULTS["ear"] = dict(DEFAULTS["ear"], kind="round", inner=False)
DEFAULTS["leg"] = dict(DEFAULTS["leg"], foot=dict(kind="pad", l=7.0, h=2.6, nails=3))
DEFAULTS["nose"] = None

PLAN = BodyPlan(
    "proboscidean", "mammoths and mastodons: trunk, tusks, domed head",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINTS["pad"], tracks="TRACKS_FOOT",
)
