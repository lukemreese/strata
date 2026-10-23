#include "global.h"
#include "event_data.h"
#include "lineage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "selection.h"
#include "string_util.h"
#include "test/overworld_script.h"
#include "test/test.h"
#include "constants/vars.h"
#include "../src/data/strata_species_eras.h"

// These tests use the lineages in src/data/lineages.h.

#define FIRST_STRATA_SPECIES (SPECIES_CUSTOM_START + 1)
#define STRATA_SPECIES_COUNT (SPECIES_CUSTOM_END - FIRST_STRATA_SPECIES)

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
}

TEST("Lineage_GetDescendant leaves species without a descent unchanged")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_WOBBUFFET, ERA_CORRAL_BLUFFS, pressures), SPECIES_WOBBUFFET);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_CIMOLESTES, ERA_HELL_CREEK, pressures), SPECIES_CIMOLESTES);
}

TEST("Lineage_GetDescendant picks the default option with no pressures")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GALLINULOID);
}

TEST("Lineage_GetDescendant picks the eligible option with the highest pressure")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_WATER] = DESCENT_MIN_SCORE + 10;
    pressures[PRESSURE_PLANT_DIET] = DESCENT_MIN_SCORE + 30;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GASTORNIS);
    pressures[PRESSURE_WATER] = DESCENT_MIN_SCORE + 40;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_PRESBYORNIS);
    // Ties go to the option listed first.
    pressures[PRESSURE_PLANT_DIET] = DESCENT_MIN_SCORE + 40;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_PRESBYORNIS);
}

TEST("Lineage_GetDescendant keeps the default until a branch reaches its threshold")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_WATER] = DESCENT_MIN_SCORE - 1;
    pressures[PRESSURE_PLANT_DIET] = DESCENT_MIN_SCORE - 1;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GALLINULOID);
    pressures[PRESSURE_WATER] = DESCENT_MIN_SCORE;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_PRESBYORNIS);
}

TEST("Lineage_GetDescendant ignores a higher pressure that is below its threshold")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    // Gastornis needs PLANT_DIET >= 64; Presbyornis is eligible with a lower counter.
    ASSUME(DESCENT_MIN_SCORE == 64);
    pressures[PRESSURE_WATER] = 64;
    pressures[PRESSURE_PLANT_DIET] = 63;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_PRESBYORNIS);
}

TEST("The dog lineage needs a clear meat diet to leave the coyote line")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_MEAT_DIET] = DESCENT_MIN_SCORE - 1;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_HESPEROCYON, ERA_ASHFALL, pressures), SPECIES_LEPTOCYON);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_LEPTOCYON, ERA_TRAP_CAVE, pressures), SPECIES_CANIS);
    pressures[PRESSURE_MEAT_DIET] = DESCENT_MIN_SCORE;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_HESPEROCYON, ERA_ASHFALL, pressures), SPECIES_EPICYON);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_LEPTOCYON, ERA_TRAP_CAVE, pressures), SPECIES_AENOCYON);
}

TEST("Every descent branch needs more pressure than knockouts can give")
{
    u32 species, era;
    const struct DescentOption *option;

    for (species = SPECIES_NONE + 1; species < NUM_SPECIES; species++)
    {
        for (era = 0; era < ERA_COUNT; era++)
        {
            option = Lineage_GetDescentOptions(species, era);
            if (option == NULL)
                continue;
            for (; option->species != SPECIES_NONE; option++)
            {
                if (option->pressure == PRESSURE_NONE)
                    EXPECT_EQ(Lineage_GetOptionMinScore(option), 0);
                else
                    EXPECT_GT(Lineage_GetOptionMinScore(option), SELECTION_PREY_CAP);
            }
        }
    }
}

TEST("A dog lineage that only hunts reaches the coyote")
{
    u32 era, i;
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(mon, SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    // Hundreds of knockouts in every era, then the next layer loads.
    for (era = ERA_IMPACT_WINTER; era <= ERA_TRAP_CAVE; era++)
    {
        for (i = 0; i < 200; i++)
            Selection_OnPreyTaken(mon);
        EXPECT_EQ(GetMonData(mon, MON_DATA_TOUGH), SELECTION_PREY_CAP);
        Lineage_AdvanceToEra(era);
    }
    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_CANIS);
}

TEST("Lineage_GetDescendant ignores pressures no option selects for")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_HEAT] = 255;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_ASTERIORNIS, ERA_BIGHORN_PETM, pressures), SPECIES_GALLINULOID);
}

