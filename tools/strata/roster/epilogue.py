"""Epilogue: the present-day Montana prairie.

Species of this section only, in global-order position (see roster/__init__.py).
Fields are documented there.
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Present day (epilogue): the Montana prairie
    # ------------------------------------------------------------------
    dict(
        name="Antilocapra", genus="Antilocapra americana", site="Living; MT", age="today",
        first_era="TRAP_CAVE",
        mass=50.0, length=1.4,
        weights=dict(hp=5, atk=5, defn=4, spa=4, spd=4, spe=10),
        types=("NORMAL",), abilities=("SPEED_BOOST", "RUN_AWAY"),
        category="Pronghorn", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="wyrdeer",
        moves=[(1, "QUICK_ATTACK"), (1, "HORN_ATTACK"), (46, "AGILITY"), (50, "DOUBLE_KICK"), (56, "HIGH_HORSEPOWER")],
        dex="The pronghorn, faster than any predator now alive in North America. Its speed may be a ghost of the extinct American cheetah.",
        notes="'Ghosts of predators past' hypothesis (Byers 1997).",
    ),
    dict(
        name="Bison", genus="Bison bison", site="Living; MT", age="today",
        first_era="EPILOGUE",
        mass=700.0, length=3.0,
        weights=dict(hp=8, atk=7, defn=6, spa=3, spd=6, spe=4),
        types=("NORMAL", "GROUND"), abilities=("THICK_FAT", "RECKLESS"),
        category="Bison", color="BROWN", growth="SLOW", catch=45, gender=50,
        borrow="bouffalant",
        moves=[(1, "HEADBUTT"), (1, "STOMP"), (46, "TAKE_DOWN"), (50, "HIGH_HORSEPOWER"), (56, "HEAD_SMASH")],
        dex="The American bison, the largest land animal in North America today. It survived the Ice Age, and later near-extinction.",
    ),
    dict(
        name="Cynomys", genus="Cynomys ludovicianus", site="Living; MT", age="today",
        first_era="TRAP_CAVE",
        mass=1.0, length=0.4,
        weights=dict(hp=5, atk=4, defn=4, spa=5, spd=5, spe=6),
        types=("NORMAL", "GROUND"), abilities=("RUN_AWAY", "PICKUP"),
        category="Prairie Dog", color="BROWN", growth="MEDIUM_FAST", catch=255, gender=50,
        borrow="skwovet",
        moves=[(1, "TACKLE"), (1, "GROWL"), (40, "DIG"), (44, "HYPER_FANG"), (48, "BULLET_SEED")],
        dex="A burrowing ground squirrel that lives in huge towns. Its alarm calls even say what kind of predator is coming.",
    ),
]
