#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "selection.h"
#include "strata_acts.h"
#include "strata_forecast.h"
#include "string_util.h"
#include "text.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/vars.h"

// The rig forecast (src/strata_forecast.c) must say exactly what the load does:
// these tests run it, then the real Lineage_AdvanceToEra, and compare.

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)
#define STRATA_SPECIES_COUNT (SPECIES_CUSTOM_END - FIRST_STRATA_SPECIES)

static void ResetStrata(void)
{
    u32 boxId, boxPos;
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    ZeroPlayerPartyMons();
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
            ZeroBoxMonData(GetBoxedMonPtr(boxId, boxPos));
    }
}

static u32 sRng;

static u32 Rand(u32 n)
{
    sRng ^= sRng << 13;
    sRng ^= sRng >> 17;
    sRng ^= sRng << 5;
    return sRng % n;
}

// Counters around every threshold in src/data/lineages.h.
static const u8 sPressureValues[] = { 0, 12, 23, 41, 63, 64, 65, 95, 96, 97, 120, 159, 160, 200, 255 };

static void SetPressure(struct BoxPokemon *boxMon, u32 pressure, u32 value)
{
    struct Pokemon mon;
    u8 pressures[PRESSURE_COUNT];
    u32 i;

    // Selection's own setter needs a struct Pokemon: go through one.
    BoxMonToMon(boxMon, &mon);
    Selection_GetBoxMonPressures(boxMon, pressures);
    pressures[pressure] = value;
    Selection_ResetBoxMonPressures(&mon.box);
    for (i = 0; i < PRESSURE_COUNT; i++)
        Selection_AddPressure(&mon, i, pressures[i]);
    *boxMon = mon.box;
}

static void RandomPressures(struct BoxPokemon *boxMon)
{
    u32 i;
    for (i = 0; i < PRESSURE_COUNT; i++)
    {
        if (Rand(5) < 2)
            SetPressure(boxMon, i, sPressureValues[Rand(ARRAY_COUNT(sPressureValues))]);
    }
}

// Half the time a species that has descent options entering `era`, else any.
static u16 RandomSpecies(u32 era)
{
    u16 candidates[STRATA_SPECIES_COUNT];
    u32 i, count = 0;

    for (i = FIRST_STRATA_SPECIES; i < SPECIES_CUSTOM_END; i++)
    {
        if (Lineage_GetDescentOptions(i, era) != NULL)
            candidates[count++] = i;
    }
    if (count != 0 && Rand(2) == 0)
        return candidates[Rand(count)];
    return FIRST_STRATA_SPECIES + Rand(STRATA_SPECIES_COUNT);
}

#define MAX_TEST_BOX_MONS 10

// What the generated cases covered: TEAM fates, hint states, refills (gift, PC).
static u16 sSeen[8];

// A species with no descent entering `era` that dies out then, or SPECIES_NONE.
static u16 RandomDoomedSpecies(u32 era)
{
    u16 candidates[STRATA_SPECIES_COUNT];
    u32 i, count = 0;

    for (i = FIRST_STRATA_SPECIES; i < SPECIES_CUSTOM_END; i++)
    {
        if (Lineage_GetDescentOptions(i, era) == NULL && Lineage_IsExtinctInEra(i, era))
            candidates[count++] = i;
    }
    return count != 0 ? candidates[Rand(count)] : SPECIES_NONE;
}

enum { TEAM_RANDOM, TEAM_KEEPER, TEAM_DOOMED };

