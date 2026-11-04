#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "strata_acts.h"
#include "strata_ending.h"
#include "strata_fossils.h"
#include "string_util.h"
#include "text.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/characters.h"
#include "constants/strata_act_flags.h"
#include "constants/vars.h"

// The ending (roadmap S3): the rig's Colby gate before today (src/strata_acts.c), the credits'
// lineage fates from the fossil flags and the TEAM/PC (src/strata_ending.c), and the widths of
// every line the ending and the credits roll show.

#define MESSAGE_WIDTH 208
#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)

// Map script texts (data/maps/StrataInterpretive1F, StrataColby).
extern const u8 StrataInterpretive1F_Text_HalvorsenIntro[];
extern const u8 StrataInterpretive1F_Text_EndingTheme[];
extern const u8 StrataInterpretive1F_Text_EndingPrairie[];
extern const u8 StrataInterpretive1F_Text_EndingThanks[];
extern const u8 StrataInterpretive1F_Text_EndingSave[];
extern const u8 StrataInterpretive1F_Text_HalvorsenAfter[];
extern const u8 StrataInterpretive1F_Text_HalvorsenAgain[];
extern const u8 StrataColby_Text_Intro[];
extern const u8 StrataColby_Text_Bones[];
extern const u8 StrataColby_Text_Point[];
extern const u8 StrataColby_Text_PointLogged[];
extern const u8 StrataColby_Text_NoteSite[];
extern const u8 StrataColby_Text_NoteEvidence[];

static void ResetStrata(void)
{
    u32 boxId, boxPos, i;
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    VarSet(VAR_STRATA_STORY, 0);
    ZeroPlayerPartyMons();
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
            ZeroBoxMonData(GetBoxedMonPtr(boxId, boxPos));
    }
    for (i = 0; i < STRATA_FOSSIL_FLAG_COUNT; i++)
        FlagClear(FLAG_STRATA_FOSSIL_BASE + i);
    FlagClear(FLAG_STRATA_GENTLE_DEEP_TIME);
    FlagClear(FLAG_STRATA_COLBY_SEEN);
}

// The widest player name, for messages with {PLAYER}.
static void SetWidePlayerName(void)
{
    u32 i;
    for (i = 0; i < PLAYER_NAME_LENGTH; i++)
        gSaveBlock2Ptr->playerName[i] = CHAR_W;
    gSaveBlock2Ptr->playerName[PLAYER_NAME_LENGTH] = EOS;
}

// Widest line of a message, after expanding placeholders: lines end at \n, \l and \p.
static u32 WidestLine(const u8 *message)
{
    static u8 expanded[1000];
    u8 line[128];
    const u8 *str = expanded;
    u32 n = 0, widest = 0;

    StringExpandPlaceholders(expanded, message);
    for (;; str++)
    {
        if (*str == EOS || *str == CHAR_NEWLINE || *str == CHAR_PROMPT_SCROLL || *str == CHAR_PROMPT_CLEAR)
        {
            line[n] = EOS;
            widest = max(widest, (u32)GetStringWidth(FONT_NORMAL, line, 0));
            n = 0;
            if (*str == EOS)
                break;
            continue;
        }
        if (n < ARRAY_COUNT(line) - 1)
            line[n++] = *str;
    }
    return widest;
}

static bool32 Fits(const u8 *str, u32 width)
{
    return (u32)GetStringWidth(Ending_FitFont(str, width), str, 0) <= width;
}

static bool32 IsStartOf(const u8 *str, const u8 *prefix)
{
    return StringCompareN(str, prefix, StringLength(prefix)) == 0;
}

// ---- the Colby gate --------------------------------------------------------------------------

