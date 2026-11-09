"""Codex Evidence pages: what each reconstruction rests on (roadmap C14).

Keyed by the species constant (SPECIES_<KEY>, see gen_species.const_name). Every roster
species needs an entry; gen_species.py fails otherwise and writes
src/data/strata_evidence.h, shown by the Codex's EVIDENCE page (src/strata_codex.c).
The page also shows the roster's `genus`, `site`, `age` and `mass_est`, so don't repeat
them here. This file is separate from the roster modules on purpose: other lanes edit
the species lines there.

Fields:
  record    Required. Confidence tag, a few words: how good the material is
            ("well known", "partial skeletons", "teeth and jaws", "living species").
            Shown as "Record: <record>".
  bones     Required. What the reconstruction rests on: the fossil material (and
            where it is, when the roster's site doesn't say it). One or two lines once
            wrapped (about 76 characters).
  inferred  Required (outline 1.2, R-e). What is a best guess: colour, calls,
            behaviour, size... Shown as "Inferred: <inferred>", one line (about 28
            characters).
  standin   Optional. For stand-ins and grades (design doc 8.2): shown as
            "Stand-in: <standin>", one line.
  note      Optional. A caveat line shown as written ("Debated: ...", "Unverified: ...").
  today     Optional. For living ends of a lineage, a status shown on the LINEAGE page
            under "Living today." Up to two lines, split with "\\n".

The wrapped body (bones, inferred, standin, note) must come to 2-4 lines;
test/strata_codex.c checks every line's pixel width. Say less rather than guess:
no specimen numbers or counts unless sure, and hedge debated points.
"""

