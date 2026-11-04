#ifndef GUARD_STRATA_STORY_H
#define GUARD_STRATA_STORY_H

#include "constants/strata.h"

// The present-day subplot (S1): the camp interludes between the acts, in order, and the
// field log's "next objective" line in the start menu. See src/strata_story.c and the
// SUBPLOT_* values in include/constants/strata_act_flags.h.

// The field log window: top left, beside the start menu (which starts at tile 22 with its frame).
#define STORY_LOG_WIDTH_TILES  19
#define STORY_LOG_HEIGHT_TILES 4
#define STORY_LOG_WIDTH_PX     (STORY_LOG_WIDTH_TILES * 8)
#define STORY_LOG_LINES        2

// Evidence Ortiz asks for at the pit (SUBPLOT_PIT_DOCUMENTED).
#define STORY_EVIDENCE_COUNT   3

u32 Story_BeatAct(u32 beat);
u32 Story_BeatMap(u32 beat);
u32 Story_PendingBeat(u32 story, u32 subplot);
u32 Story_ExpectedSubplot(u32 story);
u32 Story_EvidenceLogged(void);
const u8 *Story_QuestLine(u32 story, u32 subplot);

void Strata_StoryPrepareMap(void);
void Strata_StoryBufferCaseCount(void);

void StrataLog_Show(void);
void StrataLog_Remove(void);

#endif // GUARD_STRATA_STORY_H
