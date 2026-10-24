"""Species specs for the canid body plan (plans/canid.py, which documents the
keys). Owned by the carnivore artist. See specs/fish.py for the common keys.

Family look of the dog line (shared with Protictis and Miacis in
specs/carnivoran.py): pointed ears with dark tips, pale muzzle/lips/throat/chest,
a dark tear streak from the eye, a dark tail tip; the early forest forms add
dark socks, spots and tail rings, which fade out along the line (Protictis
spotted and ringed, Miacis ringed, Hesperocyon faintly ringed, Leptocyon plain).
Coat colours of extinct species are reconstructions from living canids and
habitat (noted per species); coyote and swift fox colours are real.
"""

from ..core.color import ramp

# The dog-line base palette: agouti brown, cream underside, charcoal points.
DOG_RAMPS = {
    "outline": ramp("2a1d18"),
    "fur": ramp("5c4130", "86613f", "a8845a", "c8a878"),
    "pale": ramp("b39a7a", "d8c4a0", "f2e6cc"),
    "dark": ramp("2e2420", "4c3b30"),
    "skin": ramp("7a3c38"),
    "white": ramp("f8f4e8"),
}

TEAR = ((-3.2, 0.3), (-5.4, 2.4))


def socks(h, legs="all", ramp_="dark"):
    return dict(on="legs", kind="socks", h=h, legs=legs, ramp=ramp_)


def tail_tip(f, ramp_="dark"):
    return dict(on="tail", kind="tip", f=f, ramp=ramp_)


def ear_tip(v=-2.5, ramp_="dark"):
    """Dark ear tips: the part of the ear above head-relative y = v - 4.5."""
    return dict(on="ear", kind="above", line=(0, v - 4.5, 0.0), ramp=ramp_)


def rings(*bands, ramp_="dark"):
    return dict(on="tail", kind="rings", bands=list(bands), ramp=ramp_)