TEST("The rig holds today back until the Colby coda is seen")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_TRAP_CAVE);
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_TRAP_CAVE));

    EXPECT(Strata_IsTodayGated());
    EXPECT_EQ(Strata_GetRigState(), RIG_REENTER);
    EXPECT_EQ(Strata_GetRigTargetEra(), ERA_COUNT);
    Strata_RigQuery();
    EXPECT_EQ(gSpecialVar_Result, RIG_REENTER);
    EXPECT_EQ(gSpecialVar_0x8006, FALSE);
    // The rig says why, then names the layer it will re-enter.
    EXPECT(IsStartOf(gStringVar1, Strata_GetTodayGateText()));
    EXPECT_EQ(StringCompare(gStringVar1 + StringLength(Strata_GetTodayGateText()), Strata_GetLayerName(ERA_TRAP_CAVE)), 0);
    // Loading does nothing: no extinctions, no story change.
    RUN_OVERWORLD_SCRIPT(
        special Strata_RigLoadNext;
    );
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_TRAP_CAVE);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_ACT_DONE(ERA_TRAP_CAVE));

    // The Clovis point read: today loads.
    FlagSet(FLAG_STRATA_COLBY_SEEN);
    EXPECT(!Strata_IsTodayGated());
    EXPECT_EQ(Strata_GetRigState(), RIG_NEXT);
    EXPECT_EQ(Strata_GetRigTargetEra(), ERA_EPILOGUE);
    Strata_RigQuery();
    EXPECT_EQ(gSpecialVar_Result, RIG_NEXT);
    EXPECT_EQ(gSpecialVar_0x8006, TRUE);
    EXPECT_EQ(StringCompare(gStringVar1, Strata_GetLayerName(ERA_EPILOGUE)), 0);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CANIS, 45, 0, OTID_STRUCT_PLAYER_ID);
    CalculatePlayerPartyCount();
    Strata_RigLoadNext();
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_EPILOGUE);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_IN_ACT(ERA_EPILOGUE));
}

TEST("The Colby gate holds only the last layer")
{
    u32 act;

    ResetStrata();
    for (act = ERA_HELL_CREEK; act < ERA_TRAP_CAVE; act++)
    {
        VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(act));
        EXPECT(!Strata_IsTodayGated());
        EXPECT_EQ(Strata_GetRigState(), RIG_NEXT);
    }
    // Inside the Ice Age, before the boss: a normal re-entry, without the gate's message.
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_TRAP_CAVE));
    EXPECT(!Strata_IsTodayGated());
    Strata_RigQuery();
    EXPECT_EQ(gSpecialVar_Result, RIG_REENTER);
    EXPECT_EQ(StringCompare(gStringVar1, Strata_GetLayerName(ERA_TRAP_CAVE)), 0);
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_EPILOGUE));
    EXPECT(!Strata_IsTodayGated());
    EXPECT_EQ(Strata_GetRigState(), RIG_COMPLETE);
}

TEST("The rig's Colby message fits the message box")
{
    static u8 message[400];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_TRAP_CAVE);
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_TRAP_CAVE));
    Strata_RigQuery();
    // As StrataFieldStation_Text_EnterLayer shows it.
    StringCopy(message, COMPOUND_STRING("STRATA RIG: "));
    StringAppend(message, gStringVar1);
    StringAppend(message, COMPOUND_STRING(".\nEnter the reconstruction?"));
    EXPECT_LE(WidestLine(message), MESSAGE_WIDTH);
}

TEST("The ending and Colby texts fit the message box")
{
    static const u8 *const texts[] =
    {
        StrataInterpretive1F_Text_HalvorsenIntro,
        StrataInterpretive1F_Text_EndingTheme,
        StrataInterpretive1F_Text_EndingPrairie,
        StrataInterpretive1F_Text_EndingThanks,
        StrataInterpretive1F_Text_EndingSave,
        StrataInterpretive1F_Text_HalvorsenAfter,
        StrataInterpretive1F_Text_HalvorsenAgain,
        StrataColby_Text_Intro,
        StrataColby_Text_Bones,
        StrataColby_Text_Point,
        StrataColby_Text_PointLogged,
        StrataColby_Text_NoteSite,
        StrataColby_Text_NoteEvidence,
    };
    u32 i;

    SetWidePlayerName();
    for (i = 0; i < ARRAY_COUNT(texts); i++)
    {
        u32 width = WidestLine(texts[i]);
        if (width > MESSAGE_WIDTH)
            Test_MgbaPrintf("text %d is %d px wide", i, width);
        EXPECT_LE(width, MESSAGE_WIDTH);
    }
}

// ---- the credits' fates ----------------------------------------------------------------------

