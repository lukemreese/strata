#ifndef GUARD_LINEAGE_H
#define GUARD_LINEAGE_H

#include "constants/strata.h"

// Pressure a branch needs by default before it can win: about three forage items,
// or most of an act spent in one habitat (docs/strata_outline.md §3.3).
#define DESCENT_MIN_SCORE 64

// One possible descendant of a lineage. A branch is eligible only once its
// pressure counter reaches minScore (0 means DESCENT_MIN_SCORE); among eligible
// branches the highest counter wins, ties going to the one listed first. With
// none eligible, the default wins: the option with PRESSURE_NONE.
struct DescentOption
{
    u16 species;
    u8 pressure; // enum SelectionPressure
    u8 minScore; // ignored for PRESSURE_NONE
};

// Table helpers for src/data/lineages.h.
#define DESCENT_DEFAULT(sp)                    { .species = (sp), .pressure = PRESSURE_NONE, .minScore = 0 }
#define DESCENT_BRANCH(sp, pressure_, score)   { .species = (sp), .pressure = (pressure_), .minScore = (score) }
#define DESCENT_END                            { .species = SPECIES_NONE }

// What a species becomes when the game enters `era`.
// Species with no entry for an era are in stasis and stay as they are.
struct LineageDescent
{
    u16 ancestor;
    u8 era; // enum StrataEra
    const struct DescentOption *options; // terminated by SPECIES_NONE
};

const struct DescentOption *Lineage_GetDescentOptions(enum Species ancestor, enum StrataEra era);
u32 Lineage_GetOptionMinScore(const struct DescentOption *option);
enum Species Lineage_GetDescendant(enum Species ancestor, enum StrataEra era, const u8 *pressures);
bool32 Lineage_DescendBoxMon(struct BoxPokemon *boxMon, enum StrataEra era);
bool32 Lineage_DescendMon(struct Pokemon *mon, enum StrataEra era);
bool32 Lineage_IsExtinctInEra(enum Species species, enum StrataEra era);
u32 Lineage_GetEraLevelFloor(enum StrataEra era);
bool32 Lineage_RaiseBoxMonToLevel(struct BoxPokemon *boxMon, u32 level);
bool32 Lineage_RaiseMonToLevel(struct Pokemon *mon, u32 level);
u32 Lineage_AdvanceToEra(enum StrataEra targetEra);
u32 Lineage_GetExtinctionCount(void);
enum Species Lineage_GetFirstExtinctSpecies(void);
void Strata_AdvanceEra(void);

#endif // GUARD_LINEAGE_H
