#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "string_util.h"
#include "test/test.h"
#include "constants/vars.h"

// These tests use the lineages in src/data/lineages.h.

static void ResetStrata(void)
{
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    ZeroPlayerPartyMons();
}

TEST("Lineage_GetDescendant leaves species without a descent unchanged")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_WOBBUFFET, ERA_CORRAL_BLUFFS, pressures), SPECIES_WOBBUFFET);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_CIMOLESTES, ERA_HELL_CREEK, pressures), SPECIES_CIMOLESTES);
}

TEST("Lineage_GetDescendant picks the default option with no pressures")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GALLINULOID);
}

TEST("Lineage_GetDescendant picks the option with the highest pressure")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_WATER] = 10;
    pressures[PRESSURE_PLANT_DIET] = 30;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GASTORNIS);
    pressures[PRESSURE_WATER] = 40;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_PRESBYORNIS);
}

TEST("Lineage_GetDescendant ignores pressures no option selects for")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_HEAT] = 255;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GALLINULOID);
}

TEST("Lineage_DescendMon keeps the mon's identity and recalculates stats")
{
    struct Pokemon mon;
    u8 pressure = 50;
    CreateMon(&mon, SPECIES_ASTERIORNIS, 30, 0x12345678, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_CUTE, &pressure); // PRESSURE_WATER

    EXPECT(Lineage_DescendMon(&mon, ERA_BIGHORN_PETM));
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SPECIES), SPECIES_PRESBYORNIS);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_LEVEL), 30);
    EXPECT_EQ(GetLevelFromMonExp(&mon), 30);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_PERSONALITY), 0x12345678);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_CUTE), 0);

    // Max HP must match a freshly recalculated Presbyornis.
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
    static const u8 sCustomName[] = _("Pip");

    CreateMon(&mon, SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_DescendMon(&mon, ERA_BIGHORN_PETM);
    GetMonData(&mon, MON_DATA_NICKNAME, nickname);
    EXPECT_EQ(StringCompare(nickname, GetSpeciesName(SPECIES_GALLINULOID)), 0);

    CreateMon(&mon, SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_NICKNAME, sCustomName);
    Lineage_DescendMon(&mon, ERA_BIGHORN_PETM);
    GetMonData(&mon, MON_DATA_NICKNAME, nickname);
    EXPECT_EQ(StringCompare(nickname, sCustomName), 0);
}

TEST("Lineage_AdvanceToEra passes a lineage through every intermediate era")
{
    ResetStrata();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);

    // Cimolestes -> Protictis (Corral Bluffs) -> Miacis (Green River) -> Hesperocyon (White River)
    // Emarginachelys -> Protochelydra (Corral Bluffs), then stasis until Ashfall
    EXPECT_EQ(Lineage_AdvanceToEra(ERA_WHITE_RIVER), 4);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_HESPEROCYON);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_SPECIES), SPECIES_PROTOCHELYD);
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_WHITE_RIVER);
}

TEST("Lineage_AdvanceToEra does nothing when moving to the current or an earlier era")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);

    EXPECT_EQ(Lineage_AdvanceToEra(ERA_HELL_CREEK), 0);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_CIMOLESTES);
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_GREEN_RIVER);
}

TEST("Lineage_AdvanceToEra also descends mons stored in the PC")
{
    struct BoxPokemon *boxMon = GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, IN_BOX_COUNT - 1);
    ResetStrata();
    ZeroBoxMonData(boxMon);
    CreateBoxMon(boxMon, SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);
    EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_SPECIES), SPECIES_PROTOCHELYD);
    ZeroBoxMonData(boxMon);
}
