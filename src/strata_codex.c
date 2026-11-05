#include "global.h"
#include "lineage.h"
#include "pokedex.h"
#include "pokemon.h"
#include "strata_codex.h"
#include "strata_ending.h"
#include "strata_fossils.h"
#include "string_util.h"
#include "text.h"
#include "constants/characters.h"

#include "data/strata_codex.h"
#include "data/strata_evidence.h"

// The Codex (roadmap C14, docs/strata_design.md 7.8): exact metric measurements, and the data
// and text of the EVIDENCE and LINEAGE pages that src/pokedex.c draws.

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)

static bool32 IsStrataSpecies(u32 species)
{
    return species >= FIRST_STRATA_SPECIES && species < SPECIES_CUSTOM_END;
}

// ---------------------------------------------------------------------------------------------
// Measurements

static const struct StrataMeasurements *GetStrataMeasurements(enum Species species)
{
    if (!IsStrataSpecies(species))
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

// `value` / `unit`, rounded half up, without overflowing near the top of a u32.
static u32 RoundDiv(u32 value, u32 unit)
{
    return value / unit + (value % unit >= (unit + 1) / 2);
}

// Each step is chosen by the rounded value, so 99,950 g reads "100 kg", not "100.0 kg", and
// 999,500 g reads "1.0 t".
u8 *Strata_WriteMass(u8 *dst, u32 grams)
{
    if (grams < 1000)
    {
        dst = WriteNumber(dst, grams, FALSE);
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_g;
    }
    else if (RoundDiv(grams, 100) < 1000)    // under 100 kg: one decimal
    {
        dst = WriteTenths(dst, RoundDiv(grams, 100));
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_k;
        *dst++ = CHAR_g;
    }
    else if (RoundDiv(grams, 1000) < 1000)   // under a tonne: whole kg
    {
        dst = WriteNumber(dst, RoundDiv(grams, 1000), FALSE);
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_k;
        *dst++ = CHAR_g;
    }
    else
    {
        if (RoundDiv(grams, 100000) < 1000)  // under 100 t: tonnes, one decimal
            dst = WriteTenths(dst, RoundDiv(grams, 100000));
        else                                 // whole tonnes, thousands comma
            dst = WriteNumber(dst, RoundDiv(grams, 1000000), TRUE);
        *dst++ = CHAR_SPACE;
        *dst++ = CHAR_t;
    }
    *dst = EOS;
    return dst;
}

u8 *Strata_WriteLength(u8 *dst, u32 centimeters)
{
    u32 decimeters = RoundDiv(centimeters, 10);

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

// ---------------------------------------------------------------------------------------------
// Shared text

const u8 *const gCodexBarLabels[CODEX_BAR_SLOTS] =
{
    COMPOUND_STRING("EVIDENCE"),
    COMPOUND_STRING("LINEAGE"),
    COMPOUND_STRING("CRY"),
};

// Short layer names for the LINEAGE page (the rig's full names are in src/strata_acts.c).
static const u8 *const sEraNames[ERA_COUNT] =
{
    [ERA_PRESENT_DIG]   = COMPOUND_STRING("the dig"),
    [ERA_HELL_CREEK]    = COMPOUND_STRING("Hell Creek"),
    [ERA_IMPACT_WINTER] = COMPOUND_STRING("the impact winter"),
    [ERA_CORRAL_BLUFFS] = COMPOUND_STRING("Corral Bluffs"),
    [ERA_BIGHORN_PETM]  = COMPOUND_STRING("the PETM"),
    [ERA_GREEN_RIVER]   = COMPOUND_STRING("Green River"),
    [ERA_WHITE_RIVER]   = COMPOUND_STRING("White River"),
    [ERA_ASHFALL]       = COMPOUND_STRING("Ashfall"),
    [ERA_TRAP_CAVE]     = COMPOUND_STRING("the Ice Age"),
    [ERA_EPILOGUE]      = COMPOUND_STRING("today"),
};

// The pressure chart's labels (src/strata_forecast.c): MEAT, not ANIMAL (strata-text skill).
static const u8 *const sPressureLabels[PRESSURE_COUNT] =
{
    [PRESSURE_FOREST]     = COMPOUND_STRING("FOREST"),
    [PRESSURE_OPEN]       = COMPOUND_STRING("OPEN"),
    [PRESSURE_WATER]      = COMPOUND_STRING("WATER"),
    [PRESSURE_PLANT_DIET] = COMPOUND_STRING("PLANT"),
    [PRESSURE_MEAT_DIET]  = COMPOUND_STRING("MEAT"),
    [PRESSURE_HEAT]       = COMPOUND_STRING("HEAT"),
};

static const u8 sText_Unknown[] = _("?");

const u8 *Codex_GetEraName(enum StrataEra era)
{
    if (era >= ERA_COUNT || sEraNames[era] == NULL)
        return sText_Unknown;
    return sEraNames[era];
}

const u8 *Codex_GetPressureLabel(u32 pressure)
{
    if (pressure >= PRESSURE_COUNT)
        return COMPOUND_STRING("default");
    return sPressureLabels[pressure];
}

u32 Codex_FitFont(const u8 *str, u32 width)
{
    return GetStringWidth(FONT_NORMAL, str, 0) <= (s32)width ? FONT_NORMAL : FONT_NARROW;
}

// ---------------------------------------------------------------------------------------------
// EVIDENCE

const struct StrataEvidence *Codex_GetEvidence(enum Species species)
{
    species = SanitizeSpeciesId(species);
    if (!IsStrataSpecies(species) || species - FIRST_STRATA_SPECIES >= ARRAY_COUNT(sStrataEvidence))
        return NULL;
    return &sStrataEvidence[species - FIRST_STRATA_SPECIES];
}

//   Tyrannosaurus rex
//   Site: Hell Creek Fm, MT
//   Age: 66.1 Ma            (mass estimated: "Age: 66.1 Ma, mass estimated")
//   Record: well known
//   <2-4 evidence lines>
u32 Codex_FormatEvidence(enum Species species, u8 rows[][CODEX_LINE_SIZE])
{
    const struct StrataEvidence *evidence = Codex_GetEvidence(species);
    u32 i, n = 0;
    u8 *end;

    if (evidence == NULL)
        return 0;
    StringCopy(rows[n++], evidence->genus);
    StringCopy(StringCopy(rows[n++], COMPOUND_STRING("Site: ")), evidence->site);
    end = StringCopy(StringCopy(rows[n++], COMPOUND_STRING("Age: ")), evidence->age);
    if (evidence->massEstimate)
        StringCopy(end, COMPOUND_STRING(", mass estimated"));
    StringCopy(StringCopy(rows[n++], COMPOUND_STRING("Record: ")), evidence->record);
    for (i = 0; i < evidence->lineCount && i < CODEX_EVIDENCE_MAX_LINES; i++)
        StringCopy(rows[n++], evidence->lines[i]);
    return n;
}

// ---------------------------------------------------------------------------------------------
// LINEAGE

// The species that descends into `species`, with the era and option it descends by. FALSE for a
// root. A species appears as a descendant of at most one ancestor (test/strata_codex.c).
static bool32 FindParent(u32 species, u16 *parent, u8 *era, u8 *pressure)
{
    u32 ancestor, e;

    for (ancestor = FIRST_STRATA_SPECIES; ancestor < SPECIES_CUSTOM_END; ancestor++)
    {
        for (e = 0; e < ERA_COUNT; e++)
        {
            const struct DescentOption *option = Lineage_GetDescentOptions(ancestor, e);
            for (; option != NULL && option->species != SPECIES_NONE; option++)
            {
                if (option->species == species)
                {
                    *parent = ancestor;
                    *era = e;
                    *pressure = option->pressure;
                    return TRUE;
                }
            }
        }
    }
    return FALSE;
}

static bool32 HasDescendants(u32 species)
{
    u32 e;
    for (e = 0; e < ERA_COUNT; e++)
    {
        const struct DescentOption *option = Lineage_GetDescentOptions(species, e);
        if (option != NULL && option->species != SPECIES_NONE)
            return TRUE;
    }
    return FALSE;
}

static bool32 IsSeen(u32 species)
{
    return GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_SEEN);
}

static void FillRow(struct CodexLineageRow *row, u32 species, u32 parent, u32 depth, u32 era, u32 pressure)
{
    const struct StrataEvidence *evidence = Codex_GetEvidence(species);

    row->species = species;
    row->parent = parent;
    row->depth = depth;
    row->pressure = pressure;
    if (parent == SPECIES_NONE)
    {
        row->kind = CODEX_LINEAGE_ROOT;
        row->era = evidence != NULL ? evidence->firstEra : ERA_COUNT;
    }
    else
    {
        row->kind = pressure == PRESSURE_NONE ? CODEX_LINEAGE_DEFAULT : CODEX_LINEAGE_BRANCH;
        row->era = era;
    }
    row->lostEra = ERA_COUNT;
    if (HasDescendants(species))
    {
        row->fate = CODEX_FATE_DESCENDS;
    }
    else if (Fossil_GetEra(species) < ERA_COUNT)
    {
        row->fate = CODEX_FATE_LOST;
        row->lostEra = Fossil_GetEra(species);
    }
    else
    {
        row->fate = CODEX_FATE_LIVING;
    }
    row->seen = IsSeen(species);
    row->isSelf = FALSE;
}

// Depth first: each era's options in table order (the default first), recursing into each.
static void AddDescendants(struct CodexLineageRow *rows, u32 *count, u32 max, u32 species, u32 depth)
{
    u32 e;

    // A lineage descends at most once per era, so the table can't nest deeper than ERA_COUNT.
    if (depth > ERA_COUNT)
        return;
    for (e = 0; e < ERA_COUNT; e++)
    {
        const struct DescentOption *option = Lineage_GetDescentOptions(species, e);
        for (; option != NULL && option->species != SPECIES_NONE; option++)
        {
            if (*count >= max)
                return;
            FillRow(&rows[(*count)++], option->species, species, depth + 1, e, option->pressure);
            AddDescendants(rows, count, max, option->species, depth + 1);
        }
    }
}

u32 Codex_BuildLineage(enum Species species, struct CodexLineageRow *rows, u32 max)
{
    u16 chain[ERA_COUNT + 1];
    u8 chainEra[ERA_COUNT + 1], chainPressure[ERA_COUNT + 1];
    u32 length = 0, count = 0, i;
    u16 current = species;

    if (max == 0)
        return 0;
    // Walk up to the root (one step per era at most), then list the chain from the root down.
    while (length < ARRAY_COUNT(chain))
    {
        u16 parent;
        u8 era, pressure;

        chain[length] = current;
        if (!FindParent(current, &parent, &era, &pressure))
        {
            chainEra[length] = ERA_COUNT;
            chainPressure[length] = PRESSURE_NONE;
            length++;
            break;
        }
        chainEra[length] = era;
        chainPressure[length] = pressure;
        length++;
        current = parent;
    }
    for (i = 0; i < length && count < max; i++)
    {
        u32 index = length - 1 - i;
        u32 parent = index + 1 < length ? chain[index + 1] : SPECIES_NONE;
        FillRow(&rows[count++], chain[index], parent, i, chainEra[index], chainPressure[index]);
    }
    rows[count - 1].isSelf = (rows[count - 1].species == species);
    AddDescendants(rows, &count, max, species, rows[count - 1].depth);
    return count;
}

static const u8 *RowName(u32 species, bool32 seen)
{
    return seen ? GetSpeciesName(species) : sText_Unknown;
}

void Codex_FormatLineageRow(const struct CodexLineageRow *row, u8 *name, u8 *tag, u8 *fate)
{
    StringCopy(name, RowName(row->species, row->seen));
    switch (row->kind)
    {
    case CODEX_LINEAGE_ROOT:
        *tag = EOS;
        break;
    case CODEX_LINEAGE_DEFAULT:
        StringCopy(tag, COMPOUND_STRING("default"));
        break;
    default:
        StringCopy(tag, Codex_GetPressureLabel(row->pressure));
        break;
    }
    if (!row->seen)
        StringCopy(fate, sText_Unknown);
    else if (row->fate == CODEX_FATE_LIVING)
        StringCopy(fate, COMPOUND_STRING("living"));
    else if (row->fate == CODEX_FATE_LOST)
        StringCopy(fate, COMPOUND_STRING("lost"));
    else
        *fate = EOS;
}

// Copies `src` with its first letter in upper case.
static u8 *CopyCapitalised(u8 *dest, const u8 *src)
{
    u8 *end = StringCopy(dest, src);
    if (dest[0] >= CHAR_a && dest[0] <= CHAR_z)
        dest[0] += CHAR_A - CHAR_a;
    return end;
}

// Splits a two-line message string (lines joined by \l or \n) into `lines`; returns the count.
static u32 SplitLines(const u8 *src, u8 lines[][CODEX_LINE_SIZE], u32 max)
{
    u32 n = 0, len = 0;

    if (src == NULL || max == 0)
        return 0;
    for (; *src != EOS; src++)
    {
        if (*src == CHAR_PROMPT_SCROLL || *src == CHAR_NEWLINE)
        {
            lines[n][len] = EOS;
            if (++n >= max)
                return n;
            len = 0;
        }
        else if (len < CODEX_LINE_SIZE - 1)
        {
            lines[n][len++] = *src;
        }
    }
    lines[n][len] = EOS;
    return n + 1;
}

//   From Leptocyon at the Ice Age: MEAT
//   Lost at the end of the Ice Age.
//   <the fossil reason, two lines>
u32 Codex_FormatLineageDetail(const struct CodexLineageRow *rows, u32 count, u32 index,
                              u8 lines[][CODEX_LINE_SIZE])
{
    const struct CodexLineageRow *row = &rows[index];
    const struct StrataEvidence *evidence = Codex_GetEvidence(row->species);
    u32 n = 0, i, children = 0;
    u8 *end;

    // 1. Where it comes from.
    end = lines[n++];
    if (row->kind == CODEX_LINEAGE_ROOT)
    {
        if (count == 1)
            end = StringCopy(end, COMPOUND_STRING("No descents: a line of its own."));
        else
            end = StringCopy(StringCopy(end, COMPOUND_STRING("Root of the line, at ")), Codex_GetEraName(row->era));
    }
    else
    {
        bool32 parentSeen = TRUE;
        for (i = 0; i < count; i++)
        {
            if (rows[i].species == row->parent)
                parentSeen = rows[i].seen;
        }
        end = StringCopy(end, COMPOUND_STRING("From "));
        end = StringCopy(end, RowName(row->parent, parentSeen));
        end = StringCopy(end, COMPOUND_STRING(" at "));
        end = StringCopy(end, Codex_GetEraName(row->era));
        end = StringCopy(end, COMPOUND_STRING(": "));
        end = StringCopy(end, row->kind == CODEX_LINEAGE_DEFAULT ? COMPOUND_STRING("default") : Codex_GetPressureLabel(row->pressure));
    }

    // 2. What became of it.
    end = lines[n++];
    if (!row->seen)
    {
        StringCopy(end, COMPOUND_STRING("Not yet seen in the Codex."));
        return n;
    }
    switch (row->fate)
    {
    case CODEX_FATE_DESCENDS:
    {
        u32 total = 0;
        for (i = index + 1; i < count; i++)
            total += rows[i].parent == row->species && rows[i].depth == row->depth + 1;
        // "Descends: A.", "Descends: A or B.", "Descends: A, B or C."
        end = StringCopy(end, COMPOUND_STRING("Descends: "));
        for (i = index + 1; i < count; i++)
        {
            if (rows[i].parent != row->species || rows[i].depth != row->depth + 1)
                continue;
            if (children != 0)
                end = StringCopy(end, children + 1 == total ? COMPOUND_STRING(" or ") : COMPOUND_STRING(", "));
            end = StringCopy(end, RowName(rows[i].species, rows[i].seen));
            children++;
        }
        StringCopy(end, COMPOUND_STRING("."));
        break;
    }
    case CODEX_FATE_LOST:
        end = CopyCapitalised(end, Ending_GetLossText(row->lostEra));
        StringCopy(end, COMPOUND_STRING("."));
        n += SplitLines(Fossil_GetReason(row->species), &lines[n], CODEX_LINEAGE_DETAIL_LINES - n);
        break;
    default:
        StringCopy(end, COMPOUND_STRING("Living today."));
        for (i = 0; evidence != NULL && i < CODEX_EVIDENCE_TODAY_LINES && n < CODEX_LINEAGE_DETAIL_LINES; i++)
        {
            if (evidence->today[i] != NULL)
                StringCopy(lines[n++], evidence->today[i]);
        }
        break;
    }
    return n;
}
