---
name: strata-build-test
description: Building, regenerating and testing Strata (pokeemerald-expansion) — generator order, the test suite and its pitfalls, and the debug-ROM recipe. Use whenever you change Strata code, data or generators.
---

# Build, generate, test

Run everything from `~/projects/strata` (see the strata-shell skill for how).

## Generators (single sources of truth; never hand-edit their output)

| Source | Generator | Writes |
|---|---|---|
| `tools/strata/sprites/` (body plans + species specs) | `gen_sprite.py` | `graphics/pokemon/strata/<name>/` art + `CUSTOM` (run before `gen_species.py`) |
| `tools/strata/cries/specs.py` (call program per species) | `gen_cry.py` | `sound/direct_sound_samples/cries/strata_<folder>.wav` + `strata_cries.txt` (run before `gen_species.py`) |
| `tools/strata/roster/` (species, per act; new species append to `part3.py`) | `gen_species.py` | species/pokedex/cries splices, `strata_families.h` (incl. `OVERWORLD` for own art), `strata_pokemon.h`, `strata_diets.h`, `strata_species_eras.h` |
| `tools/strata/gen_tilesets.py` (era palette variants) | itself | tileset palettes, `strata_headers.h`, `strata_era_art.h` |
| `tools/strata/maps/` (per-act modules) | `gen_maps.py` | layouts, `map.json`s, `map_groups.json`, encounters, `strata_maps.h`, `strata_map_eras.h`, heal locations, `event_scripts.s` includes |

Order: `gen_species.py`, `gen_tilesets.py`, `gen_maps.py`. Then `python3 tools/strata/mapcheck.py`
(every trigger, sign, forage spot and edge reachable on foot) and `balance.py` (per-act stat report).
After a merge, rerun all three; a clean tree afterwards means generated files are consistent.

## Build and test

- `make -j16` builds `pokeemerald.gba` (use `-j6`..`-j8` when other agents build too).
- `make check -j16` runs ~6000 tests. Required: **0 FAILED**. 18 KNOWN_FAILING, 9 EXPECT_FAILING
  and one "Tests resume after CRASH" are stock. Filter with `TESTS='<name prefix>'`.
- Strata tests: `test/lineage*.c`, `test/selection.c`, `test/strata_*.c`.

## Test pitfalls (each cost real time once)

- `PARAMETRIZE` inside a loop must be reached on every pass. Never `continue` before it; skip
  cases with an early `return` after the loop instead (a skipped PARAMETRIZE silently runs cases
  on map 0, Petalburg City).
- `CreateMon` in this expansion makes a bare mon (no moves, stats not calculated). Use
  `CreateRandomMon` or give moves and call `CalculateMonStats` yourself.
- `test/save.c` asserts the SaveBlock1 size. Adding dex entries or save fields changes it; confirm
  the cause, then update the constant.
- The test build enables every stock generation (`include/config/test.h`); the game build disables
  them. Anything that depends on stock species (e.g. their overworld sprites) can pass tests and
  still break the game.
- Inline test scripts can't see C enums; set vars from C.
- Never run a generator while `make`/`make check` is running in the same worktree: it rewrites
  headers mid-build (even with identical content the timestamps change) and can poison the run.

## Debug ROM for playtesting

Temporarily set three configs, build, keep the ROM and ELF, then restore with `git checkout`:

```bash
sed -i 's/#define DEBUG_OVERWORLD_IN_MENU *FALSE/#define DEBUG_OVERWORLD_IN_MENU TRUE/' include/config/debug.h
sed -i 's/#define OW_FLAG_NO_COLLISION        0/#define OW_FLAG_NO_COLLISION        FLAG_UNUSED_0x020/' include/config/overworld.h
sed -i 's/#define WE_FLAG_NO_ENCOUNTER        0/#define WE_FLAG_NO_ENCOUNTER        FLAG_UNUSED_0x021/' include/config/wild_encounter.h
make -j16 && cp pokeemerald.gba ~/strata-debug.gba && cp pokeemerald.elf ~/strata-debug.elf
git checkout include/config/debug.h include/config/overworld.h include/config/wild_encounter.h
make -j16   # rebuild the release ROM
```

Keep the ELF: crash addresses from the emulator map to functions with
`arm-none-eabi-addr2line -f -e ~/strata-debug.elf 0x08xxxxxx`. Never commit the debug configs.
