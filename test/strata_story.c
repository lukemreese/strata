#include "global.h"
#include "event_data.h"
#include "pokedex.h"
#include "strata_acts.h"
#include "strata_story.h"
#include "string_util.h"
#include "text.h"
#include "test/test.h"
#include "constants/characters.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/strata.h"
#include "constants/vars.h"

// The present-day subplot (S1, src/strata_story.c), Dr. Halvorsen's lines by story x subplot
// (S2, src/strata_acts.c), the field log line, and the interlude scripts' text.

#define MESSAGE_WIDTH 208

// Every text the interludes added to the hub map scripts (data/maps/Strata*/scripts.inc).
#define STORY_SCRIPT_TEXTS(X) \
    X(StrataFieldStation_Text_StoryKessler1) \
    X(StrataFieldStation_Text_StoryKessler2) \
    X(StrataFieldStation_Text_StoryKessler3) \
    X(StrataFieldStation_Text_StoryKessler4) \
    X(StrataFieldStation_Text_StoryKessler5) \
    X(StrataFieldStation_Text_StoryJosie1) \
    X(StrataFieldStation_Text_StoryJosie2) \
    X(StrataFieldStation_Text_StoryRefusal1) \
    X(StrataFieldStation_Text_StoryRefusal2) \
    X(StrataFieldStation_Text_StoryRefusal3) \
    X(StrataFieldStation_Text_StoryRefusal4) \
    X(StrataFieldStation_Text_StoryConsortium1) \
    X(StrataFieldStation_Text_StoryConsortium2) \
    X(StrataFieldStation_Text_VisitorKessler) \
    X(StrataFieldStation_Text_VisitorTheo) \
    X(StrataFieldStation_Text_VisitorJosie) \
    X(StrataLindqvistRanch_Text_StoryFern1) \
    X(StrataLindqvistRanch_Text_StoryFern2) \
    X(StrataLindqvistRanch_Text_StoryDate1) \
    X(StrataLindqvistRanch_Text_StoryDate2) \
    X(StrataLindqvistRanch_Text_StoryAuction1) \
    X(StrataLindqvistRanch_Text_StoryAuction2) \
    X(StrataLindqvistRanch_Text_StoryAuction3) \
    X(StrataLindqvistRanch_Text_StoryAuction4) \
    X(StrataLindqvistRanch_Text_JosieDate) \
    X(StrataLindqvistRanch_Text_JosieAfter) \
    X(StrataLindqvistRanch_Text_Halvorsen) \
    X(StrataLindqvistRanch_Text_BeaDate) \
    X(StrataLindqvistRanch_Text_BeaSold) \
    X(StrataJordan_Text_StoryCitation1) \
    X(StrataJordan_Text_StoryCitation2) \
    X(StrataJordan_Text_StoryCitation3) \
    X(StrataJordan_Text_Ortiz) \
    X(StrataJordan_Text_Kessler) \
    X(StrataBlmOffice_Text_RangerCase) \
    X(StrataBlmOffice_Text_RangerCited) \
    X(StrataSandArroyo_Text_StoryJosiesPit) \
    X(StrataSandArroyo_Text_StoryOrtizBrief) \
    X(StrataSandArroyo_Text_StoryOrtizRemind) \
    X(StrataSandArroyo_Text_StoryOrtizReport) \
    X(StrataSandArroyo_Text_StoryOrtizDone) \
    X(StrataSandArroyo_Text_StoryLogPit) \
    X(StrataSandArroyo_Text_StoryLogJacket) \
    X(StrataSandArroyo_Text_StoryLogTracks) \
    X(StrataSandArroyo_Text_StoryLogged) \
    X(StrataFieldCamp_Text_TheoCard) \
    X(StrataFieldCamp_Text_JosiePit) \
    X(StrataFieldCamp_Text_JosieDocumented) \
    X(StrataFieldCamp_Text_JosieAuction) \
    X(StrataFieldCamp_Text_JosieMuseum)

#define DECLARE_TEXT(label) extern const u8 label[];
STORY_SCRIPT_TEXTS(DECLARE_TEXT)
#define LIST_TEXT(label) label,
static const u8 *const sStoryScriptTexts[] = { STORY_SCRIPT_TEXTS(LIST_TEXT) };

// The widest the placeholders get: a full-length player name and a three-digit Codex count.
static void WidestPlaceholders(void)
{
    u32 i;
    for (i = 0; i < PLAYER_NAME_LENGTH; i++)
        gSaveBlock2Ptr->playerName[i] = CHAR_W;
    gSaveBlock2Ptr->playerName[PLAYER_NAME_LENGTH] = EOS;
    StringCopy(gStringVar1, COMPOUND_STRING("888"));
}

