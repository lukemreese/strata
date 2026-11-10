---
name: strata-maps
description: Adding or changing Strata maps, events and act content — the per-act map modules, patch helpers, story values, per-act flags, object graphics rules, forage, habitat/light tags, bosses, and checks. Use for any map, script or act-content work.
---

# Strata maps and act content

Read `docs/strata_outline.md` (plan per act, §2) and `docs/strata_design.md` (as built) first.

## Where things live

- `tools/strata/maps/actN_*.py` (and `act0_present.py`, `epilogue.py`): each defines `MAPS` and
  `MAP_SECTIONS`. Helpers are in `common.py`; the aggregator `__init__.py` documents the keys.
  Edit only your act's module when working in parallel.
- Maps are crops of stock Hoenn layouts (`crop=dict(from=LAYOUT_..., rect=...)`) with
  `patches=[dict(rect=..., like=(x, y) | metatile=0x... | tiles=... | same_as=...)]` and `swap={}`.
  The generator already swaps secret-base spots and dead signposts.
- Era variants reuse a layout with era tilesets from `gen_tilesets.py` (`VARIANTS`; set with
  `crop=dict(..., tilesets=(primary, secondary))`). **Every Act 1-5 map must use its era's
  ground-cover variants** (`hell_creek()` in common.py, `winter()`, `CORRAL_*`, `PETM_TILESETS`,
  `GREEN_RIVER_*`): the stock tall grass, long grass and lawn are anachronistic before the
  Oligocene. They redraw grass as ferns, palms, herbs, horsetails and the lawn as litter/soil
  (`gen_era_tiles.py`, docs/strata_art.md "Era ground cover"); behaviours are unchanged, so
  place encounter areas with the usual grass metatiles. A new secondary tileset in those acts
  needs a `<base>_<ground>` variant (palette-only is enough unless it has its own grass).
  Acts 6-8 keep grass (Oligocene/Miocene/ice-age palette variants).
- Scripts are hand-written: `data/maps/<Map>/scripts.inc`. `gen_maps.py` adds the
  `event_scripts.s` include for new maps.
- Tools: `maprender.py map LAYOUT_ID out.png`, `maprender.py catalog <primary> <secondary> out.png`,
  `mapascii.py <LayoutName>` (collision/elevation), `mapcheck.py` (must pass).

## Story and state

- `VAR_STRATA_STORY`: 0 new game, 1 starter chosen, act N = `STORY_IN_ACT(N)` (2N) in the act and
  `STORY_ACT_DONE(N)` (2N+1) once its boss is done, 18 epilogue (`include/constants/strata.h`).
  The rig (`src/strata_acts.c`) only loads the next layer after `STORY_ACT_DONE`, and "Today"
  (story 17 -> 18) only once `FLAG_STRATA_COLBY_SEEN` is set (`Strata_IsTodayGated`; until then
  it re-enters the Ice Age). A gate that needs words but no hub-script change can put them in
  front of the layer name in `STR_VAR_1` (the station's "STRATA RIG: {STR_VAR_1}." box).
- Fossils and Gentle Deep Time have their own section at the end of `strata_act_flags.h`
  (`FLAG_STRATA_FOSSIL_BASE` 0x493 + 64 slots, `FLAG_STRATA_GENTLE_DEEP_TIME`), then the Ending
  section (0x4DE..0x4E5, `FLAG_STRATA_ENDING_*`); 0x4D4..0x4DD are still free, inside the saved
  flag array: new flags there cost no save space. Scripts read fossils through specials
  (`Strata_BufferHallCase`, `Strata_PushFossilList`), not by flag name.
- The ending (S3): Halvorsen's script in `StrataInterpretive1F` -> `Common_EventScript_SaveGame`
  -> `fadescreen` -> `special Strata_RollCredits` (`src/credits.c`, `src/strata_ending.c`;
  design doc §7.9). The roll ends in a soft reset to the title.
- A map-script text a C test reads (`extern const u8 X_Text_Y[]`, e.g. width checks in
  `test/strata_ending.c`) needs a global label, `X_Text_Y::`; a single colon is file-local and
  the test ROM fails to link.
- Each act owns 8 save flags and one var in `include/constants/strata_act_flags.h`
  (`FLAG_STRATA_ACTn_BASE + 0..7`, `VAR_STRATA_ACTn`). Define names only in your act's section.
  The header is included by `data/map_events.s`, so the names work in map data too.
- `FLAG_TEMP_11..1F` are reserved for forage on maps that have forage. `FLAG_TEMP_1..8` hide the
  visiting researchers on the hub maps (researcher N, see Peer review below); don't reuse them there.
  `FLAG_TEMP_9..B` hide the subplot cast there, `FLAG_TEMP_1F` Kessler at the ranch; `VAR_TEMP_1`
  is the edge-trigger var (badlands, Jordan), `VAR_TEMP_2..4` the subplot's.
- Present-day (hub) content has no act of its own: its flags and vars are the "Hub" section at the end of
  `strata_act_flags.h` (`FLAG_STRATA_HUB_BASE` 0x2AC.., `VAR_STRATA_STIPEND_COUNT`). Add yours there.
- A full-screen scene from a script (the descent scenes, `Strata_StartDescentScenes`): the
  special does `LockPlayerFieldControls(); FadeScreen(FADE_TO_BLACK, 0);` and a task that waits
  for the fade, calls `CleanupOverworldWindowsAndTilemaps()` and sets CB2; it comes back with
  `CB2_ReturnToFieldContinueScriptPlayMapMusic`. Declare it `def_special X, waitstate=1`: the
  `special` macro then adds the `waitstate`, so the special must reach `ScriptContext_Enable` on
  every path. Ask first with a plain special (`Strata_GetDescentSceneCount`) and skip it when
  there is nothing to show, or the script hangs.
- Story values are set in boss scripts; keep `strata_boss_prep atk=1` / `strata_boss_done`
  around boss battles (smart AI + totem boost).
- The present-day subplot is `VAR_STRATA_SUBPLOT` (0x40DC, `SUBPLOT_*` 0–10 in the "Story" section
  of `strata_act_flags.h`, which also holds `FLAG_STRATA_STORY_BASE` 0x4D4..0x4DD; 5..9 free). Beat N
  is due when its act is done and the subplot is N − 1 (`sStoryBeats` in `src/strata_story.c`:
  act + map). Every hub map's on-transition runs `special Strata_StoryPrepareMap`: `VAR_TEMP_2` = the
  beat due on this map, `VAR_TEMP_3` = 1 if any (use it as the trigger/frame var), `VAR_TEMP_4` = the
  beat due anywhere. Interlude cast hides under `FLAG_TEMP_9..B` on hub maps (`cast_flag(n)` in
  `act0_present.py`); a map's on-transition sets them and clears the ones its due beat needs. A new
  hub map with people in the subplot needs the same on-transition lines. Don't gate the rig on a
  beat; the start-menu field log (`Story_QuestLine`) needs a line for any new state.

## Object graphics (crash risk)

- Only use `OBJ_EVENT_GFX_*` that exist in the Emerald build. Entries inside `#if IS_FRLG` in
  `src/data/object_events/object_event_graphics_info_pointers.h` are NULL here (WORKER_F/M,
  POLICEMAN, MEOWTH...). A NULL graphics info reads garbage every frame and reset the game after the
  starter screen once.
- Creatures: `OBJ_EVENT_GFX_SPECIES(<STRATA_SPECIES>)` naming the animal it represents, never a
  stock species (stock species are disabled in the game build, and the user wants no stock art).
  It shows the species' own overworld sheet once `gen_sprite.py` has drawn it (see the
  strata-species-art skill); until then the engine's substitute placeholder. No map change needed
  when the art lands.
