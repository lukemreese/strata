"""Art status of every roster species, for driving borrowed stock art to zero.

    own       a CUSTOM marker (gen_sprite.py output) exists
    borrowed  no CUSTOM: gen_species.py copies the `borrow=` stock sprites
    spec      a spec exists in specs/<plan>.py (gen_sprite.py can draw it)
    ow        overworld views: south+north+west, side-only, or none
Cries are all still borrowed (`borrow=`); see docs/strata_art.md, "Cries".
"""

import os

from .core.paths import species_dir


def art_status(roster, specs, species_plan, plans):
    out = []
    for sp in roster:
        d = species_dir(sp["folder"])
        custom = os.path.exists(os.path.join(d, "CUSTOM"))
        ow = "none"
        if custom:
            with open(os.path.join(d, "CUSTOM")) as f:
                line = next((l for l in f if l.startswith("@overworld")), None)
            if line and os.path.exists(os.path.join(d, "overworld.png")):
                ow = line.split()[4] if len(line.split()) > 4 else "south+north+west"
        plan = species_plan[sp["folder"]]
        out.append(dict(sp, custom=custom, spec=sp["folder"] in specs, plan=plan,
                        plan_ready=plans[plan].ready, ow=ow))
    return out


def report(status, plan_order, strict=False):
    """Prints the per-plan table; returns the number of borrowed species."""
    borrowed = [s for s in status if not s["custom"]]
    print(f"{'plan':<18} {'own':>4} {'borrowed':>8}  status")
    for plan in plan_order:
        members = [s for s in status if s["plan"] == plan]
        own = [s for s in members if s["custom"]]
        state = "template" if members and members[0]["plan_ready"] else "STUB"
        names = ", ".join(s["folder"] for s in members if not s["custom"])
        print(f"{plan:<18} {len(own):>4} {len(members) - len(own):>8}  {state:<8} {names}")
    print()
    for s in status:
        if s["spec"] and not s["custom"]:
            print(f"  {s['folder']}: has a spec but no output; run gen_sprite.py {s['folder']}")
        if s["custom"] and not s["spec"]:
            print(f"  {s['folder']}: CUSTOM art without a spec (hand-made or stale)")
        if s["custom"] and s["ow"] != "south+north+west":
            print(f"  {s['folder']}: overworld {s['ow']}")
    print(f"borrowed stock sprites: {len(borrowed)} of {len(status)} species")
    print(f"borrowed stock cries:   {len(status)} of {len(status)} species (no original cries yet)")
    if strict and borrowed:
        print("STRICT: every species needs its own art")
    return len(borrowed)
