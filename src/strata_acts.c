#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "strata_acts.h"
#include "strata_story.h"
#include "string_util.h"
#include "strings.h"
#include "text.h"
#include "constants/battle_ai.h"
#include "constants/characters.h"
#include "constants/flags.h"
#include "constants/vars.h"

// The acts of Strata, one per era. The STRATA rig at the field station loads them
// in order and only moves up: see data/maps/StrataFieldStation/scripts.inc.

// What the rig calls each layer: the formation the reconstruction comes from.
static const u8 *const sLayerNames[ERA_COUNT] =
{
    [ERA_HELL_CREEK]    = COMPOUND_STRING("Hell Creek Fm, 66.04 Ma"),
    [ERA_IMPACT_WINTER] = COMPOUND_STRING("Tullock Fm, 66.04 Ma +1 yr"),
    [ERA_CORRAL_BLUFFS] = COMPOUND_STRING("Denver Fm, 65.7-65.4 Ma"),
    [ERA_BIGHORN_PETM]  = COMPOUND_STRING("Willwood Fm, 56 Ma"),
    [ERA_GREEN_RIVER]   = COMPOUND_STRING("Green River Fm, 50 Ma"),
    [ERA_WHITE_RIVER]   = COMPOUND_STRING("Brule Fm, 32 Ma"),
    [ERA_ASHFALL]       = COMPOUND_STRING("Ashfall, 11.9 Ma"),
    [ERA_TRAP_CAVE]     = COMPOUND_STRING("Trap Cave, 20,000 yrs ago"),
    [ERA_EPILOGUE]      = COMPOUND_STRING("Today"),
};

// ---------------------------------------------------------------------------
// Dr. Halvorsen (S2). Talking to her in the field station gives two parts:
//   1. the science of the layer, by VAR_STRATA_STORY (sMentorLines, the Tyrannosaurus variant);
//   2. the people, by VAR_STRATA_SUBPLOT against the story: where the next interlude waits if
//      one is due (sMentorBeatDue), else what she makes of the last one (sMentorSubplotLines).
// Her voice: careful, warm, and she says how sure she is. Numbers are hedged where the
// literature is (docs/strata_outline.md §5). The theme: what survives, why, and what we keep.
// test/strata_story.c formats every story x subplot and checks the widths.
// ---------------------------------------------------------------------------

