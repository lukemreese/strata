#include "global.h"
#include "battle_environment.h"
#include "event_object_movement.h"
#include "pokemon.h"
#include "strata_art.h"
#include "test/test.h"
#include "constants/battle.h"
#include "constants/event_objects.h"
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
    EXPECT(Strata_GetBattleEnvironmentPalette(BATTLE_ENVIRONMENT_GRASS, grass) != grass); // fern ground
    EXPECT(Strata_GetBattleEnvironmentPalette(BATTLE_ENVIRONMENT_BUILDING, building) == building);

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

// Before grasslands (Acts 1-5) the grass is drawn as each era's undergrowth
// (tools/strata/gen_era_tiles.py); from the Oligocene on it stays grass.
TEST("Pre-grassland eras draw undergrowth in grass battles and field effects")
{
    static const u16 maps[] = {MAP_STRATA_LEVEE, MAP_STRATA_LEVEE_WINTER, MAP_STRATA_PALM_FOREST,
                               MAP_STRATA_RED_BEDS, MAP_STRATA_LAKE_FOREST};
    const void *tiles = gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_GRASS].background.tileset;
    const void *longTiles = gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_LONG_GRASS].background.tileset;
    const void *anim = gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_GRASS].entry.tileset;
    const void *sand = gBattleEnvironmentInfo[BATTLE_ENVIRONMENT_SAND].background.tileset;
    const struct SpriteFrameImage *stockPics = gFieldEffectObjectTemplatePointers[FLDEFFOBJ_TALL_GRASS]->images;
    const struct SpriteFrameImage *stockLong = gFieldEffectObjectTemplatePointers[FLDEFFOBJ_LONG_GRASS]->images;
    u32 i;

    for (i = 0; i < ARRAY_COUNT(maps); i++)
    {
        SetMap(maps[i]);
        EXPECT(Strata_GetBattleEnvironmentTiles(BATTLE_ENVIRONMENT_GRASS, tiles) != tiles);
        EXPECT(Strata_GetBattleEnvironmentTiles(BATTLE_ENVIRONMENT_LONG_GRASS, longTiles) != longTiles);
        EXPECT(Strata_GetBattleEnvironmentAnimTiles(BATTLE_ENVIRONMENT_GRASS, anim) != anim);
        EXPECT(Strata_GetBattleEnvironmentTiles(BATTLE_ENVIRONMENT_SAND, sand) == sand);
        EXPECT(Strata_GetFieldEffectImages(FLDEFFOBJ_TALL_GRASS, stockPics) != stockPics);
        EXPECT(Strata_GetFieldEffectImages(FLDEFFOBJ_LONG_GRASS, stockLong) != stockLong);
        EXPECT_EQ(Strata_GetFieldEffectImages(FLDEFFOBJ_TALL_GRASS, stockPics)->size, stockPics->size);
    }

    SetMap(MAP_STRATA_WHITE_RIVER);     // Oligocene: recoloured, still grass
    EXPECT(Strata_GetBattleEnvironmentTiles(BATTLE_ENVIRONMENT_GRASS, tiles) == tiles);
    EXPECT(Strata_GetFieldEffectImages(FLDEFFOBJ_TALL_GRASS, stockPics) == stockPics);
    SetMap(MAP_STRATA_PRAIRIE);
    EXPECT(Strata_GetBattleEnvironmentTiles(BATTLE_ENVIRONMENT_GRASS, tiles) == tiles);
    EXPECT(Strata_GetFieldEffectImages(FLDEFFOBJ_LONG_GRASS, stockLong) == stockLong);
}

// Own creature art (tools/strata/sprites, gen_sprite.py -> gen_species.py).

#if OW_POKEMON_OBJECT_EVENTS
TEST("Strata species with an overworld sheet use it for map objects")
{
    enum Species species = SPECIES_NONE;
    const struct ObjectEventGraphicsInfo *info;
    u32 i;
    for (i = SPECIES_CUSTOM_START + 1; i < SPECIES_CUSTOM_END; i++)
    {
        PARAMETRIZE { species = i; }
    }
    info = &gSpeciesInfo[species].overworldData;
    if (info->tileTag != TAG_NONE)
        return; // no own overworld sheet yet: the engine shows the substitute placeholder
    EXPECT(SpeciesToGraphicsInfo(species, FALSE, FALSE) == info);
    EXPECT(info->images != NULL);
    EXPECT(info->anims == sAnimTable_Following);
    EXPECT_EQ(info->paletteTag, OBJ_EVENT_PAL_TAG_DYNAMIC);
    EXPECT(info->width == 32 || info->width == 64);
    EXPECT_EQ(info->width, info->height);
#if OW_PKMN_OBJECTS_SHARE_PALETTES == FALSE
    EXPECT(gSpeciesInfo[species].overworldPalette != NULL);
    EXPECT(gSpeciesInfo[species].overworldShinyPalette != NULL);
#endif
}

TEST("The pilot creatures have their own overworld sprites")
{
    EXPECT(SpeciesToGraphicsInfo(SPECIES_MESODMA, FALSE, FALSE) != &gSpeciesInfo[SPECIES_NONE].overworldData);
    EXPECT(SpeciesToGraphicsInfo(SPECIES_KNIGHTIA, FALSE, FALSE) != &gSpeciesInfo[SPECIES_NONE].overworldData);
    EXPECT_EQ(SpeciesToGraphicsInfo(SPECIES_MESODMA, FALSE, FALSE)->width, 32);
}
#endif
