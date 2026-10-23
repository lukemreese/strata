#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "overworld.h"
#include "string_util.h"
#include "strata_acts.h"
#include "wild_encounter.h"
#include "test/overworld_script.h"
#include "test/battle.h"
#include "test/test.h"
#include "constants/map_groups.h"
#include "constants/strata.h"
#include "constants/vars.h"
#include "../src/data/strata_map_eras.h"

// Checks for the Strata region (tools/strata/maps.py, data/maps/Strata*).

static const u16 sStrataMaps[] =
{
    MAP_STRATA_FIELD_CAMP,
    MAP_STRATA_FIELD_STATION,
    MAP_STRATA_BADLANDS,
    MAP_STRATA_JORDAN,
    MAP_STRATA_JORDAN_STORE,
    MAP_STRATA_JORDAN_CAFE,
    MAP_STRATA_BLM_OFFICE,
    MAP_STRATA_LINDQVIST_RANCH,
    MAP_STRATA_SAND_ARROYO,
    MAP_STRATA_LEVEE,
    MAP_STRATA_RIVER,
    MAP_STRATA_BACKSWAMP,
    MAP_STRATA_LEVEE_WINTER,
    MAP_STRATA_RIVER_WINTER,
    MAP_STRATA_BACKSWAMP_WINTER,
    MAP_STRATA_PALM_FOREST,
    MAP_STRATA_RED_BEDS,
    MAP_STRATA_LAKE_FOREST,
    MAP_STRATA_WHITE_RIVER,
    MAP_STRATA_GRASSLAND,
    MAP_STRATA_STEPPE,
    MAP_STRATA_TRAP_CAVE,
    MAP_STRATA_PRAIRIE,
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
        special Strata_RigLoadNext;
    );
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_HELL_CREEK);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_IN_ACT(ERA_HELL_CREEK));
}

TEST("The rig only loads the next layer once the act is done")
{
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_GREEN_RIVER));
    EXPECT_EQ(Strata_GetRigState(), RIG_REENTER);
    Strata_RigLoadNext();
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_GREEN_RIVER);
    EXPECT_EQ(VarGet(VAR_STRATA_STORY), STORY_IN_ACT(ERA_GREEN_RIVER));
}

TEST("Each finished act lets the rig load the next, up to today")
{
    u32 act;

    ZeroPlayerPartyMons();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 5, 0, OTID_STRUCT_PLAYER_ID);
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    VarSet(VAR_STRATA_STORY, 1);
    EXPECT_EQ(Strata_GetRigState(), RIG_FIRST);
    Strata_RigLoadNext();
    for (act = ERA_HELL_CREEK; act < ERA_EPILOGUE; act++)
    {
        EXPECT_EQ(VarGet(VAR_STRATA_ERA), act);
        EXPECT_EQ(Strata_GetCurrentAct(), act);
        VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(act));
        EXPECT_EQ(Strata_GetRigState(), RIG_NEXT);
        Strata_RigQuery();
        EXPECT_EQ(gSpecialVar_0x8006, act + 1 == ERA_EPILOGUE);
        Strata_RigLoadNext();
    }
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_EPILOGUE);
    EXPECT_EQ(Strata_GetRigState(), RIG_COMPLETE);
}

TEST("Dr. Halvorsen has a line for every point in the story")
{
    u32 story;
    // Story 0 is the station intro, which runs before you can talk to her.
    for (story = 1; story <= STORY_IN_ACT(ERA_EPILOGUE); story++)
    {
        VarSet(VAR_STRATA_STORY, story);
        Strata_BufferMentorText();
        EXPECT_NE(StringCompare(gStringVar4, COMPOUND_STRING("Keep up the good work out there.")), 0);
    }
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

// A species in a map's encounter table must not have died out, or already
// descended into something else, by the time of that map's era.
static void ExpectAliveInEra(const struct WildPokemonInfo *info, u32 count, enum StrataEra mapEra)
{
    static const u8 sNoPressure[PRESSURE_COUNT] = {0};
    u32 i, era;
    if (info == NULL)
        return;
    for (i = 0; i < count; i++)
    {
        u16 species = info->wildPokemon[i].species;
        for (era = ERA_HELL_CREEK; era <= mapEra; era++)
        {
            EXPECT(!Lineage_IsExtinctInEra(species, era));
            EXPECT_EQ(Lineage_GetDescendant(species, era, sNoPressure), species);
        }
    }
}

TEST("Wild Pokemon in each era's maps are alive in that era")
{
    u32 i, j;
    u16 map = 0;
    u8 era = 0;
    for (i = 0; i < ARRAY_COUNT(sStrataMapEras); i++)
    {
        PARAMETRIZE { map = sStrataMapEras[i].map; era = sStrataMapEras[i].era; }
    }

    for (i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
    {
        if (gWildMonHeaders[i].mapGroup != MAP_GROUP(map) || gWildMonHeaders[i].mapNum != MAP_NUM(map))
            continue;
        for (j = 0; j < TIMES_OF_DAY_COUNT; j++)
        {
            const struct WildEncounterTypes *types = &gWildMonHeaders[i].encounterTypes[j];
            ExpectAliveInEra(types->landMonsInfo, 12, era);   // slot counts from wild_encounters.json fields
            ExpectAliveInEra(types->waterMonsInfo, 5, era);
            ExpectAliveInEra(types->fishingMonsInfo, 10, era);
        }
    }
}

// Strata has no gym badges, so the badge-based obedience cap must never apply to
// the player's own Pokémon (B_OBEDIENCE_MECHANICS < GEN_8).
WILD_BATTLE_TEST("The player's own high-level Pokemon obey without any badges")
{
    GIVEN {
        PLAYER(SPECIES_BOREALOSUCH) { Level(31); }
        OPPONENT(SPECIES_CHAMPSOSAUR) { Level(13); }
    } WHEN {
        TURN { MOVE(player, MOVE_CRUNCH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CRUNCH, player);
    }
}
