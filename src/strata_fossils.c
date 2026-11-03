#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "malloc.h"
#include "pokemon.h"
#include "script_menu.h"
#include "strata_fossils.h"
#include "string_util.h"
#include "text.h"
#include "constants/characters.h"
#include "constants/strata_act_flags.h"

// Fossils (outline §3.5, roadmap F4/S4). When the rig's extinction filter drops a party or PC
// animal (src/lineage.c), its lineage is recorded here:
// - a save flag per lineage (FLAG_STRATA_FOSSIL_BASE + slot), read by the Fossil Case and the
//   Hall of Lost Lineages. The era is the filter that drops the species, so it isn't stored.
// - the losses of the last jump (EWRAM), for the rig's loss list.

#include "data/strata_fossils.h"

STATIC_ASSERT(ARRAY_COUNT(sStrataFossils) <= STRATA_FOSSIL_FLAG_COUNT, StrataFossilSlotsFit);

// Text width of the field message box (27 tiles, minus a margin).
#define MESSAGE_WIDTH 208

s32 Fossil_GetSlot(enum Species species)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        if (sStrataFossils[i].species == species)
            return i;
    }
    return -1;
}

bool32 Fossil_Has(enum Species species)
{
    s32 slot = Fossil_GetSlot(species);
    return slot >= 0 && FlagGet(FLAG_STRATA_FOSSIL_BASE + slot);
}

void Fossil_Set(enum Species species)
{
    s32 slot = Fossil_GetSlot(species);
    if (slot >= 0)
        FlagSet(FLAG_STRATA_FOSSIL_BASE + slot);
}

u32 Fossil_Count(void)
{
    u32 i, count = 0;
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
        count += FlagGet(FLAG_STRATA_FOSSIL_BASE + i) ? 1 : 0;
    return count;
}

// The era whose filter drops `species`, or ERA_COUNT if it never dies out.
enum StrataEra Fossil_GetEra(enum Species species)
{
    u32 era;
    for (era = 0; era < ERA_COUNT; era++)
    {
        if (Lineage_IsExtinctInEra(species, era))
            return era;
    }
    return ERA_COUNT;
}

u32 Fossil_CountForEra(enum StrataEra era)
{
    u32 i, count = 0;
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        if (FlagGet(FLAG_STRATA_FOSSIL_BASE + i) && Fossil_GetEra(sStrataFossils[i].species) == era)
            count++;
    }
    return count;
}

const u8 *Fossil_GetReason(enum Species species)
{
    s32 slot = Fossil_GetSlot(species);
    return slot >= 0 ? sStrataFossils[slot].reason : NULL;
}

enum Species Fossil_GetGentleReplacement(enum Species species)
{
    s32 slot = Fossil_GetSlot(species);
    return slot >= 0 ? sStrataFossils[slot].gentle : SPECIES_NONE;
}

bool32 Fossil_IsGentle(void)
{
    return FlagGet(FLAG_STRATA_GENTLE_DEEP_TIME);
}

// ---- the losses of the last jump ------------------------------------------------------------

// A party loss is listed on its own, with its nickname; PC losses of one species in one era
// are counted together.
struct FossilLoss
{
    u16 species;
    u16 replacement; // SPECIES_NONE unless Gentle Deep Time replaced it
    u8 era;
    u8 count;
    bool8 inParty;
    u8 nickname[POKEMON_NAME_LENGTH + 1];
};

static EWRAM_DATA struct FossilLoss sLosses[FOSSIL_LOSS_LIST_MAX] = {0};
static EWRAM_DATA u8 sLossEntryCount = 0;
static EWRAM_DATA u16 sLossOverflow = 0;

void Fossil_ResetLosses(void)
{
    sLossEntryCount = 0;
    sLossOverflow = 0;
}

// Records a lost animal: its fossil flag, and an entry in the loss list.
void Fossil_RecordLoss(struct BoxPokemon *boxMon, enum StrataEra era, bool32 inParty, enum Species replacement)
{
    enum Species species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    struct FossilLoss *loss;
    u32 i;

    Fossil_Set(species);
    if (!inParty)
    {
        for (i = 0; i < sLossEntryCount; i++)
        {
            loss = &sLosses[i];
            if (!loss->inParty && loss->species == species && loss->era == era
             && loss->replacement == replacement && loss->count < 255)
            {
                loss->count++;
                return;
            }
        }
    }
    if (sLossEntryCount >= FOSSIL_LOSS_LIST_MAX)
    {
        sLossOverflow++;
        return;
    }
    loss = &sLosses[sLossEntryCount++];
    loss->species = species;
    loss->replacement = replacement;
    loss->era = era;
    loss->count = 1;
    loss->inParty = inParty;
    GetBoxMonData(boxMon, MON_DATA_NICKNAME, loss->nickname);
    loss->nickname[POKEMON_NAME_LENGTH] = EOS;
}

