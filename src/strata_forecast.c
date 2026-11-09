#include "global.h"
#include "bg.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "lineage.h"
#include "list_menu.h"
#include "main.h"
#include "malloc.h"
#include "map_name_popup.h"
#include "menu.h"
#include "menu_helpers.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "pokemon_summary_screen.h"
#include "scanline_effect.h"
#include "script.h"
#include "selection.h"
#include "sound.h"
#include "sprite.h"
#include "strata_acts.h"
#include "strata_forecast.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/vars.h"

// The rig forecast (docs/strata_outline.md §3.4, F1) and the pressure chart (F2).
//
// The forecast is a dry run of Lineage_AdvanceToEra: for each era on the way, the
// lineage takes its descendant (Lineage_GetDescendant on its counters, which reset
// on a descent), then the era's extinction filter runs on the result
// (Lineage_IsExtinctInEra), then survivors are raised to the era's level floor.
// A lineage's outcome doesn't depend on whether it is in the TEAM or the PC; the
// one thing that does is the refill when every TEAM animal is lost (lineage.c
// EnsurePartyNotEmpty). test/strata_forecast.c checks all of it against the real
// load for many generated teams.

EWRAM_DATA struct RigForecast gStrataRigForecast = {0};

// ---------------------------------------------------------------------------
// The dry run
// ---------------------------------------------------------------------------

void Forecast_Lineage(u16 species, u32 level, const u8 *pressures, u32 fromEra, u32 targetEra, struct LineageForecast *out)
{
    u8 counters[PRESSURE_COUNT];
    u32 era;

    memcpy(counters, pressures, sizeof(counters));
    memset(out, 0, sizeof(*out));
    out->species = species;
    out->level = level;
    out->newLevel = level;
    out->fate = FATE_STASIS;
    out->lostEra = ERA_COUNT;
    out->decisionEra = ERA_COUNT;
    out->decisionSpecies = SPECIES_NONE;
    if (targetEra >= ERA_COUNT)
        targetEra = ERA_COUNT - 1;
    out->targetEra = targetEra;

    for (era = fromEra + 1; era <= targetEra; era++)
    {
        enum Species descendant;
        u32 floor;

        if (out->decisionSpecies == SPECIES_NONE && Lineage_GetDescentOptions(species, era) != NULL)
        {
            out->decisionSpecies = species;
            out->decisionEra = era;
            memcpy(out->pressures, counters, sizeof(counters));
        }
        descendant = Lineage_GetDescendant(species, era, counters);
        if (descendant != species)
        {
            species = descendant;
            memset(counters, 0, sizeof(counters)); // Selection_ResetBoxMonPressures
            out->descents++;
        }
        if (Lineage_IsExtinctInEra(species, era))
        {
            out->fate = FATE_LOST;
            out->lostEra = era;
            break;
        }
        floor = Lineage_GetEraLevelFloor(era);
        if (out->newLevel < floor)
            out->newLevel = floor;
    }
    out->result = species;
    if (out->fate != FATE_LOST && out->descents != 0)
        out->fate = FATE_DESCENDS;
    if (out->fate == FATE_LOST)
        out->newLevel = level;
}

// FALSE for an empty slot or an egg: neither descends, dies out or levels.
bool32 Forecast_BoxMon(struct BoxPokemon *boxMon, u32 targetEra, struct LineageForecast *out)
{
    u8 pressures[PRESSURE_COUNT];

    if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES) || GetBoxMonData(boxMon, MON_DATA_IS_EGG))
        return FALSE;
    Selection_GetBoxMonPressures(boxMon, pressures);
    Forecast_Lineage(GetBoxMonData(boxMon, MON_DATA_SPECIES), GetLevelFromBoxMonExp(boxMon), pressures,
                     VarGet(VAR_STRATA_ERA), targetEra, out);
    return TRUE;
}

// Every branch (non-default option) of `species` entering `era`, and where its
// counter stands. Returns how many were written (up to FORECAST_MAX_HINTS).
u32 Forecast_GetBranchHints(u16 species, u32 era, const u8 *pressures, struct BranchHint *hints)
{
    const struct DescentOption *option = Lineage_GetDescentOptions(species, era);
    const struct DescentOption *winner = NULL;
    enum Species winnerSpecies;
    u32 count = 0;

    if (option == NULL)
        return 0;
    winnerSpecies = Lineage_GetDescendant(species, era, pressures);
    for (; option->species != SPECIES_NONE; option++)
    {
        if (option->pressure < PRESSURE_COUNT && option->species == winnerSpecies && winner == NULL)
            winner = option;
    }

    for (option = Lineage_GetDescentOptions(species, era); option->species != SPECIES_NONE && count < FORECAST_MAX_HINTS; option++)
    {
        struct BranchHint *hint;
        if (option->pressure >= PRESSURE_COUNT)
            continue;
        hint = &hints[count++];
        hint->species = option->species;
        hint->pressure = option->pressure;
        hint->minScore = Lineage_GetOptionMinScore(option);
        hint->now = pressures[option->pressure];
        hint->beatenBy = 0;
        if (option == winner)
        {
            hint->state = HINT_TAKEN;
        }
        else if (hint->now < hint->minScore)
        {
            hint->state = HINT_BELOW_THRESHOLD;
        }
        else
        {
            hint->state = HINT_OUTSCORED;
            hint->beatenBy = winner != NULL ? pressures[winner->pressure] : 0;
        }
    }
    return count;
}

// Who joins the TEAM when a load would leave it empty: lineage.c's
// EnsurePartyNotEmpty, the gift's level (SURVIVOR_GIFT_LEVEL) included.
#define FORECAST_SURVIVOR_GIFT_LEVEL 10

