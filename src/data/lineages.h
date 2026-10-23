// Lineage descent table: what each species becomes when the game enters an era.
// See docs/strata_design.md §4-5 and §7.1-7.3, and tools/strata/roster/ for the species.
// Every descendant must exist by its era (roster `first_era`; test/lineage.c), and
// every species a starter line can become must be `focal=True` in the roster.
// Lineages without an entry for an era are in stasis.
// Extinctions and the era level floors are at the end of this file.
//
// Thresholds: a branch needs its pressure counter at or above its minScore before
// it can beat the default (see Lineage_GetDescendant). DESCENT_MIN_SCORE (64) is
// a deliberate choice: about three forage items (+12 each, R3) plus some time in
// the right habitat, or ~2,000 steps (64 ticks) in one habitat. Knockouts alone
// can't get there: they give ANIMAL pressure only to predators and omnivores and
// stop at SELECTION_PREY_CAP (24), so the dog line reaches the coyote unless the
// player feeds it carrion on purpose. Counters reset only when a lineage
// descends, so each threshold is met over the whole window since the previous
// descent (or the catch), e.g. Acts 1-3 for Asteriornis.

// Dog line: Canidae originated in North America.
static const struct DescentOption sDescent_Cimolestes[] =
{
    DESCENT_DEFAULT(SPECIES_PROTICTIS),
    DESCENT_END,
};

static const struct DescentOption sDescent_Protictis[] =
{
    DESCENT_DEFAULT(SPECIES_MIACIS),
    DESCENT_END,
};

static const struct DescentOption sDescent_Miacis[] =
{
    DESCENT_DEFAULT(SPECIES_HESPEROCYON),
    DESCENT_END,
};

static const struct DescentOption sDescent_Hesperocyon[] =
{
    DESCENT_DEFAULT(SPECIES_LEPTOCYON), // generalist, ancestor of all living canines
    // Bone-crushing borophagine. Steered in Act 6 (Archaeotherium's bone stash).
    DESCENT_BRANCH(SPECIES_EPICYON, PRESSURE_MEAT_DIET, DESCENT_MIN_SCORE),
    DESCENT_END,
};

static const struct DescentOption sDescent_Leptocyon[] =
{
    DESCENT_DEFAULT(SPECIES_CANIS), // coyote, survives to today
    // Dire wolf, megafauna specialist. Steered in Act 7 (carrion).
    DESCENT_BRANCH(SPECIES_AENOCYON, PRESSURE_MEAT_DIET, DESCENT_MIN_SCORE),
    // Swift fox: steered in Act 7's open grassland. Survives, though it was nearly
    // lost in the 20th century. A higher bar than 64: most of Act 7 in the open.
    DESCENT_BRANCH(SPECIES_VULPES, PRESSURE_OPEN, 96),
    DESCENT_END,
};

// Bird line: ground birds survived the impact, then radiated. Window: Acts 1-3.
static const struct DescentOption sDescent_Asteriornis[] =
{
    DESCENT_DEFAULT(SPECIES_GALLINULOID), // forest ground fowl
    // Lake wader: surfing, shores and fishing (waders and fishing kit).
    DESCENT_BRANCH(SPECIES_PRESBYORNIS, PRESSURE_WATER, DESCENT_MIN_SCORE),
    // Flightless giant herbivore: plant forage (R3).
    DESCENT_BRANCH(SPECIES_GASTORNIS, PRESSURE_PLANT_DIET, DESCENT_MIN_SCORE),
    DESCENT_END,
};

// Window: Acts 4-7.
static const struct DescentOption sDescent_Gallinuloid[] =
{
    DESCENT_DEFAULT(SPECIES_MELEAGRIS),
    // Sage-grouse: steered in the White River and Ashfall grasslands.
    DESCENT_BRANCH(SPECIES_CENTROCERCUS, PRESSURE_OPEN, 96),
    DESCENT_END,
};

// Snapping turtle line: stasis, with rare changes.
static const struct DescentOption sDescent_Emarginachel[] =
{
    DESCENT_DEFAULT(SPECIES_PROTOCHELYD),
    DESCENT_END,
};

