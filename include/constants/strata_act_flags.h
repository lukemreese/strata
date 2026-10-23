#ifndef GUARD_CONSTANTS_STRATA_ACT_FLAGS_H
#define GUARD_CONSTANTS_STRATA_ACT_FLAGS_H

// Persistent save flags and vars reserved per act, so content for each act can be
// written in parallel without colliding. Each act owns 8 flags (BASE + 0..7) and
// one var. Define names for them only inside your act's section below, e.g.
//     #define FLAG_STRATA_A3_FOUND_BONEBED (FLAG_STRATA_ACT3_BASE + 0)
// For one-shot state that may reset on map load, prefer FLAG_TEMP_* (but note
// FLAG_TEMP_11..1F are reserved for forage on maps that have forage).
// This header is also included by data/map_events.s, so the names work in map
// data (object flags, trigger vars) as well as in scripts. Keep it #defines only.
// The flags are FLAG_UNUSED_0x264..0x2AB and the vars VAR_UNUSED_0x40F7..0x40FE in
// include/constants/flags.h and vars.h.

// ---- Act 1: Hell Creek -------------------------------------------
#define FLAG_STRATA_ACT1_BASE 0x264
#define VAR_STRATA_ACT1 0x40F7

// The Acheroraptor pair in the Fern Glade have been dealt with (their objects hide).
#define FLAG_STRATA_A1_RAPTORS_GONE (FLAG_STRATA_ACT1_BASE + 0)
// The tyrannosaur on the River Channel bluff is gone (the act is done: it limped off, or you left).
#define FLAG_STRATA_A1_TYRANT_GONE  (FLAG_STRATA_ACT1_BASE + 1)
// VAR_STRATA_ACT1: 0 = the Fern Glade ambush has not happened yet, 1 = it has.


// ---- Act 2: impact winter ----------------------------------------
#define FLAG_STRATA_ACT2_BASE 0x26C
#define VAR_STRATA_ACT2 0x40F8

// The first visit to the Burrow Refuge has been shown (one-time text).
#define FLAG_STRATA_A2_BURROW_SEEN (FLAG_STRATA_ACT2_BASE + 0)


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

// VAR_STRATA_ACT4: 0 = the Oxyaena at the Clarks Fork ford hasn't stalked the player yet,
// 1 = the set piece is over (won, caught or fled).
#define FLAG_STRATA_ACT4_OXYAENA        (FLAG_STRATA_ACT4_BASE + 0)  // Oxyaena beaten or caught: hides it
#define FLAG_STRATA_ACT4_KIT_UPGRADED   (FLAG_STRATA_ACT4_BASE + 1)  // Coryphodon done: fishing kit upgraded once


// ---- Act 5: Green River ------------------------------------------
#define FLAG_STRATA_ACT5_BASE 0x284
#define VAR_STRATA_ACT5 0x40FB

// The Uintatherium bull (Bridger Shore) is hidden while set; set on every map load, cleared
// by the boss line (the bull charges in).
#define FLAG_STRATA_A5_BULL_HIDDEN (FLAG_STRATA_ACT5_BASE + 0)
// Set once the Patriofelis set piece (Oil-Shale Cliffs) is won or caught: it leaves.
#define FLAG_STRATA_A5_PATRIOFELIS (FLAG_STRATA_ACT5_BASE + 1)
// VAR_STRATA_ACT5: 0 until the player has seen the Fossil Lake mass-mortality scene, then 1.


// ---- Act 6: White River ------------------------------------------
#define FLAG_STRATA_ACT6_BASE 0x28C
#define VAR_STRATA_ACT6 0x40FC

// The Hyaenodon on the Toadstool Trackways has been dealt with (its object hides). Won, caught or run.
#define FLAG_STRATA_A6_HYAENODON_GONE (FLAG_STRATA_ACT6_BASE + 0)
// The Archaeotherium at the bone stash on the White River plateau is gone (the act is done).
#define FLAG_STRATA_A6_STASH_CLEARED  (FLAG_STRATA_ACT6_BASE + 1)
// VAR_STRATA_ACT6: 0 = the Hyaenodon has not been met yet (its line of sight triggers), 1 = it has.


// ---- Act 7: Ashfall ----------------------------------------------
#define FLAG_STRATA_ACT7_BASE 0x294
#define VAR_STRATA_ACT7 0x40FD

// The Epicyon at the carcass in the Savanna Woodland has been dealt with (its object hides).
#define FLAG_STRATA_A7_EPICYON_GONE (FLAG_STRATA_ACT7_BASE + 0)
// VAR_STRATA_ACT7: 0 = the haze on the horizon has not been seen yet, 1 = it has,
// 2 = the Teleoceras battle is over and the ash maps have just loaded (Weeks-later text pending),
// 3 = that text has been shown.


// ---- Act 8: Ice Age ----------------------------------------------
#define FLAG_STRATA_ACT8_BASE 0x29C
#define VAR_STRATA_ACT8 0x40FE

// The American lion pair on the Ice Age Steppe have been dealt with (their objects hide).
#define FLAG_STRATA_A8_LIONS_GONE   (FLAG_STRATA_ACT8_BASE + 0)
// The player has examined the Clovis point at the Colby site (~13 ka coda). The epilogue gate
// (story task S3) can check it before the rig offers "Today".
#define FLAG_STRATA_COLBY_SEEN      (FLAG_STRATA_ACT8_BASE + 1)
// VAR_STRATA_ACT8: 0 = the lion pair has not been met yet, 1 = it has.


// ---- Epilogue ----------------------------------------------------
#define FLAG_STRATA_EPILOGUE_BASE 0x2A4

// The black-footed ferret in the prairie-dog town has been met (its object hides).
#define FLAG_STRATA_EPI_FERRET_MET        (FLAG_STRATA_EPILOGUE_BASE + 0)
// The player has read the Pair's case in the Interpretive Center.
#define FLAG_STRATA_EPI_PAIR_SEEN         (FLAG_STRATA_EPILOGUE_BASE + 1)
// The player has been through the Hall of Lost Lineages (set by the Docent).
#define FLAG_STRATA_EPI_HALL_SEEN         (FLAG_STRATA_EPILOGUE_BASE + 2)
// Halvorsen's final peer review is done. Not set yet: C13 sets it where the
// Lv 55 battle goes (StrataInterpretive1F_EventScript_Halvorsen).
#define FLAG_STRATA_EPI_PEER_REVIEW_DONE  (FLAG_STRATA_EPILOGUE_BASE + 3)
// (4..7 are free.) There is no epilogue var: the story value 18 is the epilogue.


#endif // GUARD_CONSTANTS_STRATA_ACT_FLAGS_H