static bool32 IsExtinctByEra(u16 species, u32 era)
{
    u32 i;
    for (i = 0; i <= era; i++)
    {
        if (Lineage_IsExtinctInEra(species, i))
            return TRUE;
    }
    return FALSE;
}

static bool32 SurvivesEra(const struct LineageForecast *f, u32 era)
{
    return f->fate != FATE_LOST || f->lostEra > era;
}

void Forecast_Rig(u32 targetEra, struct RigForecast *out)
{
    struct LineageForecast f;
    u32 i, boxId, boxPos, era, eggs = 0;
    s32 refillBox = -1;
    u16 eggSpecies[PARTY_SIZE];
    u8 eggLevel[PARTY_SIZE];

    memset(out, 0, sizeof(*out));
    out->fromEra = VarGet(VAR_STRATA_ERA);
    out->targetEra = targetEra;
    out->refillSpecies = SPECIES_NONE;
    out->pcFirstLost = SPECIES_NONE;
    if (targetEra >= ERA_COUNT)
        return;

    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct BoxPokemon *boxMon = &gParties[B_TRAINER_PLAYER][i].box;
        if (Forecast_BoxMon(boxMon, targetEra, &out->party[out->partyCount]))
        {
            out->partyCount++;
        }
        else if (GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES))
        {
            eggSpecies[eggs] = GetBoxMonData(boxMon, MON_DATA_SPECIES);
            eggLevel[eggs++] = GetLevelFromBoxMonExp(boxMon);
        }
    }

    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
        {
            if (!Forecast_BoxMon(GetBoxedMonPtr(boxId, boxPos), targetEra, &f))
                continue;
            out->pcTotal++;
            if (f.fate == FATE_LOST)
            {
                if (out->pcLost++ == 0)
                    out->pcFirstLost = f.species;
            }
            else if (f.fate == FATE_DESCENDS)
            {
                out->pcDescend++;
            }
            else
            {
                out->pcStasis++;
            }
        }
    }

    // The TEAM after the load, in party order: extinctions compact it.
    for (i = 0; i < eggs; i++)
    {
        out->expectedSpecies[out->expectedCount] = eggSpecies[i];
        out->expectedLevel[out->expectedCount++] = eggLevel[i];
    }
    // Eggs never die out, so a TEAM with one is never refilled. Party order with
    // eggs mixed in isn't modelled: Strata has no eggs.
    for (i = 0; i < out->partyCount; i++)
    {
        if (out->party[i].fate == FATE_LOST)
            continue;
        out->expectedSpecies[out->expectedCount] = out->party[i].result;
        out->expectedLevel[out->expectedCount++] = out->party[i].newLevel;
    }
    if (out->expectedCount != 0 || out->partyCount == 0)
        return;

    // Every TEAM animal is lost: in the era the last one dies out, the first
    // stored animal still alive then joins, or failing that a gift survivor.
    for (era = out->fromEra + 1; era <= targetEra; era++)
    {
        for (i = 0; i < out->partyCount; i++)
        {
            if (SurvivesEra(&out->party[i], era))
                break;
        }
        if (i == out->partyCount)
            break;
    }
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT && refillBox < 0; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
        {
            struct BoxPokemon *boxMon = GetBoxedMonPtr(boxId, boxPos);
            if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES))
                continue;
            if (!Forecast_BoxMon(boxMon, targetEra, &f))
            {
                // An egg: it joins as it is.
                out->refillSpecies = GetBoxMonData(boxMon, MON_DATA_SPECIES);
                out->refillLevel = GetLevelFromBoxMonExp(boxMon);
                refillBox = boxId * IN_BOX_COUNT + boxPos;
                break;
            }
            if (SurvivesEra(&f, era))
            {
                out->refillSpecies = f.result;
                out->refillLevel = f.newLevel;
                refillBox = boxId * IN_BOX_COUNT + boxPos;
                break;
            }
        }
    }
    if (refillBox >= 0)
    {
        out->refillFromPc = TRUE;
        out->refillSlot = refillBox;
    }
    else
    {
        u8 zero[PRESSURE_COUNT] = {0};
        u16 gift = IsExtinctByEra(SPECIES_MESODMA, era) ? SPECIES_LEPISOSTEUS : SPECIES_MESODMA;
        Forecast_Lineage(gift, max(FORECAST_SURVIVOR_GIFT_LEVEL, Lineage_GetEraLevelFloor(era)), zero, era, targetEra, &f);
        out->refillSpecies = f.result;
        out->refillLevel = f.newLevel;
        out->refillFromPc = FALSE;
    }
    out->expectedSpecies[0] = out->refillSpecies;
    out->expectedLevel[0] = out->refillLevel;
    out->expectedCount = 1;
}

// The next era after `era` that changes `species`: FATE_DESCENDS (it has descent
// options then), FATE_LOST (it dies out first), or FATE_STASIS (neither, ever).
u32 Forecast_GetNextChange(u16 species, u32 era, u32 *changeEra)
{
    u32 e;

    for (e = era + 1; e < ERA_COUNT; e++)
    {
        if (Lineage_GetDescentOptions(species, e) != NULL)
        {
            *changeEra = e;
            return FATE_DESCENDS;
        }
        if (Lineage_IsExtinctInEra(species, e))
        {
            *changeEra = e;
            return FATE_LOST;
        }
    }
    *changeEra = ERA_COUNT;
    return FATE_STASIS;
}

// ---------------------------------------------------------------------------
// Text
// ---------------------------------------------------------------------------

