#include "global.h"
#include "event_data.h"
#include "item.h"
#include "item_use.h"
#include "lineage.h"
#include "overworld.h"
#include "selection.h"
#include "test/test.h"
#include "constants/characters.h"
#include "constants/event_bg.h"
#include "constants/items.h"
#include "constants/map_groups.h"
#include "constants/strata.h"
#include "constants/vars.h"

// Strata forage (R3): items that heal a little and add diet pressure
// (src/selection.c, Selection_EatForage), placed as hidden items that regrow
// (tools/strata/maps/common.py, forage()).

static const struct { u16 item; u8 pressure; } sForage[] =
{
    { ITEM_FERN_FROND, PRESSURE_PLANT_DIET },
    { ITEM_PALM_FRUIT, PRESSURE_PLANT_DIET },
    { ITEM_LEGUME_POD, PRESSURE_PLANT_DIET },
    { ITEM_SEED_HEAD,  PRESSURE_PLANT_DIET },
    { ITEM_BROWSE,     PRESSURE_PLANT_DIET },
    { ITEM_LARVAE,     PRESSURE_MEAT_DIET },
    { ITEM_CARRION,    PRESSURE_MEAT_DIET },
};

TEST("Forage items are field-use bag items that heal 20 HP and add diet pressure")
{
    u32 i;
    u16 item = ITEM_NONE;
    u8 pressure = 0;
    for (i = 0; i < ARRAY_COUNT(sForage); i++)
        PARAMETRIZE { item = sForage[i].item; pressure = sForage[i].pressure; }

    EXPECT(Selection_IsForage(item));
    EXPECT_EQ(GetItemSecondaryId(item), pressure);
    EXPECT_EQ(GetItemHoldEffectParam(item), 20);
    EXPECT_EQ(GetItemPocket(item), POCKET_ITEMS);
    EXPECT_EQ(GetItemType(item), ITEM_USE_PARTY_MENU);
    EXPECT(GetItemFieldFunc(item) == ItemUseOutOfBattle_StrataForage);
    EXPECT_EQ(GetItemBattleUsage(item), 0);  // Field food, not battle medicine
    EXPECT_EQ(GetItemImportance(item), 0);
    EXPECT_EQ(GetItemPrice(item), 0);        // Can't be sold: it regrows
    EXPECT_NE(GetItemName(item)[0], EOS);
}

TEST("Only forage items count as forage")
{
    EXPECT(!Selection_IsForage(ITEM_NONE));
    EXPECT(!Selection_IsForage(ITEM_POTION));
    EXPECT(!Selection_IsForage(ITEM_WADERS));
    EXPECT(!Selection_IsForage(ITEMS_COUNT));
}

static void CreateHurtMon(struct Pokemon *mon, u32 hpLost)
{
    u32 hp;
    CreateMon(mon, SPECIES_ASTERIORNIS, 50, 0, OTID_STRUCT_PLAYER_ID);
    CalculateMonStats(mon);
    hp = GetMonData(mon, MON_DATA_MAX_HP) - hpLost;
    SetMonData(mon, MON_DATA_HP, &hp);
}

TEST("Eating plant forage heals 20 HP and adds plant pressure")
{
    struct Pokemon mon;
    CreateHurtMon(&mon, 30);
    EXPECT_EQ(Selection_EatForage(&mon, ITEM_FERN_FROND), 20);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), GetMonData(&mon, MON_DATA_MAX_HP) - 10);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SMART), FORAGE_PRESSURE);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), 0);
}

TEST("Eating animal forage adds animal pressure")
{
    struct Pokemon mon;
    CreateHurtMon(&mon, 30);
    Selection_EatForage(&mon, ITEM_CARRION);
    Selection_EatForage(&mon, ITEM_LARVAE);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_TOUGH), 2 * FORAGE_PRESSURE);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SMART), 0);
}

TEST("Forage heals up to max HP, and still adds pressure at full HP")
{
    struct Pokemon mon;
    CreateHurtMon(&mon, 5);
    EXPECT_EQ(Selection_EatForage(&mon, ITEM_BROWSE), 5);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), GetMonData(&mon, MON_DATA_MAX_HP));
    EXPECT(Selection_CanEatForage(&mon));
    EXPECT_EQ(Selection_EatForage(&mon, ITEM_BROWSE), 0);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SMART), 2 * FORAGE_PRESSURE);
}

TEST("Fainted mons, eggs and empty slots can't eat forage")
{
    struct Pokemon mon;
    bool8 isEgg = TRUE;

    CreateHurtMon(&mon, 0);
    SetMonData(&mon, MON_DATA_HP, &(u32){0});
    EXPECT(!Selection_CanEatForage(&mon));
    EXPECT_EQ(Selection_EatForage(&mon, ITEM_FERN_FROND), 0);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_SMART), 0);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), 0);

    CreateHurtMon(&mon, 10);
    SetMonData(&mon, MON_DATA_IS_EGG, &isEgg);
    EXPECT(!Selection_CanEatForage(&mon));

    ZeroMonData(&mon);
    EXPECT(!Selection_CanEatForage(&mon));
}

