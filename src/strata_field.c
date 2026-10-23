#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "item.h"
#include "string_util.h"
#include "strata_field.h"
#include "constants/items.h"

// Field gear for Strata's deep-time layers. The player is a field assistant, not
// a trainer with badges: waders let them wade into any surfable water (the
// reconstruction "handles the depth"), and the fishing kit is the Old Rod,
// renamed in src/data/items.h, upgraded to the Good and Super Rod later.
// Scripts give these through data/scripts/strata_gear.inc.

static const u16 sFishingKits[] = { ITEM_OLD_ROD, ITEM_GOOD_ROD, ITEM_SUPER_ROD };

bool32 Strata_HasWaders(void)
{
    return CheckBagHasItem(ITEM_WADERS, 1);
}

// TRUE if pressing A at the water's edge should offer to wade in.
bool32 Strata_CanWade(void)
{
    return Strata_HasWaders() && !TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING | PLAYER_AVATAR_FLAG_UNDERWATER);
}

// The best fishing kit in the bag, or ITEM_NONE.
enum Item Strata_GetFishingKit(void)
{
    s32 i;
    for (i = ARRAY_COUNT(sFishingKits) - 1; i >= 0; i--)
    {
        if (CheckBagHasItem(sFishingKits[i], 1))
            return sFishingKits[i];
    }
    return ITEM_NONE;
}

// Replaces the fishing kit with the next one up (none -> Old -> Good -> Super),
// so the bag only ever holds one. Returns the kit now held, or ITEM_NONE if it
// was already the best or the bag was full.
enum Item Strata_UpgradeFishingKit(void)
{
    enum Item current = Strata_GetFishingKit(), next;
    u32 i;

    if (current == ITEM_SUPER_ROD)
        return ITEM_NONE;
    next = (current == ITEM_NONE) ? ITEM_OLD_ROD : (current == ITEM_OLD_ROD) ? ITEM_GOOD_ROD : ITEM_SUPER_ROD;
    if (!AddBagItem(next, 1))
        return ITEM_NONE;
    for (i = 0; i < ARRAY_COUNT(sFishingKits); i++)
    {
        if (sFishingKits[i] != next && CheckBagHasItem(sFishingKits[i], 1))
            RemoveBagItem(sFishingKits[i], 1);
    }
    return next;
}

// special Strata_GiveWaterGear
// Silently gives the waders and the first fishing kit, if the player lacks them.
// Output: VAR_RESULT = TRUE if anything was given
void Strata_GiveWaterGear(void)
{
    gSpecialVar_Result = FALSE;
    if (!Strata_HasWaders() && AddBagItem(ITEM_WADERS, 1))
        gSpecialVar_Result = TRUE;
    if (Strata_GetFishingKit() == ITEM_NONE && AddBagItem(ITEM_OLD_ROD, 1))
        gSpecialVar_Result = TRUE;
}

// special Strata_SpecialUpgradeFishingKit
// Output: VAR_RESULT = the kit now held, or ITEM_NONE if nothing changed
//         STR_VAR_1  = its name
void Strata_SpecialUpgradeFishingKit(void)
{
    gSpecialVar_Result = Strata_UpgradeFishingKit();
    if (gSpecialVar_Result != ITEM_NONE)
        CopyItemName(gSpecialVar_Result, gStringVar1);
}
