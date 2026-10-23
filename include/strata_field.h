#ifndef GUARD_STRATA_FIELD_H
#define GUARD_STRATA_FIELD_H

bool32 Strata_HasWaders(void);
bool32 Strata_CanWade(void);
enum Item Strata_GetFishingKit(void);
enum Item Strata_UpgradeFishingKit(void);
void Strata_GiveWaterGear(void);
void Strata_SpecialUpgradeFishingKit(void);

#endif // GUARD_STRATA_FIELD_H
