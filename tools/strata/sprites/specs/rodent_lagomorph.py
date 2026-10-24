"""Species specs for the rodent_lagomorph body plan (plans/rodent_lagomorph.py;
engine keys in plans/small_mammal.py and plans/canid.py). Owned by the
small-mammal artist. See specs/fish.py for the common keys.

Family marks: every rodent has orange-enamelled upper incisors and a pale eye
ring; the squirrel line (Douglassciurus -> Cynomys) adds a dark tail tip and a
pale flank line; the ischyromyid line (Paramys -> Ischyromys) a darker back.
The rabbit has white incisors (lagomorph enamel is unpigmented) and a pale scut.
Coat colours of extinct species are reconstructions (agouti browns and greys
of living relatives); the black-tailed prairie dog's colours are real.
"""

from ..core.color import ramp
from ..plans.rodent_lagomorph import FOOTPRINT_RABBIT


def whole(group, ramp_):
    return dict(on=group, kind="below", line=(0.0, -99.0, 0.0), ramp=ramp_)


def tail_tip(f, ramp_="dark"):
    return dict(on="tail", kind="tip", f=f, ramp=ramp_)


ENAMEL = ramp("e09a3a")
GNAW = dict(len=1.9, w=0.5, dx=1.9, rake=0.2, ramp="enamel")

