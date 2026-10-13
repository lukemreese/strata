#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "strata_acts.h"
#include "string_util.h"
#include "text.h"
#include "constants/vars.h"

// The acts of Strata, one per era. The STRATA rig at the field station loads them
// in order and only moves up: see data/maps/StrataFieldStation/scripts.inc.

// What the rig calls each layer: the formation the reconstruction comes from.
static const u8 *const sLayerNames[ERA_COUNT] =
{
    [ERA_HELL_CREEK]    = COMPOUND_STRING("Hell Creek Fm, 66.04 Ma"),
    [ERA_IMPACT_WINTER] = COMPOUND_STRING("Tullock Fm, 66.04 Ma +1 yr"),
    [ERA_CORRAL_BLUFFS] = COMPOUND_STRING("Denver Fm, 65.7 Ma"),
    [ERA_BIGHORN_PETM]  = COMPOUND_STRING("Willwood Fm, 56 Ma"),
    [ERA_GREEN_RIVER]   = COMPOUND_STRING("Green River Fm, 50 Ma"),
    [ERA_WHITE_RIVER]   = COMPOUND_STRING("Brule Fm, 32 Ma"),
    [ERA_ASHFALL]       = COMPOUND_STRING("Ashfall, 11.9 Ma"),
    [ERA_TRAP_CAVE]     = COMPOUND_STRING("Trap Cave, 20,000 yrs ago"),
    [ERA_EPILOGUE]      = COMPOUND_STRING("Today"),
};

// Dr. Halvorsen's line for each value of VAR_STRATA_STORY.
static const u8 *const sMentorLines[STORY_IN_ACT(ERA_EPILOGUE) + 1] =
{
    [1] = COMPOUND_STRING(
        "The rig is calibrated to the Hell\n"
        "Creek layer, 66.04 million years ago."),
    [STORY_IN_ACT(ERA_HELL_CREEK)] = COMPOUND_STRING(
        "You saw tyrannosaur tracks by the\n"
        "river? Be careful up on that bluff."),
    [STORY_ACT_DONE(ERA_HELL_CREEK)] = COMPOUND_STRING(
        "You stood your ground against a\n"
        "TYRANNOSAURUS! Remarkable.\p"
        "The rig is ready for the next layer:\n"
        "the rock just above the boundary\l"
        "clay. About a year after the impact."),
    [STORY_IN_ACT(ERA_IMPACT_WINTER)] = COMPOUND_STRING(
        "Dark, cold, and almost nothing\n"
        "growing. Soot blocked the sun.\p"
        "Crocodiles and champsosaurs are cold-\n"
        "blooded. They can go months without\l"
        "a meal. That's part of why they\l"
        "made it."),
    [STORY_ACT_DONE(ERA_IMPACT_WINTER)] = COMPOUND_STRING(
        "Ferns! The fern spike: the first\n"
        "plants back after a disaster.\p"
        "The next good layer is 300,000\n"
        "years on, at CORRAL BLUFFS in\l"
        "Colorado. The rig is ready."),
    [STORY_IN_ACT(ERA_CORRAL_BLUFFS)] = COMPOUND_STRING(
        "In 300,000 years the biggest mammals\n"
        "tripled in size.\p"
        "Palms first, then legumes, then\n"
        "bigger plant eaters, then the\l"
        "predators that hunt them."),
    [STORY_ACT_DONE(ERA_CORRAL_BLUFFS)] = COMPOUND_STRING(
        "Next: the Bighorn Basin, Wyoming,\n"
        "56 million years ago.\p"
        "Carbon poured into the air and the\n"
        "world warmed by 5 to 8 degrees.\l"
        "Watch how the animals respond."),
    [STORY_IN_ACT(ERA_BIGHORN_PETM)] = COMPOUND_STRING(
        "The PETM heat made many mammals\n"
        "shrink. The first horses got a\l"
        "third smaller, then grew back.\p"
        "Smaller bodies shed heat better.\n"
        "Bring your team to the heat, and\l"
        "their lineages will feel it too."),
    [STORY_ACT_DONE(ERA_BIGHORN_PETM)] = COMPOUND_STRING(
        "Next: the Green River lakes, about\n"
        "50 million years ago.\p"
        "The lake mud there preserved whole\n"
        "fish, bats, even feathers."),
    [STORY_IN_ACT(ERA_GREEN_RIVER)] = COMPOUND_STRING(
        "Wyoming was subtropical then:\n"
        "palms, crocodiles and primates\l"
        "in the trees.\p"
        "It won't last. The world is\n"
        "slowly cooling."),
    [STORY_ACT_DONE(ERA_GREEN_RIVER)] = COMPOUND_STRING(
        "Next: the White River badlands of\n"
        "South Dakota, 32 million years ago.\p"
        "After the Eocene-Oligocene cooling,\n"
        "the forests opened up. Many of the\l"
        "old warm-world animals are gone."),
    [STORY_IN_ACT(ERA_WHITE_RIVER)] = COMPOUND_STRING(
        "Horses with longer legs, saber-\n"
        "toothed false cats, oreodonts by\l"
        "the thousand.\p"
        "Open country favours runners."),
    [STORY_ACT_DONE(ERA_WHITE_RIVER)] = COMPOUND_STRING(
        "Next: Nebraska, 12 million years\n"
        "ago. The grasslands have arrived.\p"
        "And something terrible happened\n"
        "at one waterhole there."),
    [STORY_IN_ACT(ERA_ASHFALL)] = COMPOUND_STRING(
        "A supereruption in Idaho, 1,600 km\n"
        "away, dropped ash on Nebraska.\p"
        "The animals at the waterhole didn't\n"
        "die at once. Breathing the ash made\l"
        "them sick over weeks."),
    [STORY_ACT_DONE(ERA_ASHFALL)] = COMPOUND_STRING(
        "Next: the Ice Age, 20,000 years\n"
        "ago, at Natural Trap Cave.\p"
        "A sinkhole that trapped animals for\n"
        "over 100,000 years. Mammoths, lions,\l"
        "cheetahs, giant bears…"),
    [STORY_IN_ACT(ERA_TRAP_CAVE)] = COMPOUND_STRING(
        "Most of these giants will be gone\n"
        "within 10,000 years.\p"
        "A changing climate, and a new\n"
        "hunter in the Americas: people."),
    [STORY_ACT_DONE(ERA_TRAP_CAVE)] = COMPOUND_STRING(
        "One layer left, {PLAYER}.\p"
        "The top of the column: the ground\n"
        "under our feet. Today."),
    [STORY_IN_ACT(ERA_EPILOGUE)] = COMPOUND_STRING(
        "66 million years, one layer at a\n"
        "time. Look at your team now.\p"
        "Every lineage you carried was\n"
        "shaped by where it lived and what\l"
        "it ate, and by luck.\p"
        "The prairie past the camp is open.\n"
        "The descendants are out there.\l"
        "Go and meet them."),
};

