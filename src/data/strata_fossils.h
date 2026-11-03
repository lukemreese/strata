// Fossil slots, Gentle Deep Time replacements and loss reasons (src/strata_fossils.c).
//
// APPEND ONLY: slot i is save flag FLAG_STRATA_FOSSIL_BASE + i, so reordering or removing a
// row reassigns old saves' fossils. Every species in an extinction list of src/data/lineages.h
// needs a row (test/strata_fossils.c checks it, and that slots fit STRATA_FOSSIL_FLAG_COUNT).
//
// reason: one or two short lines joined by \l, shown under the animal's name in the rig's loss
//   list and under the fossil in the Fossil Case. Why that era's filter took it, from the record.
// gentle: the related survivor that replaces a lost animal in Gentle Deep Time (S4). It must
//   exist and be alive in the filter's era (tested). Where no relative survives in the roster,
//   it is the closest ecological stand-in, and the comment says so.

static const struct StrataFossil sStrataFossils[] =
{
    // ---- K-Pg impact winter (ERA_IMPACT_WINTER) ----
    // Birds are the dinosaurs that survived: every dinosaur lineage is replaced by the crown bird.
    { SPECIES_AVISAURUS,    SPECIES_ASTERIORNIS, COMPOUND_STRING("A tree-percher. The forests burned\land fell, and its birds went too.") },
    { SPECIES_TYRANNOSAUR,  SPECIES_ASTERIORNIS, COMPOUND_STRING("Top of a food chain that broke\lwhen the plants stopped growing.") },
    { SPECIES_TRICERATOPS,  SPECIES_ASTERIORNIS, COMPOUND_STRING("Too big to burrow or hide, it\lstarved as the plants died back.") },
    { SPECIES_EDMONTOSAUR,  SPECIES_ASTERIORNIS, COMPOUND_STRING("A huge grazer with no refuge.\lThe dark took its plant food.") },
    { SPECIES_ANKYLOSAURUS, SPECIES_ASTERIORNIS, COMPOUND_STRING("Armor was no help: a big body\lneeds food the dark took away.") },
    { SPECIES_PACHYCEPHALO, SPECIES_ASTERIORNIS, COMPOUND_STRING("No burrow, no water to hide in,\land nothing to eat in the dark.") },
    { SPECIES_THESCELOSAUR, SPECIES_ASTERIORNIS, COMPOUND_STRING("Small for a dinosaur, but still\ltoo big to wait out the cold.") },
    { SPECIES_ACHERORAPTOR, SPECIES_ASTERIORNIS, COMPOUND_STRING("A hunter whose prey died first,\lwith no burrow from the cold.") },
    { SPECIES_ANZU,         SPECIES_ASTERIORNIS, COMPOUND_STRING("Close to the birds, but not one.\lToo big to wait out the dark.") },
    // Metatherians and eutherians are both therian mammals.
    { SPECIES_DIDELPHODON,  SPECIES_CIMOLESTES,  COMPOUND_STRING("Its whole metatherian group was\lwiped out in North America.") },

    // ---- Paleocene turnover (ERA_BIGHORN_PETM) ----
    { SPECIES_PURGATORIUS,  SPECIES_TEILHARDINA, COMPOUND_STRING("A primate cousin. Later kin and\ltrue primates took its place.") },
    // Condylarths: a grab-bag of archaic hoofed mammals; Hyopsodus is one of the last.
    { SPECIES_LOXOLOPHUS,   SPECIES_HYOPSODUS,   COMPOUND_STRING("An archaic hoofed mammal. Newer\lplant-eaters took its niche.") },
    { SPECIES_CARSIOPTYCH,  SPECIES_HYOPSODUS,   COMPOUND_STRING("A blunt-toothed browser, gone as\lthe Paleocene forests changed.") },
    { SPECIES_TAENIOLABIS,  SPECIES_MESODMA,     COMPOUND_STRING("The giant of its group. Big\lmultituberculates faded out.") },
    { SPECIES_EOCONODON,    SPECIES_HYOPSODUS,   COMPOUND_STRING("An early big predator. Its group\lwas gone within the Paleocene.") },

    // ---- Eocene-Oligocene cooling (ERA_WHITE_RIVER) ----
    // Primates and rodents are both Euarchontoglires; the tree squirrel is the forest stand-in.
    { SPECIES_OMOMYS,       SPECIES_DOUGLASSCIUR, COMPOUND_STRING("A forest primate. As it cooled,\lthe warm forests thinned away.") },
    // Oxyaenids and hyaenodonts are both "creodonts".
    { SPECIES_OXYAENA,      SPECIES_HYAENODON,   COMPOUND_STRING("Its oxyaenid group faded as\lnewer meat-eaters spread.") },
    { SPECIES_PATRIOFELIS,  SPECIES_HYAENODON,   COMPOUND_STRING("The last big oxyaenids were\lgone before the Oligocene.") },
    // Gastornis and Presbyornis are galloanserans, like the game bird.
    { SPECIES_GASTORNIS,    SPECIES_GALLINULOID, COMPOUND_STRING("A giant ground bird of warm\lforests, gone by the mid-Eocene.") },
    { SPECIES_PRESBYORNIS,  SPECIES_GALLINULOID, COMPOUND_STRING("Its lake shores dried up. Its\lduck relatives carried on.") },
    // No choristodere or crocodylian survives in the roster: the turtle is the reptile stand-in.
    { SPECIES_CHAMPSOSAUR,  SPECIES_PROTOCHELYD, COMPOUND_STRING("Champsosaurs needed warm rivers.\lThe last ones died out.") },
    { SPECIES_BOREALOSUCH,  SPECIES_PROTOCHELYD, COMPOUND_STRING("A croc of warm rivers. The\lcooling pushed crocs south.") },
    // No multituberculate survives: rodents, their ecological successors.
    { SPECIES_MESODMA,      SPECIES_ISCHYROMYS,  COMPOUND_STRING("The last multituberculates lost\lout to rodents and the cold.") },
    { SPECIES_HYOPSODUS,    SPECIES_MESOHIPPUS,  COMPOUND_STRING("A small archaic hoofed mammal.\lIts kind did not see the cold.") },
    { SPECIES_DIACODEXIS,   SPECIES_LEPTOMERYX,  COMPOUND_STRING("Its genus ended, but even-toed\lhoofed mammals thrived.") },
    // Pantodonts and uintatheres left no relatives: the big browsing rhino is the stand-in.
    { SPECIES_CORYPHODON,   SPECIES_SUBHYRACODON, COMPOUND_STRING("A big swamp browser. Pantodonts\lleft no descendants.") },
    // No bat survives in the roster: the small tree squirrel is the stand-in.
    { SPECIES_ONYCHONYCTER, SPECIES_DOUGLASSCIUR, COMPOUND_STRING("One of the first bats. Its family\ldied; other bats live on.") },
    // Fish of the same waters.
    { SPECIES_HELIOBATIS,   SPECIES_LEPISOSTEUS, COMPOUND_STRING("A freshwater ray of a warm lake\lthat shrank and cooled.") },
    { SPECIES_KNIGHTIA,     SPECIES_LEPISOSTEUS, COMPOUND_STRING("A herring of Fossil Lake. The\llake itself disappeared.") },
    { SPECIES_NOTHARCTUS,   SPECIES_DOUGLASSCIUR, COMPOUND_STRING("A lemur-like primate. The warm\lforests it needed shrank.") },
    { SPECIES_UINTATHERIUM, SPECIES_SUBHYRACODON, COMPOUND_STRING("A horned browser. Its whole\lgroup was gone by 40 Ma.") },

    // ---- grassland turnover (ERA_ASHFALL) ----
    // No other hyaenodont survives: the bone-crushing dog took its role.
    { SPECIES_HYAENODON,    SPECIES_EPICYON,     COMPOUND_STRING("Its last North American kind\ldied in the late Oligocene.") },
    // Rabbits and rodents are both Glires.
    { SPECIES_PALAEOLAGUS,  SPECIES_DOUGLASSCIUR, COMPOUND_STRING("The genus ended. Rabbits and\lhares carried the line on.") },
    { SPECIES_ARCHAEOTHERE, SPECIES_PROCAMELUS,  COMPOUND_STRING("A hell pig. Its entelodont kin\lwere gone by the early Miocene.") },
    // Nimravids are carnivoramorphs; the big dog is the nearest predator in the roster.
    { SPECIES_HOPLOPHONEUS, SPECIES_EPICYON,     COMPOUND_STRING("A false sabertooth. Its group,\lthe nimravids, faded out.") },
    // Oreodonts are often placed near the camels.
    { SPECIES_MERYCOIDODON, SPECIES_PROCAMELUS,  COMPOUND_STRING("The genus ended; later oreodonts\llasted a while longer.") },
    { SPECIES_LEPTOMERYX,   SPECIES_COSORYX,     COMPOUND_STRING("A tiny forest ruminant, lost as\lthe forests gave way to grass.") },
    // No tortoise in the roster: the snapping turtle.
    { SPECIES_STYLEMYS,     SPECIES_CHELYDRA,    COMPOUND_STRING("Its tortoise genus ended. Other\ltortoises live on.") },
    { SPECIES_ISCHYROMYS,   SPECIES_DOUGLASSCIUR, COMPOUND_STRING("An archaic rodent, replaced by\lsquirrels and other modern ones.") },

    // ---- Pliocene losses (ERA_TRAP_CAVE) ----
    // Rhinos and horses are both perissodactyls.
    { SPECIES_APHELOPS,     SPECIES_EQUUS,       COMPOUND_STRING("North America's rhinos died out\labout 5 million years ago.") },
    { SPECIES_HYPOHIPPUS,   SPECIES_EQUUS,       COMPOUND_STRING("A forest-browsing horse. The\lforests it browsed were gone.") },
    { SPECIES_CORMOHIPPARI, SPECIES_EQUUS,       COMPOUND_STRING("A three-toed grazer. One-toed\lhorses outlasted it.") },
    { SPECIES_TELEOCERAS,   SPECIES_EQUUS,       COMPOUND_STRING("A hippo-like rhino. Rhinos died\lout here about 5 million years ago.") },
    { SPECIES_EPICYON,      SPECIES_CANIS,       COMPOUND_STRING("The bone-crushing dogs were gone\lby about 2 million years ago.") },
    // No crane or vulture survives in the roster: the turkey, a ground bird of the same plains.
    { SPECIES_BALEARICA,    SPECIES_MELEAGRIS,   COMPOUND_STRING("Crowned cranes now live only in\lAfrica. North America lost them.") },
    { SPECIES_ANCHIGYPS,    SPECIES_MELEAGRIS,   COMPOUND_STRING("A vulture of the Miocene plains.\lIts line ended here.") },

    // ---- end of the Ice Age (ERA_EPILOGUE) ----
    { SPECIES_AENOCYON,     SPECIES_CANIS,       COMPOUND_STRING("It vanished with the big prey it\lhunted, about 13,000 years ago.") },
    // Bears and weasels are both arctoid carnivorans.
    { SPECIES_ARCTODUS,     SPECIES_MUSTELA,     COMPOUND_STRING("The short-faced bear was gone\lby about 11,000 years ago.") },
    // No wild cat survives in the roster: the fox, a small carnivoran of the same plains.
    { SPECIES_MIRACINONYX,  SPECIES_VULPES,      COMPOUND_STRING("The American cheetah vanished in\lthe end-Pleistocene losses.") },
    { SPECIES_PANTHERA,     SPECIES_CANIS,       COMPOUND_STRING("It died out at the end of the\lIce Age, with most big game.") },
    // No proboscidean survives: bison, the big grazer of the same steppe.
    { SPECIES_MAMMUTHUS,    SPECIES_BISON,       COMPOUND_STRING("Climate, people, or both: the\llast mammoths here were gone.") },
    // Camels and pronghorns are both artiodactyls of the open plains.
    { SPECIES_CAMELOPS,     SPECIES_ANTILOCAPRA, COMPOUND_STRING("Camels began here, but North\lAmerica's last ones died out.") },
};

