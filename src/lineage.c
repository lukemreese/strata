#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokedex.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "random.h"
#include "selection.h"
#include "string_util.h"
#include "text.h"
#include "constants/vars.h"

// Individuals don't evolve; lineages do. When the game enters a new era, every
// mon in the party and PC is replaced by its descendant species for that era.

#include "data/lineages.h"

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

// The options for `ancestor` entering `era` (terminated by SPECIES_NONE), or NULL
// if the lineage is in stasis then.
const struct DescentOption *Lineage_GetDescentOptions(enum Species ancestor, enum StrataEra era)
{
    const struct LineageDescent *descent = FindDescent(ancestor, era);
    return descent != NULL ? descent->options : NULL;
}

// Pressure a branch needs before it can win; 0 for the default.
u32 Lineage_GetOptionMinScore(const struct DescentOption *option)
{
    if (option->pressure >= PRESSURE_COUNT)
        return 0;
    return option->minScore != 0 ? option->minScore : DESCENT_MIN_SCORE;
}

// Returns the species `ancestor` becomes on entering `era`, or `ancestor` itself if
// the lineage is in stasis. A branch competes only once its pressure reaches its
// minScore; the highest eligible counter wins, ties going to the option listed
// first. If no branch is eligible, the default (PRESSURE_NONE) wins.
enum Species Lineage_GetDescendant(enum Species ancestor, enum StrataEra era, const u8 *pressures)
{
    const struct DescentOption *option = Lineage_GetDescentOptions(ancestor, era);
    enum Species best = SPECIES_NONE, fallback = ancestor;
    s32 bestScore = -1;

    if (option == NULL)
        return ancestor;

    for (; option->species != SPECIES_NONE; option++)
    {
        s32 score;
        if (option->pressure >= PRESSURE_COUNT)
        {
            if (fallback == ancestor)
                fallback = option->species;
            continue;
        }
        score = pressures[option->pressure];
        if (score >= (s32)Lineage_GetOptionMinScore(option) && score > bestScore)
        {
            best = option->species;
            bestScore = score;
        }
    }
    return best != SPECIES_NONE ? best : fallback;
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
    Selection_GetBoxMonPressures(boxMon, pressures);
    descendant = Lineage_GetDescendant(ancestor, era, pressures);
    if (descendant == ancestor)
        return FALSE;

    level = GetLevelFromBoxMonExp(boxMon);
    SetBoxMonData(boxMon, MON_DATA_SPECIES, &descendant);
    KeepBoxMonLevel(boxMon, level);
    RenameBoxMonIfDefault(boxMon, ancestor, descendant);
    Selection_ResetBoxMonPressures(boxMon);
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

bool32 Lineage_IsExtinctInEra(enum Species species, enum StrataEra era)
{
    const u16 *extinct = sEraExtinctions[era];

    if (extinct == NULL)
        return FALSE;
    for (; *extinct != SPECIES_NONE; extinct++)
    {
        if (*extinct == species)
            return TRUE;
    }
    return FALSE;
}

// TRUE if `species` died out in `era` or any era before it.
static bool32 IsExtinctByEra(enum Species species, enum StrataEra era)
{
    u32 i;
    for (i = 0; i <= era; i++)
    {
        if (Lineage_IsExtinctInEra(species, i))
            return TRUE;
    }
    return FALSE;
}

u32 Lineage_GetEraLevelFloor(enum StrataEra era)
{
    if (era >= ERA_COUNT)
        return 0;
    return sEraLevelFloor[era];
}

// Raises a stored mon to `level` as if it had levelled up there: EXP moves to the
// start of that level, and it learns the level-up moves it passed on the way, in
// order, forgetting its oldest move when all four slots are full. Box mons keep
// no stats; their HP lost is unchanged, so a party mon gains as much HP as its
// max HP rises, as on a normal level-up. Returns TRUE if the mon was raised.
bool32 Lineage_RaiseBoxMonToLevel(struct BoxPokemon *boxMon, u32 level)
{
    const struct LevelUpMove *learnset;
    enum Species species;
    u32 i, oldLevel, exp;

    if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES) || GetBoxMonData(boxMon, MON_DATA_IS_EGG))
        return FALSE;
    oldLevel = GetLevelFromBoxMonExp(boxMon);
    if (oldLevel >= level)
        return FALSE;

    species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    exp = gExperienceTables[gSpeciesInfo[species].growthRate][level];
    SetBoxMonData(boxMon, MON_DATA_EXP, &exp);

    learnset = GetSpeciesLevelUpLearnset(species);
    for (i = 0; learnset[i].move != LEVEL_UP_MOVE_END; i++)
    {
        if (learnset[i].level <= oldLevel || learnset[i].level > level)
            continue;
        if (GiveMoveToBoxMon(boxMon, learnset[i].move) == MON_HAS_MAX_MOVES)
            DeleteFirstMoveAndGiveMoveToBoxMon(boxMon, learnset[i].move);
    }
    return TRUE;
}

bool32 Lineage_RaiseMonToLevel(struct Pokemon *mon, u32 level)
{
    if (!Lineage_RaiseBoxMonToLevel(&mon->box, level))
        return FALSE;
    CalculateMonStats(mon);
    return TRUE;
}

