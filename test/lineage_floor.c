#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "move.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "test/test.h"
#include "constants/vars.h"

// Era level floor tests. These use the floors and learnsets in src/data, so they
// check levels against Lineage_GetEraLevelFloor rather than hard-coded numbers.
// Lepisosteus and Mesodma have no descents up to Corral Bluffs and survive it.

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

// CreateMon/CreateBoxMon alone give no moves or stats; these give a mon as the
// player would have it.
static void CreatePartyMon(struct Pokemon *mon, enum Species species, u32 level)
{
    CreateMon(mon, species, level, 0, OTID_STRUCT_PLAYER_ID);
    GiveMonInitialMoveset(mon);
    CalculateMonStats(mon);
}

static void CreateStoredMon(struct BoxPokemon *boxMon, enum Species species, u32 level)
{
    CreateBoxMon(boxMon, species, level, 0, OTID_STRUCT_PLAYER_ID);
    GiveBoxMonInitialMoveset(boxMon);
}

static u32 ExpForLevel(enum Species species, u32 level)
{
    return gExperienceTables[gSpeciesInfo[species].growthRate][level];
}

TEST("Era level floors never go down from one era to the next")
{
    u32 era;
    EXPECT_EQ(Lineage_GetEraLevelFloor(ERA_PRESENT_DIG), 0);
    EXPECT_EQ(Lineage_GetEraLevelFloor(ERA_HELL_CREEK), 0);
    for (era = ERA_HELL_CREEK; era < ERA_COUNT; era++)
        EXPECT_GE(Lineage_GetEraLevelFloor(era), Lineage_GetEraLevelFloor(era - 1));
}

TEST("The era level floor raises a party mon with matching EXP and stats")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    u32 floor = Lineage_GetEraLevelFloor(ERA_CORRAL_BLUFFS);
    u32 oldMaxHp, maxHp, attack;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreatePartyMon(mon, SPECIES_LEPISOSTEUS, 5);
    oldMaxHp = GetMonData(mon, MON_DATA_MAX_HP);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
    EXPECT_EQ(GetMonData(mon, MON_DATA_LEVEL), floor);
    EXPECT_EQ(GetMonData(mon, MON_DATA_EXP), ExpForLevel(SPECIES_LEPISOSTEUS, floor));
    maxHp = GetMonData(mon, MON_DATA_MAX_HP);
    attack = GetMonData(mon, MON_DATA_ATK);
    EXPECT_GT(maxHp, oldMaxHp);
    // It was at full HP, so it still is.
    EXPECT_EQ(GetMonData(mon, MON_DATA_HP), maxHp);
    // The stats must match a fresh recalculation at the new level.
    CalculateMonStats(mon);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MAX_HP), maxHp);
    EXPECT_EQ(GetMonData(mon, MON_DATA_ATK), attack);
}

TEST("The era level floor teaches the level-up moves passed on the way")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    // Knows Peck and Water Gun; Aqua Jet comes at 6, Bite at 12.
    CreatePartyMon(mon, SPECIES_LEPISOSTEUS, 5);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE1), MOVE_PECK);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE2), MOVE_WATER_GUN);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE3), MOVE_AQUA_JET);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE4), MOVE_BITE);
    EXPECT_EQ(GetMonData(mon, MON_DATA_PP4), GetMovePP(MOVE_BITE));
}

TEST("The era level floor forgets the oldest move when full and skips known moves")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    // Knows Tackle and Tail Whip, plus Bite early. Passes Quick Attack (4),
    // Bullet Seed (7) and Bite (10) on the way to 12.
    CreatePartyMon(mon, SPECIES_MESODMA, 3);
    SetMonMoveSlot(mon, MOVE_BITE, 2);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE1), MOVE_TAIL_WHIP);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE2), MOVE_BITE);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE3), MOVE_QUICK_ATTACK);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE4), MOVE_BULLET_SEED);
}

TEST("The era level floor raises a mon stored in the PC")
{
    struct BoxPokemon *boxMon = GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, IN_BOX_COUNT - 1);
    struct Pokemon mon;
    u32 floor = Lineage_GetEraLevelFloor(ERA_CORRAL_BLUFFS);

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    // A party mon, so the PC gar isn't brought out to fill an empty party.
    CreatePartyMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_LEPISOSTEUS, 30);
    CreateStoredMon(boxMon, SPECIES_LEPISOSTEUS, 5);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetLevelFromBoxMonExp(boxMon), floor);
    EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_EXP), ExpForLevel(SPECIES_LEPISOSTEUS, floor));
    EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_MOVE4), MOVE_BITE);

    // Withdrawn, it has the stats of its new level and full HP.
    BoxMonToMon(boxMon, &mon);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_LEVEL), floor);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), GetMonData(&mon, MON_DATA_MAX_HP));
    ZeroBoxMonData(boxMon);
}

