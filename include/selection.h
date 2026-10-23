#ifndef GUARD_SELECTION_H
#define GUARD_SELECTION_H

#include "constants/strata.h"

#define SELECTION_STEPS_PER_TICK  32 // Steps between habitat/climate pressure ticks
#define SELECTION_PREY_PRESSURE    1 // PRESSURE_MEAT_DIET gained per foe knocked out (animal eaters only)
#define SELECTION_PREY_CAP        24 // Knockouts can't raise PRESSURE_MEAT_DIET above this
#define SELECTION_FISH_PRESSURE    2 // PRESSURE_WATER gained by the party per fish hooked

void Selection_GetBoxMonPressures(struct BoxPokemon *boxMon, u8 *pressures);
void Selection_ResetBoxMonPressures(struct BoxPokemon *boxMon);
void Selection_AddPressure(struct Pokemon *mon, enum SelectionPressure pressure, u32 amount);
void Selection_AddPressureUpTo(struct Pokemon *mon, enum SelectionPressure pressure, u32 amount, u32 cap);
enum StrataDiet Selection_GetSpeciesDiet(enum Species species);
bool32 Selection_EatsAnimals(enum Species species);
enum SelectionPressure Selection_GetHabitat(u32 metatileBehavior, bool32 onShore);
void Selection_ApplyTick(enum SelectionPressure habitat, u32 heat);
void Selection_UpdateStepCounter(u16 metatileBehavior);
void Selection_OnPreyTaken(struct Pokemon *mon);
void Selection_OnFoeFainted(u32 battler);
void Selection_OnFishHooked(void);
void Strata_AddPressure(void);

#endif // GUARD_SELECTION_H
