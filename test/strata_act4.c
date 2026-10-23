#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "item.h"
#include "strata_field.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/strata.h"
#include "constants/vars.h"

// Act 4, Bighorn Basin (tools/strata/maps/act4_bighorn.py, data/maps/StrataRedBeds,
// StrataClarksFork): the Coryphodon boss's story state, the one-time fishing kit
// upgrade, and the Oxyaena set piece at the Clarks Fork ford.

static void ResolveCoryphodon(void)
{
    RUN_OVERWORLD_SCRIPT(call StrataRedBeds_EventScript_ResolveCoryphodon;);
}

TEST("Beating the Coryphodon finishes act 4")
{
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_BIGHORN_PETM));
    ResolveCoryphodon();
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_ACT_DONE(ERA_BIGHORN_PETM));
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), 9);
}

TEST("The Coryphodon boss asks for the fishing kit upgrade once, and the Old kit becomes the Good kit")
{
    ClearBag();
    AddBagItem(ITEM_OLD_ROD, 1);
    FlagClear(FLAG_STRATA_ACT4_KIT_UPGRADED);

    ResolveCoryphodon();
    EXPECT_EQ(VarGet(VAR_0x8004), TRUE);
    EXPECT(FlagGet(FLAG_STRATA_ACT4_KIT_UPGRADED));
    EXPECT_EQ(Strata_UpgradeFishingKit(), ITEM_GOOD_ROD);     // what Strata_EventScript_UpgradeFishingKit does
    EXPECT_EQ(Strata_GetFishingKit(), ITEM_GOOD_ROD);

    // A second battle (or a reload of the same script) never upgrades it again.
    ResolveCoryphodon();
    EXPECT_EQ(VarGet(VAR_0x8004), FALSE);
    EXPECT_EQ(Strata_GetFishingKit(), ITEM_GOOD_ROD);
}

static void ResolveOxyaena(u8 outcome)
{
    VarSet(VAR_STRATA_ACT4, 0);
    FlagClear(FLAG_STRATA_ACT4_OXYAENA);
    gBattleOutcome = outcome;
    RUN_OVERWORLD_SCRIPT(call StrataClarksFork_EventScript_ResolveOxyaena;);
}

TEST("Beating or catching the Oxyaena ends the set piece and removes it")
{
    u32 i = 0;
    u8 outcome = 0;
    PARAMETRIZE { outcome = B_OUTCOME_WON; }
    PARAMETRIZE { outcome = B_OUTCOME_CAUGHT; }
    ResolveOxyaena(outcome);
    EXPECT_EQ(VarGet(VAR_STRATA_ACT4), 1);
    EXPECT(FlagGet(FLAG_STRATA_ACT4_OXYAENA));
    EXPECT_EQ(VarGet(VAR_RESULT), TRUE);
}

TEST("Running from the Oxyaena stops the stalking but leaves it to fight again")
{
    u32 i = 0;
    u8 outcome = 0;
    PARAMETRIZE { outcome = B_OUTCOME_RAN; }
    PARAMETRIZE { outcome = B_OUTCOME_PLAYER_TELEPORTED; }
    PARAMETRIZE { outcome = B_OUTCOME_DREW; }
    ResolveOxyaena(outcome);
    EXPECT_EQ(VarGet(VAR_STRATA_ACT4), 1);
    EXPECT(!FlagGet(FLAG_STRATA_ACT4_OXYAENA));
    EXPECT_EQ(VarGet(VAR_RESULT), FALSE);
}