// One generated team and PC, forecast then loaded from `fromEra` to `targetEra`.
// TEAM_KEEPER puts a gar (never changes, never dies out) first, so no refill;
// TEAM_DOOMED is a small TEAM that dies out entirely, so it is refilled.
static void CheckForecastAgainstLoad(u32 fromEra, u32 targetEra, u32 team)
{
    struct RigForecast rig;
    struct LineageForecast boxForecast[MAX_TEST_BOX_MONS];
    u16 boxSlot[MAX_TEST_BOX_MONS];
    u32 i, j, partyCount, boxCount = 0, partyLost = 0;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, fromEra);
    if (team == TEAM_DOOMED && RandomDoomedSpecies(fromEra + 1) == SPECIES_NONE)
        team = TEAM_RANDOM;
    partyCount = 1 + Rand(team == TEAM_DOOMED ? 2 : PARTY_SIZE);
    for (i = 0; i < partyCount; i++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][i];
        u16 species;
        if (team == TEAM_KEEPER && i == 0)
            species = SPECIES_LEPISOSTEUS;
        else if (team == TEAM_DOOMED)
            species = RandomDoomedSpecies(fromEra + 1);
        else
            species = RandomSpecies(fromEra + 1);
        CreateMon(mon, species, 1 + Rand(60), 0, OTID_STRUCT_PLAYER_ID);
        RandomPressures(&mon->box);
    }
    CalculatePlayerPartyCount();
    for (i = Rand(MAX_TEST_BOX_MONS + 1) * (Rand(4) != 0); i > 0; i--)
    {
        u16 slot = Rand(TOTAL_BOXES_COUNT * IN_BOX_COUNT);
        struct BoxPokemon *boxMon = GetBoxedMonPtr(slot / IN_BOX_COUNT, slot % IN_BOX_COUNT);
        if (GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES))
            continue;
        CreateBoxMon(boxMon, RandomSpecies(fromEra + 1), 1 + Rand(60), 0, OTID_STRUCT_PLAYER_ID);
        RandomPressures(boxMon);
        boxSlot[boxCount++] = slot;
    }

    Forecast_Rig(targetEra, &rig);
    for (i = 0; i < boxCount; i++)
        EXPECT(Forecast_BoxMon(GetBoxedMonPtr(boxSlot[i] / IN_BOX_COUNT, boxSlot[i] % IN_BOX_COUNT), targetEra, &boxForecast[i]));
    for (i = 0; i < rig.partyCount; i++)
    {
        struct BranchHint hints[FORECAST_MAX_HINTS];
        u32 h, n = 0;
        partyLost += (rig.party[i].fate == FATE_LOST);
        sSeen[rig.party[i].fate]++;
        if (rig.party[i].decisionSpecies != SPECIES_NONE)
            n = Forecast_GetBranchHints(rig.party[i].decisionSpecies, rig.party[i].decisionEra, rig.party[i].pressures, hints);
        for (h = 0; h < n; h++)
            sSeen[3 + hints[h].state]++;
    }
    if (rig.refillSpecies != SPECIES_NONE)
        sSeen[6 + rig.refillFromPc]++;
    EXPECT_EQ(rig.partyCount, partyCount);
    EXPECT_EQ(rig.pcTotal, boxCount);

    Lineage_AdvanceToEra(targetEra);

    EXPECT_EQ(VarGet(VAR_STRATA_ERA), targetEra);
    EXPECT_EQ(Lineage_GetExtinctionCount(), partyLost + rig.pcLost);
    EXPECT_EQ(CalculatePlayerPartyCount(), rig.expectedCount);
    for (i = 0; i < rig.expectedCount; i++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][i];
        EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), rig.expectedSpecies[i]);
        EXPECT_EQ(GetLevelFromMonExp(mon), rig.expectedLevel[i]);
    }
    for (i = 0, j = 0; i < boxCount; i++)
    {
        struct BoxPokemon *boxMon = GetBoxedMonPtr(boxSlot[i] / IN_BOX_COUNT, boxSlot[i] % IN_BOX_COUNT);
        if ((rig.refillFromPc && rig.refillSlot == boxSlot[i]) || boxForecast[i].fate == FATE_LOST)
        {
            EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_SPECIES), SPECIES_NONE);
            continue;
        }
        EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_SPECIES), boxForecast[i].result);
        EXPECT_EQ(GetLevelFromBoxMonExp(boxMon), boxForecast[i].newLevel);
        j++;
    }
    EXPECT_EQ(j + (rig.refillFromPc ? 1 : 0), rig.pcDescend + rig.pcStasis);
}

