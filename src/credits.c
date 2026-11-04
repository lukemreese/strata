#include "global.h"
#include "bg.h"
#include "credits.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "international_string_util.h"
#include "m4a.h"
#include "main.h"
#include "malloc.h"
#include "palette.h"
#include "sound.h"
#include "sprite.h"
#include "strata_ending.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#if !IS_FRLG

// Strata's credits (roadmap S3): the roll climbs the stratigraphic column. The camera rises from
// below Hell Creek to the present, so the picture moves down and each new layer comes in at the
// top, above the one before it, as in the rock. One coloured band per layer (name and age), and
// under it the lineages the player carried and lost there, from the fossil flags; under today,
// the TEAM and PC lineages and what they descended to (src/strata_ending.c). Then the credits
// proper, THE END, and a soft reset to the title screen, as the stock credits do. The stock bike
// scene and its art are gone; nothing here names the stock games.
//
// Drawing: two 256x256 text BGs that scroll together, BG1 the band colours (one solid tile per
// palette role) and BG0 a 30x32-tile window with the text. The roll is a list of 16 px rows,
// drawn into the wrapping tilemap one row ahead of the top of the screen.

EWRAM_DATA bool8 gHasHallOfFameRecords = 0;

#define ROW_HEIGHT     16
#define TILE_ROWS      32          // the tilemaps wrap every 256 px
#define ROLL_MAX_ROWS  (ENDING_FATES_MAX + 96)
#define NO_BAND        0xFF
#define WIN_ROLL       0

// BG palettes: 0 the black backdrop, 1 + band for each band, 15 the text.
#define PAL_BAND_FIRST 1
#define PAL_TEXT       15

// BG1 tiles, one per palette role of a band palette.
enum {
    TILE_NONE,      // transparent: the black backdrop
    TILE_BODY,      // colour 1: the layer
    TILE_HEADER,    // colour 2: its header strip
    TILE_CONTACT,   // the header's top row: colour 3, the contact with the layer above
};

// Text colours (palette 15).
enum {
    TEXTCOL_DARK = 1,
    TEXTCOL_WHITE,
    TEXTCOL_SHADOW,
    TEXTCOL_GOLD,
};

enum {
    ROW_EMPTY,
    ROW_HEADER,   // a band's name and age
    ROW_FATE,     // a lineage and its fate
    ROW_TEXT,     // a centred line
    ROW_TITLE,    // a centred line, gold
};

struct RollRow
{
    u8 type;
    u8 band;      // index into the ending bands, or NO_BAND (black)
    u16 fate;     // ROW_FATE: index into the fate list
    const u8 *text;
};

struct CreditsRoll
{
    struct RollRow rows[ROLL_MAX_ROWS];  // top of the column first
    struct EndingFate fates[ENDING_FATES_MAX];
    u8 playerLine[48];
    u8 moreLine[48];
    u16 rowCount;
    u16 nextRow;      // next row to draw, counted from the bottom (the order they appear)
    s32 camera;       // world y of the top of the screen; rows sit above 0, so it goes negative
    u16 subPixel;
    u16 holdTimer;
};

static EWRAM_DATA struct CreditsRoll *sRoll = NULL;
// Read by the playtest harness (tools/strata/playtest/scenarios.py, ending_smoke).
EWRAM_DATA u16 gStrataCreditsState = 0;

#define CREDITS_STATE_ROLL     1
#define CREDITS_STATE_THE_END  2

static const struct BgTemplate sBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0 },
    { .bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .screenSize = 0, .paletteMode = 0, .priority = 1, .baseTile = 0 },
};

static const struct WindowTemplate sWindowTemplates[] =
{
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = TILE_ROWS, .paletteNum = PAL_TEXT, .baseBlock = 1 },
    DUMMY_WIN_TEMPLATE,
};

#define SOLID_ROW(c) (0x11111111u * (c))
static const u32 sBandTiles[][8] =
{
    [TILE_NONE]    = { 0 },
    [TILE_BODY]    = { SOLID_ROW(1), SOLID_ROW(1), SOLID_ROW(1), SOLID_ROW(1), SOLID_ROW(1), SOLID_ROW(1), SOLID_ROW(1), SOLID_ROW(1) },
    [TILE_HEADER]  = { SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2) },
    [TILE_CONTACT] = { SOLID_ROW(3), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2), SOLID_ROW(2) },
};

static const u16 sTextPalette[] =
{
    RGB_BLACK, RGB(4, 3, 2), RGB_WHITE, RGB(5, 5, 6), RGB(31, 26, 12),
};

