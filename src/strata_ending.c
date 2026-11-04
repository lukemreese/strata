#include "global.h"
#include "credits.h"
#include "event_data.h"
#include "lineage.h"
#include "main.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "strata_ending.h"
#include "strata_fossils.h"
#include "string_util.h"
#include "text.h"
#include "constants/rgb.h"

// The ending (roadmap S3, outline §1.5 and §2.10): after Halvorsen's final peer review and her
// last lines (data/maps/StrataInterpretive1F/scripts.inc), the credits roll up the
// stratigraphic column (src/credits.c), one band per layer from Hell Creek to today. Under each
// band: the lineages the player carried and lost there (the fossil flags), and under today the
// lineages still alive in the TEAM and PC, traced back through the descent table.
//
// "Carried" is what the save can tell: a fossil flag is set only for an animal that was in the
// TEAM or PC when its filter ran. The living list is every animal the player has now, so an
// animal caught on today's prairie is listed too ("living today", or "descended to" when the
// descent table has an ancestor for it).

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)
#define STRATA_SPECIES_COUNT (SPECIES_CUSTOM_END - FIRST_STRATA_SPECIES)

// The story lane's VAR_STRATA_SUBPLOT (S1: 0x40DC, 10 = Bea chose the museum consortium on
// auction day, Act 8). Read through a local name so this file builds before that lane lands;
// switch to VAR_STRATA_SUBPLOT once it is defined.
#define ENDING_VAR_SUBPLOT        0x40DC
#define ENDING_SUBPLOT_CONSORTIUM 10

// Bottom (oldest) to top. The age strings say "about" only where the rig's own layer name does
// not already give a range; the Colby date is approximate (calibrated radiocarbon, ~13 ka).
static const struct EndingBand sEndingBands[] =
{
    { ERA_HELL_CREEK,    FALSE, COMPOUND_STRING("Hell Creek Fm, MT"),     COMPOUND_STRING("66.04 Ma"),         RGB(14, 12, 9),  RGB(24, 22, 18) },
    { ERA_IMPACT_WINTER, FALSE, COMPOUND_STRING("Tullock Fm, MT"),        COMPOUND_STRING("66.04 Ma + 1 yr"),  RGB(8, 8, 9),    RGB(19, 19, 20) },
    { ERA_CORRAL_BLUFFS, FALSE, COMPOUND_STRING("Corral Bluffs, CO"),     COMPOUND_STRING("65.7-65.4 Ma"),     RGB(16, 12, 7),  RGB(26, 22, 16) },
    { ERA_BIGHORN_PETM,  FALSE, COMPOUND_STRING("Bighorn Basin, WY"),     COMPOUND_STRING("56 Ma"),            RGB(18, 8, 6),   RGB(28, 19, 16) },
    { ERA_GREEN_RIVER,   FALSE, COMPOUND_STRING("Green River Fm, WY"),    COMPOUND_STRING("52-46 Ma"),         RGB(16, 14, 8),  RGB(28, 26, 19) },
    { ERA_WHITE_RIVER,   FALSE, COMPOUND_STRING("White River, SD"),       COMPOUND_STRING("33 Ma"),            RGB(18, 13, 10), RGB(29, 25, 21) },
    { ERA_ASHFALL,       FALSE, COMPOUND_STRING("Ashfall, NE"),           COMPOUND_STRING("11.9 Ma"),          RGB(14, 14, 15), RGB(27, 27, 27) },
    { ERA_TRAP_CAVE,     FALSE, COMPOUND_STRING("Natural Trap Cave, WY"), COMPOUND_STRING("20,000 yrs ago"),   RGB(11, 12, 15), RGB(23, 24, 26) },
    { ERA_TRAP_CAVE,     TRUE,  COMPOUND_STRING("Colby site, WY"),        COMPOUND_STRING("about 13,000 yrs"), RGB(14, 12, 9),  RGB(26, 24, 19) },
    { ERA_EPILOGUE,      FALSE, COMPOUND_STRING("Montana prairie"),       COMPOUND_STRING("today"),            RGB(7, 14, 5),   RGB(20, 26, 15) },
};

// The credits proper, at the top of the column (read last). General on purpose: the science is
// the published record, the people are "the Strata team".
const struct EndingCreditsLine gEndingCreditsLines[] =
{
    { COMPOUND_STRING("STRATA"), TRUE },
    { NULL },
    { COMPOUND_STRING("A model you can walk around in,") },
    { COMPOUND_STRING("not a time machine.") },
    { NULL },
    { COMPOUND_STRING("Made by the Strata team.") },
    { NULL },
    { COMPOUND_STRING("THE SCIENCE"), TRUE },
    { COMPOUND_STRING("Animals, sites and ages follow") },
    { COMPOUND_STRING("published field and museum research") },
    { COMPOUND_STRING("and the Paleobiology Database.") },
    { COMPOUND_STRING("Colours, calls and behaviour are") },
    { COMPOUND_STRING("best guesses, and labelled so.") },
    { NULL },
    { COMPOUND_STRING("THANKS"), TRUE },
    { COMPOUND_STRING("To the field crews, preparators") },
    { COMPOUND_STRING("and curators who keep each bone") },
    { COMPOUND_STRING("with its layer, and to the open") },
    { COMPOUND_STRING("GBA decompilation community.") },
    { NULL },
    { COMPOUND_STRING("Thank you for playing.") },
};
const u32 gEndingCreditsLineCount = ARRAY_COUNT(gEndingCreditsLines);