u32 Fossil_GetLossEntryCount(void)
{
    return sLossEntryCount;
}

u32 Fossil_GetLossOverflow(void)
{
    return sLossOverflow;
}

static const u8 sText_Your[] = _("Your ");
static const u8 sText_The[] = _(" the ");
static const u8 sText_InThePc[] = _(" in the PC");
static const u8 sText_IsGone[] = _(" is gone.");
static const u8 sText_AreGone[] = _(" are gone.");
static const u8 sText_RelativeTakesPlace[] = _("A relative takes its place:\n");
static const u8 sText_RelativesTakePlaces[] = _("Relatives take their places:\n");
static const u8 sText_AtTheSameLevel[] = _(", at the\lsame level.");
static const u8 sText_AndMore[] = _("…and ");
static const u8 sText_MoreFromPc[] = _(" more in the PC, lost\lto the same filters.");
static const u8 sText_Space[] = _(" ");

static u8 *AppendNumber(u8 *dest, u32 n)
{
    return ConvertIntToDecimalStringN(dest + StringLength(dest), n, STR_CONV_MODE_LEFT_ALIGN, 3);
}

// `suffix` goes on the end of the line in `line` if the line still fits the message box.
static void AppendIfFits(u8 *line, const u8 *suffix)
{
    u8 buffer[64];
    StringCopy(buffer, line);
    StringAppend(buffer, suffix);
    if (GetStringWidth(FONT_NORMAL, buffer, 0) <= MESSAGE_WIDTH)
        StringCopy(line, buffer);
}

// The message for loss list entry `index`: who was lost, then why. The entry after the last
// one sums up any losses that didn't fit the list. Returns FALSE past the end.
bool32 Fossil_BufferLossText(u32 index, u8 *dest)
{
    const struct FossilLoss *loss;
    const u8 *reason;
    u8 line[64];

    if (index >= sLossEntryCount)
    {
        if (index != sLossEntryCount || sLossOverflow == 0)
            return FALSE;
        StringCopy(dest, sText_AndMore);
        AppendNumber(dest, sLossOverflow);
        StringAppend(dest, sText_MoreFromPc);
        return TRUE;
    }

    loss = &sLosses[index];
    line[0] = EOS;
    if (loss->inParty)
    {
        if (StringCompare(loss->nickname, GetSpeciesName(loss->species)) != 0)
        {
            StringCopy(line, loss->nickname);
            StringAppend(line, sText_The);
        }
        else
        {
            StringCopy(line, sText_Your);
        }
        StringAppend(line, GetSpeciesName(loss->species));
        AppendIfFits(line, sText_IsGone);
    }
    else if (loss->count == 1)
    {
        StringCopy(line, sText_Your);
        StringAppend(line, GetSpeciesName(loss->species));
        StringAppend(line, sText_InThePc);
        AppendIfFits(line, sText_IsGone);
    }
    else
    {
        AppendNumber(line, loss->count);
        StringAppend(line, sText_Space);
        StringAppend(line, GetSpeciesName(loss->species));
        StringAppend(line, sText_InThePc);
        AppendIfFits(line, sText_AreGone);
    }

    StringCopy(dest, line);
    reason = Fossil_GetReason(loss->species);
    if (reason != NULL)
    {
        u8 *end = dest + StringLength(dest);
        *end++ = CHAR_NEWLINE;
        StringCopy(end, reason);
    }
    if (loss->replacement != SPECIES_NONE)
    {
        u8 *end = dest + StringLength(dest);
        *end++ = CHAR_PROMPT_CLEAR;
        *end = EOS;
        if (loss->count > 1)
        {
            StringAppend(dest, sText_RelativesTakePlaces);
            AppendNumber(dest, loss->count);
            StringAppend(dest, sText_Space);
        }
        else
        {
            StringAppend(dest, sText_RelativeTakesPlace);
        }
        StringAppend(dest, GetSpeciesName(loss->replacement));
        StringAppend(dest, sText_AtTheSameLevel);
    }
    return TRUE;
}

// special Strata_BufferLoss
// Input:  VAR_0x8004 = index in the last jump's loss list
// Output: VAR_RESULT = FALSE past the end of the list, else TRUE and gStringVar4 = the message
void Strata_BufferLoss(void)
{
    gSpecialVar_Result = Fossil_BufferLossText(gSpecialVar_0x8004, gStringVar4);
}

// ---- the Fossil Case ------------------------------------------------------------------------