// Window: Acts 3-6, so the PETM's heat (2 per tick, sEraHeat) counts. A turtle
// carried in the party through the PETM may well get there; banking it in the PC
// (which gains no pressure) keeps the common snapper.
static const struct DescentOption sDescent_Protochelyd[] =
{
    DESCENT_DEFAULT(SPECIES_CHELYDRA),
    // Alligator snapping turtle: Miocene of Nebraska, now only in the warm Southeast.
    DESCENT_BRANCH(SPECIES_MACROCHELYS, PRESSURE_HEAT, 160),
    DESCENT_END,
};

// Horse line: one of the best-documented lineages in the fossil record. Horses
// evolved in North America, browsing in forests, then grazing as grasslands spread.
static const struct DescentOption sDescent_Sifrhippus[] =
{
    DESCENT_DEFAULT(SPECIES_EOHIPPUS),
    DESCENT_END,
};

static const struct DescentOption sDescent_Eohippus[] =
{
    DESCENT_DEFAULT(SPECIES_MESOHIPPUS),
    DESCENT_END,
};

static const struct DescentOption sDescent_Mesohippus[] =
{
    DESCENT_DEFAULT(SPECIES_PROTOHIPPUS), // grazer
    // Anchitheriine browser, steered in Act 6's gallery forest. Dies out by the Ice Age.
    DESCENT_BRANCH(SPECIES_HYPOHIPPUS, PRESSURE_FOREST, DESCENT_MIN_SCORE),
    DESCENT_END,
};

static const struct DescentOption sDescent_Protohippus[] =
{
    DESCENT_DEFAULT(SPECIES_EQUUS),
    DESCENT_END,
};

// Camel line: camels also evolved in North America.
static const struct DescentOption sDescent_Poebrothere[] =
{
    DESCENT_DEFAULT(SPECIES_PROCAMELUS),
    DESCENT_END,
};

static const struct DescentOption sDescent_Procamelus[] =
{
    DESCENT_DEFAULT(SPECIES_CAMELOPS),
    DESCENT_END,
};

// Rhino line. Grades, not ancestors: Hyrachyus is a rhinocerotoid, and the Miocene
// rhinos were immigrants, not Subhyracodon's descendants (outline §5 M7).
static const struct DescentOption sDescent_Hyrachyus[] =
{
    DESCENT_DEFAULT(SPECIES_SUBHYRACODON),
    DESCENT_END,
};

// Both branches die out by the Ice Age: fitness in one era is no guarantee.
static const struct DescentOption sDescent_Subhyracodon[] =
{
    DESCENT_DEFAULT(SPECIES_TELEOCERAS), // barrel-bodied grazer
    // Long-legged hornless browser of open country, steered on the White River flats.
    DESCENT_BRANCH(SPECIES_APHELOPS, PRESSURE_OPEN, DESCENT_MIN_SCORE),
    DESCENT_END,
};

// Primates: from the PETM newcomers to the Eocene canopy. Stand-in chain within
// one group: Teilhardina is an early omomyiform, Omomys a later omomyid (not a
// proven descendant). Notharctus is an adapiform, a different branch, and stays
// a wild species only (outline §5 H4).
static const struct DescentOption sDescent_Teilhardina[] =
{
    DESCENT_DEFAULT(SPECIES_OMOMYS),
    DESCENT_END,
};

// Rodents: a paramyid grade becomes the White River ischyromyid. Window: Acts 4-5.
static const struct DescentOption sDescent_Paramys[] =
{
    DESCENT_DEFAULT(SPECIES_ISCHYROMYS),
    DESCENT_END,
};

// Squirrels: stand-in. The oldest squirrel (a tree squirrel) stands in for the
// ground-squirrel line of the prairie dogs. Window: Acts 6-7.
static const struct DescentOption sDescent_Douglassciur[] =
{
    DESCENT_DEFAULT(SPECIES_CYNOMYS),
    DESCENT_END,
};

// Pronghorns: stand-in. Cosoryx is a merycodontine, an extinct side branch of the
// pronghorn family, not Antilocapra's ancestor. Window: Act 7.
static const struct DescentOption sDescent_Cosoryx[] =
{
    DESCENT_DEFAULT(SPECIES_ANTILOCAPRA),
    DESCENT_END,
};