// The rig can't render the people at Colby (rule R-g): only what they left.
const u8 gText_EndingColbyFind[] = _("A Clovis point beside mammoth bones.");
const u8 gText_EndingColbyTrace[] = _("Someone made this.");
const u8 gText_EndingPair[] = _("The Pair: in a public museum case.");
const u8 gText_EndingNoLoss[] = _("Every lineage you carried came through.");
const u8 gText_EndingPlayerColumn[] = _("{PLAYER}'s column");
const u8 gText_EndingPrelude1[] = _("Every lineage you carried,");
const u8 gText_EndingPrelude2[] = _("from the bottom of the rock up.");
const u8 gText_EndingTheEnd[] = _("THE END");
const u8 gText_EndingTheEndLine[] = _("The next layer isn't written yet.");

// "…and 12 more, alive today."
void Ending_FormatOverflow(u8 *dest, u32 count)
{
    u8 *end = StringCopy(dest, COMPOUND_STRING("…and "));
    end = ConvertIntToDecimalStringN(end, count, STR_CONV_MODE_LEFT_ALIGN, 3);
    StringCopy(end, COMPOUND_STRING(" more, alive today."));
}

u32 Ending_GetBandCount(void)
{
    return ARRAY_COUNT(sEndingBands);
}

const struct EndingBand *Ending_GetBand(u32 index)
{
    return index < ARRAY_COUNT(sEndingBands) ? &sEndingBands[index] : NULL;
}

// What the credits say about a lineage lost to `filterEra`'s filter (the era it failed to enter).
static const u8 *const sLossTexts[ERA_COUNT] =
{
    [ERA_IMPACT_WINTER] = COMPOUND_STRING("lost at the K-Pg boundary"),
    [ERA_BIGHORN_PETM]  = COMPOUND_STRING("gone by the late Paleocene"),
    [ERA_WHITE_RIVER]   = COMPOUND_STRING("lost in the Eocene cooling"),
    [ERA_ASHFALL]       = COMPOUND_STRING("lost as the grasslands spread"),
    [ERA_TRAP_CAVE]     = COMPOUND_STRING("gone before the Ice Age"),
    [ERA_EPILOGUE]      = COMPOUND_STRING("lost at the end of the Ice Age"),
};

const u8 *Ending_GetLossText(enum StrataEra filterEra)
{
    if (filterEra >= ERA_COUNT || sLossTexts[filterEra] == NULL)
        return COMPOUND_STRING("lost");
    return sLossTexts[filterEra];
}

static bool32 IsStrataSpecies(u32 species)
{
    return species >= FIRST_STRATA_SPECIES && species < SPECIES_CUSTOM_END;
}

// ancestors[i] = the species that descends into FIRST_STRATA_SPECIES + i, or SPECIES_NONE.
static void BuildAncestors(u16 *ancestors)
{
    u32 species, era;

    for (species = 0; species < STRATA_SPECIES_COUNT; species++)
        ancestors[species] = SPECIES_NONE;
    for (species = FIRST_STRATA_SPECIES; species < SPECIES_CUSTOM_END; species++)
    {
        for (era = 0; era < ERA_COUNT; era++)
        {
            const struct DescentOption *option = Lineage_GetDescentOptions(species, era);
            if (option == NULL)
                continue;
            for (; option->species != SPECIES_NONE; option++)
            {
                if (IsStrataSpecies(option->species) && ancestors[option->species - FIRST_STRATA_SPECIES] == SPECIES_NONE)
                    ancestors[option->species - FIRST_STRATA_SPECIES] = species;
            }
        }
    }
}

static enum Species RootFromAncestors(const u16 *ancestors, enum Species species)
{
    u32 steps;

    // A lineage descends at most once per era, so ERA_COUNT steps reach the root.
    for (steps = 0; steps < ERA_COUNT && IsStrataSpecies(species); steps++)
    {
        enum Species ancestor = ancestors[species - FIRST_STRATA_SPECIES];
        if (ancestor == SPECIES_NONE)
            break;
        species = ancestor;
    }
    return species;
}

// The oldest species of `species`' lineage in the descent table (Canis -> Cimolestes), or
// `species` itself if nothing descends into it.
enum Species Ending_GetLineageRoot(enum Species species)
{
    u16 ancestors[STRATA_SPECIES_COUNT];
    BuildAncestors(ancestors);
    return RootFromAncestors(ancestors, species);
}

