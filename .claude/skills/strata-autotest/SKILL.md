---
name: strata-autotest
description: Scripted, headless playtests of Strata — build the playtest ROM, run ready-made scenarios (new game, act tour, battles, bosses) unthrottled, write new ones in a small DSL, and read the screenshots, logs and crash reports they leave. The preferred way to test anything in game; use before reaching for the mGBA GUI.
---

# Automated playtests (tools/strata/playtest)

A headless mGBA core runs the game at ~3000 fps (50x real time) driven by Python. Scenarios boot
straight into any state (map, x/y, story, era, party, items, flags) and leave numbered PNGs, a
log and a JSON result. A full new game takes ~5 s; every map of every act ~15 s; a boss ~3 s.

## Parts

| Piece | What it is |
|---|---|
| `runner/strata-runner` | mGBA 0.10.5's GBA core + `strata_runner.c`, a stdin/stdout protocol (step N frames with keys, read/write memory, PNG, save states, log of emulator errors and SoftResets). Built by `runner/build_runner.sh` (clones mGBA once into `~/.cache/mgba-0.10.5`; needs only gcc, zlib, libpng: no cmake/Qt/SDL/Lua) |
| `src/strata_playtest.c` | Playtest ROM only (`#if STRATA_PLAYTEST`). Polled once per main loop (one hook in `AgbMain`). Mirrors state into `gStrataPlaytestStatus` and runs commands from `gStrataPlaytestCommand`: QUICKSTART, SET_VAR/FLAG, GET_VAR/FLAG, COUNT_ITEM, WARP, RUN_SCRIPT, GIVE_MON/ITEM, HEAL, READ_PARTY |
| `harness.py` | `Game`: the DSL (below), symbols from the ELF (`nm`), constants via the ARM compiler (enums too; cached in `pokeemerald-playtest.playtest_constants.json`), watchdogs |
| `world.py` | Map knowledge: act of each map, walkable tiles (mapcheck rules), creature objects, edges/warps, boss lines (`VAR_STRATA_STORY` triggers) |
| `scenarios.py` | Ready-made scenarios; `run.py` the CLI |

Why not the mGBA GUI's Lua: 0.10.5's Qt build can only load a script from its menu (no
`--script`), so it can't run unattended; the stock `mgba-rom-test` has no input. Linking the core
directly gives frame-exact input and no throttling.

## Build (once per code change)

```bash
cd ~/projects/strata-harness            # or any worktree
bash tools/strata/playtest/runner/build_runner.sh     # first time only (~1 min)
make -j8 playtest                        # -> pokeemerald-playtest.gba/.elf, own dir build/emerald-playtest
```

`make playtest` (= `PLAYTEST=1`) adds `-DSTRATA_PLAYTEST=1 -g`. That also turns on, for this ROM
only, the debug start-menu entry and the no-collision / no-encounter flags (`FLAG_UNUSED_0x020/21`,
see `include/config/{debug,overworld,wild_encounter}.h`), so the sed-and-revert debug recipe is no
longer needed: the same ROM works in the mGBA GUI. Release and `make check` builds are untouched.

## Run

```bash
python3 tools/strata/playtest/run.py --list
python3 tools/strata/playtest/run.py new_game_smoke battle_smoke boss_all
python3 tools/strata/playtest/run.py act_tour --act 5          # or --map StrataLevee
python3 tools/strata/playtest/run.py all --quiet               # everything, ~1 min
python3 tools/strata/playtest/run.py tools/strata/playtest/examples/levee_walk.txt
```

