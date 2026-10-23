#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "field_player_avatar.h"
#include "selection.h"
#include "constants/metatile_behaviors.h"
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

// Asteriornis after `ticks` water ticks (and one open one) in Corral Bluffs.
static enum Species DescendAfterWaterTicks(u32 ticks)
{
    u32 i;
    ZeroPlayerPartyMons();
    VarSet(VAR_STRATA_ERA, ERA_CORRAL_BLUFFS);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);

    for (i = 0; i < ticks; i++)
        Selection_ApplyTick(PRESSURE_WATER, 0);
    Selection_ApplyTick(PRESSURE_OPEN, 0);

    Lineage_AdvanceToEra(ERA_BIGHORN_PETM);
    return GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES);
}

TEST("Habitat pressure from ticks steers the next descent once past the threshold")
{
    EXPECT_EQ(DescendAfterWaterTicks(DESCENT_MIN_SCORE - 1), SPECIES_GALLINULOID);
    EXPECT_EQ(DescendAfterWaterTicks(DESCENT_MIN_SCORE), SPECIES_PRESBYORNIS);
}

TEST("Species diets: predators and omnivores eat animals, herbivores don't")
{
    EXPECT(Selection_EatsAnimals(SPECIES_HESPEROCYON));
    EXPECT_EQ(Selection_GetSpeciesDiet(SPECIES_TYRANNOSAUR), DIET_CARNIVORE);
    EXPECT_EQ(Selection_GetSpeciesDiet(SPECIES_LEPTOCYON), DIET_OMNIVORE);
    EXPECT(Selection_EatsAnimals(SPECIES_ASTERIORNIS));
    EXPECT(Selection_EatsAnimals(SPECIES_CHELYDRA));
    EXPECT(!Selection_EatsAnimals(SPECIES_GASTORNIS));
    EXPECT(!Selection_EatsAnimals(SPECIES_EOHIPPUS));
    EXPECT(!Selection_EatsAnimals(SPECIES_EDMONTOSAUR));
    EXPECT(!Selection_EatsAnimals(SPECIES_WOBBUFFET));
    EXPECT(!Selection_EatsAnimals(SPECIES_NONE));
}

TEST("Taking prey adds meat diet pressure only to animal eaters, up to the cap")
{
    struct Pokemon mon;
    u32 i;

    CreateMon(&mon, SPECIES_HESPEROCYON, 30, 0, OTID_STRUCT_PLAYER_ID);
    Selection_OnPreyTaken(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), SELECTION_PREY_PRESSURE);
    for (i = 0; i < 100; i++)
        Selection_OnPreyTaken(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), SELECTION_PREY_CAP);

    CreateMon(&mon, SPECIES_EDMONTOSAUR, 30, 0, OTID_STRUCT_PLAYER_ID);
    Selection_OnPreyTaken(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), 0);
}

TEST("The knockout cap doesn't undo meat diet pressure from other sources")
{
    struct Pokemon mon;
    CreateMon(&mon, SPECIES_HESPEROCYON, 30, 0, OTID_STRUCT_PLAYER_ID);
    Selection_AddPressure(&mon, PRESSURE_MEAT_DIET, SELECTION_PREY_CAP + 12); // e.g. carrion forage
    Selection_OnPreyTaken(&mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), SELECTION_PREY_CAP + 12);
    Selection_AddPressure(&mon, PRESSURE_MEAT_DIET, 12);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), SELECTION_PREY_CAP + 24);
}

TEST("Selection_AddPressureUpTo stops at the cap")
{
    struct Pokemon mon;
    CreateMon(&mon, SPECIES_TORCHIC, 5, 0, OTID_STRUCT_PLAYER_ID);
    Selection_AddPressureUpTo(&mon, PRESSURE_OPEN, 7, 10);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_BEAUTY), 7);
    Selection_AddPressureUpTo(&mon, PRESSURE_OPEN, 7, 10);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_BEAUTY), 10);
}

TEST("Shores and surfing count as water habitat")
{
    u8 savedFlags = gPlayerAvatar.flags;
    gPlayerAvatar.flags = 0;
    EXPECT_EQ(Selection_GetHabitat(MB_NORMAL, FALSE), PRESSURE_NONE);
    EXPECT_EQ(Selection_GetHabitat(MB_NORMAL, TRUE), PRESSURE_WATER);
    EXPECT_EQ(Selection_GetHabitat(MB_TALL_GRASS, FALSE), PRESSURE_OPEN);
    EXPECT_EQ(Selection_GetHabitat(MB_TALL_GRASS, TRUE), PRESSURE_WATER);
    EXPECT_EQ(Selection_GetHabitat(MB_POND_WATER, FALSE), PRESSURE_WATER);
    gPlayerAvatar.flags = PLAYER_AVATAR_FLAG_SURFING;
    EXPECT_EQ(Selection_GetHabitat(MB_NORMAL, FALSE), PRESSURE_WATER);
    gPlayerAvatar.flags = savedFlags;
}

TEST("Steps while surfing or wading add water pressure")
{
    u8 savedFlags = gPlayerAvatar.flags;
    u32 i;

    ZeroPlayerPartyMons();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    VarSet(VAR_STRATA_SELECTION_STEPS, 0);
    gPlayerAvatar.flags = PLAYER_AVATAR_FLAG_SURFING;
    for (i = 0; i < SELECTION_STEPS_PER_TICK * 3; i++)
        Selection_UpdateStepCounter(MB_NORMAL);
    gPlayerAvatar.flags = savedFlags;
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_CUTE), 3);
}

TEST("Hooking a fish adds water pressure to the whole party")
{
    ZeroPlayerPartyMons();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_CIMOLESTES, 5, 0, OTID_STRUCT_PLAYER_ID);
    Selection_OnFishHooked();
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_CUTE), SELECTION_FISH_PRESSURE);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_CUTE), SELECTION_FISH_PRESSURE);
}

WILD_BATTLE_TEST("Knocking out a foe with a move adds meat diet pressure to a predator")
{
    GIVEN {
        PLAYER(SPECIES_HESPEROCYON) { Moves(MOVE_SCRATCH); }
        OPPONENT(SPECIES_CATERPIE) { HP(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        MESSAGE("The wild Caterpie fainted!");
    } THEN {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_TOUGH), SELECTION_PREY_PRESSURE);
    }
}

WILD_BATTLE_TEST("Knocking out a foe adds no meat diet pressure to a herbivore")
{
    GIVEN {
        PLAYER(SPECIES_EOHIPPUS) { Moves(MOVE_SCRATCH); }
        OPPONENT(SPECIES_CATERPIE) { HP(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        MESSAGE("The wild Caterpie fainted!");
    } THEN {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_TOUGH), 0);
    }
}

WILD_BATTLE_TEST("A foe fainting from poison adds no meat diet pressure")
{
    GIVEN {
        PLAYER(SPECIES_HESPEROCYON);
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
        PLAYER(SPECIES_HESPEROCYON);
        OPPONENT(SPECIES_GEODUDE);
    } WHEN {
        TURN { MOVE(opponent, MOVE_MEMENTO); MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        MESSAGE("The wild Geodude fainted!");
    } THEN {
        EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_TOUGH), 0);
    }
}
