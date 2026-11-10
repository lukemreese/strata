#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "strata_acts.h"
#include "strata_descent.h"
#include "string_util.h"
#include "text.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/characters.h"
#include "constants/strata_act_flags.h"
#include "constants/vars.h"

// The descent scene (F3, src/strata_descent.c): which TEAM animals get a scene after a load,
// the time between the layers, and the scene's text.

#define MESSAGE_WIDTH 208

static void ResetStrata(void)
{
    u32 boxId, boxPos;
    VarSet(VAR_STRATA_ERA, ERA_PRESENT_DIG);
    ZeroPlayerPartyMons();
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPos = 0; boxPos < IN_BOX_COUNT; boxPos++)
            ZeroBoxMonData(GetBoxedMonPtr(boxId, boxPos));
    }
    FlagClear(FLAG_STRATA_GENTLE_DEEP_TIME);
}

// Widest line of a message: lines end at \n, \l and \p.
static u32 WidestLine(const u8 *str)
{
    u8 line[128];
    u32 n = 0, widest = 0;
    for (;; str++)
    {
        if (*str == EOS || *str == CHAR_NEWLINE || *str == CHAR_PROMPT_SCROLL || *str == CHAR_PROMPT_CLEAR)
        {
            line[n] = EOS;
            widest = max(widest, (u32)GetStringWidth(FONT_NORMAL, line, 0));
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

static bool32 IsElapsed(u32 fromEra, u32 toEra, const u8 *expected)
{
    u8 buffer[32];
    Strata_BufferElapsedTime(buffer, fromEra, toEra);
    return StringCompare(buffer, expected) == 0;
}

TEST("The time between two layers is hedged and rounded")
{
    EXPECT(IsElapsed(ERA_IMPACT_WINTER, ERA_CORRAL_BLUFFS, COMPOUND_STRING("about 500,000 years")));
    EXPECT(IsElapsed(ERA_CORRAL_BLUFFS, ERA_BIGHORN_PETM, COMPOUND_STRING("about 10 million years")));
    EXPECT(IsElapsed(ERA_BIGHORN_PETM, ERA_GREEN_RIVER, COMPOUND_STRING("about 6 million years")));
    EXPECT(IsElapsed(ERA_GREEN_RIVER, ERA_WHITE_RIVER, COMPOUND_STRING("about 18 million years")));
    EXPECT(IsElapsed(ERA_WHITE_RIVER, ERA_ASHFALL, COMPOUND_STRING("about 20 million years")));
    EXPECT(IsElapsed(ERA_ASHFALL, ERA_TRAP_CAVE, COMPOUND_STRING("about 12 million years")));
    EXPECT(IsElapsed(ERA_TRAP_CAVE, ERA_EPILOGUE, COMPOUND_STRING("about 20,000 years")));
    // A multi-era jump spans all of them.
    EXPECT(IsElapsed(ERA_CORRAL_BLUFFS, ERA_ASHFALL, COMPOUND_STRING("about 54 million years")));
}

TEST("A load gives a scene to each TEAM animal that descended, in TEAM order after the losses")
{
    u8 nick[] = _("Dobbin");
    const struct DescentScene *scene;
    struct Pokemon *party = gParties[B_TRAINER_PLAYER];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_WHITE_RIVER);
    CreateMon(&party[0], SPECIES_HYAENODON, 30, 0, OTID_STRUCT_PLAYER_ID);   // lost
    CreateMon(&party[1], SPECIES_MESOHIPPUS, 30, 0, OTID_STRUCT_PLAYER_ID);  // descends
    SetMonData(&party[1], MON_DATA_NICKNAME, nick);
    CreateMon(&party[2], SPECIES_LEPISOSTEUS, 30, 0, OTID_STRUCT_PLAYER_ID); // stays as it is
    CreateMon(&party[3], SPECIES_HESPEROCYON, 30, 0, OTID_STRUCT_PLAYER_ID); // descends
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_POEBROTHERE, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 1), SPECIES_LEPISOSTEUS, 30, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_ASHFALL);

    EXPECT_EQ(CalculatePlayerPartyCount(), 3);
    EXPECT_EQ(Descent_GetSceneCount(), 2);
    EXPECT_EQ(Descent_GetPcCount(), 1);
    EXPECT(Descent_GetScene(2) == NULL);

    scene = Descent_GetScene(0);
    EXPECT_EQ(scene->slot, 0);
    EXPECT_EQ(scene->preSpecies, SPECIES_MESOHIPPUS);
    EXPECT_EQ(StringCompare(scene->preName, nick), 0);
    EXPECT_NE(GetMonData(&party[0], MON_DATA_SPECIES), SPECIES_MESOHIPPUS);
    // The scene's words: the old name, the new species and the time between the layers.
    Descent_BufferSceneVars(scene);
    EXPECT_EQ(StringCompare(gStringVar1, nick), 0);
    EXPECT_EQ(StringCompare(gStringVar2, GetSpeciesName(GetMonData(&party[0], MON_DATA_SPECIES))), 0);
    EXPECT_EQ(StringCompare(gStringVar3, COMPOUND_STRING("about 20 million years")), 0);

    scene = Descent_GetScene(1);
    EXPECT_EQ(scene->slot, 2);
    EXPECT_EQ(scene->preSpecies, SPECIES_HESPEROCYON);
    EXPECT_NE(GetMonData(&party[2], MON_DATA_SPECIES), SPECIES_HESPEROCYON);
    // No nickname: it was called by its species, and the name followed the lineage.
    EXPECT_EQ(StringCompare(scene->preName, GetSpeciesName(SPECIES_HESPEROCYON)), 0);
    Descent_BufferSceneVars(scene);
    EXPECT_EQ(StringCompare(gStringVar1, GetSpeciesName(SPECIES_HESPEROCYON)), 0);

    EXPECT_EQ(GetMonData(&party[1], MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
}

TEST("No scene for a Gentle Deep Time relative, or with nothing that descended")
{
    struct Pokemon *party = gParties[B_TRAINER_PLAYER];

    ResetStrata();
    FlagSet(FLAG_STRATA_GENTLE_DEEP_TIME);
    VarSet(VAR_STRATA_ERA, ERA_WHITE_RIVER);
    CreateMon(&party[0], SPECIES_HYAENODON, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&party[1], SPECIES_LEPISOSTEUS, 30, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_ASHFALL);
    EXPECT_EQ(CalculatePlayerPartyCount(), 2);
    EXPECT_NE(GetMonData(&party[0], MON_DATA_SPECIES), SPECIES_HYAENODON);
    EXPECT_EQ(Descent_GetSceneCount(), 0);
    EXPECT_EQ(Descent_GetPcCount(), 0);

    // Hell Creek to the impact winter: losses only, no descents.
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&party[0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&party[1], SPECIES_TYRANNOSAUR, 10, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);
    EXPECT_EQ(Descent_GetSceneCount(), 0);
}

TEST("A TEAM that empties gets no scene for the PC animal moved into it")
{
    struct Pokemon *party = gParties[B_TRAINER_PLAYER];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_WHITE_RIVER);
    CreateMon(&party[0], SPECIES_HYAENODON, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_MESOHIPPUS, 30, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_ASHFALL);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(Descent_GetSceneCount(), 0);
    EXPECT_EQ(Descent_GetPcCount(), 1);
}

TEST("The rig's specials report the scenes and the PC line of the last load")
{
    struct Pokemon *party = gParties[B_TRAINER_PLAYER];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_IMPACT_WINTER);
    CreateMon(&party[0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 1), SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);

    RUN_OVERWORLD_SCRIPT(
        special Strata_GetDescentSceneCount;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), 1);
    RUN_OVERWORLD_SCRIPT(
        special Strata_BufferPcDescents;
    );
    EXPECT_EQ(VarGet(VAR_RESULT), 2);
    EXPECT_EQ(StringCompare(gStringVar4, COMPOUND_STRING("In the PC, 2 more lineages\nchanged as well.")), 0);
    Descent_BufferPcText(1);
    EXPECT_EQ(StringCompare(gStringVar4, COMPOUND_STRING("In the PC, one more lineage\nchanged as well.")), 0);
    // Only the scene in play is handed to the evolution scene.
    EXPECT(Descent_GetActiveScene() == NULL);
}

