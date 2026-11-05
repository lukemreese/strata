#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "test/test.h"
#include "constants/vars.h"

// Lineage resilience (F7, docs/strata_outline.md §3.2): every era a lineage survives, each IV
// rises by RESILIENCE_IV_PER_ERA, plus RESILIENCE_STASIS_BONUS if the species did not change,
// capped at 31. Lepisosteus has no descent and survives up to Corral Bluffs; Cimolestes
// becomes Protictis on entering Corral Bluffs.

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

static void SetAllIVs(struct BoxPokemon *boxMon, u8 iv)
{
    u32 i;
    for (i = 0; i < NUM_STATS; i++)
        SetBoxMonData(boxMon, MON_DATA_HP_IV + i, &iv);
}

static void ExpectAllIVs(struct BoxPokemon *boxMon, u32 iv)
{
    u32 i;
    for (i = 0; i < NUM_STATS; i++)
        EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_HP_IV + i), iv);
}

static void CreatePartyMonWithIVs(struct Pokemon *mon, enum Species species, u32 level, u8 iv)
{
    CreateMon(mon, species, level, 0, OTID_STRUCT_PLAYER_ID);
    GiveMonInitialMoveset(mon);
    SetAllIVs(&mon->box, iv);
    CalculateMonStats(mon);
}

TEST("Lineage resilience: +3 per era survived, +1 more in stasis, capped at 31")
{
    EXPECT_EQ(Lineage_ResilientIV(15, TRUE), 15 + RESILIENCE_IV_PER_ERA);
    EXPECT_EQ(Lineage_ResilientIV(15, FALSE), 15 + RESILIENCE_IV_PER_ERA + RESILIENCE_STASIS_BONUS);
    EXPECT_EQ(Lineage_ResilientIV(0, TRUE), 3);
    EXPECT_EQ(Lineage_ResilientIV(0, FALSE), 4);
    EXPECT_EQ(Lineage_ResilientIV(29, TRUE), MAX_PER_STAT_IVS);
    EXPECT_EQ(Lineage_ResilientIV(31, FALSE), MAX_PER_STAT_IVS);
}

TEST("A party lineage in stasis gains resilience IVs on a load, with its stats recalculated")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    u32 oldAttack, attack;

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreatePartyMonWithIVs(mon, SPECIES_LEPISOSTEUS, 30, 10);
    oldAttack = GetMonData(mon, MON_DATA_ATK);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
    ExpectAllIVs(&mon->box, 10 + RESILIENCE_IV_PER_ERA + RESILIENCE_STASIS_BONUS);
    attack = GetMonData(mon, MON_DATA_ATK);
    EXPECT_GT(attack, oldAttack);
    // It was at full HP, so it still is, and the stats match a fresh recalculation.
    EXPECT_EQ(GetMonData(mon, MON_DATA_HP), GetMonData(mon, MON_DATA_MAX_HP));
    CalculateMonStats(mon);
    EXPECT_EQ(GetMonData(mon, MON_DATA_ATK), attack);
}

TEST("A lineage that descends gains the plain resilience raise")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreatePartyMonWithIVs(mon, SPECIES_CIMOLESTES, 20, 15);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_PROTICTIS);
    ExpectAllIVs(&mon->box, 15 + RESILIENCE_IV_PER_ERA);
}

TEST("A PC lineage gains resilience once per era of a multi-era jump, up to 31")
{
    struct BoxPokemon *boxMon = GetBoxedMonPtr(0, 0);
    struct BoxPokemon *strong = GetBoxedMonPtr(0, 1);

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    // A party mon, so the load doesn't bring the first PC gar out to fill an empty party.
    CreatePartyMonWithIVs(&gParties[B_TRAINER_PLAYER][0], SPECIES_LEPISOSTEUS, 20, 15);
    CreateBoxMon(boxMon, SPECIES_LEPISOSTEUS, 20, 0, OTID_STRUCT_PLAYER_ID);
    SetAllIVs(boxMon, 10);
    CreateBoxMon(strong, SPECIES_LEPISOSTEUS, 20, 0, OTID_STRUCT_PLAYER_ID);
    SetAllIVs(strong, 28);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);   // the impact winter, then Corral Bluffs

    ExpectAllIVs(boxMon, 10 + 2 * (RESILIENCE_IV_PER_ERA + RESILIENCE_STASIS_BONUS));
    ExpectAllIVs(strong, MAX_PER_STAT_IVS);
}

TEST("A lineage that stays in its era gains no resilience")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_CORRAL_BLUFFS);
    CreatePartyMonWithIVs(mon, SPECIES_LEPISOSTEUS, 30, 10);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);   // re-entering the same layer

    ExpectAllIVs(&mon->box, 10);
}
