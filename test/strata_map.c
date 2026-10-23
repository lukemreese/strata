#include "global.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "overworld.h"
#include "selection.h"
#include "strata_map.h"
#include "test/test.h"
#include "constants/map_groups.h"
#include "constants/map_types.h"
#include "constants/metatile_behaviors.h"
#include "constants/rtc.h"
#include "constants/strata.h"
#include "constants/vars.h"
#include "../src/data/strata_map_eras.h"

// Per-map habitat and light tags (R4, F6): `habitat=`/`light=` in tools/strata/maps/,
// generated into sStrataMapInfo (src/strata_map.c).

static void SetMap(u16 map)
{
    gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(map);
    gSaveBlock1Ptr->location.mapNum = MAP_NUM(map);
}

TEST("Every deep-time map has a fixed light and a valid habitat")
{
    u32 i;
    const struct StrataMapInfo *info = NULL;
    for (i = 0; i < ARRAY_COUNT(sStrataMapInfo); i++)
        PARAMETRIZE { info = &sStrataMapInfo[i]; }

    EXPECT(info->habitat == PRESSURE_FOREST || info->habitat == PRESSURE_OPEN
        || info->habitat == PRESSURE_WATER || info->habitat == PRESSURE_NONE);
    EXPECT_LT(info->light, STRATA_LIGHT_COUNT);
    EXPECT(info->era <= ERA_COUNT);
    if (info->era != ERA_COUNT && info->era != ERA_PRESENT_DIG && info->era != ERA_EPILOGUE)
        EXPECT_NE(info->light, STRATA_LIGHT_DNS);
    // (The test has its own copy of the static table, so compare contents.)
    EXPECT(Strata_GetMapInfo(info->map) != NULL);
    EXPECT_EQ(Strata_GetMapInfo(info->map)->era, info->era);
    EXPECT_EQ(Strata_GetMapInfo(info->map)->habitat, info->habitat);
    EXPECT_EQ(Strata_GetMapInfo(info->map)->light, info->light);
}

TEST("Map tags: habitats and lights of the existing maps")
{
    SetMap(MAP_STRATA_PALM_FOREST);  // A Petalburg Woods crop, so audit item A6
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_FOREST);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_DAY);
    SetMap(MAP_STRATA_LEVEE);
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_FOREST);
    SetMap(MAP_STRATA_RIVER);
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_WATER);
    SetMap(MAP_STRATA_LEVEE_WINTER);   // Impact winter: dead forest, soot-dark sky
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_OPEN);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_DARK);
    SetMap(MAP_STRATA_GRASSLAND);      // Act 7 before the ash: clear day
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_OPEN);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_DAY);
    SetMap(MAP_STRATA_GRASSLAND_ASH);  // and after it
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_OPEN);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_ASH);
    SetMap(MAP_STRATA_TRAP_CAVE);
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_NONE);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_NONE);
    SetMap(MAP_STRATA_FIELD_CAMP);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_DNS);
    EXPECT_EQ(Strata_GetMapEra(), ERA_COUNT);
}

TEST("Stock maps have no Strata tags (the Petalburg Woods placeholder is gone)")
{
    EXPECT(Strata_GetMapInfo(MAP_PETALBURG_WOODS) == NULL);
    SetMap(MAP_PETALBURG_WOODS);
    EXPECT_EQ(Strata_GetMapHabitat(), PRESSURE_NONE);
    EXPECT_EQ(Strata_GetMapLight(), STRATA_LIGHT_DNS);
    EXPECT_EQ(Strata_GetMapEra(), ERA_COUNT);
}

TEST("A map's habitat wins over the grass underfoot, but water wins over both")
{
    u8 savedFlags = gPlayerAvatar.flags;
    gPlayerAvatar.flags = 0;

    SetMap(MAP_STRATA_PALM_FOREST);
    EXPECT_EQ(Selection_GetHabitat(MB_NORMAL, FALSE), PRESSURE_FOREST);
    EXPECT_EQ(Selection_GetHabitat(MB_TALL_GRASS, FALSE), PRESSURE_FOREST);
    EXPECT_EQ(Selection_GetHabitat(MB_NORMAL, TRUE), PRESSURE_WATER);
    EXPECT_EQ(Selection_GetHabitat(MB_POND_WATER, FALSE), PRESSURE_WATER);

    SetMap(MAP_STRATA_TRAP_CAVE);   // Untagged: the grass decides
    EXPECT_EQ(Selection_GetHabitat(MB_NORMAL, FALSE), PRESSURE_NONE);
    EXPECT_EQ(Selection_GetHabitat(MB_TALL_GRASS, FALSE), PRESSURE_OPEN);
    EXPECT_EQ(Selection_GetHabitat(MB_LONG_GRASS, FALSE), PRESSURE_FOREST);

    gPlayerAvatar.flags = savedFlags;
}

