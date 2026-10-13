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

static const struct LineageDescent sLineageDescents[] =
{
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

// By the Eocene-Oligocene transition (~34 Ma): Gastornis (gone in North America
// by the mid-Eocene), champsosaurs, Borealosuchus and Mesodma.
// TODO: fact-check the last appearances against the Paleobiology Database.
static const u16 sExtinctions_WhiteRiver[] =
{
    SPECIES_GASTORNIS,
    SPECIES_CHAMPSOSAUR,
    SPECIES_BOREALOSUCH,
    SPECIES_MESODMA,
    SPECIES_NONE,
};

// Epicyon and the other borophagine bone-crushers were gone by ~2 Ma.
static const u16 sExtinctions_TrapCave[] =
{
    SPECIES_EPICYON,
    SPECIES_NONE,
};

// The end-Pleistocene megafauna extinction, ~13-11 ka.
static const u16 sExtinctions_Epilogue[] =
{
    SPECIES_AENOCYON,
    SPECIES_NONE,
};

static const u16 *const sEraExtinctions[ERA_COUNT] =
{
    [ERA_IMPACT_WINTER] = sExtinctions_ImpactWinter,
    [ERA_WHITE_RIVER]   = sExtinctions_WhiteRiver,
    [ERA_TRAP_CAVE]     = sExtinctions_TrapCave,
    [ERA_EPILOGUE]      = sExtinctions_Epilogue,
};