TEST("The rig forecast matches the next-layer load for generated teams")
{
    u32 n;
    memset(sSeen, 0, sizeof(sSeen));
    for (n = 0; n < 96; n++)
    {
        sRng = 0x9E3779B9 + n * 0x85EBCA6B;
        // Every load the rig makes: Hell Creek -> impact winter ... Trap Cave -> today.
        u32 from = ERA_HELL_CREEK + n % (ERA_EPILOGUE - ERA_HELL_CREEK);
        CheckForecastAgainstLoad(from, from + 1, (n / 8) % 3 == 2 ? TEAM_DOOMED : TEAM_RANDOM);
    }
    // The cases reach every outcome, so the comparison means something.
    for (n = 0; n < ARRAY_COUNT(sSeen); n++)
        EXPECT_GT(sSeen[n], 0);
}

TEST("The rig forecast matches a load across several eras")
{
    u32 n;
    for (n = 0; n < 32; n++)
    {
        u32 from;
        sRng = 0x51ED270B + n * 0x27D4EB2F;
        from = ERA_HELL_CREEK + Rand(ERA_ASHFALL - ERA_HELL_CREEK);
        CheckForecastAgainstLoad(from, from + 2 + Rand(2), TEAM_KEEPER);
    }
}

TEST("The forecast reports how close each branch is")
{
    struct LineageForecast f;
    struct BranchHint hints[FORECAST_MAX_HINTS];
    u8 lines[FORECAST_DETAIL_LINES][FORECAST_LINE_SIZE];
    u8 pressures[PRESSURE_COUNT] = {0};

    // Hesperocyon at the White River, entering Ashfall: Epicyon needs ANIMAL 64.
    pressures[PRESSURE_MEAT_DIET] = 41;
    Forecast_Lineage(SPECIES_HESPEROCYON, 35, pressures, ERA_WHITE_RIVER, ERA_ASHFALL, &f);
    EXPECT_EQ(f.fate, FATE_DESCENDS);
    EXPECT_EQ(f.result, SPECIES_LEPTOCYON);
    EXPECT_EQ(f.newLevel, 37); // the Ashfall level floor
    EXPECT_EQ(Forecast_GetBranchHints(f.decisionSpecies, f.decisionEra, f.pressures, hints), 1);
    EXPECT_EQ(hints[0].species, SPECIES_EPICYON);
    EXPECT_EQ(hints[0].pressure, PRESSURE_MEAT_DIET);
    EXPECT_EQ(hints[0].minScore, 64);
    EXPECT_EQ(hints[0].now, 41);
    EXPECT_EQ(hints[0].state, HINT_BELOW_THRESHOLD);
    EXPECT_EQ(Forecast_FormatDetail(&f, lines), 3);
    EXPECT_EQ(StringCompare(lines[0], COMPOUND_STRING("Default descent: no branch reached.")), 0);
    EXPECT_EQ(StringCompare(lines[1], COMPOUND_STRING("Epicyon if ANIMAL reaches 64 (now 41).")), 0);
    EXPECT_EQ(StringCompare(lines[2], COMPOUND_STRING("Raised to the era floor: {LV}35 {RIGHT_ARROW} {LV}37.")), 0);

    pressures[PRESSURE_MEAT_DIET] = 64;
    Forecast_Lineage(SPECIES_HESPEROCYON, 40, pressures, ERA_WHITE_RIVER, ERA_ASHFALL, &f);
    EXPECT_EQ(f.result, SPECIES_EPICYON);
    Forecast_GetBranchHints(f.decisionSpecies, f.decisionEra, f.pressures, hints);
    EXPECT_EQ(hints[0].state, HINT_TAKEN);
    EXPECT_EQ(Forecast_FormatDetail(&f, lines), 1);
    EXPECT_EQ(StringCompare(lines[0], COMPOUND_STRING("Animal-diet branch: ANIMAL 64/64.")), 0);

    // Leptocyon steered both ways: the dire wolf's higher counter wins.
    memset(pressures, 0, sizeof(pressures));
    pressures[PRESSURE_MEAT_DIET] = 100;
    pressures[PRESSURE_OPEN] = 97;
    Forecast_Lineage(SPECIES_LEPTOCYON, 45, pressures, ERA_ASHFALL, ERA_TRAP_CAVE, &f);
    EXPECT_EQ(f.result, SPECIES_AENOCYON);
    EXPECT_EQ(Forecast_GetBranchHints(f.decisionSpecies, f.decisionEra, f.pressures, hints), 2);
    EXPECT_EQ(hints[0].species, SPECIES_AENOCYON);
    EXPECT_EQ(hints[0].state, HINT_TAKEN);
    EXPECT_EQ(hints[1].species, SPECIES_VULPES);
    EXPECT_EQ(hints[1].state, HINT_OUTSCORED);
    EXPECT_EQ(hints[1].beatenBy, 100);
    Forecast_FormatDetail(&f, lines);
    EXPECT_EQ(StringCompare(lines[1], COMPOUND_STRING("Vulpes: OPEN 97, outscored (100).")), 0);

    // Single-path lineages have no branches to hint at.
    memset(pressures, 0, sizeof(pressures));
    Forecast_Lineage(SPECIES_CIMOLESTES, 20, pressures, ERA_IMPACT_WINTER, ERA_CORRAL_BLUFFS, &f);
    EXPECT_EQ(f.result, SPECIES_PROTICTIS);
    EXPECT_EQ(Forecast_GetBranchHints(f.decisionSpecies, f.decisionEra, f.pressures, hints), 0);
}

