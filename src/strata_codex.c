#include "global.h"
#include "pokemon.h"
#include "strata_codex.h"
#include "constants/characters.h"

#include "data/strata_codex.h"

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)

static const struct StrataMeasurements *GetStrataMeasurements(enum Species species)
{
    if (species < FIRST_STRATA_SPECIES || species >= SPECIES_CUSTOM_END)
        return NULL;
    return &sStrataMeasurements[species - FIRST_STRATA_SPECIES];
}

u32 Strata_GetSpeciesMassGrams(enum Species species)
{
    const struct StrataMeasurements *measurements = GetStrataMeasurements(SanitizeSpeciesId(species));

    if (measurements != NULL)
        return measurements->massGrams;
    return GetSpeciesWeight(species) * 100; // hectograms
}

u32 Strata_GetSpeciesLengthCm(enum Species species)
{
    const struct StrataMeasurements *measurements = GetStrataMeasurements(SanitizeSpeciesId(species));

    if (measurements != NULL)
        return measurements->lengthCm;
    return GetSpeciesHeight(species) * 10; // decimeters
}

// Writes `value` in decimal, with a comma between thousands when `group` is set.
static u8 *WriteNumber(u8 *dst, u32 value, bool32 group)
{
    u32 divisor = 1;
    u32 place = 0; // power of ten of `divisor`

    while (value / divisor >= 10)
    {
        divisor *= 10;
        place++;
    }
    for (; divisor != 0; divisor /= 10, place--)
    {
        *dst++ = CHAR_0 + (value / divisor) % 10;
        if (group && place != 0 && place % 3 == 0)
            *dst++ = CHAR_COMMA;
    }
    return dst;
}

// Writes tenths as "N.N".
static u8 *WriteTenths(u8 *dst, u32 tenths)
{
    dst = WriteNumber(dst, tenths / 10, FALSE);
    *dst++ = CHAR_DEC_SEPARATOR;
    *dst++ = CHAR_0 + tenths % 10;
    return dst;
}

u8 *Strata_WriteMass(u8 *dst, u32 grams)
{
    u32 tenthsOfKg = grams / 100 + (grams % 100 >= 50); // rounded; no u32 overflow near the cap

    if (grams < 1000)
    {
        dst = WriteNumber(dst, grams, FALSE);
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_g;
    }
    else
    {
        if (tenthsOfKg < 1000) // under 100 kg: one decimal
        {
            dst = WriteTenths(dst, tenthsOfKg);
        }
        else
        {
            u32 kg = grams / 1000 + (grams % 1000 >= 500);

            if (kg > CODEX_MAX_MASS_KG)
            {
                dst = WriteNumber(dst, CODEX_MAX_MASS_KG, TRUE);
                *dst++ = CHAR_PLUS;
            }
            else
            {
                dst = WriteNumber(dst, kg, TRUE);
            }
        }
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_k;
        *dst++ = CHAR_g;
    }
    *dst = EOS;
    return dst;
}

u8 *Strata_WriteLength(u8 *dst, u32 centimeters)
{
    u32 decimeters = centimeters / 10 + (centimeters % 10 >= 5);

    if (centimeters < 100)
    {
        dst = WriteNumber(dst, centimeters, FALSE);
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_c;
    }
    else
    {
        if (decimeters > CODEX_MAX_LENGTH_DM)
        {
            dst = WriteTenths(dst, CODEX_MAX_LENGTH_DM);
            *dst++ = CHAR_PLUS;
        }
        else
        {
            dst = WriteTenths(dst, decimeters);
        }
        *dst++ = CHAR_SPACE;
    }
    *dst++ = CHAR_m;
    *dst = EOS;
    return dst;
}