// Widest line of a message (lines end at \n, \l and \p), and the most \n in any one page
// (a field message box shows two lines: the second of a page must come with \n, the rest \l).
static u32 WidestLine(const u8 *str, u32 *maxBreaksPerPage)
{
    u8 line[128];
    u32 n = 0, widest = 0, breaks = 0;
    *maxBreaksPerPage = 0;
    for (;; str++)
    {
        if (*str == EOS || *str == CHAR_NEWLINE || *str == CHAR_PROMPT_SCROLL || *str == CHAR_PROMPT_CLEAR)
        {
            line[n] = EOS;
            widest = max(widest, (u32)GetStringWidth(FONT_NORMAL, line, 0));
            n = 0;
            if (*str == CHAR_NEWLINE)
                breaks++;
            *maxBreaksPerPage = max(*maxBreaksPerPage, breaks);
            if (*str == CHAR_PROMPT_CLEAR)
                breaks = 0;
            if (*str == EOS)
                break;
            continue;
        }
        if (n < ARRAY_COUNT(line) - 1)
            line[n++] = *str;
    }
    return widest;
}

static bool32 Contains(const u8 *haystack, const u8 *needle)
{
    u32 i, j;
    for (i = 0; haystack[i] != EOS; i++)
    {
        for (j = 0; needle[j] != EOS && haystack[i + j] == needle[j]; j++)
            ;
        if (needle[j] == EOS)
            return TRUE;
    }
    return FALSE;
}

// No stock creature word anywhere the player reads (strata-text skill).
static bool32 HasStockTerm(const u8 *str)
{
    return Contains(str, COMPOUND_STRING("Pokémon")) || Contains(str, COMPOUND_STRING("POKéMON"))
        || Contains(str, COMPOUND_STRING("Poké")) || Contains(str, COMPOUND_STRING("POKé"));
}

static void ResetStory(void)
{
    VarSet(VAR_STRATA_STORY, 1);
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_NONE);
    FlagClear(FLAG_STRATA_TREX_FLED);
    FlagClear(FLAG_STRATA_BLM_PERMIT);
    FlagClear(FLAG_STRATA_DIG_DONE);
    FlagClear(FLAG_STRATA_STORY_SAW_PIT);
    FlagClear(FLAG_STRATA_STORY_EVIDENCE_STARTED);
    FlagClear(FLAG_STRATA_STORY_EVIDENCE_PIT);
    FlagClear(FLAG_STRATA_STORY_EVIDENCE_JACKET);
    FlagClear(FLAG_STRATA_STORY_EVIDENCE_TRACKS);
}

static void SetLocation(u32 map)
{
    gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(map);
    gSaveBlock1Ptr->location.mapNum = MAP_NUM(map);
}

// ---------------------------------------------------------------------------
// Subplot progression
// ---------------------------------------------------------------------------

TEST("Story beats play in order, each once its act is done")
{
    u32 story, subplot = SUBPLOT_NONE, beat, played = 0;

    for (story = 0; story <= STORY_IN_ACT(ERA_EPILOGUE); story++)
    {
        while ((beat = Story_PendingBeat(story, subplot)) != SUBPLOT_NONE)
        {
            EXPECT_EQ(beat, subplot + 1);
            EXPECT_GE(story, STORY_ACT_DONE(Story_BeatAct(beat)));
            // Due as soon as its act is done, not before.
            EXPECT_EQ(Story_PendingBeat(STORY_ACT_DONE(Story_BeatAct(beat)) - 1, subplot), SUBPLOT_NONE);
            subplot = beat;
            played++;
        }
        EXPECT_EQ(subplot, Story_ExpectedSubplot(story));
    }
    EXPECT_EQ(played, SUBPLOT_COUNT - 1);
    EXPECT_EQ(subplot, SUBPLOT_AUCTION_DAY);
}