static const u8 sColors_Body[]   = { TEXT_COLOR_TRANSPARENT, TEXTCOL_DARK, TEXT_COLOR_TRANSPARENT };
static const u8 sColors_Header[] = { TEXT_COLOR_TRANSPARENT, TEXTCOL_WHITE, TEXTCOL_SHADOW };
static const u8 sColors_Plain[]  = { TEXT_COLOR_TRANSPARENT, TEXTCOL_WHITE, TEXTCOL_SHADOW };
static const u8 sColors_Title[]  = { TEXT_COLOR_TRANSPARENT, TEXTCOL_GOLD, TEXTCOL_SHADOW };


static void VBlankCB_Credits(void);
static void CB2_Credits(void);
static void Task_Roll(u8 taskId);
static void Task_RollHold(u8 taskId);
static void Task_RollFadeOut(u8 taskId);
static void Task_TheEnd(u8 taskId);
static void Task_TheEndWait(u8 taskId);
static void Task_SoftReset(u8 taskId);

static void ResetGpuAndVram(void)
{
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    SetGpuReg(REG_OFFSET_BG2HOFS, 0);
    SetGpuReg(REG_OFFSET_BG2VOFS, 0);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
    DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
    DmaFill16(3, 0, (void *)(PLTT + 2), PLTT_SIZE - 2);
}

