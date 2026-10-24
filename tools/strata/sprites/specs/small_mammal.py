"""Species specs for the small-mammal body plan (plans/small_mammal.py).
Owned by the small-mammal artist. See specs/fish.py for the common keys."""

from ..core.color import ramp

SPECS = {
    # Mesodma, Hell Creek Fm (latest Cretaceous): a ~30 g multituberculate.
    # Mouse-sized and rodent-like by convergence: short deep snout, procumbent
    # lower incisors, a long tail (ptilodontoids had reversible hind feet and are
    # reconstructed as climbers). Fur colour is unknown; a muted agouti brown with
    # a pale belly is the conservative choice.
    "mesodma": dict(
        ramps={
            "outline": ramp("2a1c16"),
            "fur": ramp("5a3a28", "82583c", "a87c56", "cca476"),
            "belly": ramp("b4967a", "d8c2a0", "f0e2c8"),
            "skin": ramp("8c5e5c", "bc8880", "e2b2a6"),
            "white": ramp("fcfcf4"),
        },
        front=0.9, back=0.95, icon=0.46,
        shiny={"fur": dict(deg=-12, sat=0.45, val=1.12)},
        sniff=7, neck=(-10.0, 2.0),
        torso=[(7.0, 2.5, 11.5, 9.8, -8), (-4.0, 5.0, 9.0, 7.6, 5)],
        head=[(-16.0, -0.8, 8.8, 7.6, -12), (-22.8, 2.0, 5.2, 4.2, 10)],
        ear=(-11.0, -7.6, 3.6, 4.2, 20),
        thigh=(10.0, 7.0, 6.2, 6.8, 20),
        legs=[  # far legs first
            dict(near=False, swing=1, z=-2, foot_z=-1.9,
                 pts=[(15.0, 10.0), (14.5, 15.5), (13.0, 16.8)], radii=[2.4, 1.8, 1.5], foot=(11.0, 17.6, 3.8, 1.4)),
            dict(near=False, swing=-1, z=-2, foot_z=-1.9, fore=True,
                 pts=[(-2.5, 9.0), (-3.0, 13.5), (-4.5, 16.5)], radii=[2.6, 2.0, 1.6], foot=(-5.6, 17.2, 2.4, 1.3)),
            dict(near=True, swing=-1, z=2, foot_z=2.1, toes=((2.0, 3.6, 5.2), 18.4),
                 pts=[(10.0, 11.0), (8.0, 15.5), (6.5, 16.8)], radii=[2.6, 2.0, 1.6], foot=(4.2, 17.6, 4.4, 1.5)),
            dict(near=True, swing=1, z=4, foot_z=4.1, fore=True, lift=1.8, toes=((-12.5, -11.0), 17.6),
                 pts=[(-7.0, 8.5), (-8.5, 13.0), (-10.5, 16.0)], radii=[3.0, 2.2, 1.7], foot=(-11.8, 16.8, 2.6, 1.4)),
        ],
        curl=2.0,
        tail=[(16.0, 5.0, 0, 0), (22.0, 3.5, 0, 0), (26.5, -1.0, 0, 0), (28.5, -7.0, -0.5, 0),
              (27.0, -12.0, -1, 0.5), (23.5, -14.5, -1, 1)],
        tail_radii=[2.6, 2.1, 1.8, 1.5, 1.3, 1.1],
        belly_line=(7.0, 0.10),
        jaw=(-16.0, 2.6, -0.10),
        inner_ear=((-10.8, -7.0), 2.1, 1.2),
        fur_dashes=(3, 5),
        nose=((-27.0, 0.6), 1.3, 0.8),
        nostril=(-27.3, 0.0),
        mouth=[(-26.0, 3.2), (-22.5, 4.4)],
        incisors=[(-25.0, 4.6), (-25.0, 5.6)],
        eye=((-18.2, -2.0), 2.6, 1.2),
        whiskers=[((-24.0, 1.5), (-31.0, -1.0)), ((-24.0, 2.5), (-31.5, 3.5))],
    ),
}