TEST("Each act from 1 to 8 has an interlude, and the beats follow the outline")
{
    u32 act, beat;
    bool32 hasBeat;

    for (act = ERA_HELL_CREEK; act <= ERA_TRAP_CAVE; act++)
    {
        hasBeat = FALSE;
        for (beat = SUBPLOT_KESSLER_OFFER; beat < SUBPLOT_COUNT; beat++)
        {
            if (Story_BeatAct(beat) == act)
                hasBeat = TRUE;
        }
        EXPECT(hasBeat);
    }
    // docs/strata_outline.md §1.5: what happens after which act.
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_HELL_CREEK)), SUBPLOT_KESSLER_OFFER);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_IMPACT_WINTER)), SUBPLOT_BLM_PERMIT);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_CORRAL_BLUFFS)), SUBPLOT_JOSIE_PIT);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_BIGHORN_PETM)), SUBPLOT_HALVORSEN_REFUSAL);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_GREEN_RIVER)), SUBPLOT_PIT_DOCUMENTED);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_WHITE_RIVER)), SUBPLOT_AUCTION_DATE);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_ASHFALL)), SUBPLOT_CONSORTIUM);
    EXPECT_EQ(Story_ExpectedSubplot(STORY_ACT_DONE(ERA_TRAP_CAVE)), SUBPLOT_AUCTION_DAY);
    EXPECT_EQ(Story_ExpectedSubplot(1), SUBPLOT_NONE);
    // Each beat plays in the hub: the station, the ranch, Jordan, its BLM office or the arroyo.
    for (beat = SUBPLOT_KESSLER_OFFER; beat < SUBPLOT_COUNT; beat++)
    {
        u32 map = Story_BeatMap(beat);
        EXPECT(map == MAP_STRATA_FIELD_STATION || map == MAP_STRATA_LINDQVIST_RANCH || map == MAP_STRATA_JORDAN
            || map == MAP_STRATA_BLM_OFFICE || map == MAP_STRATA_SAND_ARROYO);
    }
}

TEST("A skipped beat waits, and the later ones queue behind it")
{
    // The player never visited Jordan for the permit, and finished acts 3 and 4.
    EXPECT_EQ(Story_PendingBeat(STORY_ACT_DONE(ERA_BIGHORN_PETM), SUBPLOT_FERN_SPIKE), SUBPLOT_BLM_PERMIT);
    EXPECT_EQ(Story_PendingBeat(STORY_ACT_DONE(ERA_BIGHORN_PETM), SUBPLOT_BLM_PERMIT), SUBPLOT_JOSIE_PIT);
    EXPECT_EQ(Story_PendingBeat(STORY_ACT_DONE(ERA_BIGHORN_PETM), SUBPLOT_JOSIE_PIT), SUBPLOT_HALVORSEN_REFUSAL);
    EXPECT_EQ(Story_PendingBeat(STORY_ACT_DONE(ERA_BIGHORN_PETM), SUBPLOT_HALVORSEN_REFUSAL), SUBPLOT_NONE);
    // Inside an act, nothing new is due.
    EXPECT_EQ(Story_PendingBeat(STORY_IN_ACT(ERA_CORRAL_BLUFFS), SUBPLOT_BLM_PERMIT), SUBPLOT_NONE);
    // The epilogue still lets an unplayed auction day happen.
    EXPECT_EQ(Story_PendingBeat(STORY_IN_ACT(ERA_EPILOGUE), SUBPLOT_CONSORTIUM), SUBPLOT_AUCTION_DAY);
    EXPECT_EQ(Story_PendingBeat(STORY_IN_ACT(ERA_EPILOGUE), SUBPLOT_AUCTION_DAY), SUBPLOT_NONE);
}

TEST("Strata_StoryPrepareMap flags the beat only on its own map")
{
    ResetStory();
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK));
    SetLocation(MAP_STRATA_FIELD_STATION);
    Strata_StoryPrepareMap();
    EXPECT_EQ(VarGet(VAR_TEMP_2), SUBPLOT_KESSLER_OFFER);
    EXPECT_EQ(VarGet(VAR_TEMP_3), 1);
    EXPECT_EQ(VarGet(VAR_TEMP_4), SUBPLOT_KESSLER_OFFER);

    SetLocation(MAP_STRATA_LINDQVIST_RANCH);
    Strata_StoryPrepareMap();
    EXPECT_EQ(VarGet(VAR_TEMP_2), SUBPLOT_NONE);
    EXPECT_EQ(VarGet(VAR_TEMP_3), 0);
    EXPECT_EQ(VarGet(VAR_TEMP_4), SUBPLOT_KESSLER_OFFER);

    // Caught up: nothing anywhere.
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_KESSLER_OFFER);
    SetLocation(MAP_STRATA_FIELD_STATION);
    Strata_StoryPrepareMap();
    EXPECT_EQ(VarGet(VAR_TEMP_2), SUBPLOT_NONE);
    EXPECT_EQ(VarGet(VAR_TEMP_3), 0);
    EXPECT_EQ(VarGet(VAR_TEMP_4), SUBPLOT_NONE);

    // Act 2 done: the fern spike is at the ranch.
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_IMPACT_WINTER));
    SetLocation(MAP_STRATA_LINDQVIST_RANCH);
    Strata_StoryPrepareMap();
    EXPECT_EQ(VarGet(VAR_TEMP_2), SUBPLOT_FERN_SPIKE);
    EXPECT_EQ(VarGet(VAR_TEMP_3), 1);
}

