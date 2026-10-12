#ifndef GUARD_SELECTION_H
#define GUARD_SELECTION_H

#include "constants/strata.h"

#define SELECTION_STEPS_PER_TICK  32 // Steps between habitat/climate pressure ticks
#define SELECTION_PREY_PRESSURE    2 // PRESSURE_MEAT_DIET gained per foe knocked out

void Selection_GetBoxMonPressures(struct BoxPokemon *boxMon, u8 *pressures);
void Selection_ResetBoxMonPressures(struct BoxPokemon *boxMon);
void Selection_AddPressure(struct Pokemon *mon, enum SelectionPressure pressure, u32 amount);
enum SelectionPressure Selection_GetHabitat(u32 metatileBehavior);
void Selection_ApplyTick(enum SelectionPressure habitat, u32 heat);
void Selection_UpdateStepCounter(u16 metatileBehavior);
void Selection_OnFoeFainted(u32 battler);
void Strata_AddPressure(void);

#endif // GUARD_SELECTION_H