static const struct LineageDescent sLineageDescents[] =
{
    { SPECIES_SIFRHIPPUS,   ERA_GREEN_RIVER,   sDescent_Sifrhippus },
    { SPECIES_EOHIPPUS,     ERA_WHITE_RIVER,   sDescent_Eohippus },
    { SPECIES_MESOHIPPUS,   ERA_ASHFALL,       sDescent_Mesohippus },
    { SPECIES_PROTOHIPPUS,  ERA_TRAP_CAVE,     sDescent_Protohippus },
    { SPECIES_POEBROTHERE,  ERA_ASHFALL,       sDescent_Poebrothere },
    { SPECIES_PROCAMELUS,   ERA_TRAP_CAVE,     sDescent_Procamelus },
    { SPECIES_HYRACHYUS,    ERA_WHITE_RIVER,   sDescent_Hyrachyus },
    { SPECIES_SUBHYRACODON, ERA_ASHFALL,       sDescent_Subhyracodon },
    { SPECIES_TEILHARDINA,  ERA_GREEN_RIVER,   sDescent_Teilhardina },
    { SPECIES_PARAMYS,      ERA_WHITE_RIVER,   sDescent_Paramys },
    { SPECIES_DOUGLASSCIUR, ERA_TRAP_CAVE,     sDescent_Douglassciur },
    { SPECIES_COSORYX,      ERA_TRAP_CAVE,     sDescent_Cosoryx },
    { SPECIES_CIMOLESTES,   ERA_CORRAL_BLUFFS, sDescent_Cimolestes },
    { SPECIES_PROTICTIS,    ERA_GREEN_RIVER,   sDescent_Protictis },
    { SPECIES_MIACIS,       ERA_WHITE_RIVER,   sDescent_Miacis },
    { SPECIES_HESPEROCYON,  ERA_ASHFALL,       sDescent_Hesperocyon },
    { SPECIES_LEPTOCYON,    ERA_TRAP_CAVE,     sDescent_Leptocyon },
    { SPECIES_ASTERIORNIS,  ERA_BIGHORN_PETM,  sDescent_Asteriornis },
    { SPECIES_GALLINULOID,  ERA_TRAP_CAVE,     sDescent_Gallinuloid },
    { SPECIES_EMARGINACHEL, ERA_CORRAL_BLUFFS, sDescent_Emarginachel },
    { SPECIES_PROTOCHELYD,  ERA_ASHFALL,       sDescent_Protochelyd },
};

// Extinction filters: species that do not survive into an era. Applied after that
// era's descents, so a lineage that descends into a survivor lives on.

// K-Pg mass extinction: all non-avian dinosaurs. Didelphodon's group of
// metatherians was also lost in North America. Small, burrowing, freshwater and
// detritus-feeding animals (multituberculates, champsosaurs, crocodylians, gars,
// turtles, ground birds) are the survivors in the Hell Creek-to-Tullock record.
// The tree-perching enantiornithine birds (Avisaurus) did not survive anywhere.
static const u16 sExtinctions_ImpactWinter[] =
{
    SPECIES_AVISAURUS,
    SPECIES_TYRANNOSAUR,
    SPECIES_TRICERATOPS,
    SPECIES_EDMONTOSAUR,
    SPECIES_ANKYLOSAURUS,
    SPECIES_PACHYCEPHALO,
    SPECIES_THESCELOSAUR,
    SPECIES_ACHERORAPTOR,
    SPECIES_ANZU,
    SPECIES_DIDELPHODON,
    SPECIES_NONE,
};

// The early Paleocene (Puercan) recovery fauna is gone by the late Paleocene.
static const u16 sExtinctions_BighornPetm[] =
{
    SPECIES_PURGATORIUS,
    SPECIES_LOXOLOPHUS,
    SPECIES_CARSIOPTYCH,
    SPECIES_TAENIOLABIS,
    SPECIES_EOCONODON,
    SPECIES_NONE,
};

// By the Eocene-Oligocene transition (~34 Ma): the lake fauna of Green River,
// the archaic Eocene mammals, North America's primates, Gastornis (gone by the
// mid-Eocene), champsosaurs, Borealosuchus and the last multituberculates; and
// the oxyaenids (Oxyaena by ~52 Ma, Patriofelis by the late Eocene).
// Omomys: omomyids lingered (perhaps to Ekgmowechashala, ~29 Ma), the genus did not.
// TODO: fact-check the last appearances against the Paleobiology Database.
static const u16 sExtinctions_WhiteRiver[] =
{
    SPECIES_OMOMYS,
    SPECIES_OXYAENA,
    SPECIES_PATRIOFELIS,
    SPECIES_GASTORNIS,
    SPECIES_PRESBYORNIS,
    SPECIES_CHAMPSOSAUR,
    SPECIES_BOREALOSUCH,
    SPECIES_MESODMA,
    SPECIES_HYOPSODUS,
    SPECIES_DIACODEXIS,
    SPECIES_CORYPHODON,
    SPECIES_ONYCHONYCTER,
    SPECIES_HELIOBATIS,
    SPECIES_KNIGHTIA,
    SPECIES_NOTHARCTUS,
    SPECIES_UINTATHERIUM,
    SPECIES_NONE,
};

