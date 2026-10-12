#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "string_util.h"
#include "test/test.h"
#include "constants/vars.h"

// These tests use the placeholder lineages in src/data/lineages.h.

static void ResetStrata(void)
{
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    ZeroPlayerPartyMons();
}

TEST("Lineage_GetDescendant leaves species without a descent unchanged")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_WOBBUFFET, ERA_CORRAL_BLUFFS, pressures), SPECIES_WOBBUFFET);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_POOCHYENA, ERA_HELL_CREEK, pressures), SPECIES_POOCHYENA);
}

TEST("Lineage_GetDescendant picks the default option with no pressures")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_TORCHIC, ERA_GREEN_RIVER, pressures), SPECIES_COMBUSKEN);
}

TEST("Lineage_GetDescendant picks the option with the highest pressure")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_WATER] = 10;
    pressures[PRESSURE_OPEN] = 30;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_TORCHIC, ERA_GREEN_RIVER, pressures), SPECIES_DODUO);
    pressures[PRESSURE_WATER] = 40;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_TORCHIC, ERA_GREEN_RIVER, pressures), SPECIES_DUCKLETT);
}

TEST("Lineage_GetDescendant ignores pressures no option selects for")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_HEAT] = 255;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_TORCHIC, ERA_GREEN_RIVER, pressures), SPECIES_COMBUSKEN);
}

TEST("Lineage_DescendMon keeps the mon's identity and recalculates stats")
{
    struct Pokemon mon;
    u8 pressure = 50;
    CreateMon(&mon, SPECIES_TORCHIC, 30, 0x12345678, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_CUTE, &pressure); // PRESSURE_WATER

    // Torchic and Ducklett have different growth rates.
    EXPECT_NE(gSpeciesInfo[SPECIES_TORCHIC].growthRate, gSpeciesInfo[SPECIES_DUCKLETT].growthRate);
    EXPECT(Lineage_DescendMon(&mon, ERA_GREEN_RIVER));
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SPECIES), SPECIES_DUCKLETT);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_LEVEL), 30);
    EXPECT_EQ(GetLevelFromMonExp(&mon), 30);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_PERSONALITY), 0x12345678);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_CUTE), 0);

    // Max HP must match a freshly recalculated Ducklett.
    {
        u32 maxHp = GetMonData(&mon, MON_DATA_MAX_HP);
        CalculateMonStats(&mon);
        EXPECT_EQ(GetMonData(&mon, MON_DATA_MAX_HP), maxHp);
    }
}

TEST("Lineage_DescendMon renames default nicknames but keeps custom ones")
{
    struct Pokemon mon;
    u8 nickname[POKEMON_NAME_BUFFER_SIZE];
    static const u8 sCustomName[] = _("Ember");

    CreateMon(&mon, SPECIES_TORCHIC, 5, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_DescendMon(&mon, ERA_GREEN_RIVER);
    GetMonData(&mon, MON_DATA_NICKNAME, nickname);
    EXPECT_EQ(StringCompare(nickname, GetSpeciesName(SPECIES_COMBUSKEN)), 0);

    CreateMon(&mon, SPECIES_TORCHIC, 5, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_NICKNAME, sCustomName);
    Lineage_DescendMon(&mon, ERA_GREEN_RIVER);
    GetMonData(&mon, MON_DATA_NICKNAME, nickname);
    EXPECT_EQ(StringCompare(nickname, sCustomName), 0);
}

TEST("Lineage_AdvanceToEra passes a lineage through every intermediate era")
{
    ResetStrata();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_POOCHYENA, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_SQUIRTLE, 10, 0, OTID_STRUCT_PLAYER_ID);

    // Poochyena -> Mightyena (Corral Bluffs) -> Zigzagoon (White River)
    // Squirtle -> Wartortle (Bighorn PETM), then stasis until Ashfall
    EXPECT_EQ(Lineage_AdvanceToEra(ERA_WHITE_RIVER), 3);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_ZIGZAGOON);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_SPECIES), SPECIES_WARTORTLE);
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_WHITE_RIVER);
}

TEST("Lineage_AdvanceToEra does nothing when moving to the current or an earlier era")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_POOCHYENA, 10, 0, OTID_STRUCT_PLAYER_ID);

    EXPECT_EQ(Lineage_AdvanceToEra(ERA_HELL_CREEK), 0);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_POOCHYENA);
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_GREEN_RIVER);
}

TEST("Lineage_AdvanceToEra also descends mons stored in the PC")
{
    struct BoxPokemon *boxMon = GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, IN_BOX_COUNT - 1);
    ResetStrata();
    ZeroBoxMonData(boxMon);
    CreateBoxMon(boxMon, SPECIES_SQUIRTLE, 10, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_BIGHORN_PETM);
    EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_SPECIES), SPECIES_WARTORTLE);
    ZeroBoxMonData(boxMon);
}