Results: `C:\Projects\pokemon-custom\build\harness\<scenario>\` (`/mnt/c/...` from WSL;
`--out` to change). Each holds `NNN_<name>.png`, `log.txt` (every action, check, battle message,
emulator error with the function name) and `result.json` (status pass/fail/crash/error,
checks, screenshots with map and position, emulator errors, warnings, crash PC/LR).
`summary.json` lists the last run. Exit code is non-zero if anything failed. Read the PNGs.

| Scenario | Does |
|---|---|
| `new_game_smoke` | Real intro from the title: name, field station, starter choice, gear; asserts story 1, one Lv 5 starter, Exp. Share flag, waders, 5 capsules |
| `battle_smoke` | Levee tall grass with encounters on: wild battle, capsule throws (R = last used ball), Codex registration page; asserts the catch |
| `grass_battles` | One map per era with encounter grass (Acts 1-5: ferns, palms, herbs, horsetails; `--map` to pick): the overlay around the legs, the battle's entry wall (`_battle_intro`) and background, then run |
| `act_tour` | Every Strata map: arrival, each `OBJ_EVENT_GFX_SPECIES` creature up close, every edge (a tile walkable on both sides of the seam) and warp; asserts each lands on the right map |
| `peer_review_smoke` | Camp at story 3 (act 1 done): checks the researcher gating flags, talks to Arlo, plays the peer review (Lv 100 starters), checks the 432 prize and defeat flag, then gets the survey stipend from Halvorsen (5 entries x 175) |
| `boss_1` .. `boss_8`, `boss_all` | Quick-start beside the act's boss line, walk onto it, play the script and every battle (three Lv 100 starters), assert `STORY_ACT_DONE` |
| `watchdog_selftest` | Forces a freeze and a bad jump; both must be caught |
| `extinction_smoke` | Act 1 done with dinosaurs in the team and PC: rig to the impact winter, the loss list (a shot per message), fossil flags, then START > BAG > KEY ITEMS > Fossil Case > a fossil's label |
| `forecast_smoke` | Field station after act 6, mixed TEAM (pressures set) + PC: rig -> forecast window, every row, A, YES; asserts the TEAM after the load equals `gStrataRigForecast` |
| `pressure_chart_smoke` | TEAM menu -> LINEAGE: the pressure chart for each TEAM animal (Up/Down), B back to the TEAM menu on the last one viewed |
| `story_interludes` | All 10 present-day interludes (S1): quick-start beside each one with the story and `VAR_STRATA_SUBPLOT` it needs (`vars=[("VAR_STRATA_SUBPLOT", "SUBPLOT_X")]`), walk in, play it (a shot per box), check the subplot moved on; Ortiz's three evidence records; the start-menu field log (`sLogShown`) at several states |
| `colby_gate` | Story 17 at the rig: Colby unseen -> the gate message and a re-entry to the Ice Age (no filter); the sub-layer marker, the Colby intro, the Clovis point (flag), the bone pile (hedged text), the anchor; the rig then loads today (story 18, the mammoth's fossil) |
| `ending_smoke` | Interpretive Center, story 18, fossils + mixed TEAM/PC + subplot 10: Halvorsen's review (played with `q2_battle`), the ending lines, the stock save prompt (YES), the credits roll a shot every 200 frames, THE END (stops there) |
| `q3_codex` / `q3_notes` | Review screenshots for the science text: EVIDENCE and LINEAGE of the species the fact-check changed, and the corrected field notes (a shot per box). Edit `Q3_SPECIES` / `Q3_NOTES` in `scenarios.py` to look at others |
| `starter_run_mammal` / `_bird` / `_turtle` (`starter_runs` = all three; **not in `all`**, ~3 min each) | Q2 balance: one starter's line through all 29 bosses, set pieces and peer reviews in story order, each a quick-start with a TEAM at the EXP model's level; writes `fights.csv`/`fights.md`. Env: `STRATA_Q2_REPEAT=3`, `STRATA_Q2_ONLY=arlo,coryphodon`, `STRATA_Q2_KOS`, `STRATA_Q2_FINAL_LEVEL`, `STRATA_Q2_ANIM=1`. Then `python3 tools/strata/balance.py --playtest <out>` |
| `starter_run_smoke` | The Q2 machinery on two fights (in `all`) |

## Writing a scenario

Python (add to `scenarios.py` with `@scenario`), or a `.txt` file with one `Game` call per line.

```python
@scenario
def ferret(g, args):
    """Black-footed ferret encounter on the prairie."""
    g.quickstart("MAP_STRATA_PRAIRIE", 40, 10, story=18, era=9,
                 party=[("SPECIES_CIMOLESTES", 30)], items=[("ITEM_POKE_BALL", 5)],
                 flags=["FLAG_STRATA_BLM_PERMIT"], encounters=False)
    g.walk("right", 3)          # tiles; stops early when blocked, on a map change or a script
    g.face("up"); g.press("A")  # talk / interact
    r = g.talk()                # A through text until the script ends: 'done' | 'menu' | 'battle'
    if r == "battle":
        g.battle("catch")       # 'fight' | 'run' | 'catch'; returns gBattleOutcome
    g.screenshot("after")
    g.expect_var("VAR_STRATA_STORY", 18); g.expect_flag("FLAG_STRATA_EPI_FERRET_MET")
