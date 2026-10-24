"""Species specs for the small-mammal body plan (plans/small_mammal.py).
Owned by the small-mammal artist. See specs/fish.py for the common keys.

Mesodma and Taeniolabis (multituberculates) use the classic ellipse template;
the others use the proportion engine (keys in plans/canid.py and at
ENGINE_DEFAULTS in plans/small_mammal.py). Cimolestes is the root of the dog
starter line and wears its family marks (specs/canid.py): dark ear tips, pale
muzzle/throat/chest, a tear streak, dark socks and tail tip, with the forest
spots and tail rings that fade out along the line.
"""

from ..core.color import ramp
from .canid import DOG_RAMPS, TEAR, socks, tail_tip, ear_tip, rings


def whole(group, ramp_):
    """Colours a whole part group (legs, ear, tail ...) with one ramp."""
    return dict(on=group, kind="below", line=(0.0, -99.0, 0.0), ramp=ramp_)


SPECS = {
    # Cimolestes, Hell Creek Fm (66.1 Ma), ~0.5 kg, ~30 cm with tail: a
    # cimolestid eutherian known from jaws with sharp, shearing insectivore-
    # carnivore teeth. Drawn as a small, low, long-snouted ground hunter
    # (opossum-shrew build: short legs, plantigrade, long tapering tail).
    # STARTER and root of the dog line (a stand-in ancestor): it wears the dog-
    # line marks in their richest form, rows of forest spots on the flanks and
    # a ringed tail (both fade out from Protictis to Leptocyon), dark ear tips,
    # tear streak, socks and tail tip. Coat colours are speculative.
    "cimolestes": dict(
        ramps={**DOG_RAMPS, "fur": ramp("5a3b2a", "835a3c", "a87e54", "caa474")},
        front=1.12, back=1.18, icon=0.52,
        shiny={"fur": dict(deg=-14, sat=0.45, val=0.82), "pale": dict(deg=0, sat=0.5, val=0.95),
               "dark": dict(deg=0, sat=0.8, val=1.15)},
        body=dict(L=12.5, top_s=-5.2, top_h=-5.8, chest=8.8, waist=7.4, hip=8.8, sag=0.5),
        leg=dict(h=5.2, fr=(2.0, 1.4, 1.1), hr=(2.5, 1.5, 1.1), digi=0.25, paw=(2.8, 1.05), thigh=0.95,
                 far=(2.5, -2.0), stride=20.0),
        neck=dict(r0=3.8, r1=3.3, base=(0.5, 2.6)),
        head=dict(dx=-6.0, dy=-4.6, cr=5.0, ml=4.8, md=3.5, mdrop=0.7, mtilt=7.0, jd=1.8, stop=0.3, taper=0.5),
        ear=dict(kind="point", h=4.8, w=4.4, lean=14.0),
        tail=dict(len=17.0, a0=-4.0, bends=[-6.0, -9.0, -12.0, -12.0, -10.0], r=(2.1, 1.9, 0.9), widest=0.15),
        eye=dict(dx=-2.3, dy=-0.9, r=1.55, ring=("pale", 1), line=((-3.2, 0.6), (-4.8, 2.2))),
        marks=[socks(2.0), tail_tip(0.86), rings((0.22, 0.32), (0.44, 0.54), (0.66, 0.76)), ear_tip(-2.0),
               dict(on="torso", kind="spots", step=(3.8, 3.2), r=0.7, above=-1.0, x=(-7.0, 3.5), ramp="dark")],
        whiskers=[((-7.6, 1.6), (-11.0, 0.8)), ((-7.6, 2.2), (-11.0, 3.2))],
        action=dict(tilt=8.0, gape=-18.0, tail=-14.0),
        teeth=dict(canine=1.2),
        ow_end=dict(head=2.5),
    ),
    # Mesodma, Hell Creek Fm (latest Cretaceous): a ~30 g multituberculate.
    # Mesodma, Hell Creek Fm (latest Cretaceous): a ~30 g multituberculate.
    # Mouse-sized and rodent-like by convergence: short deep snout, procumbent
    # lower incisors, a long tail (ptilodontoids had reversible hind feet and are
    # reconstructed as climbers). Fur colour is unknown; a muted agouti brown with
    # a pale belly is the conservative choice.
    "mesodma": dict(
        ramps={
            "outline": ramp("2a1c16"),
            "fur": ramp("5a3a28", "82583c", "a87c56", "cca476"),
            "belly": ramp("b4967a", "d8c2a0", "f0e2c8"),
            "skin": ramp("8c5e5c", "bc8880", "e2b2a6"),
            "white": ramp("fcfcf4"),
        },
        front=0.9, back=0.95, icon=0.46,
        shiny={"fur": dict(deg=-12, sat=0.45, val=1.12)},
        sniff=7, neck=(-10.0, 2.0),
        torso=[(7.0, 2.5, 11.5, 9.8, -8), (-4.0, 5.0, 9.0, 7.6, 5)],
        head=[(-16.0, -0.8, 8.8, 7.6, -12), (-22.8, 2.0, 5.2, 4.2, 10)],
        ear=(-11.0, -7.6, 3.6, 4.2, 20),
        thigh=(10.0, 7.0, 6.2, 6.8, 20),
        legs=[  # far legs first
            dict(near=False, swing=1, z=-2, foot_z=-1.9,
                 pts=[(15.0, 10.0), (14.5, 15.5), (13.0, 16.8)], radii=[2.4, 1.8, 1.5], foot=(11.0, 17.6, 3.8, 1.4)),
            dict(near=False, swing=-1, z=-2, foot_z=-1.9, fore=True,
                 pts=[(-2.5, 9.0), (-3.0, 13.5), (-4.5, 16.5)], radii=[2.6, 2.0, 1.6], foot=(-5.6, 17.2, 2.4, 1.3)),
            dict(near=True, swing=-1, z=2, foot_z=2.1, toes=((2.0, 3.6, 5.2), 18.4),
                 pts=[(10.0, 11.0), (8.0, 15.5), (6.5, 16.8)], radii=[2.6, 2.0, 1.6], foot=(4.2, 17.6, 4.4, 1.5)),
            dict(near=True, swing=1, z=4, foot_z=4.1, fore=True, lift=1.8, toes=((-12.5, -11.0), 17.6),
                 pts=[(-7.0, 8.5), (-8.5, 13.0), (-10.5, 16.0)], radii=[3.0, 2.2, 1.7], foot=(-11.8, 16.8, 2.6, 1.4)),
        ],
        curl=2.0,
        tail=[(16.0, 5.0, 0, 0), (22.0, 3.5, 0, 0), (26.5, -1.0, 0, 0), (28.5, -7.0, -0.5, 0),
              (27.0, -12.0, -1, 0.5), (23.5, -14.5, -1, 1)],
        tail_radii=[2.6, 2.1, 1.8, 1.5, 1.3, 1.1],
        belly_line=(7.0, 0.10),
        jaw=(-16.0, 2.6, -0.10),
        inner_ear=((-10.8, -7.0), 2.1, 1.2),
        fur_dashes=(3, 5),
        nose=((-27.0, 0.6), 1.3, 0.8),
        nostril=(-27.3, 0.0),
        mouth=[(-26.0, 3.2), (-22.5, 4.4)],
        incisors=[(-25.0, 4.6), (-25.0, 5.6)],
        eye=((-18.2, -2.0), 2.6, 1.2),
        whiskers=[((-24.0, 1.5), (-31.0, -1.0)), ((-24.0, 2.5), (-31.5, 3.5))],
    ),
    # Taeniolabis taoensis, Denver Fm (~65.4 Ma), ~30 kg, ~0.9 m: the largest
    # multituberculate. Drawn with Mesodma's template so the two read as one
    # group: the same rounded rodent-like build, scaled up to a heavy, beaver-
    # sized ground animal with a deep, short skull, huge gnawing incisors (it
    # gnawed tough plants), small ears and a short thick tail. Fur colour is
    # speculative: a darker, greyer agouti than Mesodma, pale cheeks and belly.
    "taeniolabis": dict(
        ramps={
            "outline": ramp("241914"),
            "fur": ramp("4a3426", "6c4e38", "8e6c4e", "b08e68"),
            "belly": ramp("9c8670", "c2ae92", "e2d4ba"),
            "skin": ramp("6a4a44", "94706a", "bc968c"),
            "white": ramp("f4ead0"),
        },
        front=0.86, back=0.92, icon=0.44,
        shiny={"fur": dict(deg=8, sat=1.25, val=1.12), "belly": dict(deg=6, sat=1.1, val=1.05)},
        sniff=6, neck=(-11.0, 2.0), curl=1.6, nostril=(-30.6, 1.0), whiskers=None,
        torso=[(6.0, 1.5, 14.0, 11.5, -6), (-5.5, 4.0, 10.5, 9.4, 5)],
        head=[(-17.5, -0.8, 10.0, 8.8, -10), (-25.0, 2.8, 6.4, 5.6, 12)],
        ear=(-12.0, -8.6, 3.0, 3.1, 20),
        thigh=(11.0, 6.5, 7.6, 8.2, 20),
        legs=[  # far legs first
            dict(near=False, swing=1, z=-2, foot_z=-1.9,
                 pts=[(15.0, 10.0), (14.5, 15.5), (13.5, 17.0)], radii=[3.4, 2.6, 2.1], foot=(11.6, 18.0, 4.4, 1.7)),
            dict(near=False, swing=-1, z=-2, foot_z=-1.9, fore=True,
                 pts=[(-3.0, 10.0), (-3.5, 14.0), (-4.5, 16.8)], radii=[3.4, 2.7, 2.2], foot=(-6.0, 17.8, 3.0, 1.6)),
            dict(near=True, swing=-1, z=2, foot_z=2.1, toes=((2.2, 3.8, 5.4), 18.9),
                 pts=[(11.0, 11.0), (8.6, 15.5), (7.2, 17.0)], radii=[3.4, 2.6, 2.1], foot=(4.6, 18.0, 4.8, 1.7)),
            dict(near=True, swing=1, z=4, foot_z=4.1, fore=True, lift=1.6, toes=((-14.0, -12.4, -10.8), 18.6),
                 pts=[(-8.0, 9.0), (-9.0, 13.5), (-10.8, 16.4)], radii=[3.8, 2.9, 2.3], foot=(-12.4, 17.6, 3.2, 1.7)),
        ],
        tail=[(18.0, 6.0, 0, 0), (23.0, 6.8, 0, 0), (27.0, 8.6, 0.5, -1), (29.5, 11.2, 1, -1.5)],
        tail_radii=[3.6, 3.0, 2.3, 1.6],
        belly_line=(7.5, 0.10),
        jaw=(-17.5, 3.6, -0.12),
        inner_ear=((-11.8, -8.2), 1.6, 0.9),
        fur_dashes=(3, 4),
        nose=((-30.2, 1.6), 1.5, 0.9),
        mouth=[(-28.8, 5.0), (-24.6, 6.2)],
        incisors=[(-28.4, 5.6), (-27.4, 5.6), (-28.6, 6.6), (-27.6, 6.6), (-28.8, 7.6), (-27.8, 7.6),
                  (-28.9, 8.5)],
        eye=((-19.5, -2.4), 2.4, 1.1),
    ),
    # Didelphodon vorax, Hell Creek Fm (66.1 Ma), ~5 kg, ~60 cm: a stagodontid
    # metatherian (marsupial relative) with the strongest bite for its size of
    # any known mammal: broad, short skull, huge jaw muscles, bulbous crushing
    # premolars for snails, crabs and small turtles. Found in river deposits;
    # reconstructed as a semi-aquatic, otter-like predator: long low body,
    # short legs, a thick tapering tail. Coat colour speculative (otter brown,
    # pale throat).
    "didelphodon": dict(
        ramps={
            "outline": ramp("1e1714"),
            "fur": ramp("3e2c22", "5e4434", "80604a", "a28266"),
            "pale": ramp("9a8670", "c0ae92", "ddd0b8"),
            "dark": ramp("261c18", "3a2c24"),
            "skin": ramp("7c4440"),
            "white": ramp("f4eee0"),
        },
        front=0.98, back=1.04, icon=0.48,
        shiny={"fur": dict(deg=6, sat=0.9, val=1.45), "pale": dict(deg=4, sat=0.8, val=1.08)},
        body=dict(L=19.0, top_s=-6.6, top_h=-7.4, chest=10.6, waist=9.6, hip=10.6, sag=0.3, k=0.18),
        leg=dict(h=4.2, fr=(2.6, 1.8, 1.4), hr=(3.0, 1.9, 1.4), digi=0.15, paw=(3.4, 1.25), thigh=1.0,
                 far=(2.5, -2.2), stride=18.0),
        neck=dict(r0=5.0, r1=4.6, base=(0.0, 3.0)),
        head=dict(dx=-7.0, dy=-3.6, cr=5.8, cw=1.08, ml=3.6, md=4.6, mdrop=0.9, mtilt=7.0, jd=2.8, cheek=0.85,
                  stop=0.2, taper=0.74),
        ear=dict(kind="round", h=2.6, w=3.2, lean=18.0, dx=1.6, dy=0.6, inner=False),
        tail=dict(len=18.0, a0=6.0, bend=-3.0, r=(3.4, 2.8, 0.9), widest=0.12),
        eye=dict(dx=-2.6, dy=-1.0, r=1.3),
        marks=[dict(on="legs", kind="socks", h=2.2, ramp="dark")],
        whiskers=[((-7.4, 1.8), (-11.6, 1.0)), ((-7.4, 2.5), (-11.6, 3.6))],
        action=dict(tilt=9.0, gape=-26.0, tail=-8.0),
        teeth=dict(canine=1.8),
        ow_end=dict(head=2.2),
    ),
    # Loxolophus, Denver Fm (~65.7 Ma), ~3 kg: an early "condylarth" (arctocyonid
    # grade), one of the omnivores whose size rebounded first after the impact.
    # Raccoon-sized, robust, plantigrade with claws, a blunt muzzle with low
    # crushing teeth and a long tail. Coat speculative: grizzled grey-brown with
    # darker legs and a pale cheek patch (generalist forest omnivore).
    "loxolophus": dict(
        ramps={
            "outline": ramp("221c18"),
            "fur": ramp("4e4238", "726354", "968672", "b6a890"),
            "pale": ramp("aea08a", "d0c4ac", "eee6d4"),
            "dark": ramp("2a2420", "443a32"),
            "skin": ramp("6e4440"),
            "white": ramp("f6f2e6"),
            "claw": ramp("cfc4b0"),
        },
        front=0.96, back=1.0, icon=0.48,
        shiny={"fur": dict(deg=20, sat=1.9, val=1.02), "dark": dict(deg=20, sat=1.6, val=1.3)},
        body=dict(L=15.0, top_s=-7.0, top_h=-8.4, chest=10.4, waist=9.0, hip=10.6, sag=0.6, k=0.16),
        leg=dict(h=6.4, fr=(2.6, 1.8, 1.4), hr=(3.0, 1.9, 1.4), digi=0.15, paw=(3.4, 1.3), thigh=1.0,
                 far=(2.6, -2.4), stride=18.0),
        neck=dict(r0=4.6, r1=4.0, base=(0.5, 3.0)),
        head=dict(dx=-6.8, dy=-4.2, cr=5.4, ml=4.2, md=4.0, mdrop=0.8, mtilt=8.0, jd=2.2, cheek=0.45, stop=0.3,
                  taper=0.66),
        ear=dict(kind="round", h=3.4, w=3.6, lean=16.0, dx=1.2, dy=0.6, inner=False),
        tail=dict(len=19.0, a0=34.0, bend=-10.0, r=(2.6, 2.8, 1.3), widest=0.35),
        eye=dict(dx=-2.4, dy=-1.0, r=1.35),
        marks=[whole("legs", "dark"), dict(on="tail", kind="tip", f=0.82, ramp="dark"),
               dict(on="head", kind="ell", e=(-1.6, 1.6, 2.6, 1.6, -10), ramp="pale")],
        claws=True,
        action=dict(tilt=10.0, gape=-12.0, tail=-14.0),
        teeth=dict(canine=0.0),
        ow_ramps=dict(legs="dark"),
    ),
    # Carsioptychus coarctatus, Denver Fm (~65.7 Ma), ~6 kg: a periptychid
    # "condylarth", a stout, short-limbed plant eater with swollen, crushing
    # premolars (hard seeds and nuts) and small hoof-like claws. Drawn as a
    # pig-like ground forager: barrel body, deep short muzzle, small ears,
    # short tail. Coat speculative: plain earth brown with a few faint pale
    # spots, as in many forest-floor animals (cf. young tapirs, pacas).
    "carsioptych": dict(
        ramps={
            "outline": ramp("251a12"),
            "fur": ramp("4e3622", "75532f", "9a7344", "ba9662"),
            "pale": ramp("a68c68", "c8b08a", "e4d6b6"),
            "dark": ramp("2e2016", "46321f"),
            "skin": ramp("6a3e36"),
            "white": ramp("f4ecda"),
            "claw": ramp("3a2c22"),
        },
        front=1.0, back=1.05, icon=0.5,
        shiny={"fur": dict(deg=-10, sat=0.5, val=0.85), "dark": dict(deg=0, sat=0.5, val=1.0)},
        body=dict(L=15.0, top_s=-8.0, top_h=-9.6, chest=12.4, waist=11.0, hip=12.6, sag=0.3, chest_w=1.0,
                  rump_w=1.1, k=0.2),
        leg=dict(h=5.8, fr=(2.9, 2.1, 1.7), hr=(3.2, 2.2, 1.7), digi=0.5, paw=(2.8, 1.35), thigh=0.9,
                 far=(2.4, -2.4), stride=16.0),
        neck=dict(r0=5.6, r1=5.0, base=(0.0, 3.4)),
        head=dict(dx=-6.4, dy=-1.8, cr=5.6, ml=5.4, md=4.6, mdrop=1.4, mtilt=14.0, jd=2.6, cheek=0.8, stop=0.4,
                  taper=0.8),
        ear=dict(kind="round", h=3.8, w=3.6, lean=24.0, dx=1.4, dy=0.4, inner=False),
        tail=dict(len=8.0, a0=55.0, bend=-4.0, r=(2.0, 1.8, 1.0), widest=0.3),
        eye=dict(dx=-2.6, dy=-1.2, r=1.25),
        marks=[dict(on="torso", kind="spots", step=(4.0, 3.0), r=0.6, above=-2.6, x=(-7.0, 5.0), ramp="pale"),
               dict(on="legs", kind="socks", h=1.4, ramp="claw")],
        action=dict(tilt=-6.0, gape=-10.0, tail=-20.0),
        nose_ramp=("skin", 0),
        ow_end=dict(head=2.0, body=1.15),
    ),
    # Hyopsodus, Willwood Fm (~55 Ma), ~1 kg, ~35 cm: one of the commonest
    # Eocene mammals. Long body, short limbs, long tail, small head with a
    # short snout; its skeleton suggests a scurrying, partly burrowing
    # generalist (its ear region hints at echolocation-like hearing). Coat
    # speculative: warm agouti brown with a darker back stripe.
    "hyopsodus": dict(
        ramps={
            "outline": ramp("231c18"),
            "fur": ramp("5a4230", "806048", "a4825e", "c4a47a"),
            "pale": ramp("bca486", "dcc8a8", "f2e6d0"),
            "dark": ramp("2c2420", "45392f"),
            "skin": ramp("8a5a54"),
            "white": ramp("f6f2e6"),
        },
        front=1.0, back=1.05, icon=0.5,
        shiny={"fur": dict(deg=14, sat=1.8, val=1.08), "dark": dict(deg=14, sat=1.4, val=1.2)},
        body=dict(L=19.0, top_s=-5.0, top_h=-5.6, chest=8.2, waist=7.4, hip=8.4, sag=0.2, k=0.16),
        leg=dict(h=3.8, fr=(2.0, 1.4, 1.1), hr=(2.3, 1.5, 1.1), digi=0.35, paw=(2.8, 1.05), thigh=0.9,
                 far=(2.4, -2.0), stride=20.0),
        neck=dict(r0=3.8, r1=3.4, base=(0.5, 2.6)),
        head=dict(dx=-6.2, dy=-3.0, cr=4.6, ml=3.6, md=3.4, mdrop=0.6, mtilt=6.0, jd=1.8, stop=0.3, taper=0.62),
        ear=dict(kind="round", h=3.0, w=3.2, lean=16.0, dx=1.2, dy=0.6, inner=False),
        tail=dict(len=17.0, a0=8.0, bend=-5.0, r=(2.1, 1.8, 0.9), widest=0.15),
        eye=dict(dx=-2.2, dy=-0.9, r=1.3),
        marks=[dict(on="torso", kind="above", line=(0.0, -4.2, 0.03), x=(-12.0, 14.0), ramp="dark"),
               dict(on="tail", kind="above", line=(0.0, -99.0, 0.0), ramp="fur")],
        whiskers=[((-6.6, 1.4), (-10.6, 0.6)), ((-6.6, 2.0), (-10.6, 3.0))],
        action=dict(tilt=10.0, gape=0.0, tail=-14.0, ear=-10.0),
        ow_end=dict(head=2.4),
    ),
}
