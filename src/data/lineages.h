// Lineage descent table: what each species becomes when the game enters an era.
// See docs/strata_design.md §4-5 and §7.1.
//
// PLACEHOLDER DATA: the real fossil species don't exist yet, so stock Pokémon stand
// in for them to exercise the system. Replace these as Strata species are added.
//   Poochyena line -> dog line (branching: generalist vs. specialist)
//   Torchic line   -> bird line (branching by habitat)
//   Squirtle       -> snapping turtle line (stasis between descents)

static const struct DescentOption sDescent_DogLine_CorralBluffs[] =
{
    { SPECIES_MIGHTYENA, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_DogLine_WhiteRiver[] =
{
    { SPECIES_ZIGZAGOON, PRESSURE_NONE },      // generalist, like Leptocyon
    { SPECIES_HOUNDOUR,  PRESSURE_MEAT_DIET }, // bone-crushing specialist, like Epicyon
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_BirdLine_GreenRiver[] =
{
    { SPECIES_COMBUSKEN, PRESSURE_NONE },  // ground fowl, like Gallinuloides
    { SPECIES_DUCKLETT,  PRESSURE_WATER }, // lake wader, like Presbyornis
    { SPECIES_DODUO,     PRESSURE_OPEN },  // flightless giant, like Gastornis
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_TurtleLine_BighornPetm[] =
{
    { SPECIES_WARTORTLE, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct DescentOption sDescent_TurtleLine_Ashfall[] =
{
    { SPECIES_BLASTOISE, PRESSURE_NONE },
    { SPECIES_NONE },
};

static const struct LineageDescent sLineageDescents[] =
{
    { SPECIES_POOCHYENA, ERA_CORRAL_BLUFFS, sDescent_DogLine_CorralBluffs },
    { SPECIES_MIGHTYENA, ERA_WHITE_RIVER,   sDescent_DogLine_WhiteRiver },
    { SPECIES_TORCHIC,   ERA_GREEN_RIVER,   sDescent_BirdLine_GreenRiver },
    { SPECIES_SQUIRTLE,  ERA_BIGHORN_PETM,  sDescent_TurtleLine_BighornPetm },
    { SPECIES_WARTORTLE, ERA_ASHFALL,       sDescent_TurtleLine_Ashfall },
};
