#include "global.h"
#include "pokemon.h"
#include "test/test.h"
#include "constants/characters.h"

// Sanity checks for the generated Strata species (tools/strata/gen_species.py).
// Strata species occupy the custom range after SPECIES_CUSTOM_START.

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)

TEST("Strata species have names, sprites and learnsets")
{
    enum Species species = SPECIES_NONE;
    u32 i;
    for (i = FIRST_STRATA_SPECIES; i < SPECIES_CUSTOM_END; i++)
    {
        PARAMETRIZE { species = i; }
    }
    EXPECT(IsSpeciesEnabled(species));
    EXPECT_NE(gSpeciesInfo[species].speciesName[0], EOS);
    EXPECT_NE(gSpeciesInfo[species].categoryName[0], EOS);
    EXPECT(gSpeciesInfo[species].frontPic != NULL);
    EXPECT(gSpeciesInfo[species].backPic != NULL);
    EXPECT(gSpeciesInfo[species].iconSprite != NULL);
    EXPECT(gSpeciesInfo[species].levelUpLearnset != NULL);
    EXPECT_NE(gSpeciesInfo[species].baseHP, 0);
}

TEST("Strata species have their own Pokedex numbers")
{
    enum Species species = SPECIES_NONE;
    u32 i;
    for (i = FIRST_STRATA_SPECIES; i < SPECIES_CUSTOM_END; i++)
    {
        PARAMETRIZE { species = i; }
    }
    EXPECT_GT(SpeciesToNationalPokedexNum(species), NATIONAL_DEX_PECHARUNT);
    EXPECT_LE(SpeciesToNationalPokedexNum(species), NATIONAL_DEX_COUNT);
    EXPECT_EQ(NationalPokedexNumToSpecies(SpeciesToNationalPokedexNum(species)), species);
}