static const u8 *const sPressureLabels[PRESSURE_COUNT] =
{
    [PRESSURE_FOREST]     = COMPOUND_STRING("FOREST"),
    [PRESSURE_OPEN]       = COMPOUND_STRING("OPEN"),
    [PRESSURE_WATER]      = COMPOUND_STRING("WATER"),
    [PRESSURE_PLANT_DIET] = COMPOUND_STRING("PLANT"),
    [PRESSURE_MEAT_DIET]  = COMPOUND_STRING("MEAT"),
    [PRESSURE_HEAT]       = COMPOUND_STRING("HEAT"),
};

static const u8 *const sBranchNames[PRESSURE_COUNT] =
{
    [PRESSURE_FOREST]     = COMPOUND_STRING("Forest"),
    [PRESSURE_OPEN]       = COMPOUND_STRING("Open-country"),
    [PRESSURE_WATER]      = COMPOUND_STRING("Water"),
    [PRESSURE_PLANT_DIET] = COMPOUND_STRING("Plant-diet"),
    [PRESSURE_MEAT_DIET]  = COMPOUND_STRING("Meat-diet"),
    [PRESSURE_HEAT]       = COMPOUND_STRING("Heat"),
};

static const u8 sText_Arrow[] = _(" {RIGHT_ARROW} ");
static const u8 sText_Red[] = _("{COLOR RED}{SHADOW LIGHT_RED}");
static const u8 sText_Lv[] = _("{LV}");

static u8 *AppendNumber(u8 *dest, u32 value)
{
    return ConvertIntToDecimalStringN(dest, value, STR_CONV_MODE_LEFT_ALIGN, 3);
}

// FONT_NORMAL if `str` fits in `width` pixels, else the narrow font.
u32 Forecast_FitFont(const u8 *str, u32 width)
{
    return GetStringWidth(FONT_NORMAL, str, 0) <= (s32)width ? FONT_NORMAL : FONT_NARROW;
}

// "Epicyon if MEAT reaches 64 (now 41)." and friends.
static void FormatHint(u8 *dest, const struct BranchHint *hint)
{
    u8 *end = StringCopy(dest, GetSpeciesName(hint->species));
    switch (hint->state)
    {
    case HINT_TAKEN:
        end = StringAppend(end, COMPOUND_STRING(": "));
        end = StringAppend(end, sPressureLabels[hint->pressure]);
        end = StringAppend(end, COMPOUND_STRING(" "));
        end = AppendNumber(end, hint->now);
        end = StringAppend(end, COMPOUND_STRING("/"));
        end = AppendNumber(end, hint->minScore);
        end = StringAppend(end, COMPOUND_STRING(", on course."));
        break;
    case HINT_BELOW_THRESHOLD:
        end = StringAppend(end, COMPOUND_STRING(" if "));
        end = StringAppend(end, sPressureLabels[hint->pressure]);
        end = StringAppend(end, COMPOUND_STRING(" reaches "));
        end = AppendNumber(end, hint->minScore);
        end = StringAppend(end, COMPOUND_STRING(" (now "));
        end = AppendNumber(end, hint->now);
        end = StringAppend(end, COMPOUND_STRING(")."));
        break;
    case HINT_OUTSCORED:
        end = StringAppend(end, COMPOUND_STRING(": "));
        end = StringAppend(end, sPressureLabels[hint->pressure]);
        end = StringAppend(end, COMPOUND_STRING(" "));
        end = AppendNumber(end, hint->now);
        end = StringAppend(end, COMPOUND_STRING(", outscored ("));
        end = AppendNumber(end, hint->beatenBy);
        end = StringAppend(end, COMPOUND_STRING(")."));
        break;
    }
}

// The list row: `name` is the outcome ("Cimolestes → Protictis"), `level` the
// right-hand column (the level after the load).
void Forecast_FormatRow(const struct LineageForecast *f, u8 *name, u8 *level)
{
    u8 *end = StringCopy(name, GetSpeciesName(f->species));

    *level = EOS;
    switch (f->fate)
    {
    case FATE_DESCENDS:
        end = StringAppend(end, sText_Arrow);
        StringAppend(end, GetSpeciesName(f->result));
        break;
    case FATE_STASIS:
        StringAppend(end, COMPOUND_STRING(": no change"));
        break;
    case FATE_LOST:
        end = StringAppend(end, COMPOUND_STRING(": "));
        end = StringAppend(end, sText_Red);
        StringAppend(end, COMPOUND_STRING("will not survive"));
        return;
    }
    end = StringCopy(level, sText_Lv);
    AppendNumber(end, f->newLevel);
}

