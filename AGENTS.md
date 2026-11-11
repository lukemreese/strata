# Strata: rules for every agent

Strata is a GBA game built on pokeemerald-expansion. The player is a field paleontologist who
carries animal lineages up the rock column of the North American West, 66 million years ago to
today. Every animal is real. The science has to be right, and uncertainty has to be stated.

This file is short on purpose. Read all of it before any change. Details live in the skills
(`.claude/skills/<name>/SKILL.md`) and the docs (`docs/strata_design.md`, `docs/strata_outline.md`,
`docs/strata_art.md`). Read the skill for your task before you start.

## Never

1. Never edit a generated file by hand. Edit its source and rerun the generator (table below).
2. Never insert, remove or reorder species in `tools/strata/roster/`. New species are appended
   to the last part file. Order is the species ID and the save format.
3. Never write "Pokémon", "Poké Ball" or a stock creature name in text the player can see.
   Strata's words are animal, specimen, lineage, reconstruction, Codex, capsule, TEAM.
4. Never use stock sprites or cries for a creature. All creature art and sound is generated
   by this repo's scripts.
5. Never state a fact about the fossil record that you have not checked against a source.
   If you can't check it, write it as a question for the lead and leave the game text alone.
6. Never run a generator while `make` or `make check` is running in the same worktree.
7. Never skip, disable or loosen a test to make it pass.
8. Never push, merge or delete a branch or worktree unless the person asked for it.

## The loop

```bash
# 1. edit a SOURCE (right column below), never the output
# 2. regenerate, in this order (run only the ones whose source you touched, or all):
python3 tools/strata/gen_sprite.py --all
python3 tools/strata/gen_cry.py
python3 tools/strata/gen_species.py
python3 tools/strata/gen_tilesets.py
python3 tools/strata/gen_maps.py
# 3. check without a build (2 min; --fast for 10 s without the drift check):
python3 tools/strata/check.py
# 4. build and test the ROM:
make -j8
make check -j8        # required: 0 FAILED. 18 KNOWN_FAILING and 9 EXPECT_FAILING are stock.
# 5. in-game behaviour: scripted playtest (strata-autotest skill)
make -j8 playtest && python3 tools/strata/playtest/run.py all --quiet
```

| To change | Edit this source | Generator |
|---|---|---|
| A species' stats, moves, Codex text, mass, age | `tools/strata/roster/*.py` | `gen_species.py` (mass also changes the sprite size and cry: run all) |
| A creature's sprite | `tools/strata/sprites/specs/<plan>.py`, `plans/<plan>.py` | `gen_sprite.py` then `gen_species.py` |
| A cry | `tools/strata/cries/specs.py` | `gen_cry.py` then `gen_species.py` |
| A map's layout, encounters, signs, objects | `tools/strata/maps/<act>.py` | `gen_maps.py` |
| What a sign or person says, a boss level | `data/maps/Strata*/scripts.inc` (hand-written) | none |
| Era colours and ground cover | `tools/strata/gen_tilesets.py`, `gen_era_tiles.py` | `gen_tilesets.py` |
| Game rules (lineages, pressures, rig) | `src/lineage.c`, `src/selection.c`, `src/strata_*.c`, `src/data/lineages.h` | none |

Generated, do not edit: `graphics/pokemon/strata/`, `sound/direct_sound_samples/cries/strata_*`,
`src/data/strata_*.h` and the Strata splices in species, pokedex and cry tables,
`data/layouts/Strata*`, `data/maps/Strata*/map.json`, `include/constants/strata_maps.h`,
`src/data/wild_encounters.json`.

## Done means

- `python3 tools/strata/check.py` prints `check: all passed`.
- `make check` prints 0 FAILED.
- `git status` shows only files you meant to change, plus their regenerated outputs.
- Your reply lists: what changed, what you did not finish, anything you could not verify, the
  test counts, the commit hash. Say "not verified" when it is not verified.

## Stop and ask when

- A test fails and the fix is not in a file you were told to edit.
- The task needs a fact you can't source, or a change to roster order, lineages or save data.
- A command in this file fails twice the same way.

Report what you ran and what it printed. Do not work around it.

## Local models (the desktop GPU)

A local model sorts and flags; it does not decide and it does not write shipped text.
`python3 tools/strata/local_model.py doctor`, then the strata-local-model skill.
