#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokedex.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "string_util.h"
#include "constants/vars.h"

// Individuals don't evolve; lineages do. When the game enters a new era, every
// mon in the party and PC is replaced by its descendant species for that era.

#include "data/lineages.h"

// Contest stats are unused in Strata, so they hold the selection pressure counters.
static const u8 sPressureDataIds[PRESSURE_COUNT] =
{
    [PRESSURE_FOREST]     = MON_DATA_COOL,
    [PRESSURE_OPEN]       = MON_DATA_BEAUTY,
    [PRESSURE_WATER]      = MON_DATA_CUTE,
    [PRESSURE_PLANT_DIET] = MON_DATA_SMART,
    [PRESSURE_MEAT_DIET]  = MON_DATA_TOUGH,
    [PRESSURE_HEAT]       = MON_DATA_SHEEN,
};

static const struct LineageDescent *FindDescent(enum Species ancestor, enum StrataEra era)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sLineageDescents); i++)
    {
        if (sLineageDescents[i].ancestor == ancestor && sLineageDescents[i].era == era)
            return &sLineageDescents[i];
    }
    return NULL;
}

// Returns the species `ancestor` becomes on entering `era`, or `ancestor` itself if
// the lineage is in stasis. Ties go to the option listed first.
enum Species Lineage_GetDescendant(enum Species ancestor, enum StrataEra era, const u8 *pressures)
{
    const struct LineageDescent *descent = FindDescent(ancestor, era);
    const struct DescentOption *option;
    enum Species best;
    s32 bestScore = -1;

    if (descent == NULL)
        return ancestor;

    best = ancestor;
    for (option = descent->options; option->species != SPECIES_NONE; option++)
    {
        s32 score = (option->pressure == PRESSURE_NONE) ? 0 : pressures[option->pressure];
        if (score > bestScore)
        {
            best = option->species;
            bestScore = score;
        }
    }
    return best;
}

void Lineage_GetBoxMonPressures(struct BoxPokemon *boxMon, u8 *pressures)
{
    u32 i;
    for (i = 0; i < PRESSURE_COUNT; i++)
        pressures[i] = GetBoxMonData(boxMon, sPressureDataIds[i]);
}

static void ResetBoxMonPressures(struct BoxPokemon *boxMon)
{
    u32 i;
    u8 zero = 0;
    for (i = 0; i < PRESSURE_COUNT; i++)
        SetBoxMonData(boxMon, sPressureDataIds[i], &zero);
}

// Box counterpart of EvolutionRenameMon: a mon still called by its species name
// takes on the new species name.
static void RenameBoxMonIfDefault(struct BoxPokemon *boxMon, enum Species oldSpecies, enum Species newSpecies)
{
    u8 nickname[POKEMON_NAME_BUFFER_SIZE];
    GetBoxMonData(boxMon, MON_DATA_NICKNAME, nickname);
    if (GetBoxMonData(boxMon, MON_DATA_LANGUAGE) == GAME_LANGUAGE
     && !StringCompare(GetSpeciesName(oldSpecies), nickname))
        SetBoxMonData(boxMon, MON_DATA_NICKNAME, GetSpeciesName(newSpecies));
}

// Level is derived from EXP via the species' growth rate, so a descendant with a
// different growth rate needs its EXP moved onto the new curve to keep its level.
// Progress towards the next level is not kept.
static void KeepBoxMonLevel(struct BoxPokemon *boxMon, u32 level)
{
    enum Species species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    u32 exp;

    if (GetLevelFromBoxMonExp(boxMon) == level)
        return;
    exp = gExperienceTables[gSpeciesInfo[species].growthRate][level];
    SetBoxMonData(boxMon, MON_DATA_EXP, &exp);
}

// Replaces a stored mon with its descendant for `era`. Personality, OT, IVs, EVs,
// moves and level carry over. Pressures reset, since the new era is a new
// environment. Returns TRUE if the species changed.
bool32 Lineage_DescendBoxMon(struct BoxPokemon *boxMon, enum StrataEra era)
{
    u8 pressures[PRESSURE_COUNT];
    enum Species ancestor, descendant;
    u32 level;

    if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES) || GetBoxMonData(boxMon, MON_DATA_IS_EGG))
        return FALSE;

    ancestor = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    Lineage_GetBoxMonPressures(boxMon, pressures);
    descendant = Lineage_GetDescendant(ancestor, era, pressures);
    if (descendant == ancestor)
        return FALSE;

    level = GetLevelFromBoxMonExp(boxMon);
    SetBoxMonData(boxMon, MON_DATA_SPECIES, &descendant);
    KeepBoxMonLevel(boxMon, level);
    RenameBoxMonIfDefault(boxMon, ancestor, descendant);
    ResetBoxMonPressures(boxMon);
    GetSetPokedexFlag(SpeciesToNationalPokedexNum(descendant), FLAG_SET_SEEN);
    GetSetPokedexFlag(SpeciesToNationalPokedexNum(descendant), FLAG_SET_CAUGHT);
    return TRUE;
}

bool32 Lineage_DescendMon(struct Pokemon *mon, enum StrataEra era)
{
    if (!Lineage_DescendBoxMon(&mon->box, era))
        return FALSE;
    CalculateMonStats(mon);
    return TRUE;
}

// Advances the world one era at a time up to `targetEra`, so a lineage passes
// through every intermediate descent. Box mons get their stats recalculated
// when withdrawn. Returns the number of descents that happened.
u32 Lineage_AdvanceToEra(enum StrataEra targetEra)
{
    u32 era, i, boxId, boxPos, count = 0;

    if (targetEra >= ERA_COUNT)
        targetEra = ERA_COUNT - 1;

    for (era = VarGet(VAR_STRATA_ERA) + 1; era <= targetEra; era++)
    {
        for (i = 0; i < PARTY_SIZE; i++)
            count += Lineage_DescendMon(&gParties[B_TRAINER_PLAYER][i], era);

        for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
        {
            for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
                count += Lineage_DescendBoxMon(GetBoxedMonPtr(boxId, boxPos), era);
        }
        VarSet(VAR_STRATA_ERA, era);
    }
    return count;
}

// special Strata_AdvanceEra
// Input:  VAR_0x8004 = era to advance to
// Output: VAR_RESULT = number of descents
void Strata_AdvanceEra(void)
{
    gSpecialVar_Result = Lineage_AdvanceToEra(gSpecialVar_0x8004);
}
