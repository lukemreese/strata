#include "global.h"
#include "battle_environment.h"
#include "event_object_movement.h"
#include "strata_art.h"
#include "test/test.h"
#include "constants/battle.h"
#include "constants/field_effects.h"
#include "constants/map_groups.h"
#include "constants/strata.h"

// Era art outside the tilesets (src/strata_art.c, tools/strata/gen_tilesets.py).

static void SetMap(u16 map)
{
    gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(map);
    gSaveBlock1Ptr->location.mapNum = MAP_NUM(map);
}

TEST("Battles in a recoloured era use that era's background palette")
{
    const void *grass = gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_GRASS].palette;
    const void *building = gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_BUILDING].palette;

    SetMap(MAP_STRATA_LEVEE);
    EXPECT_EQ(Strata_GetMapEra(), ERA_HELL_CREEK);
    EXPECT(Strata_GetBattleEnvironmentPalette(BATTLE_ENVIRONMENT_GRASS, grass) == grass);

    SetMap(MAP_STRATA_LEVEE_WINTER);
    EXPECT_EQ(Strata_GetMapEra(), ERA_IMPACT_WINTER);
    EXPECT(Strata_GetBattleEnvironmentPalette(BATTLE_ENVIRONMENT_GRASS, grass) != grass);
    EXPECT(Strata_GetBattleEnvironmentPalette(BATTLE_ENVIRONMENT_BUILDING, building) == building);

    SetMap(MAP_STRATA_FIELD_CAMP);
    EXPECT_EQ(Strata_GetMapEra(), ERA_COUNT);
    EXPECT(Strata_GetBattleEnvironmentPalette(BATTLE_ENVIRONMENT_GRASS, grass) == grass);
}

TEST("Grass field effects in a recoloured era use that era's palette")
{
    const struct SpritePalette *stock = &gSpritePalette_GeneralFieldEffect1;
    const struct SpritePalette *pal;

    SetMap(MAP_STRATA_RED_BEDS);
    pal = Strata_GetFieldEffectPalette(stock);
    EXPECT(pal != stock);
    EXPECT_EQ(pal->tag, FLDEFF_PAL_TAG_GENERAL_1);
    EXPECT(Strata_GetFieldEffectPalette(&gSpritePalette_GeneralFieldEffect0) == &gSpritePalette_GeneralFieldEffect0);

    SetMap(MAP_STRATA_PRAIRIE);
    EXPECT(Strata_GetFieldEffectPalette(stock) == stock);
}
