"""Act 8: Natural Trap Cave, WY (~20 ka).

Species of this section only, in global-order position (see roster/__init__.py).
Fields are documented there.
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Act 8: Natural Trap Cave, WY (~20 ka)
    # A sinkhole that trapped Ice Age animals for over 100,000 years.
    # ------------------------------------------------------------------
    dict(
        name="Equus", genus="Equus", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE",
        mass=300.0, length=2.2, mass_est=True,
        weights=dict(hp=6, atk=6, defn=5, spa=4, spd=5, spe=8),
        types=("NORMAL", "GRASS"), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Horse", color="BROWN", growth="MEDIUM_SLOW", catch=45, gender=50,
        borrow="mudsdale",
        moves=[(1, "DOUBLE_KICK"), (1, "HIGH_HORSEPOWER"), (46, "LEAF_BLADE"), (50, "BOUNCE"), (54, "DOUBLE_EDGE"),
               (60, "EARTHQUAKE")],
        dex="A one-toed Ice Age horse. Horses died out in North America about 11,000 years ago, then returned with the Spanish in the 1500s.",
        notes="Several Ice Age horse forms at the site, including a small stilt-legged horse.",
    ),
    dict(
        name="Arctodus", genus="Arctodus simus", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE", diet="CARNIVORE",  # carnivore-scavenger (debated)
        mass=900.0, length=3.0, mass_est=True,
        weights=dict(hp=8, atk=8, defn=6, spa=3, spd=5, spe=5),
        types=("DARK", "NORMAL"), abilities=("INTIMIDATE", "THICK_FAT"),
        category="Short-faced", color="BROWN", growth="SLOW", catch=10, gender=50,
        borrow="ursaring",
        moves=[(1, "SLASH"), (1, "SCARY_FACE"), (46, "CRUNCH"), (50, "HAMMER_ARM"), (56, "CRUSH_CLAW"),
               (62, "GIGA_IMPACT")],
        dex="The giant short-faced bear: one of the largest land carnivores of the Ice Age. Standing up, it reached over three metres.",
    ),
    dict(
        name="Miracinonyx", genus="Miracinonyx trumani", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE", diet="CARNIVORE",
        mass=70.0, length=1.6, mass_est=True,
        weights=dict(hp=5, atk=7, defn=4, spa=3, spd=4, spe=9),
        types=("DARK",), abilities=("SPEED_BOOST", "INFILTRATOR"),
        category="Cheetah", color="YELLOW", growth="SLOW", catch=45, gender=50,
        borrow="persian",
        moves=[(1, "QUICK_ATTACK"), (1, "SCRATCH"), (46, "NIGHT_SLASH"), (50, "SUCKER_PUNCH"), (54, "AGILITY"),
               (60, "THROAT_CHOP")],
        dex="The American cheetah, a fast cat built much like the African cheetah. It chased pronghorn across the open steppe.",
        notes="Cheetah-like build evolved convergently; closest relative is the puma.",
    ),
    dict(
        name="Panthera", genus="Panthera atrox", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE", diet="CARNIVORE",
        mass=350.0, length=2.5, mass_est=True,
        weights=dict(hp=6, atk=8, defn=5, spa=3, spd=5, spe=6),
        types=("DARK", "FIGHTING"), abilities=("INTIMIDATE", "MOXIE"),
        category="Lion", color="YELLOW", growth="SLOW", catch=25, gender=50,
        borrow="pyroar",
        moves=[(1, "BITE"), (1, "ROAR"), (46, "CRUNCH"), (50, "CLOSE_COMBAT"), (56, "THROAT_CHOP"),
               (62, "GIGA_IMPACT")],
        dex="The American lion, larger than any living lion. It hunted horses and bison across Ice Age North America.",
    ),
    dict(
        name="Mammuthus", genus="Mammuthus columbi", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE",
        mass=9000.0, length=4.5, mass_est=True,
        weights=dict(hp=8, atk=7, defn=6, spa=3, spd=6, spe=3),
        types=("ICE", "GROUND"), abilities=("THICK_FAT", "STURDY"),
        category="Mammoth", color="BROWN", growth="SLOW", catch=25, gender=50,
        borrow="mamoswine",
        moves=[(1, "STOMP"), (1, "ICE_SHARD"), (46, "AVALANCHE"), (50, "HIGH_HORSEPOWER"), (56, "ICICLE_CRASH"),
               (62, "EARTHQUAKE")],
        dex="The Columbian mammoth, taller than an African elephant. It grazed the grasslands south of the ice sheets.",
    ),
    dict(
        name="Camelops", genus="Camelops", site="Wyoming", age="~20 ka",
        first_era="TRAP_CAVE",
        mass=800.0, length=3.0, mass_est=True,
        weights=dict(hp=7, atk=6, defn=5, spa=3, spd=6, spe=5),
        types=("NORMAL", "GROUND"), abilities=("OBLIVIOUS", "THICK_FAT"),
        category="Camel", color="BROWN", growth="MEDIUM_SLOW", catch=45, gender=50,
        borrow="tauros",
        moves=[(1, "STOMP"), (1, "BULLDOZE"), (46, "DOUBLE_KICK"), (50, "HIGH_HORSEPOWER"), (56, "DOUBLE_EDGE")],
        dex="The western camel, the last of the camels' long North American story. It vanished with the other Ice Age giants.",
    ),
    dict(
        name="Ovibos", genus="Ovibos moschatus", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE",
        mass=300.0, length=2.2,
        weights=dict(hp=8, atk=6, defn=7, spa=3, spd=7, spe=3),
        types=("ICE", "NORMAL"), abilities=("THICK_FAT", "SNOW_CLOAK"),
        category="Musk Ox", color="BROWN", growth="SLOW", catch=45, gender=50,
        borrow="dubwool",
        moves=[(1, "HEADBUTT"), (1, "POWDER_SNOW"), (46, "TAKE_DOWN"), (50, "AVALANCHE"), (56, "IRON_HEAD"),
               (62, "HEAD_SMASH")],
        dex="A shaggy, cold-adapted ox. It survives today in the Arctic, far north of where its Ice Age herds once grazed.",
    ),
    dict(
        name="Ovis", genus="Ovis canadensis", site="Natural Trap Cave, WY", age="~20 ka",
        first_era="TRAP_CAVE",
        mass=100.0, length=1.6,
        weights=dict(hp=6, atk=6, defn=6, spa=3, spd=5, spe=6),
        types=("ROCK", "FIGHTING"), abilities=("ROCK_HEAD", "STURDY"),
        category="Bighorn", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="gogoat",
        moves=[(1, "HEADBUTT"), (1, "ROCK_THROW"), (46, "ZEN_HEADBUTT"), (50, "ROCK_SLIDE"), (56, "HEAD_SMASH")],
        dex="The bighorn sheep. Rams clash their curled horns in contests that echo across the cliffs. It still lives in Wyoming today.",
    ),
]