static void VBlankCB_Credits(void)
{
    u16 offset = sRoll != NULL ? (u16)(sRoll->camera & 0xFF) : 0;
    SetGpuReg(REG_OFFSET_BG0VOFS, offset);
    SetGpuReg(REG_OFFSET_BG1VOFS, offset);
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_Credits(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

// ---- building the column ------------------------------------------------------------------

static void AddRow(u8 type, u8 band, u16 fate, const u8 *text)
{
    struct RollRow *row;
    if (sRoll->rowCount >= ROLL_MAX_ROWS)
        return;
    row = &sRoll->rows[sRoll->rowCount++];
    row->type = type;
    row->band = band;
    row->fate = fate;
    row->text = text;
}

// The fate rows of one band; a band with none says so.
static void AddBandFates(u32 bandIndex, u32 fateCount)
{
    const struct EndingBand *band = Ending_GetBand(bandIndex);
    u32 i, n = 0;

    for (i = 0; i < fateCount; i++)
    {
        if (sRoll->fates[i].layer == band->era)
        {
            AddRow(ROW_FATE, bandIndex, i, NULL);
            n++;
        }
    }
    if (n == 0 && band->era != ERA_EPILOGUE)
        AddRow(ROW_TEXT, bandIndex, 0, gText_EndingNoLoss);
}

static void BuildRoll(void)
{
    u32 i, overflow, fateCount;
    s32 b;

    fateCount = Ending_BuildFates(sRoll->fates, ENDING_FATES_MAX, &overflow);
    sRoll->rowCount = 0;

    // Top: the credits proper, then three empty rows of sky.
    for (i = 0; i < gEndingCreditsLineCount; i++)
    {
        const struct EndingCreditsLine *line = &gEndingCreditsLines[i];
        if (line->text == NULL)
            AddRow(ROW_EMPTY, NO_BAND, 0, NULL);
        else
            AddRow(line->isTitle ? ROW_TITLE : ROW_TEXT, NO_BAND, 0, line->text);
    }
    for (i = 0; i < 3; i++)
        AddRow(ROW_EMPTY, NO_BAND, 0, NULL);

    // The column, youngest at the top.
    for (b = Ending_GetBandCount() - 1; b >= 0; b--)
    {
        const struct EndingBand *band = Ending_GetBand(b);

        AddRow(ROW_HEADER, b, 0, NULL);
        if (band->isColby)
        {
            // The rig can't render the people (rule R-g): only what they left.
            AddRow(ROW_TEXT, b, 0, gText_EndingColbyFind);
            AddRow(ROW_TEXT, b, 0, gText_EndingColbyTrace);
        }
        else
        {
            if (band->era == ERA_EPILOGUE && Ending_PairOnDisplay())
                AddRow(ROW_TEXT, b, 0, gText_EndingPair);
            AddBandFates(b, fateCount);
            if (band->era == ERA_EPILOGUE && overflow != 0)
            {
                Ending_FormatOverflow(sRoll->moreLine, overflow);
                AddRow(ROW_TEXT, b, 0, sRoll->moreLine);
            }
        }
        AddRow(ROW_EMPTY, b, 0, NULL);
    }

    // Bottom: the first thing the roll shows.
    StringExpandPlaceholders(sRoll->playerLine, gText_EndingPlayerColumn);
    AddRow(ROW_EMPTY, NO_BAND, 0, NULL);
    AddRow(ROW_TITLE, NO_BAND, 0, sRoll->playerLine);
    AddRow(ROW_TEXT, NO_BAND, 0, gText_EndingPrelude1);
    AddRow(ROW_TEXT, NO_BAND, 0, gText_EndingPrelude2);
    AddRow(ROW_EMPTY, NO_BAND, 0, NULL);
}

// ---- drawing --------------------------------------------------------------------------------

static void PrintCentred(u32 y, const u8 *text, const u8 *colors)
{
    u32 font = Ending_FitFont(text, ENDING_ROLL_WIDTH - 2 * ENDING_LEFT_X);
    AddTextPrinterParameterized3(WIN_ROLL, font, GetStringCenterAlignXOffset(font, text, ENDING_ROLL_WIDTH), y,
                                 colors, TEXT_SKIP_DRAW, text);
}

static void PrintAt(u32 x, u32 y, u32 width, const u8 *text, const u8 *colors)
{
    AddTextPrinterParameterized3(WIN_ROLL, Ending_FitFont(text, width), x, y, colors, TEXT_SKIP_DRAW, text);
}

static void PrintRightAligned(u32 rightEnd, u32 y, u32 width, const u8 *text, const u8 *colors)
{
    u32 font = Ending_FitFont(text, width);
    s32 x = rightEnd - GetStringWidth(font, text, 0);
    AddTextPrinterParameterized3(WIN_ROLL, font, max(x, 0), y, colors, TEXT_SKIP_DRAW, text);
}

// The tilemap row (0..30, even) of the row `fromBottom` rows above the bottom of the column.
static u32 TileRowOf(u32 fromBottom)
{
    // Its top edge is at world y -(fromBottom + 1) * 16.
    return ((u32)(-(s32)((fromBottom + 1) * ROW_HEIGHT)) & 0xFF) / 8;
}

static void DrawRow(u32 fromBottom)
{
    const struct RollRow *row = &sRoll->rows[sRoll->rowCount - 1 - fromBottom];
    u32 tileRow = TileRowOf(fromBottom);
    u32 y = tileRow * 8;
    u32 palette = row->band == NO_BAND ? 0 : PAL_BAND_FIRST + row->band;
    const u8 *colors = row->band == NO_BAND ? sColors_Plain : sColors_Body;

    // Colour.
    if (row->band == NO_BAND)
    {
        FillBgTilemapBufferRect(1, TILE_NONE, 0, tileRow, 32, 2, 0);
    }
    else if (row->type == ROW_HEADER)
    {
        FillBgTilemapBufferRect(1, TILE_CONTACT, 0, tileRow, 32, 1, palette);
        FillBgTilemapBufferRect(1, TILE_HEADER, 0, tileRow + 1, 32, 1, palette);
    }
    else
    {
        FillBgTilemapBufferRect(1, TILE_BODY, 0, tileRow, 32, 2, palette);
    }
    CopyBgTilemapBufferToVram(1);

    // Text.
    FillWindowPixelRect(WIN_ROLL, PIXEL_FILL(0), 0, y, ENDING_ROLL_WIDTH, ROW_HEIGHT);
    switch (row->type)
    {
    case ROW_HEADER:
    {
        const struct EndingBand *band = Ending_GetBand(row->band);
        PrintAt(ENDING_LEFT_X, y, ENDING_RIGHT_END - ENDING_LEFT_X, band->name, sColors_Header);
        PrintRightAligned(ENDING_RIGHT_END, y, ENDING_RIGHT_END - ENDING_RIGHT_X, band->age, sColors_Header);
        break;
    }
    case ROW_FATE:
    {
        u8 left[POKEMON_NAME_LENGTH + 8], right[64];
        Ending_FormatFate(&sRoll->fates[row->fate], left, right);
        PrintAt(ENDING_LEFT_X, y, ENDING_RIGHT_X - ENDING_LEFT_X - 4, left, colors);
        PrintAt(ENDING_RIGHT_X, y, ENDING_RIGHT_END - ENDING_RIGHT_X, right, colors);
        break;
    }
    case ROW_TEXT:
        PrintCentred(y, row->text, colors);
        break;
    case ROW_TITLE:
        PrintCentred(y, row->text, sColors_Title);
        break;
    }
    CopyWindowRectToVram(WIN_ROLL, COPYWIN_GFX, 0, tileRow, 30, 2);
}

static void LoadBandPalettes(void)
{
    u32 i;
    for (i = 0; i < Ending_GetBandCount(); i++)
    {
        const struct EndingBand *band = Ending_GetBand(i);
        u16 colors[4];
        u16 h = band->header;
        colors[0] = RGB_BLACK;
        colors[1] = band->body;
        colors[2] = h;
        // The contact line: the header, half as bright.
        colors[3] = RGB(GET_R(h) / 2, GET_G(h) / 2, GET_B(h) / 2);
        LoadPalette(colors, BG_PLTT_ID(PAL_BAND_FIRST + i), sizeof(colors));
    }
}

// ---- the sequence ---------------------------------------------------------------------------

void CB2_StartCreditsSequence(void)
{
    u16 black = RGB_BLACK;

    SetVBlankCallback(NULL);
    ResetGpuAndVram();
    InitHeap(gHeap, HEAP_SIZE);
    ResetPaletteFade();
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    sRoll = AllocZeroed(sizeof(struct CreditsRoll));
    BuildRoll();

    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    SetBgTilemapBuffer(0, AllocZeroed(BG_SCREEN_SIZE));
    SetBgTilemapBuffer(1, AllocZeroed(BG_SCREEN_SIZE));
    LoadBgTiles(1, sBandTiles, sizeof(sBandTiles), 0);
    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();
    LoadPalette(&black, BG_PLTT_ID(0), PLTT_SIZEOF(1));
    LoadBandPalettes();
    LoadPalette(sTextPalette, BG_PLTT_ID(PAL_TEXT), sizeof(sTextPalette));
    FillWindowPixelBuffer(WIN_ROLL, PIXEL_FILL(0));
    PutWindowTilemap(WIN_ROLL);
    CopyWindowToVram(WIN_ROLL, COPYWIN_FULL);
    CopyBgTilemapBufferToVram(1);
    ShowBg(0);
    ShowBg(1);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_BG0_ON | DISPCNT_BG1_ON);

    sRoll->camera = 0;
    sRoll->nextRow = 0;
    gStrataCreditsState = CREDITS_STATE_ROLL;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    EnableInterrupts(INTR_FLAG_VBLANK);
    SetVBlankCallback(VBlankCB_Credits);
    m4aSongNumStart(MUS_CREDITS);
    SetMainCallback2(CB2_Credits);
    CreateTask(Task_Roll, 0);
}

// Pixels a frame, in 1/4 px: half a pixel a frame, a pixel and a half with A or B held.
#define ROLL_SPEED       2
#define ROLL_SPEED_FAST  6

static void Task_Roll(u8 taskId)
{
    s32 top = -(s32)(sRoll->rowCount * ROW_HEIGHT);

    // Draw the rows that are about to come in at the top.
    while (sRoll->nextRow < sRoll->rowCount && sRoll->camera <= -(s32)(sRoll->nextRow * ROW_HEIGHT) + ROW_HEIGHT)
        DrawRow(sRoll->nextRow++);

    if (gPaletteFade.active)
        return;
    if (sRoll->camera <= top)
    {
        sRoll->holdTimer = 240;
        gTasks[taskId].func = Task_RollHold;
        return;
    }
    sRoll->subPixel += (JOY_HELD(A_BUTTON | B_BUTTON)) ? ROLL_SPEED_FAST : ROLL_SPEED;
    while (sRoll->subPixel >= 4 && sRoll->camera > top)
    {
        sRoll->subPixel -= 4;
        sRoll->camera--;
    }
}

// The credits stay on screen a moment, then the roll fades out.
static void Task_RollHold(u8 taskId)
{
    if (sRoll->holdTimer != 0)
    {
        sRoll->holdTimer--;
        return;
    }
    FadeOutBGM(4);
    BeginNormalPaletteFade(PALETTES_ALL, 4, 0, 16, RGB_BLACK);
    gTasks[taskId].func = Task_RollFadeOut;
}

static void Task_RollFadeOut(u8 taskId)
{
    if (!gPaletteFade.active)
        gTasks[taskId].func = Task_TheEnd;
}

#define tDelay data[0]

static void Task_TheEnd(u8 taskId)
{
    sRoll->camera = 0;
    FillBgTilemapBufferRect(1, TILE_NONE, 0, 0, 32, 32, 0);
    CopyBgTilemapBufferToVram(1);
    FillWindowPixelBuffer(WIN_ROLL, PIXEL_FILL(0));
    PrintCentred(64, gText_EndingTheEnd, sColors_Title);
    PrintCentred(84, gText_EndingTheEndLine, sColors_Plain);
    CopyWindowToVram(WIN_ROLL, COPYWIN_GFX);
    gStrataCreditsState = CREDITS_STATE_THE_END;
    m4aSongNumStart(MUS_END);
    BeginNormalPaletteFade(PALETTES_ALL, 8, 16, 0, RGB_BLACK);
    gTasks[taskId].tDelay = 7200;
    gTasks[taskId].func = Task_TheEndWait;
}

// Any key after the fade-in (or two minutes) returns to the title screen.
static void Task_TheEndWait(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].tDelay == 0 || (gTasks[taskId].tDelay < 7080 && gMain.newKeys))
    {
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 8, 0, 16, RGB_BLACK);
        gTasks[taskId].func = Task_SoftReset;
        return;
    }
    gTasks[taskId].tDelay--;
}

#undef tDelay

static void Task_SoftReset(u8 taskId)
{
    if (!gPaletteFade.active)
        SoftReset(RESET_ALL);
}

#endif // !IS_FRLG
