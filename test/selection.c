#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "selection.h"
#include "test/battle.h"
#include "constants/vars.h"

TEST("Selection_AddPressure saturates at 255")
{
    struct Pokemon mon;
    CreateMon(&mon, SPECIES_TORCHIC, 5, 0, OTID_STRUCT_PLAYER_ID);
    Selection_AddPressure(&mon, PRESSURE_WATER, 200);
    Selection_AddPressure(&mon, PRESSURE_WATER, 200);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_CUTE), 255);
}

TEST("Selection_AddPressure ignores PRESSURE_NONE and empty slots")
{
    struct Pokemon mon;
    u8 pressures[PRESSURE_COUNT];
    u32 i;

    CreateMon(&mon, SPECIES_TORCHIC, 5, 0, OTID_STRUCT_PLAYER_ID);
    Selection_AddPressure(&mon, PRESSURE_NONE, 10);
    Selection_GetBoxMonPressures(&mon.box, pressures);
    for (i = 0; i < PRESSURE_COUNT; i++)
        EXPECT_EQ(pressures[i], 0);

    ZeroMonData(&mon);
    Selection_AddPressure(&mon, PRESSURE_WATER, 10);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_CUTE), 0);
}

TEST("Selection_ApplyTick adds habitat and climate pressure to the whole party")
{
    ZeroPlayerPartyMons();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TORCHIC, 5, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_SQUIRTLE, 5, 0, OTID_STRUCT_PLAYER_ID);

    Selection_ApplyTick(PRESSURE_OPEN, 2);
    Selection_ApplyTick(PRESSURE_NONE, 2);

    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_BEAUTY), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SHEEN), 4);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_BEAUTY), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_SHEEN), 4);
}

TEST("Habitat pressure from ticks steers the next descent")
{
    u32 i;
    ZeroPlayerPartyMons();
    VarSet(VAR_STRATA_ERA, ERA_CORRAL_BLUFFS);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);

    for (i = 0; i < 5; i++)
        Selection_ApplyTick(PRESSURE_WATER, 0);
    Selection_ApplyTick(PRESSURE_OPEN, 0);

    Lineage_AdvanceToEra(ERA_BIGHORN_PETM);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_PRESBYORNIS);
}

WILD_BATTLE_TEST("Knocking out a foe with a move adds meat diet pressure")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_CATERPIE) { HP(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        MESSAGE("The wild Caterpie fainted!");
    } THEN {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_TOUGH), SELECTION_PREY_PRESSURE);
    }
}

WILD_BATTLE_TEST("A foe fainting from poison adds no meat diet pressure")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_CATERPIE) { HP(1); Status1(STATUS1_POISON); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        MESSAGE("The wild Caterpie fainted!");
    } THEN {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_TOUGH), 0);
    }
}

WILD_BATTLE_TEST("A foe fainting by its own move adds no meat diet pressure")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GEODUDE);
    } WHEN {
        TURN { MOVE(opponent, MOVE_EXPLOSION); MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        MESSAGE("The wild Geodude fainted!");
    } THEN {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_TOUGH), 0);
    }
}
