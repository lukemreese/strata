#ifndef GUARD_CONSTANTS_STRATA_ACT_FLAGS_H
#define GUARD_CONSTANTS_STRATA_ACT_FLAGS_H

// Persistent save flags and vars reserved per act, so content for each act can be
// written in parallel without colliding. Each act owns 8 flags (BASE + 0..7) and
// one var. Define names for them only inside your act's section below, e.g.
//     #define FLAG_STRATA_A3_FOUND_BONEBED (FLAG_STRATA_ACT3_BASE + 0)
// For one-shot state that may reset on map load, prefer FLAG_TEMP_* (but note
// FLAG_TEMP_11..1F are reserved for forage on maps that have forage).
// The flags are FLAG_UNUSED_0x264..0x2AB and the vars VAR_UNUSED_0x40F7..0x40FE in
// include/constants/flags.h and vars.h.

// ---- Act 1: Hell Creek -------------------------------------------
#define FLAG_STRATA_ACT1_BASE 0x264
#define VAR_STRATA_ACT1 0x40F7


// ---- Act 2: impact winter ----------------------------------------
#define FLAG_STRATA_ACT2_BASE 0x26C
#define VAR_STRATA_ACT2 0x40F8


// ---- Act 3: Corral Bluffs ----------------------------------------
#define FLAG_STRATA_ACT3_BASE 0x274
#define VAR_STRATA_ACT3 0x40F9           // concretions cracked at Concretion Bluffs (0-3)
#define FLAG_STRATA_A3_CONCRETION_1     (FLAG_STRATA_ACT3_BASE + 0)  // cracked: the rock is gone
#define FLAG_STRATA_A3_CONCRETION_2     (FLAG_STRATA_ACT3_BASE + 1)
#define FLAG_STRATA_A3_CONCRETION_3     (FLAG_STRATA_ACT3_BASE + 2)
#define FLAG_STRATA_A3_TAENIOLABIS_DONE (FLAG_STRATA_ACT3_BASE + 3)  // the Taeniolabis mini-boss is over (won or caught)
#define FLAG_STRATA_A3_EOCONODON_GONE   (FLAG_STRATA_ACT3_BASE + 4)  // the Eoconodon boss has left the marsh


// ---- Act 4: Bighorn Basin (PETM) ---------------------------------
#define FLAG_STRATA_ACT4_BASE 0x27C
#define VAR_STRATA_ACT4 0x40FA


// ---- Act 5: Green River ------------------------------------------
#define FLAG_STRATA_ACT5_BASE 0x284
#define VAR_STRATA_ACT5 0x40FB


// ---- Act 6: White River ------------------------------------------
#define FLAG_STRATA_ACT6_BASE 0x28C
#define VAR_STRATA_ACT6 0x40FC


// ---- Act 7: Ashfall ----------------------------------------------
#define FLAG_STRATA_ACT7_BASE 0x294
#define VAR_STRATA_ACT7 0x40FD


// ---- Act 8: Ice Age ----------------------------------------------
#define FLAG_STRATA_ACT8_BASE 0x29C
#define VAR_STRATA_ACT8 0x40FE


// ---- Epilogue ----------------------------------------------------
#define FLAG_STRATA_EPILOGUE_BASE 0x2A4


#endif // GUARD_CONSTANTS_STRATA_ACT_FLAGS_H
