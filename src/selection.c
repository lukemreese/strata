#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "item.h"
#include "item_use.h"
#include "metatile_behavior.h"
#include "pokemon.h"
#include "selection.h"
#include "strata_map.h"
#include "constants/items.h"
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

// Adds `amount`, but never takes the counter above `cap`. A counter already at or
// above the cap (from other sources) is left alone.
void Selection_AddPressureUpTo(struct Pokemon *mon, enum SelectionPressure pressure, u32 amount, u32 cap)
{
    u32 value, old;

    if (pressure >= PRESSURE_COUNT || amount == 0
     || !GetMonData(mon, MON_DATA_SANITY_HAS_SPECIES) || GetMonData(mon, MON_DATA_IS_EGG))
        return;

    if (cap > 255)
        cap = 255;
    old = GetMonData(mon, sPressureDataIds[pressure]);
    if (old >= cap)
        return;
    value = old + amount;
    if (value > cap)
        value = cap;
    SetMonData(mon, sPressureDataIds[pressure], &value);
}

// Saturates at 255.
void Selection_AddPressure(struct Pokemon *mon, enum SelectionPressure pressure, u32 amount)
{
    Selection_AddPressureUpTo(mon, pressure, amount, 255);
}

#include "data/strata_diets.h"

enum StrataDiet Selection_GetSpeciesDiet(enum Species species)
{
    if (species >= NUM_SPECIES)
        return DIET_HERBIVORE;
    return sSpeciesDiets[species];
}

bool32 Selection_EatsAnimals(enum Species species)
{
    return Selection_GetSpeciesDiet(species) != DIET_HERBIVORE;
}

// TRUE if the player stands on land orthogonally next to surfable water: a shore,
// bank or lake edge. FALSE with no map loaded (in tests).
static bool32 IsPlayerOnShore(void)
{
    static const s8 sOffsets[][2] = { {0, -1}, {0, 1}, {-1, 0}, {1, 0} };
    s16 x, y;
    u32 i;

    if (gMapHeader.mapLayout == NULL)
        return FALSE;
    PlayerGetDestCoords(&x, &y);
    for (i = 0; i < ARRAY_COUNT(sOffsets); i++)
    {
        if (MetatileBehavior_IsSurfableFishableWater(MapGridGetMetatileBehaviorAt(x + sOffsets[i][0], y + sOffsets[i][1])))
            return TRUE;
    }
    return FALSE;
}

// Habitat the player is in, or PRESSURE_NONE for neutral ground (paths, towns).
// Water wins over the map's habitat: a lake in a forest is still a lake, and so
// is its shore (`onShore`: standing next to surfable water). Wading (waders)
// is surfing as far as the game is concerned. Then the map's `habitat=` tag
// (Strata_GetMapHabitat, generated from tools/strata/maps/), and on untagged maps
// the grass underfoot.
enum SelectionPressure Selection_GetHabitat(u32 metatileBehavior, bool32 onShore)
{
    enum SelectionPressure habitat;

    if (TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING | PLAYER_AVATAR_FLAG_UNDERWATER)
     || MetatileBehavior_IsSurfableWaterOrUnderwater(metatileBehavior)
     || onShore)
        return PRESSURE_WATER;

    habitat = Strata_GetMapHabitat();
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
    bool32 onShore;

    if (++(*steps) < SELECTION_STEPS_PER_TICK)
        return;
    *steps = 0;
    // The shore check reads the map, so skip it when the answer is already water.
    onShore = !TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING | PLAYER_AVATAR_FLAG_UNDERWATER)
           && !MetatileBehavior_IsSurfableWaterOrUnderwater(metatileBehavior)
           && IsPlayerOnShore();
    Selection_ApplyTick(Selection_GetHabitat(metatileBehavior, onShore), era < ERA_COUNT ? sEraHeat[era] : 0);
}

