"""Species specs for the crane_raptor body plan (plans/crane_raptor.py, which uses
the shared bird template in plans/bird_ground.py). See specs/fish.py for the common
keys and plans/bird_ground.py for the bird geometry keys."""

import math

from ..core.color import ramp


def spray(cx, cy, n, a0, a1, length, r=0.55, ramp_name="crest", z=3.6, on="head", jitter=(1.0, 0.8)):
    """A bristly crest: n thin tapering tubes fanning out from (cx, cy)."""
    out = []
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * k / max(1, n - 1))
        ln = length * (jitter[0] if k % 2 == 0 else jitter[1])
        tip = (cx + ln * math.cos(a), cy + ln * math.sin(a))
        mid = (cx + ln * 0.5 * math.cos(a), cy + ln * 0.5 * math.sin(a))
        out.append(dict(shape="tube", args=([(cx, cy), mid, tip], [r * 1.3, r, r * 0.7]), ramp=ramp_name,
                        z=z, on=on, flat=0.6))
    return out


SPECS = {
    # Presbyornis, Green River Fm (~52 Ma): a long-legged anseriform, known from
    # thousands of bones in lakeshore colonies. Duck-like head and broad flat bill
    # (a filter feeder) on a long neck, with long wader legs (Olson & Feduccia
    # 1980). Colour is speculative: pale grey and white like many colonial shore
    # birds, grey-brown wings, a dark bill and pinkish legs; the starter's pale
    # eyebrow survives as a faint pale stripe. Shiny: a darker, brown-grey morph.
    "presbyornis": dict(
        ramps={
            "outline": ramp("22242a"),
            "body": ramp("7c8088", "a2a6ac", "c8cace", "eceae6"),
            "wing": ramp("4e4a46", "706a62", "988e82"),
            "beak": ramp("2e2e32", "565458"),
            "leg": ramp("9a6e6a", "c8968e"),
            "dark": ramp("3e3c3c"),
        },
        front=0.85, back=0.9, icon=0.42,
        shiny={"body": dict(deg=30, sat=2.5, val=0.82), "wing": dict(deg=0, sat=1.2, val=0.85)},
        body=[(6.0, -2.0, 13.0, 8.0, 8), (-3.0, -3.0, 8.0, 7.5, 0), (13.0, -1.0, 8.0, 6.0, 15)],
        neck=dict(pts=[(-4.0, -7.0), (-10.0, -14.0), (-8.0, -21.0), (-10.0, -27.0)], radii=[5.0, 2.6, 2.3, 2.6],
                  bend=0.4),
        head=[(-12.0, -29.2, 4.6, 3.9, 0), (-12.8, -30.6, 3.4, 2.8, 0)],
        beak=dict(upper=dict(pts=[(-15.5, -29.3), (-19.5, -28.6), (-23.2, -27.7)], radii=[1.7, 1.45, 1.5]),
                  lower=dict(pts=[(-15.5, -27.9), (-22.5, -27.0)], radii=[1.1, 1.0]),
                  hinge=(-15.5, -28.1)),
        eye=((-12.8, -29.9), 1.3, 0.8),
        wing=dict(coverts=[(6.0, -3.5, 11.0, 5.5, 8)],
                  primaries=dict(pts=[(10.0, -2.0), (20.0, 0.5), (25.5, 1.5)], radii=[4.0, 2.6, 1.1]),
                  root=(-2.0, -5.0)),
        tail=[[(17.0, -4.0), (24.0, -4.0), (23.5, -0.5), (17.0, 1.5)]],
        tail_root=(17.0, -2.0),
        legs=[
            dict(near=False, swing=-1, hip=(8.0, 2.0), ankle=(11.0, 16.0), foot=(8.0, 29.0),
                 toes=[(2.5, 30.0), (4.0, 30.5)], hallux=(10.5, 29.8), tibia_r=(2.6, 1.1), tarsus_r=(0.95, 0.85),
                 tibia_ramp="leg"),
            dict(near=True, swing=1, hip=(3.0, 2.5), ankle=(6.0, 16.0), foot=(2.0, 29.0),
                 toes=[(-4.0, 30.0), (-2.5, 30.6)], hallux=(4.5, 29.8), tibia_r=(2.8, 1.15), tarsus_r=(1.05, 0.95),
                 tibia_ramp="leg"),
        ],
        head_turn=10, gape=22, wing_lift=14, neck_pivot=(-4.0, -7.0),
        scallops=dict(ramps=("wing",), rows=3, period=4, shift=2),
        marks=[
            dict(pts=[(-15.0, -32.2), (-11.5, -33.0), (-8.5, -31.6)], color=("body", 3), on="head"),  # eyebrow
            dict(pts=[(-12.0, -28.0), (-8.0, -28.5)], color=("dark", 0), on="head"),               # eye stripe
            dict(pts=[(12.0, -2.0), (22.0, 0.5)], color=("dark", 0), on="wing"),                   # primaries
            dict(pts=[(-1.0, -7.5), (6.0, -8.5), (13.0, -6.0)], color=("wing", 2), on="wing"),     # covert edge
            dict(pts=[(-17.5, -29.4)], color=("beak", 1), on="head"),                            # nostril
        ],
        ow=dict(end_zoom=1.1), ow_end=dict(head_dy=8.0, body_w=1.25, head_w=1.3, beak_len=2.6, beak_w=3.0,
                                            leg_len=0.7, leg_w=0.8),
    ),

    # Balearica exigua, Ashfall Fossil Beds (~11.9 Ma): a crowned crane from
    # Nebraska; the genus now lives only in Africa. Bones only, so the plumage
    # follows the living crowned cranes (a reconstruction, flagged in the Codex):
    # slate-grey body, white wing coverts, golden-chestnut tertials, black velvet
    # forehead, a bristly golden crown, white-and-red cheek patch, red throat
    # wattle, dark grey bill and legs. Frame 2: a calling bob with the wings lifted
    # (cranes dance). Shiny: a paler, silver-grey population.
    "balearica": dict(
        ramps={
            "outline": ramp("1a1c22"),
            "body": ramp("383c46", "585e6a", "7c828e", "a2a8b2"),
            "white": ramp("c4c4bc", "f0eee6"),
            "crest": ramp("a8843e", "dcc06e"),
            "chestnut": ramp("7a4a2a", "aa6c3e"),
            "red": ramp("c04a3a"),
            "leg": ramp("2c2c32", "4c4c54"),
            "beak": ramp("44444a"),
        },
        front=0.75, back=0.78, icon=0.38,
        shiny={"body": dict(deg=0, sat=0.6, val=1.3)},
        body=[(6.0, -3.0, 13.0, 8.5, 12), (-3.0, -4.0, 8.0, 7.5, 0), (13.0, -1.0, 8.0, 6.5, 18)],
        wing_ramp="white",
        regions=[dict(ramp="chestnut", right=13.0, on="wing"),
                 dict(ramp="white", ellipse=(-13.4, -30.8, 2.6, 2.2), on="head"),
                 dict(ramp="outline", ellipse=(-15.0, -34.2, 2.6, 1.6), on="head")],
        neck=dict(pts=[(-4.0, -8.0), (-9.0, -17.0), (-9.0, -25.0), (-11.0, -30.0)], radii=[5.0, 3.0, 2.6, 2.8],
                  bend=0.4),
        head=[(-12.5, -32.0, 4.0, 3.6, 0)],
        beak=dict(upper=dict(pts=[(-15.8, -32.6), (-19.0, -31.6), (-20.8, -30.4)], radii=[1.4, 0.9, 0.4]),
                  lower=dict(pts=[(-15.8, -31.2), (-19.5, -30.4)], radii=[0.9, 0.4]),
                  hinge=(-15.8, -31.4)),
        beak_ramp="beak",
        eye=((-14.2, -32.6), 1.2, 0.8), iris=("white", 1), eye_hi=("white", 1),
        wing=dict(coverts=[(5.5, -4.0, 11.5, 6.5, 10)],
                  primaries=dict(pts=[(12.0, -2.0), (20.0, 2.0), (25.5, 5.0)], radii=[5.0, 3.4, 1.4]),
                  root=(-2.0, -6.0)),
        tail=[[(16.0, -4.0), (24.0, -2.0), (23.0, 2.0), (16.0, 2.0)]],
        tail_root=(16.0, -2.0), tail_ramp="body",
        legs=[
            dict(near=False, swing=-1, hip=(8.0, 1.0), ankle=(11.0, 16.0), foot=(8.0, 30.0),
                 toes=[(2.0, 31.0), (3.5, 31.5)], hallux=(10.5, 30.8), tibia_r=(3.2, 1.1), tarsus_r=(1.0, 0.9),
                 tibia_ramp="leg"),
            dict(near=True, swing=1, hip=(3.0, 1.5), ankle=(6.0, 16.0), foot=(2.0, 30.0),
                 toes=[(-4.5, 31.0), (-3.0, 31.6)], hallux=(4.5, 30.8), tibia_r=(3.4, 1.15), tarsus_r=(1.05, 0.95),
                 tibia_ramp="leg"),
        ],
        head_turn=8, gape=22, wing_lift=18, neck_pivot=(-4.0, -8.0),
        extra=[
            *spray(-11.0, -35.0, 9, -150, -30, 6.0),                                           # golden crown
            dict(shape="ellipse", args=(-14.0, -28.0, 1.0, 1.6, 0), ramp="red", z=3.4, on="head"),   # throat wattle
        ],
        scallops=None,
        marks=[
            dict(pts=[(-13.6, -30.4), (-11.8, -29.6)], color="red", on="head"),          # red upper cheek
            dict(pts=[(14.0, 0.0), (22.0, 3.2)], color=("chestnut", 0), on="wing"),
            dict(pts=[(-1.0, -9.0), (7.0, -10.2), (13.0, -7.5)], color=("white", 0), on="wing"),
            dict(pts=[(-17.5, -32.4)], color="outline", on="head"),
        ],
        ow=dict(end_zoom=1.15, length=19), ow_end=dict(head_dy=10.0, body_w=1.25, head_w=1.3, beak_len=3.0, leg_len=0.7, leg_w=0.8),
        ow_extra=[*[dict(shape="tube", args=([(0.0, -25.0), (dx * 1.0, -25.5 - dy)], [0.6, 0.45]), ramp="crest",
                         z=1.6, view=v) for dx, dy in ((-4.0, 3.0), (-2.0, 4.5), (0.0, 5.0), (2.0, 4.5), (4.0, 3.0))
                    for v in ("south", "north")]],
    ),

    # Anchigyps voorhiesi, Ashfall Fossil Beds (~11.9 Ma): an accipitrid ("near
    # vulture") from a nearly complete skeleton, intermediate between eagles and
    # Old World vultures (Zhang, Feduccia & James 2012): a scavenger that likely
    # still took live prey. Reconstruction: dark brown eagle-like plumage, a
    # partly bare pinkish face and a pale neck ruff (vulture cues, speculative),
    # hooked bill with a pale cere, feathered "trousers", yellow feet with talons.
    # Frame 2: mantling (wings lifted over prey) with a hiss. Shiny: a pale morph,
    # as in many raptors.
    "anchigyps": dict(
        ramps={
            "outline": ramp("1c140e"),
            "body": ramp("3a2a1e", "5a4230", "7e6046", "a28462"),
            "ruff": ramp("b8a58a", "e0d0b4"),
            "face": ramp("b08478", "d8aea0"),
            "beak": ramp("3a3634", "a8a49a"),
            "cere": ramp("c8b464"),
            "leg": ramp("a89048", "d4c070"),
        },
        front=0.9, back=0.95, icon=0.44,
        shiny={"body": dict(deg=6, sat=0.55, val=1.45)},
        body=[(6.0, -1.0, 13.0, 9.5, 28), (-1.0, -4.0, 8.0, 8.0, 0), (12.0, 4.0, 8.0, 7.0, 40)],
        head_ramp="face",
        regions=[dict(ramp="ruff", below=(-11.5, 0.0), on="head"),
                 dict(ramp="body", above=(-21.6, 0.0), on="head")],
        neck=dict(pts=[(-3.0, -8.0), (-6.5, -15.0)], radii=[6.0, 3.6]),
        head=[(-8.0, -19.0, 4.8, 4.2, 0)],
        beak=dict(upper=dict(pts=[(-11.5, -19.8), (-15.4, -19.6), (-17.6, -18.0), (-17.4, -15.6)],
                             radii=[2.0, 1.6, 1.1, 0.5]),
                  lower=dict(pts=[(-11.5, -17.6), (-15.0, -17.4)], radii=[1.2, 0.6]),
                  hinge=(-11.5, -17.9)),
        eye=((-8.8, -20.2), 1.4, 0.9), iris=("ruff", 0), eye_hi=("ruff", 1),
        wing=dict(coverts=[(6.0, -1.0, 11.0, 8.0, 32)],
                  primaries=dict(pts=[(10.0, 2.0), (17.0, 10.0), (20.0, 14.0)], radii=[5.6, 3.6, 1.5]),
                  root=(-1.0, -6.0)),
        wing_ramp="body",
        tail=[[(14.0, 6.0), (22.0, 16.0), (19.0, 18.5), (12.0, 10.0)]],
        tail_root=(13.0, 6.0), tail_ramp="body",
        legs=[
            dict(near=False, swing=-1, hip=(7.0, 4.0), ankle=(8.0, 14.0), foot=(6.0, 22.0),
                 toes=[(1.0, 23.0), (2.5, 23.6)], hallux=(8.5, 23.0), tibia_r=(4.6, 2.6), tarsus_r=(1.4, 1.2),
                 toe_r=0.9, tibia_ramp="body"),
            dict(near=True, swing=1, hip=(2.0, 4.0), ankle=(3.0, 14.0), foot=(1.0, 22.0),
                 toes=[(-4.5, 23.0), (-3.0, 23.6)], hallux=(3.5, 23.0), tibia_r=(4.8, 2.7), tarsus_r=(1.5, 1.3),
                 toe_r=0.95, tibia_ramp="body"),
        ],
        head_turn=-14, gape=26, wing_lift=26, neck_pivot=(-3.0, -8.0),
        extra=[dict(shape="tube", args=([(-11.6, -20.6), (-13.4, -20.4)], [1.25, 1.1]), ramp="cere", z=3.6,
                    on="head")],
        scallops=dict(ramps=("body",), rows=3, period=4, shift=2),
        marks=[
            dict(pts=[(14.0, 6.0), (17.0, 11.0)], color="outline", on="wing"),            # primary tips
            dict(pts=[(0.0, -6.0), (6.0, -7.0), (12.0, -3.0)], color=("body", 3), on="wing"),  # covert edge
            dict(pts=[(-16.8, -17.0), (-17.2, -16.0)], color=("beak", 0), on="head"),        # dark hook
            dict(pts=[(-12.8, -20.8)], color="outline", on="head"),                         # nostril
        ],
        ow=dict(end_zoom=1.05), ow_end=dict(head_dy=5.0, body_w=1.25, head_w=1.25, beak_len=3.0, belly="ruff"),
    ),
}
