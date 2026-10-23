"""Part 3: NEW species, appended after every existing species.

APPEND-ONLY. Add new species at the END of this list and never reorder or delete
entries: a species' position in the global list is its species ID and dex number
(see the ORDER RULE in roster/__init__.py). This holds even for a species that
belongs to Act 1: it goes here, not into that act's module. Same fields as the
other modules (documented in roster/__init__.py).

C1 (docs/strata_outline.md §2.12): the 17 species below, in outline order. Masses
flagged mass_est are our own size-comparison estimates. ⚠ entries of the outline
carry their caveat in `notes` (shown in the Codex).
"""

SPECIES = [
    # ------------------------------------------------------------------
    # Act 1: Hell Creek
    # ------------------------------------------------------------------
    dict(
        name="Avisaurus", genus="Avisaurus archibaldi", site="Hell Creek Fm, MT", age="~66 Ma",
        first_era="HELL_CREEK", diet="CARNIVORE",  # grasping feet: maybe raptor-like (debated)
        mass=1.0, length=0.4, mass_est=True,
        weights=dict(hp=4, atk=5, defn=3, spa=5, spd=4, spe=7),
        types=("FLYING", "DARK"), abilities=("KEEN_EYE", "SNIPER"),
        category="Tree Bird", color="BROWN", growth="MEDIUM_FAST", catch=120, gender=50,
        borrow="taillow",
        moves=[(1, "PECK"), (1, "LEER"), (4, "QUICK_ATTACK"), (7, "WING_ATTACK"), (10, "PURSUIT"),
               (13, "AERIAL_ACE"), (17, "NIGHT_SLASH")],
        dex="An enantiornithine, or opposite bird, known mostly from its feet. These tree-perching birds all died out with the dinosaurs.",
        notes="Known from foot bones (tarsometatarsi): size and a raptor-like habit are debated. "
              "Loss of tree-dwelling birds at the K-Pg: forest-collapse hypothesis (Field et al. 2018).",
    ),

    # ------------------------------------------------------------------
    # Act 4: Bighorn Basin, PETM
    # ------------------------------------------------------------------
    dict(
        name="Paramys", genus="Paramys", site="Willwood Fm, WY", age="~56-50 Ma",
        first_era="BIGHORN_PETM",
        mass=2.0, length=0.6, mass_est=True,
        weights=dict(hp=4, atk=5, defn=4, spa=4, spd=4, spe=7),
        types=("NORMAL",), abilities=("RUN_AWAY", "PICKUP"),
        category="Early Rodent", color="BROWN", growth="MEDIUM_FAST", catch=200, gender=50,
        borrow="sentret",
        moves=[(1, "TACKLE"), (1, "TAIL_WHIP"), (20, "HYPER_FANG"), (24, "BULLET_SEED"), (28, "DIG"),
               (32, "SUPER_FANG")],
        dex="A squirrel-like early rodent. Rodents reached North America just before the PETM, then spread fast through the Eocene forests.",
        notes="The oldest North American rodents (Acritoparamys) are Clarkforkian, ~57 Ma, just before "
              "the PETM. Stand-in grade for the Ischyromys line, not a proven ancestor.",
    ),
    dict(
        name="Oxyaena", genus="Oxyaena", site="Willwood Fm, WY", age="~56-52 Ma",
        first_era="BIGHORN_PETM", diet="CARNIVORE",
        mass=20.0, length=1.0, mass_est=True,
        weights=dict(hp=5, atk=7, defn=4, spa=3, spd=4, spe=5),
        types=("DARK",), abilities=("STRONG_JAW", "STAKEOUT"),
        category="Oxyaenid", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="sneasel",
        moves=[(1, "SCRATCH"), (1, "BITE"), (22, "PURSUIT"), (25, "SLASH"), (28, "CRUNCH"),
               (32, "JAW_LOCK"), (36, "THROAT_CHOP")],
        dex="A wolverine-like hunter with a long body and short, strong jaws. Not a carnivoran: it is from an older, extinct branch.",
        notes="Oxyaenids and hyaenodonts were once grouped as 'creodonts'; whether they form one group is debated.",
    ),

    # ------------------------------------------------------------------
    # Act 5: Green River and the Bridger Basin
    # ------------------------------------------------------------------
    dict(
        name="Omomys", genus="Omomys carteri", site="Bridger Fm, WY", age="~50-47 Ma",
        first_era="GREEN_RIVER", diet="OMNIVORE",  # insects and fruit
        mass=0.25, length=0.3, mass_est=True,
        weights=dict(hp=4, atk=3, defn=3, spa=7, spd=4, spe=7),
        types=("NORMAL", "PSYCHIC"), abilities=("RUN_AWAY", "INFILTRATOR"),
        category="Omomyid", color="BROWN", growth="MEDIUM_SLOW", catch=150, gender=50,
        borrow="pansage",
        moves=[(1, "SCRATCH"), (1, "CONFUSION"), (26, "FURY_SWIPES"), (29, "PSYBEAM"), (32, "ACROBATICS"),
               (36, "PSYCHIC")],
        dex="A small primate that leapt between branches, eating insects and fruit. Omomyids are probably cousins of tarsiers.",
        notes="Stand-in: Teilhardina is an early omomyiform and Omomys a later one; not a proven descendant. "
              "Notharctus is an adapiform, a different (lemur-like) branch (outline §5 H4).",
    ),
    dict(
        name="Hyrachyus", genus="Hyrachyus modestus", site="Bridger Fm, WY", age="~50-46 Ma",
        first_era="GREEN_RIVER",
        mass=70.0, length=1.5, mass_est=True,
        weights=dict(hp=6, atk=5, defn=6, spa=3, spd=5, spe=5),
        types=("GROUND",), abilities=("STURDY", "OBLIVIOUS"),
        category="Stem Rhino", color="GRAY", growth="SLOW", catch=75, gender=50,
        borrow="phanpy",
        moves=[(1, "TACKLE"), (1, "STOMP"), (28, "MUD_SHOT"), (31, "HEADBUTT"), (34, "TAKE_DOWN"),
               (38, "BULLDOZE"), (42, "BODY_SLAM")],
        dex="A lightly built, hornless relative of the early rhinos, about the size of a tapir. True rhinos arose from animals like it.",
        notes="Stand-in grade: a rhinocerotoid, not a proven ancestor of Subhyracodon.",
    ),
    dict(
        name="Patriofelis", genus="Patriofelis ferox", site="Bridger Fm, WY", age="~48-45 Ma",
        first_era="GREEN_RIVER", diet="CARNIVORE",
        mass=70.0, length=1.7, mass_est=True,
        weights=dict(hp=7, atk=8, defn=5, spa=2, spd=5, spe=4),
        types=("DARK", "FIGHTING"), abilities=("STRONG_JAW", "INTIMIDATE"),
        category="Oxyaenid", color="BROWN", growth="SLOW", catch=45, gender=50,
        borrow="litleo",
        moves=[(1, "BITE"), (1, "LEER"), (30, "CRUNCH"), (33, "BRICK_BREAK"), (36, "JAW_LOCK"),
               (40, "BULK_UP"), (44, "CLOSE_COMBAT")],
        dex="A heavy, short-legged oxyaenid as big as a jaguar, with a huge head. It was the top predator of the Bridger Basin.",
        notes="Mass estimated from skull and limb size; published estimates vary widely.",
    ),

    # ------------------------------------------------------------------
    # Act 6: White River
    # ------------------------------------------------------------------
    dict(
        name="Hyaenodon", genus="Hyaenodon horridus", site="Brule Fm, SD", age="~33 Ma",
        first_era="WHITE_RIVER", diet="CARNIVORE",
        mass=40.0, length=1.5, mass_est=True,
        weights=dict(hp=5, atk=8, defn=4, spa=3, spd=4, spe=6),
        types=("DARK",), abilities=("STRONG_JAW", "STAKEOUT"),
        category="Hyaenodont", color="GRAY", growth="SLOW", catch=45, gender=50,
        borrow="mightyena",
        moves=[(1, "BITE"), (1, "LEER"), (34, "PURSUIT"), (36, "CRUNCH"), (40, "PSYCHIC_FANGS"),
               (44, "JAW_LOCK"), (48, "THROAT_CHOP")],
        dex="A long-skulled hunter with shearing teeth. Hyaenodonts were not dogs or hyenas, but an older, unrelated branch of meat eaters.",
    ),
    dict(
        name="Palaeolagus", genus="Palaeolagus haydeni", site="Brule Fm, SD", age="~33 Ma",
        first_era="WHITE_RIVER",
        mass=0.8, length=0.3, mass_est=True,
        weights=dict(hp=4, atk=4, defn=3, spa=4, spd=4, spe=8),
        types=("NORMAL",), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Early Rabbit", color="BROWN", growth="MEDIUM_FAST", catch=255, gender=50,
        borrow="buneary",
        moves=[(1, "TACKLE"), (1, "QUICK_ATTACK"), (32, "DOUBLE_KICK"), (35, "DIG"), (38, "AGILITY"),
               (42, "BOUNCE")],
        dex="An early rabbit with shorter hind legs than today's, so it likely scurried more than it hopped. A very common badlands fossil.",
    ),
    dict(
        name="Douglassciur", genus="Douglassciurus jeffersoni", site="Chadron Fm, Flagstaff Rim, WY", age="~36 Ma",
        first_era="WHITE_RIVER", last_era="WHITE_RIVER",
        mass=0.3, length=0.35, mass_est=True,
        weights=dict(hp=4, atk=4, defn=3, spa=5, spd=4, spe=8),
        types=("NORMAL",), abilities=("RUN_AWAY", "CHEEK_POUCH"),
        category="Squirrel", color="GRAY", growth="MEDIUM_FAST", catch=200, gender=50,
        borrow="pachirisu",
        moves=[(1, "SCRATCH"), (1, "TAIL_WHIP"), (32, "QUICK_ATTACK"), (35, "BULLET_SEED"), (38, "ACROBATICS"),
               (42, "SUPER_FANG")],
        dex="The oldest known squirrel. Its skeleton was already much like a living tree squirrel's, though its skull was more primitive.",
        notes="Stand-in for the prairie-dog line: a tree-squirrel grade, not an ancestor of Cynomys. "
              "Late Eocene (~36 Ma), a little older than the act's beds. Not wild after White River.",
    ),

    # ------------------------------------------------------------------
    # Act 7: Ashfall and the Miocene Great Plains
    # ------------------------------------------------------------------
    dict(
        name="Hypohippus", genus="Hypohippus", site="Miocene Great Plains, NE", age="~17-11 Ma",
        first_era="ASHFALL",
        mass=200.0, length=1.8, mass_est=True,
        weights=dict(hp=6, atk=5, defn=5, spa=4, spd=5, spe=6),
        types=("NORMAL", "GRASS"), abilities=("RUN_AWAY", "SAP_SIPPER"),
        category="Forest Horse", color="BROWN", growth="MEDIUM_SLOW", catch=60, gender=50,
        borrow="ponyta",
        moves=[(1, "DOUBLE_KICK"), (1, "STOMP"), (40, "MAGICAL_LEAF"), (43, "LEAF_BLADE"), (46, "HIGH_HORSEPOWER"),
               (52, "WOOD_HAMMER")],
        dex="A big three-toed horse that kept browsing leaves in the woodlands while its grazing cousins took over the grassland.",
        notes="Anchitheriine browser, regional (Great Plains, ~17-11 Ma); not recorded in the Ashfall bed "
              "itself (outline §5 M9). Descends from Miohippus-grade horses, so a Mesohippus branch is a grade.",
    ),
    dict(
        name="Aphelops", genus="Aphelops", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL",
        mass=1500.0, length=3.0, mass_est=True,
        weights=dict(hp=7, atk=6, defn=7, spa=2, spd=6, spe=4),
        types=("GROUND",), abilities=("STURDY", "ROCK_HEAD"),
        category="Rhinoceros", color="GRAY", growth="SLOW", catch=45, gender=50,
        borrow="rhyhorn",
        moves=[(1, "TACKLE"), (1, "STOMP"), (40, "HEADBUTT"), (44, "TAKE_DOWN"), (48, "HIGH_HORSEPOWER"),
               (54, "HEAD_SMASH"), (60, "EARTHQUAKE")],
        dex="A long-legged, hornless rhino that browsed in drier, more open country than Teleoceras. Both died out here ~5 million years ago.",
        notes="Much rarer than Teleoceras at Ashfall; the habitat contrast is interpretive. Like Teleoceras, "
              "an immigrant rhino, not a descendant of Subhyracodon (outline §5 M7).",
    ),
    dict(
        name="Cormohippari", genus="Cormohipparion occidentale", site="Ashfall, NE", age="~11.9 Ma",
        first_era="ASHFALL",
        mass=100.0, length=1.6, mass_est=True,
        weights=dict(hp=5, atk=5, defn=4, spa=4, spd=4, spe=8),
        types=("NORMAL", "GRASS"), abilities=("RUN_AWAY", "QUICK_FEET"),
        category="Hipparion", color="BROWN", growth="MEDIUM_SLOW", catch=90, gender=50,
        borrow="blitzle",
        moves=[(1, "DOUBLE_KICK"), (1, "QUICK_ATTACK"), (40, "MAGICAL_LEAF"), (43, "AGILITY"), (46, "BOUNCE"),
               (50, "HIGH_HORSEPOWER")],
        dex="A three-toed grazing horse, the commonest horse in the Ashfall ash. Its relatives spread from North America to Asia and Africa.",
    ),
    dict(
        name="Cosoryx", genus="Cosoryx furcatus", site="Miocene Great Plains, NE", age="~13-11 Ma",
        first_era="ASHFALL",
        mass=20.0, length=1.0, mass_est=True,
        weights=dict(hp=5, atk=5, defn=4, spa=4, spd=4, spe=8),
        types=("NORMAL",), abilities=("RUN_AWAY", "SAP_SIPPER"),
        category="Merycodont", color="BROWN", growth="MEDIUM_FAST", catch=120, gender=50,
        borrow="girafarig",
        moves=[(1, "TACKLE"), (1, "HORN_ATTACK"), (40, "DOUBLE_KICK"), (43, "MAGICAL_LEAF"), (46, "AGILITY"),
               (50, "BOUNCE")],
        dex="A small, deer-like ruminant with forked horns. It belongs to an extinct branch of the pronghorn family, found only in North America.",
        notes="Merycodontine: a stand-in grade for Antilocapra, not its ancestor. Presence in the Ashfall "
              "bed itself unverified (outline §5 M9).",
    ),
    dict(
        name="Macrochelys", genus="Macrochelys", site="Miocene Great Plains, NE", age="~12 Ma",
        first_era="ASHFALL", diet="OMNIVORE",  # fish, plus nuts and fruit
        focal=True,
        mass=80.0, length=0.8,
        weights=dict(hp=6, atk=7, defn=8, spa=3, spd=6, spe=1),
        types=("WATER", "ROCK"), abilities=("STRONG_JAW", "SHELL_ARMOR"),
        category="Lure Snapper", color="BROWN", growth="MEDIUM_SLOW", catch=45, gender=50,
        borrow="carracosta",
        moves=[(1, "BITE"), (1, "WITHDRAW"), (1, "AQUA_JET"), (40, "SUCKER_PUNCH"), (44, "CRUNCH"),
               (48, "JAW_LOCK"), (52, "LIQUIDATION"), (58, "HEAD_SMASH")],
        dex="The alligator snapping turtle lures fish with its worm-like tongue. Its kind lived on the Great Plains; today only in the warm Southeast.",
        notes="Fossils: Macrochelys schmidti, Miocene of Nebraska. Mass is the living species' (big adult "
              "males); the fossil's is unknown. Lost from the north as climates cooled, survives in the SE US.",
    ),

    # ------------------------------------------------------------------
    # Act 8 and the present day
    # ------------------------------------------------------------------
    dict(
        name="Vulpes", genus="Vulpes velox", site="Living; MT", age="today",
        first_era="TRAP_CAVE", diet="OMNIVORE",  # rodents, rabbits, insects, some plants
        focal=True,
        mass=2.2, length=0.8,
        weights=dict(hp=4, atk=5, defn=3, spa=6, spd=4, spe=8),
        types=("NORMAL", "DARK"), abilities=("QUICK_FEET", "RUN_AWAY"),
        category="Swift Fox", color="YELLOW", growth="MEDIUM_SLOW", catch=45, gender=50,
        borrow="fennekin",
        moves=[(1, "QUICK_ATTACK"), (1, "BITE"), (1, "HOWL"), (40, "ASSURANCE"), (44, "AGILITY"),
               (48, "CRUNCH"), (52, "SUCKER_PUNCH")],
        dex="The swift fox, a small fox of the shortgrass prairie. Poisoning and trapping nearly wiped it out; reintroductions brought it back.",
        notes="Stand-in for the fox branch of the Leptocyon grade. Reintroduced in Canada from 1983 and in "
              "Montana from 1998 (Blackfeet Nation); check dates with state sources (outline §5 M12).",
    ),
    dict(
        name="Centrocercus", genus="Centrocercus urophasianus", site="Living; MT", age="today",
        first_era="TRAP_CAVE",  # adults eat sagebrush; chicks eat insects
        focal=True,
        mass=2.5, length=0.7,
        weights=dict(hp=5, atk=4, defn=4, spa=4, spd=5, spe=6),
        types=("NORMAL", "FLYING"), abilities=("KEEN_EYE", "OWN_TEMPO"),
        category="Sage-Grouse", color="GRAY", growth="MEDIUM_SLOW", catch=45, gender=50,
        borrow="starly",
        moves=[(1, "PECK"), (1, "GROWL"), (1, "DOUBLE_KICK"), (40, "AERIAL_ACE"), (46, "FEATHER_DANCE"),
               (52, "BRAVE_BIRD"), (58, "SEED_BOMB")],
        dex="The greater sage-grouse. In spring the males puff up and strut on display grounds. It has lost about half of its old range.",
        notes="Mass is a large male's (females ~1.4 kg). Range loss: about 44% (Schroeder et al. 2004).",
    ),
    dict(
        name="Mustela", genus="Mustela nigripes", site="Living; MT", age="today",
        first_era="EPILOGUE", diet="CARNIVORE",  # prairie dogs
        mass=0.9, length=0.55,
        weights=dict(hp=4, atk=6, defn=3, spa=5, spd=4, spe=8),
        types=("DARK",), abilities=("STAKEOUT", "INFILTRATOR"),
        category="Ferret", color="BROWN", growth="MEDIUM_FAST", catch=45, gender=50,
        borrow="furret",
        moves=[(1, "SCRATCH"), (1, "BITE"), (46, "DIG"), (48, "SUCKER_PUNCH"), (52, "CRUNCH"),
               (56, "THROAT_CHOP")],
        dex="The black-footed ferret hunts prairie dogs in their burrows. Thought extinct, it was found again in 1981 near Meeteetse, Wyoming.",
        notes="Meeteetse is in the Bighorn Basin (Act 4's basin). Reintroduced in Montana from 1994; "
              "check with USFWS (outline §5 M12).",
    ),
]
