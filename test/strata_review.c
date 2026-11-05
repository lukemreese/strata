#include "global.h"
#include "data.h"
#include "event_data.h"
#include "item.h"
#include "money.h"
#include "pokedex.h"
#include "pokemon.h"
#include "string_util.h"
#include "strata_review.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/battle_ai.h"
#include "constants/characters.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/opponents.h"
#include "constants/species.h"
#include "constants/strata.h"
#include "constants/trainers.h"
#include "constants/vars.h"

#include "../src/data/strata_species_eras.h"

// Peer review (src/data/trainers_strata.party, data/maps/StrataFieldCamp and the other hub
// maps) and the survey stipend (src/strata_review.c). The battle tests use their own trainer
// table, so the Strata one is read from the generated header here.

static const struct Trainer sStrataTrainers[DIFFICULTY_COUNT][TRAINERS_COUNT] =
{
#include "../src/data/trainers_strata.h"
};

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)

struct ExpectedTrainer
{
    u16 trainer;
    u8 era;         // every species has been met by then (first_era <= era)
    u8 minLevel;    // first animal
    u8 maxLevel;    // last animal: it sets the prize
    u8 minParty;
    u8 maxParty;
    u8 doubles;
    u8 classId;
    u8 classMoney;  // gTrainerClasses[classId].money, which src/battle_main.c sets
};

// Levels from the Q2 balance pass (tools/strata/balance.py, the headless starter runs): the last
// animal at about the level a normal player has after the act's boss (the EXP model: 15, 20, 23,
// 27, 31, 35, 41, 46), the others a level or two below. Theo's Lv 4 bird is the one the mammal
// starter faces. Halvorsen's final review (44-50) gates the ending: fair for a TEAM at about Lv 48,
// usually won at Lv 52 (7 of 9 harness runs, no items or switching).
static const struct ExpectedTrainer sExpected[] =
{
    { TRAINER_STRATA_THEO_ACT0_BIRD,   ERA_HELL_CREEK,     4,  4,  1, 1, FALSE, TRAINER_CLASS_RIVAL, 10 },
    { TRAINER_STRATA_THEO_ACT0_TURTLE, ERA_HELL_CREEK,     5,  5,  1, 1, FALSE, TRAINER_CLASS_RIVAL, 10 },
    { TRAINER_STRATA_THEO_ACT0_MAMMAL, ERA_HELL_CREEK,     5,  5,  1, 1, FALSE, TRAINER_CLASS_RIVAL, 10 },
    { TRAINER_STRATA_THEO_ACT3,        ERA_CORRAL_BLUFFS, 19, 21,  3, 3, FALSE, TRAINER_CLASS_RIVAL, 10 },
    { TRAINER_STRATA_THEO_ACT6,        ERA_WHITE_RIVER,   32, 35,  4, 4, FALSE, TRAINER_CLASS_RIVAL, 10 },
    { TRAINER_STRATA_THEO_ACT8,        ERA_TRAP_CAVE,     42, 45,  4, 4, TRUE,  TRAINER_CLASS_RIVAL, 10 },
    { TRAINER_STRATA_REVIEW_ACT1,      ERA_HELL_CREEK,    11, 13,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT2,      ERA_IMPACT_WINTER, 15, 17,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT3,      ERA_CORRAL_BLUFFS, 18, 20,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT4,      ERA_BIGHORN_PETM,  24, 26,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT5,      ERA_GREEN_RIVER,   27, 30,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT6,      ERA_WHITE_RIVER,   33, 35,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT7,      ERA_ASHFALL,       41, 42,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_REVIEW_ACT8,      ERA_TRAP_CAVE,     43, 46,  2, 4, FALSE, TRAINER_CLASS_PKMN_TRAINER_1, 12 },
    { TRAINER_STRATA_HALVORSEN,        ERA_EPILOGUE,      44, 50,  6, 6, FALSE, TRAINER_CLASS_PKMN_TRAINER_2, 14 },
};

TEST("Peer-review trainers carry only Strata species that exist by their act, at levels in range")
{
    u32 i, j;
    const struct ExpectedTrainer *e = NULL;
    const struct Trainer *trainer;
    u32 partySize, battleType;

    for (i = 0; i < ARRAY_COUNT(sExpected); i++)
        PARAMETRIZE { e = &sExpected[i]; }

    trainer = &sStrataTrainers[DIFFICULTY_NORMAL][e->trainer];
    partySize = trainer->partySize;
    battleType = trainer->battleType;
    EXPECT_GE(partySize, e->minParty);
    EXPECT_LE(partySize, e->maxParty);
    EXPECT_EQ(battleType, e->doubles ? TRAINER_BATTLE_TYPE_DOUBLES : TRAINER_BATTLE_TYPE_SINGLES);
    EXPECT_EQ(trainer->trainerClass, e->classId);
    EXPECT_NE(trainer->trainerName[0], EOS);
    EXPECT_NE(trainer->trainerPic, TRAINER_PIC_NONE);
    // A pic with only a back sprite (FRLG's Old Man) trips an assert when the battle starts.
    EXPECT(gTrainerPicInfo[trainer->trainerPic].frontPic != NULL);
    EXPECT_NE(trainer->aiFlags, 0);
    if (e->doubles)
        EXPECT_GE(partySize, 2);
    for (j = 0; j < partySize; j++)
    {
        const struct TrainerMon *mon = &trainer->party[j];
        EXPECT_GE(mon->species, FIRST_STRATA_SPECIES);
        EXPECT_LT(mon->species, SPECIES_CUSTOM_END);
        EXPECT_LE(sStrataSpeciesEras[mon->species].firstEra, e->era);
        EXPECT_GE(mon->lvl, e->minLevel);
        EXPECT_LE(mon->lvl, e->maxLevel);
        EXPECT_EQ(mon->heldItem, ITEM_NONE);
        // Levels never go down along the team: the last animal is the strongest and sets the prize.
        if (j > 0)
            EXPECT_GE(mon->lvl, trainer->party[j - 1].lvl);
    }
    EXPECT_EQ(trainer->party[partySize - 1].lvl, e->maxLevel);
}

