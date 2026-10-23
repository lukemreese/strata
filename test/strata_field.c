#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "item.h"
#include "string_util.h"
#include "strata_field.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/items.h"

// Strata water gear: waders (surf without a badge or HM) and the fishing kit.

TEST("The waders and fishing kits are key items with Strata names")
{
    static const u8 sWaders[] = _("Waders");
    static const u8 sFishingKit[] = _("Fishing Kit");

    EXPECT_EQ(GetItemPocket(ITEM_WADERS), POCKET_KEY_ITEMS);
    EXPECT_EQ(GetItemImportance(ITEM_WADERS), 1);
    EXPECT_EQ(StringCompare(GetItemName(ITEM_WADERS), sWaders), 0);
    EXPECT_EQ(GetItemPocket(ITEM_OLD_ROD), POCKET_KEY_ITEMS);
    EXPECT_EQ(StringCompare(GetItemName(ITEM_OLD_ROD), sFishingKit), 0);
}

TEST("special Strata_GiveWaterGear gives the waders and a fishing kit once")
{
    ClearBag();
    RUN_OVERWORLD_SCRIPT(
        special Strata_GiveWaterGear;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), TRUE);
    EXPECT(CheckBagHasItem(ITEM_WADERS, 1));
    EXPECT(CheckBagHasItem(ITEM_OLD_ROD, 1));
    EXPECT_EQ(Strata_GetFishingKit(), ITEM_OLD_ROD);

    RUN_OVERWORLD_SCRIPT(
        special Strata_GiveWaterGear;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), FALSE);
    EXPECT(!CheckBagHasItem(ITEM_WADERS, 2));
}

TEST("The player can wade in only with the waders and when not already in the water")
{
    u8 savedFlags = gPlayerAvatar.flags;

    ClearBag();
    gPlayerAvatar.flags = 0;
    EXPECT(!Strata_CanWade());
    AddBagItem(ITEM_WADERS, 1);
    EXPECT(Strata_CanWade());
    gPlayerAvatar.flags = PLAYER_AVATAR_FLAG_SURFING;
    EXPECT(!Strata_CanWade());
    gPlayerAvatar.flags = savedFlags;
}

TEST("Upgrading the fishing kit replaces it with the next rod up")
{
    ClearBag();
    AddBagItem(ITEM_OLD_ROD, 1);

    EXPECT_EQ(Strata_UpgradeFishingKit(), ITEM_GOOD_ROD);
    EXPECT(!CheckBagHasItem(ITEM_OLD_ROD, 1));
    EXPECT(CheckBagHasItem(ITEM_GOOD_ROD, 1));

    VarSet(VAR_RESULT, 0);
    RUN_OVERWORLD_SCRIPT(
        special Strata_SpecialUpgradeFishingKit;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), ITEM_SUPER_ROD);
    EXPECT(!CheckBagHasItem(ITEM_GOOD_ROD, 1));
    EXPECT_EQ(Strata_GetFishingKit(), ITEM_SUPER_ROD);

    EXPECT_EQ(Strata_UpgradeFishingKit(), ITEM_NONE);
    EXPECT_EQ(Strata_GetFishingKit(), ITEM_SUPER_ROD);
}
