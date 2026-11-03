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
- Era variants reuse a layout with palette-only tilesets from `gen_tilesets.py` (General and
  Fallarbor have PETM/Oligocene/ice-age variants; other tilesets have none yet).
- Scripts are hand-written: `data/maps/<Map>/scripts.inc`. `gen_maps.py` adds the
  `event_scripts.s` include for new maps.
- Tools: `maprender.py map LAYOUT_ID out.png`, `maprender.py catalog <primary> <secondary> out.png`,
  `mapascii.py <LayoutName>` (collision/elevation), `mapcheck.py` (must pass).

## Story and state

- `VAR_STRATA_STORY`: 0 new game, 1 starter chosen, act N = `STORY_IN_ACT(N)` (2N) in the act and
  `STORY_ACT_DONE(N)` (2N+1) once its boss is done, 18 epilogue (`include/constants/strata.h`).
  The rig (`src/strata_acts.c`) only loads the next layer after `STORY_ACT_DONE`.
- Each act owns 8 save flags and one var in `include/constants/strata_act_flags.h`
  (`FLAG_STRATA_ACTn_BASE + 0..7`, `VAR_STRATA_ACTn`). Define names only in your act's section.
  The header is included by `data/map_events.s`, so the names work in map data too.
- `FLAG_TEMP_11..1F` are reserved for forage on maps that have forage. `FLAG_TEMP_1..8` hide the
  visiting researchers on the hub maps (researcher N, see Peer review below); don't reuse them there.
- Present-day (hub) content has no act of its own: its flags and vars are the "Hub" section at the end of
  `strata_act_flags.h` (`FLAG_STRATA_HUB_BASE` 0x2AC.., `VAR_STRATA_STIPEND_COUNT`). Add yours there.
- Story values are set in boss scripts; keep `strata_boss_prep atk=1` / `strata_boss_done`
  around boss battles (smart AI + totem boost).

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
