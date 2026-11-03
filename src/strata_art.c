#include "global.h"
#include "strata_art.h"
#include "strata_map.h"
#include "constants/battle.h"
#include "constants/field_effects.h"
#include "constants/strata.h"

struct StrataEraArt
{
    const u16 *const *battleEnvPalettes; // [BATTLE_ENVIRONMENT_COUNT], NULL entries keep stock
    const struct SpritePalette *fieldEffectPal1; // replaces FLDEFF_PAL_TAG_GENERAL_1 (grass, ripples)
    const u32 *const *battleEnvTiles; // [BATTLE_ENVIRONMENT_COUNT], NULL entries keep stock
    const u32 *const *battleEnvAnimTiles; // the same for the entry animation
    const struct SpriteFrameImage *tallGrassPics; // FLDEFFOBJ_TALL_GRASS frames, NULL keeps stock
    const struct SpriteFrameImage *longGrassPics; // FLDEFFOBJ_LONG_GRASS frames, NULL keeps stock
};

#include "data/strata_era_art.h"

static const struct StrataEraArt *GetEraArt(void)
{
    u32 era = Strata_GetMapEra();
    return era < ERA_COUNT ? &sStrataEraArt[era] : NULL;
}

static const void *FromEnvTable(const void *const *table, u32 environment, const void *stock)
{
    if (table != NULL && environment < BATTLE_ENVIRONMENT_COUNT && table[environment] != NULL)
        return table[environment];
    return stock;
}

const void *Strata_GetBattleEnvironmentPalette(u32 environment, const void *stock)
{
    const struct StrataEraArt *art = GetEraArt();
    return art == NULL ? stock : FromEnvTable((const void *const *)art->battleEnvPalettes, environment, stock);
}

const void *Strata_GetBattleEnvironmentTiles(u32 environment, const void *stock)
{
    const struct StrataEraArt *art = GetEraArt();
    return art == NULL ? stock : FromEnvTable((const void *const *)art->battleEnvTiles, environment, stock);
}

const void *Strata_GetBattleEnvironmentAnimTiles(u32 environment, const void *stock)
{
    const struct StrataEraArt *art = GetEraArt();
    return art == NULL ? stock : FromEnvTable((const void *const *)art->battleEnvAnimTiles, environment, stock);
}

const struct SpritePalette *Strata_GetFieldEffectPalette(const struct SpritePalette *palette)
{
    const struct StrataEraArt *art = GetEraArt();

    if (art != NULL && art->fieldEffectPal1 != NULL && palette->tag == FLDEFF_PAL_TAG_GENERAL_1)
        return art->fieldEffectPal1;
    return palette;
}

const struct SpriteFrameImage *Strata_GetFieldEffectImages(u32 fieldEffectObject, const struct SpriteFrameImage *stock)
{
    const struct StrataEraArt *art = GetEraArt();

    if (art == NULL)
        return stock;
    if (fieldEffectObject == FLDEFFOBJ_TALL_GRASS && art->tallGrassPics != NULL)
        return art->tallGrassPics;
    if (fieldEffectObject == FLDEFFOBJ_LONG_GRASS && art->longGrassPics != NULL)
        return art->longGrassPics;
    return stock;
}
