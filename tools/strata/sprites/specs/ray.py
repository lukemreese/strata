"""Species specs for the ray body plan (plans/ray.py). Owned by the aqua artist.
See specs/fish.py for the common keys and the plan docstring for the knobs."""

from ..core.color import ramp

SPECS = {
    # Heliobatis radians, Green River Fm (~52 Ma): a small freshwater stingray
    # (about 30 cm), a stem relative of the living river stingrays
    # (Potamotrygonidae, Carvalho et al. 2004). Disc nearly round, a little
    # wider than long; small pelvic fins; a long whip tail with a serrated venom
    # spine a third of the way back. Fossils preserve no colour: a sandy brown
    # dorsum with sparse dark spots follows living potamotrygonids and bottom
    # dwellers on pale lake mud; the underside is white.
    "heliobatis": dict(
        ramps={
            "outline": ramp("2a2014"),
            "disc": ramp("6a5434", "927650", "b49870", "d2ba92"),
            "belly": ramp("bcb4a0", "e0dacc", "f8f6ee"),
            "spot": ramp("3e3020"),
            "eye": ramp("c8b058"),
        },
        front=1.0, back=1.15, icon=0.5,
        shiny={"disc": dict(deg=-8, sat=0.45, val=0.72), "spot": dict(deg=0, sat=1.0, val=1.0)},
        disc_w=14.0, disc_l=12.5, snout=1.2, pelvic=1.0, tail=26.0, tail_r=2.2, spine=(0.3, 4.2),
        spots=((-6, 4), (5, 6), (-9, -2), (8, -1), (-3, -6), (3, -3), (0, 7), (-10, 3), (10, 3),
               (-5, -1), (6, -7), (-7, -8), (2, 2)),
    ),
}