// Every branch of docs/strata_outline.md §2.11, at its threshold and one below.
TEST("Each lineage branch needs its pressure to reach its threshold")
{
    u32 i;
    static const struct
    {
        u16 ancestor;
        u8 era;
        u8 pressure;
        u8 minScore;
        u16 byDefault;
        u16 branch;
    } sBranches[] =
    {
        { SPECIES_HESPEROCYON,  ERA_ASHFALL,      PRESSURE_MEAT_DIET,  64, SPECIES_LEPTOCYON,   SPECIES_EPICYON },
        { SPECIES_LEPTOCYON,    ERA_TRAP_CAVE,    PRESSURE_MEAT_DIET,  64, SPECIES_CANIS,       SPECIES_AENOCYON },
        { SPECIES_LEPTOCYON,    ERA_TRAP_CAVE,    PRESSURE_OPEN,       96, SPECIES_CANIS,       SPECIES_VULPES },
        { SPECIES_ASTERIORNIS,  ERA_BIGHORN_PETM, PRESSURE_WATER,      64, SPECIES_GALLINULOID, SPECIES_PRESBYORNIS },
        { SPECIES_ASTERIORNIS,  ERA_BIGHORN_PETM, PRESSURE_PLANT_DIET, 64, SPECIES_GALLINULOID, SPECIES_GASTORNIS },
        { SPECIES_GALLINULOID,  ERA_TRAP_CAVE,    PRESSURE_OPEN,       96, SPECIES_MELEAGRIS,   SPECIES_CENTROCERCUS },
        { SPECIES_PROTOCHELYD,  ERA_ASHFALL,      PRESSURE_HEAT,      160, SPECIES_CHELYDRA,    SPECIES_MACROCHELYS },
        { SPECIES_MESOHIPPUS,   ERA_ASHFALL,      PRESSURE_FOREST,     64, SPECIES_PROTOHIPPUS, SPECIES_HYPOHIPPUS },
        { SPECIES_SUBHYRACODON, ERA_ASHFALL,      PRESSURE_OPEN,       64, SPECIES_TELEOCERAS,  SPECIES_APHELOPS },
    };

    for (i = 0; i < ARRAY_COUNT(sBranches); i++)
    {
        u8 pressures[PRESSURE_COUNT] = {0};
        pressures[sBranches[i].pressure] = sBranches[i].minScore - 1;
        EXPECT_EQ(Lineage_GetDescendant(sBranches[i].ancestor, sBranches[i].era, pressures), sBranches[i].byDefault);
        pressures[sBranches[i].pressure] = sBranches[i].minScore;
        EXPECT_EQ(Lineage_GetDescendant(sBranches[i].ancestor, sBranches[i].era, pressures), sBranches[i].branch);
    }
}

TEST("A dog lineage steered both ways takes the branch with the higher counter")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    pressures[PRESSURE_MEAT_DIET] = 100;
    pressures[PRESSURE_OPEN] = 96;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_LEPTOCYON, ERA_TRAP_CAVE, pressures), SPECIES_AENOCYON);
    pressures[PRESSURE_OPEN] = 120;
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_LEPTOCYON, ERA_TRAP_CAVE, pressures), SPECIES_VULPES);
}

TEST("Single-path lineages descend by default")
{
    u8 pressures[PRESSURE_COUNT] = {0};
    // Teilhardina's line stays within the omomyiform primates (outline §5 H4).
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_TEILHARDINA, ERA_GREEN_RIVER, pressures), SPECIES_OMOMYS);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_HYRACHYUS, ERA_WHITE_RIVER, pressures), SPECIES_SUBHYRACODON);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_PARAMYS, ERA_WHITE_RIVER, pressures), SPECIES_ISCHYROMYS);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_DOUGLASSCIUR, ERA_TRAP_CAVE, pressures), SPECIES_CYNOMYS);
    EXPECT_EQ(Lineage_GetDescendant(SPECIES_COSORYX, ERA_TRAP_CAVE, pressures), SPECIES_ANTILOCAPRA);
}

TEST("A rhino lineage from the Bridger Basin dies out by the Ice Age on either branch")
{
    u8 pressure = DESCENT_MIN_SCORE;
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][0];

    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    CreateMon(mon, SPECIES_HYRACHYUS, 30, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_CHELYDRA, 30, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_WHITE_RIVER);
    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_SUBHYRACODON);
    SetMonData(mon, MON_DATA_BEAUTY, &pressure); // PRESSURE_OPEN: the White River flats
    Lineage_AdvanceToEra(ERA_ASHFALL);
    EXPECT_EQ(GetMonData(mon, MON_DATA_SPECIES), SPECIES_APHELOPS);
    Lineage_AdvanceToEra(ERA_TRAP_CAVE);
    EXPECT_EQ(Lineage_GetFirstExtinctSpecies(), SPECIES_APHELOPS);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_CHELYDRA);
}

