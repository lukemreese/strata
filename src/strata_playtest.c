// Scripted playtest hooks (tools/strata/playtest/, strata-autotest skill).
// Compiled only into the playtest ROM (`make playtest`, -DSTRATA_PLAYTEST=1).
//
// The harness drives a headless emulator and talks to the game through two
// EWRAM structs it finds by symbol in the ELF:
//   gStrataPlaytestCommand  written by the harness: a command and a sequence number
//   gStrataPlaytestStatus   written here every frame: callbacks, map, player, story,
//                           battle and script state, and the command results
// StrataPlaytest_Poll is called once per main loop iteration from AgbMain.
#include "global.h"
#include "strata_playtest.h"

#if STRATA_PLAYTEST

#include "battle.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "field_screen_effect.h"
#include "heal_location.h"
#include "item.h"
#include "main.h"
#include "m4a.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "script.h"
#include "script_pokemon_util.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/flags.h"
#include "constants/heal_locations.h"
#include "constants/items.h"
#include "constants/strata.h"
#include "constants/vars.h"

// tools/strata/playtest/harness.py packs and unpacks these by hand (STATUS_FMT, quickstart()).
STATIC_ASSERT(sizeof(struct StrataPlaytestStatus) == 108, PlaytestStatusLayoutMatchesHarness);
STATIC_ASSERT(sizeof(struct StrataPlaytestCommand) == 12 + 296, PlaytestCommandLayoutMatchesHarness);

EWRAM_DATA struct StrataPlaytestCommand gStrataPlaytestCommand = {0};
EWRAM_DATA struct StrataPlaytestStatus gStrataPlaytestStatus = {0};
static EWRAM_DATA bool8 sQuickstartPending = FALSE;

static const u8 sText_TesterName[] = _("TESTER");

static bool32 InFreeOverworld(void)
{
    return gMain.callback2 == CB2_Overworld && !ScriptContext_IsEnabled()
        && !ArePlayerFieldControlsLocked() && !gPaletteFade.active;
}

static void WarpNow(u32 mapGroup, u32 mapNum, s32 x, s32 y)
{
    SetWarpDestination(mapGroup, mapNum, WARP_ID_NONE, x, y);
    WarpIntoMap();
    gFieldCallback = FieldCB_WarpExitFadeFromBlack;
    SetMainCallback2(CB2_LoadMap);
}

// Phase 1, from the title screen (or anywhere outside a battle): a plain new game,
// as the stock quickstart does. CB2_NewGame loads the field station.
static bool32 Quickstart_Begin(void)
{
    const struct StrataPlaytestScenario *sc = &gStrataPlaytestCommand.scenario;

    if (gMain.inBattle)
        return FALSE;
    m4aMPlayAllStop();
    ResetPaletteFade();
    FreeAllWindowBuffers();
    ResetAllPicSprites();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetTasks();
    gSaveBlock2Ptr->playerGender = (sc->options & PT_OPT_FEMALE) ? FEMALE : MALE;
    StringCopy_PlayerName(gSaveBlock2Ptr->playerName, sText_TesterName);
    sQuickstartPending = TRUE;
    SetMainCallback2(CB2_NewGame);
    return TRUE;
}

// Phase 2, on the first overworld frame: the scenario's state, then a warp.
static void Quickstart_Finish(void)
{
    const struct StrataPlaytestScenario *sc = &gStrataPlaytestCommand.scenario;
    u32 i;

    sQuickstartPending = FALSE;
    VarSet(VAR_STRATA_STORY, sc->story);
    VarSet(VAR_STRATA_ERA, sc->era);
    if (sc->story >= 1)
    {
        // What the field station intro does after the starter.
        FlagSet(FLAG_SYS_POKEMON_GET);
        FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_SYS_B_DASH);
        FlagSet(FLAG_STRATA_EXP_SHARE);
        EnableNationalPokedex();
        SetLastHealLocationWarp(HEAL_LOCATION_STRATA_FIELD_CAMP);
    }
    for (i = 0; i < sc->partyCount && i < PARTY_SIZE; i++)
        ScriptGiveMon(sc->party[i][0], sc->party[i][1], ITEM_NONE);
    for (i = 0; i < PT_MAX_ITEMS && sc->items[i][0] != ITEM_NONE; i++)
        AddBagItem(sc->items[i][0], sc->items[i][1]);
    for (i = 0; i < PT_MAX_VARS && sc->vars[i][0] != 0; i++)
        VarSet(sc->vars[i][0], sc->vars[i][1]);
    for (i = 0; i < PT_MAX_FLAGS && sc->flags[i] != 0; i++)
        FlagSet(sc->flags[i]);
#if OW_FLAG_NO_COLLISION != 0
    if (sc->options & PT_OPT_NO_COLLISION)
        FlagSet(OW_FLAG_NO_COLLISION);
#endif
#if WE_FLAG_NO_ENCOUNTER != 0
    if (sc->options & PT_OPT_NO_ENCOUNTERS)
        FlagSet(WE_FLAG_NO_ENCOUNTER);
#endif
    gSaveBlock2Ptr->optionsTextSpeed = (sc->options & PT_OPT_INSTANT_TEXT) ? OPTIONS_TEXT_SPEED_INSTANT : OPTIONS_TEXT_SPEED_FAST;
    gSaveBlock2Ptr->optionsBattleSceneOff = (sc->options & PT_OPT_NO_BATTLE_ANIM) ? TRUE : FALSE;
    WarpNow(sc->mapGroup, sc->mapNum, sc->x, sc->y);
}

