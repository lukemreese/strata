#include "global.h"
#include "strata_map.h"
#include "constants/map_groups.h"
#include "constants/rtc.h"

// Per-map Strata data: era, habitat and fixed lighting. The table is generated
// from tools/strata/maps/ (see gen_maps.py, write_map_info).

#include "data/strata_map_eras.h"

const struct StrataMapInfo *Strata_GetMapInfo(u16 map)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStrataMapInfo); i++)
    {
        if (sStrataMapInfo[i].map == map)
            return &sStrataMapInfo[i];
    }
    return NULL;
}

static const struct StrataMapInfo *GetCurrentMapInfo(void)
{
    return Strata_GetMapInfo((gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum);
}

u32 Strata_GetMapEra(void)
{
    const struct StrataMapInfo *info = GetCurrentMapInfo();
    return info != NULL ? info->era : ERA_COUNT;
}

enum SelectionPressure Strata_GetMapHabitat(void)
{
    const struct StrataMapInfo *info = GetCurrentMapInfo();
    return info != NULL ? info->habitat : PRESSURE_NONE;
}

enum StrataLight Strata_GetMapLight(void)
{
    const struct StrataMapInfo *info = GetCurrentMapInfo();
    return info != NULL ? info->light : STRATA_LIGHT_DNS;
}

// A fixed light is a fixed clock time for the day/night tint (UpdateTimeOfDay in
// src/overworld.c), so it blends exactly like the stock times of day.
bool32 Strata_GetLightTime(enum StrataLight light, s32 *hours, s32 *minutes)
{
    switch (light)
    {
    case STRATA_LIGHT_DAY:
        *hours = 12;
        *minutes = 0;
        return TRUE;
    case STRATA_LIGHT_DUSK: // Most of the way from day to the evening tint
        *hours = EVENING_HOUR_BEGIN;
        *minutes = 45;
        return TRUE;
    case STRATA_LIGHT_DARK:
        *hours = 0;
        *minutes = 0;
        return TRUE;
    case STRATA_LIGHT_ASH:  // Half the evening tint; the ash weather greys the rest
        *hours = EVENING_HOUR_BEGIN;
        *minutes = 30;
        return TRUE;
    default:
        return FALSE;
    }
}
