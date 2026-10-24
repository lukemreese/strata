"""Species specs for the ungulate body plan (plans/ungulate.py; the keys are
documented in plans/equid.py, whose engine draws them).

Colours of extinct species are reconstructions from living relatives and
habitat (noted per species); pronghorn and bighorn colours are real.
"""

from ..core.color import ramp
from ..plans.ungulate import FOOTPRINT_PAD


def tail_tip(f, ramp_="dark"):
    return dict(on="tail", kind="tip", f=f, ramp=ramp_)


def socks(h, ramp_="dark", legs="all"):
    return dict(on="legs", kind="socks", h=h, legs=legs, ramp=ramp_)


def head_ell(x, y, rx, ry, ramp_, deg=0):
    return dict(on="head", kind="ell", e=(x, y, rx, ry, deg), ramp=ramp_)


# The camel line's base palette: tawny, cream underside and muzzle.
CAMEL = {
    "outline": ramp("26180e"),
    "fur": ramp("6c4a2e", "946840", "b88a5a", "d4aa7a"),
    "pale": ramp("d0b896", "eee2cc"),
    "dark": ramp("2e2016", "4c3624"),
    "hoof": ramp("3a302a", "62564a"),
    "white": ramp("f8f2e6"),
}

SPECS = {
    # Diacodexis ilicis, Willwood Fm (~56 Ma), ~2 kg: the oldest artiodactyl,
    # rabbit-sized, with long slender hind legs (a bounding runner), a long
    # tail, small head with a short pointed snout and tiny hooves. Coat
    # speculative: grizzled agouti brown, cream belly and throat, dark tail tip
    # (forest-floor small mammals; cf. the chevrotain-like ancestors).
    "diacodexis": dict(
        ramps={
            "outline": ramp("24180f"),
            "fur": ramp("56402c", "7c5c3e", "9e7c58", "bc9c76"),
            "pale": ramp("ccb594", "ecdec4"),
            "dark": ramp("2c2018", "463428"),
            "hoof": ramp("34302c", "5c5248"),
            "white": ramp("f8f2e6"),
        },
        front=1.32, back=1.38, icon=0.64,
        shiny={"fur": dict(deg=-10, sat=1.3, val=1.05), "dark": dict(deg=0, sat=1.0, val=1.2)},
        body=dict(L=14.0, top_s=-5.0, top_h=-8.0, chest=7.8, waist=6.6, hip=9.0, sag=-1.4, k=0.26),
        leg=dict(h=10.5, fr=(2.0, 1.3, 0.8, 0.85), hr=(2.6, 1.6, 0.85, 0.85), pas=1.5, slope=0.5, hoof=(1.4, 1.0),
                 stifle=2.4, hock=2.6, hk=0.42, far=(2.4, -2.2), stride=20.0, arm=0.6),
        neck=dict(pts=[(0.5, 3.4), (-2.2, -0.6), (-3.4, -3.0)], r=[3.8, 3.2, 2.6]),
        head=dict(dx=-1.3, dy=-1.2, face=18.0, cr=3.0, ml=6.6, md=3.6, mt=1.8, drop=0.6, jaw=0.7),
        ear=dict(h=3.2, w=2.4, lean=16.0),
        eye=dict(dx=-0.8, dy=-0.6, r=1.15),
        tail=dict(len=12.0, a0=28.0, bend=12.0, r=(1.2, 1.2, 0.6), widest=0.3, dy=0.5),
        mouth=1.6, throat=0.2, fur_dashes=(3, 5),
        marks=[tail_tip(0.72), head_ell(-6.0, 0.6, 1.4, 1.2, "dark")],
        action=dict(tilt=14.0, neck=6.0, tail=-26.0, ear=-16.0),
        ow_end=dict(head=2.0, legs=0.9, face=1.1),
    ),
    # Leptomeryx, Brule Fm (~32 Ma), ~5 kg: a hornless chevrotain-like
    # ruminant. Hunched back with the rump high, slender legs, short neck, small
    # low-held head, short tail. Coat speculative after living chevrotains
    # (mouse-deer): dark brown with rows of pale spots and pale flank stripes,
    # white throat chevrons.
    "leptomeryx": dict(
        ramps={
            "outline": ramp("20140c"),
            "fur": ramp("4a3020", "6c4630", "8e6446", "ac8260"),
            "pale": ramp("c8b090", "ece0c8"),
            "dark": ramp("26180e", "3e2a1c"),
            "hoof": ramp("302a26", "585048"),
            "white": ramp("f6f0e4"),
        },
        front=1.3, back=1.36, icon=0.62,
        shiny={"fur": dict(deg=12, sat=0.7, val=1.25), "pale": dict(deg=0, sat=0.6, val=1.04)},
        body=dict(L=15.0, top_s=-5.0, top_h=-8.6, chest=8.8, waist=8.0, hip=10.0, sag=-2.0, k=0.28),
        leg=dict(h=9.0, fr=(1.9, 1.2, 0.75, 0.8), hr=(2.5, 1.5, 0.8, 0.8), pas=1.5, slope=0.5, hoof=(1.4, 1.0),
                 stifle=2.4, hock=2.2, hk=0.4, far=(2.4, -2.2), arm=0.5),
        neck=dict(pts=[(0.5, 3.4), (-2.4, 0.2), (-3.8, -1.6)], r=[3.8, 3.2, 2.7]),
        head=dict(dx=-1.4, dy=-1.0, face=32.0, cr=3.0, ml=7.0, md=3.8, mt=1.9, drop=0.5, jaw=0.75),
        ear=dict(h=3.0, w=2.6, lean=18.0),
        eye=dict(dx=-0.8, dy=-0.6, r=1.2),
        tail=dict(len=5.0, a0=60.0, bend=4.0, r=(1.2, 1.3, 0.8), widest=0.4, dy=0.3),
        mouth=1.6, throat=0.4,
        marks=[dict(on="torso", kind="spots", step=(3.0, 2.4), r=0.7, x=(-6.0, 10.0), above=-2.8, below=-7.0,
                    ramp="pale"),
               dict(on="torso", kind="below", line=(-6.0, -0.6, 0.06), x=(-4.0, 9.0), ramp="pale", above=-2.4),
               dict(on="neck", kind="ell", e=(-6.8, 0.6, 1.0, 2.6, 30), ramp="pale"),
               tail_tip(0.0, "fur")],
        belly=(0.5, 0.0),
        action=dict(tilt=-6.0, neck=-6.0, tail=-20.0, ear=-18.0),
        ow_end=dict(head=2.0, legs=0.85),
    ),
    # Cosoryx furcatus, Miocene Great Plains (~13-11 Ma), ~20 kg: a
    # merycodont, a small extinct relative of the pronghorn (a stand-in grade,
    # not its ancestor). Slender, long-legged, with permanent bony horns that
    # fork into two tines. Coat speculative: pronghorn-like cinnamon with a
    # white belly and pale rump (open-country countershading).
    "cosoryx": dict(
        ramps={
            "outline": ramp("24160c"),
            "fur": ramp("744a2a", "9a683c", "bc8854", "d6a874"),
            "pale": ramp("dccdb6", "f6f0e4"),
            "dark": ramp("2c1c12", "4a3020"),
            "horn": ramp("4e3e2e", "7a6650", "a8927a"),
            "hoof": ramp("302a26", "5a5048"),
        },
        front=1.22, back=1.28, icon=0.58,
        shiny={"fur": dict(deg=-4, sat=0.55, val=0.78), "horn": dict(deg=0, sat=0.6, val=0.9)},
        body=dict(L=16.5, top_s=-6.8, top_h=-7.2, chest=9.4, waist=7.8, hip=9.2, sag=0.0, k=0.28),
        leg=dict(h=12.5, fr=(2.0, 1.3, 0.75, 0.85), hr=(2.4, 1.5, 0.8, 0.85), pas=1.7, slope=0.6, hoof=(1.5, 1.1),
                 stifle=2.4, hock=2.2, far=(2.6, -2.4), arm=0.55),
        neck=dict(pts=[(0.5, 3.6), (-3.0, -1.6), (-4.6, -5.4)], r=[3.8, 3.0, 2.5]),
        head=dict(dx=-1.2, dy=-1.2, face=36.0, cr=2.9, ml=7.6, md=3.8, mt=2.0, drop=0.4, jaw=0.8),
        ear=dict(h=3.6, w=2.2, lean=22.0, dx=0.45),
        horns=[dict(base=(0.25 * 2.9, -0.8 * 2.9), pts=[(0, 0), (0.4, -2.4), (0.8, -3.8), (2.6, -5.8)],
                    r=[0.8, 0.7, 0.6, 0.38], far=(-1.6, 0.2),
                    end=[(0, 0), (0.3, -2.4), (0.6, -3.8), (1.8, -5.4)], end_r=[0.8, 0.7, 0.6, 0.4], spread=0.32),
               dict(base=(0.25 * 2.9, -0.8 * 2.9), pts=[(0.8, -3.8), (-0.5, -6.2)], r=[0.55, 0.36], far=(-1.6, 0.2),
                    end=[(0.6, -3.8), (0.0, -5.8)], end_r=[0.55, 0.36], spread=0.32)],
        eye=dict(dx=-0.8, dy=-0.6, r=1.15),
        tail=dict(len=4.5, a0=40.0, bend=4.0, r=(1.0, 1.2, 0.8), widest=0.4, dy=0.2),
        mouth=1.8, throat=0.0,
        marks=[dict(on="torso", kind="rump", e=(9.6, -2.6, 2.6, 3.6), ramp="pale"),
               tail_tip(0.0, "pale"),
               head_ell(-6.4, 0.2, 1.5, 1.2, "dark")],
        action=dict(tilt=16.0, neck=6.0, tail=-20.0, ear=-14.0),
        ow_end=dict(head=1.8, legs=0.8, horn=0.8),
        ow_ramps=dict(rump="pale", rump_w=0.55, chest="pale"),
    ),
    # Antilocapra americana, the pronghorn (living; MT), ~50 kg. Known colours:
    # tan-cinnamon back and flanks, white belly, rump patch and two white bands
    # across the throat, black horn sheaths with a forward prong, a dark nose
    # bridge and (bucks) a black cheek patch below the ear, a short dark mane.
    # Long slim legs, large eyes set high, short tail.
    "antilocapra": dict(
        ramps={
            "outline": ramp("22140a"),
            "fur": ramp("7a4a26", "a26a38", "c48a50", "dcaa70"),
            "pale": ramp("d8d0c0", "f6f2ea"),
            "dark": ramp("1e1610", "3a2c22"),
            "horn": ramp("1e1814", "3c322a"),
            "hoof": ramp("2c2622", "564c44"),
            "white": ramp("fcfaf4"),
        },
        front=1.12, back=1.18, icon=0.54,
        shiny={"fur": dict(deg=4, sat=0.35, val=1.08)},
        body=dict(L=19.0, top_s=-8.0, top_h=-8.0, chest=10.6, waist=8.6, hip=10.0, sag=0.2, k=0.28),
        leg=dict(h=15.0, fr=(2.3, 1.5, 0.8, 0.9), hr=(2.7, 1.7, 0.85, 0.9), pas=1.9, slope=0.6, hoof=(1.8, 1.3),
                 stifle=2.6, hock=2.4, far=(2.8, -2.6), arm=0.6),
        neck=dict(pts=[(0.5, 4.0), (-3.4, -2.0), (-5.0, -6.6)], r=[4.4, 3.3, 2.8]),
        mane=dict(r=0.8, off=0.95, ramp="dark"),
        head=dict(dx=-1.1, dy=-1.3, face=38.0, cr=3.2, ml=8.6, md=4.4, mt=2.4, drop=0.4, jaw=0.9),
        ear=dict(h=3.8, w=2.3, lean=24.0, dx=0.5),
        horns=[dict(base=(0.05 * 3.2, -0.8 * 3.2), pts=[(0, 0), (0.1, -3.0), (0.0, -5.4), (1.3, -6.8)],
                    r=[1.15, 1.0, 0.75, 0.45], far=(-1.6, 0.2),
                    end=[(0, 0), (0.2, -3.0), (0.0, -5.2), (-0.9, -6.4)], end_r=[1.0, 0.9, 0.7, 0.45], spread=0.3),
               dict(base=(0.05 * 3.2, -0.8 * 3.2), pts=[(0.1, -2.8), (-1.4, -3.7)], r=[0.8, 0.45], far=(-1.6, 0.2),
                    end=[(0.1, -2.6), (0.9, -3.3)], end_r=[0.7, 0.45], spread=0.3)],
        eye=dict(dx=-0.7, dy=-0.7, r=1.3),
        tail=dict(len=4.5, a0=36.0, bend=4.0, r=(1.0, 1.3, 0.9), widest=0.4, dy=0.2),
        mouth=1.8, throat=99.0,
        marks=[dict(on="torso", kind="rump", e=(11.0, -2.0, 3.2, 4.6), ramp="pale"),
               tail_tip(0.0, "pale"),
               dict(on="neck", kind="stripes", period=99.0, width=1.6, x=(-10.6, -9.0), lean=0.55, ramp="pale"),
               dict(on="neck", kind="stripes", period=99.0, width=1.5, x=(-8.0, -6.4), lean=0.55, ramp="pale"),
               head_ell(-6.2, -0.8, 3.0, 1.2, "dark", -4),     # dark nose bridge
               head_ell(1.6, 1.8, 1.4, 1.2, "dark"),          # cheek patch (bucks)
               head_ell(-2.0, 2.0, 3.4, 1.6, "pale", 6)],     # pale cheeks and jaw
        action=dict(tilt=14.0, neck=4.0, tail=-26.0, ear=-14.0),
        ow_end=dict(head=1.8, legs=0.72, horn=0.75),
        ow_ramps=dict(rump="pale", rump_w=0.6, chest="pale", throat="pale"),
    ),
    # Poebrotherium, Brule Fm (~32 Ma), ~30 kg: an early camelid, gazelle-
    # like: long slender legs ending in two small hooved toes (no pads yet),
    # a long neck, small head with a narrow muzzle, short tail. Coat
    # speculative: the camel line's tawny with a cream belly and muzzle.
    "poebrothere": dict(
        ramps=CAMEL,
        front=1.18, back=1.24, icon=0.56,
        shiny={"fur": dict(deg=0, sat=0.4, val=1.12)},
        body=dict(L=16.5, top_s=-7.0, top_h=-7.4, chest=9.4, waist=7.4, hip=9.0, sag=0.4, k=0.28),
        leg=dict(h=14.0, fr=(2.0, 1.3, 0.75, 0.85), hr=(2.4, 1.5, 0.8, 0.85), pas=1.8, slope=0.6, hoof=(1.5, 1.1),
                 stifle=2.4, hock=2.2, far=(2.6, -2.4), arm=0.5),
        neck=dict(pts=[(0.5, 3.4), (-3.0, -2.6), (-4.8, -8.8)], r=[3.8, 2.8, 2.3]),
        head=dict(dx=-1.0, dy=-1.2, face=26.0, cr=2.8, ml=7.8, md=3.6, mt=2.0, drop=0.4, jaw=0.75),
        ear=dict(h=2.8, w=2.2, lean=26.0, dx=0.45),
        eye=dict(dx=-0.7, dy=-0.6, r=1.1),
        tail=dict(len=5.5, a0=58.0, bend=4.0, r=(1.0, 1.2, 0.8), widest=0.4, dy=0.4),
        mouth=1.8, throat=0.0,
        marks=[head_ell(-6.6, 0.4, 1.8, 1.6, "pale"), tail_tip(0.6), socks(1.6, "fur")],
        action=dict(tilt=-12.0, neck=-6.0, tail=-14.0, ear=-14.0),
        ow_end=dict(head=1.9, neck=1.6, legs=0.85),
    ),
    # Procamelus grandis, Ashfall (~12 Ma), ~300 kg: llama-like, with a long
    # upright neck, long legs and padded feet with the toes splayed (an early
    # step towards living camels). No hump. Coat speculative: llama/guanaco
    # brown, cream belly and inner legs, slightly woolly.
    "procamelus": dict(
        ramps={**CAMEL,
               "fur": ramp("624028", "8a5c38", "ae7e52", "caa070")},
        front=1.02, back=1.08, icon=0.5,
        shiny={"fur": dict(deg=0, sat=0.35, val=1.18), "dark": dict(deg=0, sat=0.4, val=1.5)},
        body=dict(L=20.0, top_s=-8.0, top_h=-8.2, chest=11.0, waist=9.4, hip=10.4, sag=0.4, k=0.28),
        leg=dict(h=17.0, fr=(2.6, 1.7, 1.0, 1.0), hr=(3.0, 1.9, 1.0, 1.0), pas=2.0, slope=1.4, hoof=(3.0, 1.2),
                 foot="pad", stifle=2.8, hock=2.4, far=(3.0, -2.6), arm=0.6),
        neck=dict(pts=[(0.5, 3.6), (-3.0, -4.0), (-4.2, -12.0)], r=[4.6, 3.3, 2.8]),
        head=dict(dx=-1.0, dy=-1.2, face=14.0, cr=3.0, ml=8.4, md=4.0, mt=2.4, drop=0.5, jaw=0.85, chin=0.8),
        ear=dict(h=3.4, w=2.2, lean=18.0, dx=0.45),
        eye=dict(dx=-0.7, dy=-0.6, r=1.15),
        tail=dict(len=6.0, a0=60.0, bend=4.0, r=(1.2, 1.4, 0.9), widest=0.4, dy=0.4),
        mouth=2.0, throat=0.0, fur_dashes=(3, 4),
        marks=[head_ell(-7.2, 0.4, 2.0, 1.8, "pale"), tail_tip(0.5)],
        action=dict(tilt=10.0, neck=3.0, tail=-14.0, ear=-24.0),
        ow_end=dict(head=1.8, neck=2.0, legs=0.8),
        ow=dict(length=24),
        footprint=FOOTPRINT_PAD,
    ),
    # Camelops hesternus, the western camel (~20 ka), ~800 kg: larger than a
    # dromedary, long legs, long neck carried forward then up, long face, padded
    # feet. Whether it had a hump is unknown: none drawn (the cautious choice),
    # only a slight withers rise. Coat speculative: dromedary-like tawny.
    "camelops": dict(
        ramps={**CAMEL,
               "fur": ramp("70502e", "98703e", "bc9256", "d6b07a")},
        front=0.98, back=1.04, icon=0.48,
        shiny={"fur": dict(deg=-6, sat=0.6, val=0.72), "pale": dict(deg=0, sat=0.8, val=0.85)},
        body=dict(L=22.0, top_s=-10.0, top_h=-9.0, chest=12.5, waist=10.0, hip=11.0, sag=0.6, k=0.28,
                  hump=(4.0, 2.0, 5.0, 3.0)),
        leg=dict(h=18.0, fr=(3.0, 2.0, 1.15, 1.15), hr=(3.4, 2.2, 1.15, 1.15), pas=2.2, slope=1.6, hoof=(3.6, 1.4),
                 foot="pad", stifle=3.0, hock=2.6, far=(3.2, -2.8), arm=0.6),
        neck=dict(pts=[(0.5, 4.5), (-5.0, -1.0), (-7.4, -6.0), (-7.6, -10.0)], r=[5.4, 3.8, 3.2, 3.0]),
        head=dict(dx=-1.4, dy=-1.0, face=12.0, cr=3.4, ml=10.6, md=4.8, mt=3.0, drop=0.2, jaw=0.95, chin=1.0),
        ear=dict(h=3.0, w=2.4, lean=28.0, dx=0.5),
        eye=dict(dx=-0.7, dy=-0.7, r=1.2),
        tail=dict(len=8.0, a0=70.0, bend=3.0, r=(1.2, 1.3, 1.0), widest=0.4, dy=0.4),
        mouth=2.4, throat=0.0,
        marks=[head_ell(-9.0, 0.4, 2.2, 2.0, "pale"), tail_tip(0.55)],
        action=dict(tilt=12.0, neck=3.0, tail=-14.0, ear=-20.0),
        ow_end=dict(head=1.7, neck=1.7, legs=0.75),
        footprint=FOOTPRINT_PAD,
    ),
    # Merycoidodon, Brule Fm (~32 Ma), ~100 kg: an oreodont, a sheep-sized
    # herd animal with a short, deep, pig-like head (big canines, deep jaw),
    # short legs with four toes, a long tail. Coat speculative: grey-brown,
    # darker along the back, a dark face with a pale chin (living
    # peccary/pig-like pattern), no spots.
    "merycoidodon": dict(
        ramps={
            "outline": ramp("1c1612"),
            "fur": ramp("4a3c32", "6a5848", "8a7662", "a8947e"),
            "pale": ramp("b4a48e", "d8ccb6"),
            "dark": ramp("261e18", "3e322a"),
            "hoof": ramp("2c2622", "564c44"),
            "white": ramp("f0eadc"),
        },
        front=1.12, back=1.18, icon=0.54,
        shiny={"fur": dict(deg=-8, sat=1.5, val=1.05), "dark": dict(deg=-6, sat=1.3, val=1.1)},
        body=dict(L=20.0, top_s=-8.0, top_h=-8.6, chest=11.5, waist=11.0, hip=11.4, sag=0.4, k=0.28,
                  chest_w=1.05, rump_w=1.05),
        leg=dict(h=8.0, fr=(2.8, 2.0, 1.3, 1.3), hr=(3.2, 2.2, 1.3, 1.3), pas=1.6, slope=0.6, hoof=(2.0, 1.3),
                 toes=(3, 3), side=(0.5, 0.4), stifle=2.6, hock=2.0, kn=0.5, hk=0.45, far=(3.0, -2.6), stride=14.0),
        neck=dict(pts=[(0.5, 4.4), (-2.6, 0.6), (-4.2, -2.0)], r=[5.0, 4.6, 4.2]),
        head=dict(dx=-1.8, dy=-1.0, face=12.0, cr=4.0, ml=7.6, md=6.4, mt=4.6, drop=1.2, jaw=1.3, jx=0.2, jy=0.6),
        ear=dict(h=2.6, w=2.8, lean=40.0, dx=0.5),
        horns=[dict(base=(-7.6 + 4.6 / 2 + 1.6, -0.62 * 4.0 + 1.2 + 4.6 * 0.95), pts=[(0, 0), (-0.2, 1.4)],
                    r=[0.6, 0.35], ramp="white", far=(0.0, 0.0), end=[(0, 0), (0, 1.0)], end_r=[0.5, 0.3],
                    spread=0.25)],
        eye=dict(dx=-0.85, dy=-0.12, r=1.2, ring="pale"),
        tail=dict(len=13.0, a0=62.0, bend=4.0, r=(1.6, 1.4, 0.8), widest=0.3, dy=0.6),
        mouth=2.6, throat=0.2, fur_dashes=(3, 5),
        marks=[
               head_ell(-4.0, 3.2, 5.6, 1.8, "pale", 4), socks(3.0)],
        action=dict(tilt=10.0, neck=3.0, tail=-14.0, ear=-12.0),
        ow_end=dict(head=1.7, body=1.1, legs=1.1, face=1.2, muzzle=1.3),
        ow_ramps=dict(muzzle="pale"),
    ),
    # Ovis canadensis, the bighorn (living; Natural Trap Cave fossils), ~100 kg
    # ram. Known colours: brown coat, white rump patch, white muzzle and eye
    # ring, white backs of the legs and belly, short dark tail; massive curled
    # horns with growth rings. Stocky, sure-footed, roman-nosed.
    "ovis": dict(
        ramps={
            "outline": ramp("20160e"),
            "fur": ramp("5a4230", "7e5e42", "9e7c5a", "ba9a76"),
            "pale": ramp("d8ceba", "f4eee2"),
            "dark": ramp("2a1e16", "463426"),
            "horn": ramp("6a5640", "927a5c", "b8a07e", "d4c0a0"),
            "hoof": ramp("2c2622", "564c44"),
        },
        front=1.1, back=1.16, icon=0.53,
        shiny={"fur": dict(deg=6, sat=0.45, val=1.3), "horn": dict(deg=0, sat=0.6, val=1.08)},
        body=dict(L=19.0, top_s=-8.6, top_h=-8.6, chest=12.4, waist=11.0, hip=11.6, sag=0.3, k=0.28, chest_w=1.05),
        leg=dict(h=11.5, fr=(2.8, 1.9, 1.05, 1.05), hr=(3.2, 2.1, 1.05, 1.05), pas=1.8, slope=0.6, hoof=(1.9, 1.3),
                 stifle=2.8, hock=2.2, far=(3.0, -2.6), arm=0.7),
        neck=dict(pts=[(0.5, 4.4), (-3.0, -0.8), (-4.8, -3.6)], r=[5.4, 4.6, 4.0]),
        head=dict(dx=-1.4, dy=-1.4, face=30.0, cr=3.6, ml=8.4, md=5.0, mt=3.0, drop=-0.2, jaw=0.95),
        ear=dict(h=2.8, w=2.2, lean=40.0, dx=0.6, dy=-0.2),
        horns=[dict(kind="curl", base=(0.0, -0.78 * 3.6), R=(4.6, 2.6), a=(-140.0, 175.0), thick=(2.3, 0.7),
                    n=12, rings=7, far=(-1.2, -0.3), behind=False)],
        eye=dict(dx=-0.6, dy=-0.55, r=1.2, ring="pale"),
        tail=dict(len=4.0, a0=56.0, bend=4.0, r=(1.2, 1.4, 1.0), widest=0.4, dy=0.4),
        mouth=1.9, throat=0.0,
        marks=[dict(on="torso", kind="rump", e=(10.2, -1.8, 3.0, 4.6), ramp="pale"),
               dict(on="legs", kind="below", line=(9.0, -99.0, 0.0), x=(10.6, 99.0), ramp="pale"),
               tail_tip(0.0, "dark"),
               head_ell(-6.8, 0.6, 2.4, 2.4, "pale")],
        action=dict(tilt=-14.0, neck=-6.0, tail=-14.0, ear=-8.0),
        ow_end=dict(head=1.75, horn=0.85),
        ow_ramps=dict(rump="pale", rump_w=0.6, muzzle="pale"),
    ),
}