EVIDENCE = {
    # ---- Hell Creek starters ----
    "CIMOLESTES": dict(
        record="teeth and jaws",
        bones="Teeth and jaw pieces from Hell Creek and other latest Cretaceous beds.",
        inferred="body, habits, fur, mass",
        standin="a grade, not an ancestor",
    ),
    "ASTERIORNIS": dict(
        record="skull and leg bones",
        bones="A near-complete skull and some leg bones in one block of rock.",
        inferred="plumage, calls, habits",
        standin="not from Hell Creek itself",
    ),
    "EMARGINACHEL": dict(
        record="few specimens",
        bones="Shell and skull material from the Hell Creek Fm of Montana.",
        inferred="colour, habits, mass",
        note="Debated: maybe not a snapper",
    ),
    # ---- Hell Creek ----
    "TYRANNOSAUR": dict(
        record="well known",
        bones="Dozens of specimens, a few nearly complete, plus bitten bones and dung.",
        inferred="skin, colour, calls",
    ),
    "TRICERATOPS": dict(
        record="very common",
        bones="Hundreds of skulls and partial skeletons; whole skeletons are rare.",
        inferred="colour, calls, herding",
    ),
    "EDMONTOSAUR": dict(
        record="well known",
        bones="Many skeletons and bonebeds, and rare mummies with skin impressions.",
        inferred="colour, calls",
    ),
    "ANKYLOSAURUS": dict(
        record="partial skeletons",
        bones="A few partial skeletons: skulls, armour and a tail club. No whole one.",
        inferred="size, colour, calls",
    ),
    "PACHYCEPHALO": dict(
        record="mostly skull domes",
        bones="Thick skull domes and a few skulls. The body is barely known.",
        inferred="body, colour, head-butting",
    ),
    "THESCELOSAUR": dict(
        record="good skeletons",
        bones="Several good skeletons. A 'fossil heart' in one is likely just rock.",
        inferred="colour, calls, habits",
    ),
    "ACHERORAPTOR": dict(
        record="jaws and teeth only",
        bones="An upper jaw, lower jaws and many shed teeth. No skeleton yet.",
        inferred="size, feathers, colour",
    ),
    "ANZU": dict(
        record="partial skeletons",
        bones="Three partial skeletons from the Dakotas, together most of the body.",
        inferred="feathers, colour, diet",
    ),
    "DIDELPHODON": dict(
        record="skulls, jaws, teeth",
        bones="Many teeth and jaws; a near-complete skull was described in 2016.",
        inferred="habits, fur, bite force",
    ),
    "MESODMA": dict(
        record="teeth and jaws",
        bones="Teeth and jaws, common in sieved Hell Creek sediment.",
        inferred="body, fur, mass, habits",
        standin="Mesodma-grade after 57 Ma",
    ),
    "CHAMPSOSAUR": dict(
        record="well known",
        bones="Many bones at Hell Creek; whole skeletons come from other beds.",
        inferred="colour, behaviour",
        standin="past its range in the PETM",
    ),
    "BOREALOSUCH": dict(
        record="skulls, partial skeletons",
        bones="Skulls and partial skeletons from Hell Creek and Paleocene beds.",
        inferred="size, colour, habits",
    ),
    "LEPISOSTEUS": dict(
        record="scales and bones",
        bones="Gar scales and bones are common at Hell Creek; living gars show the rest.",
        inferred="species, size",
    ),
    "AVISAURUS": dict(
        record="foot bones only",
        bones="Known from foot bones (tarsometatarsi) found in the Hell Creek Fm.",
        inferred="size, wings, habits, colour",
    ),
    # ---- Corral Bluffs (Paleocene) ----
    "PROTICTIS": dict(
        record="teeth and jaws",
        bones="Mostly teeth and jaws from Paleocene beds in Montana and Wyoming.",
        inferred="build, mass, colour",
        standin="a grade, not an ancestor",
    ),
    "PROTOCHELYD": dict(
        record="shells and bones",
        bones="Shells, skulls and other bones from Paleocene beds of North Dakota.",
        inferred="colour, why the dome",
        standin="a grade, kept past its age",
    ),
    "PURGATORIUS": dict(
        record="teeth, jaws, ankles",
        bones="Teeth and jaws, and ankle bones that show a tree climber.",
        inferred="body, fur, mass",
    ),
    "LOXOLOPHUS": dict(
        record="skulls and jaws",
        bones="Skulls and jaws, some from Corral Bluffs concretions.",
        inferred="body, diet, colour",
    ),
    "CARSIOPTYCH": dict(
        record="skulls and jaws",
        bones="Skulls and jaws from the Denver and San Juan basins.",
        inferred="body, mass, colour",
    ),
    "TAENIOLABIS": dict(
        record="skulls and teeth",
        bones="Skulls and teeth from the Denver and San Juan basins; little else.",
        inferred="body, mass, fur",
    ),
    "EOCONODON": dict(
        record="skulls and jaws",
        bones="Skulls and jaws from the Denver and San Juan basins.",
        inferred="body, hunting",
    ),
    # ---- Bighorn Basin (PETM) ----
    "GASTORNIS": dict(
        record="good skeletons",
        bones="Skulls and fairly complete skeletons from Wyoming and Europe.",
        inferred="diet, colour, calls",
    ),
    "PRESBYORNIS": dict(
        record="thousands of bones",
        bones="Thousands of bones and eggshell in lake-shore bonebeds.",
        inferred="colonies, colour, calls",
    ),
    "GALLINULOID": dict(
        record="a few skeletons",
        bones="A few flattened skeletons from the Green River lake beds.",
        inferred="colour, mass, habits",
        standin="fills a gap to the turkey",
    ),
    "SIFRHIPPUS": dict(
        record="teeth and jaws",
        bones="Teeth and jaws. Tooth size tracks its shrinking in the PETM.",
        inferred="body, coat, colour",
    ),
    "TEILHARDINA": dict(
        record="teeth, jaws, feet",
        bones="Teeth and jaws, and a few ankle and foot bones, from the Willwood Fm.",
        inferred="body, fur, diet",
    ),
    "DIACODEXIS": dict(
        record="a good skeleton",
        bones="Teeth and jaws, and one nearly complete skeleton from Wyoming.",
        inferred="coat, colour, habits",
    ),
    "HYOPSODUS": dict(
        record="very common",
        bones="Teeth and jaws by the thousand, plus skulls and some skeletons.",
        inferred="colour, habits, diet",
    ),
    "CORYPHODON": dict(
        record="well known",
        bones="Many skulls and skeletons from the Willwood and other beds.",
        inferred="habits, colour, skin",
    ),
    "PARAMYS": dict(
        record="skulls, skeletons",
        bones="Teeth and jaws, and some skulls and partial skeletons.",
        inferred="fur, colour, tree life",
        standin="a grade, not an ancestor",
    ),
    "OXYAENA": dict(
        record="skulls, partial skeletons",
        bones="Skulls and partial skeletons from early Eocene Wyoming.",
        inferred="mass, colour, hunting",
    ),
    # ---- Green River and Bridger ----
    "MIACIS": dict(
        record="teeth and skulls",
        bones="Teeth, jaws and skulls. Many old 'Miacis' finds are now other genera.",
        inferred="mass, colour, climbing",
        standin="a grade, not an ancestor",
    ),
    "EOHIPPUS": dict(
        record="well known",
        bones="Many teeth and jaws, and several skeletons from Wyoming.",
        inferred="coat, colour",
    ),
    "ONYCHONYCTER": dict(
        record="two whole skeletons",
        bones="Two near-complete skeletons from the Green River Fm (2008).",
        inferred="echolocation, colour",
    ),
    "HELIOBATIS": dict(
        record="complete skeletons",
        bones="Many complete skeletons from the Fossil Butte lake beds.",
        inferred="colour, behaviour",
    ),
    "KNIGHTIA": dict(
        record="thousands of fish",
        bones="Thousands of complete fish, at times whole schools on one layer.",
        inferred="colour, schooling",
    ),
    "NOTHARCTUS": dict(
        record="skeletons",
        bones="Skulls and near-complete skeletons from the Bridger Basin.",
        inferred="colour, diet, social life",
    ),
    "UINTATHERIUM": dict(
        record="well known",
        bones="Many skulls and some skeletons from Wyoming and Utah.",
        inferred="colour, mass, knob use",
    ),
    "OMOMYS": dict(
        record="teeth, jaws, bones",
        bones="Teeth and jaws, and some limb bones, from the Bridger Fm.",
        inferred="leaping, fur, diet",
        standin="a later omomyid",
    ),
    "HYRACHYUS": dict(
        record="skulls, skeletons",
        bones="Skulls and skeletons from the Bridger Fm and other Eocene beds.",
        inferred="colour, habits",
        standin="a grade, not an ancestor",
    ),
    "PATRIOFELIS": dict(
        record="skulls, partial skeletons",
        bones="Skulls and a few partial skeletons from the Bridger Basin.",
        inferred="mass, hunting, colour",
    ),
    # ---- White River ----
    "HESPEROCYON": dict(
        record="well known",
        bones="Many skulls and several skeletons from the White River beds.",
        inferred="coat, colour, hunting",
        standin="a grade, not an ancestor",
    ),
    "MESOHIPPUS": dict(
        record="well known",
        bones="Many skulls and complete skeletons from the Big Badlands.",
        inferred="coat, colour",
    ),
    "ARCHAEOTHERE": dict(
        record="well known",
        bones="Many skulls and skeletons; bitten bone piles hint at caching.",
        inferred="caching, colour, sounds",
    ),
    "HOPLOPHONEUS": dict(
        record="skulls, skeletons",
        bones="Skulls and skeletons from the White River badlands.",
        inferred="colour, hunting style",
    ),
    "MERYCOIDODON": dict(
        record="very common",
        bones="Thousands of skulls and many skeletons from the badlands.",
        inferred="herding, colour",
    ),
    "SUBHYRACODON": dict(
        record="well known",
        bones="Many skulls and skeletons from the Chadron and Brule beds.",
        inferred="colour, skin",
        standin="a grade, not an ancestor",
    ),
    "POEBROTHERE": dict(
        record="skulls, skeletons",
        bones="Skulls and complete skeletons from the White River Group.",
        inferred="coat, colour, habits",
    ),
    "LEPTOMERYX": dict(
        record="very common",
        bones="Many skulls and skeletons from the White River Group.",
        inferred="coat, colour, habits",
    ),
    "STYLEMYS": dict(
        record="thousands of shells",
        bones="Thousands of shells, many whole; skulls and limbs are rarer.",
        inferred="colour, habits",
    ),
    "ISCHYROMYS": dict(
        record="skulls, skeletons",
        bones="Skulls and partial skeletons from the White River Group.",
        inferred="fur, colour, habits",
    ),
    "HYAENODON": dict(
        record="well known",
        bones="Many skulls and skeletons from the White River badlands.",
        inferred="coat, colour, hunting",
    ),
    "PALAEOLAGUS": dict(
        record="very common",
        bones="Many skulls and skeletons, among the commonest small fossils.",
        inferred="fur, colour, gait",
    ),
    "DOUGLASSCIUR": dict(
        record="one skeleton",
        bones="One near-complete skeleton from Flagstaff Rim, Wyoming.",
        inferred="fur, colour, habits",
        standin="a tree squirrel grade",
    ),
    # ---- Ashfall ----
    "EPICYON": dict(
        record="skulls, partial skeletons",
        bones="Skulls, jaws and partial skeletons from the Great Plains.",
        inferred="coat, colour, pack life",
    ),
    "LEPTOCYON": dict(
        record="skulls and jaws",
        bones="Skulls, jaws and teeth from Miocene beds of the Great Plains.",
        inferred="body, coat, colour",
        standin="a grade near the root",
    ),
    "CHELYDRA": dict(
        record="living species",
        bones="Living. The genus is known from the Miocene; the species is younger.",
        inferred="how old the species is",
    ),
    "PROTOHIPPUS": dict(
        record="complete skeletons",
        bones="Complete skeletons buried in the Ashfall ash bed.",
        inferred="coat, colour",
        standin="a grade, near the Equus line",
    ),
    "TELEOCERAS": dict(
        record="100+ skeletons",
        bones="Over 100 skeletons at Ashfall, some females with unborn young.",
        inferred="skin, hair, colour",
        standin="immigrant, not a descendant",
    ),
    "PROCAMELUS": dict(
        record="skeletons",
        bones="Skeletons in the Ashfall bed and other Miocene sites.",
        inferred="coat, hump, colour",
    ),
    "BALEARICA": dict(
        record="skeletons",
        bones="Crane skeletons in the Ashfall ash, at the old waterhole.",
        inferred="crown, colour, calls",
    ),
    "ANCHIGYPS": dict(
        record="fragments",
        bones="Fragmentary wing and leg bones and part of a beak, from Nebraska.",
        inferred="habits, colour, size",
    ),
    "HYPOHIPPUS": dict(
        record="skulls, skeletons",
        bones="Skulls and skeletons from the Plains; listed in the Ashfall ash bed.",
        inferred="coat, woodland life",
        standin="a branch via Miohippus kin",
    ),
    "APHELOPS": dict(
        record="skeletons",
        bones="Skeletons at Ashfall, much rarer there than Teleoceras.",
        inferred="habitat, colour, skin",
        standin="immigrant, not a descendant",
    ),
    "CORMOHIPPARI": dict(
        record="many skeletons",
        bones="Many complete skeletons in the Ashfall ash bed, beside other horses.",
        inferred="coat, stripes, colour",
    ),
    "COSORYX": dict(
        record="horns, jaws, bones",
        bones="Horns, jaws and limb bones from the Miocene Great Plains.",
        inferred="coat, colour, habits",
        standin="a side branch, no ancestor",
    ),
    "MACROCHELYS": dict(
        record="partial fossils",
        bones="A skull from the Marsland Fm of Nebraska, and other Plains fossils.",
        inferred="mass (living kind's), lure",
        standin="an older fossil, not Ashfall",
        today="It lives on only in the warm\nSoutheast US, far from Montana.",
    ),
    # ---- Natural Trap Cave (Ice Age) ----
    "AENOCYON": dict(
        record="very well known",
        bones="Thousands of bones from La Brea, and ancient DNA (2021).",
        inferred="coat, pack life",
        note="Thin record at the cave; debated",
    ),
    "CANIS": dict(
        record="living species",
        bones="A living species. Ice Age coyote fossils are known across the West.",
        inferred="little, it lives today",
    ),
    "MELEAGRIS": dict(
        record="living species",
        bones="A living bird; Ice Age turkey bones come from caves and tar pits.",
        inferred="little, it lives today",
        note="Unconfirmed at Natural Trap Cave",
    ),
    "EQUUS": dict(
        record="many bones",
        bones="Many bones at Natural Trap Cave, from more than one horse form.",
        inferred="coat colour, species",
        today="Gone from the Americas by about\n11 ka; back with the Spanish, 1500s.",
    ),
    "ARCTODUS": dict(
        record="skulls, skeletons",
        bones="Skulls and partial skeletons from caves and tar pits.",
        inferred="diet, hunting or scavenging",
    ),
    "MIRACINONYX": dict(
        record="skulls, skeletons",
        bones="Skulls and skeletons, many from Natural Trap Cave.",
        inferred="speed, coat, prey",
    ),
    "PANTHERA": dict(
        record="very well known",
        bones="Many individuals at La Brea; also at Natural Trap Cave.",
        inferred="mane, coat, social life",
    ),
    "MAMMUTHUS": dict(
        record="well known",
        bones="Many skeletons across the West; Wyoming has the Colby site.",
        inferred="hair, colour",
        note="At the cave: genus only",
    ),
    "CAMELOPS": dict(
        record="skulls, skeletons",
        bones="Skulls, skeletons and teeth from across the Ice Age West.",
        inferred="hump, coat, colour",
    ),
    "BOOTHERIUM": dict(
        record="skulls and partial bones",
        bones="Listed at Natural Trap Cave, and widely across Ice Age North America.",
        inferred="coat, colour, habits",
    ),
    "OVIS": dict(
        record="living species",
        bones="A living species; bighorn bones are known from Ice Age caves.",
        inferred="little, it lives today",
    ),
    "ANTILOCAPRA": dict(
        record="living species",
        bones="A living species; Ice Age pronghorn fossils are known too.",
        inferred="why it is so fast",
    ),
    "CYNOMYS": dict(
        record="living species",
        bones="A living species, studied in its towns for decades.",
        inferred="little, it lives today",
    ),
    "VULPES": dict(
        record="living species",
        bones="A living species, nearly lost and then brought back.",
        inferred="little, it lives today",
        standin="the fox branch of the grade",
    ),
    "CENTROCERCUS": dict(
        record="living species",
        bones="A living bird, watched on its spring display grounds.",
        inferred="little, it lives today",
        standin="the grouse branch",
    ),
    # ---- Today ----
    "BISON": dict(
        record="living species",
        bones="A living species; Ice Age bison fossils are abundant.",
        inferred="little, it lives today",
    ),
    "MUSTELA": dict(
        record="living species",
        bones="A living species, found again in 1981 near Meeteetse, WY.",
        inferred="little, it lives today",
    ),
}
