#ifndef GUARD_CONSTANTS_STRATA_H
#define GUARD_CONSTANTS_STRATA_H

// Acts of the game, oldest first. Each era is one rock layer the player climbs into.
// The current era is stored in VAR_STRATA_ERA.
enum StrataEra
{
    ERA_PRESENT_DIG,    // Prologue: present-day dig site, Hell Creek, MT
    ERA_HELL_CREEK,     // 66.04 Ma: last days of the dinosaurs
    ERA_IMPACT_WINTER,  // 66.04 Ma + ~1 yr: Chicxulub aftermath
    ERA_CORRAL_BLUFFS,  // ~65.7-65.4 Ma: mammal recovery
    ERA_BIGHORN_PETM,   // ~56 Ma: Paleocene-Eocene Thermal Maximum
    ERA_GREEN_RIVER,    // ~52-46 Ma: subtropical Eocene lakes
    ERA_WHITE_RIVER,    // ~33 Ma: Eocene-Oligocene cooling
    ERA_ASHFALL,        // ~11.9 Ma: grasslands and supereruption
    ERA_TRAP_CAVE,      // ~20 ka: Ice Age megafauna
    ERA_EPILOGUE,       // Present day
    ERA_COUNT,
};

// Selection pressures. Each is a hidden per-mon counter stored in one of the
// (otherwise unused) contest stats, see sPressureDataIds in src/selection.c.
enum SelectionPressure
{
    PRESSURE_FOREST,     // MON_DATA_COOL:   time spent in closed, wooded habitat
    PRESSURE_OPEN,       // MON_DATA_BEAUTY: time spent in open plains / grassland
    PRESSURE_WATER,      // MON_DATA_CUTE:   time spent in or near water
    PRESSURE_PLANT_DIET, // MON_DATA_SMART:  plant foods eaten
    PRESSURE_MEAT_DIET,  // MON_DATA_TOUGH:  meat foods eaten / prey taken
    PRESSURE_HEAT,       // MON_DATA_SHEEN:  time spent in hot climates
    PRESSURE_COUNT,
    PRESSURE_NONE = PRESSURE_COUNT, // Default descendant, chosen when nothing else scores higher
};

// Story progress (VAR_STRATA_STORY): 0 new game, 1 starter chosen, then for each
// act N (= its era): 2N while in it, 2N+1 once its boss is done. The epilogue is
// act ERA_EPILOGUE and has no "done" step. See src/strata_acts.c.
#define STORY_IN_ACT(act)    ((act) * 2)
#define STORY_ACT_DONE(act)  ((act) * 2 + 1)

// Results of special Strata_RigQuery.
#define RIG_IDLE      0 // No starter yet
#define RIG_FIRST     1 // Load the first layer (no warning, nothing to lose)
#define RIG_REENTER   2 // Re-enter the current layer
#define RIG_NEXT      3 // Load the next layer: one-way, extinctions apply
#define RIG_COMPLETE  4 // The present is loaded; nothing above it

#endif // GUARD_CONSTANTS_STRATA_H
