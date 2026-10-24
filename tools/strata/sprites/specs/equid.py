"""Species specs for the equid body plan (plans/equid.py documents the keys).

The horse series is drawn as one lineage: the same template and family marks
(pale belly and mealy muzzle, dark mane and tail hair, darkening lower legs)
with the proportions evolving species by species:

    species         kg   back      legs/chest  toes (fore/hind)       face (ml/cr)  mane
    Sifrhippus       4   arched    1.0         4 / 3, padded           2.2           none
    Eohippus        10   arched    1.05        4 / 3, padded           2.4           crest
    Mesohippus      40   level     1.25        3 / 3, all on ground    2.8           short
    Hypohippus     200   level     1.1         3 / 3, broad, on ground 3.0           short
    Protohippus    100   level     1.3         3 / 3, side toes raised 3.4           upright
    Cormohipparion 100   level     1.45        3 / 3, side toes raised 3.4           upright
    Equus          300   level     1.3         1 / 1                   3.5           upright

Coat colours of the extinct horses are reconstructions (no pigment evidence):
small forest browsers get the dappled coat of living forest ungulates (duikers,
chevrotains, fawns), with dapples fading out as horses moved into open
country; Hypohippus stayed a forest browser and keeps a dappled coat; the
grazers are plain sandy/bay; Equus is a dun with the primitive markings of
wild horses (dorsal stripe, dark points, faint leg bars), as in Przewalski's
horse and the ancient-DNA coat colours of Pleistocene horses (dun / bay).
"""

from ..core.color import ramp
from ..plans.equid import FOOTPRINT_THREE_TOED

# The forest-horse base palette: rufous agouti with cream dapples.
FOREST = {
    "outline": ramp("24160e"),
    "fur": ramp("5a3824", "805234", "a4704a", "c4946a"),
    "pale": ramp("caa682", "eedcc0"),
    "dark": ramp("2c1c14", "4a3020"),
    "mane": ramp("2c1c14", "4a3020", "6a4630"),
    "hoof": ramp("5c5248", "908676"),
    "white": ramp("f8f0e2"),
}


def tail_hair(f=0.15):
    return dict(on="tail", kind="tip", f=f, ramp="mane")


def socks(h, ramp_="dark", legs="all"):
    return dict(on="legs", kind="socks", h=h, legs=legs, ramp=ramp_)


def muzzle(x, y, r=2.4, ramp_="pale"):
    """The mealy muzzle: a pale patch round the nose tip (head-local)."""
    return dict(on="head", kind="ell", e=(x, y, r, r * 0.9), ramp=ramp_)


def dapples(step, r, x, above=-1.5, ramp_="pale"):
    return dict(on="torso", kind="spots", step=step, r=r, x=x, above=above, ramp=ramp_)


