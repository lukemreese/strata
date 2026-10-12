// Lineage descent table: what each species becomes when the game enters an era.
// See docs/strata_design.md §4-5 and §7.1, and tools/strata/roster.py for the species.
// Lineages without an entry for an era are in stasis.
//
// TODO: extinction. Epicyon, Aenocyon and Gastornis lines end in extinction, and
// will be handled by the extinction filters rather than this table.

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
