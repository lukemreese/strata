"""Species specs for the theropod body plan (plans/theropod.py). See specs/fish.py
for the common keys and plans/theropod.py for the shape data and pose groups."""

from ..core.color import ramp

SPECS = {
    # Tyrannosaurus rex, Hell Creek Fm (66 Ma): 12.3 m, ~8 t. The Act 1 boss.
    # Deep, broad-backed skull with forward-facing eyes under heavy brow bosses,
    # lipped jaws (teeth hidden when closed: Cullen et al. 2023), tiny two-fingered
    # arms, a massive thigh, three forward toes, horizontal back. Skin impressions
    # are small pebbly scales (Bell et al. 2017), so it is scaly here. Colour is a
    # reconstruction: dark umber above, pale buff below, faint darker saddle bands
    # (speculative, as in big living predators of open woodland). The pose is a
    # three-quarter-ish stance with the tail raised and receding so the animal
    # fills the battle frame. Frame 2: the roar (jaws open, head raised).
    # Variant: a paler, sandy population.
    "tyrannosaur": dict(
        ramps={
            "outline": ramp("22180f"),
            "skin": ramp("3e2e22", "5e4632", "806246", "a68662"),
            "belly": ramp("9c8a6a", "c2b08a", "e2d4b0"),
            "mouth": ramp("5c2626", "9a4a44"),
            "eye": ramp("e0a040"),
            "white": ramp("f2ecd8"),
            "claw": ramp("bcae94"),
        },
        front=0.88, back=0.88, icon=0.43, ow=dict(end_zoom=1.05),
        shiny={"skin": dict(deg=8, sat=0.7, val=1.25), "belly": dict(deg=5, sat=0.8, val=1.05)},
        body=[
            ("E", -1.0, -3.0, 16.0, 10.0, -4),
            ("E", -11.0, 2.0, 8.0, 8.5, 0),
            ("E", 9.0, -6.0, 9.0, 8.5, 0),
            ("T", [(-12.0, -5.0), (-17.0, -11.0), (-19.0, -14.0)], [8.0, 7.2, 6.8]),
            ("T", [(12.0, -6.0), (20.0, -9.0), (27.0, -12.0), (32.0, -16.0), (34.5, -21.0)],
             [8.0, 6.2, 4.5, 3.0, 1.6]),
        ],
        tail_shapes=(4,), tail_base=(12.0, -6.0), tail_reach=24.0,
        body_k=0.15,
        belly=[(-26, -4), (-15, -1), (0, 3), (10, 2), (20, -4), (28, -9), (36, -16)],
        neck=(-17.0, -12.0),
        head=("L", -34.0, -15.0, [(0, 1.8), (0.12, 3.2), (0.45, 4.5), (0.7, 5.8), (1, 6.2)],
              [(0, 1.2), (0.2, 1.8), (0.6, 2.4), (1, 3.6)], 1.5, -19.0),
        head_belly=[(-40, -14.5), (-10, -14.5)],
        jaw_pivot=(-16.0, -15.0),
        jaw=("L", -33.0, -13.0, [(0, 0.6), (0.15, 1.2), (0.5, 1.5), (1, 2.5)],
             [(0, 0.8), (0.15, 1.6), (0.4, 2.0), (0.75, 3.0), (1, 3.6)], -1.5, -13.0),
        jaw_belly=[(-40, -13.5), (-10, -12.5)],
        mouth=("P", [(-32.0, -17.5), (-16.0, -16.5), (-17.0, -12.0), (-31.0, -6.0)]),
        eye=dict(c=(-20.5, -21.0), r=1.6, brow=[(-23.0, -23.2), (-20.5, -23.8), (-18.5, -23.2)]),
        nostril=(-31.5, -19.5),
        lip=[(-33.0, -16.4), (-24.0, -15.8), (-17.0, -15.2)],
        teeth=dict(upper=[(-31.0, -14.8), (-28.5, -14.6), (-26.0, -14.4), (-23.5, -14.2), (-21.0, -14.0)],
                   lower=[(-30.0, -16.0), (-27.0, -16.2), (-24.0, -16.3), (-21.0, -16.5)]),
        tongue=("E", -23.0, -15.0, 6.0, 1.4, 0),
        extras=[  # lacrimal boss in front of the eye, postorbital boss behind it
            dict(s=("E", -23.0, -24.0, 2.4, 1.3, -10), ramp="skin", z=4.05, group="head", inner=("skin", 0)),
        ],
        arms=[
            dict(near=False, pts=[(-8.0, 1.0), (-10.0, 6.0), (-13.0, 7.5)], radii=[2.0, 1.5, 1.1], z=-1),
            dict(near=True, pts=[(-10.0, 2.0), (-12.0, 7.0), (-15.0, 8.0)], radii=[2.2, 1.6, 1.2], z=3,
                 claws=[(-16.0, 8.6)]),
        ],
        legs=[
            dict(near=False, swing=-1, z=-2, pts=[(11.0, -2.0), (8.0, 10.0), (16.0, 18.0), (14.0, 24.5)],
                 radii=[5.5, 3.8, 2.8, 2.2], foot=("T", [(14.5, 25.5), (8.5, 26.0)], [2.1, 1.5])),
            dict(near=True, swing=1, z=2, pts=[(8.0, -2.0), (4.0, 11.0), (10.0, 19.0), (7.0, 25.0)],
                 radii=[6.0, 4.2, 3.0, 2.4], thigh=("E", 7.0, 1.0, 7.0, 10.0, 22), thigh_flat=0.3,
                 foot=("T", [(8.0, 25.8), (0.5, 26.2)], [2.3, 1.6]), claws=[(-1.0, 26.6), (1.5, 27.2)]),
        ],
        action=dict(head=7.0, jaw=-28.0, tail=-5.0, arms=8.0),
        walk=16.0,
        texture=[
            dict(kind="scales", ramp="skin", rows=3, cols=4, shift=2, levels=(1, 2)),
            dict(kind="bands", ramp="skin", period=7.0, width=0.32, x0=-8.0, x1=32.0,
                 top=[(-20, -8), (0, -6), (14, -10), (24, -15), (32, -22)], levels=(1, 3)),
        ],
        end=dict(
            body_w={0: 9.5, 1: 7.5, 2: 8.5}, leg_w=7.5, arm_w=4.5, head_zoom=1.35, head_zoom_n=1.0, kd=0.6, head_shift_n=(0.0, 10.0),
            tail_flat=0.25, tail_side=8.0, tail_drop=14.0,
            head=[("U", [("S", -19.0, -20.5, 0.0, 5.0, 5.5, 7.0),      # broad cranium
                         ("S", -25.0, -19.0, 0.0, 5.0, 4.2, 5.2),      # snout
                         ("S", -30.5, -18.0, 0.0, 3.5, 3.0, 3.8)], 0.15),
                  dict(s=("S", -24.0, -14.8, 0.0, 9.0, 2.2, 5.4), ramp="skin", light=-0.15)],  # lower jaw
            eyes=(-21.0, -21.8, 5.4), eye_r=1.3,
            lines=[("south", [(-32.0, -16.6, -2.6), (-26.0, -16.2, -4.6), (-19.0, -15.6, -6.4)], "outline", True),
                   ("south", [(-23.0, -24.0, -3.0), (-21.0, -24.5, -5.5)], -2, True),
                   ("south", [(-33.2, -19.5, -1.2), (-33.2, -19.5, -1.2)], "outline", True)],
        ),
    ),

    # Acheroraptor temertyorum, Hell Creek Fm (66 Ma): a velociraptorine
    # dromaeosaurid known from a maxilla and dentaries; ~3 m, ~40 kg is
    # extrapolated from relatives. Dromaeosaurs had pennaceous wing feathers on
    # the arms (quill knobs in Velociraptor) and a frond of tail feathers, so it
    # is fully feathered: no naked raptors. Long low snout, big eyes, S-neck,
    # folded wings, stiff tail, the raised sickle claw on toe II. Colour is a
    # reconstruction: hawk-like brown above with darker barring on the wings and
    # tail, pale buff below, scaly grey-brown feet. Frame 2: a threat display
    # (hiss, wings half raised). Variant: a melanistic morph.
    "acheroraptor": dict(
        ramps={
            "outline": ramp("22170f"),
            "plume": ramp("3e2c20", "60432f", "886044", "b08660"),
            "belly": ramp("b09c80", "d2c2a2", "eee4cc"),
            "wing": ramp("3a2a20", "5c4232"),
            "skin": ramp("4a4640", "7a7264"),
            "mouth": ramp("8a3c38"),
            "eye": ramp("d8b048"),
            "white": ramp("f4f0e4"),
        },
        claw_color=("belly", 2),
        front=0.92, back=0.92, icon=0.46, ow=dict(end_zoom=1.6),
        shiny={"plume": dict(deg=0, sat=0.5, val=0.55), "belly": dict(deg=0, sat=0.6, val=0.8)},
        body=[
            ("E", 0.0, -3.0, 10.0, 6.5, -12),
            ("E", -6.0, -1.0, 6.0, 6.0, -10),
            ("E", 6.0, -4.0, 6.5, 6.0, 0),
            ("T", [(-7.0, -5.0), (-11.0, -12.0), (-12.0, -18.0)], [4.8, 3.6, 3.4]),
            ("T", [(9.0, -6.0), (18.0, -9.0), (27.0, -12.0), (34.0, -15.0)], [4.8, 3.2, 2.0, 1.2]),
        ],
        tail_shapes=(4,), tail_base=(9.0, -6.0), tail_reach=26.0,
        body_ragged=(0.28, 1.5, 0.4), body_ramp="plume",
        belly=[(-24, -16), (-12, -8), (-6, 0), (6, 1), (14, -3), (24, -7), (40, -12)],
        neck=(-12.0, -16.0),
        head_ramp="plume",
        head=("L", -27.0, -9.0, [(0, 1.2), (0.3, 2.3), (0.65, 3.8), (1, 4.6)],
              [(0, 0.8), (0.4, 1.3), (1, 2.8)], 1.0, -20.5),
        head_belly=[(-40, -18.6), (-5, -18.0)],
        jaw_pivot=(-11.0, -17.5),
        jaw=("L", -26.0, -10.0, [(0, 0.5), (0.5, 0.9), (1, 1.6)], [(0, 0.6), (0.4, 1.0), (1, 2.2)], -2.0, -16.0),
        jaw_ramp="belly",
        mouth=("P", [(-26.0, -18.8), (-11.0, -18.0), (-11.5, -15.0), (-25.0, -11.0)]),
        tongue=("E", -18.0, -17.6, 4.5, 0.8, 0),
        teeth=dict(upper=[(-25.0, -17.9), (-22.5, -17.7), (-20.0, -17.5), (-17.5, -17.3)],
                   lower=[(-24.0, -18.4), (-21.0, -18.3), (-18.0, -18.0)], length=1),
        eye=dict(c=(-14.6, -21.6), r=1.6, brow=[(-16.6, -23.6), (-13.0, -23.8)]),
        nostril=(-25.0, -20.3),
        lip=[(-26.5, -18.6), (-19.0, -18.2), (-12.0, -17.6)],
        extras=[
            # the tail frond: vanes either side of the tail, widest towards the tip
            dict(s=("P", [(13.0, -9.5), (22.0, -14.0), (31.0, -17.5), (38.0, -19.0), (41.0, -17.0),
                          (38.0, -14.5), (30.0, -10.0), (21.0, -5.5), (13.0, -3.5)]),
                 ramp="plume", z=-0.5, group="tail", normal=(0, -0.3, 1), inner=("plume", 0)),
            # bare scaly snout tip
            dict(s=("L", -27.2, -23.5, [(0, 1.2), (0.5, 1.7), (1, 2.0)], [(0, 0.8), (0.5, 1.0), (1, 1.2)], 0.3, -19.4),
                 ramp="skin", z=4.05, group="head", line=False),
        ],
        lines=[  # barring across the tail frond
            ("tail", [(21.0, -13.0), (20.0, -6.0)], -1, True),
            ("tail", [(28.0, -16.0), (27.0, -9.0)], -1, True),
            ("tail", [(35.0, -18.0), (34.0, -12.5)], -1, True),
        ],
        arms=[
            dict(near=False, pts=[(-4.0, -3.0), (1.0, 0.0), (-4.0, 3.0)], radii=[2.0, 1.6, 1.2], z=-1,
                 ramp="plume",
                 wing=("P", [(-5.0, -5.0), (2.0, -4.5), (9.0, -1.5), (15.0, 1.5), (7.0, 3.0), (-5.0, 3.0)]),
                 wing_z=-1.0, wing_ramp="wing"),
            dict(near=True, pts=[(-6.0, -3.0), (-1.0, 1.0), (-7.0, 4.0)], radii=[2.2, 1.7, 1.3], z=3, ramp="plume",
                 wing=("P", [(-9.0, -4.5), (-1.0, -4.0), (6.0, -1.0), (14.0, 3.0), (11.0, 4.5), (3.0, 6.0),
                             (-6.0, 6.0), (-10.0, 2.0)]),
                 wing_z=3.2, wing_ramp="wing", claws=[(-9.0, 5.6), (-8.0, 6.2)],
                 end_wing=("Q", [(-9.0, -4.5, 4.5), (4.0, -2.0, 5.5), (14.0, 3.0, 6.5), (4.0, 6.0, 7.5), (-8.0, 5.0, 6.0)]),
                 lines=[([(-3.0, -2.0), (8.0, 1.5)], ("belly", 0)), ([(-4.0, 1.5), (10.0, 3.6)], ("belly", 0)),
                        ([(0.0, 5.0), (8.0, 5.2)], ("belly", 0))]),
        ],
        legs=[
            dict(near=False, swing=-1, z=-2, ramp="skin", pts=[(8.0, -2.0), (6.0, 7.0), (11.0, 14.0), (10.0, 20.5)],
                 radii=[3.0, 1.9, 1.2, 1.0], thigh=("E", 7.5, 1.5, 4.4, 6.5, 15), thigh_ramp="plume",
                 foot=("T", [(10.5, 21.2), (5.5, 21.6)], [1.1, 0.9])),
            dict(near=True, swing=1, z=2, ramp="skin", pts=[(5.0, -2.0), (2.0, 8.0), (8.0, 14.5), (6.0, 21.0)],
                 radii=[3.2, 2.0, 1.3, 1.1], thigh=("E", 4.5, 1.5, 5.0, 7.5, 15), thigh_ramp="plume",
                 thigh_ragged=(0.3, 1.6, 0.4),
                 foot=("T", [(6.5, 21.5), (1.0, 21.9)], [1.2, 0.9]), claws=[(0.0, 22.3)],
                 parts=[dict(s=("P", [(6.2, 21.0), (5.6, 18.0), (3.2, 16.8), (1.4, 17.4), (3.8, 18.6), (4.4, 21.2)]),
                             ramp="belly",
                             normal=(0, -0.3, 1), z=0.2)]),
        ],
        action=dict(head=5.0, jaw=-16.0, tail=-4.0, arms=-26.0, arm_lift=3.0),
        walk=18.0, ground=22.0,
        texture=[dict(kind="dashes", ramp="plume", rows=3, cols=5, levels=(1, 2))],
        end=dict(
            body_w={0: 5.5, 1: 5.0, 2: 5.0}, leg_w=4.5, arm_w=5.5, head_zoom=1.7, kd=0.55,
            head_shift=(-3.0, 9.0), head_shift_n=(0.0, 7.0),
            tail_flat=0.0, tail_side=11.0, tail_drop=8.0,
            head=[("U", [("S", -13.0, -21.0, 0.0, 3.5, 3.8, 3.8),
                         ("S", -20.0, -19.5, 0.0, 6.0, 2.2, 2.3)], 0.15),
                  dict(s=("S", -19.0, -17.2, 0.0, 6.5, 1.0, 2.0), ramp="belly")],
            eyes=(-14.6, -21.6, 3.0), eye_r=1.2,
            lines=[("south", [(-26.0, -18.4, -0.8), (-19.0, -18.2, -2.0), (-12.0, -17.6, -3.0)], "outline", True)],
        ),
    ),

    # Anzu wyliei, Hell Creek Fm (66 Ma): the largest North American
    # caenagnathid oviraptorosaur, ~3.5 m, ~250 kg ("chicken from hell"). Tall
    # rounded casque over the snout, deep toothless beak, long S-neck, long legs,
    # big-clawed hands. Oviraptorosaurs had pennaceous wing and tail-fan feathers
    # (Caudipteryx, brooding Citipati), so it is fully feathered. Colour is a
    # reconstruction: dusky grey-brown plumage, buff underside, horn beak; the
    # brick-red casque is speculative (by analogy with the cassowary's display
    # casque). Frame 2: a display (neck up, beak open, wings half spread).
    # Variant: a paler, sandy population.
    "anzu": dict(
        ramps={
            "outline": ramp("1e1816"),
            "plume": ramp("342a24", "524236", "735e4a", "9a8266"),
            "belly": ramp("bcae94", "ddd0b4"),
            "skin": ramp("4e463e", "807460"),
            "beak": ramp("8c7a5c", "cdbb94"),
            "crest": ramp("7a3426", "b0563c"),
            "eye": ramp("e0b040"),
            "white": ramp("f4f0e4"),
        },
        claw_color=("beak", 1), mouth_ramp="crest",
        front=0.95, back=0.95, icon=0.48, ow=dict(length=25, end_zoom=1.2),
        shiny={"plume": dict(deg=6, sat=0.8, val=1.35), "crest": dict(deg=-8, sat=0.8, val=1.1)},
        body_ramp="plume", head_ramp="plume", belly_ramp="belly",
        body=[
            ("E", 2.0, -2.0, 11.0, 7.0, -8),
            ("E", -5.0, 0.0, 6.5, 6.5, 0),
            ("E", 9.0, -3.0, 7.0, 6.0, 0),
            ("T", [(-6.0, -4.0), (-10.0, -12.0), (-11.0, -19.0), (-10.0, -24.0)], [4.6, 3.4, 3.0, 3.0]),
            ("T", [(12.0, -4.0), (20.0, -5.0), (26.0, -5.0)], [4.5, 3.0, 1.8]),
        ],
        tail_shapes=(4,), tail_base=(12.0, -4.0), tail_reach=16.0,
        body_ragged=(0.28, 1.5, 0.4),
        belly=[(-20, -12), (-12, -6), (-6, 2), (6, 3), (14, 0), (30, -2)],
        neck=(-10.0, -23.0),
        head=("L", -20.0, -6.5, [(0, 0.6), (0.3, 2.2), (0.7, 3.6), (1, 3.6)], [(0, 1.4), (0.4, 2.0), (1, 2.6)],
              1.0, -27.0),
        jaw_pivot=(-8.0, -24.5),
        jaw=("L", -19.0, -8.0, [(0, 0.6), (1, 1.2)], [(0, 1.2), (0.35, 2.0), (1, 2.0)], 0.0, -23.5),
        jaw_ramp="beak",
        mouth=("P", [(-19.0, -25.0), (-8.0, -25.0), (-9.0, -22.0), (-17.0, -19.0)]),
        eye=dict(c=(-11.0, -28.5), r=1.4),
        nostril=None,
        lip=[(-19.5, -25.2), (-13.0, -24.8)],
        extras=[
            # horny beak over the front of the snout
            dict(s=("L", -20.2, -13.0, [(0, 0.6), (0.4, 2.0), (1, 3.0)], [(0, 1.4), (0.5, 2.0), (1, 2.4)], 1.0, -26.8),
                 ramp="beak", z=4.05, group="head", inner=("beak", 0)),
            # the casque
            dict(s=("U", [("E", -12.0, -33.0, 3.4, 5.2, 18), ("E", -14.5, -30.0, 2.8, 2.6, 0)]),
                 ramp="crest", z=3.95, group="head", inner=("crest", 0)),
            # the tail fan
            dict(s=("P", [(15.0, -8.0), (24.0, -10.5), (32.0, -10.0), (34.0, -6.0), (31.0, -1.5), (23.0, -0.5),
                          (15.0, -1.0)]),
                 ramp="plume", z=-0.5, group="tail", normal=(0, -0.3, 1), light=-0.15, inner=("plume", 0)),
        ],
        lines=[("tail", [(22.0, -9.0), (22.0, -2.0)], -1, True), ("tail", [(28.0, -9.5), (28.0, -2.0)], -1, True)],
        arms=[
            dict(near=False, pts=[(-2.0, -2.0), (3.0, 2.0), (-2.0, 5.0)], radii=[2.0, 1.6, 1.2], z=-1,
                 wing=("P", [(-4.0, -4.0), (4.0, -3.5), (11.0, 0.0), (16.0, 4.0), (8.0, 6.0), (-3.0, 5.0)]),
                 wing_z=-1.0, wing_light=-0.2),
            dict(near=True, pts=[(-4.0, -2.0), (1.0, 2.0), (-5.0, 5.5)], radii=[2.3, 1.8, 1.4], z=3,
                 wing=("P", [(-7.0, -3.5), (2.0, -3.0), (10.0, 1.0), (16.0, 6.5), (9.0, 8.0), (0.0, 8.5),
                             (-6.0, 7.0)]),
                 wing_z=3.2, wing_light=0.15, claws=[(-7.5, 6.5), (-6.5, 7.5)],
                 lines=[([(-3.0, 0.0), (9.0, 3.5)], -2), ([(-3.0, 4.0), (12.0, 6.0)], -2), ([(0.0, 7.6), (9.0, 7.2)], ("belly", 0))]),
        ],
        legs=[
            dict(near=False, swing=-1, z=-2, ramp="skin", pts=[(10.0, -1.0), (7.0, 9.0), (13.0, 16.0), (11.5, 23.0)],
                 radii=[3.2, 2.2, 1.5, 1.2], thigh=("E", 9.5, 2.0, 4.6, 7.5, 15), thigh_ramp="plume",
                 foot=("T", [(12.0, 23.5), (6.5, 23.9)], [1.2, 1.0])),
            dict(near=True, swing=1, z=2, ramp="skin", pts=[(7.0, -1.0), (3.0, 9.0), (9.0, 16.0), (7.0, 23.0)],
                 radii=[3.4, 2.4, 1.6, 1.3], thigh=("E", 6.5, 2.0, 5.2, 8.0, 15), thigh_ramp="plume",
                 thigh_ragged=(0.3, 1.6, 0.4),
                 foot=("T", [(7.5, 23.5), (1.5, 23.9)], [1.3, 1.0]), claws=[(0.5, 24.3)]),
        ],
        action=dict(head=8.0, jaw=-14.0, tail=-6.0, arms=-24.0, arm_lift=3.0),
        walk=18.0, ground=24.0,
        texture=[dict(kind="dashes", ramp="plume", rows=3, cols=5, levels=(1, 2))],
        end=dict(
            body_w={0: 6.5, 1: 6.0, 2: 6.0}, leg_w=5.0, arm_w=6.5, head_zoom=1.4, kd=0.55,
            head_shift=(-3.0, 9.0), head_shift_n=(0.0, 10.0),
            tail_flat=0.2, tail_side=7.0, tail_drop=8.0,
            head=[("U", [("S", -10.0, -27.0, 0.0, 3.5, 3.6, 3.2),
                         ("S", -15.0, -26.0, 0.0, 4.0, 2.6, 2.2)], 0.15),
                  dict(s=("S", -16.5, -25.5, 0.0, 3.5, 2.4, 2.0), ramp="beak"),
                  dict(s=("S", -12.5, -33.0, 0.0, 3.5, 5.0, 1.3), ramp="crest")],
            eyes=(-11.0, -28.5, 2.8), eye_r=1.1,
        ),
    ),
}