// Up to FORECAST_DETAIL_LINES lines on the selected TEAM animal: why it goes the
// way it does, the branches it could still reach, its level. Returns the count.
u32 Forecast_FormatDetail(const struct LineageForecast *f, u8 lines[][FORECAST_LINE_SIZE])
{
    struct BranchHint hints[FORECAST_MAX_HINTS];
    u32 i, n = 0, hintCount = 0;
    const struct BranchHint *taken = NULL;
    u8 *end;

    if (f->decisionSpecies != SPECIES_NONE)
        hintCount = Forecast_GetBranchHints(f->decisionSpecies, f->decisionEra, f->pressures, hints);
    for (i = 0; i < hintCount; i++)
    {
        if (hints[i].state == HINT_TAKEN)
            taken = &hints[i];
    }

    end = lines[n];
    switch (f->fate)
    {
    case FATE_STASIS:
        StringCopy(end, COMPOUND_STRING("No descent in this layer (stasis)."));
        break;
    case FATE_DESCENDS:
        if (f->descents > 1)
        {
            end = StringCopy(end, COMPOUND_STRING("Descends "));
            end = AppendNumber(end, f->descents);
            StringAppend(end, COMPOUND_STRING(" times on the way."));
        }
        else if (taken != NULL)
        {
            end = StringCopy(end, sBranchNames[taken->pressure]);
            end = StringAppend(end, COMPOUND_STRING(" branch: "));
            end = StringAppend(end, sPressureLabels[taken->pressure]);
            end = StringAppend(end, COMPOUND_STRING(" "));
            end = AppendNumber(end, taken->now);
            end = StringAppend(end, COMPOUND_STRING("/"));
            end = AppendNumber(end, taken->minScore);
            StringAppend(end, COMPOUND_STRING("."));
        }
        else if (hintCount != 0)
        {
            StringCopy(end, COMPOUND_STRING("Default descent: no branch reached."));
        }
        else
        {
            StringCopy(end, COMPOUND_STRING("Its one descendant in the record."));
        }
        break;
    case FATE_LOST:
        if (f->descents == 0)
        {
            end = StringCopy(end, sText_Red);
            StringAppend(end, COMPOUND_STRING("Extinct in the record: the lineage ends."));
        }
        else
        {
            end = StringCopy(end, COMPOUND_STRING("Becomes "));
            end = StringAppend(end, GetSpeciesName(f->result));
            end = StringAppend(end, COMPOUND_STRING(", which "));
            end = StringAppend(end, sText_Red);
            StringAppend(end, COMPOUND_STRING("dies out."));
        }
        break;
    }
    n++;

    for (i = 0; i < hintCount && n < FORECAST_DETAIL_LINES; i++)
    {
        if (&hints[i] != taken)
            FormatHint(lines[n++], &hints[i]);
    }

    if (n < FORECAST_DETAIL_LINES && f->fate != FATE_LOST && f->newLevel > f->level)
    {
        end = StringCopy(lines[n++], COMPOUND_STRING("Raised to the era floor: "));
        end = StringAppend(end, sText_Lv);
        end = AppendNumber(end, f->level);
        end = StringAppend(end, sText_Arrow);
        end = StringAppend(end, sText_Lv);
        end = AppendNumber(end, f->newLevel);
        StringAppend(end, COMPOUND_STRING("."));
    }

    if (n < FORECAST_DETAIL_LINES && f->fate == FATE_STASIS)
    {
        u32 era, change = Forecast_GetNextChange(f->result, f->targetEra, &era);
        if (change == FATE_DESCENDS)
        {
            end = StringCopy(lines[n++], COMPOUND_STRING("Next change: "));
            StringAppend(end, Strata_GetLayerName(era));
        }
        else if (change == FATE_LOST)
        {
            end = StringCopy(lines[n++], COMPOUND_STRING("Dies out by "));
            StringAppend(end, Strata_GetLayerName(era));
        }
    }
    return n;
}

void Forecast_FormatPcRow(const struct RigForecast *rig, u8 *name, u8 *lost)
{
    u8 *end;

    *lost = EOS;
    if (rig->pcTotal == 0)
    {
        StringCopy(name, COMPOUND_STRING("PC: empty"));
        return;
    }
    end = StringCopy(name, COMPOUND_STRING("PC: "));
    end = AppendNumber(end, rig->pcTotal);
    StringAppend(end, rig->pcTotal == 1 ? COMPOUND_STRING(" animal") : COMPOUND_STRING(" animals"));
    if (rig->pcLost != 0)
    {
        end = StringCopy(lost, sText_Red);
        end = AppendNumber(end, rig->pcLost);
        StringAppend(end, COMPOUND_STRING(" lost"));
    }
}

u32 Forecast_FormatPcDetail(const struct RigForecast *rig, u8 lines[][FORECAST_LINE_SIZE])
{
    u32 n = 0;
    u8 *end;

    if (rig->pcTotal == 0)
    {
        StringCopy(lines[n++], COMPOUND_STRING("No animals in the PC."));
    }
    else
    {
        end = AppendNumber(lines[n], rig->pcDescend);
        end = StringAppend(end, COMPOUND_STRING(" descend, "));
        end = AppendNumber(end, rig->pcStasis);
        end = StringAppend(end, COMPOUND_STRING(" no change, "));
        end = AppendNumber(end, rig->pcLost);
        StringAppend(end, COMPOUND_STRING(" lost."));
        n++;
        if (rig->pcLost != 0)
        {
            end = StringCopy(lines[n], COMPOUND_STRING("Lost: "));
            end = StringAppend(end, GetSpeciesName(rig->pcFirstLost));
            if (rig->pcLost > 1)
            {
                end = StringAppend(end, COMPOUND_STRING(" and "));
                end = AppendNumber(end, rig->pcLost - 1);
                StringAppend(end, COMPOUND_STRING(" more."));
            }
            else
            {
                StringAppend(end, COMPOUND_STRING("."));
            }
        }
        else
        {
            StringCopy(lines[n], COMPOUND_STRING("Every lineage in the PC survives."));
        }
        n++;
    }

    if (rig->refillSpecies != SPECIES_NONE)
    {
        end = StringCopy(lines[n++], COMPOUND_STRING("TEAM lost: "));
        if (!rig->refillFromPc)
            end = StringAppend(end, COMPOUND_STRING("a wild "));
        end = StringAppend(end, GetSpeciesName(rig->refillSpecies));
        StringAppend(end, rig->refillFromPc ? COMPOUND_STRING(" joins from the PC.") : COMPOUND_STRING(" joins."));
    }
    else if (n < FORECAST_DETAIL_LINES)
    {
        StringCopy(lines[n++], COMPOUND_STRING("PC animals gain no pressure."));
    }
    return n;
}

