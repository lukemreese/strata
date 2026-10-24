"""Species specs for the rhino_brontothere body plan (plans/rhino_brontothere.py;
the keys are documented in plans/hoofed_giant.py, whose engine it uses).
Owned by the giant-lane artist. See specs/fish.py for the common keys.

Rhino-line family look: tall tubular ears with dark rims and pale insides, a
pale upper lip and chin, three-toed feet with pale nails, skin folds behind
the shoulder and before the thigh. Skin and hair colours of these extinct
rhinos are reconstructions from living rhinos and tapirs (noted per species).
"""

from ..core.color import ramp
from ..plans.hoofed_giant import FOOTPRINTS


def ear_rim(v, ramp_="dark"):
    """Dark ear tips above head-relative y = v."""
    return dict(on="ear", kind="above", line=(0.0, v, 0.0), ramp=ramp_)


def head_ell(cx, cy, rx, ry, ramp_, deg=0):
    return dict(on="head", kind="ell", e=(cx, cy, rx, ry, deg), ramp=ramp_)


def socks(h, ramp_="dark"):
    return dict(on="legs", kind="socks", h=h, ramp=ramp_)


def folds(xs, xh, top, bottom, k=1.0):
    """The rhino skin folds: behind the shoulder and in front of the thigh."""
    return [dict(on="body", pts=[(xs + 5.0 * k, top + 1.0), (xs + 4.0 * k, (top + bottom) / 2),
                                 (xs + 4.6 * k, bottom)]),
            dict(on="body", pts=[(xh - 4.0 * k, top + 1.5), (xh - 5.0 * k, (top + bottom) / 2 + 1.0),
                                 (xh - 4.4 * k, bottom)])]


# end-on face: a pale upper lip under the long snout
RHINO_FACE = [dict(kind="ell", e=(0.0, 1.0, 0.36, 0.16), ramp="pale", z=3.4, line=False)]