// The science of each story value.
static const u8 *const sMentorLines[STORY_IN_ACT(ERA_EPILOGUE) + 1] =
{
    [1] = COMPOUND_STRING(
        "The rig is calibrated to the Hell\n"
        "Creek layer, about 66 million years\l"
        "old.\p"
        "It can only rebuild what the rock\n"
        "records. Where the record is silent\l"
        "it makes a best guess, and says so."),
    [STORY_IN_ACT(ERA_HELL_CREEK)] = COMPOUND_STRING(
        "You saw tyrannosaur tracks by the\n"
        "river? Be careful up on that bluff.\p"
        "In this layer a mammal is a snack.\n"
        "Out there, surviving counts as\l"
        "winning."),
    [STORY_ACT_DONE(ERA_HELL_CREEK)] = COMPOUND_STRING(
        "You stood your ground against a\n"
        "TYRANNOSAURUS! Remarkable.\p"
        "The rig is ready for the next layer:\n"
        "the rock just above the boundary\l"
        "clay, about a year after the impact.\p"
        "That year is the model's window, not\n"
        "a date anyone measured."),
    [STORY_IN_ACT(ERA_IMPACT_WINTER)] = COMPOUND_STRING(
        "Dark, cold, and almost nothing\n"
        "growing. Soot and dust blocked much\l"
        "of the sun, probably for months.\p"
        "Crocodiles and champsosaurs are cold-\n"
        "blooded. They can go months without\l"
        "a meal. That's likely part of why\l"
        "they made it.\p"
        "This layer is about who's left, not\n"
        "who changes. Nothing new evolves\l"
        "in a year; the filter just runs."),
    [STORY_ACT_DONE(ERA_IMPACT_WINTER)] = COMPOUND_STRING(
        "Ferns! The fern spike: the first\n"
        "plants back after a disaster.\p"
        "The next good layer is a few hundred\n"
        "thousand years on, at CORRAL BLUFFS\l"
        "in Colorado. The rig is ready."),
    [STORY_IN_ACT(ERA_CORRAL_BLUFFS)] = COMPOUND_STRING(
        "Within a few hundred thousand years\n"
        "the biggest mammals were several\l"
        "times heavier than any that lived\l"
        "beside the dinosaurs.\p"
        "Palms first, then legumes, then\n"
        "bigger plant eaters, then the\l"
        "predators. The order is solid. The\l"
        "exact numbers are still being\l"
        "refined."),
    [STORY_ACT_DONE(ERA_CORRAL_BLUFFS)] = COMPOUND_STRING(
        "Next: the Bighorn Basin, Wyoming,\n"
        "56 million years ago.\p"
        "Carbon poured into the air and the\n"
        "world warmed by roughly 5 to 8\l"
        "degrees. Watch how the animals\l"
        "respond."),
    [STORY_IN_ACT(ERA_BIGHORN_PETM)] = COMPOUND_STRING(
        "The PETM heat made many mammals\n"
        "shrink. The first horses got about\l"
        "a third smaller, then grew back.\p"
        "Smaller bodies shed heat better.\n"
        "That's the leading explanation,\l"
        "not the only one."),
    [STORY_ACT_DONE(ERA_BIGHORN_PETM)] = COMPOUND_STRING(
        "The PETM carbon release took\n"
        "thousands of years. Ours is going\l"
        "roughly ten times faster, by current\l"
        "estimates. Maybe more.\p"
        "Those animals had millennia to move\n"
        "or shrink. We're giving today's far\l"
        "less time.\p"
        "Next: the Green River lakes, about\n"
        "50 million years ago. The lake mud\l"
        "kept whole fish, bats, even feathers."),
    [STORY_IN_ACT(ERA_GREEN_RIVER)] = COMPOUND_STRING(
        "Wyoming was subtropical then:\n"
        "palms, crocodiles and primates\l"
        "in the trees.\p"
        "It won't last. Over the next fifteen\n"
        "million years the world slowly\l"
        "cools."),
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
        "Open country seems to favour\n"
        "runners and burrowers. Notice who\l"
        "is missing, too."),
    [STORY_ACT_DONE(ERA_WHITE_RIVER)] = COMPOUND_STRING(
        "Next: Nebraska, 12 million years\n"
        "ago. The grasslands have arrived.\p"
        "And something terrible happened\n"
        "at one waterhole there."),
    [STORY_IN_ACT(ERA_ASHFALL)] = COMPOUND_STRING(
        "A massive eruption in Idaho, some\n"
        "1,600 km away, dropped ash on\l"
        "Nebraska.\p"
        "The animals at the waterhole didn't\n"
        "die at once. Breathing the ash made\l"
        "them sick over weeks, perhaps\l"
        "months. The small ones went first."),
    [STORY_ACT_DONE(ERA_ASHFALL)] = COMPOUND_STRING(
        "Next: the Ice Age, about 20,000\n"
        "years ago, at Natural Trap Cave.\p"
        "A sinkhole that trapped animals for\n"
        "over 100,000 years. Mammoths, lions,\l"
        "cheetah-like cats, giant bears…"),
    [STORY_IN_ACT(ERA_TRAP_CAVE)] = COMPOUND_STRING(
        "Most of these giants will be gone\n"
        "within 10,000 years.\p"
        "A changing climate, and people, who\n"
        "may already be in the Americas.\p"
        "How much each mattered is still\n"
        "argued. We don't know."),
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
        "The highway west of JORDAN is open.\n"
        "The descendants are out there.\l"
        "Go and meet them."),
};

// The act 1 line when the player ran from the Tyrannosaurus instead of fighting it
// (FLAG_STRATA_TREX_FLED): running is survival too.
static const u8 *const sMentorLineTyrantFled = COMPOUND_STRING(
    "You ran from a TYRANNOSAURUS and\n"
    "lived to tell it. Good.\p"
    "Small and quick: that's how mammals\n"
    "lived here.\p"
    "The rig is ready for the next layer:\n"
    "the rock just above the boundary\l"
    "clay, about a year after the impact.");

// The next interlude is due (Story_PendingBeat): where it waits.
static const u8 *const sMentorBeatDue[SUBPLOT_COUNT] =
{
    [SUBPLOT_KESSLER_OFFER] = COMPOUND_STRING(
        "A truck just pulled up outside. A\n"
        "dealer's, I think. I suspect he'll\l"
        "come in on his own."),
    [SUBPLOT_FERN_SPIKE] = COMPOUND_STRING(
        "PRIYA, the palynologist, is out at\n"
        "the LINDQVIST RANCH with her spore\l"
        "counts. Go and hear her out.\p"
        "She can read a whole forest in a\n"
        "pinch of mud."),
    [SUBPLOT_BLM_PERMIT] = COMPOUND_STRING(
        "RANGER ORTIZ wants to see you at the\n"
        "BLM office in JORDAN, west past the\l"
        "ranch. She has a permit for you."),
    [SUBPLOT_JOSIE_PIT] = COMPOUND_STRING(
        "JOSIE radioed from the arroyo. She's\n"
        "on her way in, and she sounded\l"
        "upset."),
    [SUBPLOT_HALVORSEN_REFUSAL] = COMPOUND_STRING(
        "KESSLER's truck is at the gate again.\n"
        "And THEO wants a word with both of\l"
        "us. I can guess why."),
    [SUBPLOT_PIT_DOCUMENTED] = COMPOUND_STRING(
        "RANGER ORTIZ is at the pit in SAND\n"
        "ARROYO. She asked for you by name.\p"
        "Bring your notebook. Notes are the\n"
        "one thing nobody can dig up later."),
    [SUBPLOT_AUCTION_DATE] = COMPOUND_STRING(
        "JOSIE went home to the ranch in a\n"
        "hurry. Something about a date.\p"
        "Go and see her. Gently."),
    [SUBPLOT_CITATION] = COMPOUND_STRING(
        "ORTIZ called from JORDAN. Your notes\n"
        "from the pit have done their work,\l"
        "I think."),
    [SUBPLOT_CONSORTIUM] = COMPOUND_STRING(
        "I've been on the phone all week.\n"
        "Stay a moment. I have a plan for\l"
        "the Pair."),
    [SUBPLOT_AUCTION_DAY] = COMPOUND_STRING(
        "Today is the auction at the\n"
        "LINDQVIST RANCH. I'll be there with\l"
        "the consortium's offer.\p"
        "Come with me. You built half of it."),
};

