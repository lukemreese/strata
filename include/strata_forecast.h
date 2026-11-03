#ifndef GUARD_STRATA_FORECAST_H
#define GUARD_STRATA_FORECAST_H

#include "constants/strata.h"

// Rig forecast (F1) and pressure chart (F2): what the next rig load will do to
// each lineage, and what is steering it. A dry run of the same steps as
// Lineage_AdvanceToEra (src/lineage.c), built on lineage's public API; the tests
// in test/strata_forecast.c hold it to the real outcome.

enum LineageFate
{
    FATE_STASIS,   // same species after the load
    FATE_DESCENDS, // becomes another species
    FATE_LOST,     // dies out (removed from the TEAM or PC)
};

// One lineage over a load from VAR_STRATA_ERA up to a target era.
struct LineageForecast
{
    u16 species;         // now
    u16 result;          // after the load; for FATE_LOST the species that dies out
    u8 fate;             // enum LineageFate
    u8 level;            // now
    u8 newLevel;         // after the era level floors (FATE_LOST: unchanged)
    u8 lostEra;          // FATE_LOST: the era it dies out in; else ERA_COUNT
    u8 descents;         // descents on the way (more than one only across several eras)
    u8 targetEra;        // the era loaded
    u8 decisionEra;      // first era on the way with descent options, or ERA_COUNT
    u16 decisionSpecies; // the species deciding then (SPECIES_NONE if none)
    u8 pressures[PRESSURE_COUNT]; // its counters at that decision
};

enum BranchHintState
{
    HINT_TAKEN,           // this branch wins
    HINT_BELOW_THRESHOLD, // its counter hasn't reached minScore
    HINT_OUTSCORED,       // eligible, but another branch has a higher counter
};

// A non-default descent option and how close the lineage is to it.
struct BranchHint
{
    u16 species;
    u8 pressure;  // enum SelectionPressure
    u8 minScore;
    u8 now;       // the counter now
    u8 state;     // enum BranchHintState
    u8 beatenBy;  // HINT_OUTSCORED: the winning branch's counter
};

#define FORECAST_MAX_HINTS 4

// Everything a rig load will do, for the forecast window and the harness.
struct RigForecast
{
    u8 fromEra;
    u8 targetEra;        // ERA_COUNT: nothing to load
    u8 partyCount;       // party[] entries (eggs are skipped: they never change)
    u8 expectedCount;    // the TEAM after the load, in order (eggs, survivors, refill)
    struct LineageForecast party[PARTY_SIZE];
    u16 expectedSpecies[PARTY_SIZE];
    u8 expectedLevel[PARTY_SIZE];
    u16 pcTotal;
    u16 pcDescend;
    u16 pcStasis;
    u16 pcLost;
    u16 pcFirstLost;     // species of the first PC animal lost (box order)
    u16 refillSpecies;   // when every TEAM animal is lost: who joins (else SPECIES_NONE)
    u16 refillSlot;      // refillFromPc: boxId * IN_BOX_COUNT + boxPos it leaves
    u8 refillLevel;
    bool8 refillFromPc;  // TRUE: the first surviving PC animal; FALSE: a gift survivor
};

extern struct RigForecast gStrataRigForecast; // the last forecast shown (read by the harness)

void Forecast_Lineage(u16 species, u32 level, const u8 *pressures, u32 fromEra, u32 targetEra, struct LineageForecast *out);
bool32 Forecast_BoxMon(struct BoxPokemon *boxMon, u32 targetEra, struct LineageForecast *out);
u32 Forecast_GetBranchHints(u16 species, u32 era, const u8 *pressures, struct BranchHint *hints);
void Forecast_Rig(u32 targetEra, struct RigForecast *out);
u32 Forecast_GetNextChange(u16 species, u32 era, u32 *changeEra);

// Text, exposed for the width tests. A row is two columns (the outcome, and the
// level or PC losses); a detail is up to FORECAST_DETAIL_LINES lines.
#define FORECAST_LINE_SIZE 72
#define FORECAST_DETAIL_LINES 3
void Forecast_FormatRow(const struct LineageForecast *f, u8 *name, u8 *level);
u32 Forecast_FormatDetail(const struct LineageForecast *f, u8 lines[][FORECAST_LINE_SIZE]);
void Forecast_FormatPcRow(const struct RigForecast *rig, u8 *name, u8 *lost);
u32 Forecast_FormatPcDetail(const struct RigForecast *rig, u8 lines[][FORECAST_LINE_SIZE]);
u32 Forecast_FitFont(const u8 *str, u32 width);

#define FORECAST_NAME_WIDTH   160 // list row, before the level column
#define FORECAST_LEVEL_WIDTH  44  // level column (to the window's edge)
#define FORECAST_DETAIL_WIDTH 224 // detail window (28 tiles)

void Strata_RigForecast(void);
void ShowStrataPressureChart(u8 slot, void (*exitCallback)(void));

#endif // GUARD_STRATA_FORECAST_H
