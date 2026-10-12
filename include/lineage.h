#ifndef GUARD_LINEAGE_H
#define GUARD_LINEAGE_H

#include "constants/strata.h"

// One possible descendant of a lineage. The descendant whose pressure counter is
// highest wins; PRESSURE_NONE marks the default, which scores zero.
struct DescentOption
{
    u16 species;
    u8 pressure; // enum SelectionPressure
};

// What a species becomes when the game enters `era`.
// Species with no entry for an era are in stasis and stay as they are.
struct LineageDescent
{
    u16 ancestor;
    u8 era; // enum StrataEra
    const struct DescentOption *options; // terminated by SPECIES_NONE
};

enum Species Lineage_GetDescendant(enum Species ancestor, enum StrataEra era, const u8 *pressures);
bool32 Lineage_DescendBoxMon(struct BoxPokemon *boxMon, enum StrataEra era);
bool32 Lineage_DescendMon(struct Pokemon *mon, enum StrataEra era);
u32 Lineage_AdvanceToEra(enum StrataEra targetEra);
void Strata_AdvanceEra(void);

#endif // GUARD_LINEAGE_H
