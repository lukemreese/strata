#include "global.h"
#include "event_data.h"
#include "evolution_scene.h"
#include "field_weather.h"
#include "main.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "script.h"
#include "strata_acts.h"
#include "strata_descent.h"
#include "string_util.h"
#include "task.h"
#include "text.h"

// The descent scene (F3). Lineage_AdvanceToEra changes every lineage first (descents, then
// extinctions, then the level floor) and tells this file which TEAM slot did what. Afterwards
// the field station's script runs special Strata_StartDescentScenes: one stock evolution scene
// per TEAM animal whose lineage changed and is still in the TEAM, chained through
// gCB2_AfterEvolution, then back to the field and the script (the loss list follows there).
// The evolution scene asks Descent_GetActiveScene for the old species and name and for its
// text, skips setting the species (already done), and keeps its move check. It can't be
// stopped with B: a descent is not optional.

// One record per TEAM slot at the start of the advance, kept in slot order as losses are
// compacted away, like the TEAM itself.
struct DescentRecord
{
    u16 preSpecies;
    u16 descended;  // species after the last descent, or SPECIES_NONE
    bool8 lost;     // lost to extinction: the loss list tells it
    bool8 replaced; // replaced by a relative in Gentle Deep Time: the loss list tells it
    u8 preName[POKEMON_NAME_BUFFER_SIZE];
};

static EWRAM_DATA struct DescentRecord sRecords[PARTY_SIZE] = {0};
static EWRAM_DATA u8 sRecordCount = 0;
static EWRAM_DATA struct DescentScene sScenes[PARTY_SIZE] = {0};
static EWRAM_DATA u8 sSceneCount = 0;
static EWRAM_DATA u8 sSceneCurrent = 0;
static EWRAM_DATA bool8 sSceneActive = FALSE;
static EWRAM_DATA u8 sFromEra = 0;
static EWRAM_DATA u8 sToEra = 0;
static EWRAM_DATA u16 sPcCount = 0;

const u8 gText_DescentIntro[] = _("Deep time runs on for the lineage\nof {STR_VAR_1}…");
const u8 gText_DescentDone[] = _("Over {STR_VAR_3},\nthe lineage of {STR_VAR_1}\lbecame {STR_VAR_2}.{WAIT_SE}\p");
static const u8 sText_PcDescentOne[] = _("In the PC, one more lineage\nchanged as well.");
static const u8 sText_PcDescentMany[] = _("In the PC, {STR_VAR_1} more lineages\nchanged as well.");

void Descent_BeginAdvance(void)
{
    u32 i;

    sRecordCount = 0;
    sSceneCount = 0;
    sSceneActive = FALSE;
    sPcCount = 0;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][i];
        struct DescentRecord *record = &sRecords[sRecordCount++];

        record->preSpecies = GetMonData(mon, MON_DATA_SPECIES);
        record->descended = SPECIES_NONE;
        record->lost = FALSE;
        record->replaced = FALSE;
        GetMonData(mon, MON_DATA_NICKNAME, record->preName);
    }
}

void Descent_NoteTeamDescent(u32 slot, u16 species)
{
    if (slot < sRecordCount)
        sRecords[slot].descended = species;
}

void Descent_NoteTeamLost(u32 slot)
{
    if (slot < sRecordCount)
        sRecords[slot].lost = TRUE;
}

void Descent_NoteTeamReplaced(u32 slot)
{
    if (slot < sRecordCount)
        sRecords[slot].replaced = TRUE;
}

// As CompactPartySlots: empty and lost slots go, the rest keep their order.
void Descent_CompactTeam(void)
{
    u32 i, n = 0;

    for (i = 0; i < sRecordCount; i++)
    {
        if (sRecords[i].preSpecies == SPECIES_NONE || sRecords[i].lost)
            continue;
        if (i != n)
            sRecords[n] = sRecords[i];
        n++;
    }
    sRecordCount = n;
}

void Descent_NotePcDescent(void)
{
    sPcCount++;
}

