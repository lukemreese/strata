#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "string_util.h"
#include "strata_acts.h"
#include "test/overworld_script.h"
#include "test/battle.h"
#include "test/test.h"
#include "constants/battle_ai.h"
#include "constants/flags.h"
#include "constants/strata.h"
#include "constants/vars.h"

// Boss battles and the act 1 survival rule (data/maps/StrataRiver/scripts.inc, and the
// strata_boss_prep / strata_boss_done macros in asm/macros/event.inc).

// The boss macros use these names; the overworld script test harness only knows a few.
STATIC_ASSERT(B_POSITION_OPPONENT_LEFT == 1, BossMacroAssumesOpponentLeftIsOne);
asm(".set B_POSITION_OPPONENT_LEFT, 1\n"
    ".set VAR_STRATA_BOSS_AI, " STR(VAR_STRATA_BOSS_AI) "\n"
    ".set STRATA_BOSS_AI_FLAGS, " STR(STRATA_BOSS_AI_FLAGS) "\n");

// Runs the script that settles the act after the Tyrannosaurus battle, as if the battle
// ended with `outcome`.
static void ResolveTyrannosaur(u8 outcome)
{
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_HELL_CREEK));
    FlagSet(FLAG_STRATA_TREX_FLED);
    gBattleOutcome = outcome;
    RUN_OVERWORLD_SCRIPT(call StrataRiver_EventScript_ResolveTyrannosaur;);
}

TEST("Standing your ground against the Tyrannosaurus finishes act 1 without the fled flag")
{
    u32 i = 0;
    u8 outcome = 0;
    PARAMETRIZE { outcome = B_OUTCOME_WON; }
    PARAMETRIZE { outcome = B_OUTCOME_CAUGHT; }
    ResolveTyrannosaur(outcome);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_ACT_DONE(ERA_HELL_CREEK));
    EXPECT(!FlagGet(FLAG_STRATA_TREX_FLED));
}

TEST("Running from the Tyrannosaurus finishes act 1 and sets the fled flag")
{
    u32 i = 0;
    u8 outcome = 0;
    PARAMETRIZE { outcome = B_OUTCOME_RAN; }
    PARAMETRIZE { outcome = B_OUTCOME_PLAYER_TELEPORTED; }
    PARAMETRIZE { outcome = B_OUTCOME_DREW; }
    PARAMETRIZE { outcome = B_OUTCOME_FORFEITED; }
    ResolveTyrannosaur(outcome);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_ACT_DONE(ERA_HELL_CREEK));
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), 3);
    EXPECT(FlagGet(FLAG_STRATA_TREX_FLED));
}

TEST("Dr. Halvorsen has a different line when the player ran from the Tyrannosaurus")
{
    u8 expected[] = _("You ran from a TYRANNOSAURUS");
    u8 stoodGround[] = _("You stood your ground");

    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK));

    FlagSet(FLAG_STRATA_TREX_FLED);
    Strata_BufferMentorText();
    EXPECT_EQ(StringCompareN(gStringVar4, expected, StringLength(expected)), 0);

    FlagClear(FLAG_STRATA_TREX_FLED);
    Strata_BufferMentorText();
    EXPECT_EQ(StringCompareN(gStringVar4, stoodGround, StringLength(stoodGround)), 0);
}

TEST("strata_boss_prep sets smart wild AI and the totem boost, strata_boss_done clears the AI")
{
    memset(gQueuedStatBoosts, 0, sizeof(gQueuedStatBoosts));
    VarSet(VAR_STRATA_BOSS_AI, 0);

    RUN_OVERWORLD_SCRIPT(strata_boss_prep atk=1, def=0;);
    EXPECT_EQ(VarGet(B_VAR_WILD_AI_FLAGS), STRATA_BOSS_AI_FLAGS);
    EXPECT_EQ(VarGet(VAR_STRATA_BOSS_AI), (AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY));
    EXPECT_EQ(gQueuedStatBoosts[B_POSITION_OPPONENT_LEFT].stats, 1 << STAT_ATK);
    EXPECT_EQ(gQueuedStatBoosts[B_POSITION_OPPONENT_LEFT].statChanges[STAT_ATK], 1);
    EXPECT_EQ(gQueuedStatBoosts[B_POSITION_PLAYER_LEFT].stats, 0);

    RUN_OVERWORLD_SCRIPT(strata_boss_done;);
    EXPECT_EQ(VarGet(VAR_STRATA_BOSS_AI), 0);
    memset(gQueuedStatBoosts, 0, sizeof(gQueuedStatBoosts));
}

WILD_BATTLE_TEST("A boss prepared with strata_boss_prep starts the battle with +1 Attack")
{
    RUN_OVERWORLD_SCRIPT(strata_boss_prep atk=1;);
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_TYRANNOSAUR) { Level(12); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); }
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(opponent->statStages[STAT_DEF], DEFAULT_STAT_STAGE);
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE);
    }
}

// FLAG_STRATA_EXP_SHARE is I_EXP_SHARE_FLAG; the intro in StrataFieldStation sets it.
WILD_BATTLE_TEST("The Exp. Share flag gives experience to party members that sat out the battle")
{
    bool32 shared = FALSE;
    PARAMETRIZE { shared = FALSE; }
    PARAMETRIZE { shared = TRUE; }
    if (shared)
        FlagSet(FLAG_STRATA_EXP_SHARE);
    else
        FlagClear(FLAG_STRATA_EXP_SHARE);
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        PLAYER(SPECIES_WYNAUT) { Level(40); }
        OPPONENT(SPECIES_CATERPIE) { Level(10); HP(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        MESSAGE("Wobbuffet used Scratch!");
        MESSAGE("The wild Caterpie fainted!");
    } THEN {
        if (shared)
            EXPECT_GT(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_EXP), gExperienceTables[gSpeciesInfo[SPECIES_WYNAUT].growthRate][40]);
        else
            EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_EXP), gExperienceTables[gSpeciesInfo[SPECIES_WYNAUT].growthRate][40]);
    } FINALLY {
        FlagClear(FLAG_STRATA_EXP_SHARE);
    }
}