TEST("The forecast reports extinctions, including a descendant's")
{
    struct LineageForecast f;
    u8 name[FORECAST_LINE_SIZE], level[FORECAST_LINE_SIZE];
    u8 pressures[PRESSURE_COUNT] = {0};

    Forecast_Lineage(SPECIES_BOREALOSUCH, 30, pressures, ERA_GREEN_RIVER, ERA_WHITE_RIVER, &f);
    EXPECT_EQ(f.fate, FATE_LOST);
    EXPECT_EQ(f.lostEra, ERA_WHITE_RIVER);
    EXPECT_EQ(f.newLevel, 30);
    Forecast_FormatRow(&f, name, level);
    EXPECT_EQ(StringCompare(name, COMPOUND_STRING("Borealosuch: {COLOR RED}{SHADOW LIGHT_RED}will not survive")), 0);
    EXPECT_EQ(level[0], EOS);

    // Two layers at once: Hesperocyon takes the Epicyon branch, which dies out by the Ice Age.
    pressures[PRESSURE_MEAT_DIET] = 80;
    Forecast_Lineage(SPECIES_HESPEROCYON, 35, pressures, ERA_WHITE_RIVER, ERA_TRAP_CAVE, &f);
    EXPECT_EQ(f.fate, FATE_LOST);
    EXPECT_EQ(f.result, SPECIES_EPICYON);
    EXPECT_EQ(f.descents, 1);
    EXPECT_EQ(f.lostEra, ERA_TRAP_CAVE);

    // Stasis: the gar, with no change in the record ahead.
    memset(pressures, 0, sizeof(pressures));
    Forecast_Lineage(SPECIES_LEPISOSTEUS, 50, pressures, ERA_ASHFALL, ERA_TRAP_CAVE, &f);
    EXPECT_EQ(f.fate, FATE_STASIS);
    EXPECT_EQ(f.newLevel, 50);
    Forecast_FormatRow(&f, name, level);
    EXPECT_EQ(StringCompare(level, COMPOUND_STRING("{LV}50")), 0);
}

TEST("The forecast counts what happens in the PC")
{
    struct RigForecast rig;
    u8 lines[FORECAST_DETAIL_LINES][FORECAST_LINE_SIZE];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_LEPISOSTEUS, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_KNIGHTIA, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 4), SPECIES_EOHIPPUS, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(2, 0), SPECIES_LEPISOSTEUS, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(5, 9), SPECIES_CHAMPSOSAUR, 30, 0, OTID_STRUCT_PLAYER_ID);

    Forecast_Rig(ERA_WHITE_RIVER, &rig);
    EXPECT_EQ(rig.pcTotal, 4);
    EXPECT_EQ(rig.pcDescend, 1);
    EXPECT_EQ(rig.pcStasis, 1);
    EXPECT_EQ(rig.pcLost, 2);
    EXPECT_EQ(rig.pcFirstLost, SPECIES_KNIGHTIA);
    EXPECT_EQ(rig.refillSpecies, SPECIES_NONE);
    EXPECT_EQ(Forecast_FormatPcDetail(&rig, lines), 3);
    EXPECT_EQ(StringCompare(lines[0], COMPOUND_STRING("1 descend, 1 no change, 2 lost.")), 0);
    EXPECT_EQ(StringCompare(lines[1], COMPOUND_STRING("Lost: Knightia and 1 more.")), 0);

    Lineage_AdvanceToEra(ERA_WHITE_RIVER);
    EXPECT_EQ(Lineage_GetExtinctionCount(), 2);
    EXPECT_EQ(GetBoxMonData(GetBoxedMonPtr(0, 4), MON_DATA_SPECIES), SPECIES_MESOHIPPUS);
}