SPECS = {
    # Sifrhippus sandrae, Willwood Fm (~56 Ma), ~4 kg (dwarfed during the PETM):
    # the earliest North American horse, cat-sized. Arched back with the rump
    # above the withers, hind legs longer than the fore, short neck, short low
    # face with a big eye, small padded feet with 4 front / 3 hind toes, a
    # longish thin tail. Coat speculative: rufous agouti with rows of cream
    # dapples (duiker/fawn pattern of forest-floor browsers).
    "sifrhippus": dict(
        ramps=FOREST,
        front=1.3, back=1.36, icon=0.62,
        shiny={"fur": dict(deg=-8, sat=0.55, val=0.78), "mane": dict(deg=0, sat=0.6, val=0.85)},
        body=dict(L=16.0, top_s=-6.0, top_h=-8.5, chest=10.0, waist=9.0, hip=10.5, sag=-1.4, k=0.26),
        leg=dict(h=10.0, fr=(2.3, 1.6, 0.95, 1.05), hr=(2.8, 1.8, 1.0, 1.05), pas=1.8, slope=0.6, hoof=(1.6, 1.2),
                 toes=(4, 3), side=(0.7, 0.3), stifle=2.4, hock=2.0, hk=0.4, far=(2.6, -2.4), stride=18.0),
        neck=dict(pts=[(0.5, 4.0), (-2.6, -0.5), (-4.0, -3.5)], r=[4.4, 3.7, 3.2]),
        head=dict(dx=-1.5, dy=-1.6, face=26.0, cr=3.6, ml=8.0, md=4.6, mt=2.8, drop=0.4, jaw=0.85),
        ear=dict(h=3.8, w=2.4, lean=8.0),
        eye=dict(dx=-0.9, dy=-0.6, r=1.3),
        tail=dict(len=13.0, a0=55.0, bend=6.0, r=(1.4, 1.6, 0.8), widest=0.35, dy=0.6),
        mouth=1.8,
        throat=0.2,
        fur_dashes=(3, 5),
        marks=[tail_hair(0.7), muzzle(-7.0, 0.4, 2.0),
               dapples((3.6, 2.8), 0.85, (-7.0, 9.0), above=-1.6)],
        action=dict(tilt=10.0, neck=3.0, tail=-22.0, ear=-14.0),
        ow_end=dict(head=2.0, face=1.0, legs=0.9),
        footprint=[
            "................",
            "................",
            "................",
            "................",
            ".....#....#.....",
            "...#..#..#..#...",
            "...#........#...",
            "......####......",
            ".....######.....",
            ".....######.....",
            "......####......",
            "................",
            "................",
            "................",
            "................",
            "................",
        ],
    ),
    # Eohippus angustidens, Wind River Fm (~52 Ma), ~10 kg: fox-sized, still
    # arched-backed with 4 front / 3 hind toes; a slightly longer face and legs
    # than Sifrhippus, low-crowned browsing teeth. Coat speculative: the forest
    # dapples, fewer and fainter; a short crest of a mane appears (speculative).
    "eohippus": dict(
        ramps={**FOREST,
               "fur": ramp("5c3c28", "84583a", "a87650", "c69a70"),
               "pale": ramp("c8a684", "ead8bc")},
        front=1.25, back=1.3, icon=0.6,
        shiny={"fur": dict(deg=10, sat=0.45, val=0.92), "mane": dict(deg=0, sat=0.5, val=1.1)},
        body=dict(L=17.5, top_s=-6.5, top_h=-8.5, chest=10.5, waist=9.0, hip=10.8, sag=-1.0, k=0.26),
        leg=dict(h=11.0, fr=(2.4, 1.6, 0.95, 1.05), hr=(2.9, 1.8, 1.0, 1.05), pas=1.9, slope=0.6, hoof=(1.7, 1.3),
                 toes=(4, 3), side=(0.66, 0.4), stifle=2.5, hock=2.1, hk=0.4, far=(2.8, -2.5)),
        neck=dict(pts=[(0.5, 4.0), (-2.8, -1.0), (-4.4, -4.5)], r=[4.5, 3.7, 3.1]),
        mane=dict(r=0.8, off=0.95),
        head=dict(dx=-1.5, dy=-1.6, face=30.0, cr=3.5, ml=8.6, md=4.6, mt=2.8, drop=0.4, jaw=0.9),
        ear=dict(h=3.5, w=2.4, lean=10.0),
        eye=dict(dx=-0.9, dy=-0.6, r=1.3),
        tail=dict(len=13.0, a0=50.0, bend=7.0, r=(1.4, 1.7, 0.9), widest=0.4, dy=0.6),
        mouth=1.9,
        throat=0.3,
        fur_dashes=(3, 5),
        marks=[tail_hair(0.55), muzzle(-7.6, 0.5, 2.1), socks(2.2, "fur"),
               dapples((4.2, 3.0), 0.75, (-3.0, 9.0), above=-2.0)],
        action=dict(tilt=12.0, neck=4.0, tail=-20.0, ear=-14.0),
        ow_end=dict(head=1.95, legs=0.9),
    ),
    # Mesohippus bairdi, Brule Fm (~32 Ma), ~40 kg: a sheep-sized horse with a
    # straight back, longer legs and three toes on every foot (all reaching the
    # ground), a longer face but still low-crowned browsing teeth. Coat
    # speculative: brown with the last faint dapples on the rump, darker legs.
    "mesohippus": dict(
        ramps={**FOREST,
               "fur": ramp("5a4030", "7e5c42", "a07c5a", "c09e7a"),
               "pale": ramp("c8ae90", "ead8c0")},
        front=1.2, back=1.25, icon=0.58,
        shiny={"fur": dict(deg=0, sat=0.25, val=0.95), "mane": dict(deg=0, sat=0.3, val=1.0)},
        body=dict(L=19.0, top_s=-7.5, top_h=-8.2, chest=10.5, waist=8.8, hip=10.2, sag=0.1, k=0.26),
        leg=dict(h=13.0, fr=(2.4, 1.6, 0.9, 1.0), hr=(2.8, 1.8, 0.95, 1.0), pas=2.0, slope=0.8, hoof=(2.0, 1.4),
                 toes=(3, 3), side=(0.55, 0.5), stifle=2.6, hock=2.2, far=(3.0, -2.6)),
        neck=dict(pts=[(0.5, 4.2), (-3.4, -1.6), (-5.4, -6.0)], r=[4.6, 3.6, 2.9]),
        mane=dict(r=1.1, off=1.0),
        head=dict(dx=-1.3, dy=-1.5, face=34.0, cr=3.4, ml=9.6, md=4.8, mt=3.0, drop=0.5, jaw=0.95),
        ear=dict(h=3.7, w=2.4, lean=8.0),
        eye=dict(dx=-0.9, dy=-0.7, r=1.25),
        tail=dict(len=13.0, a0=62.0, bend=5.0, r=(1.4, 2.0, 0.9), widest=0.5, dy=0.6),
        mouth=2.1,
        throat=0.5,
        marks=[tail_hair(0.35), muzzle(-8.6, 0.6, 2.3), socks(3.4),
               dapples((4.0, 3.0), 0.7, (3.0, 12.0), above=-2.5)],
        action=dict(tilt=14.0, neck=5.0, tail=-18.0, ear=-12.0),
        ow_end=dict(head=1.85),
    ),
    # Protohippus simus, Ashfall (~12 Ma), ~100 kg: a pony-sized grazer. Long
    # face with a deep jaw for its high-crowned (hypsodont) grinding teeth,
    # long legs, the side toes reduced and lifted off the ground. Coat
    # speculative: plain sandy bay of an open-grassland horse, dark points and
    # an upright mane (speculative for Miocene horses).
    "protohippus": dict(
        ramps={
            "outline": ramp("22160e"),
            "fur": ramp("6a4428", "925e38", "b67e4e", "d29e6c"),
            "pale": ramp("d2b48e", "eedfc4"),
            "dark": ramp("2a1c14", "463022"),
            "mane": ramp("2a1c14", "463022", "644632"),
            "hoof": ramp("5c5248", "908676"),
            "white": ramp("f8f0e2"),
        },
        front=1.12, back=1.17, icon=0.54,
        shiny={"fur": dict(deg=-6, sat=0.5, val=0.75), "pale": dict(deg=0, sat=0.6, val=0.92)},
        body=dict(L=21.0, top_s=-8.5, top_h=-8.6, chest=11.5, waist=9.6, hip=10.8, sag=0.3, k=0.28),
        leg=dict(h=15.0, fr=(2.6, 1.8, 0.95, 1.1), hr=(2.9, 1.9, 0.95, 1.1), pas=2.3, slope=0.9, hoof=(2.3, 1.6),
                 toes=(3, 3), side=(0.42, 1.6), stifle=2.8, hock=2.3),
        neck=dict(pts=[(1.0, 4.6), (-3.8, -1.8), (-6.4, -7.2)], r=[5.0, 3.9, 3.1]),
        mane=dict(r=1.5, off=1.0, up=True),
        head=dict(dx=-1.1, dy=-1.5, face=38.0, cr=3.3, ml=11.2, md=5.4, mt=3.3, drop=0.6, jaw=1.2),
        ear=dict(h=3.8, w=2.4, lean=6.0),
        tail=dict(len=14.0, a0=70.0, bend=3.0, r=(1.4, 2.5, 1.1), widest=0.6),
        throat=1.2,
        marks=[tail_hair(0.15), muzzle(-9.8, 0.6, 2.6), socks(4.6)],
        action=dict(tilt=6.0, neck=2.0, tail=-12.0, ear=-10.0, paw=(30.0, -95.0)),
        ow_end=dict(head=1.8),
    ),
    # Hypohippus, Miocene Great Plains (~17-11 Ma), ~200 kg: a large
    # anchitheriine horse that stayed a forest browser: robust body, broad
    # three-toed feet with the side toes on the ground, low-crowned teeth, so a
    # moderate face without the grazers' deep jaw. Coat speculative: dark brown
    # with the forest dapples kept (a woodland horse), shaggier short mane.
    "hypohippus": dict(
        ramps={
            "outline": ramp("1e140e"),
            "fur": ramp("4a3022", "6c4832", "8e6446", "ae8462"),
            "pale": ramp("b89c80", "dccaae"),
            "dark": ramp("261a14", "3e2a1e"),
            "mane": ramp("261a14", "3e2a1e", "5a3e2c"),
            "hoof": ramp("5c5248", "908676"),
            "white": ramp("f6eee0"),
        },
        front=1.08, back=1.12, icon=0.52,
        shiny={"fur": dict(deg=8, sat=0.35, val=1.25), "pale": dict(deg=0, sat=0.5, val=1.05)},
        body=dict(L=22.0, top_s=-9.0, top_h=-9.2, chest=13.0, waist=11.5, hip=12.0, sag=0.4, k=0.28,
                  chest_w=1.05),
        leg=dict(h=14.0, fr=(3.0, 2.1, 1.15, 1.3), hr=(3.3, 2.2, 1.15, 1.3), pas=2.2, slope=0.8, hoof=(2.6, 1.7),
                 toes=(3, 3), side=(0.6, 0.5), stifle=3.0, hock=2.4),
        neck=dict(pts=[(1.0, 5.0), (-4.0, -1.6), (-6.4, -6.6)], r=[5.6, 4.4, 3.4]),
        mane=dict(r=1.3, off=1.0),
        head=dict(dx=-1.2, dy=-1.5, face=36.0, cr=3.6, ml=10.6, md=5.4, mt=3.4, drop=0.5, jaw=1.0),
        ear=dict(h=3.8, w=2.6, lean=8.0),
        tail=dict(len=14.0, a0=68.0, bend=4.0, r=(1.5, 2.4, 1.1), widest=0.55),
        throat=0.8,
        marks=[tail_hair(0.2), muzzle(-9.4, 0.7, 2.5), socks(4.0),
               dapples((4.4, 3.2), 0.85, (-9.0, 13.0), above=-2.2)],
        action=dict(tilt=-14.0, neck=-8.0, tail=-14.0, ear=-8.0),
        ow_end=dict(head=1.8, body=1.1),
    ),
    # Cormohipparion occidentale, Ashfall (~12 Ma), ~100 kg: a slender,
    # gazelle-like hipparionine grazer with long thin legs, a long face with a
    # deep preorbital fossa in front of the eye, high-crowned teeth and three
    # toes (side toes lifted). Coat speculative: pale fawn-grey with faint leg
    # bars and a dark face pit (the fossa), upright mane.
    "cormohippari": dict(
        ramps={
            "outline": ramp("201814"),
            "fur": ramp("6a5442", "907660", "b49a80", "d2bca0"),
            "pale": ramp("d6c6ae", "f0e6d4"),
            "dark": ramp("2a221c", "4a3c32"),
            "mane": ramp("2a221c", "4a3c32", "6a5a4a"),
            "hoof": ramp("5c5248", "908676"),
            "white": ramp("f8f2e6"),
        },
        front=1.12, back=1.17, icon=0.54,
        shiny={"fur": dict(deg=20, sat=1.5, val=0.95), "mane": dict(deg=10, sat=1.3, val=1.1)},
        body=dict(L=20.0, top_s=-8.0, top_h=-8.2, chest=10.8, waist=8.6, hip=10.0, sag=0.3, k=0.28),
        leg=dict(h=16.0, fr=(2.3, 1.6, 0.85, 1.0), hr=(2.7, 1.7, 0.85, 1.0), pas=2.3, slope=0.9, hoof=(2.1, 1.5),
                 toes=(3, 3), side=(0.4, 1.7), stifle=2.6, hock=2.2),
        neck=dict(pts=[(1.0, 4.4), (-3.6, -1.8), (-6.0, -7.0)], r=[4.6, 3.6, 2.9]),
        mane=dict(r=1.4, off=1.0, up=True),
        head=dict(dx=-1.1, dy=-1.4, face=36.0, cr=3.2, ml=11.0, md=5.0, mt=3.0, drop=0.6, jaw=1.15),
        ear=dict(h=4.0, w=2.4, lean=6.0),
        tail=dict(len=14.0, a0=66.0, bend=3.0, r=(1.3, 2.3, 1.0), widest=0.6),
        throat=0.6,
        marks=[tail_hair(0.15), muzzle(-9.6, 0.6, 2.4),
               dict(on="head", kind="ell", e=(-3.6, -0.6, 1.6, 0.9, -8), ramp="dark"),  # preorbital fossa
               socks(2.6),
               dict(on="legs", kind="bars", period=2.6, width=1.0, top=10.0, ramp="mane")],
        action=dict(tilt=16.0, neck=6.0, tail=-16.0, ear=-12.0),
        ow_end=dict(head=1.8, legs=0.95),
    ),
    # Equus (Natural Trap Cave, ~20 ka), ~300 kg: a caballine horse, one toe
    # per foot, long face with a deep jaw, upright mane. Coat: dun with the
    # primitive markings (dark dorsal stripe, mane, tail and lower legs, faint
    # leg bars) and a pale mealy muzzle, as in Przewalski's horse; ancient DNA
    # shows dun and bay in Pleistocene horses. Variant: a paler grullo-like dun.
    "equus": dict(
        ramps={
            "outline": ramp("22180f"),
            "fur": ramp("6e5434", "94744c", "b89868", "d4b88a"),
            "pale": ramp("c8b08c", "e8dcc0"),
            "dark": ramp("2a201a", "483628"),
            "mane": ramp("2e241c", "4e3e30", "6e5a46"),
            "hoof": ramp("5c5248", "908676"),
            "white": ramp("f6f0e2"),
        },
        front=1.1, back=1.15, icon=0.53,
        shiny={"fur": dict(deg=0, sat=0.3, val=1.05), "pale": dict(deg=0, sat=0.5, val=1.0)},
        body=dict(L=22.0, top_s=-9.0, top_h=-9.0, chest=12.5, waist=10.5, hip=11.5, sag=0.3, k=0.28),
        leg=dict(h=16.0, toes=(1, 1), fr=(2.8, 1.9, 1.0, 1.2), hr=(3.0, 2.0, 1.0, 1.2), hoof=(2.6, 1.8)),
        neck=dict(pts=[(1.0, 5.0), (-4.0, -2.0), (-7.0, -8.0)], r=[5.5, 4.2, 3.3]),
        mane=dict(r=2.0, off=1.0, up=True),
        head=dict(dx=-1.0, dy=-1.5, face=40.0, cr=3.4, ml=12.0, md=5.6, mt=3.6, jaw=1.25),
        tail=dict(len=15.0, a0=72.0, bend=3.0, r=(1.4, 2.6, 1.2), widest=0.6),
        throat=99.0,
        marks=[tail_hair(0.12),
               dict(on="torso", kind="dorsal", w=1.9, ramp="dark"),
               socks(5.0),
               dict(on="legs", kind="bars", period=2.4, width=0.9, top=11.0, ramp="mane"),
               muzzle(-10.4, 0.6, 2.8)],
        action=dict(tilt=8.0, neck=3.0, tail=-12.0, ear=-10.0, paw=(30.0, -95.0)),
        ow_end=dict(head=1.7),
    ),
}

for _k in ("mesohippus", "protohippus", "hypohippus", "cormohippari"):
    SPECS[_k]["footprint"] = FOOTPRINT_THREE_TOED
