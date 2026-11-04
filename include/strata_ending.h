#ifndef GUARD_STRATA_ENDING_H
#define GUARD_STRATA_ENDING_H

#include "constants/strata.h"

// The ending (roadmap S3): the lineage fates the credits list under each band of the column,
// and the bands themselves. See src/strata_ending.c; the roll is drawn by src/credits.c.

enum EndingFateKind
{
    ENDING_FATE_LOST,      // a fossil flag: the lineage died out at a filter
    ENDING_FATE_DESCENDED, // alive today in the TEAM or PC, as a descendant of its root species
    ENDING_FATE_LIVING,    // alive today, a species the descent table never changed
};

struct EndingFate
{
    u16 species; // the lost species, or the living one
    u16 root;    // the oldest species of its lineage in the descent table (= species if none)
    u8 kind;     // enum EndingFateKind
    u8 layer;    // enum StrataEra: the band it is listed under (a loss: the layer it was lost leaving)
    bool8 inTeam;
    u8 padding;
};

// Enough for every fossil slot plus every living species.
#define ENDING_FATES_MAX 128

// One band of the credits' column, listed from the bottom (oldest) up.
struct EndingBand
{
    u8 era;        // enum StrataEra
    bool8 isColby; // the late-glacial sub-layer: a thin band of its own above the Ice Age
    const u8 *name;
    const u8 *age;
    u16 header;    // band colours (the header strip and the layer below it)
    u16 body;
};

// Credits roll columns (pixels in the 240 px wide roll window).
#define ENDING_ROLL_WIDTH   240
#define ENDING_LEFT_X       8
#define ENDING_RIGHT_X      92
#define ENDING_RIGHT_END    232

// A line of the credits proper (the top of the roll).
struct EndingCreditsLine
{
    const u8 *text; // NULL: an empty row
    bool8 isTitle;
};

extern const struct EndingCreditsLine gEndingCreditsLines[];
extern const u32 gEndingCreditsLineCount;
// The roll's fixed lines (every one is width-checked by test/strata_ending.c).
extern const u8 gText_EndingColbyFind[];
extern const u8 gText_EndingColbyTrace[];
extern const u8 gText_EndingPair[];
extern const u8 gText_EndingNoLoss[];
extern const u8 gText_EndingPlayerColumn[];
extern const u8 gText_EndingPrelude1[];
extern const u8 gText_EndingPrelude2[];
extern const u8 gText_EndingTheEnd[];
extern const u8 gText_EndingTheEndLine[];

void Ending_FormatOverflow(u8 *dest, u32 count);
u32 Ending_GetBandCount(void);
const struct EndingBand *Ending_GetBand(u32 index);
enum Species Ending_GetLineageRoot(enum Species species);
const u8 *Ending_GetLossText(enum StrataEra filterEra);
u32 Ending_BuildFates(struct EndingFate *fates, u32 max, u32 *overflow);
void Ending_FormatFate(const struct EndingFate *fate, u8 *left, u8 *right);
u32 Ending_FitFont(const u8 *str, u32 width);
bool32 Ending_PairOnDisplay(void);
void Strata_RollCredits(void);

#endif // GUARD_STRATA_ENDING_H