TEST("A save that already holds the permit skips the permit beat")
{
    ResetStory();
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_CORRAL_BLUFFS));
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_FERN_SPIKE);
    FlagSet(FLAG_STRATA_BLM_PERMIT);
    SetLocation(MAP_STRATA_FIELD_STATION);
    Strata_StoryPrepareMap();
    EXPECT_EQ(VarGet(VAR_STRATA_SUBPLOT), SUBPLOT_BLM_PERMIT);
    EXPECT_EQ(VarGet(VAR_TEMP_2), SUBPLOT_JOSIE_PIT);
    FlagClear(FLAG_STRATA_BLM_PERMIT);
}

// ---------------------------------------------------------------------------
// Dr. Halvorsen (S2)
// ---------------------------------------------------------------------------

TEST("Dr. Halvorsen has a line for every story x subplot that fits the message box")
{
    u32 story, subplot, trex, breaks;
    WidestPlaceholders();
    for (trex = 0; trex < 2; trex++)
    {
        ResetStory();
        if (trex)
            FlagSet(FLAG_STRATA_TREX_FLED);
        for (story = 1; story <= STORY_IN_ACT(ERA_EPILOGUE); story++)
        {
            for (subplot = SUBPLOT_NONE; subplot < SUBPLOT_COUNT; subplot++)
            {
                VarSet(VAR_STRATA_STORY, story);
                VarSet(VAR_STRATA_SUBPLOT, subplot);
                WidestPlaceholders();
                Strata_BufferMentorText();
                EXPECT_NE(gStringVar4[0], EOS);
                EXPECT_NE(StringCompare(gStringVar4, COMPOUND_STRING("Keep up the good work out there.")), 0);
                EXPECT_LT(StringLength(gStringVar4), sizeof(gStringVar4) - 1);
                EXPECT_LE(WidestLine(gStringVar4, &breaks), MESSAGE_WIDTH);
                EXPECT_LE(breaks, 1);
                EXPECT(!HasStockTerm(gStringVar4));
            }
        }
    }
    FlagClear(FLAG_STRATA_TREX_FLED);
}

TEST("Dr. Halvorsen's lines follow the subplot")
{
    u8 before[sizeof(gStringVar4)];

    ResetStory();
    // A beat is due: she says where it waits.
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK));
    Strata_BufferMentorText();
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("truck")));
    // Played: what she makes of it.
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_KESSLER_OFFER);
    Strata_BufferMentorText();
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("I said no")));

    // The same story value reads differently before and after the refusal.
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_GREEN_RIVER));
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_JOSIE_PIT);
    Strata_BufferMentorText();
    StringCopy(before, gStringVar4);
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_HALVORSEN_REFUSAL);
    Strata_BufferMentorText();
    EXPECT_NE(StringCompare(before, gStringVar4), 0);
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("subtropical")));

    // The consortium line counts the research case.
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_TRAP_CAVE));
    VarSet(VAR_STRATA_SUBPLOT, SUBPLOT_CONSORTIUM);
    Strata_BufferMentorText();
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("species, each tied")));
    EXPECT(!Contains(gStringVar4, COMPOUND_STRING("{STR_VAR_1}")));
}

TEST("Dr. Halvorsen keeps the Tyrannosaurus line whatever the subplot")
{
    u8 fled[] = _("You ran from a TYRANNOSAURUS");
    u32 subplot;

    ResetStory();
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK));
    FlagSet(FLAG_STRATA_TREX_FLED);
    for (subplot = SUBPLOT_NONE; subplot <= SUBPLOT_KESSLER_OFFER; subplot++)
    {
        VarSet(VAR_STRATA_SUBPLOT, subplot);
        Strata_BufferMentorText();
        EXPECT_EQ(StringCompareN(gStringVar4, fled, StringLength(fled)), 0);
    }
    FlagClear(FLAG_STRATA_TREX_FLED);
}

// ---------------------------------------------------------------------------
// The field log (start menu)
// ---------------------------------------------------------------------------

