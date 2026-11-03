#ifndef GUARD_STRATA_REVIEW_H
#define GUARD_STRATA_REVIEW_H

#include "constants/flags.h"
#include "constants/opponents.h"
#include "constants/strata.h"

// Peer review (humans battle only in the present day) and the survey stipend. See
// src/strata_review.c and docs/strata_design.md ("Peer review").

// The visiting researcher of act N (1..8) is TRAINER_STRATA_REVIEW_ACT1 + N - 1, and is hidden
// by FLAG_TEMP_1 + N - 1 until the act is done.
#define STRATA_REVIEWER_COUNT       8
#define STRATA_REVIEWER_TRAINER(act)    (TRAINER_STRATA_REVIEW_ACT1 + (act) - 1)
#define STRATA_REVIEWER_HIDE_FLAG(act)  (FLAG_TEMP_1 + (act) - 1)

// Survey stipend: dollars per new Codex "caught" entry = STRATA_STIPEND_BASE plus
// STRATA_STIPEND_PER_ACT for every act finished (150 at the start, 350 once Ice Age is done).
#define STRATA_STIPEND_BASE      150
#define STRATA_STIPEND_PER_ACT    25

u32 Strata_ActsDone(u32 story);
u32 Strata_StipendRate(u32 story);
u32 Strata_StipendAmount(u32 newEntries, u32 story);

void Strata_HideLockedReviewers(void);
void Strata_PayStipend(void);
void Strata_StipendBaseline(void);

#endif // GUARD_STRATA_REVIEW_H
