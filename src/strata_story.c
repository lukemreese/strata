#include "global.h"
#include "event_data.h"
#include "map_name_popup.h"
#include "menu.h"
#include "pokedex.h"
#include "strata_story.h"
#include "string_util.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/vars.h"

// The present-day subplot (S1): one interlude at the hub after each act, in a fixed order
// (docs/strata_outline.md §1.5). VAR_STRATA_SUBPLOT is the last beat played. The next beat is due
// once its act is done; it plays on its own map, when the player arrives (a frame-table script
// on the ranch and in Jordan, a coord trigger row in the field station, a talk with Ranger Ortiz
// at the BLM office and at the pit). A beat the player walks past waits; nothing gates the rig.
//
// The scripts are in data/maps/StrataFieldStation, StrataLindqvistRanch, StrataJordan,
// StrataBlmOffice and StrataSandArroyo. Dr. Halvorsen's lines, which follow the subplot too, are
// in src/strata_acts.c.

struct StoryBeat
{
    u8 act;   // the act whose end makes it due
    u16 map;  // where it plays
};

static const struct StoryBeat sStoryBeats[SUBPLOT_COUNT] =
{
    [SUBPLOT_KESSLER_OFFER]     = { ERA_HELL_CREEK,    MAP_STRATA_FIELD_STATION },
    [SUBPLOT_FERN_SPIKE]        = { ERA_IMPACT_WINTER, MAP_STRATA_LINDQVIST_RANCH },
    [SUBPLOT_BLM_PERMIT]        = { ERA_IMPACT_WINTER, MAP_STRATA_BLM_OFFICE },
    [SUBPLOT_JOSIE_PIT]         = { ERA_CORRAL_BLUFFS, MAP_STRATA_FIELD_STATION },
    [SUBPLOT_HALVORSEN_REFUSAL] = { ERA_BIGHORN_PETM,  MAP_STRATA_FIELD_STATION },
    [SUBPLOT_PIT_DOCUMENTED]    = { ERA_GREEN_RIVER,   MAP_STRATA_SAND_ARROYO },
    [SUBPLOT_AUCTION_DATE]      = { ERA_WHITE_RIVER,   MAP_STRATA_LINDQVIST_RANCH },
    [SUBPLOT_CITATION]          = { ERA_ASHFALL,       MAP_STRATA_JORDAN },
    [SUBPLOT_CONSORTIUM]        = { ERA_ASHFALL,       MAP_STRATA_FIELD_STATION },
    [SUBPLOT_AUCTION_DAY]       = { ERA_TRAP_CAVE,     MAP_STRATA_LINDQVIST_RANCH },
};

// The act whose end makes `beat` due (ERA_COUNT for SUBPLOT_NONE or out of range).
u32 Story_BeatAct(u32 beat)
{
    if (beat == SUBPLOT_NONE || beat >= SUBPLOT_COUNT)
        return ERA_COUNT;
    return sStoryBeats[beat].act;
}

// The map `beat` plays on (MAP_UNDEFINED for SUBPLOT_NONE or out of range).
u32 Story_BeatMap(u32 beat)
{
    if (beat == SUBPLOT_NONE || beat >= SUBPLOT_COUNT)
        return MAP_UNDEFINED;
    return sStoryBeats[beat].map;
}

// The beat that should play next at this story value, or SUBPLOT_NONE if the subplot has caught
// up with the acts done so far.
u32 Story_PendingBeat(u32 story, u32 subplot)
{
    u32 next = subplot + 1;

    if (next >= SUBPLOT_COUNT)
        return SUBPLOT_NONE;
    if (story < STORY_ACT_DONE(sStoryBeats[next].act))
        return SUBPLOT_NONE;
    return next;
}

// The subplot once every beat due at `story` has played.
u32 Story_ExpectedSubplot(u32 story)
{
    u32 subplot = SUBPLOT_NONE;

    while (Story_PendingBeat(story, subplot) != SUBPLOT_NONE)
        subplot++;
    return subplot;
}

// How many of Ortiz's three records the player has made at the pit.
u32 Story_EvidenceLogged(void)
{
    return FlagGet(FLAG_STRATA_STORY_EVIDENCE_PIT)
         + FlagGet(FLAG_STRATA_STORY_EVIDENCE_JACKET)
         + FlagGet(FLAG_STRATA_STORY_EVIDENCE_TRACKS);
}

