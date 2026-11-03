#include "global.h"
#include "event_data.h"
#include "item.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "strata_fossils.h"
#include "string_util.h"
#include "text.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/characters.h"
#include "constants/strata_act_flags.h"
#include "constants/vars.h"
#include "../src/data/strata_species_eras.h"
#include "../src/data/strata_fossils.h"

// Fossil flags, the rig's loss list, the Fossil Case, the Hall and Gentle Deep Time
// (src/strata_fossils.c, src/lineage.c).

#define MESSAGE_WIDTH 208

static void ResetStrata(void)
{
    u32 boxId, boxPos, i;
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    ZeroPlayerPartyMons();
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
            ZeroBoxMonData(GetBoxedMonPtr(boxId, boxPos));
    }
    for (i = 0; i < STRATA_FOSSIL_FLAG_COUNT; i++)
        FlagClear(FLAG_STRATA_FOSSIL_BASE + i);
    FlagClear(FLAG_STRATA_GENTLE_DEEP_TIME);
}

static bool32 IsExtinctByEra(enum Species species, enum StrataEra era)
{
    u32 i;
    for (i = 0; i <= era; i++)
    {
        if (Lineage_IsExtinctInEra(species, i))
            return TRUE;
    }
    return FALSE;
}

// Widest line of a message: lines end at \n, \l and \p. Also counts the lines.
static u32 WidestLine(const u8 *str, u32 *lines)
{
    u8 line[128];
    u32 n = 0, widest = 0;
    *lines = 0;
    for (;; str++)
    {
        if (*str == EOS || *str == CHAR_NEWLINE || *str == CHAR_PROMPT_SCROLL || *str == CHAR_PROMPT_CLEAR)
        {
            line[n] = EOS;
            widest = max(widest, (u32)GetStringWidth(FONT_NORMAL, line, 0));
            (*lines)++;
            n = 0;
            if (*str == EOS)
                break;
            continue;
        }
        if (n < ARRAY_COUNT(line) - 1)
            line[n++] = *str;
    }
    return widest;
}

static bool32 Contains(const u8 *haystack, const u8 *needle)
{
    u32 i, j;
    for (i = 0; haystack[i] != EOS; i++)
    {
        for (j = 0; needle[j] != EOS && haystack[i + j] == needle[j]; j++)
            ;
        if (needle[j] == EOS)
            return TRUE;
    }
    return FALSE;
}

TEST("Every lineage an extinction filter drops has one fossil slot, and the slots fit the flags")
{
    u32 era, species, count = 0;
    for (species = SPECIES_CUSTOM_START + 1; species < SPECIES_CUSTOM_END; species++)
    {
        for (era = 0; era < ERA_COUNT; era++)
        {
            if (Lineage_IsExtinctInEra(species, era))
            {
                EXPECT_GE(Fossil_GetSlot(species), 0);
                EXPECT_EQ(Fossil_GetEra(species), era);
                count++;
            }
        }
    }
    EXPECT_EQ(count, ARRAY_COUNT(sStrataFossils));
    EXPECT_LE(ARRAY_COUNT(sStrataFossils), STRATA_FOSSIL_FLAG_COUNT);
    // The fossil and Gentle flags are inside the unused block 0x493..0x4E5 of flags.h.
    EXPECT_GE(FLAG_STRATA_FOSSIL_BASE, 0x493);
    EXPECT_LE(FLAG_STRATA_GENTLE_DEEP_TIME, 0x4E5);
}

TEST("Each fossil slot names a different species that really dies out")
{
    u32 i, j;
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        EXPECT_LT(Fossil_GetEra(sStrataFossils[i].species), ERA_COUNT);
        for (j = i + 1; j < ARRAY_COUNT(sStrataFossils); j++)
            EXPECT_NE(sStrataFossils[i].species, sStrataFossils[j].species);
    }
}

TEST("Every Gentle Deep Time relative is alive in the era its lineage is lost")
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        enum Species relative = sStrataFossils[i].gentle;
        enum StrataEra era = Fossil_GetEra(sStrataFossils[i].species);
        EXPECT_NE(relative, SPECIES_NONE);
        EXPECT_LE(sStrataSpeciesEras[relative].firstEra, era);
        EXPECT(!IsExtinctByEra(relative, era));
    }
}

TEST("Fossil reasons and era lines fit the message box in at most two lines")
{
    u32 i, lines;
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        EXPECT_LE(WidestLine(sStrataFossils[i].reason, &lines), MESSAGE_WIDTH);
        EXPECT_LE(lines, 2);
    }
    for (i = 0; i < ERA_COUNT; i++)
    {
        if (sStrataFossilEras[i].lost == NULL)
            continue;
        EXPECT_LE(WidestLine(sStrataFossilEras[i].lost, &lines), MESSAGE_WIDTH);
        EXPECT_LE(lines, 2);
    }
}