// ---------------------------------------------------------------------------
// F1: the forecast window, before the rig's YES/NO
// ---------------------------------------------------------------------------

#define FORECAST_ROWS      (1 + PARTY_SIZE + 1) // header, TEAM, PC
#define FORECAST_ID_PC     PARTY_SIZE
#define FORECAST_SHOWN     5
#define FORECAST_LEVEL_X   164 // level column, from the item's x
#define TAG_FORECAST_ARROWS 0x5F01

struct ForecastUi
{
    struct ListMenuItem items[FORECAST_ROWS];
    u8 rows[FORECAST_ROWS][FORECAST_LINE_SIZE];
    u8 detail[FORECAST_DETAIL_LINES][FORECAST_LINE_SIZE];
    u16 scrollOffset;
    u8 count;
    u8 listWindowId;
    u8 detailWindowId;
    u8 listTaskId;
    u8 arrowTaskId;
};

static EWRAM_DATA struct ForecastUi *sForecastUi = NULL;

static void Task_RigForecast(u8 taskId);

static void Task_ResumeScript(u8 taskId)
{
    DestroyTask(taskId);
    ScriptContext_Enable();
}

// The field message box (0x194-0x1FF) is closed while the forecast is up, so the
// windows may use every tile below the dialogue frame (DLG_WINDOW_BASE_TILE_NUM).
static const struct WindowTemplate sForecastListWindow = { .bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 10, .paletteNum = 15, .baseBlock = 0x001 };
static const struct WindowTemplate sForecastDetailWindow = { .bg = 0, .tilemapLeft = 1, .tilemapTop = 13, .width = 28, .height = 6, .paletteNum = 15, .baseBlock = 0x119 };
STATIC_ASSERT(0x119 >= 0x001 + 28 * 10 && 0x119 + 28 * 6 <= DLG_WINDOW_BASE_TILE_NUM, ForecastWindowsFitBelowTheDialogueFrame);

STATIC_ASSERT(FORECAST_NAME_WIDTH <= FORECAST_LEVEL_X - 4, ForecastNameColumnEndsBeforeTheLevel);
STATIC_ASSERT(8 + FORECAST_LEVEL_X + FORECAST_LEVEL_WIDTH <= 28 * 8, ForecastLevelColumnFitsTheWindow);

// A row: the outcome, then the level column; the narrow font if it's too wide.
static void BuildRow(u8 *dest, const u8 *name, const u8 *level)
{
    static const u8 sClearToLevel[] = { EXT_CTRL_CODE_BEGIN, EXT_CTRL_CODE_CLEAR_TO, FORECAST_LEVEL_X, EOS };
    static const u8 sNarrow[] = _("{FONT_NARROW}");
    u8 *end = dest;

    if (Forecast_FitFont(name, FORECAST_NAME_WIDTH) != FONT_NORMAL)
        end = StringCopy(end, sNarrow);
    end = StringCopy(end, name);
    end = StringAppend(end, sClearToLevel);
    StringAppend(end, level);
}

static void PrintForecastDetail(u32 id)
{
    u32 i, n;
    u8 windowId = sForecastUi->detailWindowId;

    if (id == FORECAST_ID_PC)
        n = Forecast_FormatPcDetail(&gStrataRigForecast, sForecastUi->detail);
    else
        n = Forecast_FormatDetail(&gStrataRigForecast.party[id], sForecastUi->detail);

    FillWindowPixelBuffer(windowId, PIXEL_FILL(1));
    for (i = 0; i < n; i++)
    {
        const u8 *line = sForecastUi->detail[i];
        AddTextPrinterParameterized(windowId, Forecast_FitFont(line, FORECAST_DETAIL_WIDTH), line, 0, 1 + i * 16, TEXT_SKIP_DRAW, NULL);
    }
    CopyWindowToVram(windowId, COPYWIN_GFX);
}

static void Forecast_MoveCursor(s32 id, bool8 onInit, struct ListMenu *list)
{
    if (!onInit)
        PlaySE(SE_SELECT);
    sForecastUi->scrollOffset = list->scrollOffset;
    if (id >= 0 && id <= FORECAST_ID_PC)
        PrintForecastDetail(id);
}

