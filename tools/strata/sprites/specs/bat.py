"""Species specs for the bat body plan (plans/bat.py, which documents the keys).
Owned by the small-mammal artist. See specs/fish.py for the common keys."""

from ..core.color import ramp

SPECS = {
    # Onychonycteris finneyi, Green River Fm (~52.5 Ma), ~40 g, ~10 cm body,
    # ~30 cm span: one of the oldest bats, from two complete skeletons.
    # Claws on all five fingers (living bats keep one or two), short, broad
    # wings (a fluttering, gliding flight), long hind legs for climbing, a
    # long tail in a tail membrane. Its small cochlea suggests it did not
    # echolocate like modern bats (debated), so it has big eyes and moderate
    # ears here. Colour speculative: warm brown fur, paler belly, dark brown
    # membranes, as in many living insectivorous bats.
    "onychonycter": dict(
        ramps={
            "outline": ramp("1e1612"),
            "fur": ramp("4e3426", "72503a", "966e50"),
            "pale": ramp("aa8a6a", "ccb08e"),
            "wing": ramp("382824", "54403a", "705850"),
            "skin": ramp("6c463e", "986c60"),
            "claw": ramp("e2d6be"),
            "white": ramp("f6f2e8"),
        },
        front=1.22, back=1.0, icon=0.56,
        shiny={"fur": dict(deg=10, sat=0.5, val=1.5), "pale": dict(deg=10, sat=0.4, val=1.12),
               "wing": dict(deg=8, sat=0.7, val=1.25)},
        flap=38.0,
        body=dict(e=(2.0, 0.0, 7.5, 4.6, -8), belly=1.0),
        head=dict(c=(-7.6, -2.8), r=(4.8, 4.3)),
        snout=dict(a=(-10.4, -1.4), b=(-13.8, -0.6), r=[2.4, 1.4]),
        ear=dict(near=(-5.4, -8.6, 2.0, 3.8, 16), far=(-8.6, -8.2, 1.8, 3.4, -6)),
        eye=dict(c=(-9.6, -3.4), r=1.5),
        mouth=[(-13.0, 0.6), (-10.0, 1.2)],
        wing=dict(S=(0.0, -3.5), E=(5.0, -11.0), W=(0.5, -22.0), thumb=(-3.0, -24.0),
                  tips=[(7.0, -31.0), (17.0, -28.0), (22.0, -18.0), (17.0, -7.0)],
                  ankle=(10.5, 6.5), hip=(7.0, -3.2), scallop=0.24),
        far_wing=dict(dx=-4.0, dy=0.5, deg=-16.0),
        legs=dict(near=[(6.0, 2.0), (10.0, 5.0), (9.5, 8.0)], far=[(4.0, 2.0), (7.5, 5.5), (7.0, 8.5)],
                  r=[1.5, 1.1, 0.9]),
        tail=dict(pts=[(9.0, 1.5), (14.0, 4.0), (18.0, 7.5)], r=[1.0, 0.8, 0.6],
                  membrane=[(9.0, 1.5), (18.0, 7.5), (9.5, 8.5)]),
        spread=dict(S=(3.0, -3.0), E=(9.0, -6.0), W=(16.0, -11.0), thumb=(17.0, -14.5),
                    tips=[(22.0, -19.0), (28.0, -11.0), (27.0, -1.0), (19.0, 5.0)],
                    ankle=(4.0, 9.0), hip=(3.0, 4.0), scallop=0.22, up=14.0, down=-14.0),
        spread_body=dict(cy=0.0, rx=4.4, ry=6.5, head=(-8.0, 4.0), ear=(2.6, -3.6, 1.6, 2.8),
                         leg=[(2.0, 5.0), (4.0, 9.0)], tail=12.0),
        ow=dict(end_zoom=0.85, tracks="TRACKS_NONE", shadow="SHADOW_SIZE_S"),
    ),
}