TEST("Extinctions across a multi-era jump record a fossil for each lost lineage, party and PC")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_TYRANNOSAUR, 12, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 1), SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(1, 0), SPECIES_TAENIOLABIS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(1, 1), SPECIES_UINTATHERIUM, 10, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_WHITE_RIVER);

    EXPECT(Fossil_Has(SPECIES_TYRANNOSAUR));
    EXPECT(Fossil_Has(SPECIES_TRICERATOPS));
    EXPECT(Fossil_Has(SPECIES_TAENIOLABIS));
    EXPECT(Fossil_Has(SPECIES_UINTATHERIUM));
    EXPECT(!Fossil_Has(SPECIES_EMARGINACHEL));
    EXPECT(!Fossil_Has(SPECIES_ANZU));
    EXPECT_EQ(Fossil_Count(), 4);
    EXPECT_EQ(Fossil_CountForEra(ERA_IMPACT_WINTER), 2);
    EXPECT_EQ(Fossil_CountForEra(ERA_BIGHORN_PETM), 1);
    EXPECT_EQ(Fossil_CountForEra(ERA_WHITE_RIVER), 1);
    EXPECT_EQ(Lineage_GetExtinctionCount(), 5);
    // The tyrannosaur alone, the two triceratops together, then the later eras.
    EXPECT_EQ(Fossil_GetLossEntryCount(), 4);
    EXPECT_EQ(Fossil_GetLossOverflow(), 0);
    // The flags are save flags: a later jump keeps them and adds to them.
    CreateBoxMon(GetBoxedMonPtr(2, 0), SPECIES_HYAENODON, 30, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_ASHFALL);
    EXPECT_EQ(Fossil_Count(), 5);
    EXPECT(Fossil_Has(SPECIES_TYRANNOSAUR));
    EXPECT_EQ(Fossil_GetLossEntryCount(), 1);
}

TEST("The loss list names each lost team animal, groups PC losses and gives the reason")
{
    u8 nick[] = _("Rex");
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_TYRANNOSAUR, 12, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_NICKNAME, nick);
    CreateMon(&gParties[B_TRAINER_PLAYER][2], SPECIES_ANZU, 12, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 1), SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 2), SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);
    EXPECT_EQ(Fossil_GetLossEntryCount(), 3);

    EXPECT(Fossil_BufferLossText(0, gStringVar4));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("Rex the ")));
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_TYRANNOSAUR)));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("food chain")));
    EXPECT(Fossil_BufferLossText(1, gStringVar4));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("Your ")));
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_ANZU)));
    EXPECT(Fossil_BufferLossText(2, gStringVar4));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("3 ")));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING(" in the PC")));
    EXPECT(!Fossil_BufferLossText(3, gStringVar4));
}

TEST("The loss list sums up PC losses that don't fit it")
{
    u32 i, n = 0;
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);
    // More single team losses than the list holds can't happen (6 per era), so fill it with
    // a multi-era jump's distinct PC groups: 24 entries at most, the rest summed up.
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
    {
        enum StrataEra era = Fossil_GetEra(sStrataFossils[i].species);
        if (era > ERA_ASHFALL)
            continue;
        CreateBoxMon(GetBoxedMonPtr(n / IN_BOX_COUNT, n % IN_BOX_COUNT), sStrataFossils[i].species, 10, 0, OTID_STRUCT_PLAYER_ID);
        n++;
    }
    Lineage_AdvanceToEra(ERA_ASHFALL);
    EXPECT_EQ(Fossil_GetLossEntryCount(), FOSSIL_LOSS_LIST_MAX);
    EXPECT_EQ(Fossil_GetLossOverflow(), n - FOSSIL_LOSS_LIST_MAX);
    EXPECT(Fossil_BufferLossText(FOSSIL_LOSS_LIST_MAX, gStringVar4));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("more in the PC")));
    EXPECT(!Fossil_BufferLossText(FOSSIL_LOSS_LIST_MAX + 1, gStringVar4));
    EXPECT_EQ(Fossil_Count(), n);
}