// special Strata_RigForecast (then waitstate): the scrolling forecast window
// for the load Strata_RigLoadNext would do. A or B closes it.
void Strata_RigForecast(void)
{
    struct ListMenuTemplate list;
    u8 name[FORECAST_LINE_SIZE], level[FORECAST_LINE_SIZE];
    u32 i;

    Forecast_Rig(Strata_GetRigTargetEra(), &gStrataRigForecast);
    if (gStrataRigForecast.targetEra >= ERA_COUNT)
    {
        // Nothing to forecast: let the script's waitstate run first, then go on.
        CreateTask(Task_ResumeScript, 80);
        return;
    }

    HideMapNamePopUpWindow();
    sForecastUi = AllocZeroed(sizeof(*sForecastUi));

    // Header
    {
        u8 *end = StringCopy(sForecastUi->rows[0], COMPOUND_STRING("{COLOR BLUE}{SHADOW LIGHT_BLUE}FORECAST: "));
        StringAppend(end, Strata_GetLayerName(gStrataRigForecast.targetEra));
        sForecastUi->items[0].name = sForecastUi->rows[0];
        sForecastUi->items[0].id = LIST_HEADER;
        sForecastUi->count = 1;
    }
    for (i = 0; i < gStrataRigForecast.partyCount; i++)
    {
        u32 row = sForecastUi->count++;
        Forecast_FormatRow(&gStrataRigForecast.party[i], name, level);
        BuildRow(sForecastUi->rows[row], name, level);
        sForecastUi->items[row].name = sForecastUi->rows[row];
        sForecastUi->items[row].id = i;
    }
    {
        u32 row = sForecastUi->count++;
        Forecast_FormatPcRow(&gStrataRigForecast, name, level);
        BuildRow(sForecastUi->rows[row], name, level);
        sForecastUi->items[row].name = sForecastUi->rows[row];
        sForecastUi->items[row].id = FORECAST_ID_PC;
    }

    sForecastUi->listWindowId = AddWindow(&sForecastListWindow);
    sForecastUi->detailWindowId = AddWindow(&sForecastDetailWindow);
    SetStandardWindowBorderStyle(sForecastUi->listWindowId, FALSE);
    SetStandardWindowBorderStyle(sForecastUi->detailWindowId, FALSE);
    FillWindowPixelBuffer(sForecastUi->listWindowId, PIXEL_FILL(1));

    memset(&list, 0, sizeof(list));
    list.items = sForecastUi->items;
    list.moveCursorFunc = Forecast_MoveCursor;
    list.totalItems = sForecastUi->count;
    list.maxShowed = min(sForecastUi->count, FORECAST_SHOWN);
    list.windowId = sForecastUi->listWindowId;
    list.header_X = 0;
    list.item_X = 8;
    list.cursor_X = 0;
    list.upText_Y = 1;
    list.cursorPal = 2;
    list.fillValue = 1;
    list.cursorShadowPal = 3;
    list.scrollMultiple = LIST_NO_MULTIPLE_SCROLL;
    list.fontId = FONT_NORMAL;
    list.cursorKind = CURSOR_BLACK_ARROW;
    sForecastUi->listTaskId = ListMenuInit(&list, 0, 1);

    sForecastUi->arrowTaskId = TASK_NONE;
    if (sForecastUi->count > FORECAST_SHOWN)
        sForecastUi->arrowTaskId = AddScrollIndicatorArrowPairParameterized(SCROLL_ARROW_UP, 120, 8, 90,
                                       sForecastUi->count - FORECAST_SHOWN, TAG_FORECAST_ARROWS, TAG_FORECAST_ARROWS,
                                       &sForecastUi->scrollOffset);
    CopyWindowToVram(sForecastUi->listWindowId, COPYWIN_FULL);
    ScheduleBgCopyTilemapToVram(0);
    CreateTask(Task_RigForecast, 80);
}

// Frames before the window takes input, so the A that closed the message
// before it can't skip the forecast too.
#define FORECAST_INPUT_DELAY 12

static void Task_RigForecast(u8 taskId)
{
    s32 input;

    if (gTasks[taskId].data[0] < FORECAST_INPUT_DELAY)
    {
        gTasks[taskId].data[0]++;
        return;
    }
    input = ListMenu_ProcessInput(sForecastUi->listTaskId);
    if (input == LIST_NOTHING_CHOSEN)
        return;
    PlaySE(SE_SELECT);
    if (sForecastUi->arrowTaskId != TASK_NONE)
        RemoveScrollIndicatorArrowPair(sForecastUi->arrowTaskId);
    DestroyListMenuTask(sForecastUi->listTaskId, NULL, NULL);
    ClearStdWindowAndFrameToTransparent(sForecastUi->listWindowId, FALSE);
    ClearStdWindowAndFrameToTransparent(sForecastUi->detailWindowId, TRUE);
    RemoveWindow(sForecastUi->listWindowId);
    RemoveWindow(sForecastUi->detailWindowId);
    FREE_AND_SET_NULL(sForecastUi);
    DestroyTask(taskId);
    ScriptContext_Enable();
}

// ---------------------------------------------------------------------------
// F2: the pressure chart, from the TEAM menu's LINEAGE option
// ---------------------------------------------------------------------------

// Indices 1-5 match the standard text palette (background, text, shadow, and
// TEXT_COLOR_RED / LIGHT_RED), so {COLOR RED} text works on the chart too.
enum
{
    CHART_COLOR_BG = 1,
    CHART_COLOR_TEXT,
    CHART_COLOR_SHADOW,
    CHART_COLOR_RED,
    CHART_COLOR_LIGHT_RED,
    CHART_COLOR_FOREST,
    CHART_COLOR_OPEN,
    CHART_COLOR_WATER,
    CHART_COLOR_PLANT,
    CHART_COLOR_ANIMAL,
    CHART_COLOR_HEAT,
    CHART_COLOR_TRACK,
    CHART_COLOR_MARKER,
    CHART_COLOR_BAND,
    CHART_COLOR_WHITE,
};
STATIC_ASSERT(CHART_COLOR_RED == TEXT_COLOR_RED && CHART_COLOR_LIGHT_RED == TEXT_COLOR_LIGHT_RED, ChartRedIsTheTextRed);
STATIC_ASSERT(CHART_COLOR_FOREST + PRESSURE_HEAT == CHART_COLOR_HEAT, ChartBarColorsFollowThePressures);

static const u16 sChartPalette[16] =
{
    RGB(0, 0, 0),
    [CHART_COLOR_BG]        = RGB(29, 28, 24),
    [CHART_COLOR_TEXT]      = RGB(7, 7, 7),
    [CHART_COLOR_SHADOW]    = RGB(21, 20, 17),
    [CHART_COLOR_RED]       = RGB(25, 4, 4),
    [CHART_COLOR_LIGHT_RED] = RGB(30, 20, 18),
    [CHART_COLOR_FOREST]    = RGB(5, 17, 8),
    [CHART_COLOR_OPEN]      = RGB(25, 20, 7),
    [CHART_COLOR_WATER]     = RGB(6, 13, 26),
    [CHART_COLOR_PLANT]     = RGB(14, 23, 5),
    [CHART_COLOR_ANIMAL]    = RGB(23, 8, 6),
    [CHART_COLOR_HEAT]      = RGB(29, 14, 3),
    [CHART_COLOR_TRACK]     = RGB(24, 23, 19),
    [CHART_COLOR_MARKER]    = RGB(3, 3, 3),
    [CHART_COLOR_BAND]      = RGB(8, 12, 14),
    [CHART_COLOR_WHITE]     = RGB(31, 31, 31),
};