TEST("The forecast names who joins a TEAM the load would empty")
{
    struct RigForecast rig;

    // A survivor from the PC.
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TYRANNOSAUR, 12, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(3, 5), SPECIES_LEPISOSTEUS, 5, 0, OTID_STRUCT_PLAYER_ID);
    Forecast_Rig(ERA_IMPACT_WINTER, &rig);
    EXPECT(rig.refillFromPc);
    EXPECT_EQ(rig.refillSlot, 3 * IN_BOX_COUNT + 5);
    EXPECT_EQ(rig.refillSpecies, SPECIES_LEPISOSTEUS);
    EXPECT_EQ(rig.refillLevel, 7); // the impact winter's floor
    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
    EXPECT_EQ(GetLevelFromMonExp(&gParties[B_TRAINER_PLAYER][0]), 7);

    // Nobody anywhere: the gift survivor.
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TRICERATOPS, 12, 0, OTID_STRUCT_PLAYER_ID);
    Forecast_Rig(ERA_IMPACT_WINTER, &rig);
    EXPECT(!rig.refillFromPc);
    EXPECT_EQ(rig.expectedCount, 1);
    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), rig.refillSpecies);
    EXPECT_EQ(GetLevelFromMonExp(&gParties[B_TRAINER_PLAYER][0]), rig.refillLevel);

    // After the multituberculates die out, the gift is the gar.
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_KNIGHTIA, 30, 0, OTID_STRUCT_PLAYER_ID);
    Forecast_Rig(ERA_WHITE_RIVER, &rig);
    EXPECT_EQ(rig.refillSpecies, SPECIES_LEPISOSTEUS);
    Lineage_AdvanceToEra(ERA_WHITE_RIVER);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
    EXPECT_EQ(GetLevelFromMonExp(&gParties[B_TRAINER_PLAYER][0]), rig.refillLevel);
}

TEST("The forecast covers the load the rig makes")
{
    struct RigForecast rig;
    u8 pressure = 96;
    u32 i;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_ASHFALL);
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_ASHFALL));
    EXPECT_EQ(Strata_GetRigTargetEra(), ERA_TRAP_CAVE);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_GALLINULOID, 40, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_BEAUTY, &pressure); // OPEN
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_TELEOCERAS, 40, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][2], SPECIES_LEPTOCYON, 30, 0, OTID_STRUCT_PLAYER_ID);
    CalculatePlayerPartyCount();

    Forecast_Rig(Strata_GetRigTargetEra(), &rig);
    EXPECT_EQ(rig.party[0].result, SPECIES_CENTROCERCUS);
    EXPECT_EQ(rig.party[1].fate, FATE_LOST);
    EXPECT_EQ(rig.party[2].result, SPECIES_CANIS);
    EXPECT_EQ(rig.party[2].newLevel, 43);
    RUN_OVERWORLD_SCRIPT(
        special Strata_RigLoadNext;
    );
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_TRAP_CAVE);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_IN_ACT(ERA_TRAP_CAVE));
    EXPECT_EQ(CalculatePlayerPartyCount(), rig.expectedCount);
    for (i = 0; i < rig.expectedCount; i++)
    {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES), rig.expectedSpecies[i]);
        EXPECT_EQ(GetLevelFromMonExp(&gParties[B_TRAINER_PLAYER][i]), rig.expectedLevel[i]);
    }
    // Re-entering a layer loads nothing new.
    EXPECT_EQ(Strata_GetRigTargetEra(), ERA_COUNT);
}

