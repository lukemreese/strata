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


// ---- Fossils and the Gentle Deep Time option (F4, S4) -------------
// Not per act: owned by src/strata_fossils.c. FLAG_UNUSED_0x493..0x4D3 in flags.h, inside the
// saved flag array, so they cost no save space. (0x4D4..0x4DD are still free; 0x4DE..0x4E5 are
// the Ending section below.)
// One flag per lineage that can be lost to an extinction filter: fossil slot i of
// sStrataFossils (src/data/strata_fossils.h, append-only) is FLAG_STRATA_FOSSIL_BASE + i,
// set when the rig drops a party or PC animal of that species. Use Fossil_Has(species) in C.
#define FLAG_STRATA_FOSSIL_BASE   0x493
#define STRATA_FOSSIL_FLAG_COUNT  64
// Chosen at new game (Halvorsen's question): a lost animal is replaced at the same level by a
// related survivor (S4). The fossil is still recorded. Default (clear): the strict record.
#define FLAG_STRATA_GENTLE_DEEP_TIME (FLAG_STRATA_FOSSIL_BASE + STRATA_FOSSIL_FLAG_COUNT)

// ---- Ending: Halvorsen's last lines and the credits up the column (S3) ----------
// Not per act: owned by the Interpretive Center scripts and src/strata_ending.c.
// FLAG_UNUSED_0x4DE..0x4E5 in flags.h (inside the saved flag array, no extra save space).
#define FLAG_STRATA_ENDING_BASE 0x4DE
// Halvorsen has given the ending lines after the final peer review, and the credits have been
// offered. Set before the save prompt, so a save made there continues after the ending.
#define FLAG_STRATA_ENDING_SEEN  (FLAG_STRATA_ENDING_BASE + 0)
// (1..7 are free.)

// ---- Hub: the present-day camp, Jordan and the ranch (peer review, stipend) --
// Present-day content has no act of its own, so the hub has this section. Its trainers' defeat
// flags are the trainer flags (include/constants/opponents.h); the researchers' hide flags are
// FLAG_TEMP_1..FLAG_TEMP_8 (see src/strata_review.c: researcher k hides while act k isn't done).
#define FLAG_STRATA_HUB_BASE 0x2AC
#define VAR_STRATA_STIPEND_COUNT 0x40DB  // Codex "caught" entries Dr. Halvorsen has already paid for

// Dr. Halvorsen has explained the survey stipend (the first time the player asks about it).
#define FLAG_STRATA_HUB_STIPEND_TOLD  (FLAG_STRATA_HUB_BASE + 0)
// (1..7 are free.)


// ---- Story: the present-day subplot (S1, src/strata_story.c) ------
// VAR_STRATA_SUBPLOT (0x40DC, include/constants/vars.h) counts the camp interludes played. They
// play in this order, once each: beat N becomes due when its act is done (VAR_STRATA_STORY >=
// STORY_ACT_DONE(act)) and VAR_STRATA_SUBPLOT is N - 1, so a beat the player walks past waits
// for them, and the later ones queue behind it. None of them gates the rig. Each hub map runs
// special Strata_StoryPrepareMap in its on-transition script: VAR_TEMP_2 = the beat due on this
// map (or 0), VAR_TEMP_3 = 1 if there is one. Where each plays and who is in it is the beat
// table in src/strata_story.c (sStoryBeats); docs/strata_outline.md §1.5 has the script.
#define SUBPLOT_NONE              0
#define SUBPLOT_KESSLER_OFFER     1   // act 1: Kessler offers a "partnership"; Halvorsen says no (field station)
#define SUBPLOT_FERN_SPIKE        2   // act 2: Priya's spore counts, Bea's drought (ranch)
#define SUBPLOT_BLM_PERMIT        3   // act 2: Ranger Ortiz issues the collecting permit (BLM office, Jordan)
#define SUBPLOT_JOSIE_PIT         4   // act 3: Josie finds a fresh pit on BLM land (field station)
#define SUBPLOT_HALVORSEN_REFUSAL 5   // act 4: Kessler's funding deal; Halvorsen refuses, Theo nearly takes it (field station)
#define SUBPLOT_PIT_DOCUMENTED    6   // act 5: the player documents the pit with Ortiz (Sand Arroyo)
#define SUBPLOT_AUCTION_DATE      7   // act 6: Bea sets an auction date; Josie argues (ranch)
#define SUBPLOT_CITATION          8   // act 7: Ortiz cites Kessler's crew for the trespass (Jordan)
#define SUBPLOT_CONSORTIUM        9   // act 7: Halvorsen proposes the museum consortium (field station)
#define SUBPLOT_AUCTION_DAY       10  // act 8: Bea picks the consortium (ranch)
#define SUBPLOT_COUNT             11

// FLAG_UNUSED_0x4D4..0x4DD in flags.h: inside the saved flag array, no save space.
#define FLAG_STRATA_STORY_BASE 0x4D4
// The player has looked at the pit Josie found (Sand Arroyo), so the field log moves on.
#define FLAG_STRATA_STORY_SAW_PIT          (FLAG_STRATA_STORY_BASE + 0)
// Ortiz's evidence scene: she asked for three records, and each one logged.
#define FLAG_STRATA_STORY_EVIDENCE_STARTED (FLAG_STRATA_STORY_BASE + 1)
#define FLAG_STRATA_STORY_EVIDENCE_PIT     (FLAG_STRATA_STORY_BASE + 2)
#define FLAG_STRATA_STORY_EVIDENCE_JACKET  (FLAG_STRATA_STORY_BASE + 3)
#define FLAG_STRATA_STORY_EVIDENCE_TRACKS  (FLAG_STRATA_STORY_BASE + 4)
// (5..9 are free.)
// The interlude cast on the hub maps hides under FLAG_TEMP_9..FLAG_TEMP_C (set in each map's
// on-transition script unless its beat is due; FLAG_TEMP_1..8 are the researchers).


#endif // GUARD_CONSTANTS_STRATA_ACT_FLAGS_H
