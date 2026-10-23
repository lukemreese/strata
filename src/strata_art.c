#include "global.h"
#include "strata_art.h"
#include "constants/battle.h"
#include "constants/field_effects.h"
#include "constants/map_groups.h"
#include "constants/strata.h"

struct StrataEraArt
{
    const u16 *const *battleEnvPalettes; // [BATTLE_ENVIRONMENT_COUNT], NULL entries keep stock
    const struct SpritePalette *fieldEffectPal1; // replaces FLDEFF_PAL_TAG_GENERAL_1 (grass, ripples)
};

#include "data/strata_map_eras.h"
#include "data/strata_era_art.h"

u32 Strata_GetMapEra(void)
{
    u32 i;
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;

    for (i = 0; i < ARRAY_COUNT(sStrataMapEras); i++)
    {
        if (sStrataMapEras[i].map == map)
            return sStrataMapEras[i].era;
    }
    return ERA_COUNT;
}

static const struct StrataEraArt *GetEraArt(void)
{
    u32 era = Strata_GetMapEra();
    return era < ERA_COUNT ? &sStrataEraArt[era] : NULL;
}

const void *Strata_GetBattleEnvironmentPalette(u32 environment, const void *stock)
{
    const struct StrataEraArt *art = GetEraArt();

    if (art != NULL && art->battleEnvPalettes != NULL
     && environment < BATTLE_ENVIRONMENT_COUNT && art->battleEnvPalettes[environment] != NULL)
        return art->battleEnvPalettes[environment];
    return stock;
}

const struct SpritePalette *Strata_GetFieldEffectPalette(const struct SpritePalette *palette)
{
    const struct StrataEraArt *art = GetEraArt();

    if (art != NULL && art->fieldEffectPal1 != NULL && palette->tag == FLDEFF_PAL_TAG_GENERAL_1)
        return art->fieldEffectPal1;
    return palette;
}