TEST("Peer-review trainers use the RESEARCHER class and the class money the design sets")
{
    u8 name[] = _("RESEARCHER");

    EXPECT_EQ(StringCompare(gTrainerClasses[TRAINER_CLASS_PKMN_TRAINER_1].name, name), 0);
    EXPECT_EQ(StringCompare(gTrainerClasses[TRAINER_CLASS_PKMN_TRAINER_2].name, name), 0);
    EXPECT_EQ(StringCompare(gTrainerClasses[TRAINER_CLASS_RIVAL].name, name), 0);
    EXPECT_EQ(gTrainerClasses[TRAINER_CLASS_PKMN_TRAINER_1].money, 12);
    EXPECT_EQ(gTrainerClasses[TRAINER_CLASS_PKMN_TRAINER_2].money, 14);
    EXPECT_EQ(gTrainerClasses[TRAINER_CLASS_RIVAL].money, 10);
}

// The prize of a battle: 4 x the last animal's level x the class money (a double battle pays
// twice, GetTrainerMoneyToGive in src/battle_script_commands.c).
static u32 Prize(u32 trainerId)
{
    const struct Trainer *trainer = &sStrataTrainers[DIFFICULTY_NORMAL][trainerId];
    u32 prize = 4 * trainer->party[trainer->partySize - 1].lvl * gTrainerClasses[trainer->trainerClass].money;

    return trainer->battleType == TRAINER_BATTLE_TYPE_DOUBLES ? prize * 2 : prize;
}

TEST("Peer-review prizes grow with the acts and are worth a few camp-store purchases")
{
    u32 act;
    u32 capsule = gItemsInfo[ITEM_POKE_BALL].price;

    EXPECT_EQ(capsule, 200);
    EXPECT_EQ(Prize(TRAINER_STRATA_THEO_ACT0_BIRD), 160);            // 4 x 4 x 10
    EXPECT_EQ(Prize(TRAINER_STRATA_THEO_ACT0_TURTLE), 200);          // 4 x 5 x 10
    EXPECT_EQ(Prize(TRAINER_STRATA_REVIEW_ACT1), 624);               // 4 x 13 x 12
    EXPECT_EQ(Prize(TRAINER_STRATA_REVIEW_ACT8), 2208);              // 4 x 46 x 12
    EXPECT_EQ(Prize(TRAINER_STRATA_THEO_ACT8), 3600);                // a double battle: 4 x 45 x 10 x 2
    EXPECT_EQ(Prize(TRAINER_STRATA_HALVORSEN), 2800);                // 4 x 50 x 14
    for (act = 1; act <= STRATA_REVIEWER_COUNT; act++)
    {
        // At least two capsules in act 1, and every act pays more than the one before.
        EXPECT_GE(Prize(STRATA_REVIEWER_TRAINER(act)), 2 * capsule);
        if (act > 1)
            EXPECT_GT(Prize(STRATA_REVIEWER_TRAINER(act)), Prize(STRATA_REVIEWER_TRAINER(act - 1)));
    }
}

TEST("Researcher N is hidden until act N is done")
{
    u32 story, act;

    for (story = 0; story <= STORY_IN_ACT(ERA_EPILOGUE); story++)
    {
        VarSet(VAR_STRATA_STORY, story);
        RUN_OVERWORLD_SCRIPT(special Strata_HideLockedReviewers;);
        for (act = ERA_HELL_CREEK; act <= ERA_TRAP_CAVE; act++)
        {
            if (story >= STORY_ACT_DONE(act))
                EXPECT(!FlagGet(STRATA_REVIEWER_HIDE_FLAG(act)));
            else
                EXPECT(FlagGet(STRATA_REVIEWER_HIDE_FLAG(act)));
        }
    }
    // Spot checks: the ornithologist shows up when act 1 ends, the ecologist only in the epilogue run.
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_HELL_CREEK));
    Strata_HideLockedReviewers();
    EXPECT(FlagGet(FLAG_TEMP_1));
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_HELL_CREEK));
    Strata_HideLockedReviewers();
    EXPECT(!FlagGet(FLAG_TEMP_1));
    EXPECT(FlagGet(FLAG_TEMP_2));
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_EPILOGUE));
    Strata_HideLockedReviewers();
    EXPECT(!FlagGet(FLAG_TEMP_8));
}