SPECS = {
    # Paramys, Willwood Fm (~56-50 Ma), ~2 kg, ~60 cm with tail: an early
    # ischyromyid, the squirrel-like grade of the first North American rodents.
    # Long body, short limbs with claws, long tail, small rounded ears, a blunt
    # deep snout with big incisors. Coat speculative: grey-brown agouti, darker
    # back, cream belly (forest-floor and trunk climber).
    "paramys": dict(
        ramps={
            "outline": ramp("231a15"),
            "fur": ramp("4e3e32", "73604e", "978268", "b8a486"),
            "pale": ramp("b0a088", "d4c6aa", "efe6d2"),
            "dark": ramp("2a211c", "41342b"),
            "skin": ramp("8a5a50"),
            "white": ramp("f6f2e6"),
            "enamel": ENAMEL,
        },
        front=1.0, back=1.05, icon=0.5,
        shiny={"fur": dict(deg=16, sat=1.9, val=1.06), "dark": dict(deg=16, sat=1.6, val=1.2)},
        body=dict(L=16.0, top_s=-6.2, top_h=-7.4, chest=9.6, waist=8.6, hip=10.2, sag=0.4, k=0.16),
        leg=dict(h=5.0, fr=(2.2, 1.5, 1.1), hr=(2.8, 1.7, 1.2), digi=0.25, paw=(2.8, 1.05), hpaw=(3.8, 1.15),
                 thigh=1.0, far=(2.4, -2.2), stride=20.0),
        neck=dict(r0=4.2, r1=3.8, base=(0.5, 2.6)),
        head=dict(dx=-6.2, dy=-3.6, cr=5.0, ml=2.8, md=4.0, mdrop=0.9, mtilt=10.0, jd=1.7, stop=0.4, taper=0.82),
        ear=dict(kind="round", h=2.8, w=3.2, lean=14.0, dx=1.4, dy=0.6, inner=False),
        tail=dict(len=21.0, a0=4.0, bends=[-9.0, -9.0, -7.0, -5.0, -3.0], r=(2.4, 2.9, 1.6), widest=0.5),
        eye=dict(dx=-2.0, dy=-1.1, r=1.6, ring=("pale", 2)),
        teeth=dict(gnaw=GNAW),
        marks=[dict(on="torso", kind="above", line=(0.0, -5.4, 0.02), x=(-12.0, 14.0), ramp=("dark")),
               dict(on="tail", kind="above", line=(0.0, -99.0, 0.0), ramp="fur")],
        whiskers=[((-5.6, 1.4), (-9.8, 0.4)), ((-5.6, 2.0), (-9.8, 3.0))],
        claws=True,
        action=dict(tilt=9.0, gape=0.0, tail=-12.0, ear=-8.0),
        ow_end=dict(head=2.3),
        ow_face=[(0.0, 0.88, "enamel")],
    ),
    # Ischyromys, Brule Fm (~32 Ma), ~0.8 kg, ~40 cm: a late ischyromyid, the
    # descendant grade of Paramys: same long-bodied, long-tailed build with a
    # lighter frame, longer legs and a fuller tail. Coat speculative: a warmer
    # brown agouti than Paramys with the line's darker back and a dark tail tip.
    "ischyromys": dict(
        ramps={
            "outline": ramp("251912"),
            "fur": ramp("56402e", "7e6044", "a2825e", "c2a47c"),
            "pale": ramp("bca88a", "dccaaa", "f2e8d4"),
            "dark": ramp("2c2018", "463426"),
            "skin": ramp("8c5a50"),
            "white": ramp("f6f2e6"),
            "enamel": ENAMEL,
        },
        front=1.08, back=1.12, icon=0.52,
        shiny={"fur": dict(deg=-8, sat=0.35, val=1.0), "dark": dict(deg=0, sat=0.4, val=1.0)},
        body=dict(L=14.0, top_s=-6.0, top_h=-7.2, chest=9.0, waist=7.8, hip=9.6, sag=0.4, k=0.16),
        leg=dict(h=5.8, fr=(2.0, 1.4, 1.05), hr=(2.6, 1.6, 1.1), digi=0.3, paw=(2.6, 1.0), hpaw=(3.8, 1.1),
                 thigh=1.0, far=(2.3, -2.1), stride=20.0),
        neck=dict(r0=4.0, r1=3.6, base=(0.5, 2.6)),
        head=dict(dx=-6.0, dy=-3.8, cr=4.8, ml=2.8, md=3.8, mdrop=0.8, mtilt=10.0, jd=1.6, stop=0.4, taper=0.8),
        ear=dict(kind="round", h=3.2, w=3.2, lean=12.0, dx=1.4, dy=0.4, inner=False),
        tail=dict(len=20.0, a0=-2.0, bends=[-10.0, -10.0, -8.0, -5.0, -2.0], r=(2.3, 3.2, 1.8), widest=0.55),
        eye=dict(dx=-2.0, dy=-1.0, r=1.5, ring=("pale", 1)),
        teeth=dict(gnaw=dict(GNAW, len=1.8)),
        marks=[tail_tip(0.84),
               dict(on="torso", kind="above", line=(0.0, -5.2, 0.02), x=(-12.0, 14.0), ramp=("dark"))],
        whiskers=[((-5.4, 1.4), (-9.6, 0.4)), ((-5.4, 2.0), (-9.6, 3.0))],
        claws=True,
        action=dict(tilt=9.0, gape=0.0, tail=-14.0, ear=-8.0),
        ow_end=dict(head=2.3),
        ow_face=[(0.0, 0.88, "enamel")],
    ),
    # Palaeolagus haydeni, Brule Fm (~33 Ma), ~0.8 kg, ~30 cm: an early
    # leporid, very common in the White River badlands. Rabbit build, but
    # hind legs shorter than a living rabbit's (it scurried more than hopped)
    # and ears shorter than a jackrabbit's (ear length is soft tissue:
    # speculative, kept moderate). Coat speculative: cottontail agouti brown,
    # pale belly and a white scut.
    "palaeolagus": dict(
        ramps={
            "outline": ramp("251c16"),
            "fur": ramp("56442f", "7c6448", "a08766", "c2aa86"),
            "pale": ramp("c0b098", "dcd0bc", "f6f0e4"),
            "dark": ramp("2c221c", "4a3a2c"),
            "skin": ramp("b07c70"),
            "white": ramp("fbf8f0"),
        },
        front=1.12, back=1.16, icon=0.52,
        shiny={"fur": dict(deg=0, sat=0.25, val=1.2), "dark": dict(deg=0, sat=0.4, val=1.5)},
        body=dict(L=11.0, top_s=-6.0, top_h=-9.6, chest=9.4, waist=10.0, hip=13.0, sag=-1.4, rump_w=1.12,
                  k=0.22),
        leg=dict(h=4.8, fr=(1.8, 1.3, 1.0), hr=(3.2, 2.0, 1.3), digi=0.05, paw=(2.6, 1.0), hpaw=(5.6, 1.25),
                 thigh=1.3, far=(2.0, -2.6), knee=4.0, hock=1.2, stride=22.0),
        neck=dict(r0=4.4, r1=4.0, base=(0.5, 2.6)),
        head=dict(dx=-5.6, dy=-5.2, cr=5.0, ml=3.0, md=4.2, mdrop=0.8, mtilt=8.0, jd=1.6, stop=0.2, taper=0.86),
        ear=dict(kind="round", h=7.0, w=3.4, lean=28.0, dx=1.6, dy=0.4, inner=False, far=0.6),
        tail=dict(len=4.0, a0=-40.0, bend=-10.0, r=(2.2, 2.6, 2.0), widest=0.5, dy=-0.6),
        eye=dict(dx=-1.6, dy=-1.2, r=1.75, ring=("pale", 1)),
        teeth=dict(gnaw=dict(len=1.1, w=0.5, dx=1.6, rake=0.1, ramp="white")),
        marks=[whole("tail", "pale"),
               dict(on="head", kind="above", line=(0.0, 2.6, 0.0), ramp="fur"),
               dict(on="ear", kind="above", line=(0.0, -10.4, 0.0), ramp="dark")],
        whiskers=[((-5.2, 1.6), (-9.0, 0.8)), ((-5.2, 2.2), (-9.0, 3.2))],
        nose_ramp=("skin", 0),
        action=dict(tilt=6.0, gape=0.0, tail=-10.0, ear=-14.0),
        footprint=FOOTPRINT_RABBIT,
        ow_end=dict(head=2.2, ear=1.1),
        ow_face=[(0.0, 0.9, "white")],
    ),
    # Douglassciurus jeffersoni, Chadron Fm, Flagstaff Rim (~36 Ma), ~0.3 kg:
    # the oldest known squirrel, known from a near-complete skeleton already
    # like a living tree squirrel's (long bushy tail, long hind feet, climbing
    # claws). Drawn in the classic squirrel pose, front raised, the tail curled
    # up over the back. Coat speculative: grey squirrel pattern (grizzled
    # grey, white belly and eye ring, the line's dark tail tip and pale flank
    # line).
    "douglassciur": dict(
        ramps={
            "outline": ramp("1f1c1c"),
            "fur": ramp("4a4446", "6e6666", "948a86", "b8aea6"),
            "pale": ramp("c4bcb0", "e2dcd2", "f8f6f0"),
            "dark": ramp("282426", "3e3838"),
            "tawny": ramp("8e6c50"),
            "skin": ramp("a87870"),
            "white": ramp("fcfaf6"),
            "enamel": ENAMEL,
        },
        front=1.16, back=1.2, icon=0.52,
        shiny={"fur": dict(deg=24, sat=4.0, val=1.05), "dark": dict(deg=20, sat=3.0, val=1.3)},
        body=dict(L=11.0, top_s=-5.4, top_h=-6.6, chest=8.4, waist=7.4, hip=9.4, sag=0.2, rear=16.0,
                  head_follow=0.3, k=0.16),
        leg=dict(h=5.2, fr=(1.8, 1.3, 1.0), hr=(2.6, 1.6, 1.1), digi=0.2, paw=(2.4, 1.0), hpaw=(4.4, 1.1),
                 thigh=1.1, far=(2.0, -2.0), knee=3.2, stride=22.0),
        neck=dict(r0=3.8, r1=3.4, base=(0.5, 2.4)),
        head=dict(dx=-5.4, dy=-3.8, cr=4.6, ml=2.6, md=3.6, mdrop=0.7, mtilt=9.0, jd=1.5, stop=0.4, taper=0.82),
        ear=dict(kind="point", h=3.6, w=3.2, lean=8.0, dx=1.2, dy=0.6, inner=True),
        tail=dict(len=23.0, a0=-64.0, bends=[-16.0, -24.0, -30.0, -30.0, -16.0], r=(2.0, 4.4, 2.8), widest=0.55,
                  dy=-0.6, z=-3),
        eye=dict(dx=-1.9, dy=-1.0, r=1.5, ring=("pale", 2)),
        teeth=dict(gnaw=dict(GNAW, len=1.6, w=0.45)),
        marks=[tail_tip(0.86),
               dict(on="torso", kind="below", line=(0.0, 0.6, 0.06), x=(-8.0, 8.0), ramp="tawny", above=-1.2)],
        whiskers=[((-5.0, 1.2), (-8.6, 0.2)), ((-5.0, 1.8), (-8.6, 2.8))],
        claws=True,
        action=dict(tilt=8.0, gape=0.0, tail=12.0, ear=-6.0),
        ow_side=dict(body=dict(rear=0.0)),
        ow_end=dict(head=2.3, tail_up=True),
        ow_face=[(0.0, 0.88, "enamel")],
    ),
    # Cynomys ludovicianus, the black-tailed prairie dog (living; MT), ~1 kg.
    # Real colours: cinnamon-tan grizzled back, paler buff belly, a pale eye
    # ring, a short tail with a black tip. Stocky ground squirrel with small
    # ears, short legs and strong digging claws, drawn in the upright sentinel
    # posture it uses to watch for predators (alarm calls: the dex).
    "cynomys": dict(
        ramps={
            "outline": ramp("2a1c12"),
            "fur": ramp("6a4c30", "93704a", "b89568", "d4b689"),
            "pale": ramp("c8b08c", "e2d0b0", "f6eedc"),
            "dark": ramp("241a14", "3c2c20"),
            "skin": ramp("9a6650"),
            "white": ramp("fbf8f0"),
            "enamel": ENAMEL,
        },
        front=1.36, back=1.4, icon=0.62,
        shiny={"fur": dict(deg=-6, sat=0.35, val=1.12), "pale": dict(deg=0, sat=0.4, val=1.04)},
        body=dict(L=11.0, top_s=-6.0, top_h=-6.8, chest=10.4, waist=10.4, hip=12.4, sag=-0.4, rump_w=1.15,
                  rear=56.0, rear_pivot=(0.6, 0.85), head_follow=-0.1, k=0.22),
        leg=dict(h=2.2, fr=(1.9, 1.4, 1.1), hr=(3.0, 1.8, 1.2), digi=0.0, paw=(2.2, 1.0), hpaw=(4.4, 1.2),
                 thigh=0.8, far=(1.6, -2.6), knee=3.2, hock=1.0, arms=(-1.8, 3.2, -1.8, 1.0), stride=20.0),
        neck=dict(r0=4.6, r1=4.2, base=(0.5, 2.6)),
        head=dict(dx=-4.6, dy=-3.4, cr=5.0, ml=2.4, md=3.8, mdrop=0.7, mtilt=8.0, jd=1.6, stop=0.4, taper=0.84),
        ear=dict(kind="round", h=2.4, w=2.8, lean=14.0, dx=1.6, dy=1.0, inner=False),
        tail=dict(len=6.5, a0=-6.0, bend=-12.0, r=(2.0, 2.1, 1.6), widest=0.4),
        eye=dict(dx=-1.8, dy=-1.0, r=1.4, ring=("pale", 1)),
        teeth=dict(gnaw=dict(GNAW, len=1.5, w=0.5)),
        marks=[tail_tip(0.62), dict(on="head", kind="above", line=(0.0, 9.0, 0.0), ramp="fur")],
        nose_ramp=("skin", 0),
        whiskers=[((-4.6, 1.4), (-8.0, 0.6)), ((-4.6, 2.0), (-8.0, 3.0))],
        claws=True,
        action=dict(tilt=14.0, gape=-14.0, tail=-30.0, ear=0.0),
        ow_side=dict(body=dict(rear=0.0), leg=dict(h=4.6, arms=None)),
        ow_end=dict(head=2.2, body=1.15),
        ow_face=[(0.0, 0.9, "enamel")],
    ),
}
