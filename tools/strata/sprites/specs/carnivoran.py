"""Species specs for the carnivoran body plan (plans/carnivoran.py; the keys are
documented in plans/canid.py, whose engine it uses). Owned by the carnivore
artist. See specs/fish.py for the common keys.

Coat colours of extinct species are reconstructions (noted per species);
black-footed ferret colours are real.
"""

from ..core.color import ramp
from ..plans.carnivoran import FOOTPRINTS
from .canid import DOG_RAMPS, TEAR, socks, tail_tip, ear_tip, rings


def whole(group, ramp_):
    """Colours a whole part group (legs, ear, ...) with one ramp."""
    return dict(on=group, kind="below", line=(0.0, -99.0, 0.0), ramp=ramp_)


def head_ell(cx, cy, rx, ry, ramp_, deg=0):
    return dict(on="head", kind="ell", e=(cx, cy, rx, ry, deg), ramp=ramp_)


CAT_WHISKERS = [((-6.0, 2.6), (-11.0, 1.6)), ((-6.0, 3.2), (-11.0, 4.2))]

SPECS = {
    # Protictis, Paleocene of MT/WY (~63 Ma), ~1.5 kg, ~50 cm with tail: a
    # viverravid, one of the earliest carnivoramorphs (known mostly from teeth).
    # Drawn as a genet/mongoose-like forest hunter: long low body, short legs,
    # long tail, pointed muzzle. Coat speculative: spotted flanks and a ringed
    # tail as in living genets, plus the dog-line marks (ear tips, tear streak,
    # socks, tail tip); the spots and rings fade along the line to Leptocyon.
    "protictis": dict(
        ramps={**DOG_RAMPS, "fur": ramp("5a3c2a", "82593a", "a67c54", "c6a074")},
        front=0.86, back=0.88, icon=0.43,
        shiny={"fur": dict(deg=-8, sat=0.5, val=0.8), "pale": dict(deg=0, sat=0.6, val=0.92)},
        body=dict(L=21.0, top_s=-6.0, top_h=-6.5, chest=9.5, waist=7.5, hip=9.0, sag=0.5),
        leg=dict(h=6.0, fr=(2.2, 1.5, 1.1), hr=(2.5, 1.6, 1.1), digi=0.45, paw=(3.2, 1.1), thigh=0.85),
        neck=dict(r0=4.0, r1=3.3, base=(0.5, 2.8)),
        head=dict(dx=-7.5, dy=-4.5, cr=4.8, ml=5.4, md=3.6, mdrop=0.4, mtilt=4.0, jd=1.9, stop=0.3, taper=0.6),
        ear=dict(kind="point", h=3.8, w=4.0, lean=18.0),
        tail=dict(len=25.0, a0=14.0, bend=-9.0, r=(2.2, 2.2, 1.1), widest=0.3),
        eye=dict(dx=-2.4, dy=-0.8, r=1.35, line=TEAR),
        marks=[socks(2.4), tail_tip(0.88), rings((0.22, 0.31), (0.44, 0.53), (0.66, 0.75)), ear_tip(-1.5),
               dict(on="torso", kind="spots", step=(4.0, 3.2), r=0.85, above=-1.0, x=(-10.0, 12.0), ramp="dark")],
        footprint=FOOTPRINTS["canid"],
        ow_end=dict(head=2.4),
    ),
    # Miacis, Bridger Fm (~48 Ma), ~1.5 kg, ~60 cm with tail: a miacid,
    # stem carnivoran. Arboreal: long body and tail, short limbs, flexible
    # ankles, larger brain than earlier forms. Coat speculative: forest agouti
    # with a ringed tail and faint shoulder spots (fading from Protictis), the
    # dog-line points kept; ears a little taller, muzzle a little longer.
    "miacis": dict(
        ramps={**DOG_RAMPS, "fur": ramp("5b3e2c", "84603e", "a8825a", "c8a67a")},
        front=0.85, back=0.87, icon=0.43,
        shiny={"fur": dict(deg=10, sat=0.45, val=1.08), "dark": dict(deg=0, sat=0.6, val=1.3)},
        body=dict(L=21.0, top_s=-6.5, top_h=-7.0, chest=10.0, waist=7.8, hip=9.4, sag=0.6),
        leg=dict(h=7.0, fr=(2.3, 1.5, 1.15), hr=(2.6, 1.6, 1.15), digi=0.5, paw=(3.2, 1.15), thigh=0.88),
        neck=dict(r0=4.2, r1=3.5, base=(0.5, 3.0)),
        head=dict(dx=-7.8, dy=-5.2, cr=5.0, ml=5.6, md=3.8, mdrop=0.4, mtilt=4.0, jd=2.0, stop=0.45, taper=0.62),
        ear=dict(kind="point", h=4.4, w=4.2, lean=16.0),
        tail=dict(len=26.0, a0=12.0, bend=-11.0, r=(2.3, 2.4, 1.2), widest=0.35),
        eye=dict(dx=-2.5, dy=-0.9, r=1.4, line=TEAR),
        marks=[socks(2.5), tail_tip(0.87), rings((0.3, 0.4), (0.52, 0.62), (0.72, 0.8)), ear_tip(-2.0),
               dict(on="torso", kind="spots", step=(4.2, 3.4), r=0.75, above=-2.0, x=(-12.0, -2.0), ramp="dark")],
        footprint=FOOTPRINTS["canid"],
        ow_end=dict(head=2.4),
    ),
    # Mustela nigripes, the black-footed ferret (living; MT), ~0.9 kg. Real
    # colours: buff-yellow body with a brown-washed back, black mask across
    # the eyes, black legs and feet, black tail tip, white muzzle, forehead and
    # throat. Very long body, short legs, long neck, flat head, small round ears.
    "mustela": dict(
        ramps={
            "outline": ramp("201814"),
            "fur": ramp("6c5638", "967c56", "bca27a", "dac6a0"),
            "pale": ramp("d0c6ae", "ebe4d2", "fbf9f2"),
            "dark": ramp("1c1614", "382c26"),
            "skin": ramp("7a3c38"),
            "white": ramp("fcfaf4"),
        },
        front=0.92, back=0.95, icon=0.46,
        shiny={"fur": dict(deg=0, sat=0.25, val=1.1), "dark": dict(deg=10, sat=1.2, val=2.6)},
        body=dict(L=27.0, top_s=-5.0, top_h=-5.5, chest=8.0, waist=7.0, hip=8.2, sag=0.0),
        leg=dict(h=4.5, fr=(2.0, 1.5, 1.2), hr=(2.3, 1.6, 1.2), digi=0.4, paw=(2.8, 1.1), thigh=0.8,
                 far=(2.5, -2.0)),
        neck=dict(r0=3.6, r1=3.2, base=(0.0, 2.2)),
        head=dict(dx=-8.0, dy=-3.6, cr=4.4, cw=1.05, ml=2.6, md=3.4, mdrop=0.5, mtilt=6.0, jd=1.7, taper=0.62),
        ear=dict(kind="round", h=2.6, w=3.2, lean=10.0, dx=1.4, dy=0.4),
        tail=dict(len=15.0, a0=8.0, bend=-6.0, r=(1.9, 2.1, 1.4), widest=0.5),
        eye=dict(dx=-2.2, dy=-0.7, r=1.3),
        marks=[whole("legs", "dark"), tail_tip(0.6),
               head_ell(-2.0, -0.4, 2.7, 1.5, "dark", -8),
               dict(on="head", kind="below", line=(0.0, 0.6, 0.0), ramp="pale"),
               dict(on="head", kind="below", line=(0.0, -9.0, 0.0), x=(-99.0, -4.6), ramp="pale"),
               dict(on="head", kind="above", line=(0.0, -1.9, 0.0), x=(-3.8, 1.0), ramp="pale"),
               dict(on="torso", kind="above", line=(0.0, -3.2, 0.0), x=(-6.0, 14.0), ramp=("fur")),
               ],
        whiskers=[((-6.0, 1.4), (-10.0, 0.6)), ((-6.0, 2.0), (-10.0, 3.0))],
        action=dict(tilt=8.0, gape=-14.0, tail=-8.0),
        teeth=dict(canine=1.2),
        fur_dashes=None, ow_end=dict(head=2.4),
        ow_ramps=dict(legs="dark", muzzle="pale"),
        ow_face=[(-0.45, 0.02, ("dark", 0)), (0.45, 0.02, ("dark", 0))],
    ),
    # Hoplophoneus, Brule Fm (~32 Ma), ~50 kg: a nimravid "false sabretooth".
    # Long body, short robust legs (semi-plantigrade), long blade-like upper
    # canines guarded by a bony flange on the lower jaw, a wide gape. Coat
    # speculative: tawny-brown with faint spots for a forest-edge ambusher.
    "hoplophoneus": dict(
        ramps={
            "outline": ramp("24180f"),
            "fur": ramp("5c4028", "86603c", "aa8456", "c8a676"),
            "pale": ramp("b8a080", "dccaa6", "f2e8d2"),
            "dark": ramp("2e2016", "4c3622"),
            "skin": ramp("7a3a34"),
            "white": ramp("f6f0dc"),
            "eye": ramp("c09030"),
        },
        front=0.88, back=0.92, icon=0.44,
        shiny={"fur": dict(deg=0, sat=0.35, val=0.62), "pale": dict(deg=0, sat=0.4, val=0.7)},
        body=dict(L=24.0, top_s=-9.5, top_h=-9.0, chest=13.0, waist=10.5, hip=11.5, sag=0.6),
        leg=dict(h=8.0, fr=(3.4, 2.4, 1.9), hr=(3.4, 2.2, 1.8), digi=0.55, paw=(4.0, 1.6), thigh=1.0),
        neck=dict(r0=5.2, r1=4.6, base=(0.0, 3.4)),
        head=dict(dx=-7.0, dy=-4.5, cr=5.9, ml=2.6, md=5.2, mdrop=0.4, mtilt=6.0, jd=2.4, cheek=0.55,
                  taper=0.8),
        ear=dict(kind="round", h=3.2, w=3.6, lean=20.0, dx=1.0, dy=0.6),
        tail=dict(len=22.0, a0=55.0, bend=-10.0, r=(2.6, 2.4, 1.5), widest=0.3),
        eye=dict(dx=-2.8, dy=-1.0, r=1.45, iris="eye"),
        marks=[tail_tip(0.86),
               dict(on="torso", kind="spots", step=(4.0, 3.4), r=0.9, above=-1.0, x=(-12.0, 15.0), ramp="dark"),
               dict(on="tail", kind="rings", bands=[(0.55, 0.62), (0.7, 0.77)], ramp="dark")],
        teeth=dict(canine=0.0, sabre=(6.4, 0.3), flange=(0.2, 3.0)),
        whiskers=[((-6.2, 2.0), (-10.5, 1.0)), ((-6.2, 2.6), (-10.5, 3.6))],
        action=dict(tilt=10.0, gape=-34.0, tail=-10.0),
        footprint=FOOTPRINTS["cat"],
    ),
    # Miracinonyx trumani, Natural Trap Cave (~20 ka), ~70 kg: the "American
    # cheetah", a puma relative that converged on the cheetah build: small
    # head, short face, very long slender legs, deep chest, narrow waist, long
    # tail. Coat speculative: plain tawny like its closest relative the puma
    # (no cheetah spots or tear lines), dark tail tip and whisker patch.
    "miracinonyx": dict(
        ramps={
            "outline": ramp("26190f"),
            "fur": ramp("6a4a2e", "967048", "bc9466", "d8b88a"),
            "pale": ramp("c6b294", "e4d8c0", "f8f2e4"),
            "dark": ramp("2c2016", "4a3826"),
            "skin": ramp("8a4a40"),
            "white": ramp("f8f4e8"),
            "eye": ramp("b89236"),
        },
        front=0.84, back=0.88, icon=0.42,
        shiny={"fur": dict(deg=-6, sat=0.55, val=0.78)},
        body=dict(L=22.0, top_s=-11.0, top_h=-11.0, chest=13.0, waist=7.5, hip=10.0, sag=0.8),
        leg=dict(h=16.0, fr=(2.7, 1.8, 1.4), hr=(3.2, 1.8, 1.4), digi=1.0, paw=(3.4, 1.35), thigh=1.0,
                 far=(3.5, -3.0), knee=3.5, hock=2.5),
        neck=dict(r0=4.6, r1=3.8, base=(0.0, 3.4)),
        head=dict(dx=-7.0, dy=-4.5, cr=4.8, ml=2.4, md=4.2, mdrop=0.3, mtilt=6.0, jd=2.0, cheek=0.35,
                  taper=0.82),
        ear=dict(kind="round", h=3.0, w=3.4, lean=24.0, dx=1.2, dy=0.6),
        tail=dict(len=27.0, a0=62.0, bend=-13.0, r=(2.2, 2.0, 1.5), widest=0.3),
        eye=dict(dx=-2.4, dy=-0.9, r=1.35, iris="eye"),
        marks=[tail_tip(0.88), head_ell(-6.0, 2.6, 1.3, 1.0, "dark")],
        whiskers=[((-5.6, 2.4), (-9.6, 1.4)), ((-5.6, 3.0), (-9.6, 4.0))],
        action=dict(tilt=6.0, gape=-20.0, tail=-12.0),
        footprint=FOOTPRINTS["cat"],
    ),
    # Panthera atrox, Natural Trap Cave (~20 ka), ~350 kg: the American lion,
    # bigger than living lions, longer-legged. Plain tawny lion coat with a dark
    # tail tuft; maneless here (cave art of the related cave lion shows no mane;
    # for P. atrox it is unknown).
    "panthera": dict(
        ramps={
            "outline": ramp("24180e"),
            "fur": ramp("6c4e2e", "9a764a", "c09a68", "dcbe8c"),
            "pale": ramp("c8b694", "e4d8bc", "f6f0e0"),
            "dark": ramp("2a1e14", "4a3624"),
            "skin": ramp("8a4a40"),
            "white": ramp("f8f4e6"),
            "eye": ramp("b88a30"),
        },
        front=0.77, back=0.79, icon=0.39,
        shiny={"fur": dict(deg=4, sat=0.3, val=1.12), "dark": dict(deg=0, sat=0.6, val=1.5)},
        body=dict(L=26.0, top_s=-12.0, top_h=-11.5, chest=16.0, waist=12.5, hip=13.5, sag=1.0, chest_w=1.05),
        leg=dict(h=13.0, fr=(4.0, 2.8, 2.2), hr=(4.0, 2.5, 2.0), digi=1.0, paw=(4.6, 2.0), thigh=1.05,
                 far=(3.5, -3.0), knee=3.5),
        neck=dict(r0=6.4, r1=5.4, base=(0.0, 4.0)),
        head=dict(dx=-8.0, dy=-5.0, cr=6.6, ml=3.4, md=6.0, mdrop=0.6, mtilt=6.0, jd=2.8, cheek=0.7,
                  taper=0.85, stop=0.3),
        ear=dict(kind="round", h=3.4, w=3.8, lean=24.0, dx=1.6, dy=0.6),
        tail=dict(len=28.0, a0=62.0, bend=-10.0, r=(2.6, 2.2, 2.6), widest=0.3),
        eye=dict(dx=-2.9, dy=-1.3, r=1.4, iris="eye"),
        marks=[tail_tip(0.86), head_ell(-7.5, 3.0, 1.5, 1.1, "dark")],
        whiskers=[((-7.4, 2.8), (-12.0, 1.8)), ((-7.4, 3.4), (-12.0, 4.4))],
        action=dict(tilt=8.0, gape=-24.0, tail=-10.0),
        teeth=dict(canine=2.2),
        footprint=FOOTPRINTS["cat"],
    ),
    # Arctodus simus, Natural Trap Cave (~20 ka), ~900 kg: the giant short-faced
    # bear (Tremarctinae). Long legs, short deep body, short broad face, small
    # round ears, stub tail, plantigrade feet with long claws. Coat speculative:
    # dark brown with a pale muzzle and pale "spectacle" marks around the eyes,
    # after its living relative the spectacled bear.
    "arctodus": dict(
        ramps={
            "outline": ramp("1e140e"),
            "fur": ramp("3c2a1e", "5a4030", "7a5a42", "9c7c5c"),
            "pale": ramp("a08462", "c4aa84", "e0cca8"),
            "dark": ramp("22170f", "34241a"),
            "skin": ramp("6a3832"),
            "white": ramp("f0e8d8"),
            "claw": ramp("cfc4b0"),
        },
        front=1.1, back=1.14, icon=0.55,
        shiny={"fur": dict(deg=8, sat=1.15, val=1.45), "pale": dict(deg=0, sat=0.8, val=1.08)},
        body=dict(L=19.0, top_s=-15.0, top_h=-13.5, chest=18.0, waist=15.0, hip=16.0, sag=0.0,
                  chest_w=1.0, rump_w=1.0, hump=(2.5, 3.0, 8.0, 5.5)),
        leg=dict(h=13.0, fr=(4.4, 3.4, 2.9), hr=(4.6, 3.4, 2.8), digi=0.15, paw=(6.0, 2.0), thigh=1.0,
                 far=(3.0, -2.5), knee=2.0, hock=1.0),
        neck=dict(r0=7.0, r1=6.2, base=(-0.5, 4.5)),
        head=dict(dx=-8.0, dy=-1.5, cr=7.2, cw=1.0, ml=1.8, md=6.2, mdrop=1.0, mtilt=12.0, jd=3.0, cheek=0.8,
                  taper=0.8, stop=0.6),
        ear=dict(kind="round", h=3.6, w=4.2, lean=10.0, dx=1.8, dy=0.6),
        tail=dict(len=4.0, a0=40.0, bend=0.0, r=(2.4, 2.4, 1.6), widest=0.5),
        eye=dict(dx=-3.4, dy=-1.4, r=1.3),
        marks=[head_ell(-3.4, -1.0, 2.6, 2.0, "pale"),
               dict(on="head", kind="below", line=(0.0, 1.8, 0.0), x=(-99.0, -6.2), ramp="pale"),
               dict(on="head", kind="below", line=(0.0, -9.0, 0.0), x=(-99.0, -7.5), ramp="pale")],
        belly=(99.0, 0.0), throat=(99.0, 0.0),
        claws=True, fur_dashes=(3, 4),
        action=dict(tilt=12.0, gape=-24.0, tail=0.0),
        teeth=dict(canine=2.4),
        ow=dict(tracks="TRACKS_FOOT"),
        ow_end=dict(head=1.6, ear=1.2),
        footprint=FOOTPRINTS["plantigrade"],
    ),
    # Oxyaena, Willwood Fm (~56-52 Ma), ~20 kg: an oxyaenid ("creodont").
    # Wolverine-like: long low body, short stout plantigrade limbs, long thick
    # tail, short broad head with a deep jaw, small round ears. Coat
    # speculative: dark brown with a pale buff side band, after the wolverine.
    "oxyaena": dict(
        ramps={
            "outline": ramp("1e1610"),
            "fur": ramp("3e2c20", "5c4232", "7c5c46", "9a7a60"),
            "pale": ramp("a68c66", "c8b08a", "e2d2b0"),
            "dark": ramp("221812", "36281e"),
            "skin": ramp("6e3a34"),
            "white": ramp("f2eada"),
        },
        front=0.9, back=0.94, icon=0.45,
        shiny={"fur": dict(deg=6, sat=0.9, val=1.45), "pale": dict(deg=0, sat=0.5, val=1.1)},
        body=dict(L=22.0, top_s=-7.5, top_h=-8.0, chest=11.5, waist=9.5, hip=10.5, sag=-0.6),
        leg=dict(h=6.0, fr=(3.0, 2.2, 1.8), hr=(3.2, 2.2, 1.8), digi=0.15, paw=(4.6, 1.5), thigh=0.95,
                 knee=2.0, hock=1.0),
        neck=dict(r0=4.8, r1=4.2, base=(0.0, 3.0)),
        head=dict(dx=-7.0, dy=-3.4, cr=5.6, ml=3.0, md=4.8, mdrop=0.6, mtilt=6.0, jd=2.6, cheek=0.7, taper=0.8),
        ear=dict(kind="round", h=2.8, w=3.4, lean=16.0, dx=1.2, dy=0.8),
        tail=dict(len=22.0, a0=24.0, bend=-3.0, r=(3.0, 2.8, 1.4), widest=0.25),
        eye=dict(dx=-2.6, dy=-0.9, r=1.3),
        marks=[whole("legs", "dark"), tail_tip(0.75),
               dict(on="torso", kind="ell", e=(1.0, -3.6, 13.0, 1.8, 2), ramp="pale"),
               head_ell(-4.0, -2.0, 3.0, 1.0, "pale", -10)],
        belly=(99.0, 0.0),
        teeth=dict(canine=1.8),
        footprint=FOOTPRINTS["plantigrade"],
    ),
    # Patriofelis ferox, Bridger Fm (~48-45 Ma), ~70 kg (estimates vary): a big
    # oxyaenid, the Bridger Basin's top predator. Heavy, short-legged,
    # plantigrade, an enormous broad head with a short face, long tail. Coat
    # speculative: drab grey-brown with darker limbs and faint dorsal bands.
    "patriofelis": dict(
        ramps={
            "outline": ramp("1e1814"),
            "fur": ramp("4a4036", "6c5e4e", "8e7e6a", "ae9e86"),
            "pale": ramp("a89a82", "cabea6", "e6dcc8"),
            "dark": ramp("26201a", "3c3228"),
            "skin": ramp("6e3a34"),
            "white": ramp("f2ecde"),
            "eye": ramp("a88a3a"),
        },
        front=0.82, back=0.84, icon=0.41,
        shiny={"fur": dict(deg=-14, sat=1.6, val=1.05), "dark": dict(deg=-10, sat=1.4, val=1.2)},
        body=dict(L=24.0, top_s=-10.0, top_h=-9.5, chest=14.0, waist=12.0, hip=12.5, sag=0.2),
        leg=dict(h=7.5, fr=(3.9, 2.9, 2.3), hr=(3.9, 2.8, 2.2), digi=0.2, paw=(5.2, 1.8), thigh=1.0,
                 knee=2.2, hock=1.0),
        neck=dict(r0=6.0, r1=5.6, base=(0.0, 3.6)),
        head=dict(dx=-7.6, dy=-3.6, cr=7.2, cw=1.05, ml=3.4, md=6.4, mdrop=0.8, mtilt=8.0, jd=3.2, cheek=1.0,
                  taper=0.8),
        ear=dict(kind="round", h=3.0, w=3.6, lean=16.0, dx=1.8, dy=1.0),
        tail=dict(len=24.0, a0=36.0, bend=-6.0, r=(3.2, 3.0, 1.6), widest=0.2),
        eye=dict(dx=-3.4, dy=-1.6, r=1.4, iris="eye"),
        marks=[socks(5.0), tail_tip(0.82),
               dict(on="torso", kind="stripes", period=4.2, width=1.4, x=(-4.0, 14.0), lean=0.35, above=-6.5,
                    ramp="dark")],
        action=dict(tilt=8.0, gape=-26.0, tail=-8.0),
        teeth=dict(canine=2.4),
        footprint=FOOTPRINTS["plantigrade"],
    ),
    # Hyaenodon horridus, Brule Fm (~33 Ma), ~40 kg: a hyaenodont ("creodont").
    # A huge, long, narrow skull with a long muzzle and shearing teeth, a deep
    # chest, digitigrade dog-like legs, moderately long tail. Coat speculative:
    # grey with a darker saddle and faint dark stripes on the flanks.
    "hyaenodon": dict(
        ramps={
            "outline": ramp("1c1a18"),
            "fur": ramp("4a4640", "6c665c", "8e877a", "afa898"),
            "pale": ramp("aaa292", "ccc6b8", "eae6dc"),
            "dark": ramp("24221e", "3a3630"),
            "skin": ramp("6e3a36"),
            "white": ramp("f4f0e6"),
            "eye": ramp("a8862e"),
        },
        front=0.86, back=0.9, icon=0.43,
        shiny={"fur": dict(deg=30, sat=2.2, val=1.05), "pale": dict(deg=25, sat=1.6, val=1.0)},
        body=dict(L=22.0, top_s=-9.5, top_h=-8.5, chest=13.0, waist=9.5, hip=10.5, sag=0.6),
        leg=dict(h=11.0, fr=(3.0, 2.0, 1.5), hr=(3.2, 1.9, 1.5), digi=0.9, paw=(3.6, 1.4), thigh=1.0),
        neck=dict(r0=5.0, r1=4.4, base=(0.0, 3.4)),
        head=dict(dx=-7.0, dy=-4.0, cr=5.8, ml=9.4, md=4.8, mdrop=0.8, mtilt=6.0, jd=2.6, cheek=0.5, taper=0.68,
                  stop=0.2),
        ear=dict(kind="point", h=3.6, w=4.0, lean=22.0, dx=1.2, dy=0.6, inner=False),
        tail=dict(len=19.0, a0=56.0, bend=-4.0, r=(2.6, 2.4, 1.2), widest=0.25),
        eye=dict(dx=-2.6, dy=-1.2, r=1.35, iris="eye"),
        marks=[tail_tip(0.8),
               dict(on="torso", kind="above", line=(0.0, -6.8, 0.04), x=(-12.0, 14.0), ramp="dark"),
               dict(on="torso", kind="stripes", period=3.6, width=1.2, x=(-6.0, 12.0), lean=0.3, above=-4.0,
                    ramp="dark")],
        action=dict(tilt=6.0, gape=-24.0, tail=-8.0),
        teeth=dict(canine=2.4),
    ),
    # Eoconodon, Denver Fm (~65.4 Ma), ~30 kg: a triisodontine "condylarth",
    # among the first big mammalian predators after the impact. Wolf-sized but
    # heavy: robust limbs, plantigrade feet with claws, long heavy tail, a big
    # head with blunt, crushing cheek teeth and stout canines. Coat speculative:
    # warm brown with dark limbs and a dark muzzle, in a post-impact fern forest.
    "eoconodon": dict(
        ramps={
            "outline": ramp("20160f"),
            "fur": ramp("4e3626", "744f36", "98704c", "b8916a"),
            "pale": ramp("a88c6c", "c9b08e", "e4d4b8"),
            "dark": ramp("261a12", "3e2c1e"),
            "skin": ramp("72403a"),
            "white": ramp("f2eada"),
            "eye": ramp("9c7a34"),
        },
        front=0.84, back=0.86, icon=0.42,
        shiny={"fur": dict(deg=0, sat=0.2, val=0.85), "pale": dict(deg=0, sat=0.3, val=0.95)},
        body=dict(L=22.0, top_s=-9.0, top_h=-9.0, chest=12.5, waist=10.5, hip=11.5, sag=0.4),
        leg=dict(h=8.5, fr=(3.3, 2.4, 1.9), hr=(3.5, 2.4, 1.9), digi=0.3, paw=(4.8, 1.6), thigh=1.0,
                 knee=2.4, hock=1.2),
        neck=dict(r0=5.2, r1=4.8, base=(0.0, 3.4)),
        head=dict(dx=-7.4, dy=-4.0, cr=6.2, ml=4.6, md=5.2, mdrop=0.6, mtilt=6.0, jd=2.8, cheek=0.6, taper=0.78,
                  stop=0.2),
        ear=dict(kind="round", h=3.2, w=3.6, lean=14.0, dx=1.4, dy=0.6),
        tail=dict(len=25.0, a0=34.0, bend=-6.0, r=(3.2, 2.8, 1.4), widest=0.2),
        eye=dict(dx=-2.6, dy=-1.2, r=1.35, iris="eye"),
        marks=[socks(5.5), tail_tip(0.84), head_ell(-8.4, 1.4, 3.2, 2.0, "dark", 6),
               dict(on="torso", kind="above", line=(0.0, -7.4, 0.02), x=(-12.0, 14.0), ramp="dark")],
        action=dict(tilt=8.0, gape=-24.0, tail=-8.0),
        teeth=dict(canine=2.4),
        footprint=FOOTPRINTS["plantigrade"],
    ),
}