u32 Strata_GetCurrentAct(void)
{
    return VarGet(VAR_STRATA_STORY) / 2;
}

u32 Strata_GetRigState(void)
{
    u32 story = VarGet(VAR_STRATA_STORY);

    if (story == 0)
        return RIG_IDLE;
    if (story == 1)
        return RIG_FIRST;
    if (story >= STORY_IN_ACT(ERA_EPILOGUE))
        return RIG_COMPLETE;
    if (story % 2 == 0)
        return RIG_REENTER;
    return RIG_NEXT;
}

// special Strata_RigQuery
// Output: VAR_RESULT = RIG_*
//         STR_VAR_1  = name of the layer the rig would load
//         VAR_0x8006 = TRUE if that layer is the present (nothing to warp to)
void Strata_RigQuery(void)
{
    u32 state = Strata_GetRigState();
    u32 act = Strata_GetCurrentAct();

    if (state == RIG_FIRST)
        act = ERA_HELL_CREEK;
    else if (state == RIG_NEXT)
        act++;
    if (act < ERA_COUNT && sLayerNames[act] != NULL)
        StringCopy(gStringVar1, sLayerNames[act]);
    gSpecialVar_0x8006 = (act == ERA_EPILOGUE);
    gSpecialVar_Result = state;
}

// special Strata_RigLoadNext
// Moves the world up to the next act: descents, then extinctions.
// Output: as special Strata_AdvanceEra (VAR_0x8005 = mons lost, STR_VAR_1/2).
void Strata_RigLoadNext(void)
{
    u32 state = Strata_GetRigState();
    u32 act;

    if (state == RIG_FIRST)
        act = ERA_HELL_CREEK;
    else if (state == RIG_NEXT)
        act = Strata_GetCurrentAct() + 1;
    else
        return;

    gSpecialVar_0x8004 = act;
    Strata_AdvanceEra();
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(act));
}

// special Strata_SpecialGetCurrentAct
// Output: VAR_RESULT = the act (era) the story is in
void Strata_SpecialGetCurrentAct(void)
{
    gSpecialVar_Result = Strata_GetCurrentAct();
}

// special Strata_BufferMentorText
// Output: gStringVar4 = Dr. Halvorsen's line for the current story
void Strata_BufferMentorText(void)
{
    u32 story = VarGet(VAR_STRATA_STORY);
    const u8 *line = NULL;

    if (story < ARRAY_COUNT(sMentorLines))
        line = sMentorLines[story];
    if (line == NULL)
        line = COMPOUND_STRING("Keep up the good work out there.");
    StringExpandPlaceholders(gStringVar4, line);
}