// Roster `first_era` (src/data/strata_species_eras.h) and the descent table agree:
// a lineage can't turn into a species before that species exists, and the
// ancestor must exist before the era it descends in.
TEST("Every descent happens after its ancestor's first era, into a species that exists by then")
{
    u32 species, era;
    const struct DescentOption *option;

    for (species = FIRST_STRATA_SPECIES; species < SPECIES_CUSTOM_END; species++)
    {
        for (era = 0; era < ERA_COUNT; era++)
        {
            option = Lineage_GetDescentOptions(species, era);
            if (option == NULL)
                continue;
            EXPECT_LT(sStrataSpeciesEras[species].firstEra, era);
            for (; option->species != SPECIES_NONE; option++)
                EXPECT_LE(sStrataSpeciesEras[option->species].firstEra, era);
        }
    }
}

// The focal bonus (+40 BST, tools/strata/gen_species.py) is for the three starter
// lines: every species a starter can become, and nothing else.
TEST("Exactly the species a starter can become are focal")
{
    static const u16 sStarters[] = { SPECIES_CIMOLESTES, SPECIES_ASTERIORNIS, SPECIES_EMARGINACHEL };
    bool8 reachable[STRATA_SPECIES_COUNT] = {0};
    bool8 next[STRATA_SPECIES_COUNT];
    u8 pressures[PRESSURE_COUNT];
    u32 i, era, p;

    for (i = 0; i < ARRAY_COUNT(sStarters); i++)
        reachable[sStarters[i] - FIRST_STRATA_SPECIES] = TRUE;
    for (era = ERA_HELL_CREEK; era < ERA_COUNT; era++)
    {
        memcpy(next, reachable, sizeof(next));
        for (i = 0; i < STRATA_SPECIES_COUNT; i++)
        {
            if (!reachable[i])
                continue;
            // Every branch is steered by a single pressure, so trying each one
            // alone (and none) reaches every option.
            for (p = 0; p <= PRESSURE_COUNT; p++)
            {
                u16 descendant;
                memset(pressures, 0, sizeof(pressures));
                if (p < PRESSURE_COUNT)
                    pressures[p] = 255;
                descendant = Lineage_GetDescendant(i + FIRST_STRATA_SPECIES, era, pressures);
                EXPECT(descendant >= FIRST_STRATA_SPECIES && descendant < SPECIES_CUSTOM_END);
                if (descendant >= FIRST_STRATA_SPECIES && descendant < SPECIES_CUSTOM_END)
                    next[descendant - FIRST_STRATA_SPECIES] = TRUE;
            }
        }
        memcpy(reachable, next, sizeof(reachable));
    }
    for (i = 0; i < STRATA_SPECIES_COUNT; i++)
        EXPECT_EQ(sStrataSpeciesEras[i + FIRST_STRATA_SPECIES].focal, reachable[i]);
}

TEST("Lineage_DescendMon keeps the mon's identity and recalculates stats")
{
    struct Pokemon mon;
    u8 pressure = DESCENT_MIN_SCORE;
    CreateMon(&mon, SPECIES_ASTERIORNIS, 30, 0x12345678, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_CUTE, &pressure); // PRESSURE_WATER

    EXPECT(Lineage_DescendMon(&mon, ERA_BIGHORN_PETM));
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SPECIES), SPECIES_PRESBYORNIS);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_LEVEL), 30);
    EXPECT_EQ(GetLevelFromMonExp(&mon), 30);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_PERSONALITY), 0x12345678);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_CUTE), 0);

    // Max HP must match a freshly recalculated Presbyornis.
    {
        u32 maxHp = GetMonData(&mon, MON_DATA_MAX_HP);
        CalculateMonStats(&mon);
        EXPECT_EQ(GetMonData(&mon, MON_DATA_MAX_HP), maxHp);
    }
}

TEST("Lineage_DescendMon renames default nicknames but keeps custom ones")
{
    struct Pokemon mon;
    u8 nickname[POKEMON_NAME_BUFFER_SIZE];
    static const u8 sCustomName[] = _("Pip");

    CreateMon(&mon, SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_DescendMon(&mon, ERA_BIGHORN_PETM);
    GetMonData(&mon, MON_DATA_NICKNAME, nickname);
    EXPECT_EQ(StringCompare(nickname, GetSpeciesName(SPECIES_GALLINULOID)), 0);

    CreateMon(&mon, SPECIES_ASTERIORNIS, 5, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&mon, MON_DATA_NICKNAME, sCustomName);
    Lineage_DescendMon(&mon, ERA_BIGHORN_PETM);
    GetMonData(&mon, MON_DATA_NICKNAME, nickname);
    EXPECT_EQ(StringCompare(nickname, sCustomName), 0);
}

TEST("Lineage_AdvanceToEra passes a lineage through every intermediate era")
{
    ResetStrata();
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);

    // Cimolestes -> Protictis (Corral Bluffs) -> Miacis (Green River) -> Hesperocyon (White River)
    // Emarginachelys -> Protochelydra (Corral Bluffs), then stasis until Ashfall
    EXPECT_EQ(Lineage_AdvanceToEra(ERA_WHITE_RIVER), 4);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_HESPEROCYON);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_SPECIES), SPECIES_PROTOCHELYD);
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_WHITE_RIVER);
}

