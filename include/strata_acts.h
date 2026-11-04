#ifndef GUARD_STRATA_ACTS_H
#define GUARD_STRATA_ACTS_H

#include "constants/strata.h"

u32 Strata_GetCurrentAct(void);
u32 Strata_GetRigState(void);
bool32 Strata_IsTodayGated(void);
const u8 *Strata_GetTodayGateText(void);
u32 Strata_GetRigTargetEra(void);
const u8 *Strata_GetLayerName(u32 era);
void Strata_RigQuery(void);
void Strata_RigLoadNext(void);
void Strata_SpecialGetCurrentAct(void);
void Strata_BufferMentorText(void);

#endif // GUARD_STRATA_ACTS_H