TEST("Lineage roots follow the descent table back")
{
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_CANIS), SPECIES_CIMOLESTES);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_VULPES), SPECIES_CIMOLESTES);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_EPICYON), SPECIES_CIMOLESTES);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_MELEAGRIS), SPECIES_ASTERIORNIS);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_CENTROCERCUS), SPECIES_ASTERIORNIS);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_CHELYDRA), SPECIES_EMARGINACHEL);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_MACROCHELYS), SPECIES_EMARGINACHEL);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_EQUUS), SPECIES_SIFRHIPPUS);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_CYNOMYS), SPECIES_DOUGLASSCIUR);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_BISON), SPECIES_BISON);
    EXPECT_EQ(Ending_GetLineageRoot(SPECIES_CIMOLESTES), SPECIES_CIMOLESTES);
}

TEST("The credits list each lost lineage under its layer, then the living TEAM and PC")
{
    struct EndingFate fates[ENDING_FATES_MAX];
    u32 count, overflow;
    u8 left[32], right[64];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_EPILOGUE);
    Fossil_Set(SPECIES_MAMMUTHUS);
    Fossil_Set(SPECIES_TYRANNOSAUR);
    Fossil_Set(SPECIES_EPICYON);
    Fossil_Set(SPECIES_HYOPSODUS);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CANIS, 50, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_CHELYDRA, 50, 0, OTID_STRUCT_PLAYER_ID);
    CalculatePlayerPartyCount();
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_BISON, 50, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 1), SPECIES_CANIS, 48, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(2, 5), SPECIES_MELEAGRIS, 48, 0, OTID_STRUCT_PLAYER_ID);

    count = Ending_BuildFates(fates, ARRAY_COUNT(fates), &overflow);
    EXPECT_EQ(count, 8);
    EXPECT_EQ(overflow, 0);

    // Losses, oldest filter first, each under the layer it was lost leaving.
    EXPECT_EQ(fates[0].species, SPECIES_TYRANNOSAUR);
    EXPECT_EQ(fates[0].kind, ENDING_FATE_LOST);
    EXPECT_EQ(fates[0].layer, ERA_HELL_CREEK);
    EXPECT_EQ(fates[1].species, SPECIES_HYOPSODUS);
    EXPECT_EQ(fates[1].layer, ERA_GREEN_RIVER);
    EXPECT_EQ(fates[2].species, SPECIES_EPICYON);
    EXPECT_EQ(fates[2].layer, ERA_ASHFALL);
    EXPECT_EQ(fates[3].species, SPECIES_MAMMUTHUS);
    EXPECT_EQ(fates[3].layer, ERA_TRAP_CAVE);

    // The living, TEAM first, one row per species (the PC Canis joins the TEAM's).
    EXPECT_EQ(fates[4].species, SPECIES_CANIS);
    EXPECT_EQ(fates[4].root, SPECIES_CIMOLESTES);
    EXPECT_EQ(fates[4].kind, ENDING_FATE_DESCENDED);
    EXPECT_EQ(fates[4].layer, ERA_EPILOGUE);
    EXPECT(fates[4].inTeam);
    EXPECT_EQ(fates[5].species, SPECIES_CHELYDRA);
    EXPECT_EQ(fates[5].root, SPECIES_EMARGINACHEL);
    EXPECT_EQ(fates[6].species, SPECIES_BISON);
    EXPECT_EQ(fates[6].kind, ENDING_FATE_LIVING);
    EXPECT(!fates[6].inTeam);
    EXPECT_EQ(fates[7].species, SPECIES_MELEAGRIS);
    EXPECT_EQ(fates[7].root, SPECIES_ASTERIORNIS);

    Ending_FormatFate(&fates[0], left, right);
    EXPECT_EQ(StringCompare(left, GetSpeciesName(SPECIES_TYRANNOSAUR)), 0);
    EXPECT_EQ(StringCompare(right, COMPOUND_STRING("lost at the K-Pg boundary")), 0);
    Ending_FormatFate(&fates[4], left, right);
    EXPECT_EQ(StringCompare(left, GetSpeciesName(SPECIES_CIMOLESTES)), 0);
    EXPECT_EQ(StringCompare(right, COMPOUND_STRING("descended to Canis")), 0);
    Ending_FormatFate(&fates[6], left, right);
    EXPECT_EQ(StringCompare(right, COMPOUND_STRING("living today")), 0);
}