static void ApplyLevelFloor(enum StrataEra era)
{
    u32 i, boxId, boxPos, floor = Lineage_GetEraLevelFloor(era);

    if (floor == 0)
        return;
    for (i = 0; i < PARTY_SIZE; i++)
        Lineage_RaiseMonToLevel(&gParties[B_TRAINER_PLAYER][i], floor);
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
            Lineage_RaiseBoxMonToLevel(GetBoxedMonPtr(boxId, boxPos), floor);
    }
}

static EWRAM_DATA u16 sExtinctionCount = 0;
static EWRAM_DATA u16 sFirstExtinctSpecies = SPECIES_NONE;

// Returns TRUE if the stored mon's lineage doesn't survive into `era`. The caller
// removes it.
static bool32 IsBoxMonExtinct(struct BoxPokemon *boxMon, enum StrataEra era)
{
    enum Species species;

    if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES) || GetBoxMonData(boxMon, MON_DATA_IS_EGG))
        return FALSE;
    species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    if (!Lineage_IsExtinctInEra(species, era))
        return FALSE;
    if (sExtinctionCount++ == 0)
        sFirstExtinctSpecies = species;
    return TRUE;
}

// An extinction can't leave the player with no party: bring a survivor from the
// PC, or failing that, a small survivor joins at the era's level floor (but no
// lower than the level it always had). Mesodma until the multituberculates die
// out, then the gar, which lives to the present. It joins with its moves for that
// level and full HP.
#define SURVIVOR_GIFT_LEVEL 10

static void EnsurePartyNotEmpty(enum StrataEra era)
{
    u32 boxId, boxPos;
    enum Species survivor;

    if (CalculatePlayerPartyCount() != 0)
        return;
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
        {
            struct BoxPokemon *boxMon = GetBoxedMonPtr(boxId, boxPos);
            if (GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES))
            {
                BoxMonToMon(boxMon, &gParties[B_TRAINER_PLAYER][0]);
                ZeroBoxMonData(boxMon);
                CalculatePlayerPartyCount();
                return;
            }
        }
    }
    survivor = IsExtinctByEra(SPECIES_MESODMA, era) ? SPECIES_LEPISOSTEUS : SPECIES_MESODMA;
    // CreateMon alone leaves the mon with no moves or stats.
    CreateRandomMon(&gParties[B_TRAINER_PLAYER][0], survivor, max(SURVIVOR_GIFT_LEVEL, Lineage_GetEraLevelFloor(era)));
    CalculatePlayerPartyCount();
}

static void ApplyExtinctions(enum StrataEra era)
{
    u32 i, boxId, boxPos;

    for (i = 0; i < PARTY_SIZE; i++)
    {
        if (IsBoxMonExtinct(&gParties[B_TRAINER_PLAYER][i].box, era))
            ZeroMonData(&gParties[B_TRAINER_PLAYER][i]);
    }
    CompactPartySlots();
    CalculatePlayerPartyCount();

    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
        {
            struct BoxPokemon *boxMon = GetBoxedMonPtr(boxId, boxPos);
            if (IsBoxMonExtinct(boxMon, era))
                ZeroBoxMonData(boxMon);
        }
    }
    EnsurePartyNotEmpty(era);
}

// Advances the world one era at a time up to `targetEra`, so a lineage passes
// through every intermediate descent and extinction filter, then is raised to
// that era's level floor (learning its moves level by level, era by era). Box
// mons get their stats recalculated when withdrawn. Returns the number of
// descents that happened; see Lineage_GetExtinctionCount for the losses.
u32 Lineage_AdvanceToEra(enum StrataEra targetEra)
{
    u32 era, i, boxId, boxPos, count = 0;

    sExtinctionCount = 0;
    sFirstExtinctSpecies = SPECIES_NONE;
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
        ApplyExtinctions(era);
        ApplyLevelFloor(era);
        VarSet(VAR_STRATA_ERA, era);
    }
    return count;
}

// Mons lost to extinction in the last Lineage_AdvanceToEra.
u32 Lineage_GetExtinctionCount(void)
{
    return sExtinctionCount;
}

enum Species Lineage_GetFirstExtinctSpecies(void)
{
    return sFirstExtinctSpecies;
}

// special Strata_AdvanceEra
// Input:  VAR_0x8004 = era to advance to
// Output: VAR_RESULT = number of descents
//         VAR_0x8005 = number of mons lost to extinction
//         STR_VAR_1  = species of the first mon lost
//         STR_VAR_2  = how many others were lost
void Strata_AdvanceEra(void)
{
    gSpecialVar_Result = Lineage_AdvanceToEra(gSpecialVar_0x8004);
    gSpecialVar_0x8005 = sExtinctionCount;
    if (sExtinctionCount != 0)
    {
        StringCopy(gStringVar1, GetSpeciesName(sFirstExtinctSpecies));
        ConvertIntToDecimalStringN(gStringVar2, sExtinctionCount - 1, STR_CONV_MODE_LEFT_ALIGN, 3);
    }
}
