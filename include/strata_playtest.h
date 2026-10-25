#ifndef GUARD_STRATA_PLAYTEST_H
#define GUARD_STRATA_PLAYTEST_H

// Hooks for the scripted playtest harness (tools/strata/playtest/, the
// strata-autotest skill). Only built into the playtest ROM: `make playtest`
// passes -DSTRATA_PLAYTEST=1. Release and normal builds compile none of it.
#ifndef STRATA_PLAYTEST
#define STRATA_PLAYTEST 0
#endif

#define STRATA_PLAYTEST_MAGIC 0x54505453 // "STPT"

// Commands the harness writes into gStrataPlaytestCommand. The game runs a
// command once per new seq value and copies seq into gStrataPlaytestStatus.doneSeq.
enum StrataPlaytestCmd
{
    PT_CMD_NONE,
    PT_CMD_QUICKSTART, // a new game in the state described by .scenario
    PT_CMD_SET_VAR,    // args[0] = var, args[1] = value
    PT_CMD_SET_FLAG,   // args[0] = flag, args[1] = 0 clear / 1 set
    PT_CMD_WARP,       // args = map group, map num, x, y (overworld, no script running)
    PT_CMD_RUN_SCRIPT, // args[0..1] = script address (low, high)
    PT_CMD_GIVE_MON,   // args[0] = species, args[1] = level
    PT_CMD_GIVE_ITEM,  // args[0] = item, args[1] = count
    PT_CMD_HEAL,       // heal the party
    PT_CMD_READ_PARTY, // fill gStrataPlaytestStatus.party
    PT_CMD_GET_VAR,    // value = VarGet(args[0])
    PT_CMD_GET_FLAG,   // value = FlagGet(args[0])
    PT_CMD_COUNT_ITEM, // value = how many of item args[0] are in the bag
};

// PT_CMD_QUICKSTART options
#define PT_OPT_NO_ENCOUNTERS  (1 << 0)
#define PT_OPT_NO_COLLISION   (1 << 1)
#define PT_OPT_INSTANT_TEXT   (1 << 2)
#define PT_OPT_NO_BATTLE_ANIM (1 << 3)
#define PT_OPT_FEMALE         (1 << 4)

#define PT_MAX_ITEMS 16
#define PT_MAX_VARS  24
#define PT_MAX_FLAGS 48

// All fields are u16 so the layout has no padding; harness.py packs it.
struct StrataPlaytestScenario
{
    u16 mapGroup;
    u16 mapNum;
    s16 x;
    s16 y;
    u16 story;
    u16 era;
    u16 options;
    u16 partyCount;
    u16 party[PARTY_SIZE][2];       // species, level
    u16 items[PT_MAX_ITEMS][2];     // item, count
    u16 vars[PT_MAX_VARS][2];       // var, value
    u16 flags[PT_MAX_FLAGS];        // flags to set
};

struct StrataPlaytestCommand
{
    u16 seq;
    u16 cmd;
    u16 args[4];
    struct StrataPlaytestScenario scenario;
};

struct StrataPlaytestMon
{
    u16 species;
    u8 level;
    u8 isEgg;
    u16 hp;
    u16 maxHP;
};

// Written by the game every frame (party only on PT_CMD_READ_PARTY).
struct StrataPlaytestStatus
{
    u32 magic;
    u32 frames;       // main loop iterations: stops growing when the game hangs
    u32 callback1;
    u32 callback2;
    u16 doneSeq;
    u16 result;       // 1 done, 0xFFFF refused (wrong state)
    u16 mapGroup;
    u16 mapNum;
    s16 x;
    s16 y;
    u16 story;
    u16 era;
    u8 facing;
    u8 moving;        // gPlayerAvatar.tileTransitionState
    u8 inBattle;
    u8 battleOutcome;
    u32 battleTypeFlags;
    u8 scriptActive;  // ScriptContext_IsEnabled
    u8 fieldLocked;   // ArePlayerFieldControlsLocked
    u8 fadeActive;
    u8 partyCount;
    struct StrataPlaytestMon party[PARTY_SIZE];
    // Layout facts the harness needs to walk the text printer list
    // (sFirstTextPrinter in text.c) and gTasks itself.
    u8 printerNext;       // offsetof(struct TextPrinter, nextPrinter)
    u8 printerState;      // offsetof(struct TextPrinter, state)
    u8 printerActiveByte; // byte holding the .active bit
    u8 printerActiveMask;
    u8 printerWindowId;   // offsetof(struct TextPrinter, printerTemplate.windowId)
    u8 sizeofTask;
    u8 renderStateWait;   // RENDER_STATE_WAIT
    u8 renderStateWaitSE; // RENDER_STATE_WAIT_SE
    u8 scriptNative;      // offsetof(struct ScriptContext, nativePtr), for sGlobalScriptContext
    u8 scriptMode;        // offsetof(struct ScriptContext, mode)
    u16 padding;
    u32 value;            // result of PT_CMD_GET_VAR / GET_FLAG / COUNT_ITEM
};

#if STRATA_PLAYTEST
void StrataPlaytest_Poll(void);
#endif

#endif // GUARD_STRATA_PLAYTEST_H
