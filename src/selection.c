#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "metatile_behavior.h"
#include "pokemon.h"
#include "selection.h"
#include "constants/map_groups.h"
#include "constants/vars.h"

// Selection pressures: hidden per-mon counters that decide which descendant a
// lineage becomes at the next era jump (see src/lineage.c). They rise with where
// the party lives, the era's climate, and what the party eats.

// Contest stats are unused in Strata, so they hold the pressure counters.
static const u8 sPressureDataIds[PRESSURE_COUNT] =
{
    [PRESSURE_FOREST]     = MON_DATA_COOL,
    [PRESSURE_OPEN]       = MON_DATA_BEAUTY,
    [PRESSURE_WATER]      = MON_DATA_CUTE,
    [PRESSURE_PLANT_DIET] = MON_DATA_SMART,
    [PRESSURE_MEAT_DIET]  = MON_DATA_TOUGH,
    [PRESSURE_HEAT]       = MON_DATA_SHEEN,
};

// PRESSURE_HEAT gained per tick in each era, from its global climate.
static const u8 sEraHeat[ERA_COUNT] =
{
    [ERA_PRESENT_DIG]   = 0,
    [ERA_HELL_CREEK]    = 1, // Warm-temperate to subtropical coastal plain
    [ERA_IMPACT_WINTER] = 0, // Sunlight blocked by impact debris
    [ERA_CORRAL_BLUFFS] = 1, // Warm, humid early Paleocene
    [ERA_BIGHORN_PETM]  = 2, // Paleocene-Eocene Thermal Maximum: ~5-8 °C global warming
    [ERA_GREEN_RIVER]   = 1, // Early Eocene climatic optimum winding down
    [ERA_WHITE_RIVER]   = 0, // Eocene-Oligocene cooling
    [ERA_ASHFALL]       = 0, // Cooling after the mid-Miocene optimum
    [ERA_TRAP_CAVE]     = 0, // Last Glacial Maximum
    [ERA_EPILOGUE]      = 0,
};

// Maps whose habitat isn't evident from their metatiles.
// PLACEHOLDER: replace with Strata maps as they're built.
static const struct
{
    u16 map;
    u8 habitat; // enum SelectionPressure
} sMapHabitats[] =
{
    { MAP_PETALBURG_WOODS, PRESSURE_FOREST },
};

void Selection_GetBoxMonPressures(struct BoxPokemon *boxMon, u8 *pressures)
{
    u32 i;
    for (i = 0; i < PRESSURE_COUNT; i++)
        pressures[i] = GetBoxMonData(boxMon, sPressureDataIds[i]);
}

void Selection_ResetBoxMonPressures(struct BoxPokemon *boxMon)
{
    u32 i;
    u8 zero = 0;
    for (i = 0; i < PRESSURE_COUNT; i++)
        SetBoxMonData(boxMon, sPressureDataIds[i], &zero);
}

// Saturates at 255.
void Selection_AddPressure(struct Pokemon *mon, enum SelectionPressure pressure, u32 amount)
{
    u32 value;

    if (pressure >= PRESSURE_COUNT || amount == 0
     || !GetMonData(mon, MON_DATA_SANITY_HAS_SPECIES) || GetMonData(mon, MON_DATA_IS_EGG))
        return;

    value = GetMonData(mon, sPressureDataIds[pressure]) + amount;
    if (value > 255)
        value = 255;
    SetMonData(mon, sPressureDataIds[pressure], &value);
}

static enum SelectionPressure GetMapHabitat(void)
{
    u32 i;
    u32 map = gSaveBlock1Ptr->location.mapNum | (gSaveBlock1Ptr->location.mapGroup << 8);

    for (i = 0; i < ARRAY_COUNT(sMapHabitats); i++)
    {
        if (sMapHabitats[i].map == map)
            return sMapHabitats[i].habitat;
    }
    return PRESSURE_NONE;
}

// Habitat the player is in, or PRESSURE_NONE for neutral ground (paths, towns).
// Water wins over the map's habitat: a lake in a forest is still a lake.
enum SelectionPressure Selection_GetHabitat(u32 metatileBehavior)
{
    enum SelectionPressure habitat;

    if (TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING | PLAYER_AVATAR_FLAG_UNDERWATER)
     || MetatileBehavior_IsSurfableWaterOrUnderwater(metatileBehavior))
        return PRESSURE_WATER;

    habitat = GetMapHabitat();
    if (habitat != PRESSURE_NONE)
        return habitat;

    if (MetatileBehavior_IsLongGrass(metatileBehavior))
        return PRESSURE_FOREST; // Dense cover
    if (MetatileBehavior_IsTallGrass(metatileBehavior))
        return PRESSURE_OPEN;
    return PRESSURE_NONE;
}

void Selection_ApplyTick(enum SelectionPressure habitat, u32 heat)
{
    u32 i;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        Selection_AddPressure(&gParties[B_TRAINER_PLAYER][i], habitat, 1);
        Selection_AddPressure(&gParties[B_TRAINER_PLAYER][i], PRESSURE_HEAT, heat);
    }
}

void Selection_UpdateStepCounter(u16 metatileBehavior)
{
    u16 *steps = GetVarPointer(VAR_STRATA_SELECTION_STEPS);
    u32 era = VarGet(VAR_STRATA_ERA);

    if (++(*steps) < SELECTION_STEPS_PER_TICK)
        return;
    *steps = 0;
    Selection_ApplyTick(Selection_GetHabitat(metatileBehavior), era < ERA_COUNT ? sEraHeat[era] : 0);
}

// Called when a foe faints. If one of the player's mons knocked it out with a
// move, that counts as prey taken. Faints are resolved after the move ends, but
// gBattlerAttacker/gBattlerTarget still describe it; self-inflicted and
// end-of-turn damage make the fainting foe the attacker, so they don't count.
void Selection_OnFoeFainted(u32 battler)
{
    if (gBattlerTarget != battler
     || !IsOnPlayerSide(gBattlerAttacker)
     || GetBattlerParty(gBattlerAttacker) != gParties[B_TRAINER_PLAYER])
        return;

    Selection_AddPressure(GetBattlerMon(gBattlerAttacker), PRESSURE_MEAT_DIET, SELECTION_PREY_PRESSURE);
}

// special Strata_AddPressure
// Input: VAR_0x8004 = party slot, VAR_0x8005 = enum SelectionPressure, VAR_0x8006 = amount
void Strata_AddPressure(void)
{
    if (gSpecialVar_0x8004 < PARTY_SIZE)
        Selection_AddPressure(&gParties[B_TRAINER_PLAYER][gSpecialVar_0x8004], gSpecialVar_0x8005, gSpecialVar_0x8006);
}
