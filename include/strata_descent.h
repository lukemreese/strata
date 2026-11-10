#ifndef GUARD_STRATA_DESCENT_H
#define GUARD_STRATA_DESCENT_H

// The descent scene (F3, src/strata_descent.c): after the rig loads the next layer, each TEAM
// animal whose lineage changed gets the stock evolution scene with Strata's words. The species
// has already changed (Lineage_AdvanceToEra); the scene shows the old and the new and offers
// the new species' moves. PC animals change silently and are counted in one message.

struct DescentScene
{
    u8 slot;                                // TEAM slot after the load (losses compacted)
    u16 preSpecies;                         // the species before the load
    u8 preName[POKEMON_NAME_BUFFER_SIZE];   // what the animal was called before the load
};

// Hooks for Lineage_AdvanceToEra (src/lineage.c). Slots are TEAM slots of the era being
// applied; Descent_CompactTeam follows CompactPartySlots.
void Descent_BeginAdvance(void);
void Descent_NoteTeamDescent(u32 slot, u16 species);
void Descent_NoteTeamLost(u32 slot);
void Descent_NoteTeamReplaced(u32 slot);
void Descent_CompactTeam(void);
void Descent_NotePcDescent(void);
void Descent_EndAdvance(u32 fromEra, u32 toEra);

u32 Descent_GetSceneCount(void);
const struct DescentScene *Descent_GetScene(u32 i);
u32 Descent_GetPcCount(void);

// For src/evolution_scene.c: the scene playing now, or NULL for a stock evolution.
const struct DescentScene *Descent_GetActiveScene(void);
// STR_VAR_1 = the old name, STR_VAR_2 = the new species, STR_VAR_3 = the time it took.
void Descent_BufferSceneVars(const struct DescentScene *scene);
// The scene's two messages (placeholders STR_VAR_1..3) and the PC message (into gStringVar4).
extern const u8 gText_DescentIntro[];
extern const u8 gText_DescentDone[];
void Descent_BufferPcText(u32 count);

void Strata_GetDescentSceneCount(void);
void Strata_StartDescentScenes(void);
void Strata_BufferPcDescents(void);

#endif // GUARD_STRATA_DESCENT_H
