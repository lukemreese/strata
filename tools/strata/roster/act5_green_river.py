"""Act 5: Green River lakes and Bridger Basin, WY (~52-46 Ma).

Species of this section only, in global-order position (see roster/__init__.py).
Fields are documented there.
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Act 5: Green River lakes and Bridger Basin, WY (~52-46 Ma)
    # Huge subtropical lakes; fine-grained lake beds preserve whole skeletons.
    # ------------------------------------------------------------------
    dict(
        name="Eohippus", genus="Eohippus angustidens", site="Wind River Fm, WY", age="~52 Ma",
        first_era="GREEN_RIVER",
        mass=10.0, length=0.6, mass_est=True,
        weights=dict(hp=5, atk=5, defn=4, spa=4, spd=4, spe=7),
        types=("NORMAL", "GRASS"), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Dawn Horse", color="BROWN", growth="MEDIUM_SLOW", catch=90, gender=50,
        borrow="blitzle",
        moves=[(1, "TACKLE"), (1, "DOUBLE_KICK"), (28, "QUICK_ATTACK"), (32, "MAGICAL_LEAF"), (36, "STOMP"),
               (40, "AGILITY"), (44, "BOUNCE")],
        dex="A fox-sized forest horse with four toes on its front feet. It browsed soft leaves; its low teeth could not handle grass.",
        notes="Often lumped into 'Hyracotherium'; Eohippus is the North American genus.",
    ),
    dict(
        name="Onychonycter", genus="Onychonycteris finneyi", site="Green River Fm, WY", age="~52.5 Ma",
        first_era="GREEN_RIVER", diet="CARNIVORE",  # insects
        mass=0.04, length=0.1, mass_est=True,
        weights=dict(hp=4, atk=4, defn=3, spa=5, spd=4, spe=7),
        types=("FLYING", "DARK"), abilities=("INFILTRATOR", "KEEN_EYE"),
        category="Claw Bat", color="BROWN", growth="MEDIUM_FAST", catch=170, gender=50,
        borrow="zubat",
        moves=[(1, "LEECH_LIFE"), (1, "ASTONISH"), (24, "WING_ATTACK"), (28, "BITE"), (32, "AIR_SLASH"),
               (36, "ACROBATICS"), (40, "CRUNCH")],
        dex="One of the oldest bats. It could fly, and still had claws on every finger. Whether it could echolocate is still debated.",
    ),
    dict(
        name="Heliobatis", genus="Heliobatis radians", site="Green River Fm, WY", age="~52 Ma",
        first_era="GREEN_RIVER", diet="CARNIVORE",  # buried invertebrates
        mass=2.0, length=0.3, mass_est=True,
        weights=dict(hp=5, atk=4, defn=5, spa=6, spd=5, spe=5),
        types=("WATER", "ELECTRIC"), abilities=("POISON_POINT", "SWIFT_SWIM"),
        category="Stingray", color="BROWN", growth="MEDIUM_FAST", catch=150, gender=50,
        borrow="mantyke",
        moves=[(1, "WATER_GUN"), (1, "POISON_STING"), (24, "SHOCK_WAVE"), (28, "BUBBLE_BEAM"), (32, "POISON_JAB"),
               (36, "DISCHARGE"), (42, "SURF")],
        dex="A freshwater stingray with a venomous tail spine. Like living rays it sensed the weak electric fields of buried prey.",
    ),
    dict(
        name="Knightia", genus="Knightia eocaena", site="Green River Fm, WY", age="~51 Ma",
        first_era="GREEN_RIVER", diet="OMNIVORE",  # plankton and small insects
        mass=0.05, length=0.15,
        weights=dict(hp=4, atk=4, defn=4, spa=4, spd=4, spe=7),
        types=("WATER",), abilities=("SWIFT_SWIM", "WATER_VEIL"),
        category="Herring", color="BLUE", growth="FAST", catch=255, gender=50,
        borrow="finneon",
        moves=[(1, "WATER_GUN"), (1, "TACKLE"), (22, "AQUA_JET"), (26, "BUBBLE_BEAM"), (30, "AGILITY"),
               (36, "WATERFALL")],
        dex="A small herring that swam in vast schools. Whole schools died at once and were buried in the lake mud: Wyoming's state fossil.",
    ),
    dict(
        name="Notharctus", genus="Notharctus tenebrosus", site="Bridger Fm, WY", age="~50 Ma",
        first_era="GREEN_RIVER",
        mass=4.0, length=0.9, mass_est=True,
        weights=dict(hp=5, atk=4, defn=4, spa=7, spd=5, spe=6),
        types=("GRASS", "PSYCHIC"), abilities=("INFILTRATOR", "LEAF_GUARD"),
        category="Adapiform", color="BROWN", growth="MEDIUM_SLOW", catch=90, gender=50,
        borrow="passimian",
        moves=[(1, "CONFUSION"), (1, "MAGICAL_LEAF"), (28, "FURY_SWIPES"), (32, "PSYBEAM"), (36, "GIGA_DRAIN"),
               (40, "PSYCHIC"), (46, "LEAF_STORM")],
        dex="A lemur-like primate that leapt through the subtropical canopy, eating leaves. Its grasping hands look much like ours.",
    ),
    dict(
        name="Uintatherium", genus="Uintatherium anceps", site="Bridger Fm, WY", age="~46 Ma",
        first_era="GREEN_RIVER",
        mass=2000.0, length=4.0, mass_est=True,
        weights=dict(hp=7, atk=7, defn=7, spa=2, spd=6, spe=3),
        types=("GROUND", "FIGHTING"), abilities=("STURDY", "INTIMIDATE"),
        category="Uintathere", color="GRAY", growth="SLOW", catch=25, gender=50,
        borrow="rhyperior",
        moves=[(1, "HORN_ATTACK"), (1, "STOMP"), (30, "TAKE_DOWN"), (34, "BULLDOZE"), (38, "CRUNCH"),
               (44, "HIGH_HORSEPOWER"), (50, "HEAD_SMASH")],
        dex="A rhino-sized browser with six bony knobs on its head and long, saber-like upper canines. Its brain was remarkably small.",
    ),
]
