"""Species specs for the turtle body plan (plans/turtle.py). Owned by the aqua
artist. See specs/fish.py for the common keys and the plan docstring for the
knobs.

The snapper line (Emarginachelys -> Protochelydra -> Chelydra / Macrochelys) is
the 'stasis' starter line: the same head, beak, shell pattern, tail crest and
palette structure throughout, with small changes in dome height, keels, head
size and colour. Colour is a reconstruction for the fossil species: olive and
brown like living chelydrids (which are often algae-covered); the tortoise is
tan with darker seams like living Gopherus.
"""

from ..core.color import ramp

# shared by the snapper line; per-species ramps below shift these slightly
_BELLY = ramp("a49c70", "cac090", "ece4bc")
_MOUTH = ramp("c49c8c")

SPECS = {
    # Emarginachelys cretacea, Hell Creek Fm (~66 Ma): the earliest well-known
    # chelydrid-like turtle (Whetstone 1978; some analyses place it nearer the
    # kinosternoids). A small snapper: lowish carapace with three weak keels,
    # slightly serrated rear margin, a large head and a long crested tail. The
    # warmer brown is speculative; the eye is a touch larger (it is the starter).
    "emarginachel": dict(
        ramps={
            "outline": ramp("201a10"),
            "shell": ramp("43351f", "68502e", "8c7042", "b0935e"),
            "skin": ramp("4c4232", "726450", "9a8c6c"),
            "belly": _BELLY,
            "beak": ramp("5a4c34", "907e5a"),
            "eye": ramp("c8a444"),
            "mouth": _MOUTH,
        },
        front=0.86, back=1.2, icon=0.41,
        shiny={"shell": dict(deg=-8, sat=0.55, val=1.12), "skin": dict(deg=-6, sat=0.6, val=1.12)},
        dome=8.4, keel=0.8, serr=2, serr_len=1.8, head=1.0, hook=0.8, tail=1.08, crest=0.75,
        eye_k=1.12, wid=0.80,
    ),
    # Protochelydra zangerli, Paleocene of North Dakota (~60 Ma): a large
    # snapper with an unusually high, domed carapace (Erickson 1973), possibly a
    # defence against the big crocodylians it lived with. Smooth dome, keels
    # nearly worn away, same head and tail as its ancestor.
    "protochelyd": dict(
        ramps={
            "outline": ramp("1e1910"),
            "shell": ramp("41361f", "645232", "887248", "ab9562"),
            "skin": ramp("4b4433", "706651", "968c6d"),
            "belly": _BELLY,
            "beak": ramp("584c34", "8e805c"),
            "eye": ramp("c4a442"),
            "mouth": _MOUTH,
        },
        front=0.86, back=1.18, icon=0.41,
        shiny={"shell": dict(deg=-10, sat=0.5, val=1.14), "skin": dict(deg=-6, sat=0.6, val=1.12)},
        dome=12.2, dome_shape=0.62, peak=0.47, keel=0.5, serr=2, serr_len=2.0, head=1.05, hook=0.9,
        tail=1.0, crest=0.85, wid=0.84,
    ),
    # Chelydra serpentina, living common snapping turtle (Montana today). Olive
    # to dark-brown carapace with three low keels of knobs (worn smooth in old
    # adults), strongly serrated rear margin, big head, long tail with a saw-
    # toothed crest; often algae-covered. Colour from life.
    "chelydra": dict(
        ramps={
            "outline": ramp("1c1c10"),
            "shell": ramp("403e26", "646038", "8a8450", "b2ac70"),
            "skin": ramp("4e4a38", "767256", "9e9878"),
            "belly": ramp("a69e6c", "cac28a", "ece6b6"),
            "beak": ramp("6a6448", "aca478"),
            "eye": ramp("bca23e"),
            "mouth": _MOUTH,
        },
        front=0.86, back=1.18, icon=0.41,
        shiny={"shell": dict(deg=-14, sat=0.5, val=1.18), "skin": dict(deg=-10, sat=0.55, val=1.18)},
        dome=8.8, keel=1.3, serr=3, serr_len=2.6, head=1.12, hook=1.0, tail=1.18, crest=1.0, algae=True,
        wid=0.82,
    ),
    # Macrochelys schmidti, Miocene of Nebraska (~12 Ma); drawn like the living
    # alligator snapper (M. temminckii): a huge triangular head with a strongly
    # hooked beak, eyes on the sides of the head, three rows of tall spiky keels
    # on a dark brown-grey carapace, a shorter crested tail. Frame 2 opens the
    # jaws on the pink, worm-like tongue lure (a living-species trait; assumed).
    "macrochelys": dict(
        ramps={
            "outline": ramp("1a1612"),
            "shell": ramp("36302a", "554b3e", "776a56", "998c72"),
            "skin": ramp("423c34", "665e50", "8a8270"),
            "belly": ramp("9c9478", "beb694", "dcd6b6"),
            "beak": ramp("4e463a", "827a64"),
            "eye": ramp("a89040"),
            "mouth": ramp("d88c8c"),
        },
        front=0.84, back=1.12, icon=0.39,
        shiny={"shell": dict(deg=8, sat=0.8, val=1.18), "skin": dict(deg=6, sat=0.8, val=1.15)},
        dome=8.6, dome_shape=0.85, keel=3.0, keel_w=0.075, serr=3, serr_len=3.0, head=1.42, hook=1.5,
        neck=0.85, neck_up=1, tail=0.95, crest=1.1, gape=30, lure=True, eye_k=0.8, wid=0.86,
    ),
    # Stylemys nebrascensis, Brule Fm (~32 Ma): a gopher-tortoise-sized land
    # tortoise, the commonest Big Badlands fossil. High dome, no keels or
    # serrations, growth annuli on the scutes, a small blunt-beaked head,
    # columnar elephantine legs with scaled forelimbs and a short tail. Tan with
    # dark seams like Gopherus; colour speculative.
    "stylemys": dict(
        ramps={
            "outline": ramp("24180c"),
            "shell": ramp("4e3a20", "7a5a30", "a6804a", "caa66c"),
            "skin": ramp("5e5244", "887a64", "b0a088"),
            "belly": ramp("b29c76", "d2bc92", "f0e0ba"),
            "beak": ramp("5e5038", "948464"),
            "eye": ramp("5a3418"),
            "mouth": ramp("c09080"),
        },
        front=1.08, back=1.25, icon=0.5,
        shiny={"shell": dict(deg=-6, sat=0.55, val=0.78), "skin": dict(deg=0, sat=0.7, val=0.85)},
        legs="tortoise", dome=14.5, dome_shape=0.5, peak=0.5, front_lift=0.6, keel=0.0, serr=0,
        head=0.95, hook=0.0, neck=1.0, neck_up=14, lunge=14, eye_k=0.62, tail=0.32, crest=0.0, tubercles=False,
        rings=True, wid=0.78,
    ),
}