// The subplot has caught up: what Halvorsen makes of the last beat.
static const u8 *const sMentorSubplotLines[SUBPLOT_COUNT] =
{
    [SUBPLOT_NONE] = COMPOUND_STRING(
        "Keep one question in your notebook:\n"
        "why did your partner's kind make it\l"
        "through, when the giants didn't?\p"
        "Size, diet, habitat, luck. The rock\n"
        "will answer a piece at a time."),
    [SUBPLOT_KESSLER_OFFER] = COMPOUND_STRING(
        "MR. KESSLER is right that bones\n"
        "erode if no one collects them.\p"
        "He's wrong about what a bone is\n"
        "worth without its layer. I said no.\l"
        "I'd say it again."),
    [SUBPLOT_FERN_SPIKE] = COMPOUND_STRING(
        "Ferns came back first because their\n"
        "spores are small, tough, and travel\l"
        "on the wind.\p"
        "Survival often looks like that. Not\n"
        "strength: the right trait in the\l"
        "right place when the filter came."),
    [SUBPLOT_BLM_PERMIT] = COMPOUND_STRING(
        "With that permit, anything you find\n"
        "on BLM ground stays public, in a\l"
        "museum anyone can visit.\p"
        "That's the point of a permit: what\n"
        "we dig belongs to everyone."),
    [SUBPLOT_JOSIE_PIT] = COMPOUND_STRING(
        "A bone dug out with no notes loses\n"
        "its layer, its date, its neighbours.\p"
        "Whoever dug that pit kept the bone\n"
        "and threw away the science."),
    [SUBPLOT_HALVORSEN_REFUSAL] = COMPOUND_STRING(
        "His money would keep the rig running\n"
        "after I retire. I know.\p"
        "But data you sell first stops being\n"
        "science. THEO will choose for\l"
        "himself. I hope he chooses well."),
    [SUBPLOT_PIT_DOCUMENTED] = COMPOUND_STRING(
        "Your notes put that pit on federal\n"
        "ground, in a layer, on a date.\p"
        "Evidence is only careful looking\n"
        "that someone else can check."),
    [SUBPLOT_AUCTION_DATE] = COMPOUND_STRING(
        "BEA has every right to sell. The\n"
        "law is clear on private land.\p"
        "I can't ask her to be poorer for\n"
        "science. I can try to find her a\l"
        "better offer."),
    [SUBPLOT_CITATION] = COMPOUND_STRING(
        "The citation covers the digging on\n"
        "BLM land. It can't touch the sale:\l"
        "the Pair is on BEA's land."),
    [SUBPLOT_CONSORTIUM] = COMPOUND_STRING(
        "The consortium is less money than an\n"
        "auction might bring, probably.\p"
        "What it buys is a Pair that stays\n"
        "together, where anyone can study it.\p"
        "Your CODEX is our research case:\n"
        "{STR_VAR_1} species, each tied to its\l"
        "layer. Keep logging."),
    [SUBPLOT_AUCTION_DAY] = COMPOUND_STRING(
        "The Pair goes to a public museum,\n"
        "and BEA was paid. Not as much as a\l"
        "dealer might have, but fairly.\p"
        "We kept what mattered: the bones,\n"
        "and the layer they came from."),
};

// The science line for a story value (the Tyrannosaurus variant included), or NULL.
static const u8 *Mentor_ScienceLine(u32 story)
{
    if (story == STORY_ACT_DONE(ERA_HELL_CREEK) && FlagGet(FLAG_STRATA_TREX_FLED))
        return sMentorLineTyrantFled;
    if (story < ARRAY_COUNT(sMentorLines))
        return sMentorLines[story];
    return NULL;
}