// Per filter: the short age in the Fossil Case list, the sentence on a fossil, and the
// Hall of Lost Lineages case title.
struct StrataFossilEra
{
    const u8 *age;
    const u8 *lost;
};

static const struct StrataFossilEra sStrataFossilEras[ERA_COUNT] =
{
    [ERA_IMPACT_WINTER] = { COMPOUND_STRING("66 Ma"), COMPOUND_STRING("Lost in the K-Pg impact winter,\l66 million years ago.") },
    [ERA_BIGHORN_PETM]  = { COMPOUND_STRING("56 Ma"), COMPOUND_STRING("Gone by the end of the Paleocene,\labout 56 million years ago.") },
    [ERA_WHITE_RIVER]   = { COMPOUND_STRING("34 Ma"), COMPOUND_STRING("Gone in the Eocene cooling,\labout 34 million years ago.") },
    [ERA_ASHFALL]       = { COMPOUND_STRING("12 Ma"), COMPOUND_STRING("Gone by the grassland turnover,\labout 12 million years ago.") },
    [ERA_TRAP_CAVE]     = { COMPOUND_STRING("2 Ma"),  COMPOUND_STRING("Gone before the Ice Age, 5 to 2\lmillion years ago.") },
    [ERA_EPILOGUE]      = { COMPOUND_STRING("12 ka"), COMPOUND_STRING("Gone at the end of the Ice Age,\labout 12,000 years ago.") },
};
