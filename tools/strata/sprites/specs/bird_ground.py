"""Species specs for the bird_ground body plan (plans/bird_ground.py). See specs/fish.py
for the common keys and the plan module for the bird geometry keys.

The starter line Asteriornis -> Gallinuloides -> Meleagris / Centrocercus shares one
build (plump body, short down-curved beak, short rounded wing with pale-barred
primaries, scalloped breast feathers, pale-edged nape) whose proportions grow
along the line."""

import math

from ..core.color import ramp


def arc(cx, cy, rx, ry, a0, a1, n=12):
    """Points on an ellipse arc (degrees, 0 = right, -90 = up)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


FAN = (20.0, -9.0, 13.0, 16.5)  # the turkey's display fan (frame 2): centre and radii

SPECS = {
    # Asteriornis maastrichtensis, Maastricht Fm (66.8 Ma): the 'Wonderchicken', a
    # ~0.4 kg crown galloanseran known from a 3D skull and leg bones. Skull: a
    # chicken-like face (short, slightly hooked beak) on a duck-like braincase;
    # long slender legs suggest a shoreline ground bird (Field et al. 2020).
    # Colour is unknown: a mottled grey-brown ground bird with a buff belly and a
    # pale eyebrow is the conservative reconstruction. Shiny: a rufous morph.
    "asteriornis": dict(
        ramps={
            "outline": ramp("2a2018"),
            "body": ramp("5a4636", "7e6650", "a48a6c", "c4ad8c"),
            "belly": ramp("b8a488", "d6c6a8", "eee4cc"),
            "wing": ramp("4a3a2e", "6e5642", "96785c"),
            "beak": ramp("6a625a", "aaa296"),
            "leg": ramp("8a7468", "b8a090"),
        },
        front=1.05, back=1.12, icon=0.5,
        shiny={"body": dict(deg=-8, sat=1.5, val=1.02), "wing": dict(deg=-8, sat=1.4, val=1.05)},
        body=[(3.0, 2.0, 12.5, 9.0, 10), (-5.5, 1.5, 8.5, 8.0, 0), (10.0, 2.5, 8.0, 6.5, 18)],
        regions=[dict(ramp="belly", below=(4.0, 0.12), on="body"),
                 dict(ramp="belly", ellipse=(-14.5, -9.5, 4.0, 3.0), on="head")],
        neck=dict(pts=[(-7.0, -3.0), (-10.5, -10.0)], radii=[5.6, 4.4]),
        head=[(-12.0, -13.5, 5.4, 4.9, 0)],
        beak=dict(upper=dict(pts=[(-16.0, -14.0), (-19.6, -13.3), (-21.4, -11.9)], radii=[1.9, 1.1, 0.45]),
                  lower=dict(pts=[(-16.0, -12.3), (-19.4, -11.9)], radii=[1.3, 0.45]),
                  hinge=(-16.0, -12.6)),
        eye=((-12.8, -14.6), 1.6, 0.9),
        wing=dict(coverts=[(5.0, -0.5, 9.5, 6.2, 12)],
                  primaries=dict(pts=[(9.0, 0.5), (16.0, 3.5), (19.0, 5.0)], radii=[4.6, 2.8, 1.2]),
                  root=(-2.0, -3.0)),
        tail=[[(13.0, -1.5), (21.0, -4.5), (22.5, -1.5), (15.0, 4.5)]],
        tail_root=(14.0, 0.0),
        legs=[
            dict(near=False, swing=-1, hip=(6.0, 6.0), ankle=(9.5, 15.0), foot=(6.5, 22.5),
                 toes=[(2.0, 23.6), (3.3, 24.0)], hallux=(9.0, 23.6), tibia_r=(3.2, 1.5), tarsus_r=(0.95, 0.85)),
            dict(near=True, swing=1, hip=(0.5, 6.5), ankle=(3.5, 15.0), foot=(0.0, 22.5),
                 toes=[(-5.0, 23.6), (-3.6, 24.2)], hallux=(2.6, 23.6), tibia_r=(3.4, 1.6), tarsus_r=(1.0, 0.9)),
        ],
        head_turn=8, gape=34, neck_pivot=(-7.0, -3.0),
        scallops=dict(ramps=("body", "wing"), rows=3, period=4, shift=2),
        marks=[
            dict(pts=[(-15.5, -17.0), (-12.0, -18.2), (-8.0, -16.8)], color=("belly", 2), on="head"),  # eyebrow
            dict(pts=[(-15.6, -14.9), (-12.0, -14.8), (-8.4, -14.0)], color=("body", 0), on="head"),     # eye stripe
            dict(pts=[(10.0, 1.5), (16.0, 4.2)], color=("belly", 1), on="wing"),   # pale primary bars
            dict(pts=[(8.0, 3.5), (13.0, 6.0)], color=("belly", 0), on="wing"),
            dict(pts=[(-1.0, -4.5), (6.0, -5.5), (12.0, -3.0)], shade=-1, on="wing"),  # covert row
            dict(pts=[(-18.6, -13.7)], color="outline", on="head"),  # nostril
        ],
    ),
    # Gallinuloides wyomingensis, Green River Fm (~52 Ma): the oldest well-known
    # stem galliform, from complete skeletons in lake shales. Partridge-sized
    # (mass estimated ~0.3 kg); short strong legs, a short galliform beak, rounded
    # wings and a longer tail than Asteriornis. Colour unknown: a rufous forest
    # partridge with barred flanks (forest ground birds are often barred) keeps the
    # starter's eyebrow and wing bars. Shiny: a grey (less phaeomelanin) morph.
    "gallinuloid": dict(
        ramps={
            "outline": ramp("2a1a12"),
            "body": ramp("5e3a26", "86563a", "ac7652", "cc9a70"),
            "belly": ramp("b4967a", "d6ba98", "eedcbc"),
            "wing": ramp("482e20", "6e4832", "98704e"),
            "beak": ramp("5e5650", "9c948a"),
            "leg": ramp("7a6458", "aa9080"),
        },
        front=1.0, back=1.08, icon=0.48,
        shiny={"body": dict(deg=8, sat=0.35, val=1.0), "wing": dict(deg=8, sat=0.4, val=1.0),
               "belly": dict(deg=0, sat=0.6, val=1.0)},
        body=[(3.0, 3.0, 14.0, 10.0, 8), (-6.0, 2.0, 9.5, 9.0, 0), (11.0, 3.0, 9.0, 7.0, 15)],
        regions=[dict(ramp="belly", below=(6.0, 0.12), on="body"),
                 dict(ramp="belly", ellipse=(-14.8, -8.2, 3.8, 2.8), on="head")],
        neck=dict(pts=[(-8.0, -3.0), (-11.0, -9.0)], radii=[6.0, 4.6]),
        head=[(-12.5, -12.2, 5.0, 4.6, 0)],
        beak=dict(upper=dict(pts=[(-16.3, -12.5), (-19.6, -11.9), (-21.2, -10.4)], radii=[1.8, 1.05, 0.45]),
                  lower=dict(pts=[(-16.3, -10.9), (-19.3, -10.5)], radii=[1.25, 0.45]),
                  hinge=(-16.3, -11.2)),
        eye=((-13.2, -13.2), 1.6, 0.9),
        wing=dict(coverts=[(5.5, 0.0, 10.5, 6.8, 12)],
                  primaries=dict(pts=[(10.0, 1.0), (17.0, 4.5), (20.5, 6.0)], radii=[5.0, 3.0, 1.3]),
                  root=(-2.0, -3.0)),
        tail=[[(13.0, -2.0), (24.0, -7.5), (26.5, -4.5), (16.0, 4.5)]],
        tail_root=(14.0, 0.0),
        legs=[
            dict(near=False, swing=-1, hip=(6.5, 8.0), ankle=(9.5, 15.5), foot=(7.0, 21.5),
                 toes=[(2.5, 22.6), (3.8, 23.0)], hallux=(9.5, 22.6), tibia_r=(3.6, 1.7), tarsus_r=(1.1, 1.0)),
            dict(near=True, swing=1, hip=(0.5, 8.5), ankle=(3.5, 16.0), foot=(0.0, 21.5),
                 toes=[(-5.0, 22.6), (-3.6, 23.2)], hallux=(2.6, 22.6), tibia_r=(3.8, 1.8), tarsus_r=(1.15, 1.0)),
        ],
        head_turn=-24, neck_pivot=(-8.0, -3.0),
        scallops=dict(ramps=("body", "wing"), rows=3, period=4, shift=2),
        marks=[
            dict(pts=[(-15.8, -15.6), (-12.5, -16.8), (-8.5, -15.2)], color=("belly", 2), on="head"),  # eyebrow
            dict(pts=[(-16.0, -13.4), (-12.5, -13.4), (-8.8, -12.6)], color=("body", 0), on="head"),     # eye stripe
            dict(pts=[(11.0, 2.5), (17.0, 5.2)], color=("belly", 1), on="wing"),   # pale primary bars
            dict(pts=[(9.0, 4.5), (14.0, 7.0)], color=("belly", 0), on="wing"),
            dict(pts=[(-1.0, -4.0), (6.0, -5.0), (12.0, -2.5)], shade=-1, on="wing"),  # covert row
            dict(pts=[(-6.0, 6.0), (-5.0, 9.0)], color=("body", 1)),   # flank bars
            dict(pts=[(-3.0, 7.0), (-2.0, 10.0)], color=("body", 1)),
            dict(pts=[(0.0, 8.0), (1.0, 11.0)], color=("body", 1)),
            dict(pts=[(-18.3, -12.4)], color="outline", on="head"),  # nostril
        ],
    ),
    # Meleagris gallopavo, the wild turkey (Natural Trap Cave, WY, ~20 ka). Real
    # colours of the western (Merriam's) turkey: bronze iridescent body feathers
    # with dark tips, black-and-white barred primaries, a tail with a dark band and
    # pale buff-white tips, bare blue-and-red head with snood and wattle, a black
    # breast beard, pinkish legs with a spur. Frame 2: the strut (fan raised, wing
    # tips dropped, head drawn back). Shiny: the smoke-grey morph seen in wild flocks.
    "meleagris": dict(
        ramps={
            "outline": ramp("1e1610"),
            "body": ramp("3a2a1e", "5e4430", "866440", "ae8c5a"),
            "wing": ramp("2c241e", "4e4238", "766654"),
            "white": ramp("e0d8c6"),
            "skin": ramp("8a2a28", "c4504a"),
            "face": ramp("94b0d8"),
            "leg": ramp("94625e", "c8948a"),
        },
        beak_ramp="leg",
        front=0.82, back=0.88, icon=0.4,
        shiny={"body": dict(deg=0, sat=0.25, val=1.45), "wing": dict(deg=0, sat=0.4, val=1.5)},
        body=[(5.0, 0.0, 16.0, 11.0, 6), (-8.0, -1.0, 10.5, 10.5, 0), (14.0, 1.0, 9.0, 8.0, 15)],
        head_ramp="skin",
        regions=[dict(ramp="body", below=(-13.0, 0.0), on="head"),
                 dict(ramp="face", ellipse=(-15.2, -24.5, 3.2, 2.4), on="head")],
        neck=dict(pts=[(-9.0, -5.0), (-13.0, -14.0), (-14.5, -21.0)], radii=[6.5, 3.2, 2.7], bend=0.5),
        head=[(-15.3, -23.6, 3.6, 3.3, 0)],
        beak=dict(upper=dict(pts=[(-18.0, -23.8), (-20.3, -23.0), (-21.4, -21.9)], radii=[1.4, 0.9, 0.4]),
                  lower=dict(pts=[(-18.0, -22.5), (-20.0, -22.1)], radii=[0.9, 0.4]),
                  hinge=(-18.0, -22.7)),
        eye=((-15.8, -24.6), 1.2, 0.8), eye_hi="white",
        wing=dict(coverts=[(5.0, -1.0, 12.0, 7.5, 10)],
                  primaries=dict(pts=[(11.0, 0.0), (20.0, 4.0), (24.5, 6.0)], radii=[5.6, 3.4, 1.5]),
                  root=(-3.0, -4.0)),
        tail=[dict(poly=[(15.0, -3.0), (28.0, 1.0), (28.5, 5.5), (16.0, 6.0)], phase=0),
],
        tail_root=(15.0, 0.0),
        legs=[
            dict(near=False, swing=-1, hip=(8.0, 7.0), ankle=(12.0, 18.0), foot=(9.0, 28.0),
                 toes=[(3.0, 29.2), (4.5, 29.8)], hallux=(12.0, 29.2), tibia_r=(5.0, 2.2), tarsus_r=(1.5, 1.3),
                 tibia_ramp="body"),
            dict(near=True, swing=1, hip=(0.5, 8.0), ankle=(4.5, 18.0), foot=(1.0, 28.0),
                 toes=[(-5.5, 29.2), (-4.0, 29.8)], hallux=(4.0, 29.2), tibia_r=(5.2, 2.3), tarsus_r=(1.6, 1.4),
                 tibia_ramp="body"),
        ],
        head_turn=12, wing_lift=-9, neck_pivot=(-9.0, -5.0),
        ow=dict(end_zoom=1.0), ow_end=dict(head_dy=5.0, body_w=1.25, head_w=1.25),
        extra=[
            dict(shape="ellipse", args=FAN, ramp="wing", z=-1.5, flat=0.35, phase=1),  # display fan
            dict(shape="tube", args=([(-17.6, -25.6), (-19.4, -25.2), (-20.7, -23.0), (-21.0, -20.0)],
                                     [0.9, 0.8, 0.7, 0.6]), ramp="skin", z=3.6, on="head"),   # snood
            dict(shape="ellipse", args=(-15.6, -19.8, 2.0, 3.0, 10), ramp="skin", z=3.1, on="head"),  # wattle
        ],
        scallops=dict(ramps=("body",), rows=2, period=3, shift=1, delta=-2),
        marks=[
            dict(pts=[(-15.0, -1.0), (-15.8, 3.0), (-16.6, 6.5)], color="outline"),  # beard
            dict(pts=[(-14.4, -0.5), (-15.0, 4.0)], color="outline"),
            dict(pts=[(13.0, 0.5), (14.0, 3.5)], color="white", on="wing"),   # barred primaries
            dict(pts=[(16.0, 1.5), (17.0, 4.5)], color="white", on="wing"),
            dict(pts=[(19.0, 3.0), (19.8, 5.5)], color="white", on="wing"),
            dict(pts=[(22.0, 4.5), (22.6, 6.3)], color="white", on="wing"),
            dict(pts=[(-2.0, -5.5), (6.0, -7.0), (13.0, -4.5)], color="white", on="wing"),  # covert edge
            dict(pts=[(27.0, 1.5), (27.4, 5.0)], color="white", phase=0),   # tail tips
            dict(pts=[(25.0, 1.0), (25.4, 5.5)], color="outline", phase=0),
            dict(pts=arc(FAN[0], FAN[1], FAN[2] - 0.6, FAN[3] - 0.6, -200, 20, 16), color="white", phase=1),
            dict(pts=arc(FAN[0], FAN[1], FAN[2] - 1.3, FAN[3] - 1.3, -200, 20, 16), color="white", phase=1),    # fan: pale tips
            *[dict(pts=[(FAN[0] - 2.0, FAN[1] + 7.0), q], shade=-1, phase=1)
              for q in arc(FAN[0], FAN[1], FAN[2] - 2.5, FAN[3] - 2.5, -170, -10, 6)],
            dict(pts=arc(FAN[0], FAN[1], FAN[2] - 2.4, FAN[3] - 2.4, -200, 20, 16), color=("wing", 0), phase=1),
            dict(pts=[(-19.6, -23.4)], color="outline", on="head"),  # nostril
            dict(pts=[(4.6, 22.5)], color="outline"),  # spur
        ],
    ),
    # Centrocercus urophasianus, the greater sage-grouse (living; MT). Real colours of
    # the male: mottled grey-brown upperparts with pale spots, black belly patch,
    # black throat, white breast ruff, yellow eye comb, long pointed tail feathers,
    # feathered legs. Frame 2 is the lek strut: spiky tail fan, puffed white ruff
    # with the two olive-yellow air sacs, head drawn back. Shiny: a pale (leucistic-
    # tending) morph, rare but recorded in sage-grouse.
    "centrocercus": dict(
        ramps={
            "outline": ramp("201a16"),
            "body": ramp("4a4038", "6e6254", "948672", "b8aa94"),
            "wing": ramp("564a3e", "7a6e5e", "a29680"),
            "white": ramp("c4c0b8", "f0eee6"),
            "black": ramp("2e2a28", "4a4440"),
            "sac": ramp("a89a48", "d6c870"),
            "beak": ramp("3a3430"),
        },
        front=0.95, back=1.0, icon=0.46,
        shiny={"body": dict(deg=0, sat=0.4, val=1.3), "wing": dict(deg=0, sat=0.4, val=1.3),
               "black": dict(deg=0, sat=0.6, val=1.9)},
        body=[(4.0, 1.0, 15.0, 10.5, 4), (-7.0, 0.0, 10.0, 10.0, 0), (12.0, 2.0, 8.5, 7.0, 12)],
        regions=[dict(ramp="white", ellipse=(-10.5, 0.5, 6.5, 8.0), on="body"),
                 dict(ramp="black", ellipse=(3.0, 11.0, 9.0, 4.5), on="body"),
                 dict(ramp="black", ellipse=(-14.0, -9.0, 3.6, 3.2), on="head"),
                 dict(ramp="white", ellipse=(-10.0, -5.0, 5.0, 2.4), on="head")],
        neck=dict(pts=[(-8.0, -4.0), (-11.0, -10.0)], radii=[6.0, 4.5]),
        head=[(-12.5, -13.0, 4.6, 4.2, 0)],
        beak=dict(upper=dict(pts=[(-16.4, -13.2), (-18.8, -12.6), (-19.8, -11.4)], radii=[1.5, 0.9, 0.4]),
                  lower=dict(pts=[(-16.4, -11.8), (-18.6, -11.5)], radii=[1.0, 0.4]),
                  hinge=(-16.4, -12.0)),
        eye=((-13.2, -13.6), 1.4, 0.8), eye_hi=("white", 1),
        wing=dict(coverts=[(5.0, -0.5, 11.0, 6.8, 10)],
                  primaries=dict(pts=[(10.0, 1.0), (18.0, 4.0), (21.5, 5.5)], radii=[5.0, 3.0, 1.3]),
                  root=(-3.0, -3.0)),
        tail=[dict(poly=[(13.0, -2.0), (29.0, -0.5), (26.5, 1.0), (30.0, 2.4), (26.5, 3.4), (28.5, 5.0),
                         (14.0, 4.5)], phase=0)],
        tail_root=(14.0, 0.0),
        legs=[
            dict(near=False, swing=-1, hip=(7.5, 8.0), ankle=(10.5, 15.0), foot=(8.0, 21.0),
                 toes=[(3.5, 22.2), (4.8, 22.6)], hallux=(10.0, 22.0), tibia_r=(3.8, 2.0), tarsus_r=(1.6, 1.3),
                 tibia_ramp="body"),
            dict(near=True, swing=1, hip=(1.0, 8.5), ankle=(4.0, 15.0), foot=(1.0, 21.0),
                 toes=[(-4.0, 22.2), (-2.6, 22.6)], hallux=(3.6, 22.0), tibia_r=(4.0, 2.1), tarsus_r=(1.7, 1.4),
                 tibia_ramp="body"),
        ],
        tarsus_scutes=False, claws=True,
        head_turn=14, wing_lift=-8, neck_pivot=(-8.0, -4.0),
        extra=[
            *[dict(shape="poly", args=[(16.0 + 1.3 * math.cos(math.radians(a + 90)), -2.0 + 1.3 * math.sin(math.radians(a + 90))),
                                       (16.0 + 17.0 * math.cos(math.radians(a)), -2.0 + 17.0 * math.sin(math.radians(a))),
                                       (16.0 - 1.3 * math.cos(math.radians(a + 90)), -2.0 - 1.3 * math.sin(math.radians(a + 90)))],
                   ramp="wing", z=-1.5, normal=(-0.2, -0.3, 0.93), phase=1)
              for a in (-165, -145, -125, -105, -85, -65, -45, -25, -5)],                 # spiky display fan
            dict(shape="ellipse", args=(-10.5, 1.0, 9.0, 10.5, 0), ramp="white", z=0.5, phase=1),   # puffed ruff
            dict(shape="ellipse", args=(-14.5, -1.5, 2.6, 3.0, 0), ramp="sac", z=3.3, phase=1),      # air sacs
            dict(shape="ellipse", args=(-13.0, 5.0, 2.6, 3.0, 0), ramp="sac", z=3.3, phase=1),
        ],
        scallops=dict(ramps=("body", "wing"), rows=2, period=3, shift=1),
        marks=[
            dict(pts=[(-15.4, -16.2), (-12.6, -16.6), (-10.6, -15.6)], color=("sac", 1), on="head"),  # eye comb
            dict(pts=[(1.0, -4.0), (5.0, -4.8), (9.0, -3.6), (13.0, -1.5)], r=0.45, color=("white", 0), on="wing"),
            dict(pts=[(3.0, -1.0), (7.0, -1.6), (11.0, 0.5)], r=0.45, color=("white", 0), on="wing"),
            dict(pts=[(-18.0, -12.8)], color="outline", on="head"),  # nostril
        ],
        ow_end=dict(belly="white"),
        ow_extra=[dict(shape="ellipse", args=(0.0, 8.5, 5.0, 2.6), ramp="black", z=0.2)],
    ),
    # Gastornis, Willwood Fm (~55 Ma): a flightless galloanseran about 2 m tall,
    # ~160 kg. A huge, very deep beak without a hook on a big head, short thick neck,
    # tiny vestigial wings, massive legs with three stout toes (hallux reduced).
    # Footprints and beak mechanics point to a plant eater (Angst et al. 2014;
    # Tutken et al. 2024). Integument unknown: shaggy hair-like feathers (as in
    # ratites) in dark grey-brown with a paler head is a reconstruction; the pale
    # horn beak and grey scaly legs follow living ground birds. Shiny: a warmer,
    # rufous-brown population.
    "gastornis": dict(
        ramps={
            "outline": ramp("1e1a1a"),
            "body": ramp("3c3634", "5a5250", "7c7370", "9e9690"),
            "belly": ramp("847a70", "a89e92", "c8c0b2"),
            "beak": ramp("8a7e68", "b8ac90", "dcd2b8"),
            "leg": ramp("4e4a48", "76706a", "9c968e"),
            "white": ramp("ece8dc"),
        },
        front=0.82, back=0.86, icon=0.4,
        shiny={"body": dict(deg=18, sat=1.9, val=1.05), "belly": dict(deg=10, sat=1.4, val=1.0)},
        body=[(6.0, -1.0, 15.0, 12.0, 16), (-2.0, -3.0, 10.0, 10.5, 0), (15.0, 2.0, 9.0, 8.5, 12)],
        regions=[dict(ramp="belly", below=(7.0, 0.18), on="body"),
                 dict(ramp="belly", ellipse=(-11.0, -13.0, 5.0, 4.0), on="head")],
        neck=dict(pts=[(-5.0, -9.0), (-9.5, -17.0)], radii=[8.0, 6.2]),
        head=[(-11.0, -21.5, 7.2, 6.4, 0)],
        beak=dict(upper=dict(pts=[(-15.5, -22.0), (-20.0, -21.6), (-24.0, -19.0), (-25.8, -16.4)],
                             radii=[4.8, 3.9, 2.3, 0.7]),
                  lower=dict(pts=[(-15.5, -17.0), (-21.0, -16.4), (-24.2, -16.0)], radii=[3.0, 2.0, 0.8]),
                  hinge=(-15.5, -18.0)),
        eye=((-11.5, -23.2), 1.5, 0.9), iris=("beak", 2), eye_hi="white",
        wing=dict(coverts=[(5.0, -4.0, 6.5, 4.0, 25)], root=(1.0, -6.0)),
        tail=[[(19.0, -3.0), (27.0, -5.0), (27.5, -1.0), (22.0, 5.0)]],
        tail_root=(19.0, 0.0), tail_ramp="body",
        legs=[
            dict(near=False, swing=-1, hip=(10.0, 7.0), ankle=(13.0, 18.0), foot=(10.0, 29.0),
                 toes=[(3.5, 30.2), (5.0, 30.8)], tibia_r=(6.5, 3.2), tarsus_r=(2.4, 2.1), toe_r=1.2,
                 tibia_ramp="body"),
            dict(near=True, swing=1, hip=(2.0, 7.5), ankle=(5.0, 18.0), foot=(2.0, 29.0),
                 toes=[(-5.0, 30.2), (-3.2, 30.8)], tibia_r=(6.8, 3.4), tarsus_r=(2.5, 2.2), toe_r=1.25,
                 tibia_ramp="body"),
        ],
        head_turn=6, gape=14, neck_pivot=(-5.0, -9.0),
        scallops=dict(ramps=("body",), rows=3, period=3, shift=1),
        marks=[
            dict(pts=[(-6.0, 8.0), (-5.5, 10.5)], shade=-1), dict(pts=[(-2.0, 10.0), (-1.5, 12.5)], shade=-1),
            dict(pts=[(2.0, 11.5), (2.5, 13.5)], shade=-1), dict(pts=[(12.0, 11.0), (12.5, 13.0)], shade=-1),
            dict(pts=[(-21.0, -21.5), (-17.5, -22.5)], shade=1, on="head"),   # culmen highlight
            dict(pts=[(-17.0, -21.0)], color=("beak", 0), on="head"),          # nostril
        ],
        ow=dict(end_zoom=1.0), ow_end=dict(head_dy=8.0, body_w=1.15, head_w=1.45, beak_len=6.0, beak_w=3.6, wings=False),
        body_k=0.3,
    ),
}