// The people line for a story value and subplot: the beat that is due, or the last one played.
static const u8 *Mentor_PeopleLine(u32 story, u32 subplot)
{
    u32 beat = Story_PendingBeat(story, subplot);

    if (story == 0)
        return NULL;
    if (beat != SUBPLOT_NONE)
        return sMentorBeatDue[beat];
    if (subplot < SUBPLOT_COUNT)
        return sMentorSubplotLines[subplot];
    return NULL;
}

// The wild AI flags of boss battles must stay the plain "smart trainer" set: scripts set
// them as the number STRATA_BOSS_AI_FLAGS, which assembly can't build from AI_FLAG_*.
STATIC_ASSERT(STRATA_BOSS_AI_FLAGS == (AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_TRY_TO_FAINT | AI_FLAG_CHECK_VIABILITY),
              BossAiFlagsMatchTheScriptConstant);

u32 Strata_GetCurrentAct(void)
{
    return VarGet(VAR_STRATA_STORY) / 2;
}

// The Colby gate (roadmap S3): once the Ice Age boss is done, the rig holds "Today" back until
// the player has read the late-glacial sub-layer, the Colby site, ~13 ka (FLAG_STRATA_COLBY_SEEN,
// set by the Clovis point in data/maps/StrataColby/scripts.inc). Until then it only offers to
// re-enter the Ice Age layer, where the sub-layer marker stands by the anchor.
bool32 Strata_IsTodayGated(void)
{
    return VarGet(VAR_STRATA_STORY) == STORY_ACT_DONE(ERA_TRAP_CAVE) && !FlagGet(FLAG_STRATA_COLBY_SEEN);
}

// Why, in the rig's words. Strata_RigQuery puts it in front of the layer name, so the field
// station's "STRATA RIG: {STR_VAR_1}.\nEnter the reconstruction?" reads it out first (rule R-b:
// each layer is chained from the one below it).
static const u8 sText_TodayGated[] = _(
    "Today can't load yet.\p"
    "Each layer is chained from the one\n"
    "below. The Colby sub-layer, about\l"
    "13,000 years ago, isn't read.\p"
    "Its marker stands by the Ice Age\n"
    "anchor.\p");

const u8 *Strata_GetTodayGateText(void)
{
    return sText_TodayGated;
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
    if (story % 2 == 0 || Strata_IsTodayGated())
        return RIG_REENTER;
    return RIG_NEXT;
}

// The era the rig loads next (Strata_RigLoadNext, and the forecast before it), or
// ERA_COUNT if it has nothing to load.
u32 Strata_GetRigTargetEra(void)
{
    switch (Strata_GetRigState())
    {
    case RIG_FIRST:
        return ERA_HELL_CREEK;
    case RIG_NEXT:
        return Strata_GetCurrentAct() + 1;
    default:
        return ERA_COUNT;
    }
}

// What the rig calls `era`'s layer ("Denver Fm, 65.7-65.4 Ma"), or an empty string.
const u8 *Strata_GetLayerName(u32 era)
{
    if (era >= ERA_COUNT || sLayerNames[era] == NULL)
        return gText_EmptyString2;
    return sLayerNames[era];
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
    gStringVar1[0] = EOS;
    if (Strata_IsTodayGated())
        StringCopy(gStringVar1, sText_TodayGated);
    if (act < ERA_COUNT && sLayerNames[act] != NULL)
        StringAppend(gStringVar1, sLayerNames[act]);
    gSpecialVar_0x8006 = (act == ERA_EPILOGUE);
    gSpecialVar_Result = state;
}

// special Strata_RigLoadNext
// Moves the world up to the next act: descents, then extinctions.
// Output: as special Strata_AdvanceEra (VAR_0x8005 = mons lost, STR_VAR_1/2).
void Strata_RigLoadNext(void)
{
    u32 act = Strata_GetRigTargetEra();

    if (act >= ERA_COUNT)
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
// Output: gStringVar4 = Dr. Halvorsen's lines for the current story and subplot (science, then
// people, as two parts of one message). STR_VAR_1 = the research case (Codex species).
void Strata_BufferMentorText(void)
{
    u32 story = VarGet(VAR_STRATA_STORY);
    const u8 *science = Mentor_ScienceLine(story);
    const u8 *people = Mentor_PeopleLine(story, VarGet(VAR_STRATA_SUBPLOT));
    u8 *end;

    if (science == NULL)
        science = COMPOUND_STRING("Keep up the good work out there.");
    Strata_StoryBufferCaseCount();
    end = StringExpandPlaceholders(gStringVar4, science);
    if (people != NULL)
    {
        *end++ = CHAR_PROMPT_CLEAR;
        StringExpandPlaceholders(end, people);
    }
}
