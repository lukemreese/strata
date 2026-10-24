"""Species specs for the hoofed_giant body plan (plans/hoofed_giant.py documents
the keys; the engine is shared with rhino_brontothere and proboscidean).
Owned by the giant-lane artist. See specs/fish.py for the common keys.

Colours of extinct species are reconstructions (noted per species); bison and
musk ox colours are real.
"""

from ..core.color import ramp
from ..plans.hoofed_giant import FOOTPRINTS


def whole(group, ramp_):
    """Colours a whole part group (legs, ear, ...) with one ramp."""
    return dict(on=group, kind="below", line=(0.0, -99.0, 0.0), ramp=ramp_)


def head_ell(cx, cy, rx, ry, ramp_, deg=0, on="head"):
    return dict(on=on, kind="ell", e=(cx, cy, rx, ry, deg), ramp=ramp_)


def ell(on, cx, cy, rx, ry, ramp_, deg=0):
    return dict(on=on, kind="ell", e=(cx, cy, rx, ry, deg), ramp=ramp_)


SPECS = {
    # Bison bison, living (MT), ~700 kg, 3 m. Known colours: dark chocolate
    # woolly cape over the head, hump, shoulders and forelegs, a beard, paler
    # tan-brown short-haired hindquarters, short black upcurved horns, a tufted
    # tail. The head hangs low below the hump. Frame 2: head lowered to charge,
    # tail up. Variant: the rare pale "white buffalo" (leucistic).
    "bison": dict(
        ramps={
            "outline": ramp("1c120c"),
            "fur": ramp("4a3020", "6e4a30", "8e6644", "a8825a"),
            "hair": ramp("22160e", "382416", "523822", "6c4e32"),
            "dark": ramp("161010", "2c2420"),
            "horn": ramp("2a2622", "5a5450"),
            "pale": ramp("b09070"),
            "skin": ramp("5a3030"),
        },
        front=1.07, back=1.1, icon=0.53,
        shiny={"fur": dict(deg=8, sat=0.35, val=1.6), "hair": dict(deg=10, sat=0.45, val=2.1),
               "pale": dict(deg=0, sat=0.4, val=1.3)},
        body=dict(L=24.0, top_s=-15.0, top_h=-9.0, chest=20.0, waist=15.0, hip=14.0, sag=0.0,
                  chest_w=1.05, rump_w=0.95, hump=(2.5, 2.5, 9.0, 7.5)),
        leg=dict(h=9.0, fr=(4.2, 2.4, 2.0), hr=(4.4, 2.4, 2.0), fx=2.5, hx=0.5, far=(3.0, -2.5),
                 elbow=1.0, knee=2.5, hock=2.0, wrist=0.3, hockh=0.45, thigh=0.75,
                 foot=dict(kind="hoof", l=3.6, h=2.2)),
        neck=dict(r0=8.0, r1=6.5, base=(-1.0, 7.0)),
        head=dict(dx=-9.5, dy=8.0, cr=6.6, cw=1.0, chh=0.95, ml=3.4, md=6.2, mdrop=0.5, mtilt=62.0,
                  taper=0.8, jd=2.4, lumps=[(0.5, -3.5, 5.5, 4.0, 0)]),
        ear=dict(kind="leaf", h=3.2, w=1.8, lean=105.0, dx=0.5, dy=3.4),
        tail=dict(len=10.0, a0=80.0, bend=2.0, r=(1.3, 1.0, 1.7), widest=0.2),
        eye=dict(dx=-2.6, dy=0.8, r=1.1),
        marks=[ell("torso", -12.0, -6.0, 13.0, 18.0, "hair", -10),
               dict(on=("head", "jaw", "neck", "ear"), kind="below", line=(0.0, -99.0, 0.0), ramp="hair"),
               dict(on="legs", kind="below", line=(-9.0, -99.0, 0.0), x=(-99.0, -6.0), ramp="hair"),
               dict(on="tail", kind="tip", f=0.6, ramp="hair")],
        belly=(99.0, 0.0), throat=(99.0, 0.0),
        hair=dict(ramps=("hair",), period=3, run=2),
        extras=[
            # horns: short, out and up, black
            dict(kind="tube", on="head", pts=[(0.6, -4.2), (0.0, -7.0), (-1.2, -8.6)], radii=[1.3, 1.0, 0.5],
                 ramp="horn", z=3.5, far=(-2.6, 0.3)),
            # beard under the chin and throat
            dict(kind="fringe", on="head", top=[(-6.0, 4.0), (-1.0, 5.0)], bottom=[(-6.0, 6.0), (0.5, 7.5)],
                 teeth=3, depth=2.5, r=1.6, ramp="hair", z=2.95),
            # chaps: long hair on the upper forelegs
            dict(kind="fringe", on="body", top=[(-15.0, 2.0), (-7.0, 3.0)], bottom=[(-15.5, 8.0), (-7.0, 7.0)],
                 teeth=3, depth=2.5, r=1.6, ramp="hair", z=2.2),
        ],
        action=dict(tilt=-12.0, tail=-40.0),
        ow_end=dict(head=1.5, hump=0.9, head_dy=0.4, ear=1.0, head_inner="outline", muzzle=0.9, muzzle_dy=0.55),
        ow_ramps=dict(body="hair", muzzle="hair", head="hair", legs="hair"),
        ow_chest_pale=False,
        ow_extras=dict(
            south=[dict(kind="tube", pts=[(0.55, -0.55), (1.05, -0.6), (1.2, -1.0)], radii=[0.2, 0.15, 0.09],
                        ramp="horn", z=3.5, mirror=True),
                   dict(kind="fringe", top=[(-0.45, 0.8), (0.45, 0.8)], bottom=[(-0.4, 1.05), (0.4, 1.05)],
                        teeth=2, depth=0.35, r=0.3, ramp="hair", z=3.2)],
            north=[dict(kind="tube", pts=[(0.55, -0.6), (1.0, -0.65), (1.15, -1.0)], radii=[0.2, 0.15, 0.09],
                        ramp="horn", z=-0.3, mirror=True)]),
        footprint=FOOTPRINTS["cloven"],
    ),
    # Ovibos moschatus, Natural Trap Cave (~20 ka; living in the Arctic), ~300 kg,
    # 2.2 m. Known colours: long dark-brown guard hair hanging as a skirt almost
    # to the ground, a pale cream saddle, whitish stockings, a pale muzzle;
    # horns with a broad boss across the forehead that sweep down beside the
    # face and hook forward and up, cream with dark tips. Frame 2: head lowered
    # to present the horns. Variant: a paler, greyer coat (white-faced musk oxen
    # and paler populations occur).
    "ovibos": dict(
        ramps={
            "outline": ramp("1a120c"),
            "fur": ramp("2a1c12", "44301e", "60462e", "7c6040"),
            "pale": ramp("a48c66", "c8b088", "e4d4b0"),
            "horn": ramp("6a5a44", "b0a07e", "dcd0b0"),
            "dark": ramp("161010", "30261e"),
            "skin": ramp("5a3030"),
        },
        front=1.25, back=1.3, icon=0.62,
        shiny={"fur": dict(deg=6, sat=0.45, val=1.55), "pale": dict(deg=0, sat=0.5, val=1.05)},
        body=dict(L=19.0, top_s=-13.0, top_h=-10.5, chest=16.5, waist=14.0, hip=13.5, sag=0.2,
                  chest_w=1.05, rump_w=1.0, hump=(2.0, 2.0, 7.0, 5.0)),
        leg=dict(h=8.0, fr=(3.2, 2.0, 1.8), hr=(3.4, 2.0, 1.8), fx=2.5, hx=0.0, far=(3.0, -2.5),
                 elbow=0.8, knee=2.0, hock=1.6, wrist=0.3, hockh=0.45, thigh=0.0,
                 foot=dict(kind="hoof", l=3.2, h=2.0)),
        neck=dict(r0=7.0, r1=5.8, base=(-1.0, 6.0)),
        head=dict(dx=-7.5, dy=5.5, cr=5.4, cw=1.0, chh=0.92, ml=3.0, md=5.0, mdrop=0.4, mtilt=52.0,
                  taper=0.85, jd=2.0),
        ear=dict(kind="leaf", h=2.0, w=1.4, lean=110.0, dx=1.0, dy=3.0, inner=False),
        tail=dict(len=4.0, a0=80.0, bend=0.0, r=(1.4, 1.4, 1.2), widest=0.5),
        eye=dict(dx=-2.4, dy=0.4, r=1.0),
        marks=[ell("torso", 2.0, -12.5, 7.5, 3.6, "pale", 4),
               dict(on="legs", kind="socks", h=4.6, ramp="pale"),
               head_ell(-7.5, 4.5, 3.6, 3.2, "pale", -30)],
        belly=(99.0, 0.0), throat=(99.0, 0.0),
        hair=dict(ramps=("fur",), period=3, run=3),
        extras=[
            # the skirt of guard hair, hanging over the upper legs
            dict(kind="fringe", on="body", top=[(-16.0, -2.0), (-6.0, -2.0), (6.0, -3.0), (14.5, -4.0)],
                 bottom=[(-15.5, 7.0), (-5.0, 8.0), (6.0, 8.0), (14.5, 6.5)],
                 teeth=6, depth=1.6, r=2.5, ramp="fur", z=2.3),
            # chin and throat ruff
            dict(kind="fringe", on="head", top=[(-5.5, 4.0), (0.5, 4.5)], bottom=[(-5.0, 6.5), (1.5, 8.0)],
                 teeth=3, depth=1.8, r=1.4, ramp="fur", z=2.95),
            # horn boss and the hooked horn
            dict(kind="ell", on="head", e=(0.2, -4.2, 4.2, 1.9, -8), ramp="horn", z=3.45),
            dict(kind="tube", on="head", pts=[(1.4, -3.2), (2.4, -0.6), (1.6, 2.8), (-0.6, 4.0), (-2.4, 3.0)],
                 radii=[1.9, 1.6, 1.25, 0.9, 0.5], ramp="horn", tip=(0.8, "dark"), z=3.5),
        ],
        action=dict(tilt=-10.0, tail=0.0),
        ow_end=dict(head=1.7, hump=0.55, head_dy=0.35, ear=0.7, head_inner="outline", muzzle=0.85,
                    muzzle_dy=0.55, legs=0.8),
        ow_ramps=dict(muzzle="pale"),
        ow_chest_pale=False,
        ow_extras=dict(
            south=[dict(kind="ell", e=(0.0, -0.6, 0.85, 0.32), ramp="horn", z=3.45),
                   dict(kind="tube", pts=[(0.35, -0.62), (0.95, -0.45), (1.05, 0.15), (1.3, 0.3), (1.42, 0.0)],
                        radii=[0.3, 0.26, 0.2, 0.15, 0.09], ramp="horn", tip=(0.8, "dark"), z=3.5, mirror=True),
                   dict(kind="fringe", top=[(-1.55, 0.6), (1.55, 0.6)], bottom=[(-1.7, 1.45), (1.7, 1.45)],
                        teeth=5, depth=0.25, r=0.4, ramp="fur", z=2.3)],
            north=[dict(kind="ell", e=(0.0, -0.6, 0.8, 0.3), ramp="horn", z=-0.3),
                   dict(kind="tube", pts=[(0.35, -0.62), (0.95, -0.45), (1.05, 0.15), (1.3, 0.3), (1.42, 0.0)],
                        radii=[0.3, 0.26, 0.2, 0.15, 0.09], ramp="horn", tip=(0.8, "dark"), z=-0.3,
                        mirror=True),
                   dict(kind="ell", e=(0.0, 0.3, 1.05, 0.45), ramp="pale", z=0.1),
                   dict(kind="fringe", top=[(-1.6, 0.8), (1.6, 0.8)], bottom=[(-1.75, 1.5), (1.75, 1.5)],
                        teeth=5, depth=0.25, r=0.4, ramp="fur", z=1.5)]),
        footprint=FOOTPRINTS["cloven"],
    ),
    # Coryphodon, Willwood Fm (~55 Ma), ~500 kg, 2.3 m: a pantodont, the
    # largest animal of its world. Hippo-like: long barrel body, short stout
    # limbs, broad five-toed feet with hoof-like nails, short tail, a big head
    # with a deep short muzzle and large tusk-like canines (upper and lower), a
    # tiny brain case, small eyes and ears. Skin speculative: sparse-haired
    # grey-brown with a pinkish underside and mouth, after hippos and its
    # swampy habitat. Frame 2: the hippo-style yawn showing the tusks.
    # Variant: a ruddier, sun-browned morph.
    "coryphodon": dict(
        ramps={
            "outline": ramp("1c1414"),
            "fur": ramp("3a302a", "5a4c42", "7a6a5c", "9a8a7a"),
            "pale": ramp("9a7a72", "bc9c90", "d8bcae"),
            "dark": ramp("1e1818", "3a2e2c"),
            "hoof": ramp("3a3230", "7a706a"),
            "tusk": ramp("a89a80", "e8dcc4"),
            "skin": ramp("8a4a48"),
        },
        front=1.05, back=1.08, icon=0.52,
        shiny={"fur": dict(deg=-14, sat=1.9, val=1.05), "pale": dict(deg=-6, sat=1.2, val=1.0)},
        body=dict(L=24.0, top_s=-10.5, top_h=-10.0, chest=16.5, waist=15.5, hip=15.0, sag=0.8, paunch=1.8,
                  chest_w=1.05, rump_w=1.0),
        leg=dict(h=6.5, fr=(4.6, 3.6, 3.3), hr=(4.8, 3.6, 3.3), fx=2.5, hx=0.0, far=(3.0, -2.5),
                 elbow=1.0, knee=1.6, hock=1.0, wrist=0.25, hockh=0.35, thigh=0.85, stride=12.0,
                 foot=dict(kind="pad", l=6.0, h=2.4, nails=3)),
        neck=dict(r0=7.0, r1=6.2, base=(0.0, 4.0)),
        head=dict(dx=-9.5, dy=0.0, cr=6.2, cw=1.1, chh=0.85, ml=5.2, md=7.2, mdrop=0.6, mtilt=16.0,
                  taper=0.86, jd=3.2, lumps=[(-4.5, -2.6, 2.2, 1.6, 0)]),
        ear=dict(kind="leaf", h=3.2, w=2.0, lean=45.0, dx=0.5, dy=0.6),
        tail=dict(len=7.0, a0=75.0, bend=4.0, r=(1.8, 1.4, 0.9), widest=0.2),
        eye=dict(dx=-3.4, dy=-1.8, r=1.0),
        marks=[head_ell(-11.0, 6.5, 3.5, 2.6, "pale", -10)],
        wrinkles=[dict(on="body", pts=[(-8.5, -6.0), (-7.5, -1.0), (-8.0, 3.0)]),
                  dict(on="body", pts=[(7.0, -7.5), (6.2, -3.0), (6.8, 1.0)]),
                  dict(on="head", pts=[(3.0, -1.0), (4.5, 2.0), (4.0, 5.0)])],
        extras=[
            # upper canine (tusk): stout, curving down and back
            dict(kind="tube", on="head", pts=[(-10.6, 5.8), (-10.8, 8.8), (-9.6, 10.8)], radii=[1.1, 0.9, 0.4],
                 ramp="tusk", z=3.5, outline="outline"),
            # lower canine on the jaw, procumbent, up and forward
            dict(kind="tube", on="jaw", pts=[(-13.2, 9.4), (-14.6, 7.6), (-15.2, 5.6)], radii=[0.95, 0.75, 0.35],
                 ramp="tusk", z=3.45, outline="outline"),
        ],
        teeth=[((-14.6, 6.6), (-14.6, 7.4), False)],
        action=dict(tilt=14.0, gape=-26.0, tail=0.0, ear=-10.0),
        ow_end=dict(head=1.55, ear=0.9, head_dy=0.15, muzzle=1.1, muzzle_dy=0.62, legs=0.8, eyes=0.55,
                    eye_dy=-0.25),
        ow_ramps=dict(muzzle="pale"),
        ow_extras=dict(
            south=[dict(kind="tube", pts=[(0.42, 0.8), (0.46, 1.0), (0.4, 1.12)], radii=[0.14, 0.11, 0.06],
                        ramp="tusk", z=3.5, mirror=True)]),
        footprint=FOOTPRINTS["pad"],
    ),
    # Uintatherium anceps, Bridger Fm (~46 Ma), ~2 t, 4 m: a uintathere
    # (dinoceratan), rhino-sized and graviportal. A long, low skull with three
    # pairs of bony knobs (small nasal ones at the snout tip, maxillary ones
    # before the eyes, large parietal ones at the back of the skull), long
    # sabre-like upper canines sheathed by a flange on the lower jaw (males),
    # pillar legs, short broad feet, short tail. Skin speculative: grey with a
    # darker dorsum and paler belly, rhino-like folds. Frame 2: head raised,
    # jaw dropped to bare the sabres. Variant: a browner, ochre-dusted morph.
    "uintatherium": dict(
        ramps={
            "outline": ramp("181618"),
            "fur": ramp("38363a", "56525a", "76727a", "96929a"),
            "pale": ramp("8a8480", "aaa4a0"),
            "dark": ramp("1c1a1e"),
            "hoof": ramp("2c2a2c", "6a6664"),
            "tusk": ramp("a89c86", "e6dcc6"),
            "knob": ramp("6a6670", "a8a4ac"),
            "skin": ramp("7a4848"),
        },
        front=0.86, back=0.88, icon=0.42,
        shiny={"fur": dict(deg=125, sat=2.6, val=1.02), "knob": dict(deg=125, sat=2.2, val=1.0),
               "pale": dict(deg=4, sat=1.5, val=1.0)},
        body=dict(L=29.0, top_s=-16.0, top_h=-13.0, chest=19.5, waist=17.0, hip=17.0, sag=1.0, paunch=1.5,
                  chest_w=1.05, rump_w=1.0, hump=(3.0, 2.0, 8.0, 4.0)),
        leg=dict(h=9.5, fr=(4.8, 3.9, 3.6), hr=(5.0, 3.8, 3.6), fx=2.5, hx=0.5, far=(3.5, -3.0),
                 elbow=0.4, knee=1.2, hock=0.8, wrist=0.3, hockh=0.35, thigh=0.6, stride=10.0,
                 foot=dict(kind="pad", l=6.2, h=2.6, nails=3)),
        neck=dict(r0=7.5, r1=6.5, base=(0.0, 4.5)),
        head=dict(dx=-12.5, dy=-1.5, cr=7.0, cw=1.2, chh=0.8, cdeg=4.0, ml=8.5, md=5.2, mdrop=0.4, mtilt=8.0,
                  taper=0.8, jd=2.2),
        ear=dict(kind="leaf", h=2.6, w=1.6, lean=70.0, dx=2.5, dy=1.4),
        tail=dict(len=7.0, a0=75.0, bend=4.0, r=(1.6, 1.2, 1.0), widest=0.2),
        eye=dict(dx=-3.8, dy=-0.6, r=1.0),
        marks=[dict(on="torso", kind="above", line=(0.0, -12.0, 0.03), ramp="fur"),
               head_ell(4.0, -10.0, 3.0, 3.6, "knob", 10),
               head_ell(-6.0, -5.2, 2.0, 2.6, "knob", 30), whole("jaw", "fur")],
        wrinkles=[dict(on="body", pts=[(-10.0, -11.0), (-9.0, -5.0), (-9.6, 1.0)]),
                  dict(on="body", pts=[(9.0, -11.5), (8.2, -6.0), (8.8, -1.0)]),
                  dict(on="body", pts=[(-18.0, -2.0), (-14.5, 0.0)])],
        extras=[
            # parietal knobs (largest), at the back of the skull, far one behind
            dict(kind="tube", on="head", pts=[(2.6, -3.4), (3.4, -7.4), (4.2, -9.6)], radii=[2.8, 2.2, 2.0],
                 ramp="knob", z=3.35, far=(-1.6, 0.4), far_z=-0.55),
            # maxillary knobs before the eyes
            dict(kind="tube", on="head", pts=[(-6.0, -1.6), (-6.4, -4.5), (-6.6, -5.6)], radii=[1.8, 1.4, 1.3],
                 ramp="knob", z=3.35, far=(-1.4, 0.3), far_z=2.95),
            # nasal knobs at the snout tip
            dict(kind="tube", on="head", pts=[(-14.6, 0.6), (-15.4, -1.2)], radii=[1.2, 0.9],
                 ramp="knob", z=3.35),
            # mandibular flange: a deep blade under the chin, sheathing the sabre
            dict(kind="pillow", on="jaw", pts=[(-13.5, 5.2), (-7.5, 5.0), (-8.6, 10.0), (-12.6, 11.2)], r=1.4,
                 ramp="fur", z=2.92),
            # sabre upper canine
            dict(kind="facet", on="head", pts=[(-12.0, 3.0), (-8.6, 3.2), (-9.2, 9.4), (-11.2, 13.8)],
                 ramp="tusk", z=2.96, outline="outline"),
        ],
        action=dict(tilt=10.0, gape=-24.0, tail=0.0, ear=-10.0),
        ow=dict(size=64, end_zoom=1.45),
        ow_end=dict(head=1.6, ear=0.6, head_dy=0.0, muzzle=0.9, muzzle_dy=0.62, legs=0.9, eyes=0.68,
                    eye_dy=-0.05),
        ow_extras=dict(
            south=[dict(kind="tube", pts=[(0.45, -0.55), (0.7, -0.85), (0.86, -1.0)], radii=[0.34, 0.31, 0.3],
                        ramp="knob", z=2.9, mirror=True),
                   dict(kind="tube", pts=[(0.38, 0.0), (0.45, -0.4)], radii=[0.22, 0.2], ramp="knob", z=3.4,
                        mirror=True),
                   dict(kind="facet", pts=[(0.42, 0.85), (0.6, 0.85), (0.52, 1.45)], ramp="tusk", z=3.5,
                        mirror=True)],
            north=[dict(kind="tube", pts=[(0.45, -0.55), (0.7, -0.85), (0.86, -1.0)], radii=[0.34, 0.31, 0.3],
                        ramp="knob", z=-0.3, mirror=True)]),
        footprint=FOOTPRINTS["pad"],
    ),
    # Archaeotherium, Brule Fm (~32 Ma), ~270 kg, 2 m: an entelodont, the "hell
    # pig". A huge, long head (a third of the body), bony jugal flanges hanging
    # below the eyes and knobs under the chin, big canines, high shoulders over
    # tall neural spines, slender legs with two-toed cloven hooves, a thin tail.
    # Coat speculative: bristly dark brown with a black dorsal mane, after
    # pigs and peccaries. Frame 2: the very wide entelodont gape.
    # Variant: a rufous, wild-boar-like morph.
    "archaeothere": dict(
        ramps={
            "outline": ramp("1a1210"),
            "fur": ramp("3a2a22", "5a4232", "7a5c46", "98785c"),
            "pale": ramp("8e7460", "b49a80"),
            "dark": ramp("1a1412", "2e2420"),
            "hoof": ramp("2a2220", "5a4e46"),
            "tusk": ramp("b0a488", "ece2ca"),
            "skin": ramp("8a4440"),
        },
        front=1.04, back=1.06, icon=0.52,
        shiny={"fur": dict(deg=6, sat=1.7, val=1.15), "pale": dict(deg=4, sat=1.3, val=1.05)},
        body=dict(L=20.0, top_s=-15.0, top_h=-10.5, chest=15.0, waist=11.5, hip=11.5, sag=0.3,
                  chest_w=1.0, rump_w=0.95, hump=(2.5, 1.5, 7.5, 5.0)),
        leg=dict(h=13.0, fr=(3.0, 1.7, 1.4), hr=(3.4, 1.8, 1.4), fx=2.5, hx=0.5, far=(3.0, -2.5),
                 elbow=1.0, knee=2.6, hock=2.4, wrist=0.32, hockh=0.42, thigh=0.85, stride=16.0,
                 foot=dict(kind="hoof", l=2.8, h=2.0)),
        neck=dict(r0=6.0, r1=5.2, base=(-0.5, 5.0)),
        head=dict(dx=-10.5, dy=1.5, cr=5.2, cw=1.15, chh=0.95, ml=10.0, md=5.6, mdrop=0.3, mtilt=10.0,
                  taper=0.7, jd=2.8, lumps=[(-2.0, -2.0, 3.5, 2.2, 10)]),
        ear=dict(kind="leaf", h=3.6, w=2.0, lean=35.0, dx=1.0, dy=0.4),
        tail=dict(len=9.0, a0=78.0, bend=3.0, r=(1.0, 0.8, 1.3), widest=0.2),
        eye=dict(dx=-1.4, dy=-2.0, r=1.2),
        marks=[dict(on=("torso", "neck"), kind="above", line=(0.0, -13.5, 0.15), ramp="dark"),
               dict(on="legs", kind="socks", h=6.0, ramp="dark"),
               dict(on="tail", kind="tip", f=0.65, ramp="dark")],
        hair=dict(ramps=("fur",), period=3, run=2),
        extras=[
            # bristly dorsal mane over the shoulder hump
            # (a fringe whose "bottom" is its upper edge and negative depth: spikes point up)
            dict(kind="fringe", on="body", top=[(-17.0, -12.0), (-1.0, -12.0)],
                 bottom=[(-17.0, -14.0), (-13.0, -17.5), (-7.0, -18.0), (-1.0, -14.5)], teeth=5, depth=-2.2,
                 r=1.3, ramp="dark", z=0.2),
            # jugal flange hanging below the eye
            dict(kind="ell", on="head", e=(-1.8, 4.4, 2.0, 2.8, 15), ramp="fur", z=3.1, light=0.1),
            # chin knob (mandibular tubercle)
            dict(kind="ell", on="jaw", e=(-12.0, 6.6, 1.7, 1.9, 0), ramp="fur", z=2.93),
            # upper canine
            dict(kind="tube", on="head", pts=[(-14.4, 3.4), (-14.6, 6.6)], radii=[1.0, 0.4], ramp="tusk", z=3.5),
        ],
        teeth=[((-14.2, 2.8), (-14.2, 3.6), False), ((-13.6, 4.4), (-13.6, 3.6), True)],
        action=dict(tilt=16.0, gape=-34.0, tail=-20.0, ear=-15.0),
        ow_end=dict(head=1.55, ear=1.1, hump=0.6, head_dy=0.15, muzzle=0.9, muzzle_dy=0.65, legs=1.1, eyes=0.5,
                    eye_dy=-0.35),
        ow_extras=dict(
            south=[dict(kind="ell", e=(0.82, 0.45, 0.32, 0.45, 10), ramp="fur", z=3.2, mirror=True),
                   dict(kind="tube", pts=[(0.3, 0.85), (0.34, 1.15)], radii=[0.13, 0.07], ramp="tusk", z=3.5,
                        mirror=True)]),
        footprint=FOOTPRINTS["cloven"],
    ),
}
