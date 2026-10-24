"""Species specs for the ornithischian body plan (plans/ornithischian.py). See
specs/fish.py for the common keys and plans/theropod.py (the dinosaur kit) for
the shape data, pose groups, limbs, extras and end-on views."""

from ..core.color import ramp

SPECS = {
    # Triceratops horridus, Hell Creek Fm (66 Ma): 8.5 m, ~9 t, the commonest
    # big dinosaur of Hell Creek. Huge skull: solid frill rimmed with
    # epoccipital bumps, two long brow horns, a short nose horn, a parrot-like
    # beak; massive barrel body on columnar legs, short drooping tail. Skin
    # impressions show large polygonal scales (Lanzendorf specimen). Colour is a
    # reconstruction: dark olive-brown above, paler below; the warmer frill
    # centre is a speculative display patch; horns and beak pale keratin.
    # Frame 2: head lowered, horns to the front. Variant: a darker, greyer form.
    "triceratops": dict(
        ramps={
            "outline": ramp("1f1a14"),
            "skin": ramp("39332a", "585040", "7a7058", "9e9474"),
            "belly": ramp("8c846a", "b0a688", "d0c8aa"),
            "frill": ramp("6e5038", "9c7652"),
            "horn": ramp("8a7c62", "dcd0b2"),
            "eye": ramp("c89a40"),
            "white": ramp("f2eee0"),
        },
        claw_color=("horn", 0),
        front=0.78, back=0.78, icon=0.38,
        shiny={"skin": dict(deg=-20, sat=0.45, val=0.85), "frill": dict(deg=-15, sat=0.6, val=0.9)},
        body=[
            ("E", 2.0, -3.0, 17.0, 12.0, 0),
            ("E", 12.0, -5.0, 10.0, 10.5, 0),
            ("E", -10.0, -1.0, 10.0, 11.0, 0),
            ("T", [(-12.0, -3.0), (-18.0, -5.0)], [9.0, 8.0]),
            ("T", [(18.0, -6.0), (26.0, -3.0), (32.0, 2.0), (35.0, 7.0)], [7.5, 5.0, 3.0, 1.5]),
        ],
        tail_shapes=(4,), tail_base=(18.0, -6.0), tail_reach=18.0,
        belly=[(-30, 4), (-12, 5), (2, 7), (14, 5), (22, 0), (36, 3)],
        neck=(-17.0, -5.0),
        head=("L", -40.0, -14.0, [(0, 1.5), (0.18, 3.2), (0.45, 4.6), (0.75, 5.6), (1, 6.5)],
              [(0, 2.5), (0.25, 4.0), (0.6, 5.0), (1, 5.5)], 2.5, -5.0),
        head_belly=[(-50, -1.0), (-10, 0.0)],
        jaw_pivot=(-16.0, -2.0),
        eye=dict(c=(-24.5, -8.0), r=1.5, brow=[(-27.0, -10.0), (-23.0, -10.4)]),
        nostril=(-35.5, -6.0),
        lip=[(-37.5, -1.0), (-30.0, -1.2), (-24.0, -0.5)],
        extras=[
            # the frill: behind the skull, rising up and back, edged with epoccipitals
            dict(s=("R", ("E", -15.0, -15.0, 9.0, 14.0, 28), 0.22, 2.3), ramp="frill", z=3.5, group="head",
                 region=("skin", [(-40, 50), (0, 50)]), inner=("skin", 0)),
            # beak
            dict(s=("L", -40.5, -34.0, [(0, 1.6), (0.5, 3.2), (1, 4.0)], [(0, 2.6), (0.5, 3.8), (1, 4.5)], 2.5, -5.0),
                 ramp="horn", z=4.05, group="head", inner=("horn", 0)),
            # far brow horn (behind the head, in front of the frill)
            dict(s=("T", [(-21.0, -11.0), (-26.0, -21.0), (-29.0, -27.0)], [1.9, 1.2, 0.4]), ramp="horn", z=3.7,
                 group="head", light=-0.25),
            # near brow horn
            dict(s=("T", [(-24.0, -10.0), (-30.0, -20.0), (-34.5, -25.5)], [2.1, 1.3, 0.4]), ramp="horn", z=4.2,
                 group="head", inner=("horn", 0)),
            # nose horn
            dict(s=("T", [(-34.5, -9.5), (-35.5, -13.5)], [1.7, 0.5]), ramp="horn", z=4.1, group="head",
                 inner=("horn", 0)),
        ],
        knobs=[dict(group="head", ramp="frill", r=0.7, level=1,
                    pts=[(-9.0, -10.0), (-9.5, -16.0), (-12.0, -21.0)])],
        lines=[("head", [(-20.0, -6.0), (-16.0, -3.0)], -1, True)],
        legs=[
            dict(near=False, swing=1, z=-2, pts=[(16.0, 0.0), (18.0, 10.0), (17.0, 19.0)], radii=[6.0, 4.4, 3.8],
                 foot=("E", 16.5, 20.5, 4.2, 1.8)),
            dict(near=False, swing=-1, z=-2, pts=[(-5.0, 2.0), (-6.0, 11.0), (-5.0, 19.0)], radii=[5.0, 4.0, 3.6],
                 foot=("E", -5.5, 20.5, 4.0, 1.8)),
            dict(near=True, swing=-1, z=2, pts=[(12.0, 0.0), (14.0, 10.0), (12.0, 19.0)], radii=[6.5, 4.6, 4.0],
                 thigh=("E", 12.0, 1.0, 8.0, 10.0, 8), thigh_flat=0.35,
                 foot=("E", 11.5, 20.5, 4.6, 1.8), claws=[(8.0, 21.6), (10.0, 21.8)]),
            dict(near=True, swing=1, z=2.5, pts=[(-9.0, 3.0), (-11.0, 12.0), (-10.0, 19.0)], radii=[5.4, 4.2, 3.8],
                 foot=("E", -10.5, 20.5, 4.4, 1.8), claws=[(-14.0, 21.6), (-12.0, 21.8)]),
        ],
        action=dict(head=-9.0, jaw=0.0, tail=-4.0),
        walk=12.0, ground=22.0,
        texture=[dict(kind="scales", ramp="skin", rows=3, cols=4, shift=2, levels=(1, 2))],
        end=dict(
            body_w={0: 12.0, 1: 10.0, 2: 10.0}, leg_w=9.0, kd=0.5, head_zoom=1.15,
            tail_flat=0.6, tail_side=4.0, tail_drop=4.0,
            head=[("U", [("S", -22.0, -6.0, 0.0, 6.0, 5.5, 6.5), ("S", -32.0, -4.5, 0.0, 6.0, 4.0, 4.0)], 0.15),
                  dict(s=("S", -38.0, -3.5, 0.0, 2.5, 3.5, 2.6), ramp="horn")],
            eyes=(-24.5, -8.0, 5.8), eye_r=1.0,
            extras=[
                dict(s=("R", ("D", -14.0, -16.0, 0.0, 16.0, 13.0, 2.0), 0.35, 1.9), ramp="frill", group="head",
                     z=-1.0, inner=("skin", 0)),
                dict(s=("C", [(-24.0, -10.0, 4.0), (-30.0, -20.0, 5.0), (-34.5, -25.5, 5.0)], [2.0, 1.2, 0.5]),
                     ramp="horn", group="head", mirror=True, z=1.0, inner=("horn", 0)),
                dict(s=("C", [(-34.5, -9.5, 0.0), (-35.5, -13.5, 0.0)], [1.6, 0.5]), ramp="horn", group="head",
                     z=1.0, inner=("horn", 0), view="south"),
            ],
        ),
    ),

    # Edmontosaurus annectens, Hell Creek Fm (66 Ma): ~12 m, ~4 t hadrosaurid.
    # Long low skull ending in a broad toothless duck bill (keratin rhamphotheca
    # preserved), big nasal vestibule, batteries of grinding teeth; deep tail,
    # big hind legs, slender forelimbs ending in hoof-like hands (it walked on
    # all fours or two). Mummies preserve pebbly scales. The fleshy head comb is
    # known from an E. regalis specimen (Bell et al. 2014); giving it to
    # E. annectens is speculative. Colour is a reconstruction: dull olive-brown
    # with a paler belly and faint dark saddles. Frame 2: head up, calling.
    # Variant: a sandy, paler population.
    "edmontosaur": dict(
        ramps={
            "outline": ramp("1c1a12"),
            "skin": ramp("38382a", "54553c", "727250", "96946c"),
            "belly": ramp("8e8a6c", "b4ae8c", "d6d0b0"),
            "bill": ramp("443a30", "786654"),
            "crest": ramp("7a4c3c", "a46a52"),
            "mouth": ramp("7a3a34"),
            "eye": ramp("c89a40"),
            "white": ramp("f2eee0"),
        },
        claw_color=("bill", 0),
        front=0.76, back=0.76, icon=0.37,
        shiny={"skin": dict(deg=-25, sat=0.85, val=1.2), "belly": dict(deg=-10, sat=0.9, val=1.05)},
        body=[
            ("E", 2.0, -6.0, 16.0, 10.0, -6),
            ("E", 12.0, -8.0, 10.0, 10.0, 0),
            ("E", -10.0, -2.0, 8.0, 8.0, 10),
            ("T", [(-12.0, -4.0), (-17.0, -10.0), (-20.0, -16.0)], [6.5, 4.6, 4.2]),
            ("T", [(18.0, -10.0), (26.0, -10.0), (33.0, -7.5), (38.5, -4.0)], [8.0, 5.5, 3.4, 1.4]),
        ],
        tail_shapes=(4,), tail_base=(18.0, -10.0), tail_reach=24.0,
        belly=[(-30, -6), (-14, 2), (0, 3), (12, 1), (22, -3), (34, -3), (44, -1)],
        neck=(-20.0, -15.0),
        head=("L", -40.0, -17.0, [(0, 1.8), (0.25, 2.3), (0.55, 3.1), (0.8, 4.8), (1, 5.0)],
              [(0, 2.2), (0.3, 2.2), (0.7, 2.6), (1, 3.4)], 2.5, -17.5),
        head_belly=[(-50, -13.5), (-10, -13.5)],
        jaw_pivot=(-19.0, -14.5),
        jaw=("L", -37.0, -18.0, [(0, 0.7), (1, 1.2)], [(0, 1.0), (0.5, 1.7), (1, 2.8)], 0.8, -13.6),
        jaw_belly=[(-50, -13.2), (-10, -13.2)],
        mouth=("P", [(-37.0, -15.0), (-19.0, -15.0), (-20.0, -12.0), (-36.0, -10.0)]),
        eye=dict(c=(-24.5, -19.5), r=1.5, brow=[(-26.5, -21.6), (-22.8, -22.0)]),
        nostril=None,
        lip=[(-38.5, -14.6), (-30.0, -14.4), (-22.0, -14.0)],
        extras=[
            # duck bill (keratin)
            dict(s=("L", -40.6, -32.0, [(0, 2.0), (0.5, 2.4), (1, 2.6)], [(0, 2.8), (0.5, 3.4), (1, 3.8)], 2.6, -17.0),
                 ramp="bill", z=4.05, group="head", inner=("bill", 0)),
            # fleshy comb over the skull roof (speculative, see above)
            dict(s=("U", [("E", -23.5, -22.6, 4.4, 2.0, -12), ("E", -19.5, -21.6, 2.6, 1.7, 10)]), ramp="crest",
                 z=3.95, group="head", inner=("crest", 0)),
        ],
        lines=[("head", [(-36.0, -19.0), (-30.0, -19.0), (-28.0, -17.4)], -1, True)],  # nasal vestibule
        legs=[
            dict(near=False, swing=1, z=-2, pts=[(16.0, -3.0), (13.0, 8.0), (18.0, 15.0), (17.0, 20.5)],
                 radii=[5.4, 3.6, 2.6, 2.3], foot=("T", [(17.0, 21.0), (12.0, 21.3)], [2.2, 1.7])),
            dict(near=False, swing=-1, z=-2, pts=[(-6.0, 1.0), (-7.0, 10.0), (-7.0, 19.5)], radii=[2.8, 2.0, 1.6],
                 foot=("E", -7.5, 20.6, 2.2, 1.4)),
            dict(near=True, swing=-1, z=2, pts=[(12.0, -3.0), (9.0, 8.0), (14.0, 15.0), (13.0, 20.5)],
                 radii=[6.0, 4.0, 2.9, 2.5], thigh=("E", 11.0, -1.0, 8.0, 10.0, 10), thigh_flat=0.35,
                 foot=("T", [(13.0, 21.0), (7.5, 21.3)], [2.4, 1.8]), claws=[(6.5, 21.8)]),
            dict(near=True, swing=1, z=2.5, pts=[(-9.0, 1.0), (-11.0, 10.0), (-11.0, 19.5)], radii=[3.0, 2.2, 1.8],
                 foot=("E", -11.5, 20.6, 2.4, 1.4)),
        ],
        action=dict(head=12.0, jaw=-10.0, tail=-3.0),
        walk=14.0, ground=22.0,
        texture=[
            dict(kind="scales", ramp="skin", rows=2, cols=3, shift=1, levels=(1, 2)),
            dict(kind="bands", ramp="skin", period=9.0, width=0.3, x0=-6.0, x1=40.0,
                 top=[(-20, -10), (0, -10), (20, -13), (40, -7)], levels=(1, 3)),
        ],
        end=dict(
            body_w={0: 10.0, 1: 9.0, 2: 7.5}, leg_w=7.5, kd=0.5, head_zoom=1.6, head_shift=(-4.0, 1.0), head_shift_n=(0.0, 9.0),
            tail_flat=0.5, tail_side=8.0, tail_drop=6.0,
            head=[("U", [("S", -22.0, -18.5, 0.0, 4.5, 4.2, 4.6), ("S", -30.0, -16.5, 0.0, 5.0, 2.8, 3.4)], 0.15),
                  dict(s=("S", -37.0, -16.0, 0.0, 3.0, 2.8, 4.8), ramp="bill"),
                  dict(s=("S", -22.5, -22.6, 0.0, 4.0, 1.8, 1.4), ramp="crest")],
            eyes=(-24.5, -19.5, 4.2), eye_r=1.1,
        ),
    ),

    # Ankylosaurus magniventris, Hell Creek Fm (66 Ma): ~7 m, ~5 t, the last
    # and largest ankylosaurid. Very wide, low body; the back is paved with
    # keeled osteoderms in transverse rows, with triangular plates along the
    # flanks; a short broad head with pyramidal horns at the back corners and
    # cheeks and a narrow beak; a stiff tail ending in a two-lobed bony club.
    # Colour is a reconstruction: dull brown skin, the armour a paler horn
    # brown (Borealopelta preserves reddish-brown countershading, so a darker
    # back fading to a paler side is plausible). Frame 2: the tail club swings
    # up. Variant: a reddish (erythristic) form, after Borealopelta.
    "ankylosaurus": dict(
        ramps={
            "outline": ramp("1e1812"),
            "skin": ramp("2e2620", "4a3e32", "66574a", "86765e"),
            "belly": ramp("9a8668", "c0ae8c"),
            "armor": ramp("4e4232", "786650", "a48e70", "c8b490"),
            "eye": ramp("c89a40"),
            "white": ramp("f2eee0"),
        },
        claw_color=("armor", 0),
        front=0.76, back=0.76, icon=0.37,
        shiny={"skin": dict(deg=-14, sat=1.35, val=1.0), "armor": dict(deg=-12, sat=1.3, val=0.95)},
        body=[
            ("E", 2.0, -2.0, 20.0, 10.0, 0),
            ("E", 12.0, -3.0, 10.0, 9.0, 0),
            ("E", -12.0, 0.0, 9.0, 8.0, 0),
            ("T", [(-15.0, -1.0), (-20.0, 0.0)], [6.5, 5.0]),
            ("T", [(22.0, -4.0), (30.0, -4.0), (38.0, -4.0), (42.0, -4.0)], [6.0, 3.6, 2.2, 1.8]),
        ],
        tail_shapes=(4,), tail_base=(22.0, -4.0), tail_reach=22.0,
        belly=[(-30, 4), (-10, 5), (10, 5), (30, 2), (50, 2)],
        neck=(-19.0, 0.0),
        head=("L", -31.0, -17.5, [(0, 2.2), (0.3, 4.2), (1, 5.4)], [(0, 2.4), (0.5, 3.2), (1, 3.8)], 1.0, -1.0),
        head_belly=[(-50, 1.5), (-10, 1.5)],
        jaw_pivot=(-19.0, 1.0),
        eye=dict(c=(-23.0, -2.0), r=1.3, brow=[(-25.5, -4.2), (-21.5, -4.6)]),
        nostril=(-30.0, -1.4),
        lip=[(-31.5, 1.6), (-26.0, 2.0)],
        extras=[
            # the armour: a domed carapace band over the back and flanks
            dict(s=("R", ("L", -21.0, 31.0, [(0, 4.0), (0.15, 8.5), (0.5, 11.0), (0.85, 8.5), (1, 5.0)],
                          [(0, 2.0), (0.5, 4.0), (1, 2.0)], 1.0, -3.0), 0.25, 1.8),
                 ramp="armor", z=0.5, inner=("armor", 0)),
            # triangular flank plates along its lower edge
            *[dict(s=("P", [(x - 2.4, 0.6 + abs(x - 4) * 0.035), (x + 2.4, 0.6 + abs(x - 4) * 0.035),
                            (x - 0.6, 4.2 + abs(x - 4) * 0.02)]),
                   ramp="armor", z=0.6, normal=(0, 0.2, 1), inner=("armor", 0))
              for x in (-14.0, -7.0, 0.0, 7.0, 14.0, 21.0)],
            # head horns: squamosal (back corner) and quadratojugal (cheek)
            dict(s=("P", [(-23.0, -5.5), (-16.0, -9.0), (-19.0, -3.5)]), ramp="armor", z=4.1, group="head",
                 normal=(0, -0.3, 1), inner=("armor", 0)),
            dict(s=("P", [(-23.5, 1.0), (-16.5, 5.5), (-21.0, 2.8)]), ramp="armor", z=4.1, group="head",
                 normal=(0, 0.2, 1), inner=("armor", 0)),
            # the tail club
            dict(s=("U", [("E", 44.0, -4.0, 5.0, 3.8, 0), ("E", 41.0, -4.0, 2.6, 2.8, 0)]), ramp="armor", z=0.4,
                 group="tail", inner=("armor", 0)),
            # tail osteoderm keels
            *[dict(s=("P", [(x - 1.8, -6.8 + (x - 22) * 0.05), (x + 1.8, -6.8 + (x - 22) * 0.05),
                            (x + 0.8, -8.6 + (x - 22) * 0.07)]),
                   ramp="armor", z=0.45, group="tail", normal=(0, -0.3, 1), inner=("armor", 0))
              for x in (25.0, 30.0, 35.0)],
        ],
        knobs=[dict(group="body", ramp="armor", r=1.0, level=3,
                    pts=[(x, y) for y, xs in ((-11.0, (-6, 0, 6, 12, 18)), (-7.0, (-12, -6, 0, 6, 12, 18, 24)),
                                              (-3.0, (-15, -9, -3, 3, 9, 15, 21, 27)))
                         for x in xs]),
               dict(group="tail", ramp="armor", r=0.7, level=3, pts=[(43.0, -5.5), (46.0, -4.5)])],
        legs=[
            dict(near=False, swing=1, z=-2, pts=[(17.0, 1.0), (18.0, 8.0), (17.0, 13.5)], radii=[5.0, 3.8, 3.4],
                 foot=("E", 16.5, 14.5, 3.8, 1.5)),
            dict(near=False, swing=-1, z=-2, pts=[(-8.0, 3.0), (-9.0, 9.0), (-8.0, 13.5)], radii=[4.4, 3.6, 3.2],
                 foot=("E", -8.5, 14.5, 3.6, 1.5)),
            dict(near=True, swing=-1, z=2, pts=[(13.0, 1.0), (14.0, 8.0), (13.0, 13.5)], radii=[5.5, 4.2, 3.6],
                 thigh=("E", 13.0, 2.0, 6.5, 7.0, 8), thigh_flat=0.35,
                 foot=("E", 12.5, 14.5, 4.0, 1.5), claws=[(9.3, 15.6), (11.3, 15.8)]),
            dict(near=True, swing=1, z=2.5, pts=[(-12.0, 3.0), (-13.0, 9.0), (-12.0, 13.5)], radii=[4.8, 3.8, 3.4],
                 foot=("E", -12.5, 14.5, 3.8, 1.5), claws=[(-15.7, 15.6), (-13.7, 15.8)]),
        ],
        action=dict(head=-3.0, jaw=0.0, tail=-14.0),
        walk=10.0, ground=16.0,
        texture=[dict(kind="scales", ramp="skin", rows=2, cols=3, shift=1, levels=(1, 2))],
        end=dict(
            body_w={0: 15.0, 1: 13.0, 2: 12.0}, leg_w=11.0, kd=0.55, head_zoom=1.35, head_shift=(-2.0, -1.0),
            tail_flat=1.0, tail_side=3.0, tail_drop=3.0,
            head=[("S", -25.0, -0.5, 0.0, 6.0, 4.0, 6.5),
                  dict(s=("S", -31.0, 0.5, 0.0, 2.0, 2.2, 3.0), ramp="armor")],
            eyes=(-23.5, -1.6, 5.2), eye_r=1.0,
            extras=[
                dict(s=("R", ("S", 4.0, -5.0, 0.0, 22.0, 9.5, 16.0), 0.25, 1.8), ramp="armor", z=0.3,
                     inner=("armor", 0)),
                dict(s=("C", [(-19.5, -3.0, 5.5), (-18.0, -6.5, 7.5)], [1.6, 0.5]), ramp="armor", group="head",
                     mirror=True, z=0.2, inner=("armor", 0)),
                dict(s=("C", [(-6.0, 2.0, 15.0), (-6.0, 3.5, 17.5)], [1.6, 0.4]), ramp="armor", mirror=True,
                     z=0.4, inner=("armor", 0)),
                dict(s=("C", [(8.0, 2.0, 15.0), (8.0, 3.5, 17.5)], [1.6, 0.4]), ramp="armor", mirror=True,
                     z=0.4, inner=("armor", 0)),
                dict(s=("S", 44.0, -4.0, 0.0, 4.6, 3.4, 5.0), ramp="armor", z=0.5, view="north",
                     inner=("armor", 0)),
            ],
        ),
    ),

    # Pachycephalosaurus wyomingensis, Hell Creek Fm (66 Ma): ~4.5 m, ~400 kg
    # biped. A dome of solid bone up to 25 cm thick, ringed at the back by
    # bony knobs, with blunt spikes on the snout; short muzzle with a small
    # beak, short arms, stiff tail, long hind legs. Colour is a reconstruction:
    # sandy brown with darker dorsal bands (open woodland); the dome is shown
    # in pale keratin (a display colour would be speculative). Frame 2: head
    # lowered to butt. Variant: a darker, greyer population.
    "pachycephalo": dict(
        ramps={
            "outline": ramp("1f1912"),
            "skin": ramp("3e3224", "604c36", "84694a", "a88c66"),
            "belly": ramp("a8946e", "cab690", "e6d8b4"),
            "dome": ramp("7c6a52", "ac9672", "d8c6a0"),
            "eye": ramp("d0a040"),
            "white": ramp("f4f0e2"),
        },
        claw_color=("dome", 0),
        front=0.98, back=1.0, icon=0.48, ow=dict(end_zoom=1.25),
        shiny={"skin": dict(deg=-10, sat=0.45, val=0.8), "belly": dict(deg=0, sat=0.6, val=0.9)},
        body=[
            ("E", 2.0, -4.0, 11.0, 8.0, -5),
            ("E", 8.0, -5.0, 7.0, 7.0, 0),
            ("E", -5.0, -2.0, 6.0, 6.5, 10),
            ("T", [(-6.0, -5.0), (-10.0, -11.0), (-12.0, -15.0)], [4.6, 3.6, 3.4]),
            ("T", [(11.0, -6.0), (20.0, -7.0), (28.0, -6.0), (34.0, -4.0)], [5.0, 3.4, 2.2, 1.2]),
        ],
        tail_shapes=(4,), tail_base=(11.0, -6.0), tail_reach=22.0,
        belly=[(-20, -10), (-10, -3), (0, 3), (10, 2), (20, -3), (36, -2)],
        neck=(-12.0, -14.0),
        head=("L", -24.0, -9.5, [(0, 1.0), (0.4, 2.4), (1, 3.0)], [(0, 1.5), (0.5, 2.2), (1, 3.2)], 1.5, -15.0),
        head_belly=[(-50, -13.0), (-5, -12.6)],
        eye=dict(c=(-17.5, -16.0), r=1.4, brow=[(-19.5, -18.0), (-16.0, -18.4)]),
        nostril=(-22.6, -14.6),
        lip=[(-23.5, -13.4), (-18.0, -13.0)],
        extras=[
            # the dome
            dict(s=("E", -14.0, -20.0, 6.6, 5.6, -12), ramp="dome", z=4.2, group="head", inner=("dome", 0)),
            # beak tip
            dict(s=("E", -23.2, -14.0, 1.5, 1.8, 0), ramp="dome", z=4.1, group="head", inner=("dome", 0)),
            # snout spikes
            dict(s=("T", [(-21.0, -16.5), (-22.0, -18.6)], [0.9, 0.3]), ramp="dome", z=4.05, group="head"),
            # squamosal spikes behind the dome
            dict(s=("T", [(-9.5, -18.0), (-6.5, -19.5)], [1.0, 0.3]), ramp="dome", z=4.15, group="head",
                 inner=("dome", 0)),
            dict(s=("T", [(-9.0, -15.5), (-6.0, -15.8)], [0.9, 0.3]), ramp="dome", z=4.15, group="head",
                 inner=("dome", 0)),
        ],
        knobs=[dict(group="head", ramp="dome", r=0.8, level=2,
                    pts=[(-10.0, -21.0), (-9.6, -18.4), (-11.0, -16.2), (-13.5, -15.2)])],
        arms=[
            dict(near=False, pts=[(-3.0, -1.0), (-5.0, 3.0), (-8.0, 4.0)], radii=[1.5, 1.2, 0.9], z=-1),
            dict(near=True, pts=[(-5.0, -1.0), (-7.0, 3.0), (-10.0, 4.0)], radii=[1.7, 1.3, 1.0], z=3,
                 claws=[(-10.8, 4.4)]),
        ],
        legs=[
            dict(near=False, swing=-1, z=-2, pts=[(8.0, -2.0), (5.0, 8.0), (11.0, 15.0), (9.5, 21.0)],
                 radii=[3.4, 2.4, 1.7, 1.4], foot=("T", [(10.0, 21.4), (4.5, 21.8)], [1.4, 1.1])),
            dict(near=True, swing=1, z=2, pts=[(5.0, -2.0), (2.0, 8.0), (8.0, 15.0), (6.0, 21.0)],
                 radii=[3.6, 2.6, 1.8, 1.5], thigh=("E", 4.5, 1.0, 5.5, 8.0, 15),
                 foot=("T", [(6.5, 21.4), (1.0, 21.8)], [1.5, 1.1]), claws=[(0.0, 22.2)]),
        ],
        action=dict(head=-16.0, jaw=0.0, tail=5.0),
        walk=18.0, ground=22.0,
        texture=[
            dict(kind="scales", ramp="skin", rows=3, cols=4, shift=2, levels=(1, 2)),
            dict(kind="bands", ramp="skin", period=6.0, width=0.3, x0=-4.0, x1=34.0,
                 top=[(-10, -6), (0, -7), (12, -8), (24, -8), (34, -5)], levels=(1, 3)),
        ],
        end=dict(
            body_w={0: 7.0, 1: 6.5, 2: 5.5}, leg_w=5.0, arm_w=4.0, kd=0.55, head_zoom=1.4,
            head_shift=(-3.0, 7.0), head_shift_n=(0.0, 7.0),
            tail_flat=0.3, tail_side=7.0, tail_drop=8.0,
            head=[("S", -17.0, -14.5, 0.0, 5.0, 3.2, 3.6),
                  dict(s=("S", -14.0, -20.0, 0.0, 6.0, 5.2, 5.0), ramp="dome")],
            eyes=(-17.5, -16.0, 3.4), eye_r=1.0,
        ),
    ),

    # Thescelosaurus neglectus, Hell Creek Fm (66 Ma): ~3.5 m, ~300 kg
    # thescelosaurid ornithopod. Small, low, long-snouted head with a horny beak
    # and cheek teeth, a bony palpebral over the eye, compact body, short arms,
    # long legs and a long stiffened tail. Patches of skin show small scales; a
    # light covering of filaments (as in Kulindadromeus) is possible but not
    # shown. Colour is a reconstruction for a forest-floor animal: olive-brown
    # with a pale flank stripe, pale belly. Frame 2: alert, head raised.
    # Variant: a rufous population.
    "thescelosaur": dict(
        ramps={
            "outline": ramp("1b1a12"),
            "skin": ramp("33321f", "4e4c30", "6d6a44", "8f8c5c"),
            "belly": ramp("a49e7a", "c8c29e", "e4e0c4"),
            "beak": ramp("5a4c38", "8c7858"),
            "eye": ramp("c89a40"),
            "white": ramp("f2f0e2"),
        },
        claw_color=("beak", 0),
        front=0.93, back=0.93, icon=0.44, ow=dict(end_zoom=1.45),
        shiny={"skin": dict(deg=-28, sat=1.25, val=1.05), "belly": dict(deg=-10, sat=1.1, val=1.0)},
        body=[
            ("E", 2.0, -3.0, 10.0, 6.5, -4),
            ("E", 8.0, -4.0, 6.5, 6.0, 0),
            ("E", -5.0, -1.5, 5.5, 5.5, 8),
            ("T", [(-6.0, -4.0), (-11.0, -9.0), (-14.0, -12.0)], [4.0, 3.0, 2.8]),
            ("T", [(11.0, -5.0), (20.0, -6.0), (30.0, -6.0), (38.0, -4.0)], [4.5, 3.0, 1.9, 1.0]),
        ],
        tail_shapes=(4,), tail_base=(11.0, -5.0), tail_reach=26.0,
        belly=[(-24, -9), (-10, -2), (0, 2), (10, 1), (20, -3), (40, -2)],
        neck=(-13.0, -11.0),
        head=("L", -27.0, -11.5, [(0, 0.8), (0.4, 1.8), (0.8, 3.0), (1, 3.0)], [(0, 1.2), (0.5, 1.6), (1, 2.6)],
              1.2, -13.0),
        head_belly=[(-50, -11.4), (-5, -11.0)],
        eye=dict(c=(-16.5, -14.3), r=1.5, brow=[(-18.6, -16.2), (-14.8, -16.6)]),
        nostril=(-25.0, -13.2),
        lip=[(-26.5, -11.8), (-20.0, -11.4), (-15.0, -11.0)],
        extras=[
            dict(s=("L", -27.4, -22.5, [(0, 0.9), (0.5, 1.6), (1, 2.0)], [(0, 1.2), (0.5, 1.4), (1, 1.6)], 1.2, -13.0),
                 ramp="beak", z=4.05, group="head", inner=("beak", 0)),
        ],
        lines=[  # a pale flank stripe and a dark one below it
            ("body", [(-4.0, -5.0), (6.0, -6.5), (16.0, -6.5), (26.0, -6.0)], ("belly", 1), True),
            ("body", [(-2.0, -2.5), (8.0, -3.0), (14.0, -3.5)], -1, True),
        ],
        arms=[
            dict(near=False, pts=[(-3.0, -1.0), (-5.0, 3.0), (-8.0, 4.0)], radii=[1.4, 1.1, 0.9], z=-1),
            dict(near=True, pts=[(-5.0, -1.0), (-7.0, 3.0), (-10.0, 4.0)], radii=[1.6, 1.2, 1.0], z=3,
                 claws=[(-10.8, 4.4)]),
        ],
        legs=[
            dict(near=False, swing=-1, z=-2, pts=[(8.0, -2.0), (5.0, 8.0), (11.0, 15.0), (9.5, 21.0)],
                 radii=[3.0, 2.0, 1.4, 1.2], foot=("T", [(10.0, 21.4), (4.5, 21.8)], [1.2, 1.0])),
            dict(near=True, swing=1, z=2, pts=[(5.0, -2.0), (2.0, 8.0), (8.0, 15.0), (6.0, 21.0)],
                 radii=[3.2, 2.2, 1.5, 1.3], thigh=("E", 4.5, 1.0, 5.0, 7.5, 15),
                 foot=("T", [(6.5, 21.4), (1.0, 21.8)], [1.3, 1.0]), claws=[(0.0, 22.2)]),
        ],
        action=dict(head=10.0, jaw=0.0, tail=-6.0),
        walk=20.0, ground=22.0,
        texture=[dict(kind="scales", ramp="skin", rows=2, cols=5, shift=3, levels=(1, 2))],
        end=dict(
            body_w={0: 6.0, 1: 5.5, 2: 4.8}, leg_w=4.5, arm_w=3.5, kd=0.55, head_zoom=1.5,
            head_shift=(-3.0, 6.0), head_shift_n=(0.0, 6.0),
            tail_flat=0.3, tail_side=9.0, tail_drop=8.0,
            head=[("U", [("S", -16.0, -13.5, 0.0, 3.5, 3.0, 3.4), ("S", -22.0, -12.5, 0.0, 5.0, 2.0, 2.2)], 0.15),
                  dict(s=("S", -26.0, -12.6, 0.0, 1.6, 1.8, 1.6), ramp="beak")],
            eyes=(-16.5, -14.3, 3.0), eye_r=1.0,
        ),
    ),
}
