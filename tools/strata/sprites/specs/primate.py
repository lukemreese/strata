"""Species specs for the primate body plan (plans/primate.py; engine keys in
plans/small_mammal.py and plans/canid.py). Owned by the small-mammal artist.
See specs/fish.py for the common keys.

All coat colours are reconstructions from living relatives (tree shrews for
Purgatorius; tarsiers and galagos for the omomyids; lemurs for Notharctus).
Branch bark is the same in every primate spec.
"""

from ..core.color import ramp

BARK = ramp("54422f", "7c664c")
EYE = ramp("c8902e")


def whole(group, ramp_):
    return dict(on=group, kind="below", line=(0.0, -99.0, 0.0), ramp=ramp_)


def tail_tip(f, ramp_="dark"):
    return dict(on="tail", kind="tip", f=f, ramp=ramp_)


def head_ell(cx, cy, rx, ry, ramp_, deg=0):
    return dict(on="head", kind="ell", e=(cx, cy, rx, ry, deg), ramp=ramp_)


SPECS = {
    # Purgatorius, Tullock Fm (~65.9 Ma), ~40 g, ~15 cm: a plesiadapiform,
    # close to the ancestry of primates, known from teeth and ankle bones that
    # show tree-climbing mobility. Tree-shrew build: pointed snout, eyes on the
    # sides of the head (not forward), claws, long tail. Drawn on a branch.
    # Coat speculative: olive-brown tree-shrew agouti, pale belly.
    "purgatorius": dict(
        ramps={
            "outline": ramp("221a14"),
            "fur": ramp("4e3e2a", "73603f", "988158", "b8a276"),
            "pale": ramp("b6a284", "d6c6a6", "efe6d0"),
            "dark": ramp("2a2018", "403226"),
            "skin": ramp("8c5c50"),
            "white": ramp("f6f2e6"),
            "bark": BARK,
        },
        front=1.12, back=1.16, icon=0.5,
        shiny={"fur": dict(deg=-14, sat=1.4, val=1.0), "dark": dict(deg=-10, sat=1.2, val=1.2)},
        body=dict(L=12.0, top_s=-5.2, top_h=-6.4, chest=7.8, waist=7.0, hip=8.6, sag=0.4, k=0.16),
        leg=dict(h=5.2, fr=(1.8, 1.3, 1.0), hr=(2.4, 1.5, 1.05), digi=0.1, paw=(2.6, 1.0), hpaw=(3.2, 1.05),
                 thigh=0.95, far=(2.2, -2.0), knee=3.4, stride=22.0),
        neck=dict(r0=3.6, r1=3.2, base=(0.5, 2.4)),
        head=dict(dx=-5.6, dy=-3.6, cr=4.4, ml=4.6, md=3.0, mdrop=0.6, mtilt=6.0, jd=1.5, stop=0.2, taper=0.56),
        ear=dict(kind="round", h=3.2, w=3.0, lean=12.0, dx=1.2, dy=0.6, inner=False),
        tail=dict(len=20.0, a0=48.0, bends=[-4.0, -10.0, -14.0, -14.0, -10.0], r=(1.8, 1.9, 1.1), widest=0.3),
        eye=dict(dx=-2.0, dy=-0.9, r=1.4, ring=("pale", 1)),
        marks=[tail_tip(0.86), dict(on="torso", kind="above", line=(0.0, -4.6, 0.02), x=(-12.0, 14.0),
                                    ramp="dark")],
        whiskers=[((-7.6, 1.4), (-11.2, 0.6)), ((-7.6, 2.0), (-11.2, 3.0))],
        claws=True,
        branch=dict(x=(-17.0, 16.0), r=2.0, dy=0.0, tilt=-1.0),
        action=dict(tilt=12.0, gape=0.0, tail=-16.0, ear=-8.0),
        ow_side=dict(tail=dict(a0=12.0, bends=[-6.0, -8.0, -8.0, -6.0, -4.0])),
        ow_end=dict(head=2.4),
    ),
    # Teilhardina brandti, Willwood Fm (~55.8 Ma), ~30 g: one of the oldest
    # true primates (an early omomyiform), mouse-sized, arboreal. Nails, not
    # claws; grasping hands and feet; a short snout and large forward-facing
    # eyes (orbit size suggests it was nocturnal or crepuscular). Coat
    # speculative: warm brown like a mouse lemur or galago, pale belly and eye
    # ring, dark muzzle and tail end (omomyid family marks shared with Omomys).
    "teilhardina": dict(
        ramps={
            "outline": ramp("241911"),
            "fur": ramp("583e28", "80603e", "a6845a", "c6a67a"),
            "pale": ramp("bca486", "dcc8a6", "f4ead6"),
            "dark": ramp("2a1e16", "443224"),
            "skin": ramp("9a6a5c"),
            "white": ramp("fbf8ee"),
            "eye": EYE,
            "bark": BARK,
        },
        front=1.22, back=1.26, icon=0.56,
        shiny={"fur": dict(deg=0, sat=0.3, val=1.06), "dark": dict(deg=0, sat=0.4, val=1.2)},
        body=dict(L=10.0, top_s=-5.2, top_h=-6.6, chest=7.4, waist=6.8, hip=8.6, sag=0.4, k=0.16),
        leg=dict(h=5.0, fr=(1.6, 1.2, 0.95), hr=(2.4, 1.5, 1.0), digi=0.05, paw=(2.4, 1.0), hpaw=(3.4, 1.0),
                 thigh=1.05, far=(2.0, -2.0), knee=3.6, stride=22.0),
        neck=dict(r0=3.4, r1=3.2, base=(0.5, 2.2)),
        head=dict(dx=-4.6, dy=-4.2, cr=5.0, cw=1.0, ml=1.4, md=3.0, mdrop=0.6, mtilt=8.0, jd=1.3, stop=0.0,
                  taper=0.7),
        ear=dict(kind="round", h=4.0, w=3.2, lean=10.0, dx=1.6, dy=0.4, inner=False, far=0.7),
        tail=dict(len=21.0, a0=72.0, bends=[-4.0, -6.0, -8.0, -8.0, -6.0], r=(1.6, 1.6, 1.3), widest=0.3),
        eye=dict(dx=-2.0, dy=-0.9, r=2.2, big="eye", ring=("pale", 1)),
        marks=[tail_tip(0.6), head_ell(-6.2, 1.2, 2.2, 1.6, "dark")],
        whiskers=[((-5.6, 1.0), (-8.8, 0.2)), ((-5.6, 1.6), (-8.8, 2.6))],
        branch=dict(x=(-15.0, 15.0), r=1.9, dy=0.0, tilt=1.0),
        action=dict(tilt=-12.0, gape=0.0, tail=-14.0, ear=-10.0),
        ow_side=dict(tail=dict(a0=-6.0, bends=[-4.0, -2.0, 4.0, 8.0, 8.0])),
        ow_end=dict(head=2.5, ear=1.1),
        ow_face=[(-0.45, -0.12, "eye"), (0.45, -0.12, "eye")],
    ),
    # Omomys carteri, Bridger Fm (~50-47 Ma), ~250 g, ~30 cm with tail: an
    # omomyid, probably related to tarsiers. Huge orbits (nocturnal), short
    # face, long hind legs for leaping, long tail. The descendant-grade of
    # Teilhardina here: the same face and marks on a bigger, longer-legged
    # body. Coat speculative: grey-brown galago/tarsier tones.
    "omomys": dict(
        ramps={
            "outline": ramp("221a15"),
            "fur": ramp("54443a", "7a6656", "9e8a76", "c0ae98"),
            "pale": ramp("bcae98", "dcd0bc", "f4eee2"),
            "dark": ramp("28201c", "40342c"),
            "skin": ramp("96685e"),
            "white": ramp("fbf8f0"),
            "eye": EYE,
            "bark": BARK,
        },
        front=1.08, back=1.12, icon=0.5,
        shiny={"fur": dict(deg=24, sat=1.9, val=1.02), "dark": dict(deg=20, sat=1.4, val=1.2)},
        body=dict(L=12.0, top_s=-5.8, top_h=-7.6, chest=8.2, waist=7.4, hip=9.8, sag=0.5, k=0.16),
        leg=dict(h=6.6, fr=(1.8, 1.3, 1.0), hr=(2.9, 1.7, 1.1), digi=0.05, paw=(2.6, 1.05), hpaw=(4.4, 1.1),
                 thigh=1.15, far=(2.2, -2.2), knee=4.6, hock=1.0, stride=22.0),
        neck=dict(r0=3.6, r1=3.4, base=(0.5, 2.4)),
        head=dict(dx=-4.8, dy=-4.6, cr=5.2, cw=1.0, ml=1.6, md=3.2, mdrop=0.6, mtilt=8.0, jd=1.4, stop=0.0,
                  taper=0.7),
        ear=dict(kind="round", h=4.4, w=3.4, lean=8.0, dx=1.6, dy=0.4, inner=False, far=0.7),
        tail=dict(len=24.0, a0=74.0, bends=[-4.0, -6.0, -8.0, -8.0, -6.0], r=(1.8, 1.9, 1.6), widest=0.4),
        eye=dict(dx=-2.0, dy=-0.9, r=2.35, big="eye", ring=("pale", 1)),
        marks=[tail_tip(0.55), head_ell(-6.4, 1.2, 2.3, 1.6, "dark")],
        whiskers=[((-5.8, 1.0), (-9.0, 0.2)), ((-5.8, 1.6), (-9.0, 2.6))],
        branch=dict(x=(-16.0, 17.0), r=2.1, dy=0.0, tilt=-1.5),
        action=dict(tilt=-14.0, gape=0.0, tail=-12.0, ear=-10.0),
        ow_side=dict(tail=dict(a0=-6.0, bends=[-4.0, -2.0, 4.0, 8.0, 8.0])),
        ow_end=dict(head=2.4, ear=1.1),
        ow_face=[(-0.45, -0.12, "eye"), (0.45, -0.12, "eye")],
    ),
    # Notharctus tenebrosus, Bridger Fm (~50 Ma), ~4 kg, ~90 cm with tail: an
    # adapiform, the lemur-like branch of early primates, known from complete
    # skeletons: long body, long hind legs (a leaper), grasping hands with an
    # opposable big toe, a long tail, a moderately long snout and forward-
    # facing eyes (diurnal-sized orbits). Leaf eater. Coat speculative, by
    # analogy with lemurs: grey-brown with a rufous back, dark face, pale
    # throat and belly, a bushy tail darkening to the tip.
    "notharctus": dict(
        ramps={
            "outline": ramp("201a18"),
            "fur": ramp("4c423e", "706460", "968a82", "b8aea4"),
            "pale": ramp("bcb2a4", "dcd4c8", "f4f0e8"),
            "dark": ramp("221c1a", "3a3230"),
            "tawny": ramp("8a5e3c"),
            "white": ramp("fbf8f0"),
            "eye": ramp("c89a34"),
            "bark": BARK,
        },
        front=0.96, back=1.0, icon=0.46,
        shiny={"fur": dict(deg=24, sat=2.2, val=1.08), "tawny": dict(deg=10, sat=0.6, val=1.4)},
        body=dict(L=16.0, top_s=-6.8, top_h=-8.6, chest=9.6, waist=8.6, hip=11.0, sag=0.5, k=0.16),
        leg=dict(h=7.4, fr=(2.2, 1.6, 1.2), hr=(3.3, 2.0, 1.3), digi=0.05, paw=(3.0, 1.15), hpaw=(4.6, 1.2),
                 thigh=1.1, far=(2.4, -2.4), knee=4.8, hock=1.0, stride=20.0),
        neck=dict(r0=4.2, r1=3.8, base=(0.5, 2.6)),
        head=dict(dx=-5.4, dy=-4.6, cr=5.2, cw=1.0, ml=3.4, md=3.2, mdrop=0.5, mtilt=6.0, jd=1.5, stop=0.3,
                  taper=0.6),
        ear=dict(kind="round", h=3.4, w=3.2, lean=14.0, dx=1.6, dy=0.4, inner=False, far=0.7),
        tail=dict(len=36.0, a0=70.0, bends=[-2.0, -4.0, -6.0, -8.0, -8.0], r=(2.4, 3.8, 3.0), widest=0.6),
        eye=dict(dx=-2.2, dy=-1.1, r=1.85, big="eye", ring=None, far=(-4.6, -1.0, 1.3)),
        marks=[tail_tip(0.62), head_ell(-4.6, 0.6, 3.6, 2.4, "dark", -12),
               dict(on="torso", kind="above", line=(0.0, -5.6, 0.04), x=(-10.0, 14.0), ramp="tawny")],
        nose_ramp=("dark", 0),
        branch=dict(x=(-20.0, 17.0), r=2.4, dy=0.0, tilt=-1.0),
        action=dict(tilt=-10.0, gape=0.0, tail=-10.0, ear=-8.0),
        ow_side=dict(tail=dict(a0=-10.0, bends=[-2.0, 2.0, 6.0, 10.0, 10.0])),
        ow_end=dict(head=2.2),
        ow_face=[(-0.45, -0.12, "eye"), (0.45, -0.12, "eye")],
        fur_dashes=(3, 6),
    ),
}