TEST("The credits never list an animal of a lineage the record ends as living")
{
    struct EndingFate fates[ENDING_FATES_MAX];
    u32 overflow;

    ResetStrata();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_MAMMUTHUS, 50, 0, OTID_STRUCT_PLAYER_ID);
    CalculatePlayerPartyCount();
    EXPECT_EQ(Ending_BuildFates(fates, ARRAY_COUNT(fates), &overflow), 0);
}

TEST("The credits count the living that don't fit")
{
    struct EndingFate fates[3];
    u32 count, overflow;

    ResetStrata();
    Fossil_Set(SPECIES_ANZU);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CANIS, 50, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_BISON, 50, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][2], SPECIES_OVIS, 50, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][3], SPECIES_EQUUS, 50, 0, OTID_STRUCT_PLAYER_ID);
    CalculatePlayerPartyCount();
    count = Ending_BuildFates(fates, ARRAY_COUNT(fates), &overflow);
    EXPECT_EQ(count, 3);
    EXPECT_EQ(fates[0].species, SPECIES_ANZU);
    EXPECT_EQ(overflow, 2);
}

TEST("Every line of the credits roll fits its column")
{
    struct EndingFate fate = {0};
    u8 left[32], right[64], line[64];
    u32 i, species;
    const u32 leftWidth = ENDING_RIGHT_X - ENDING_LEFT_X - 4;
    const u32 rightWidth = ENDING_RIGHT_END - ENDING_RIGHT_X;
    const u32 centredWidth = ENDING_ROLL_WIDTH - 2 * ENDING_LEFT_X;

    // Bands: name on the left, age on the right, not touching.
    for (i = 0; i < Ending_GetBandCount(); i++)
    {
        const struct EndingBand *band = Ending_GetBand(i);
        u32 nameWidth = GetStringWidth(Ending_FitFont(band->name, ENDING_RIGHT_END - ENDING_LEFT_X), band->name, 0);
        u32 ageWidth = GetStringWidth(Ending_FitFont(band->age, rightWidth), band->age, 0);
        EXPECT_LE(ENDING_LEFT_X + nameWidth + 8 + ageWidth, ENDING_RIGHT_END);
    }
    // Every lineage that can be lost, at its filter; every living species, as itself or as its
    // root's descendant.
    for (species = FIRST_STRATA_SPECIES; species < SPECIES_CUSTOM_END; species++)
    {
        enum StrataEra era = Fossil_GetEra(species);
        fate.species = species;
        fate.root = Ending_GetLineageRoot(species);
        if (era < ERA_COUNT)
        {
            fate.kind = ENDING_FATE_LOST;
            fate.layer = era - 1;
        }
        else
        {
            fate.kind = fate.root != species ? ENDING_FATE_DESCENDED : ENDING_FATE_LIVING;
            fate.layer = ERA_EPILOGUE;
        }
        Ending_FormatFate(&fate, left, right);
        EXPECT(Fits(left, leftWidth));
        EXPECT(Fits(right, rightWidth));
    }
    // Centred lines.
    for (i = 0; i < gEndingCreditsLineCount; i++)
    {
        if (gEndingCreditsLines[i].text != NULL)
            EXPECT(Fits(gEndingCreditsLines[i].text, centredWidth));
    }
    EXPECT(Fits(gText_EndingColbyFind, centredWidth));
    EXPECT(Fits(gText_EndingColbyTrace, centredWidth));
    EXPECT(Fits(gText_EndingPair, centredWidth));
    EXPECT(Fits(gText_EndingNoLoss, centredWidth));
    EXPECT(Fits(gText_EndingPrelude1, centredWidth));
    EXPECT(Fits(gText_EndingPrelude2, centredWidth));
    EXPECT(Fits(gText_EndingTheEnd, centredWidth));
    EXPECT(Fits(gText_EndingTheEndLine, centredWidth));
    Ending_FormatOverflow(line, 999);
    EXPECT(Fits(line, centredWidth));
    SetWidePlayerName();
    StringExpandPlaceholders(line, gText_EndingPlayerColumn);
    EXPECT(Fits(line, centredWidth));
}