// The party's pressures after `ticks` ticks' worth of steps on `map`, on `behavior`.
static void WalkOn(u16 map, u16 behavior, u32 ticks)
{
    u8 savedFlags = gPlayerAvatar.flags;
    const struct MapLayout *savedLayout = gMapHeader.mapLayout;
    u32 i;

    ZeroPlayerPartyMons();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_CIMOLESTES, 5, 0, OTID_STRUCT_PLAYER_ID);
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);   // No heat
    VarSet(VAR_STRATA_SELECTION_STEPS, 0);
    SetMap(map);
    gPlayerAvatar.flags = PLAYER_AVATAR_FLAG_ON_FOOT;
    gMapHeader.mapLayout = NULL;   // No map loaded: no shore
    for (i = 0; i < SELECTION_STEPS_PER_TICK * ticks; i++)
        Selection_UpdateStepCounter(behavior);
    gMapHeader.mapLayout = savedLayout;
    gPlayerAvatar.flags = savedFlags;
}

TEST("Steps on a forest map add forest pressure to the whole party")
{
    WalkOn(MAP_STRATA_LAKE_FOREST, MB_NORMAL, 3);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_COOL), 3);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_COOL), 3);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_BEAUTY), 0);
}

TEST("Steps on an open map add open pressure, even off the grass")
{
    WalkOn(MAP_STRATA_STEPPE, MB_NORMAL, 2);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_BEAUTY), 2);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_COOL), 0);
}

TEST("Steps on a water map add water pressure on land")
{
    WalkOn(MAP_STRATA_RIVER, MB_NORMAL, 2);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_CUTE), 2);
}

TEST("Steps on an untagged map's bare ground add no habitat pressure")
{
    u32 i;
    u8 pressures[PRESSURE_COUNT];

    WalkOn(MAP_STRATA_FIELD_CAMP, MB_NORMAL, 2);
    Selection_GetBoxMonPressures(&gParties[B_TRAINER_PLAYER][0].box, pressures);
    for (i = 0; i < PRESSURE_COUNT; i++)
        EXPECT_EQ(pressures[i], 0);
}

TEST("Fixed lights show as fixed clock times; the wall clock and caves have none")
{
    s32 hours = -1, minutes = -1;

    EXPECT(Strata_GetLightTime(STRATA_LIGHT_DAY, &hours, &minutes));
    EXPECT_EQ(hours, 12);
    EXPECT(Strata_GetLightTime(STRATA_LIGHT_DARK, &hours, &minutes));
    EXPECT(hours >= NIGHT_HOUR_BEGIN || hours < NIGHT_HOUR_END);
    EXPECT(Strata_GetLightTime(STRATA_LIGHT_DUSK, &hours, &minutes));
    EXPECT(hours >= EVENING_HOUR_BEGIN && hours < EVENING_HOUR_END);
    EXPECT(Strata_GetLightTime(STRATA_LIGHT_ASH, &hours, &minutes));
    EXPECT(hours >= EVENING_HOUR_BEGIN && hours < EVENING_HOUR_END);
    EXPECT(!Strata_GetLightTime(STRATA_LIGHT_DNS, &hours, &minutes));
    EXPECT(!Strata_GetLightTime(STRATA_LIGHT_NONE, &hours, &minutes));
}

TEST("Deep-time maps take their time of day from their light, not the clock")
{
    SetMap(MAP_STRATA_LEVEE);
    UpdateTimeOfDay(TRUE);
    EXPECT_EQ(gTimeOfDay, TIME_DAY);
    SetMap(MAP_STRATA_LEVEE_WINTER);
    UpdateTimeOfDay(TRUE);
    EXPECT_EQ(gTimeOfDay, TIME_NIGHT);
    SetMap(MAP_STRATA_GRASSLAND);
    UpdateTimeOfDay(TRUE);
    EXPECT_EQ(gTimeOfDay, TIME_DAY);
    SetMap(MAP_STRATA_GRASSLAND_ASH);
    UpdateTimeOfDay(TRUE);
    EXPECT_EQ(gTimeOfDay, TIME_EVENING);
}

TEST("Maps with light=none are never tinted")
{
    SetMap(MAP_STRATA_TRAP_CAVE);
    EXPECT(!MapHasNaturalLight(MAP_TYPE_ROUTE));
    SetMap(MAP_STRATA_LEVEE);
    EXPECT_EQ(MapHasNaturalLight(MAP_TYPE_ROUTE), OW_ENABLE_DNS);
}