static void ExpectQuestLineFits(const u8 *line)
{
    u32 i, newlines = 0;
    EXPECT(line != NULL);
    EXPECT_NE(line[0], EOS);
    for (i = 0; line[i] != EOS; i++)
    {
        EXPECT_NE(line[i], CHAR_PROMPT_CLEAR);
        EXPECT_NE(line[i], CHAR_PROMPT_SCROLL);
        EXPECT_NE(line[i], PLACEHOLDER_BEGIN);
        if (line[i] == CHAR_NEWLINE)
            newlines++;
    }
    EXPECT_LT(newlines, STORY_LOG_LINES);
    EXPECT_LE(GetStringWidth(FONT_NORMAL, line, 0), STORY_LOG_WIDTH_PX);
    EXPECT(!HasStockTerm(line));
}

TEST("The field log has a line that fits its window for every state")
{
    u32 story, subplot, flags, logged;

    for (flags = 0; flags < 4; flags++)
    {
        ResetStory();
        if (flags & 1)
            FlagSet(FLAG_STRATA_DIG_DONE);
        if (flags & 2)
            FlagSet(FLAG_STRATA_STORY_SAW_PIT);
        for (story = 0; story <= STORY_IN_ACT(ERA_EPILOGUE); story++)
        {
            for (subplot = SUBPLOT_NONE; subplot < SUBPLOT_COUNT; subplot++)
                ExpectQuestLineFits(Story_QuestLine(story, subplot));
        }
    }
    // Ortiz's evidence scene, each count of records.
    ResetStory();
    FlagSet(FLAG_STRATA_STORY_EVIDENCE_STARTED);
    for (logged = 0; logged <= STORY_EVIDENCE_COUNT; logged++)
    {
        if (logged >= 1)
            FlagSet(FLAG_STRATA_STORY_EVIDENCE_PIT);
        if (logged >= 2)
            FlagSet(FLAG_STRATA_STORY_EVIDENCE_JACKET);
        if (logged >= 3)
            FlagSet(FLAG_STRATA_STORY_EVIDENCE_TRACKS);
        EXPECT_EQ(Story_EvidenceLogged(), logged);
        ExpectQuestLineFits(Story_QuestLine(STORY_ACT_DONE(ERA_GREEN_RIVER), SUBPLOT_HALVORSEN_REFUSAL));
    }
    ResetStory();
}

TEST("The field log points at the next thing to do")
{
    ResetStory();
    EXPECT(Contains(Story_QuestLine(0, SUBPLOT_NONE), COMPOUND_STRING("HALVORSEN")));
    EXPECT(Contains(Story_QuestLine(1, SUBPLOT_NONE), COMPOUND_STRING("DALE")));
    FlagSet(FLAG_STRATA_DIG_DONE);
    EXPECT(Contains(Story_QuestLine(1, SUBPLOT_NONE), COMPOUND_STRING("Hell Creek")));
    EXPECT(Contains(Story_QuestLine(STORY_IN_ACT(ERA_HELL_CREEK), SUBPLOT_NONE), COMPOUND_STRING("tyrant")));
    // Act 2 done: the ranch, then Jordan, then the rig.
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_IMPACT_WINTER), SUBPLOT_KESSLER_OFFER), COMPOUND_STRING("RANCH")));
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_IMPACT_WINTER), SUBPLOT_FERN_SPIKE), COMPOUND_STRING("JORDAN")));
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_IMPACT_WINTER), SUBPLOT_BLM_PERMIT), COMPOUND_STRING("next layer")));
    // Josie's pit: go and look, then move on.
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_CORRAL_BLUFFS), SUBPLOT_JOSIE_PIT), COMPOUND_STRING("pit")));
    FlagSet(FLAG_STRATA_STORY_SAW_PIT);
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_CORRAL_BLUFFS), SUBPLOT_JOSIE_PIT), COMPOUND_STRING("next layer")));
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_GREEN_RIVER), SUBPLOT_HALVORSEN_REFUSAL), COMPOUND_STRING("ORTIZ")));
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_TRAP_CAVE), SUBPLOT_CONSORTIUM), COMPOUND_STRING("auction")));
    EXPECT(Contains(Story_QuestLine(STORY_ACT_DONE(ERA_TRAP_CAVE), SUBPLOT_AUCTION_DAY), COMPOUND_STRING("last layer")));
    ResetStory();
}

// ---------------------------------------------------------------------------
// The interlude scripts' text
// ---------------------------------------------------------------------------

TEST("Interlude texts fit the message box")
{
    u32 i, breaks;
    for (i = 0; i < ARRAY_COUNT(sStoryScriptTexts); i++)
    {
        WidestPlaceholders();
        StringExpandPlaceholders(gStringVar4, sStoryScriptTexts[i]);
        EXPECT_LE(WidestLine(gStringVar4, &breaks), MESSAGE_WIDTH);
        EXPECT_LE(breaks, 1);
        EXPECT(!HasStockTerm(gStringVar4));
    }
}