static const u8 sChartTextColors[] = { CHART_COLOR_BG, CHART_COLOR_TEXT, CHART_COLOR_SHADOW };
static const u8 sChartBandColors[] = { CHART_COLOR_BAND, CHART_COLOR_WHITE, CHART_COLOR_TEXT };

#define CHART_BAND_HEIGHT 18
#define CHART_BAR_TOP     22
#define CHART_ROW_HEIGHT  13
#define CHART_BAR_X       54
#define CHART_BAR_WIDTH   128 // 0-255, two points a pixel
#define CHART_VALUE_X     188
#define CHART_HINT_TOP    (CHART_BAR_TOP + PRESSURE_COUNT * CHART_ROW_HEIGHT + 2)
#define CHART_HINT_HEIGHT 14
#define CHART_HINT_LINES  4

struct PressureChart
{
    void (*exitCallback)(void);
    u8 slot;
    u8 tilemap[BG_SCREEN_SIZE] ALIGNED(4);
};

static EWRAM_DATA struct PressureChart *sChart = NULL;

static const struct BgTemplate sChartBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0 },
};

static const struct WindowTemplate sChartWindowTemplates[] =
{
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = DISPLAY_TILE_WIDTH, .height = DISPLAY_TILE_HEIGHT, .paletteNum = 15, .baseBlock = 1 },
    DUMMY_WIN_TEMPLATE,
};

static void CB2_InitPressureChart(void);
static void Task_PressureChart(u8 taskId);
static void Task_PressureChartExit(u8 taskId);

void ShowStrataPressureChart(u8 slot, void (*exitCallback)(void))
{
    sChart = AllocZeroed(sizeof(*sChart));
    if (sChart == NULL)
    {
        SetMainCallback2(exitCallback);
        return;
    }
    sChart->exitCallback = exitCallback;
    sChart->slot = slot;
    gMain.state = 0;
    SetMainCallback2(CB2_InitPressureChart);
}