TEST("special Strata_BufferLoss walks the loss list for the rig's script")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_ANZU, 10, 0, OTID_STRUCT_PLAYER_ID);
    VarSet(VAR_0x8004, ERA_IMPACT_WINTER);
    RUN_OVERWORLD_SCRIPT(
        special Strata_AdvanceEra;
    );
    EXPECT_EQ(VarGet(VAR_0x8005), 1);
    VarSet(VAR_0x8004, 0);
    RUN_OVERWORLD_SCRIPT(
        special Strata_BufferLoss;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), TRUE);
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_ANZU)));
    VarSet(VAR_0x8004, 1);
    RUN_OVERWORLD_SCRIPT(
        special Strata_BufferLoss;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), FALSE);
}

TEST("Gentle Deep Time replaces a lost animal with its relative at the same level, and keeps the fossil")
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];
    ResetStrata();
    FlagSet(FLAG_STRATA_GENTLE_DEEP_TIME);
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateRandomMon(mon, SPECIES_TRICERATOPS, 14);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_DIDELPHODON, 12, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);

    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_ASTERIORNIS);
    EXPECT_EQ(GetMonData(mon, MON_DATA_LEVEL), 14);
    EXPECT_NE(GetMonData(mon, MON_DATA_MOVE1), MOVE_NONE);
    EXPECT_GT(GetMonData(mon, MON_DATA_MAX_HP), 0);
    EXPECT_EQ(GetBoxMonData(GetBoxedMonPtr(0, 0), MON_DATA_SPECIES), SPECIES_CIMOLESTES);
    EXPECT(Fossil_Has(SPECIES_TRICERATOPS));
    EXPECT(Fossil_Has(SPECIES_DIDELPHODON));
    EXPECT_EQ(Lineage_GetExtinctionCount(), 2);
    EXPECT(Fossil_BufferLossText(0, gStringVar4));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("A relative takes its place")));
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_ASTERIORNIS)));
}

TEST("Gentle Deep Time is off by default: the strict record removes lost animals")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);
    EXPECT(!Fossil_IsGentle());
    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT(Fossil_Has(SPECIES_TRICERATOPS));
}

TEST("A Gentle relative carries on through later eras like any lineage")
{
    ResetStrata();
    FlagSet(FLAG_STRATA_GENTLE_DEEP_TIME);
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateRandomMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TYRANNOSAUR, 14);
    Lineage_AdvanceToEra(ERA_BIGHORN_PETM);
    // Tyrannosaur -> Asteriornis in the impact winter -> its Bighorn default descendant.
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_GALLINULOID);
}

TEST("The Hall lists the player's own lineages for a filter, and nothing when there are none")
{
    ResetStrata();
    Fossil_Set(SPECIES_TRICERATOPS);
    Fossil_Set(SPECIES_ANZU);
    Fossil_Set(SPECIES_AVISAURUS);
    Fossil_Set(SPECIES_EPICYON);

    VarSet(VAR_0x8004, ERA_IMPACT_WINTER);
    RUN_OVERWORLD_SCRIPT(
        special Strata_BufferHallCase;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), 3);
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_TRICERATOPS)));
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_ANZU)));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING(" and"))); // may wrap right after "and"
    EXPECT(!Contains(gStringVar4, GetSpeciesName(SPECIES_EPICYON)));

    VarSet(VAR_0x8004, ERA_BIGHORN_PETM);
    RUN_OVERWORLD_SCRIPT(
        special Strata_BufferHallCase;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), 0);
}

TEST("The Hall's list of the player's lineages wraps to the message box")
{
    u32 i, lines;
    ResetStrata();
    for (i = 0; i < ARRAY_COUNT(sStrataFossils); i++)
        Fossil_Set(sStrataFossils[i].species);
    for (i = 0; i < ERA_COUNT; i++)
    {
        if (!Fossil_BufferHallText(i, gStringVar4))
            continue;
        EXPECT_LE(WidestLine(gStringVar4, &lines), MESSAGE_WIDTH);
    }
}

TEST("The Fossil Case labels a fossil with when and why it was lost")
{
    u32 lines;
    ResetStrata();
    Fossil_Set(SPECIES_CAMELOPS);
    VarSet(VAR_0x8004, SPECIES_CAMELOPS);
    RUN_OVERWORLD_SCRIPT(
        special Strata_BufferFossil;
    );
    EXPECT(Contains(gStringVar4, GetSpeciesName(SPECIES_CAMELOPS)));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("end of the Ice Age")));
    EXPECT(Contains(gStringVar4, COMPOUND_STRING("Camels began here")));
    EXPECT_LE(WidestLine(gStringVar4, &lines), MESSAGE_WIDTH);
}

TEST("The Fossil Case is a key item")
{
    EXPECT_EQ(GetItemPocket(ITEM_FOSSIL_CASE), POCKET_KEY_ITEMS);
    EXPECT_EQ(GetItemImportance(ITEM_FOSSIL_CASE), 1);
}