TEST("The pressure chart finds the next layer that changes a lineage")
{
    u32 era;
    EXPECT_EQ(Forecast_GetNextChange(SPECIES_GALLINULOID, ERA_BIGHORN_PETM, &era), FATE_DESCENDS);
    EXPECT_EQ(era, ERA_TRAP_CAVE);
    EXPECT_EQ(Forecast_GetNextChange(SPECIES_TELEOCERAS, ERA_ASHFALL, &era), FATE_LOST);
    EXPECT_EQ(era, ERA_TRAP_CAVE);
    EXPECT_EQ(Forecast_GetNextChange(SPECIES_LEPISOSTEUS, ERA_HELL_CREEK, &era), FATE_STASIS);
    EXPECT_EQ(era, ERA_COUNT);
    EXPECT_EQ(Forecast_GetNextChange(SPECIES_CIMOLESTES, ERA_HELL_CREEK, &era), FATE_DESCENDS);
    EXPECT_EQ(era, ERA_CORRAL_BLUFFS);
}

static void ExpectFits(const u8 *str, u32 width)
{
    EXPECT_LE(GetStringWidth(Forecast_FitFont(str, width), str, 0), width);
}

// Every species entering every era, with no pressure, each pressure at the top,
// and each just below its branch threshold, at a level the floor raises.
TEST("Every forecast row and detail line fits its window")
{
    u32 species, era, p, i, n;
    u8 pressures[PRESSURE_COUNT];
    u8 name[FORECAST_LINE_SIZE], level[FORECAST_LINE_SIZE];
    u8 lines[FORECAST_DETAIL_LINES][FORECAST_LINE_SIZE];
    struct LineageForecast f;
    struct RigForecast rig;

    for (species = FIRST_STRATA_SPECIES; species < SPECIES_CUSTOM_END; species++)
    {
        for (era = ERA_IMPACT_WINTER; era < ERA_COUNT; era++)
        {
            // Pressures only matter where the lineage has a choice to make.
            bool32 decides = Lineage_GetDescentOptions(species, era) != NULL;
            for (p = decides ? 0 : PRESSURE_COUNT * 2; p <= PRESSURE_COUNT * 2; p++)
            {
                memset(pressures, 0, sizeof(pressures));
                if (p < PRESSURE_COUNT)
                    pressures[p] = 255;
                else if (p < PRESSURE_COUNT * 2)
                    pressures[p - PRESSURE_COUNT] = 63;
                Forecast_Lineage(species, 1, pressures, era - 1, era, &f);
                Forecast_FormatRow(&f, name, level);
                ExpectFits(name, FORECAST_NAME_WIDTH);
                ExpectFits(level, FORECAST_LEVEL_WIDTH);
                n = Forecast_FormatDetail(&f, lines);
                EXPECT_LE(n, FORECAST_DETAIL_LINES);
                for (i = 0; i < n; i++)
                    ExpectFits(lines[i], FORECAST_DETAIL_WIDTH);
            }
        }
    }

    // The PC at its widest: three-digit counts, the longest names, a refill.
    memset(&rig, 0, sizeof(rig));
    rig.pcTotal = 420;
    rig.pcDescend = 140;
    rig.pcStasis = 140;
    rig.pcLost = 140;
    for (species = FIRST_STRATA_SPECIES; species < SPECIES_CUSTOM_END; species++)
    {
        rig.pcFirstLost = species;
        rig.refillSpecies = species;
        for (i = 0; i < 2; i++)
        {
            rig.refillFromPc = i;
            Forecast_FormatPcRow(&rig, name, level);
            ExpectFits(name, FORECAST_NAME_WIDTH);
            ExpectFits(level, FORECAST_LEVEL_WIDTH);
            n = Forecast_FormatPcDetail(&rig, lines);
            EXPECT_LE(n, FORECAST_DETAIL_LINES);
            for (p = 0; p < n; p++)
                ExpectFits(lines[p], FORECAST_DETAIL_WIDTH);
        }
    }
}