// A scene for each record that descended and is still that descendant. An animal moved from
// the PC into an empty TEAM (EnsurePartyNotEmpty) has no record and gets none.
void Descent_EndAdvance(u32 fromEra, u32 toEra)
{
    u32 i;

    sFromEra = fromEra;
    sToEra = toEra;
    sSceneCount = 0;
    for (i = 0; i < sRecordCount; i++)
    {
        const struct DescentRecord *record = &sRecords[i];
        struct DescentScene *scene;

        if (record->descended == SPECIES_NONE || record->replaced || record->lost)
            continue;
        if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) != record->descended)
            continue;
        scene = &sScenes[sSceneCount++];
        scene->slot = i;
        scene->preSpecies = record->preSpecies;
        memcpy(scene->preName, record->preName, sizeof(scene->preName));
    }
}

u32 Descent_GetSceneCount(void)
{
    return sSceneCount;
}

const struct DescentScene *Descent_GetScene(u32 i)
{
    return i < sSceneCount ? &sScenes[i] : NULL;
}

u32 Descent_GetPcCount(void)
{
    return sPcCount;
}

const struct DescentScene *Descent_GetActiveScene(void)
{
    if (!sSceneActive || sSceneCurrent >= sSceneCount)
        return NULL;
    return &sScenes[sSceneCurrent];
}

void Descent_BufferSceneVars(const struct DescentScene *scene)
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][scene->slot];

    StringCopy_Nickname(gStringVar1, scene->preName);
    StringCopy(gStringVar2, GetSpeciesName(GetMonData(mon, MON_DATA_SPECIES)));
    Strata_BufferElapsedTime(gStringVar3, sFromEra, sToEra);
}

void Descent_BufferPcText(u32 count)
{
    ConvertIntToDecimalStringN(gStringVar1, count, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringExpandPlaceholders(gStringVar4, count == 1 ? sText_PcDescentOne : sText_PcDescentMany);
}

// special Strata_GetDescentSceneCount
// Output: VAR_RESULT = scenes waiting from the last load (0: skip Strata_StartDescentScenes)
void Strata_GetDescentSceneCount(void)
{
    gSpecialVar_Result = sSceneCount;
}

static void CB2_DescentScene(void);

static void CB2_AfterDescentScene(void)
{
    sSceneActive = FALSE;
    sSceneCurrent++;
    CB2_DescentScene();
}

// Each scene ends faded to black and calls gCB2_AfterEvolution: the next scene starts the
// same way, as the stock post-battle evolutions do. After the last, back to the script.
static void CB2_DescentScene(void)
{
    if (sSceneCurrent < sSceneCount)
    {
        u32 slot = sScenes[sSceneCurrent].slot;
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][slot];

        sSceneActive = TRUE;
        gCB2_AfterEvolution = CB2_AfterDescentScene;
        EvolutionScene(mon, GetMonData(mon, MON_DATA_SPECIES), FALSE, slot);
        return;
    }
    sSceneActive = FALSE;
    sSceneCount = 0;
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void Task_StartDescentScenes(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        CleanupOverworldWindowsAndTilemaps();
        DestroyTask(taskId);
        SetMainCallback2(CB2_DescentScene);
    }
}

// special Strata_StartDescentScenes (waitstate): the scenes of the last load, then the script
// goes on. Call only when Strata_GetDescentSceneCount is not 0, as ChoosePartyMon is called.
void Strata_StartDescentScenes(void)
{
    sSceneCurrent = 0;
    LockPlayerFieldControls();
    FadeScreen(FADE_TO_BLACK, 0);
    CreateTask(Task_StartDescentScenes, 10);
}

// special Strata_BufferPcDescents
// Output: VAR_RESULT = PC lineages that changed in the last load; gStringVar4 = the message
void Strata_BufferPcDescents(void)
{
    gSpecialVar_Result = sPcCount;
    if (sPcCount != 0)
        Descent_BufferPcText(sPcCount);
}