SPECS = {
    # Hyrachyus modestus, Bridger Fm (~50-46 Ma), ~70 kg, 1.5 m: a lightly
    # built, hornless, tapir-sized rhinocerotoid (stand-in grade for the
    # line's start). Slender legs, a long low head, a moderate tail. Coat
    # speculative: short warm grey-brown hair with a paler belly, as in a
    # forest browser; the rhino-line points (dark ear rims, pale lips, socks).
    "hyrachyus": dict(
        ramps={
            "outline": ramp("1e1614"),
            "fur": ramp("3e3028", "5e4a3e", "806858", "a08872"),
            "pale": ramp("a08c78", "c6b49e", "e2d6c2"),
            "dark": ramp("221a16", "3a2e28"),
            "hoof": ramp("2a2220", "8a7c70"),
            "skin": ramp("7a4440"),
        },
        front=1.25, back=1.3, icon=0.62,
        shiny={"fur": dict(deg=-8, sat=1.5, val=1.1), "pale": dict(deg=0, sat=0.8, val=1.05)},
        body=dict(L=19.0, top_s=-8.0, top_h=-9.6, chest=11.0, waist=9.5, hip=11.0, sag=0.8, rump_w=1.05),
        leg=dict(h=10.0, fr=(2.4, 1.5, 1.3), hr=(2.9, 1.6, 1.3), fx=2.0, hx=0.5, far=(2.5, -2.0),
                 elbow=0.8, knee=2.4, hock=2.2, wrist=0.28, hockh=0.42, thigh=0.5, stride=18.0,
                 foot=dict(kind="pad", l=3.2, h=1.6, nails=2)),
        neck=dict(r0=4.4, r1=3.8, base=(0.0, 3.0)),
        head=dict(dx=-8.0, dy=1.0, cr=4.4, cw=1.15, chh=0.85, ml=6.4, md=3.8, mdrop=0.4, mtilt=20.0,
                  taper=0.74, jd=1.8, lumps=[(1.0, -2.4, 2.4, 1.5, -10), (-7.6, 0.2, 1.8, 1.0, -18)]),
        ear=dict(kind="leaf", h=5.0, w=2.6, lean=14.0, dx=1.4, dy=0.3),
        tail=dict(len=7.0, a0=72.0, bend=3.0, r=(1.2, 0.9, 0.6), widest=0.2),
        eye=dict(dx=-1.8, dy=-0.2, r=0.95),
        marks=[ear_rim(-6.8), socks(3.5), dict(on="jaw", kind="below", line=(0.0, -99.0, 0.0), x=(-6.0, 99.0), ramp="fur")],
        wrinkles=[],
        action=dict(tilt=12.0, gape=-14.0, ear=-20.0, tail=-15.0),
        ow_end=dict(head=1.9, ear=1.0, ear_angle=32.0, head_dy=0.0, muzzle=0.7, muzzle_dy=0.6, legs=1.2, eyes=0.62),
        ow_ramps=dict(muzzle="fur"),
        ow_extras=dict(south=RHINO_FACE),
        footprint=FOOTPRINTS["rhino"],
    ),
    # Subhyracodon, Brule Fm (~32 Ma), ~500 kg, 2.5 m: a hornless, cow-sized
    # rhino with a pair of low rugose ridges at the tip of the nasals.
    # Moderately long legs, three-toed feet. Skin speculative: grey-brown,
    # sparsely haired, after living rhinos; rhino-line points.
    "subhyracodon": dict(
        ramps={
            "outline": ramp("1c1816"),
            "fur": ramp("3c3430", "5c524a", "7e7268", "9e9286"),
            "pale": ramp("a09486", "c4b8a8", "e0d6c8"),
            "dark": ramp("221c1a", "38302c"),
            "hoof": ramp("2c2622", "8a8076"),
            "skin": ramp("7a4844"),
        },
        front=1.02, back=1.04, icon=0.51,
        shiny={"fur": dict(deg=10, sat=1.8, val=1.12), "pale": dict(deg=4, sat=1.2, val=1.04)},
        body=dict(L=24.0, top_s=-13.0, top_h=-12.0, chest=16.5, waist=14.5, hip=14.5, sag=0.8, paunch=1.2,
                  hump=(3.0, 1.5, 6.0, 3.0)),
        leg=dict(h=8.0, fr=(4.2, 2.9, 2.7), hr=(4.6, 3.0, 2.7), fx=2.2, hx=0.5, far=(3.0, -2.5),
                 elbow=0.8, knee=2.2, hock=1.8, wrist=0.28, hockh=0.4, thigh=0.5, stride=15.0,
                 foot=dict(kind="pad", l=4.4, h=2.1, nails=3)),
        neck=dict(r0=6.0, r1=5.2, base=(0.0, 4.0)),
        head=dict(dx=-10.5, dy=2.5, cr=5.6, cw=1.2, chh=0.85, ml=7.4, md=5.0, mdrop=0.5, mtilt=22.0,
                  taper=0.78, jd=2.2, lumps=[(1.4, -3.0, 3.0, 1.9, -10), (-9.6, 0.2, 2.4, 1.4, -20)]),
        ear=dict(kind="leaf", h=6.0, w=3.0, lean=14.0, dx=1.8, dy=0.4),
        tail=dict(len=7.0, a0=75.0, bend=3.0, r=(1.4, 1.0, 0.8), widest=0.2),
        eye=dict(dx=-2.2, dy=0.0, r=1.0),
        marks=[ear_rim(-8.6), socks(3.0), dict(on="jaw", kind="below", line=(0.0, -99.0, 0.0), x=(-6.0, 99.0), ramp="fur")],
        wrinkles=folds(-12.0, 12.0, -11.0, -1.0),
        extras=[dict(kind="ell", on="head", e=(-12.0, 2.2, 1.3, 0.8, -10), ramp="fur", z=3.35, light=0.15)],
        action=dict(tilt=14.0, gape=-14.0, ear=-20.0, tail=-15.0),
        ow_end=dict(head=1.7, ear=1.0, ear_angle=32.0, head_dy=0.05, muzzle=0.75, muzzle_dy=0.6, legs=1.0, eyes=0.64),
        ow_ramps=dict(muzzle="fur"),
        ow_extras=dict(south=RHINO_FACE),
        footprint=FOOTPRINTS["rhino"],
    ),
    # Teleoceras major, Ashfall Fossil Beds (~11.9 Ma), ~1.8 t, 4 m: a
    # barrel-bodied, very short-legged rhino, hippo-like and probably
    # semi-aquatic or a grazer near water, with a small conical horn at the tip
    # of the nose (larger in males). Skin speculative: grey with darker legs,
    # mud-dulled, after living rhinos. Frame 2: head up, a bellow.
    # Variant: a browner, mud-red morph.
    "teleoceras": dict(
        ramps={
            "outline": ramp("181616"),
            "fur": ramp("383434", "56504e", "766f6a", "968e88"),
            "pale": ramp("9a9088", "beb4aa", "dcd4ca"),
            "dark": ramp("1e1a1a", "302b2a"),
            "hoof": ramp("2a2624", "88807a"),
            "horn": ramp("5a4e42", "a89a84"),
            "skin": ramp("7a4846"),
        },
        front=0.92, back=0.94, icon=0.46,
        shiny={"fur": dict(deg=18, sat=2.6, val=1.08), "pale": dict(deg=10, sat=1.4, val=1.02)},
        body=dict(L=25.0, top_s=-14.5, top_h=-13.5, chest=19.5, waist=19.0, hip=18.0, sag=1.2, paunch=3.0,
                  chest_w=1.05, rump_w=1.05, hump=(3.0, 1.5, 7.0, 3.0)),
        leg=dict(h=4.5, fr=(5.0, 4.2, 4.0), hr=(5.4, 4.2, 4.0), fx=2.6, hx=0.0, far=(3.5, -3.0),
                 elbow=0.4, knee=1.2, hock=0.6, wrist=0.2, hockh=0.3, thigh=0.5, stride=10.0,
                 foot=dict(kind="pad", l=6.0, h=2.4, nails=3)),
        neck=dict(r0=7.2, r1=6.4, base=(0.0, 4.5)),
        head=dict(dx=-11.0, dy=4.0, cr=7.0, cw=1.2, chh=0.85, ml=8.0, md=6.4, mdrop=0.6, mtilt=22.0,
                  taper=0.8, jd=2.6, lumps=[(1.6, -3.6, 3.6, 2.2, -10), (-13.2, 1.6, 3.0, 1.8, -20)]),
        ear=dict(kind="leaf", h=6.6, w=3.2, lean=16.0, dx=2.2, dy=0.4),
        tail=dict(len=7.0, a0=78.0, bend=3.0, r=(1.6, 1.2, 1.0), widest=0.2),
        eye=dict(dx=-2.6, dy=0.0, r=1.05),
        marks=[ear_rim(-10.0), socks(3.0), dict(on="jaw", kind="below", line=(0.0, -99.0, 0.0), x=(-6.0, 99.0), ramp="fur")],
        wrinkles=folds(-15.5, 15.5, -11.0, 1.0, 1.3) + [dict(on="head", pts=[(3.8, -1.0), (5.0, 2.0), (4.4, 5.0)])],
        extras=[dict(kind="facet", on="head", pts=[(-16.8, 2.4), (-12.6, 1.0), (-14.8, -3.0), (-15.8, -3.2)], ramp="horn", z=3.4)],
        action=dict(tilt=16.0, gape=-16.0, ear=-24.0, tail=-10.0),
        ow=dict(size=64, end_zoom=1.45),
        ow_end=dict(head=1.6, ear=1.0, ear_angle=32.0, head_dy=0.15, muzzle=0.85, muzzle_dy=0.6, legs=0.6, eyes=0.66, body=1.1),
        ow_ramps=dict(muzzle="fur"),
        ow_extras=dict(south=RHINO_FACE + [dict(kind="facet", pts=[(-0.2, 0.42), (0.2, 0.42), (0.04, -0.12), (-0.04, -0.12)], ramp="horn", z=3.5)]),
        footprint=FOOTPRINTS["rhino"],
    ),
    # Aphelops, Ashfall Fossil Beds (~11.9 Ma), ~1.5 t, 3 m: a hornless,
    # long-legged rhino with retracted nasals and a pointed, prehensile
    # browsing upper lip, living in drier, more open country than Teleoceras.
    # Skin speculative: paler, dust-coloured grey-brown; rhino-line points.
    "aphelops": dict(
        ramps={
            "outline": ramp("1e1a16"),
            "fur": ramp("463c34", "685a4e", "8c7c6c", "ac9c8a"),
            "pale": ramp("ae9e8a", "ccbea8", "e6dccc"),
            "dark": ramp("241e1a", "3c322c"),
            "hoof": ramp("2c2622", "908476"),
            "skin": ramp("7a4844"),
        },
        front=0.95, back=0.96, icon=0.47,
        shiny={"fur": dict(deg=0, sat=0.35, val=1.18), "pale": dict(deg=0, sat=0.4, val=1.05)},
        body=dict(L=26.0, top_s=-15.0, top_h=-14.0, chest=17.0, waist=15.0, hip=15.5, sag=0.8, paunch=0.8,
                  chest_w=1.0, rump_w=1.0, hump=(3.0, 1.5, 6.0, 3.0)),
        leg=dict(h=13.0, fr=(4.0, 2.8, 2.6), hr=(4.5, 2.9, 2.6), fx=2.4, hx=0.5, far=(3.0, -2.5),
                 elbow=0.8, knee=2.2, hock=1.8, wrist=0.28, hockh=0.4, thigh=0.5, stride=15.0,
                 foot=dict(kind="pad", l=5.0, h=2.2, nails=3)),
        neck=dict(r0=6.6, r1=5.8, base=(0.0, 4.5)),
        head=dict(dx=-11.0, dy=2.0, cr=6.2, cw=1.2, chh=0.84, ml=7.4, md=5.0, mdrop=0.4, mtilt=28.0,
                  taper=0.7, jd=2.2, lumps=[(1.4, -3.2, 3.2, 2.0, -10), (-14.0, 7.3, 1.9, 1.3, -35)]),
        ear=dict(kind="leaf", h=6.4, w=3.0, lean=12.0, dx=2.0, dy=0.4),
        tail=dict(len=8.0, a0=76.0, bend=3.0, r=(1.5, 1.1, 0.8), widest=0.2),
        eye=dict(dx=-2.4, dy=0.0, r=1.05),
        marks=[ear_rim(-9.6), socks(3.0), dict(on="jaw", kind="below", line=(0.0, -99.0, 0.0), x=(-6.0, 99.0), ramp="fur")],
        wrinkles=folds(-13.0, 13.0, -14.0, -1.0, 1.1),
        extras=[],
        action=dict(tilt=18.0, gape=-12.0, ear=-24.0, tail=-15.0),
        ow=dict(size=64, end_zoom=1.45),
        ow_end=dict(head=1.6, ear=1.0, ear_angle=32.0, head_dy=0.0, muzzle=0.7, muzzle_dy=0.62, legs=1.1, eyes=0.64),
        ow_ramps=dict(muzzle="fur"),
        ow_extras=dict(south=RHINO_FACE),
        footprint=FOOTPRINTS["rhino"],
    ),
}