static u32 RunCommand(void)
{
    const u16 *args = gStrataPlaytestCommand.args;

    switch (gStrataPlaytestCommand.cmd)
    {
    case PT_CMD_QUICKSTART:
        return Quickstart_Begin();
    case PT_CMD_SET_VAR:
        VarSet(args[0], args[1]);
        return TRUE;
    case PT_CMD_SET_FLAG:
        if (args[1])
            FlagSet(args[0]);
        else
            FlagClear(args[0]);
        return TRUE;
    case PT_CMD_WARP:
        if (!InFreeOverworld())
            return FALSE;
        WarpNow(args[0], args[1], (s16)args[2], (s16)args[3]);
        return TRUE;
    case PT_CMD_RUN_SCRIPT:
        if (!InFreeOverworld())
            return FALSE;
        ScriptContext_SetupScript((const u8 *)(args[0] | ((u32)args[1] << 16)));
        return TRUE;
    case PT_CMD_GIVE_MON:
        return ScriptGiveMon(args[0], args[1], ITEM_NONE) != MON_CANT_GIVE;
    case PT_CMD_GIVE_ITEM:
        return AddBagItem(args[0], args[1]);
    case PT_CMD_HEAL:
        HealPlayerParty();
        return TRUE;
    case PT_CMD_GET_VAR:
        gStrataPlaytestStatus.value = VarGet(args[0]);
        return TRUE;
    case PT_CMD_GET_FLAG:
        gStrataPlaytestStatus.value = FlagGet(args[0]);
        return TRUE;
    case PT_CMD_COUNT_ITEM:
        gStrataPlaytestStatus.value = CountTotalItemQuantityInBag(args[0]);
        return TRUE;
    case PT_CMD_READ_PARTY:
    {
        u32 i;
        struct StrataPlaytestStatus *st = &gStrataPlaytestStatus;

        st->partyCount = gPlayerPartyCount;
        for (i = 0; i < PARTY_SIZE; i++)
        {
            struct Pokemon *mon = &gPlayerParty[i];
            st->party[i].species = GetMonData(mon, MON_DATA_SPECIES);
            st->party[i].level = GetMonData(mon, MON_DATA_LEVEL);
            st->party[i].isEgg = GetMonData(mon, MON_DATA_IS_EGG);
            st->party[i].hp = GetMonData(mon, MON_DATA_HP);
            st->party[i].maxHP = GetMonData(mon, MON_DATA_MAX_HP);
        }
        return TRUE;
    }
    }
    return FALSE;
}

static void InitLayoutFacts(struct StrataPlaytestStatus *st)
{
    struct TextPrinter probe;
    u32 i;

    memset(&probe, 0, sizeof(probe));
    probe.active = TRUE;
    for (i = 0; i < sizeof(probe); i++)
    {
        if (((u8 *)&probe)[i])
        {
            st->printerActiveByte = i;
            st->printerActiveMask = ((u8 *)&probe)[i];
            break;
        }
    }
    st->printerNext = offsetof(struct TextPrinter, nextPrinter);
    st->printerState = offsetof(struct TextPrinter, state);
    st->printerWindowId = offsetof(struct TextPrinter, printerTemplate.windowId);
    st->sizeofTask = sizeof(struct Task);
    st->renderStateWait = RENDER_STATE_WAIT;
    st->renderStateWaitSE = RENDER_STATE_WAIT_SE;
    st->scriptNative = offsetof(struct ScriptContext, nativePtr);
    st->scriptMode = offsetof(struct ScriptContext, mode);
}

void StrataPlaytest_Poll(void)
{
    struct StrataPlaytestStatus *st = &gStrataPlaytestStatus;

    if (st->magic != STRATA_PLAYTEST_MAGIC)
    {
        InitLayoutFacts(st);
        st->magic = STRATA_PLAYTEST_MAGIC;
    }
    st->frames++;

    if (sQuickstartPending && gMain.callback2 == CB2_Overworld)
        Quickstart_Finish();
    if (gStrataPlaytestCommand.seq != st->doneSeq)
    {
        st->result = RunCommand() ? 1 : 0xFFFF;
        st->doneSeq = gStrataPlaytestCommand.seq;
    }

    st->callback1 = (u32)gMain.callback1;
    st->callback2 = (u32)gMain.callback2;
    st->inBattle = gMain.inBattle;
    st->battleTypeFlags = gBattleTypeFlags;
    st->battleOutcome = gBattleOutcome;
    st->scriptActive = ScriptContext_IsEnabled();
    st->fieldLocked = ArePlayerFieldControlsLocked();
    st->fadeActive = gPaletteFade.active;
    if (gSaveBlock1Ptr != NULL)
    {
        struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
        st->mapGroup = gSaveBlock1Ptr->location.mapGroup;
        st->mapNum = gSaveBlock1Ptr->location.mapNum;
        st->x = player->currentCoords.x - MAP_OFFSET;
        st->y = player->currentCoords.y - MAP_OFFSET;
        st->facing = player->facingDirection;
        st->moving = gPlayerAvatar.tileTransitionState;
        st->story = VarGet(VAR_STRATA_STORY);
        st->era = VarGet(VAR_STRATA_ERA);
    }
}

#endif // STRATA_PLAYTEST