// ---------------------------------------------------------------------------
// The field log: one line of "what next" for every state, shown beside the start menu.
// Two lines of at most STORY_LOG_WIDTH_PX in FONT_NORMAL (test/strata_story.c checks).
// ---------------------------------------------------------------------------

// What to do inside each act (VAR_STRATA_STORY = 2N): find its boss.
static const u8 *const sQuestInAct[ERA_COUNT] =
{
    [ERA_HELL_CREEK]    = COMPOUND_STRING("Hell Creek: survive the\ntyrant by the river."),
    [ERA_IMPACT_WINTER] = COMPOUND_STRING("Impact winter: get through\nthe ashen swamp alive."),
    [ERA_CORRAL_BLUFFS] = COMPOUND_STRING("Corral Bluffs: find the\nbig predator's carcass."),
    [ERA_BIGHORN_PETM]  = COMPOUND_STRING("Bighorn: cross the land\nbridge in the Red Beds."),
    [ERA_GREEN_RIVER]   = COMPOUND_STRING("Green River: walk the\nbeach of the Bridger Shore."),
    [ERA_WHITE_RIVER]   = COMPOUND_STRING("White River: climb to\nthe bone stash plateau."),
    [ERA_ASHFALL]       = COMPOUND_STRING("Ashfall: go east to the\nwaterhole."),
    [ERA_TRAP_CAVE]     = COMPOUND_STRING("Ice Age: find the way\ndown into the trap cave."),
    [ERA_EPILOGUE]      = COMPOUND_STRING("Today: the highway west\nof JORDAN is open."),
};

// Where the next beat waits (the beat is due but hasn't played).
static const u8 *const sQuestPendingBeat[SUBPLOT_COUNT] =
{
    [SUBPLOT_KESSLER_OFFER]     = COMPOUND_STRING("A visitor is at the\nFIELD STATION door."),
    [SUBPLOT_FERN_SPIKE]        = COMPOUND_STRING("Visit the LINDQVIST\nRANCH, west of camp."),
    [SUBPLOT_BLM_PERMIT]        = COMPOUND_STRING("See RANGER ORTIZ at the\nBLM office in JORDAN."),
    [SUBPLOT_JOSIE_PIT]         = COMPOUND_STRING("JOSIE is at the FIELD\nSTATION door, upset."),
    [SUBPLOT_HALVORSEN_REFUSAL] = COMPOUND_STRING("Visitors are at the\nFIELD STATION door."),
    [SUBPLOT_PIT_DOCUMENTED]    = COMPOUND_STRING("Meet RANGER ORTIZ at\nthe pit in SAND ARROYO."),
    [SUBPLOT_AUCTION_DATE]      = COMPOUND_STRING("Something is wrong at\nthe LINDQVIST RANCH."),
    [SUBPLOT_CITATION]          = COMPOUND_STRING("RANGER ORTIZ has news.\nGo to JORDAN."),
    [SUBPLOT_CONSORTIUM]        = COMPOUND_STRING("DR. HALVORSEN has a plan.\nGo to the FIELD STATION."),
    [SUBPLOT_AUCTION_DAY]       = COMPOUND_STRING("It's auction day at\nthe LINDQVIST RANCH."),
};

// Ortiz's evidence scene, by records logged.
static const u8 *const sQuestEvidence[STORY_EVIDENCE_COUNT + 1] =
{
    COMPOUND_STRING("Log the pit, the jacket\nand the tracks: 0 of 3."),
    COMPOUND_STRING("Log the pit, the jacket\nand the tracks: 1 of 3."),
    COMPOUND_STRING("Log the pit, the jacket\nand the tracks: 2 of 3."),
    COMPOUND_STRING("Report back to RANGER\nORTIZ at the pit."),
};

static const u8 sQuestNewGame[]   = _("Talk to DR. HALVORSEN\nin the FIELD STATION.");
static const u8 sQuestDig[]       = _("Find DALE at the dig in\nthe badlands, south.");
static const u8 sQuestFirstLoad[] = _("Use the rig: enter the\nHell Creek layer.");
static const u8 sQuestNextLayer[] = _("Load the next layer at\nthe FIELD STATION rig.");
static const u8 sQuestLastLayer[] = _("Load the last layer,\nToday, at the rig.");
static const u8 sQuestSeePit[]    = _("Look at the pit in SAND\nARROYO, past the dig.");