// special Strata_PushFossilList
// Pushes one dynmultistack row per fossil (id = species), in the order the record drops them.
// Output: VAR_RESULT = number of fossils
void Strata_PushFossilList(void)
{
    u32 era, i, count = 0;

    for (era = 0; era < ERA_COUNT; era++)
    {
        if (sStrataFossilEras[era].age == NULL)
            continue;
        for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
        {
            struct ListMenuItem item;
            u8 *name, *end;
            enum Species species = sStrataFossils[i].species;

            if (!FlagGet(FLAG_STRATA_FOSSIL_BASE + i) || Fossil_GetEra(species) != era)
                continue;
            // The menu frees the names.
            name = Alloc(40);
            end = StringCopy(name, GetSpeciesName(species));
            *end++ = EXT_CTRL_CODE_BEGIN;
            *end++ = EXT_CTRL_CODE_CLEAR_TO;
            *end++ = 70;
            StringCopy(end, sStrataFossilEras[era].age);
            item.name = name;
            item.id = species;
            MultichoiceDynamic_PushElement(item);
            count++;
        }
    }
    gSpecialVar_Result = count;
}

// special Strata_BufferFossil
// Input:  VAR_0x8004 = species
// Output: gStringVar4 = the fossil's label: name, when it was lost, why
void Strata_BufferFossil(void)
{
    enum Species species = gSpecialVar_0x8004;
    enum StrataEra era = Fossil_GetEra(species);
    const u8 *reason = Fossil_GetReason(species);
    u8 *end = StringCopy(gStringVar4, GetSpeciesName(species));

    if (era < ERA_COUNT && sStrataFossilEras[era].lost != NULL)
    {
        *end++ = CHAR_NEWLINE;
        end = StringCopy(end, sStrataFossilEras[era].lost);
    }
    if (reason != NULL)
    {
        *end++ = CHAR_PROMPT_CLEAR;
        StringCopy(end, reason);
    }
}

// ---- the Hall of Lost Lineages --------------------------------------------------------------

static const u8 sText_HallOwn[] = _("From your own team, this case\nholds: ");
static const u8 sText_Comma[] = _(", ");
static const u8 sText_And[] = _(" and ");
static const u8 sText_Period[] = _(".");

// "From your own team, this case holds: A, B and C." for the player's fossils from `era`'s
// filter, wrapped to the message box. Returns FALSE (and leaves dest alone) if there are none.
bool32 Fossil_BufferHallText(enum StrataEra era, u8 *dest)
{
    u32 i, n = 0, total = Fossil_CountForEra(era);
    u8 *lineStart;

    if (total == 0)
        return FALSE;
    StringCopy(dest, sText_HallOwn);
    // The second line starts after the \n in sText_HallOwn.
    lineStart = dest + StringLength(dest) - StringLength(COMPOUND_STRING("holds: "));
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        enum Species species = sStrataFossils[i].species;
        u8 word[48];
        u8 *end;

        if (!FlagGet(FLAG_STRATA_FOSSIL_BASE + i) || Fossil_GetEra(species) != era)
            continue;
        n++;
        word[0] = EOS;
        if (n > 1)
            StringCopy(word, n == total ? sText_And : sText_Comma);
        StringAppend(word, GetSpeciesName(species));
        if (n == total)
            StringAppend(word, sText_Period);

        // Wrap before the word if it would run past the box.
        {
            u8 trial[128];
            StringCopy(trial, lineStart);
            StringAppend(trial, word);
            // Leave room for the "," or " and" that stays on this line if the next word wraps.
            if (GetStringWidth(FONT_NORMAL, trial, 0) > MESSAGE_WIDTH - 24)
            {
                // Break after the separator: ", B" -> ",\lB"; " and B" -> " and\lB".
                u8 *w = word;
                end = dest + StringLength(dest);
                if (n > 1)
                {
                    const u8 *sep = (n == total) ? COMPOUND_STRING(" and") : COMPOUND_STRING(",");
                    end = StringCopy(end, sep);
                    w += StringLength(n == total ? sText_And : sText_Comma);
                }
                *end++ = CHAR_PROMPT_SCROLL;
                *end = EOS;
                lineStart = end;
                StringAppend(dest, w);
                continue;
            }
        }
        StringAppend(dest, word);
    }
    return TRUE;
}

// special Strata_BufferHallCase
// Input:  VAR_0x8004 = the era whose filter the case shows
// Output: VAR_RESULT = how many of the player's lineages it holds;
//         if any, gStringVar4 = their names, as a message
void Strata_BufferHallCase(void)
{
    gSpecialVar_Result = Fossil_CountForEra(gSpecialVar_0x8004);
    if (gSpecialVar_Result != 0)
        Fossil_BufferHallText(gSpecialVar_0x8004, gStringVar4);
}