// White River genera gone by the late Miocene. Hyaenodon's last North American
// species are late Oligocene; rabbits live on, Palaeolagus does not.
static const u16 sExtinctions_Ashfall[] =
{
    SPECIES_HYAENODON,
    SPECIES_PALAEOLAGUS,
    SPECIES_ARCHAEOTHERE,
    SPECIES_HOPLOPHONEUS,
    SPECIES_MERYCOIDODON,
    SPECIES_LEPTOMERYX,
    SPECIES_STYLEMYS,
    SPECIES_ISCHYROMYS,
    SPECIES_NONE,
};

// By the Ice Age: the North American rhinos (gone ~5 Ma; both rhino branches),
// Epicyon and the other bone-crushing dogs (~2 Ma), the Ashfall crane and
// scavenger, the browsing horse Hypohippus and the three-toed Cormohipparion.
static const u16 sExtinctions_TrapCave[] =
{
    SPECIES_APHELOPS,
    SPECIES_HYPOHIPPUS,
    SPECIES_CORMOHIPPARI,
    SPECIES_TELEOCERAS,
    SPECIES_EPICYON,
    SPECIES_BALEARICA,
    SPECIES_ANCHIGYPS,
    SPECIES_NONE,
};

// The end-Pleistocene megafauna extinction, ~13-11 ka. Horses and musk oxen
// vanished from the lower 48 but survived elsewhere, so their lineages live on.
static const u16 sExtinctions_Epilogue[] =
{
    SPECIES_AENOCYON,
    SPECIES_ARCTODUS,
    SPECIES_MIRACINONYX,
    SPECIES_PANTHERA,
    SPECIES_MAMMUTHUS,
    SPECIES_CAMELOPS,
    SPECIES_NONE,
};

static const u16 *const sEraExtinctions[ERA_COUNT] =
{
    [ERA_IMPACT_WINTER] = sExtinctions_ImpactWinter,
    [ERA_BIGHORN_PETM]  = sExtinctions_BighornPetm,
    [ERA_WHITE_RIVER]   = sExtinctions_WhiteRiver,
    [ERA_ASHFALL]       = sExtinctions_Ashfall,
    [ERA_TRAP_CAVE]     = sExtinctions_TrapCave,
    [ERA_EPILOGUE]      = sExtinctions_Epilogue,
};

// Era level floor: on entering an era, every party and PC mon below its floor is
// raised to it. A descendant arrives as a mature adult of its era, not as the
// level the player last left its ancestor at, so a lineage kept in the PC since
// Hell Creek is still usable in the Ice Age. Each floor is the era's lowest
// land encounter level (tools/strata/maps.py) minus 3: below the wild mons, so
// training still matters, but in reach of them. Fishing tables run a few levels
// lower on purpose and are not counted. Hell Creek and the present dig start
// the game and have no floor. The impact winter is the same animals a year
// later; its floor only catches the low-level Hell Creek catches.
static const u8 sEraLevelFloor[ERA_COUNT] =
{
    [ERA_PRESENT_DIG]   = 0,
    [ERA_HELL_CREEK]    = 0,
    [ERA_IMPACT_WINTER] = 7,  // wild 10-16
    [ERA_CORRAL_BLUFFS] = 12, // wild 15-20
    [ERA_BIGHORN_PETM]  = 19, // wild 22-28
    [ERA_GREEN_RIVER]   = 25, // wild 28-34
    [ERA_WHITE_RIVER]   = 31, // wild 34-39
    [ERA_ASHFALL]       = 37, // wild 40-45
    [ERA_TRAP_CAVE]     = 43, // wild 46-51
    [ERA_EPILOGUE]      = 45, // wild 48-53
};
