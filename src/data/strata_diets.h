// What each Strata species eats, for knockout pressure (Selection_OnFoeFainted):
// only animal eaters gain PRESSURE_MEAT_DIET from a knockout. Unlisted species
// (and every stock species) are herbivores.
//
// Hand-written for now. TODO(content): add a `diet` field to the roster
// (tools/strata/roster*.py) and generate this table from it in gen_species.py.
// The classification follows each genus' dex entry and teeth:
//   CARNIVORE  vertebrate prey, fish or insects make up most of the diet
//   OMNIVORE   regularly eats both plants and animals
static const u8 sSpeciesDiets[NUM_SPECIES] =
{
    // Dog line
    [SPECIES_CIMOLESTES]   = DIET_CARNIVORE, // insectivore-carnivore teeth
    [SPECIES_PROTICTIS]    = DIET_CARNIVORE,
    [SPECIES_MIACIS]       = DIET_CARNIVORE,
    [SPECIES_HESPEROCYON]  = DIET_CARNIVORE,
    [SPECIES_EPICYON]      = DIET_CARNIVORE,
    [SPECIES_LEPTOCYON]    = DIET_OMNIVORE,  // fox-like generalist
    [SPECIES_AENOCYON]     = DIET_CARNIVORE,
    [SPECIES_CANIS]        = DIET_OMNIVORE,  // coyote

    // Bird line: ground fowl and waders eat seeds, shoots and invertebrates.
    [SPECIES_ASTERIORNIS]  = DIET_OMNIVORE,
    [SPECIES_PRESBYORNIS]  = DIET_OMNIVORE,  // filter-feeding wader
    [SPECIES_GALLINULOID]  = DIET_OMNIVORE,
    [SPECIES_MELEAGRIS]    = DIET_OMNIVORE,
    // SPECIES_GASTORNIS: herbivore (bone isotopes and beak shape)

    // Snapping turtles: opportunistic omnivores.
    [SPECIES_EMARGINACHEL] = DIET_OMNIVORE,
    [SPECIES_PROTOCHELYD]  = DIET_OMNIVORE,
    [SPECIES_CHELYDRA]     = DIET_OMNIVORE,

    // Hell Creek
    [SPECIES_TYRANNOSAUR]  = DIET_CARNIVORE,
    [SPECIES_ACHERORAPTOR] = DIET_CARNIVORE,
    [SPECIES_ANZU]         = DIET_OMNIVORE,  // diet debated: plants and small animals
    [SPECIES_DIDELPHODON]  = DIET_CARNIVORE, // shell- and bone-cracking
    [SPECIES_CHAMPSOSAUR]  = DIET_CARNIVORE, // fish
    [SPECIES_BOREALOSUCH]  = DIET_CARNIVORE,
    [SPECIES_LEPISOSTEUS]  = DIET_CARNIVORE, // fish

    // Paleocene recovery
    [SPECIES_PURGATORIUS]  = DIET_OMNIVORE,  // insects and fruit
    [SPECIES_LOXOLOPHUS]   = DIET_OMNIVORE,
    [SPECIES_EOCONODON]    = DIET_CARNIVORE,

    // Eocene
    [SPECIES_TEILHARDINA]  = DIET_OMNIVORE,  // insects and fruit
    [SPECIES_HYOPSODUS]    = DIET_OMNIVORE,
    [SPECIES_ONYCHONYCTER] = DIET_CARNIVORE, // insects
    [SPECIES_HELIOBATIS]   = DIET_CARNIVORE, // buried invertebrates
    [SPECIES_KNIGHTIA]     = DIET_OMNIVORE,  // plankton and small insects

    // Oligocene and Miocene
    [SPECIES_ARCHAEOTHERE] = DIET_OMNIVORE,  // "hell pig", cached carcasses
    [SPECIES_HOPLOPHONEUS] = DIET_CARNIVORE,
    [SPECIES_BALEARICA]    = DIET_OMNIVORE,  // cranes
    [SPECIES_ANCHIGYPS]    = DIET_CARNIVORE, // raptor and scavenger

    // Ice Age
    [SPECIES_ARCTODUS]     = DIET_CARNIVORE, // carnivore-scavenger (debated)
    [SPECIES_MIRACINONYX]  = DIET_CARNIVORE,
    [SPECIES_PANTHERA]     = DIET_CARNIVORE,
};