static void CB2_PressureChart(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void VBlankCB_PressureChart(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void ChartPrint(const u8 *str, u32 x, u32 y, const u8 *colors, u32 width)
{
    AddTextPrinterParameterized3(0, Forecast_FitFont(str, width), x, y, colors, TEXT_SKIP_DRAW, str);
}

static void DrawChartHint(u32 line, const u8 *str)
{
    if (line < CHART_HINT_LINES)
        ChartPrint(str, 6, CHART_HINT_TOP + line * CHART_HINT_HEIGHT, sChartTextColors, DISPLAY_WIDTH - 12);
}

static void DrawPressureChart(void)
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][sChart->slot];
    struct BranchHint hints[FORECAST_MAX_HINTS];
    u8 pressures[PRESSURE_COUNT];
    u8 buffer[FORECAST_LINE_SIZE];
    u8 *end;
    u16 species = GetMonData(mon, MON_DATA_SPECIES);
    u32 i, j, era, line = 0, hintCount = 0, change;
    u32 partyCount = CalculatePlayerPartyCount();

    Selection_GetBoxMonPressures(&mon->box, pressures);
    change = Forecast_GetNextChange(species, VarGet(VAR_STRATA_ERA), &era);
    if (change == FATE_DESCENDS)
        hintCount = Forecast_GetBranchHints(species, era, pressures, hints);

    FillWindowPixelBuffer(0, PIXEL_FILL(CHART_COLOR_BG));

    // Title band: the lineage, its level, which TEAM slot.
    FillWindowPixelRect(0, PIXEL_FILL(CHART_COLOR_BAND), 0, 0, DISPLAY_WIDTH, CHART_BAND_HEIGHT);
    end = StringCopy(buffer, COMPOUND_STRING("LINEAGE  "));
    StringAppend(end, GetSpeciesName(species));
    ChartPrint(buffer, 6, 1, sChartBandColors, 150);
    end = StringCopy(buffer, sText_Lv);
    AppendNumber(end, GetMonData(mon, MON_DATA_LEVEL));
    ChartPrint(buffer, 166, 1, sChartBandColors, 40);
    end = AppendNumber(buffer, sChart->slot + 1);
    end = StringAppend(end, COMPOUND_STRING("/"));
    AppendNumber(end, partyCount);
    ChartPrint(buffer, 208, 1, sChartBandColors, 30);

    // One bar per pressure, with a marker at each branch threshold it feeds.
    for (i = 0; i < PRESSURE_COUNT; i++)
    {
        u32 y = CHART_BAR_TOP + i * CHART_ROW_HEIGHT;
        u32 threshold = 0;

        ChartPrint(sPressureLabels[i], 6, y - 2, sChartTextColors, CHART_BAR_X - 8);
        FillWindowPixelRect(0, PIXEL_FILL(CHART_COLOR_TRACK), CHART_BAR_X, y + 2, CHART_BAR_WIDTH, 8);
        if (pressures[i] != 0)
            FillWindowPixelRect(0, PIXEL_FILL(CHART_COLOR_FOREST + i), CHART_BAR_X, y + 2, max(1, pressures[i] / 2), 8);
        for (j = 0; j < hintCount; j++)
        {
            if (hints[j].pressure != i)
                continue;
            threshold = hints[j].minScore;
            FillWindowPixelRect(0, PIXEL_FILL(CHART_COLOR_MARKER), CHART_BAR_X + threshold / 2 - 1, y, 2, 12);
        }
        end = AppendNumber(buffer, pressures[i]);
        if (threshold != 0)
        {
            end = StringAppend(end, COMPOUND_STRING("/"));
            AppendNumber(end, threshold);
        }
        ChartPrint(buffer, CHART_VALUE_X, y - 2, sChartTextColors, DISPLAY_WIDTH - CHART_VALUE_X - 2);
    }

    // What the counters steer: the next layer that changes this lineage.
    switch (change)
    {
    case FATE_STASIS:
        DrawChartHint(line++, COMPOUND_STRING("No change ahead in the record."));
        DrawChartHint(line++, COMPOUND_STRING("This lineage lives on as it is."));
        break;
    case FATE_LOST:
        end = StringCopy(buffer, COMPOUND_STRING("{COLOR RED}{SHADOW LIGHT_RED}Dies out by "));
        StringAppend(end, Strata_GetLayerName(era));
        DrawChartHint(line++, buffer);
        DrawChartHint(line++, COMPOUND_STRING("No descendant in the record survives."));
        break;
    case FATE_DESCENDS:
    {
        const struct DescentOption *option = Lineage_GetDescentOptions(species, era);
        bool32 onDefault = TRUE, hasDefault = FALSE;

        for (j = 0; j < hintCount; j++)
        {
            if (hints[j].state == HINT_TAKEN)
                onDefault = FALSE;
        }
        end = StringCopy(buffer, COMPOUND_STRING("Next change: "));
        StringAppend(end, Strata_GetLayerName(era));
        DrawChartHint(line++, buffer);
        for (; option->species != SPECIES_NONE; option++)
        {
            if (option->pressure < PRESSURE_COUNT)
                continue;
            end = StringCopy(buffer, GetSpeciesName(option->species));
            StringAppend(end, onDefault ? COMPOUND_STRING(" by default, on course.") : COMPOUND_STRING(" by default."));
            DrawChartHint(line++, buffer);
            hasDefault = TRUE;
            break;
        }
        // Only a branch here (Protochelyd entering Ashfall): below it, the lineage stays as it is.
        if (!hasDefault)
            DrawChartHint(line++, onDefault ? COMPOUND_STRING("Stays as it is by default, on course.") : COMPOUND_STRING("Stays as it is by default."));
        for (j = 0; j < hintCount; j++)
        {
            FormatHint(buffer, &hints[j]);
            DrawChartHint(line++, buffer);
        }
        break;
    }
    }
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void CB2_InitPressureChart(void)
{
    switch (gMain.state)
    {
    case 0:
        SetVBlankHBlankCallbacksToNull();
        ClearScheduledBgCopiesToVram();
        ScanlineEffect_Stop();
        ResetVramOamAndBgCntRegs();
        ResetAllBgsCoordinates();
        ResetPaletteFade();
        ResetSpriteData();
        FreeAllSpritePalettes();
        ResetTasks();
        gMain.state++;
        break;
    case 1:
        ResetBgsAndClearDma3BusyFlags(0);
        InitBgsFromTemplates(0, sChartBgTemplates, ARRAY_COUNT(sChartBgTemplates));
        SetBgTilemapBuffer(0, sChart->tilemap);
        InitWindows(sChartWindowTemplates);
        DeactivateAllTextPrinters();
        LoadPalette(sChartPalette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
        LoadPalette(&sChartPalette[CHART_COLOR_BG], BG_PLTT_ID(0), PLTT_SIZEOF(1));
        gMain.state++;
        break;
    case 2:
        DrawPressureChart();
        ScheduleBgCopyTilemapToVram(0);
        gMain.state++;
        break;
    case 3:
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP);
        ShowBg(0);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB_PressureChart);
        CreateTask(Task_PressureChart, 0);
        SetMainCallback2(CB2_PressureChart);
        break;
    }
}

// The next TEAM slot from `slot` in direction `delta` that holds an animal (not an egg).
static u32 GetNextChartSlot(u32 slot, s32 delta)
{
    u32 i;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct Pokemon *mon;
        slot = (slot + PARTY_SIZE + delta) % PARTY_SIZE;
        mon = &gParties[B_TRAINER_PLAYER][slot];
        if (GetMonData(mon, MON_DATA_SANITY_HAS_SPECIES) && !GetMonData(mon, MON_DATA_IS_EGG))
            return slot;
    }
    return slot;
}

static void Task_PressureChart(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    if (JOY_NEW(A_BUTTON | B_BUTTON))
    {
        PlaySE(SE_SELECT);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        gTasks[taskId].func = Task_PressureChartExit;
    }
    else if (JOY_REPEAT(DPAD_UP | DPAD_DOWN))
    {
        u32 slot = GetNextChartSlot(sChart->slot, JOY_REPEAT(DPAD_UP) ? -1 : 1);
        if (slot != sChart->slot)
        {
            PlaySE(SE_SELECT);
            sChart->slot = slot;
            DrawPressureChart();
        }
    }
}

static void Task_PressureChartExit(u8 taskId)
{
    void (*exitCallback)(void);

    if (gPaletteFade.active)
        return;
    gLastViewedMonIndex = sChart->slot;
    exitCallback = sChart->exitCallback;
    FreeAllWindowBuffers();
    FREE_AND_SET_NULL(sChart);
    DestroyTask(taskId);
    SetMainCallback2(exitCallback);
}
