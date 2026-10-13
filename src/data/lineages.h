// Lineage descent table: what each species becomes when the game enters an era.
// See docs/strata_design.md §4-5 and §7.1-7.3, and tools/strata/roster.py for the species.
// Lineages without an entry for an era are in stasis.
// Extinctions are at the end of this file.

// Dog line: Canidae originated in North America.
static const struct DescentOption sDescent_Cimolestes[] =
{
    { SPECIES_PROTICTIS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Protictis[] =
{
    { SPECIES_MIACIS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Miacis[] =
{
    { SPECIES_HESPEROCYON, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Hesperocyon[] =
{
    { SPECIES_LEPTOCYON, PRESSURE_NONE },      // generalist, ancestor of all living canines
    { SPECIES_EPICYON,   PRESSURE_MEAT_DIET }, // bone-crushing borophagine
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Leptocyon[] =
{
    { SPECIES_CANIS,    PRESSURE_NONE },      // coyote, survives to today
    { SPECIES_AENOCYON, PRESSURE_MEAT_DIET }, // dire wolf, megafauna specialist
    { SPECIES_NONE },
};

// Bird line: ground birds survived the impact, then radiated.
static const struct DescentOption sDescent_Asteriornis[] =
{
    { SPECIES_GALLINULOID, PRESSURE_NONE },       // forest ground fowl
    { SPECIES_PRESBYORNIS, PRESSURE_WATER },      // lake wader
    { SPECIES_GASTORNIS,   PRESSURE_PLANT_DIET }, // flightless giant herbivore
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Gallinuloid[] =
{
    { SPECIES_MELEAGRIS, PRESSURE_NONE },
    { SPECIES_NONE },
};

// Snapping turtle line: stasis, with rare changes.
static const struct DescentOption sDescent_Emarginachel[] =
{
    { SPECIES_PROTOCHELYD, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Protochelyd[] =
{
    { SPECIES_CHELYDRA, PRESSURE_NONE },
    { SPECIES_NONE },
};

// Horse line: one of the best-documented lineages in the fossil record. Horses
// evolved in North America, browsing in forests, then grazing as grasslands spread.
static const struct DescentOption sDescent_Sifrhippus[] =
{
    { SPECIES_EOHIPPUS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Eohippus[] =
{
    { SPECIES_MESOHIPPUS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Mesohippus[] =
{
    { SPECIES_PROTOHIPPUS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Protohippus[] =
{
    { SPECIES_EQUUS, PRESSURE_NONE },
    { SPECIES_NONE },
};

// Camel line: camels also evolved in North America.
static const struct DescentOption sDescent_Poebrothere[] =
{
    { SPECIES_PROCAMELUS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_Procamelus[] =
{
    { SPECIES_CAMELOPS, PRESSURE_NONE },
    { SPECIES_NONE },
};

// Rhino line.
static const struct DescentOption sDescent_Subhyracodon[] =
{
    { SPECIES_TELEOCERAS, PRESSURE_NONE },
    { SPECIES_NONE },
};

// Primates: from the PETM newcomers to the Eocene canopy. Stand-in chain;
// Notharctus is a relative of Teilhardina's descendants, not a proven one.
static const struct DescentOption sDescent_Teilhardina[] =
{
    { SPECIES_NOTHARCTUS, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct LineageDescent sLineageDescents[] =
{
    { SPECIES_SIFRHIPPUS,   ERA_GREEN_RIVER,   sDescent_Sifrhippus },
    { SPECIES_EOHIPPUS,     ERA_WHITE_RIVER,   sDescent_Eohippus },
    { SPECIES_MESOHIPPUS,   ERA_ASHFALL,       sDescent_Mesohippus },
    { SPECIES_PROTOHIPPUS,  ERA_TRAP_CAVE,     sDescent_Protohippus },
    { SPECIES_POEBROTHERE,  ERA_ASHFALL,       sDescent_Poebrothere },
    { SPECIES_PROCAMELUS,   ERA_TRAP_CAVE,     sDescent_Procamelus },
    { SPECIES_SUBHYRACODON, ERA_ASHFALL,       sDescent_Subhyracodon },
    { SPECIES_TEILHARDINA,  ERA_GREEN_RIVER,   sDescent_Teilhardina },
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
static const u16 sExtinctions_ImpactWinter[] =
{
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
// mid-Eocene), champsosaurs, Borealosuchus and the last multituberculates.
// TODO: fact-check the last appearances against the Paleobiology Database.
static const u16 sExtinctions_WhiteRiver[] =
{
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

// White River genera gone by the late Miocene.
static const u16 sExtinctions_Ashfall[] =
{
    SPECIES_ARCHAEOTHERE,
    SPECIES_HOPLOPHONEUS,
    SPECIES_MERYCOIDODON,
    SPECIES_LEPTOMERYX,
    SPECIES_STYLEMYS,
    SPECIES_ISCHYROMYS,
    SPECIES_NONE,
};

// By the Ice Age: the North American rhinos (gone ~5 Ma), Epicyon and the other
// bone-crushing dogs (~2 Ma), and the Ashfall crane and scavenger.
static const u16 sExtinctions_TrapCave[] =
{
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
