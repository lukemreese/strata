"""Act 3: Corral Bluffs, Denver Basin, CO (~65.7-65.4 Ma).

Species of this section only, in global-order position (see roster/__init__.py).
Fields are documented there.
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Act 3: Corral Bluffs, Denver Basin, CO (~65.7-65.4 Ma, ~300-700 kyr after the impact)
    # Body sizes rebound: the largest mammals triple in mass (Lyson et al. 2019).
    # ------------------------------------------------------------------
    dict(
        name="Purgatorius", genus="Purgatorius", site="Tullock Fm, MT", age="~65.9 Ma",
        mass=0.04, length=0.15, mass_est=True,
        weights=dict(hp=4, atk=3, defn=3, spa=6, spd=4, spe=7),
        types=("NORMAL", "PSYCHIC"), abilities=("RUN_AWAY", "PICKUP"),
        category="Stem Primate", color="BROWN", growth="MEDIUM_FAST", catch=200, gender=50,
        borrow="pachirisu",
        moves=[(1, "SCRATCH"), (1, "TAIL_WHIP"), (12, "QUICK_ATTACK"), (16, "CONFUSION"), (20, "FURY_SWIPES"),
               (24, "AGILITY"), (28, "PSYBEAM")],
        dex="A tiny tree climber with nimble ankles, close to the ancestor of all primates. It appeared within 140,000 years of the impact.",
    ),
    dict(
        name="Loxolophus", genus="Loxolophus", site="Denver Fm, CO", age="~65.7 Ma",
        mass=3.0, length=0.5, mass_est=True,
        weights=dict(hp=5, atk=5, defn=4, spa=4, spd=4, spe=5),
        types=("NORMAL",), abilities=("PICKUP", "GLUTTONY"),
        category="Condylarth", color="BROWN", growth="MEDIUM_FAST", catch=190, gender=50,
        borrow="zigzagoon",
        moves=[(1, "TACKLE"), (1, "SAND_ATTACK"), (14, "BITE"), (18, "FURY_SWIPES"), (22, "BULLET_SEED"),
               (26, "CRUNCH"), (30, "BODY_SLAM")],
        dex="A raccoon-sized omnivore of the recovering forests. It ate whatever the new world offered: fruit, roots and small animals.",
    ),
    dict(
        name="Carsioptych", genus="Carsioptychus", site="Denver Fm, CO", age="~65.7 Ma",
        mass=6.0, length=0.6, mass_est=True,
        weights=dict(hp=6, atk=5, defn=5, spa=3, spd=5, spe=4),
        types=("GRASS", "NORMAL"), abilities=("THICK_FAT", "GLUTTONY"),
        category="Periptychid", color="BROWN", growth="MEDIUM_FAST", catch=170, gender=50,
        borrow="lechonk",
        moves=[(1, "TACKLE"), (1, "GROWL"), (14, "BULLET_SEED"), (18, "HEADBUTT"), (22, "SEED_BOMB"),
               (26, "TAKE_DOWN"), (32, "BODY_SLAM")],
        dex="A stout plant eater with swollen, crushing cheek teeth. It cracked the hard seeds and nuts of the first post-impact forests.",
    ),
    dict(
        name="Taeniolabis", genus="Taeniolabis taoensis", site="Denver Fm, CO", age="~65.4 Ma",
        mass=30.0, length=0.9, mass_est=True,
        weights=dict(hp=7, atk=6, defn=6, spa=3, spd=5, spe=3),
        types=("NORMAL", "GROUND"), abilities=("THICK_FAT", "STRONG_JAW"),
        category="Multituber", color="BROWN", growth="MEDIUM_FAST", catch=120, gender=50,
        borrow="bidoof",
        moves=[(1, "TACKLE"), (1, "HYPER_FANG"), (16, "DIG"), (20, "BULLET_SEED"), (24, "CRUNCH"),
               (30, "SUPER_FANG"), (36, "BODY_SLAM")],
        dex="A beaver-sized multituberculate, the largest of its kind. It arrived as legumes spread, and gnawed tough plants with chisel teeth.",
    ),
    dict(
        name="Eoconodon", genus="Eoconodon", site="Denver Fm, CO", age="~65.4 Ma",
        mass=30.0, length=1.2, mass_est=True,
        weights=dict(hp=6, atk=7, defn=5, spa=3, spd=4, spe=5),
        types=("DARK", "NORMAL"), abilities=("STRONG_JAW", "INTIMIDATE"),
        category="Triisodont", color="BROWN", growth="SLOW", catch=45, gender=50,
        borrow="stoutland",
        moves=[(1, "BITE"), (1, "LEER"), (18, "PURSUIT"), (22, "CRUNCH"), (26, "SLASH"),
               (30, "JAW_LOCK"), (36, "THROAT_CHOP")],
        dex="A wolf-sized meat eater with heavy jaws. It was among the first large predators to appear after the dinosaurs were gone.",
    ),
]