- `gen_maps.py` refuses both mistakes; don't work around the check.

## Peer review trainers (humans battle only in the present day)

- Data: `src/data/trainers_strata.party` (generated into `trainers_strata.h`, included by `src/data.c`),
  IDs in `include/constants/opponents.h`. **Trainer IDs are scarce**: each owns a flag in a fixed range
  (`MAX_TRAINERS_COUNT` 864) and ids 864+ are battle partners. Strata's 15 reuse unreferenced stock
  slots (851..863, 485, 486). A new trainer needs another unreferenced stock slot (grep for it: the
  `TRAINER_` constants nothing but `opponents.h`/`trainers.party` mention), not a larger count.
- Scripts: `trainerbattle_single TRAINER_X, intro, defeat, EventScript_Won` after `lock`/`faceplayer`; the
  line after the macro runs only when the trainer is already beaten. Choose between trainers with
  `goto_if_defeated`. `trainerbattle_double` needs the not-enough-animals text. Money is
  4 x last level x the class multiplier in `gTrainerClasses` (`src/battle_main.c`).
- Unlocking by story: `special Strata_HideLockedReviewers` in the map's `ON_TRANSITION` hides researcher N
  (`FLAG_TEMP_N`) until act N is done; give the object `flag=reviewer_flag(N)` (`act0_present.py`).
- Check teams with `python3 tools/strata/balance.py` ("Peer review" table) and `make check TESTS='Peer-review'`.

## Cutscenes on arrival (lessons from S1)

- A frame-table script (`map_script_2 VAR_TEMP_3, 1, ...`) runs as soon as the player is on the
  map, at the edge they came in by, so the cast must stand where the camera sees them: move existing
  NPCs with `setobjectxyperm` + `setobjectmovementtype` in the on-transition script (works across
  connections: templates load before the transition script), place new ones there.
- A frame script on a map the harness quick-starts into blocks `quickstart` (it waits for map
  scripts). Existing scenarios quick-start in the Field Station (rig, Halvorsen) and the camp at story
  3 and 13, so station beats use a **trigger row** (y 10, between rig and door: every way in or out
  crosses it), not a frame script. Check `scenarios.py` for quick-start spots before choosing.
- Trigger tiles and object tiles are excluded from the harness's walk set (`world.MapInfo.walk_set`):
  keep both off the tiles next to doors and edges, or `act_tour` can't reach the warp. Hidden objects
  count too.
- Scripted walks of the player toward a scene can loop forever on a blocked tile (a wandering NPC):
  prefer moving the cast to the player over moving the player.

## Encounters, forage, habitat

- `encounters=dict(land_mons=mons(...), water_mons=..., fishing_mons=...)` with species that are
  alive in the map's era (`test/strata_region.c` checks `first_era`, `last_era`, extinctions,
  descents). Levels: era floor `sEraLevelFloor` in `src/data/lineages.h`; wild ranges per act in
  the design doc.
- `forage=[forage(x, y, "ITEM")]`: the generator rejects food that doesn't fit the era.
- `habitat="forest"|"open"|"water"|None` and `light="day"|"dusk"|"dark"|"ash"|"none"|"dns"` on every
  map (present-day maps use `"dns"`, the real clock).

## Checklist before committing

`gen_maps.py` clean, `mapcheck.py` clean, render new maps and look at them (`Read` the PNG) for
Hoenn leftovers, `make` and full `make check` green, design-doc maps table rows updated.
