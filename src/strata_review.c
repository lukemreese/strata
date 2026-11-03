#include "global.h"
#include "event_data.h"
#include "money.h"
#include "pokedex.h"
#include "string_util.h"
#include "strata_review.h"
#include "constants/flags.h"
#include "constants/strata.h"
#include "constants/vars.h"

// Peer review and the survey stipend, the two sources of money in Strata.
//
// The visiting researchers (data/maps/StrataFieldCamp, StrataFieldStation, StrataLindqvistRanch
// and StrataJordan scripts) are placed in the hub and unlock as acts are done: researcher N is
// hidden by FLAG_TEMP_N until VAR_STRATA_STORY reaches STORY_ACT_DONE(N). The hub maps call
// special Strata_HideLockedReviewers when they load.
//
// The stipend is paid by Dr. Halvorsen (StrataFieldStation_EventScript_Mentor): a fixed amount
// for every Codex "caught" entry gained since the last payment.

// Acts finished at a story value: 0 until act 1 is done, 8 once the Ice Age is done and after.
u32 Strata_ActsDone(u32 story)
{
    u32 done;

    if (story < STORY_IN_ACT(ERA_HELL_CREEK))
        return 0;
    done = (story - 1) / 2;
    if (done > ERA_TRAP_CAVE)
        done = ERA_TRAP_CAVE;
    return done;
}

// Dollars per new Codex entry: the consortium's grant grows with every act finished.
u32 Strata_StipendRate(u32 story)
{
    return STRATA_STIPEND_BASE + STRATA_STIPEND_PER_ACT * Strata_ActsDone(story);
}

u32 Strata_StipendAmount(u32 newEntries, u32 story)
{
    return newEntries * Strata_StipendRate(story);
}

// special Strata_HideLockedReviewers
// Sets the hide flag of every visiting researcher whose act isn't done yet, clears the others.
void Strata_HideLockedReviewers(void)
{
    u32 story = VarGet(VAR_STRATA_STORY);
    u32 act;

    for (act = ERA_HELL_CREEK; act <= ERA_TRAP_CAVE; act++)
    {
        if (story < STORY_ACT_DONE(act))
            FlagSet(STRATA_REVIEWER_HIDE_FLAG(act));
        else
            FlagClear(STRATA_REVIEWER_HIDE_FLAG(act));
    }
}

// special Strata_PayStipend
// Pays for the Codex "caught" entries gained since the last payment.
// Output: VAR_RESULT = dollars paid (0 if nothing new); gStringVar1 = new entries,
// gStringVar2 = dollars per entry, gStringVar3 = dollars paid.
void Strata_PayStipend(void)
{
    u32 caught = GetNationalPokedexCount(FLAG_GET_CAUGHT);
    u32 paid = VarGet(VAR_STRATA_STIPEND_COUNT);
    u32 fresh = caught > paid ? caught - paid : 0;
    u32 story = VarGet(VAR_STRATA_STORY);
    u32 amount = Strata_StipendAmount(fresh, story);

    if (fresh != 0)
    {
        AddMoney(&gSaveBlock1Ptr->money, amount);
        VarSet(VAR_STRATA_STIPEND_COUNT, caught);
    }
    ConvertIntToDecimalStringN(gStringVar1, fresh, STR_CONV_MODE_LEFT_ALIGN, 3);
    ConvertIntToDecimalStringN(gStringVar2, Strata_StipendRate(story), STR_CONV_MODE_LEFT_ALIGN, 3);
    ConvertIntToDecimalStringN(gStringVar3, amount, STR_CONV_MODE_LEFT_ALIGN, MAX_MONEY_DIGITS);
    gSpecialVar_Result = amount;
}

// special Strata_StipendBaseline
// Counts the entries the player has now as already paid for (the starter is a gift, not a find).
void Strata_StipendBaseline(void)
{
    VarSet(VAR_STRATA_STIPEND_COUNT, GetNationalPokedexCount(FLAG_GET_CAUGHT));
}