// Adds a living TEAM or PC animal, once per species.
static void AddLiving(struct EndingFate *fates, u32 *count, u32 max, u32 *overflow,
                      const u16 *ancestors, struct BoxPokemon *boxMon, bool32 inTeam)
{
    enum Species species;
    struct EndingFate *fate;
    u32 i;

    if (!GetBoxMonData(boxMon, MON_DATA_SANITY_HAS_SPECIES) || GetBoxMonData(boxMon, MON_DATA_IS_EGG))
        return;
    species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    // An animal of a lineage the record ends is not alive today (only possible in a state the
    // rig never made, e.g. a debug or test save); its fossil, if any, is listed instead.
    if (Fossil_GetEra(species) < ERA_COUNT)
        return;
    for (i = 0; i < *count; i++)
    {
        if (fates[i].kind != ENDING_FATE_LOST && fates[i].species == species)
        {
            fates[i].inTeam |= inTeam;
            return;
        }
    }
    if (*count >= max)
    {
        (*overflow)++;
        return;
    }
    fate = &fates[(*count)++];
    fate->species = species;
    fate->root = RootFromAncestors(ancestors, species);
    fate->kind = fate->root != species ? ENDING_FATE_DESCENDED : ENDING_FATE_LIVING;
    fate->layer = ERA_EPILOGUE;
    fate->inTeam = inTeam;
    fate->padding = 0;
}

// The credits' fate list: first every lost lineage (fossil flags), oldest filter first, each
// under the layer it was lost leaving; then every living species in the TEAM (in TEAM order)
// and the PC, under today. Returns the number of entries; *overflow counts living species that
// didn't fit.
u32 Ending_BuildFates(struct EndingFate *fates, u32 max, u32 *overflow)
{
    u16 ancestors[STRATA_SPECIES_COUNT];
    u32 era, species, i, boxId, boxPos, count = 0;

    *overflow = 0;
    BuildAncestors(ancestors);

    for (era = ERA_HELL_CREEK + 1; era < ERA_COUNT; era++)
    {
        for (species = FIRST_STRATA_SPECIES; species < SPECIES_CUSTOM_END; species++)
        {
            struct EndingFate *fate;
            if (!Fossil_Has(species) || Fossil_GetEra(species) != era)
                continue;
            if (count >= max)
                return count;
            fate = &fates[count++];
            fate->species = species;
            fate->root = RootFromAncestors(ancestors, species);
            fate->kind = ENDING_FATE_LOST;
            fate->layer = era - 1;
            fate->inTeam = FALSE;
            fate->padding = 0;
        }
    }

    for (i = 0; i < PARTY_SIZE; i++)
        AddLiving(fates, &count, max, overflow, ancestors, &gParties[B_TRAINER_PLAYER][i].box, TRUE);
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
            AddLiving(fates, &count, max, overflow, ancestors, GetBoxedMonPtr(boxId, boxPos), FALSE);
    }
    return count;
}

// The two columns of a fate row: who (left) and what became of it (right).
//   Tyrannosaur   lost at the K-Pg boundary
//   Cimolestes    descended to Canis
//   Bison         living today
void Ending_FormatFate(const struct EndingFate *fate, u8 *left, u8 *right)
{
    switch (fate->kind)
    {
    case ENDING_FATE_LOST:
        StringCopy(left, GetSpeciesName(fate->species));
        StringCopy(right, Ending_GetLossText(fate->layer + 1));
        break;
    case ENDING_FATE_DESCENDED:
        StringCopy(left, GetSpeciesName(fate->root));
        StringCopy(StringCopy(right, COMPOUND_STRING("descended to ")), GetSpeciesName(fate->species));
        break;
    default:
        StringCopy(left, GetSpeciesName(fate->species));
        StringCopy(right, COMPOUND_STRING("living today"));
        break;
    }
}

// FONT_NORMAL if `str` fits `width` pixels, else FONT_NARROW (test/strata_ending.c checks that
// every line fits one of them).
u32 Ending_FitFont(const u8 *str, u32 width)
{
    return GetStringWidth(FONT_NORMAL, str, 0) <= (s32)width ? FONT_NORMAL : FONT_NARROW;
}

// The Pair went to the public museum (the auction-day choice, story lane S1). The epilogue
// always shows it on display; the credits name it only once the subplot says so.
bool32 Ending_PairOnDisplay(void)
{
    return VarGet(ENDING_VAR_SUBPLOT) >= ENDING_SUBPLOT_CONSORTIUM;
}

// special Strata_RollCredits
// The credits up the column (src/credits.c), then THE END and back to the title screen, as the
// stock game does after the Hall of Fame. The script saves first (Common_EventScript_SaveGame)
// and fades to black before calling this.
void Strata_RollCredits(void)
{
    SetMainCallback2(CB2_StartCreditsSequence);
}