// A party mon took prey. Only animal eaters count it, and knockouts alone can't
// lift PRESSURE_MEAT_DIET past SELECTION_PREY_CAP: a branch steered by diet needs
// animal forage (carrion, larvae) on top. Storage: the save has no spare per-mon
// field to count knockouts per era, so the cap is on the counter itself. It
// resets on descent, and every diet-steered descent (Hesperocyon, Leptocyon) has
// a one-era window, so this is 24 per era wherever it matters.
void Selection_OnPreyTaken(struct Pokemon *mon)
{
    if (!Selection_EatsAnimals(GetMonData(mon, MON_DATA_SPECIES)))
        return;
    Selection_AddPressureUpTo(mon, PRESSURE_MEAT_DIET, SELECTION_PREY_PRESSURE, SELECTION_PREY_CAP);
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

    Selection_OnPreyTaken(GetBattlerMon(gBattlerAttacker));
}

// A fish took the hook (called as the fishing encounter starts): the whole party
// has been at the water's edge.
void Selection_OnFishHooked(void)
{
    u32 i;
    for (i = 0; i < PARTY_SIZE; i++)
        Selection_AddPressure(&gParties[B_TRAINER_PLAYER][i], PRESSURE_WATER, SELECTION_FISH_PRESSURE);
}

// Forage items (ITEM_FERN_FROND ... ITEM_CARRION, src/data/items.h): food found in
// the field. The item's secondaryId is the pressure it adds (PRESSURE_PLANT_DIET or
// PRESSURE_MEAT_DIET), its holdEffectParam the HP it heals.
//
// Forage is placed as hidden items whose flags are temp flags, so it regrows on every
// map load (tools/strata/maps/common.py, forage()). Hidden items store their flag as a
// 13-bit offset that wraps (GET_HIDDEN_ITEM_FLAG), which needs every flag ID to fit.
STATIC_ASSERT(FLAGS_COUNT <= (1 << 13), HiddenItemFlagsFitIn13Bits);
bool32 Selection_IsForage(enum Item item)
{
    return item < ITEMS_COUNT && GetItemFieldFunc(item) == ItemUseOutOfBattle_StrataForage;
}

// Any conscious mon can eat, even at full HP: the diet is the point, the HP a bonus.
bool32 Selection_CanEatForage(struct Pokemon *mon)
{
    return GetMonData(mon, MON_DATA_SANITY_HAS_SPECIES)
        && !GetMonData(mon, MON_DATA_IS_EGG)
        && GetMonData(mon, MON_DATA_HP) != 0;
}

// `mon` eats one `item`: adds FORAGE_PRESSURE of its pressure and heals it. Returns
// the HP healed (0 at full HP). Doesn't take the item from the bag. Does nothing
// (returns 0) if the mon can't eat or `item` isn't forage.
u32 Selection_EatForage(struct Pokemon *mon, enum Item item)
{
    u32 hp, maxHP, heal;

    if (!Selection_IsForage(item) || !Selection_CanEatForage(mon))
        return 0;

    Selection_AddPressure(mon, GetItemSecondaryId(item), FORAGE_PRESSURE);
    hp = GetMonData(mon, MON_DATA_HP);
    maxHP = GetMonData(mon, MON_DATA_MAX_HP);
    heal = GetItemHoldEffectParam(item);
    if (heal > maxHP - hp)
        heal = maxHP - hp;
    hp += heal;
    SetMonData(mon, MON_DATA_HP, &hp);
    return heal;
}

// special Strata_AddPressure
// Input: VAR_0x8004 = party slot, VAR_0x8005 = enum SelectionPressure, VAR_0x8006 = amount
void Strata_AddPressure(void)
{
    if (gSpecialVar_0x8004 < PARTY_SIZE)
        Selection_AddPressure(&gParties[B_TRAINER_PLAYER][gSpecialVar_0x8004], gSpecialVar_0x8005, gSpecialVar_0x8006);
}