SPECS = {
    # Hesperocyon gregarius, White River Gp (~37-34 Ma), ~2 kg, ~80 cm with tail.
    # The earliest canid: long, low body, short legs, long tail, semi-digitigrade
    # feet; fox-sized skull with a moderate muzzle. Described as civet-like, so a
    # forest-edge agouti coat with faint tail rings (speculative), plus the
    # dog-line points (ear tips, tear streak, socks, tail tip).
    "hesperocyon": dict(
        ramps=DOG_RAMPS,
        front=0.9, back=0.92, icon=0.45,
        shiny={"fur": dict(deg=8, sat=0.55, val=1.05), "dark": dict(deg=0, sat=0.6, val=1.25)},
        body=dict(L=19.0, top_s=-7.0, top_h=-7.0, chest=11.0, waist=9.0, hip=10.0, sag=0.6),
        leg=dict(h=8.0, fr=(2.4, 1.6, 1.2), hr=(2.7, 1.7, 1.2), digi=0.6, paw=(3.0, 1.15), thigh=0.9),
        neck=dict(r0=4.6, r1=3.8, base=(0.5, 3.0)),
        head=dict(dx=-8.0, dy=-6.0, cr=5.4, ml=5.6, md=4.4, mdrop=0.4, mtilt=4.0, jd=2.2, stop=0.6),
        ear=dict(kind="point", h=5.0, w=4.4, lean=14.0),
        tail=dict(len=22.0, a0=20.0, bend=-14.0, r=(2.4, 2.6, 1.2), widest=0.4),
        eye=dict(dx=-2.6, dy=-0.9, r=1.4, line=TEAR),
        ow_end=dict(head=2.3),
        marks=[socks(2.6), tail_tip(0.86), rings((0.36, 0.46), (0.6, 0.7)), ear_tip()],
    ),
    # Leptocyon, Ogallala Gp (~12 Ma), ~2 kg: the fox-sized stem of the living
    # dogs (Canini and Vulpini). Slender, longer-legged than Hesperocyon, long
    # narrow muzzle, large ears, a fuller tail. Coat speculative: a plain grey-
    # fawn fox pattern for open woodland, the spots and rings of the forest
    # ancestors gone; dark socks, ear tips and tail tip kept as family marks.
    "leptocyon": dict(
        ramps={
            "outline": ramp("261c1a"),
            "fur": ramp("5e4a3c", "88705a", "ac9476", "ccb898"),
            "pale": ramp("b8a48a", "dccab0", "f4eadc"),
            "dark": ramp("2c2422", "4a3c34"),
            "skin": ramp("7a3c38"),
            "white": ramp("f8f4e8"),
        },
        front=0.92, back=0.95, icon=0.46,
        shiny={"fur": dict(deg=-6, sat=1.6, val=1.04), "pale": dict(deg=-4, sat=1.2, val=1.0)},
        body=dict(L=18.0, top_s=-8.0, top_h=-8.0, chest=10.5, waist=7.5, hip=9.0, sag=0.4),
        leg=dict(h=11.0, fr=(2.2, 1.4, 1.1), hr=(2.6, 1.5, 1.1), digi=0.9, paw=(2.8, 1.1), thigh=0.85),
        neck=dict(r0=4.2, r1=3.4, base=(0.5, 3.0)),
        head=dict(dx=-7.5, dy=-6.0, cr=5.0, ml=6.6, md=3.8, mdrop=0.4, mtilt=5.0, jd=1.9, stop=0.5, taper=0.6),
        ear=dict(kind="point", h=6.2, w=4.6, lean=12.0),
        tail=dict(len=20.0, a0=48.0, bend=-6.0, r=(2.0, 3.0, 1.3), widest=0.55),
        eye=dict(dx=-2.4, dy=-0.9, r=1.35, line=TEAR),
        marks=[socks(3.2), tail_tip(0.82), ear_tip()],
    ),
    # Epicyon haydeni, Ogallala Gp (~12-6 Ma), ~120 kg: the largest canid, a
    # borophagine bone-cracker. Massive head with a short, deep muzzle, domed
    # forehead (big jaw muscles), heavy forequarters, back sloping slightly to
    # the hips, relatively short tail. Coat speculative: dusky brown with faint
    # spotting by analogy with hyenas (convergent bone-crackers), keeping the
    # dog-line pale throat, ear tips, tear streak and dark tail tip.
    "epicyon": dict(
        ramps={
            "outline": ramp("231916"),
            "fur": ramp("4e382a", "735440", "967358", "b69878"),
            "pale": ramp("a68e72", "ccb696", "e8dcc4"),
            "dark": ramp("2a201c", "44352c"),
            "skin": ramp("7a3c38"),
            "white": ramp("f6f0e2"),
            "eye": ramp("a8782c"),
        },
        front=0.9, back=0.95, icon=0.46,
        shiny={"fur": dict(deg=-10, sat=0.7, val=0.78), "pale": dict(deg=0, sat=0.6, val=0.85)},
        body=dict(L=20.0, top_s=-11.0, top_h=-7.5, chest=15.0, waist=11.0, hip=11.5, sag=0.4,
                  chest_w=1.05, hump=(3.0, 3.5, 7.0, 5.0)),
        leg=dict(h=10.0, fr=(3.4, 2.3, 1.8), hr=(3.2, 2.1, 1.6), digi=0.85, paw=(3.8, 1.6), thigh=1.0,
                 far=(3.0, -2.5)),
        neck=dict(r0=6.0, r1=5.0, base=(0.0, 4.0)),
        head=dict(dx=-8.0, dy=-3.0, cr=6.6, cw=1.0, ml=3.6, md=6.2, mdrop=0.8, mtilt=8.0, jd=3.2, stop=1.2,
                  cheek=0.9, taper=0.8),
        ear=dict(kind="point", h=4.6, w=4.4, lean=18.0),
        tail=dict(len=15.0, a0=62.0, bend=-4.0, r=(2.8, 2.9, 1.6), widest=0.5),
        eye=dict(dx=-3.4, dy=-1.4, r=1.45, iris="eye", line=((-4.2, -0.2), (-6.0, 2.4))),
        marks=[tail_tip(0.75), ear_tip(-1.8),
               dict(on="torso", kind="spots", step=(4.5, 4.0), r=0.9, above=-1.5, x=(-9.0, 14.0), ramp="dark")],
        action=dict(tilt=4.0, gape=-18.0, tail=-10.0),
        teeth=dict(canine=2.0),
    ),
    # Aenocyon dirus, Natural Trap Cave (~20 ka), ~65 kg: the dire wolf, a
    # separate lineage from the grey wolf (ancient DNA). Wolf build, heavier,
    # broad head with big carnassials. Coat unknown: a tawny-grey wolf pattern
    # (pale muzzle and underside, dark saddle, dark tail tip); a 2025 genome study
    # suggested light coats, which the variant palette uses (debated).
    "aenocyon": dict(
        ramps={
            "outline": ramp("221c1a"),
            "fur": ramp("54483e", "7c6c5c", "a2907a", "c4b49c"),
            "pale": ramp("b4a690", "d8ccb6", "f2ece0"),
            "dark": ramp("2a2420", "463c34"),
            "tawny": ramp("8a6440", "b08a5c"),
            "skin": ramp("6e3a36"),
            "white": ramp("f8f4ea"),
            "eye": ramp("b8862c"),
        },
        front=0.82, back=0.86, icon=0.42,
        shiny={"fur": dict(deg=10, sat=0.3, val=1.22), "tawny": dict(deg=6, sat=0.45, val=1.25),
               "dark": dict(deg=0, sat=0.5, val=1.9)},
        body=dict(L=22.0, top_s=-10.0, top_h=-9.0, chest=14.0, waist=10.0, hip=11.5, sag=0.5, chest_w=1.05),
        leg=dict(h=14.0, fr=(3.2, 2.1, 1.6), hr=(3.4, 2.0, 1.5), digi=1.0, paw=(3.6, 1.5), thigh=1.0),
        neck=dict(r0=5.6, r1=4.6, base=(0.0, 3.5)),
        head=dict(dx=-8.5, dy=-5.5, cr=6.2, cw=1.05, ml=6.6, md=5.2, mdrop=0.6, mtilt=6.0, jd=2.8, stop=0.7,
                  cheek=0.55, taper=0.72),
        ear=dict(kind="point", h=5.4, w=4.8, lean=14.0),
        tail=dict(len=19.0, a0=66.0, bend=-3.0, r=(2.6, 3.6, 1.6), widest=0.5),
        eye=dict(dx=-3.0, dy=-1.3, r=1.4, iris="eye", line=((-3.8, 0.0), (-5.6, 2.0))),
        marks=[tail_tip(0.8), ear_tip(-2.0),
               dict(on="torso", kind="above", line=(0.0, -7.0, 0.05), x=(-12.0, 14.0), ramp="dark"),
               dict(on="legs", kind="below", line=(0.0, -99.0, 0.0), ramp="tawny"),
               dict(on="ear", kind="below", line=(0.0, -99.0, 0.0), ramp="tawny")],
        action=dict(tilt=5.0, gape=-18.0, tail=-8.0),
        teeth=dict(canine=2.0),
    ),
    # Canis latrans, the coyote (living; WY), ~13 kg. Known colours: grizzled
    # grey-buff back with a darker saddle, tawny-rufous ears, muzzle and legs,
    # cream throat and belly, black tail tip, a dark line down the forelegs.
    # Narrow pointed muzzle, large ears, bushy tail carried low.
    "canis": dict(
        ramps={
            "outline": ramp("241c18"),
            "fur": ramp("5a4c40", "807060", "a69680", "c8baa0"),
            "pale": ramp("c0b098", "e0d4bc", "f6f0e2"),
            "dark": ramp("2a2220", "483c34"),
            "tawny": ramp("9a6638", "c08c54"),
            "skin": ramp("7a3c38"),
            "white": ramp("f8f4ea"),
        },
        front=0.86, back=0.9, icon=0.44,
        shiny={"fur": dict(deg=6, sat=1.3, val=0.62), "tawny": dict(deg=-4, sat=0.9, val=0.6),
               "pale": dict(deg=0, sat=0.8, val=0.82)},
        body=dict(L=20.0, top_s=-9.0, top_h=-8.5, chest=12.5, waist=8.5, hip=10.0, sag=0.5),
        leg=dict(h=13.0, fr=(2.7, 1.8, 1.3), hr=(3.0, 1.8, 1.3), digi=1.0, paw=(3.2, 1.25), thigh=0.95),
        neck=dict(r0=4.8, r1=3.9, base=(0.0, 3.2)),
        head=dict(dx=-8.0, dy=-6.0, cr=5.2, ml=7.4, md=4.2, mdrop=0.4, mtilt=5.0, jd=2.1, stop=0.5, taper=0.62),
        ear=dict(kind="point", h=6.6, w=4.8, lean=12.0),
        tail=dict(len=20.0, a0=64.0, bend=-3.0, r=(2.2, 3.4, 1.5), widest=0.55),
        eye=dict(dx=-2.6, dy=-1.0, r=1.35, line=((-3.2, 0.3), (-4.8, 1.8))),
        marks=[tail_tip(0.8), ear_tip(-2.5, "dark"),
               dict(on="torso", kind="above", line=(0.0, -6.0, 0.04), x=(-12.0, 14.0), ramp="dark"),
               dict(on="legs", kind="below", line=(0.0, -99.0, 0.0), ramp="tawny"),
               dict(on="ear", kind="below", line=(0.0, -99.0, 0.0), ramp="tawny"),
               dict(on="head", kind="ell", e=(-7.5, 1.6, 3.6, 1.6, 6), ramp="tawny")],
    ),
    # Vulpes velox, the swift fox (living; MT), ~2.2 kg. Known colours: grizzled
    # buff-grey back, orange-tawny flanks and legs, white-cream throat and belly,
    # black tail tip and a black patch on each side of the muzzle. Very large
    # ears, short slender muzzle, full tail held low.
    "vulpes": dict(
        ramps={
            "outline": ramp("2a1c16"),
            "fur": ramp("6a5444", "92785e", "b49c7e", "d2c0a2"),
            "pale": ramp("cabca6", "e8decc", "faf6ee"),
            "dark": ramp("221a18", "403430"),
            "tawny": ramp("a46634", "cc8c4c", "e0ac70"),
            "skin": ramp("7a3c38"),
            "white": ramp("fcfaf4"),
        },
        front=0.95, back=0.98, icon=0.47,
        shiny={"fur": dict(deg=0, sat=0.15, val=1.12), "tawny": dict(deg=0, sat=0.2, val=1.12)},
        body=dict(L=16.0, top_s=-8.0, top_h=-7.5, chest=10.0, waist=7.5, hip=9.0, sag=0.4),
        leg=dict(h=10.0, fr=(2.1, 1.4, 1.1), hr=(2.5, 1.5, 1.1), digi=1.0, paw=(2.8, 1.1), thigh=0.85),
        neck=dict(r0=4.0, r1=3.4, base=(0.3, 3.0)),
        head=dict(dx=-7.0, dy=-5.5, cr=5.0, ml=5.0, md=3.6, mdrop=0.5, mtilt=6.0, jd=1.8, stop=0.6, taper=0.6),
        ear=dict(kind="point", h=7.6, w=5.2, lean=10.0),
        tail=dict(len=19.0, a0=40.0, bend=-4.0, r=(2.0, 3.6, 1.6), widest=0.55),
        eye=dict(dx=-2.4, dy=-0.9, r=1.35, line=TEAR),
        marks=[tail_tip(0.8), ear_tip(-3.0),
               dict(on="head", kind="ell", e=(-6.4, 2.6, 1.7, 1.0, 10), ramp="dark"),
               dict(on="legs", kind="below", line=(0.0, -99.0, 0.0), ramp="tawny"),
               dict(on="torso", kind="below", line=(-20.0, -6.4, 0.07), x=(-20.0, 30.0), ramp="tawny",
                    above=0.0),
               dict(on="ear", kind="below", line=(0.0, -99.0, 0.0), ramp="tawny")],
    ),
}
