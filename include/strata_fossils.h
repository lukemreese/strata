#ifndef GUARD_STRATA_FOSSILS_H
#define GUARD_STRATA_FOSSILS_H

#include "constants/strata.h"

// Fossils: every lineage the player loses to an extinction filter (src/lineage.c) is recorded
// in a save flag (FLAG_STRATA_FOSSIL_BASE + slot, include/constants/strata_act_flags.h) and
// listed by the Fossil Case, the rig's loss list and the Hall of Lost Lineages.

// One lineage that can be lost. The era is the filter that drops it (sEraExtinctions).
struct StrataFossil
{
    u16 species;
    u16 gentle;         // Gentle Deep Time: the related survivor that takes its place
    const u8 *reason;   // why the filter killed it: two lines joined by \l (message box width)
};

// Number of losses the rig lists one by one after a jump; the rest are summed up.
#define FOSSIL_LOSS_LIST_MAX 24

s32 Fossil_GetSlot(enum Species species);
bool32 Fossil_Has(enum Species species);
void Fossil_Set(enum Species species);
u32 Fossil_Count(void);
u32 Fossil_CountForEra(enum StrataEra era);
enum StrataEra Fossil_GetEra(enum Species species);
const u8 *Fossil_GetReason(enum Species species);
enum Species Fossil_GetGentleReplacement(enum Species species);
bool32 Fossil_IsGentle(void);

// The losses of the last Lineage_AdvanceToEra, for the rig's list.
void Fossil_ResetLosses(void);
void Fossil_RecordLoss(struct BoxPokemon *boxMon, enum StrataEra era, bool32 inParty, enum Species replacement);
u32 Fossil_GetLossEntryCount(void);
u32 Fossil_GetLossOverflow(void);
bool32 Fossil_BufferLossText(u32 index, u8 *dest);
bool32 Fossil_BufferHallText(enum StrataEra era, u8 *dest);

void Strata_BufferLoss(void);
void Strata_PushFossilList(void);
void Strata_BufferFossil(void);
void Strata_BufferHallCase(void);

#endif // GUARD_STRATA_FOSSILS_H