TEST("Lineage_AdvanceToEra does nothing when moving to the current or an earlier era")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_GREEN_RIVER);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);

    EXPECT_EQ(Lineage_AdvanceToEra(ERA_HELL_CREEK), 0);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_CIMOLESTES);
    EXPECT_EQ(VarGet(VAR_STRATA_ERA), ERA_GREEN_RIVER);
}

TEST("Lineage_AdvanceToEra also descends mons stored in the PC")
{
    struct BoxPokemon *boxMon = GetBoxedMonPtr(TOTAL_BOXES_COUNT - 1, IN_BOX_COUNT - 1);
    ResetStrata();
    // A party mon, so the PC turtle isn't brought out to fill an empty party.
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(boxMon, SPECIES_EMARGINACHEL, 10, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_CORRAL_BLUFFS);
    EXPECT_EQ(GetBoxMonData(boxMon, MON_DATA_SPECIES), SPECIES_PROTOCHELYD);
    ZeroBoxMonData(boxMon);
}

TEST("The impact wipes out dinosaur lineages in the party and PC")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TYRANNOSAUR, 12, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][2], SPECIES_TRICERATOPS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 0), SPECIES_ANKYLOSAURUS, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(0, 1), SPECIES_CHAMPSOSAUR, 10, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);

    EXPECT_EQ(Lineage_GetExtinctionCount(), 3);
    EXPECT_EQ(Lineage_GetFirstExtinctSpecies(), SPECIES_TYRANNOSAUR);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_CIMOLESTES);
    EXPECT_EQ(GetBoxMonData(GetBoxedMonPtr(0, 0), MON_DATA_SPECIES), SPECIES_NONE);
    EXPECT_EQ(GetBoxMonData(GetBoxedMonPtr(0, 1), MON_DATA_SPECIES), SPECIES_CHAMPSOSAUR);
}

TEST("An extinction brings a survivor from the PC rather than leave the party empty")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TYRANNOSAUR, 12, 0, OTID_STRUCT_PLAYER_ID);
    CreateBoxMon(GetBoxedMonPtr(3, 5), SPECIES_LEPISOSTEUS, 8, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);

    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_LEPISOSTEUS);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_LEVEL), 8);
    EXPECT_EQ(GetBoxMonData(GetBoxedMonPtr(3, 5), MON_DATA_SPECIES), SPECIES_NONE);
}

TEST("An extinction with no survivors anywhere gives the player a survivor")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TYRANNOSAUR, 12, 0, OTID_STRUCT_PLAYER_ID);

    Lineage_AdvanceToEra(ERA_IMPACT_WINTER);

    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_MESODMA);
}

TEST("A lineage that descends into a survivor escapes the extinction")
{
    u8 pressure = 100;
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_ASHFALL);
    // Epicyon has no descendant and dies out; Leptocyon becomes the coyote.
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_EPICYON, 40, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_LEPTOCYON, 40, 0, OTID_STRUCT_PLAYER_ID);
    SetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_TOUGH, &pressure); // meat diet -> dire wolf

    Lineage_AdvanceToEra(ERA_TRAP_CAVE);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_AENOCYON);

    // ...and the dire wolf in turn dies out at the end of the Ice Age.
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_CANIS, 40, 0, OTID_STRUCT_PLAYER_ID);
    Lineage_AdvanceToEra(ERA_EPILOGUE);
    EXPECT_EQ(CalculatePlayerPartyCount(), 1);
    EXPECT_EQ(GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES), SPECIES_CANIS);
}

TEST("special Strata_AdvanceEra reports extinctions for the message")
{
    ResetStrata();
    VarSet(VAR_STRATA_ERA, ERA_HELL_CREEK);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_CIMOLESTES, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][1], SPECIES_ANZU, 10, 0, OTID_STRUCT_PLAYER_ID);
    CreateMon(&gParties[B_TRAINER_PLAYER][2], SPECIES_DIDELPHODON, 10, 0, OTID_STRUCT_PLAYER_ID);

    VarSet(VAR_0x8004, ERA_IMPACT_WINTER);
    RUN_OVERWORLD_SCRIPT(
        special Strata_AdvanceEra;
    );
    EXPECT_EQ(VarGet(VAR_0x8005), 2);
    EXPECT_EQ(StringCompare(gStringVar1, GetSpeciesName(SPECIES_ANZU)), 0);
}