TEST("Eating something that isn't forage does nothing")
{
    struct Pokemon mon;
    CreateHurtMon(&mon, 30);
    EXPECT_EQ(Selection_EatForage(&mon, ITEM_POTION), 0);
    EXPECT_EQ(GetMonData(&mon, MON_DATA_HP), GetMonData(&mon, MON_DATA_MAX_HP) - 30);
}

// The species a lone `species` descends into after eating `count` of `item`.
static enum Species DescendAfterEating(enum Species species, enum StrataEra era, u16 item, u32 count)
{
    u32 i;
    ZeroPlayerPartyMons();
    VarSet(VAR_STRATA_ERA, era);
    CreateMon(&gParties[B_TRAINER_PLAYER][0], species, 40, 0, OTID_STRUCT_PLAYER_ID);
    CalculateMonStats(&gParties[B_TRAINER_PLAYER][0]);
    for (i = 0; i < count; i++)
        Selection_EatForage(&gParties[B_TRAINER_PLAYER][0], item);
    Lineage_AdvanceToEra(era + 1);
    return GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES);
}

TEST("Six plant forage take Asteriornis past the Gastornis threshold, five don't")
{
    EXPECT_LT(5 * FORAGE_PRESSURE, DESCENT_MIN_SCORE);
    EXPECT_GE(6 * FORAGE_PRESSURE, DESCENT_MIN_SCORE);
    EXPECT_EQ(DescendAfterEating(SPECIES_ASTERIORNIS, ERA_CORRAL_BLUFFS, ITEM_PALM_FRUIT, 5), SPECIES_GALLINULOID);
    EXPECT_EQ(DescendAfterEating(SPECIES_ASTERIORNIS, ERA_CORRAL_BLUFFS, ITEM_PALM_FRUIT, 6), SPECIES_GASTORNIS);
}

TEST("Carrion takes Hesperocyon to Epicyon, which knockouts alone can't")
{
    EXPECT_EQ(DescendAfterEating(SPECIES_HESPEROCYON, ERA_WHITE_RIVER, ITEM_CARRION, 5), SPECIES_LEPTOCYON);
    EXPECT_EQ(DescendAfterEating(SPECIES_HESPEROCYON, ERA_WHITE_RIVER, ITEM_CARRION, 6), SPECIES_EPICYON);
}

// Forage placement: hidden items with temp flags, so they regrow on every map load.

TEST("Hidden items can use temp flags, and stock hidden item flags still decode")
{
    struct BgEvent event = {0};

    event.bgUnion.hiddenItem.hiddenItemId = (FLAG_TEMP_11 - FLAG_HIDDEN_ITEMS_START) & 0x1FFF;
    EXPECT_EQ(GET_HIDDEN_ITEM_FLAG(&event), FLAG_TEMP_11);
    event.bgUnion.hiddenItem.hiddenItemId = FLAG_HIDDEN_ITEM_ROUTE_111_STARDUST - FLAG_HIDDEN_ITEMS_START;
    EXPECT_EQ(GET_HIDDEN_ITEM_FLAG(&event), FLAG_HIDDEN_ITEM_ROUTE_111_STARDUST);
}

TEST("Forage flags are cleared on every map load, so forage regrows")
{
    FlagSet(FLAG_TEMP_11);
    FlagSet(FLAG_TEMP_1F);
    ClearTempFieldEventData();
    EXPECT(!FlagGet(FLAG_TEMP_11));
    EXPECT(!FlagGet(FLAG_TEMP_1F));
}

static const u16 sForageMaps[] =
{
    MAP_STRATA_LEVEE, MAP_STRATA_RIVER, MAP_STRATA_BACKSWAMP,
    MAP_STRATA_LEVEE_WINTER, MAP_STRATA_RIVER_WINTER, MAP_STRATA_BACKSWAMP_WINTER,
    MAP_STRATA_PALM_FOREST, MAP_STRATA_RED_BEDS, MAP_STRATA_LAKE_FOREST, MAP_STRATA_WHITE_RIVER,
    MAP_STRATA_GRASSLAND, MAP_STRATA_STEPPE, MAP_STRATA_TRAP_CAVE, MAP_STRATA_PRAIRIE,
};

TEST("Every deep-time map has forage, hidden under temp flags")
{
    u32 i, found = 0;
    u16 map = 0;
    const struct MapHeader *header;
    for (i = 0; i < ARRAY_COUNT(sForageMaps); i++)
        PARAMETRIZE { map = sForageMaps[i]; }

    header = Overworld_GetMapHeaderByGroupAndId(MAP_GROUP(map), MAP_NUM(map));
    for (i = 0; i < header->events->bgEventCount; i++)
    {
        const struct BgEvent *event = &header->events->bgEvents[i];
        if (event->kind != BG_EVENT_HIDDEN_ITEM)
            continue;
        EXPECT(Selection_IsForage((u32)event->bgUnion.hiddenItem.item));
        EXPECT_GE(GET_HIDDEN_ITEM_FLAG(event), FLAG_TEMP_11);
        EXPECT_LE(GET_HIDDEN_ITEM_FLAG(event), FLAG_TEMP_1F);
        EXPECT_EQ((u32)event->bgUnion.hiddenItem.quantity, 1);
        found++;
    }
    EXPECT_GE(found, 1);
}