TEST("The era level floor leaves mons at or above it untouched")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    struct Pokemon *atFloor = &gParties[B_TRAINER_PLAYER][1];
    u32 floor = Lineage_GetEraLevelFloor(ERA_CORRAL_BLUFFS);
    u32 exp = ExpForLevel(SPECIES_LEPISOSTEUS, 20) + 5;
    u32 hp = 3;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreatePartyMon(mon, SPECIES_LEPISOSTEUS, 20);
    SetMonData(mon, MON_DATA_EXP, &exp);
    SetMonData(mon, MON_DATA_HP, &hp);
    CreatePartyMon(atFloor, SPECIES_LEPISOSTEUS, floor);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_LEVEL), 20);
    EXPECT_EQ(GetMonData(mon, MON_DATA_EXP), exp);
    EXPECT_EQ(GetMonData(mon, MON_DATA_HP), hp);
    EXPECT_EQ(GetMonData(atFloor, MON_DATA_LEVEL), floor);
    EXPECT_EQ(GetMonData(atFloor, MON_DATA_EXP), ExpForLevel(SPECIES_LEPISOSTEUS, floor));
}

TEST("The era level floor raises a fainted mon but leaves it fainted")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    u32 hp = 0;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreatePartyMon(mon, SPECIES_LEPISOSTEUS, 5);
    SetMonData(mon, MON_DATA_HP, &hp);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_LEVEL), Lineage_GetEraLevelFloor(ERA_CORRAL_BLUFFS));
    EXPECT_EQ(GetMonData(mon, MON_DATA_HP), 0);
}

TEST("The era level floor skips eggs")
{
    struct BoxPokemon *boxMon = GetBoxedMonPtr(0, 0);
    bool32 isEgg = TRUE;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreatePartyMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_LEPISOSTEUS, 30);
    CreateStoredMon(boxMon, SPECIES_LEPISOSTEUS, 5);
    SetBoxMonData(boxMon, MON_DATA_IS_EGG, &isEgg);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetLevelFromBoxMonExp(boxMon), 5);
    ZeroBoxMonData(boxMon);
}

TEST("A multi-era jump raises mons to the floor of the last era, learning moves on the way")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    u32 floor = Lineage_GetEraLevelFloor(ERA_BIGHORN_PETM);

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreatePartyMon(mon, SPECIES_LEPISOSTEUS, 5);

    Lineage_AdvanceToEra(ERA_BIGHORN_PETM);

    EXPECT_EQ(GetMonData(mon, MON_DATA_LEVEL), floor);
    EXPECT_EQ(GetMonData(mon, MON_DATA_EXP), ExpForLevel(SPECIES_LEPISOSTEUS, floor));
    // Aqua Jet (6) and Bite (12) fill the slots, then Harden (18) pushes out Peck.
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE1), MOVE_WATER_GUN);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE2), MOVE_AQUA_JET);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE3), MOVE_BITE);
    EXPECT_EQ(GetMonData(mon, MON_DATA_MOVE4), MOVE_HARDEN);
}

TEST("A lineage descending during a multi-era jump is raised to each floor in turn")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    // Cimolestes -> Protictis (Corral Bluffs) -> Miacis (Green River) -> Hesperocyon (White River)
    CreatePartyMon(mon, SPECIES_CIMOLESTES, 5);

    Lineage_AdvanceToEra(ERA_WHITE_RIVER);

    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_HESPEROCYON);
    EXPECT_EQ(GetMonData(mon, MON_DATA_LEVEL), Lineage_GetEraLevelFloor(ERA_WHITE_RIVER));
    EXPECT_EQ(GetMonData(mon, MON_DATA_EXP), ExpForLevel(SPECIES_HESPEROCYON, Lineage_GetEraLevelFloor(ERA_WHITE_RIVER)));
}

TEST("The survivor gift joins at the old level when the era's floor is lower")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreatePartyMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TYRANNOSAUR, 12);

    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);

    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_MESODMA);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_LEVEL), 10);
}

TEST("The survivor gift joins at the era's floor, as a species still alive then")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_WHITE_RIVER);
    // Archaeotherium dies out at Ashfall. Mesodma died out at White River, before.
    CreatePartyMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_ARCHAEOTHERE, 40);

    Lineage_AdvanceToEra(ERA_ASHFALL);

    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_LEVEL), Lineage_GetEraLevelFloor(ERA_ASHFALL));
    // ...ready to fight: its moves for that level, and full HP.
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_MOVE4), MOVE_LIQUIDATION);
    EXPECT_GT(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_MAX_HP), 0);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_HP), GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_MAX_HP));
}
