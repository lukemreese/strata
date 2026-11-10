#include "global.h"
#include "string_util.h"
#include "text.h"
#include "test/test.h"
#include "constants/characters.h"

// The new game's arrival (data/maps/InsideOfTruck, StrataFieldCamp's arrival script): the texts
// fit the message window and carry no stock branding.

#define MESSAGE_WIDTH 208

#define TRUCK_TEXTS(X) \
    X(InsideOfTruck_Text_Arrival) \
    X(InsideOfTruck_Text_Crate) \
    X(StrataFieldCamp_Text_Arrival)

#define DECLARE_TEXT(label) extern const u8 label[];
TRUCK_TEXTS(DECLARE_TEXT)
#define LIST_TEXT(label) label,
static const u8 *const sTruckTexts[] = { TRUCK_TEXTS(LIST_TEXT) };

// Widest line of a message (lines end at \n, \l and \p), and the most \n in any one page.
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

TEST("The truck arrival texts fit the message window")
{
    u32 i, j, breaks;

    // Widest placeholder: a full-length player name.
    for (i = 0; i < PLAYER_NAME_LENGTH; i++)
        gSaveBlock2Ptr->playerName[i] = CHAR_W;
    gSaveBlock2Ptr->playerName[PLAYER_NAME_LENGTH] = EOS;

    for (i = 0; i < ARRAY_COUNT(sTruckTexts); i++)
    {
        StringExpandPlaceholders(gStringVar4, sTruckTexts[i]);
        EXPECT_LE(WidestLine(gStringVar4, &breaks), MESSAGE_WIDTH);
        EXPECT_LE(breaks, 1);   // two lines to a page: the second comes with \n, the rest scroll
        // No stock branding: nothing starting "POK" (the stock name prefix) in the text.
        for (j = 0; gStringVar4[j] != EOS; j++)
            EXPECT(!(gStringVar4[j] == CHAR_P && gStringVar4[j + 1] == CHAR_O && gStringVar4[j + 2] == CHAR_K));
    }
}
