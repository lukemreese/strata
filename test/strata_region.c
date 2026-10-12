#include "global.h"
#include "event_data.h"
#include "overworld.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/map_groups.h"
#include "constants/strata.h"
#include "constants/vars.h"

// Checks for the Strata region (tools/strata/maps.py, data/maps/Strata*).

extern const u8 StrataFieldStation_EventScript_FirstEntry[];

static const u16 sStrataMaps[] =
{
    MAP_STRATA_FIELD_CAMP,
    MAP_STRATA_FIELD_STATION,
    MAP_STRATA_BADLANDS,
    MAP_STRATA_LEVEE,
    MAP_STRATA_RIVER,
    MAP_STRATA_BACKSWAMP,
};

static u32 OppositeDirection(u32 direction)
{
    switch (direction)
    {
    case CONNECTION_NORTH: return CONNECTION_SOUTH;
    case CONNECTION_SOUTH: return CONNECTION_NORTH;
    case CONNECTION_EAST:  return CONNECTION_WEST;
    case CONNECTION_WEST:  return CONNECTION_EAST;
    default:               return direction;
    }
}

TEST("The rig's first trip moves the world and the story to Hell Creek")
{
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    VarSet(VAR_STRATA_STORY, 1);
    RUN_OVERWORLD_SCRIPT(
        call StrataFieldStation_EventScript_FirstEntry;
    );
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_HELL_CREEK);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), 2);
}

TEST("Strata map connections lead back the way they came")
{
    u32 i, j, k;
    u16 map = 0;
    for (i = 0; i < ARRAY_COUNT(sStrataMaps); i++)
    {
        PARAMETRIZE { map = sStrataMaps[i]; }
    }

    const struct MapHeader *header = Overworld_GetMapHeaderByGroupAndId(MAP_GROUP(map), MAP_NUM(map));
    if (header->connections == NULL)
        return;
    for (j = 0; j < header->connections->count; j++)
    {
        const struct MapConnection *out = &header->connections->connections[j];
        const struct MapHeader *dest = Overworld_GetMapHeaderByGroupAndId(out->mapGroup, out->mapNum);
        bool32 found = FALSE;
        EXPECT(dest->connections != NULL);
        for (k = 0; k < dest->connections->count; k++)
        {
            const struct MapConnection *back = &dest->connections->connections[k];
            if (back->mapGroup == MAP_GROUP(map) && back->mapNum == MAP_NUM(map)
             && back->direction == OppositeDirection(out->direction)
             && back->offset == -out->offset)
                found = TRUE;
        }
        EXPECT(found);
    }
}