TEST("The stipend rate starts at 150 and grows by 25 for every act done")
{
    EXPECT_EQ(Strata_ActsDone(0), 0);
    EXPECT_EQ(Strata_ActsDone(1), 0);
    EXPECT_EQ(Strata_ActsDone(STORY_IN_ACT(ERA_HELL_CREEK)), 0);
    EXPECT_EQ(Strata_ActsDone(STORY_ACT_DONE(ERA_HELL_CREEK)), 1);
    EXPECT_EQ(Strata_ActsDone(STORY_IN_ACT(ERA_IMPACT_WINTER)), 1);
    EXPECT_EQ(Strata_ActsDone(STORY_ACT_DONE(ERA_TRAP_CAVE)), 8);
    EXPECT_EQ(Strata_ActsDone(STORY_IN_ACT(ERA_EPILOGUE)), 8);
    EXPECT_EQ(Strata_StipendRate(1), 150);
    EXPECT_EQ(Strata_StipendRate(STORY_ACT_DONE(ERA_HELL_CREEK)), 175);
    EXPECT_EQ(Strata_StipendRate(STORY_ACT_DONE(ERA_CORRAL_BLUFFS)), 225);
    EXPECT_EQ(Strata_StipendRate(STORY_IN_ACT(ERA_EPILOGUE)), 350);
    EXPECT_EQ(Strata_StipendAmount(0, STORY_IN_ACT(ERA_EPILOGUE)), 0);
    EXPECT_EQ(Strata_StipendAmount(4, 1), 600);
    // The grant keeps pace with the shop: by the end one entry pays for nearly two capsules,
    // and the whole Codex (87 species) is worth about 21,000.
    EXPECT_GE(Strata_StipendRate(STORY_IN_ACT(ERA_EPILOGUE)), gItemsInfo[ITEM_POKE_BALL].price);
}

static void CatchSpecies(enum Species species)
{
    GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_SET_SEEN);
    GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_SET_CAUGHT);
}

TEST("special Strata_PayStipend pays for new Codex entries once")
{
    ResetPokedex();
    VarSet(VAR_STRATA_STIPEND_COUNT, 0);
    VarSet(VAR_STRATA_STORY, 1);
    SetMoney(&gSaveBlock1Ptr->money, 1000);

    // Nothing caught, nothing paid.
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 0);
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), 1000);

    // Three entries at the opening rate.
    CatchSpecies(SPECIES_CIMOLESTES);
    CatchSpecies(SPECIES_ANZU);
    CatchSpecies(SPECIES_MESODMA);
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 450);
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), 1450);
    EXPECT_EQ(VarGet(VAR_STRATA_STIPEND_COUNT), 3);
    {
        u8 three[] = _("3");
        u8 rate[] = _("150");
        u8 total[] = _("450");
        EXPECT_EQ(StringCompare(gStringVar1, three), 0);
        EXPECT_EQ(StringCompare(gStringVar2, rate), 0);
        EXPECT_EQ(StringCompare(gStringVar3, total), 0);
    }

    // Asking again pays nothing; catching an animal that is already logged adds nothing.
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 0);
    CatchSpecies(SPECIES_ANZU);
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 0);
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), 1450);

    // A new entry after Corral Bluffs is paid at the higher rate.
    VarSet(VAR_STRATA_STORY, STORY_ACT_DONE(ERA_CORRAL_BLUFFS));
    CatchSpecies(SPECIES_PROTICTIS);
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 225);
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), 1675);
}

TEST("special Strata_StipendBaseline counts the starter as already paid for")
{
    ResetPokedex();
    VarSet(VAR_STRATA_STIPEND_COUNT, 0);
    VarSet(VAR_STRATA_STORY, 1);
    SetMoney(&gSaveBlock1Ptr->money, 0);
    CatchSpecies(SPECIES_ASTERIORNIS);
    RUN_OVERWORLD_SCRIPT(special Strata_StipendBaseline;);
    EXPECT_EQ(VarGet(VAR_STRATA_STIPEND_COUNT), 1);
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 0);
    CatchSpecies(SPECIES_EMARGINACHEL);
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(VarGet(VAR_RESULT), 150);
}

TEST("The stipend never takes the purse past the maximum")
{
    ResetPokedex();
    VarSet(VAR_STRATA_STIPEND_COUNT, 0);
    VarSet(VAR_STRATA_STORY, STORY_IN_ACT(ERA_EPILOGUE));
    SetMoney(&gSaveBlock1Ptr->money, MAX_MONEY - 100);
    CatchSpecies(SPECIES_CHELYDRA);
    RUN_OVERWORLD_SCRIPT(special Strata_PayStipend;);
    EXPECT_EQ(GetMoney(&gSaveBlock1Ptr->money), MAX_MONEY);
}