const u8 *Story_QuestLine(u32 story, u32 subplot)
{
    u32 beat = Story_PendingBeat(story, subplot);

    if (story == 0)
        return sQuestNewGame;
    if (beat == SUBPLOT_PIT_DOCUMENTED && FlagGet(FLAG_STRATA_STORY_EVIDENCE_STARTED))
        return sQuestEvidence[Story_EvidenceLogged()];
    if (beat != SUBPLOT_NONE)
        return sQuestPendingBeat[beat];
    if (story == 1)
        return FlagGet(FLAG_STRATA_DIG_DONE) ? sQuestFirstLoad : sQuestDig;
    if (subplot == SUBPLOT_JOSIE_PIT && !FlagGet(FLAG_STRATA_STORY_SAW_PIT))
        return sQuestSeePit;
    if (story >= STORY_IN_ACT(ERA_EPILOGUE))
        return sQuestInAct[ERA_EPILOGUE];
    if (story % 2 == 0)
        return sQuestInAct[story / 2];
    if (story == STORY_ACT_DONE(ERA_TRAP_CAVE))
        return sQuestLastLayer;
    return sQuestNextLayer;
}

// ---------------------------------------------------------------------------
// Specials
// ---------------------------------------------------------------------------

// special Strata_StoryPrepareMap (each hub map's on-transition script)
// Output: VAR_TEMP_2 = the beat due on this map (SUBPLOT_*), or 0; VAR_TEMP_3 = 1 if there is one;
//         VAR_TEMP_4 = the beat due anywhere, or 0 (so a map can send its cast to it).
void Strata_StoryPrepareMap(void)
{
    u32 story = VarGet(VAR_STRATA_STORY);
    u32 subplot = VarGet(VAR_STRATA_SUBPLOT);
    u32 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    u32 beat;

    // A save from before the subplot may already hold the permit: that beat has happened.
    if (subplot == SUBPLOT_FERN_SPIKE && FlagGet(FLAG_STRATA_BLM_PERMIT))
    {
        subplot = SUBPLOT_BLM_PERMIT;
        VarSet(VAR_STRATA_SUBPLOT, subplot);
    }
    beat = Story_PendingBeat(story, subplot);
    VarSet(VAR_TEMP_4, beat);
    if (Story_BeatMap(beat) != map)
        beat = SUBPLOT_NONE;
    VarSet(VAR_TEMP_2, beat);
    VarSet(VAR_TEMP_3, beat != SUBPLOT_NONE);
}

// special Strata_StoryBufferCaseCount
// Output: STR_VAR_1 = the research case for the consortium: the species in the player's Codex.
void Strata_StoryBufferCaseCount(void)
{
    ConvertIntToDecimalStringN(gStringVar1, GetNationalPokedexCount(FLAG_GET_CAUGHT), STR_CONV_MODE_LEFT_ALIGN, 3);
}

// ---------------------------------------------------------------------------
// The field log window in the start menu (src/start_menu.c calls these). Same corner and
// tiles as the Safari Zone's ball counter, which Strata never shows.
// ---------------------------------------------------------------------------

static EWRAM_DATA u8 sLogWindowId = 0;
static EWRAM_DATA bool8 sLogShown = FALSE;

static const struct WindowTemplate sLogWindowTemplate =
{
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = STORY_LOG_WIDTH_TILES,
    .height = STORY_LOG_HEIGHT_TILES,
    .paletteNum = 15,
    .baseBlock = 0x8,
};

void StrataLog_Show(void)
{
    const u8 *line;

    if (sLogShown)
        return;
    line = Story_QuestLine(VarGet(VAR_STRATA_STORY), VarGet(VAR_STRATA_SUBPLOT));
    HideMapNamePopUpWindow();
    sLogWindowId = AddWindow(&sLogWindowTemplate);
    PutWindowTilemap(sLogWindowId);
    DrawStdWindowFrame(sLogWindowId, FALSE);
    FillWindowPixelBuffer(sLogWindowId, PIXEL_FILL(1));
    AddTextPrinterParameterized(sLogWindowId, FONT_NORMAL, line, 0, 1, TEXT_SKIP_DRAW, NULL);
    CopyWindowToVram(sLogWindowId, COPYWIN_GFX);
    sLogShown = TRUE;
}

void StrataLog_Remove(void)
{
    if (!sLogShown)
        return;
    ClearStdWindowAndFrameToTransparent(sLogWindowId, FALSE);
    CopyWindowToVram(sLogWindowId, COPYWIN_GFX);
    RemoveWindow(sLogWindowId);
    sLogShown = FALSE;
}
