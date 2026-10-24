"""Species specs for the proboscidean body plan (plans/proboscidean.py; the keys
are documented in plans/hoofed_giant.py, whose engine it uses). Owned by the
giant-lane artist. See specs/fish.py for the common keys."""

from ..core.color import ramp
from ..plans.hoofed_giant import FOOTPRINTS

SPECS = {
    # Mammuthus columbi, Natural Trap Cave (~20 ka), ~9 t, ~4 m at the shoulder:
    # the Columbian mammoth. A high single dome on the head, the shoulders the
    # highest point and the back sloping down to the hips, pillar legs, long
    # tusks curving out, down, forward and up again, a long trunk, small ears
    # and a short tufted tail. Less woolly than the woolly mammoth: drawn with
    # sparse brown hair, darker on the dome, shoulders and belly fringe
    # (speculative, from frozen woolly mammoth hair and its warmer range).
    # Frame 2: head up, trunk raised to trumpet. Variant: a paler, ginger morph
    # (light hair is known from woolly mammoth DNA, MC1R).
    "mammuthus": dict(
        ramps={
            "outline": ramp("1c1410"),
            "fur": ramp("3e2e24", "5e4636", "806250", "a0826a"),
            "hair": ramp("261a14", "3c2a20", "56402e"),
            "tusk": ramp("8a7a60", "c8b898", "ece2cc"),
            "pale": ramp("b49c82"),
            "hoof": ramp("2e241e", "a89880"),
            "skin": ramp("7a4440"),
        },
        front=0.8, back=0.84, icon=0.4,
        shiny={"fur": dict(deg=6, sat=1.5, val=1.35), "hair": dict(deg=8, sat=1.7, val=1.9)},
        body=dict(L=26.0, top_s=-22.0, top_h=-15.0, chest=22.0, waist=18.0, hip=16.0, sag=0.0, paunch=1.0,
                  chest_w=1.0, rump_w=0.95, hump=(3.0, 1.5, 9.0, 6.0)),
        leg=dict(h=16.0, fr=(5.4, 4.4, 4.2), hr=(5.6, 4.3, 4.1), fx=3.0, hx=0.5, far=(3.5, -3.0),
                 elbow=0.4, knee=1.0, hock=0.6, wrist=0.25, hockh=0.3, thigh=0.4, stride=10.0,
                 foot=dict(kind="pad", l=7.4, h=2.6, nails=3)),
        neck=dict(r0=9.0, r1=8.0, base=(-1.0, 6.0)),
        head=dict(dx=-9.5, dy=-2.0, cr=8.0, cw=0.95, chh=1.05, ml=2.0, md=6.4, mdrop=0.0, mtilt=72.0,
                  taper=0.8, jd=2.4, lumps=[(1.0, -6.4, 5.8, 4.6, 10)]),
        ear=dict(kind="round", h=6.0, w=4.6, lean=12.0, dx=1.6, dy=9.0, inner=False),
        tail=dict(len=9.0, a0=80.0, bend=2.0, r=(1.4, 1.0, 1.6), widest=0.2),
        eye=dict(dx=-3.4, dy=0.6, r=1.1),
        marks=[dict(on="head", kind="above", line=(0.0, -6.0, 0.15), ramp="hair"),
               dict(on="torso", kind="ell", e=(-16.0, -26.0, 12.0, 8.0, 10), ramp="hair"),
               dict(on="tail", kind="tip", f=0.6, ramp="hair"),
               dict(on=("head", "jaw"), kind="below", line=(0.0, -99.0, 0.0), ramp="fur")],
        belly=(99.0, 0.0), throat=(99.0, 0.0),
        hair=dict(ramps=("hair", "fur"), period=4, run=2),
        extras=[
            # trunk: hangs almost to the ground, the tip curled forward; raised to trumpet in frame 2
            dict(kind="tube", on="head", pts=[(-5.5, 6.0), (-7.0, 14.0), (-7.4, 22.0), (-7.0, 28.0), (-8.4, 32.0),
                                              (-10.4, 31.4)],
                 radii=[3.4, 2.8, 2.3, 1.9, 1.5, 1.2], ramp="fur", z=3.3,
                 alt=dict(pts=[(-5.5, 6.0), (-9.0, 11.5), (-14.0, 10.5), (-17.4, 5.0), (-17.8, -0.5),
                               (-16.0, -3.4)])),
            # tusks: out, down, forward and up again; the far one behind the trunk
            dict(kind="tube", on="head", pts=[(-4.0, 8.0), (-7.0, 14.0), (-12.0, 18.0), (-18.0, 17.0), (-21.0, 12.0),
                                              (-20.0, 7.0)],
                 radii=[1.9, 1.8, 1.6, 1.3, 1.0, 0.6], ramp="tusk", z=3.5, far=(2.5, -1.2), far_z=2.95),
            # sparse hair fringe under the chest and belly
            dict(kind="fringe", on="body", top=[(-17.0, -6.0), (-4.0, -4.0), (8.0, -4.0)],
                 bottom=[(-17.0, -3.0), (-4.0, -1.5), (8.0, -2.0)], teeth=6, depth=1.8, r=1.4, ramp="hair",
                 z=0.5),
        ],
        action=dict(tilt=10.0, gape=-10.0, ear=-8.0, tail=-10.0),
        ow=dict(size=64, end_zoom=1.4),
        ow_end=dict(head=1.3, ear=1.1, head_dy=-0.2, muzzle=0.6, muzzle_dy=0.6, legs=1.15, eyes=0.5,
                    hump=0.6),
        ow_ramps=dict(muzzle="fur"),
        ow_chest_pale=False,
        ow_extras=dict(
            south=[dict(kind="tube", pts=[(0.0, 0.35), (0.0, 1.0), (0.04, 1.5), (0.18, 1.78)],
                        radii=[0.36, 0.3, 0.24, 0.19], ramp="fur", z=3.6, inner="outline"),
                   dict(kind="tube", pts=[(0.3, 0.6), (0.55, 1.15), (0.95, 1.42), (1.25, 1.2), (1.32, 0.8)],
                        radii=[0.19, 0.18, 0.15, 0.12, 0.08], ramp="tusk", z=3.7, mirror=True),
                   dict(kind="ell", e=(0.0, -0.95, 0.62, 0.3), ramp="hair", z=3.05, line=False)],
            north=[dict(kind="ell", e=(0.0, -0.75, 0.75, 0.5), ramp="hair", z=-0.3),
                   dict(kind="tube", pts=[(1.0, 1.35), (1.25, 1.2), (1.32, 0.8)], radii=[0.14, 0.11, 0.08],
                        ramp="tusk", z=-0.6, mirror=True)]),
        footprint=FOOTPRINTS["pad"],
    ),
}
