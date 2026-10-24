"""rhino_brontothere body plan: rhinocerotoids (hornless and horned) and brontotheres.

Species (taxonomy.py):
    hyrachyus     Hyrachyus modestus (Bridger Fm, WY, 70 kg)
    subhyracodon  Subhyracodon (Brule Fm, SD, 500 kg)
    teleoceras    Teleoceras major (Ashfall, NE, 1800 kg)     Act 7 boss
    aphelops      Aphelops (Ashfall, NE, 1500 kg)

The rhino line (Hyrachyus -> Subhyracodon -> Teleoceras / Aphelops; grades,
not proven ancestors) uses the giant engine of plans/hoofed_giant.py (`side`,
`overworld`; keys documented there) with rhino family features carried by the
specs: tall tubular ears with dark rims, a pale upper lip and chin, three-toed
feet with pale nails, skin folds behind the shoulder and before the thigh,
and a grey-brown ramp that greys along the line. Proportions carry the story:
light and long-legged (Hyrachyus), cow-like (Subhyracodon), barrel-bodied and
short-legged with a small nasal horn (Teleoceras), long-legged and hornless
with a pointed browsing lip (Aphelops).
"""

from ..core.plan import BodyPlan
from .hoofed_giant import side, overworld, DEFAULTS as GIANT_DEFAULTS, FOOTPRINTS

DEFAULTS = {k: (dict(v) if isinstance(v, dict) else v) for k, v in GIANT_DEFAULTS.items()}
DEFAULTS["ear"] = dict(DEFAULTS["ear"], kind="leaf", lean=18.0)
DEFAULTS["leg"] = dict(DEFAULTS["leg"], foot=dict(kind="pad", l=5.0, h=2.2, nails=3))

PLAN = BodyPlan(
    "rhino_brontothere", "rhinocerotoids (hornless and horned) and brontotheres",
    side=side, overworld=overworld, defaults=DEFAULTS, footprint=FOOTPRINTS["rhino"], tracks="TRACKS_FOOT",
)