TEST("The descent scene's messages fit the battle message box")
{
    u8 longName[] = _("MMMMMMMMMMMM");
    u32 species, era, widest = SPECIES_CUSTOM_START + 1;

    for (species = SPECIES_CUSTOM_START + 1; species < SPECIES_CUSTOM_END; species++)
    {
        if (GetStringWidth(FONT_NORMAL, GetSpeciesName(species), 0) > GetStringWidth(FONT_NORMAL, GetSpeciesName(widest), 0))
            widest = species;
    }

    StringCopy(gStringVar1, longName);
    StringExpandPlaceholders(gStringVar4, gText_DescentIntro);
    EXPECT_LE(WidestLine(gStringVar4), MESSAGE_WIDTH);
    StringCopy(gStringVar1, GetSpeciesName(widest));
    StringExpandPlaceholders(gStringVar4, gText_DescentIntro);
    EXPECT_LE(WidestLine(gStringVar4), MESSAGE_WIDTH);

    for (era = ERA_HELL_CREEK; era < ERA_EPILOGUE; era++)
    {
        StringCopy(gStringVar1, longName);
        StringCopy(gStringVar2, GetSpeciesName(widest));
        Strata_BufferElapsedTime(gStringVar3, era, era + 1);
        StringExpandPlaceholders(gStringVar4, gText_DescentDone);
        EXPECT_LE(WidestLine(gStringVar4), MESSAGE_WIDTH);
    }

    // The most the PC can hold.
    Descent_BufferPcText(TOTAL_BOXES_COUNT * IN_BOX_COUNT);
    EXPECT_LE(WidestLine(gStringVar4), MESSAGE_WIDTH);
}
