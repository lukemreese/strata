"""Act 7: Ashfall Fossil Beds, NE (~11.9 Ma).

Species of this section only, in global-order position (see roster/__init__.py).
Fields are documented there.
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Act 7: Ashfall Fossil Beds, NE (~11.9 Ma)
    # Grassland waterhole buried by ash from a Yellowstone-hotspot eruption in Idaho.
    # ------------------------------------------------------------------
    dict(
        name="Protohippus", genus="Protohippus simus", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL",
        mass=100.0, length=1.6, mass_est=True,
        weights=dict(hp=6, atk=5, defn=4, spa=4, spd=4, spe=8),
        types=("NORMAL", "GRASS"), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Grazer", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="rapidash",
        moves=[(1, "DOUBLE_KICK"), (1, "STOMP"), (40, "HIGH_HORSEPOWER"), (44, "LEAF_BLADE"), (48, "BOUNCE"),
               (54, "DOUBLE_EDGE")],
        dex="A pony-sized three-toed grazer with tall, grinding teeth. As grasslands spread, horses evolved to eat grass.",
        notes="High-crowned (hypsodont) teeth as a response to grass and grit.",
    ),
    dict(
        name="Teleoceras", genus="Teleoceras major", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL",
        mass=1800.0, length=4.0, mass_est=True,
        weights=dict(hp=8, atk=6, defn=7, spa=2, spd=6, spe=2),
        types=("GROUND", "WATER"), abilities=("THICK_FAT", "STURDY"),
        category="Rhinoceros", color="GRAY", growth="SLOW", catch=45, gender=50,
        borrow="rhydon",
        moves=[(1, "HORN_ATTACK"), (1, "STOMP"), (40, "MUD_SHOT"), (44, "TAKE_DOWN"), (48, "HIGH_HORSEPOWER"),
               (54, "HEAD_SMASH"), (60, "EARTHQUAKE")],
        dex="A barrel-bodied, short-legged rhino that grazed near water. Whole herds lie in the ash at Ashfall, calves beside their mothers.",
    ),
    dict(
        name="Procamelus", genus="Procamelus grandis", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL",
        mass=300.0, length=2.5, mass_est=True,
        weights=dict(hp=6, atk=5, defn=5, spa=4, spd=5, spe=6),
        types=("NORMAL", "GROUND"), abilities=("OBLIVIOUS", "STURDY"),
        category="Camel", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="camerupt",
        moves=[(1, "STOMP"), (1, "SAND_ATTACK"), (40, "BULLDOZE"), (44, "DOUBLE_KICK"), (48, "HIGH_HORSEPOWER"),
               (54, "DOUBLE_EDGE")],
        dex="A llama-like camel of the Miocene grasslands. It walked on padded feet, an early step toward the camels of today.",
    ),
    dict(
        name="Balearica", genus="Balearica exigua", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL", diet="OMNIVORE",  # cranes
        mass=3.5, length=1.0, mass_est=True,
        weights=dict(hp=5, atk=5, defn=4, spa=5, spd=5, spe=6),
        types=("FLYING", "GRASS"), abilities=("KEEN_EYE", "BIG_PECKS"),
        category="Crane", color="GRAY", growth="MEDIUM_FAST", catch=90, gender=50,
        borrow="flamigo",
        moves=[(1, "PECK"), (1, "GROWL"), (40, "FEATHER_DANCE"), (44, "AERIAL_ACE"), (48, "DRILL_PECK"),
               (54, "BRAVE_BIRD")],
        dex="A crowned crane that waded at the waterhole. Its living relatives are found only in Africa today.",
    ),
    dict(
        name="Anchigyps", genus="Anchigyps voorhiesi", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL", diet="CARNIVORE",  # raptor and scavenger
        mass=5.0, length=0.8, mass_est=True,
        weights=dict(hp=5, atk=6, defn=4, spa=4, spd=5, spe=6),
        types=("FLYING", "DARK"), abilities=("KEEN_EYE", "BIG_PECKS"),
        category="Scavenger", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="mandibuzz",
        moves=[(1, "PECK"), (1, "LEER"), (40, "PLUCK"), (44, "AERIAL_ACE"), (48, "SUCKER_PUNCH"),
               (54, "BRAVE_BIRD")],
        dex="An eagle-like bird of prey that also scavenged. It may have fed on the animals dying at the ash-choked waterhole.",
    ),
]