```

DSL: `quickstart MAP_X 10 20 story=2 era=1 party=SPECIES_A:12,SPECIES_B:10 flags=FLAG_X`,
`press A`, `hold UP 30`, `wait 60`, `walk up 3`, `wait_text`, `advance 2`, `talk`,
`screenshot name`, `expect_map MAP_X`, `expect_var VAR_X 2`, `expect_flag FLAG_X`,
`expect_pos 10 12`, `warp MAP_X 5 5`, `set_var`, `set_flag`, `give_mon`, `give_item`, `heal`,
`run_script <ScriptLabel>`, `party`, `tasks`, `add_pressure 0 PRESSURE_OPEN 64` (TEAM slot,
counter, amount). Giving more mons than the TEAM holds sends them to the PC. `g.const` evaluates
any C expression over the harness headers (e.g. `offsetof(struct RigForecast, expectedSpecies)`),
which with `g.read` reads game structs.

Python helpers for trainers and money: `g.trainer_defeated('TRAINER_X')` (the flag at `TRAINER_FLAGS_START` + id) and
`g.money()` (decrypts `SaveBlock1.money`). Trainer battles use `g.battle('fight')` as well; `g.talk()` returns
`'battle'` once the intro text ends.

Useful state: `g.st` (map, x, y, story, era, inBattle, scriptActive, fieldLocked, fadeActive,
callbacks), `g.cb2()` (main callback name), `g.tasks()` (active task function names: menus show
here), `g.printers()`, `g.text_waiting()`, `g.script_native()`, `g.controllers()` (battle input
state), `g.battle_text()`, `g.read_text(symbol)`, `g.read(symbol, size)`, `g.var/flag/item_count`.
Names are C names: anything in `include/constants/*` resolves, including enums.

Input timing: buttons are held `frames` (default 4) then released; walking is counted by position
changes, not timed. `quickstart` defaults: encounters off, collision on, instant text, battle
animations off; pass `encounters=True`, `collision=False`, `instant_text=False`, `battle_anim=True`.

## Watchdogs (every step)

- **Freeze**: the game's main loop counter (`gStrataPlaytestStatus.frames`) stops for 600 frames
  -> `crash`, with PC/LR named from the ELF and `crash_last.png`.
- **Crash**: mGBA's "Jumped to invalid address" -> `crash`. Other "Bad memory" lines are logged as
  `EMU` with the function (`pc=... (Func+0x..)`) and listed in `result.json` (not fatal).
- **Reset**: a SoftReset SWI -> `crash`.
- **Frozen screen**: keys held but the picture unchanged for 600 frames -> warning + screenshot.
- A scenario over 1.5 M frames fails (scenario bug guard). Every wait has a timeout.

## Limits and traps

- Quick-start state is "new game + vars": no rig extinctions or descents are applied, and earlier
  acts' flags aren't set unless you pass them. Use the real flow (new game, rig) to test those.
- Objects hidden by their own flag until a trigger (e.g. the Uintatherium) don't show on the tour.
- Audio isn't checked. Present-day light uses a fixed RTC (`Game(rtc=...)`).
- `walk` near triggers starts their scripts; `world.MapInfo.walk_set()` excludes trigger tiles.
- `print`ing from a scenario is fine; use `g.log` so it lands in `log.txt`.
- When a scenario's status is `error`, the traceback is in `log.txt`: a harness/scenario bug.
- Don't run a generator or `make` in the worktree while a scenario reads the ELF.
- Rebuild the playtest ROM after pulling changes: the runner reads `pokeemerald-playtest.gba`.
- `talk()` returns `menu` as soon as any menu-like task exists, and the harness samples between
  frames, so a special that builds a big window can be caught half-way (its list task up, its
  own task not yet). Wait for your own task: `g.wait_until(lambda: "Task_X" in g.tasks(), ...)`.
- The TEAM menu ignores A for a moment after its fade ends: press, poll ~40 frames for
  `Task_HandleSelectionMenuInput`, retry (see `pressure_chart_smoke`).
- Start-menu entries vary (debug entry, flags): read `sCurrentStartMenuActions` and find the
  action you want (`open_team_menu` in `scenarios.py`).
- Parallel agents share the default output folder (and its `summary.json`): pass
  `--out /mnt/c/Projects/pokemon-custom/build/harness_<lane>` so runs don't overwrite each other.
- PC mons: `give_mon` after a full 6-mon quick-start party sends them to the PC.
- `read_text` decodes the game's apostrophe as `’` (U+2019): match substrings without one
  ("load yet", "happening now isn"), not "can't".
- The stock save dialog (`Common_EventScript_SaveGame`) runs its YES/NO inside `SaveGameTask`,
  which `menu_open()` doesn't match: treat that task as a menu (`read_messages` in scenarios.py).
- `g.battle()` can't send in the next animal after a faint in a trainer battle (it sits in
  `WaitForMonSelection` until the timeout). `trainer_battle()` in scenarios.py retries with a
  short timeout and picks the next one (DOWN, A, A). `q2_battle()` handles faints properly. A
  "Lv 100 animal loses" result usually means the policy, not the game: move 1 every turn (the
  bison's Stomp), chip damage over five opponents, stat drops, Sturdy (Q2 diagnosis).
- The credits end in `SoftReset`, which the harness reports as a crash: stop at THE END
  (`gStrataCreditsState`: 1 rolling, 2 THE END) without pressing a key.
- A trainer pic with no front sprite (FRLG's "Old Man") asserts (`CrashScreen`, "does not have a
  front pic defined") the moment its battle starts; `test/strata_review.c` now checks every
  Strata trainer's pic.
- `quickstart` waits up to 600 frames for map scripts to finish, so it can't land on a map whose
  frame script starts a cutscene: quick-start on the neighbouring map and `walk` across the edge
  (`walk` stops when a script starts), then press through with `play_script`.
- The start menu has a field-log box top left (`src/strata_story.c`); screenshots of the menu show
  it, and `sLogShown` says whether it is up.
- `g.st["party"]` is only filled by READ_PARTY: call `g.party()`, never read the mirror directly.
- `g.battle('fight')` always uses move 1. For a balance verdict use `q2_battle(g)` (scenarios.py):
  best expected damage (gMovesInfo power/type/category, the type chart, stats and stages), TEAM
  menu driven by its tasks (`Task_HandleChooseMonInput` -> DOWN, A; `Task_HandleSelectionMenuInput`
  -> A; `Task_PrintAndWaitForText` -> A), and the level-up prompt "give up on having X learn Y?"
  answered with A (B loops back to the question for ever).
- Reading battle data: add `pokemon.h`, `move.h`, `battle_main.h` to `harness.Constants.HEADERS`
  for `offsetof`/`sizeof`. `gTypeEffectivenessTable` is `uq4_12_t` = **u32** (4096 = x1).
  `struct MoveInfo` word at +8: type bits 16-20, category 21-22 (PHYSICAL 1, SPECIAL 2, STATUS 3),
  power 23-31. `TYPE_NONE` is 0, so `TYPE_NORMAL` is 1. Bit-fields have no `offsetof`: take
  `DW_AT_data_bit_offset` from `arm-none-eabi-readelf --debug-dump=info` (`q2_ko_counter`).
- Equalising a TEAM: write IV-15/neutral stats into the plain part of `struct Pokemon` (hp..spDefense
  at `offsetof(struct Pokemon, hp)`); a battle copies them, only a level-up recalculates. Moves are
  encrypted: set them with a `setmonmove` script written to `gStringVar4` and started with
  RUN_SCRIPT (`q2_set_moves`). A quick-started animal knows only its own last four level-up moves;
  a carried lineage keeps its ancestors' (`q2_carried_moves`), which mattered a lot for the bird.
- Hub-map quick-starts: pass `("VAR_STRATA_SUBPLOT", "SUBPLOT_COUNT - 1")` so no interlude starts;
  Theo offers his earliest review not had, so set the earlier ones' flags as
  `"(TRAINER_FLAGS_START + TRAINER_STRATA_THEO_ACT3)"`; `VAR_STARTER_MON` picks his act 0 animal.
- Engine bug, fixed by config: the after-KO animation (B_ANIMATE_MON_AFTER_KO, launched twice per
  faint) gave an assert screen "disabled species: 48" and a soft-lock with `battlerKOAnimsRunning`
  stuck. It is now FALSE in `include/config/battle.h` (0 hits in 93 fights with
  `STRATA_Q2_ANIM=1`). The workarounds (`q2_assert_screen`, `q2_softlock`) and the `engine` column
  of fights.csv stay as a tripwire: any non-zero count is a new engine bug. A freeze at
  `CrashScreen` is an assert screen, not a hang.
- Several run.py processes can run at once with separate `--out` folders, but warm the
  constants cache (`pokeemerald-playtest.playtest_constants.json`) with one run first.
- Menus by memory, not by guessing the cursor: the start menu is `sCurrentStartMenuActions`/
  `sNumStartMenuActions`/`sStartMenuCursorPos` (BAG is action 2), the bag pocket is byte 5 of
  `gBagPosition`. Static EWRAM symbols resolve like globals. `FLAG_STRATA_*` and `POCKET_*`
  resolve too (`constants/strata_act_flags.h`, `constants/item.h` are in `Constants.HEADERS`).
