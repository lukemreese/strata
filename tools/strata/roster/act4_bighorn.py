"""Act 4: Bighorn Basin, WY (PETM, ~56 Ma).

Species of this section only, in global-order position (see roster/__init__.py).
Fields are documented there.
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Act 4: Bighorn Basin, WY, Paleocene-Eocene Thermal Maximum (~56 Ma)
    # Rapid global warming; mammals dwarf, and horses and primates arrive.
    # ------------------------------------------------------------------
    dict(
        name="Sifrhippus", genus="Sifrhippus sandrae", site="Willwood Fm, WY", age="~55.8 Ma",
        mass=4.0, length=0.5,
        weights=dict(hp=4, atk=4, defn=4, spa=4, spd=4, spe=7),
        types=("NORMAL", "GRASS"), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Dawn Horse", color="BROWN", growth="MEDIUM_SLOW", catch=120, gender=50,
        borrow="ponyta",
        moves=[(1, "TACKLE"), (1, "TAIL_WHIP"), (20, "DOUBLE_KICK"), (24, "QUICK_ATTACK"), (28, "MAGICAL_LEAF"),
               (32, "AGILITY"), (36, "STOMP")],
        dex="The earliest horse in North America, about the size of a cat. It shrank by a third as the PETM heat peaked, then grew again.",
        notes="Dwarfing during the PETM: Secord et al. 2012.",
    ),
    dict(
        name="Teilhardina", genus="Teilhardina brandti", site="Willwood Fm, WY", age="~55.8 Ma",
        mass=0.03, length=0.1, mass_est=True,
        weights=dict(hp=4, atk=3, defn=3, spa=7, spd=4, spe=7),
        types=("NORMAL", "PSYCHIC"), abilities=("RUN_AWAY", "INFILTRATOR"),
        category="True Primate", color="BROWN", growth="MEDIUM_SLOW", catch=150, gender=50,
        borrow="aipom",
        moves=[(1, "SCRATCH"), (1, "CONFUSION"), (20, "QUICK_ATTACK"), (24, "FURY_SWIPES"), (28, "PSYBEAM"),
               (32, "AGILITY"), (36, "PSYCHIC")],
        dex="One of the earliest true primates, a mouse-sized tree dweller. Primates spread across the northern continents in the PETM heat.",
    ),
    dict(
        name="Diacodexis", genus="Diacodexis ilicis", site="Willwood Fm, WY", age="~55.8 Ma",
        mass=2.0, length=0.5, mass_est=True,
        weights=dict(hp=4, atk=4, defn=3, spa=4, spd=4, spe=8),
        types=("NORMAL",), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Artiodactyl", color="BROWN", growth="MEDIUM_FAST", catch=150, gender=50,
        borrow="skiddo",
        moves=[(1, "TACKLE"), (1, "GROWL"), (20, "DOUBLE_KICK"), (24, "QUICK_ATTACK"), (28, "AGILITY"),
               (32, "BOUNCE"), (36, "HIGH_JUMP_KICK")],
        dex="A rabbit-sized, long-legged runner. It is the oldest known even-toed hoofed mammal: the group that includes pigs, deer and whales.",
    ),
    dict(
        name="Hyopsodus", genus="Hyopsodus", site="Willwood Fm, WY", age="~55 Ma",
        mass=1.0, length=0.35, mass_est=True,
        weights=dict(hp=5, atk=4, defn=4, spa=4, spd=5, spe=5),
        types=("NORMAL", "GROUND"), abilities=("PICKUP", "RUN_AWAY"),
        category="Condylarth", color="BROWN", growth="MEDIUM_FAST", catch=200, gender=50,
        borrow="furret",
        moves=[(1, "TACKLE"), (1, "SAND_ATTACK"), (20, "DIG"), (24, "BITE"), (28, "FURY_SWIPES"),
               (32, "BULLET_SEED"), (36, "BODY_SLAM")],
        dex="A small, long-bodied omnivore. It is one of the most common fossils in the Eocene rocks of Wyoming.",
    ),
    dict(
        name="Coryphodon", genus="Coryphodon", site="Willwood Fm, WY", age="~55 Ma",
        mass=500.0, length=2.3, mass_est=True,
        weights=dict(hp=8, atk=6, defn=7, spa=2, spd=6, spe=2),
        types=("GROUND", "WATER"), abilities=("THICK_FAT", "STURDY"),
        category="Pantodont", color="GRAY", growth="SLOW", catch=45, gender=50,
        borrow="hippowdon",
        moves=[(1, "TACKLE"), (1, "STOMP"), (24, "MUD_SHOT"), (28, "BITE"), (32, "TAKE_DOWN"),
               (36, "CRUNCH"), (42, "BODY_SLAM"), (48, "EARTHQUAKE")],
        dex="A hippo-like giant with tusks and a tiny brain. It wallowed in the warm swamps and was the largest animal of its world.",
    ),
]
