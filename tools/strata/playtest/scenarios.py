"""Ready-made Strata scenarios. Each is a function (g, args) on a harness.Game.
Register new ones with @scenario; parametrised names (boss_3) go in expand()."""

import re

from harness import TestFailure
import world

REGISTRY = {}


def scenario(fn):
    REGISTRY[fn.__name__] = fn
    return fn


def get(name):
    m = re.fullmatch(r"boss_(\d)", name)
    if m:
        return lambda g, args: boss(g, args, int(m.group(1)))
    return REGISTRY[name]


def expand(name):
    if name == "boss_all":
        return [f"boss_{a}" for a in range(1, 9)]
    if name == "starter_runs":   # Q2 balance playthroughs (slow, not in `all`)
        return ["starter_run_mammal", "starter_run_bird", "starter_run_turtle"]
    if name == "all":
        return ["watchdog_selftest", "new_game_smoke", "battle_smoke", "forecast_smoke", "pressure_chart_smoke",
                "peer_review_smoke", "act_tour", "extinction_smoke", "story_interludes"] \
            + [f"boss_{a}" for a in range(1, 9)] + ["colby_gate", "ending_smoke"]
    if name in REGISTRY or name.endswith(".txt") or re.fullmatch(r"boss_[1-8]", name):
        return [name]
    raise SystemExit(f"unknown scenario {name} (try --list)")


# Flags a tour needs so story gates don't stop it (the BLM permit opens Sand Arroyo).
TOUR_FLAGS = ["FLAG_STRATA_BLM_PERMIT"]


def quickstart_act(g, mi, x, y, level=None, party=None, encounters=False, **kw):
    act = mi.act
    party = party or [(world.STARTERS[0], level or world.ACT_LEVEL[act])]
    g.quickstart(mi.id, x, y, story=world.story_for_act(act), era=min(act, 9), party=party,
                 items=[("ITEM_POKE_BALL", 10), ("ITEM_POTION", 5)], encounters=encounters, **kw)


def settle(g):
    """Finish whatever a step started: scripts, text, a battle (run from it)."""
    for _ in range(3):
        if g.st["inBattle"]:
            g.battle("run", shots=False)
        if g.st["scriptActive"] or g.st["fieldLocked"] or g.text_active():
            r = g.talk(stop_at_menu=False, timeout=4000)
            if r == "battle":
                continue
        break


# ---------------------------------------------------------------------------
@scenario
def new_game_smoke(g, args):
    """Full new game: title, intro, naming, the field station, starter choice, gear gift."""
    g.boot()
    g.screenshot("title")
    screens = set()
    start = g.frame
    boxes = 0
    idle = 0
    starter_done = False
    while True:
        if g.frame - start > 60 * 60 * 8:
            raise TestFailure("new game did not reach the free overworld with the starter in 8 game minutes")
        cb2 = g.cb2()
        if cb2 not in screens:
            screens.add(cb2)
            g.log(f"screen {cb2}")
            g.wait(20)
            g.screenshot(f"screen_{cb2}")
            continue
        if any("TitleScreen" in t for t in g.tasks()):
            g.press("START", 4, 30)
            continue
        if "Naming" in cb2:
            # Accept the default (or an empty, defaulted) name: START jumps to OK.
            g.press("START", 4, 10)
            g.press("A", 4, 30)
            continue
        if cb2 == "CB2_Overworld" and g.st["magic"] and not g.st["scriptActive"] and not g.st["fieldLocked"] \
                and not g.text_active() and g.st["story"] >= 1:
            break
        if g.text_waiting():
            idle = 0
            boxes += 1
            if boxes % 4 == 1:
                g.screenshot(f"text_{boxes:03d}")
            g.press("A", 2, 4)
            continue
        if "ChooseStarter" in cb2 or "StarterChoose" in cb2:
            if not starter_done:
                g.wait(60)
                g.screenshot("starter_choice")
                starter_done = True
            g.press("A", 4, 30)
            continue
        if g.menu_open() and not g.text_active():
            g.screenshot(f"menu_{len(g.shots)}")
            g.press("A", 4, 20)
            continue
        idle += 4
        if idle >= 40:  # main menu, gender choice, fades: A moves things on
            idle = 0
            g.press("A", 4, 4)
        g.step(4, 0)
    g.screenshot("after_intro")
    g.expect_map("MAP_STRATA_FIELD_STATION")
    g.expect_var("VAR_STRATA_STORY", 1)
    party = g.party()
    g.log(f"party {party}")
    g.check(len(party) == 1 and party[0]["level"] == 5, "one starter at Lv 5")
    g.expect_flag("FLAG_STRATA_EXP_SHARE")
    g.check(g.item_count("ITEM_WADERS") >= 1, "the waders were given")
    g.check(g.item_count("ITEM_POKE_BALL") >= 5, "5 capsules were given")
    g.log(f"intro took {(g.frame - start) / 60:.0f} game seconds")


# ---------------------------------------------------------------------------
@scenario
def battle_smoke(g, args):
    """Tall grass in the Levee Forest: a wild battle, capsule throws, Codex registration."""
    mi = world.MapInfo("StrataLevee")
    grass = mi.tall_grass()
    if not grass:
        raise TestFailure("no tall grass on the Levee")
    # A pair of neighbouring grass tiles to pace on.
    gs = set(grass)
    a = next(t for t in grass if (t[0] + 1, t[1]) in gs)
    quickstart_act(g, mi, a[0], a[1], level=5, encounters=True)
    g.screenshot("in_grass")
    steps = 0
    while not g.st["inBattle"] and g.cb2() == "CB2_Overworld":
        g.walk("right" if steps % 2 == 0 else "left", 1)
        steps += 1
        if steps > 400:
            raise TestFailure("no wild encounter in 400 steps of tall grass")
    g.log(f"encounter after {steps} steps")
    party_before = len(g.party())
    outcome = g.battle("catch", max_actions=10)
    g.check(outcome == 7, f"the wild animal was caught (outcome {outcome})")
    g.check(len(g.party()) == party_before + 1, "the catch joined the party")


# One map per era with encounter "grass" (Acts 1-5 draw it as undergrowth, gen_era_tiles.py).
GRASS_MAPS = ["StrataLevee", "StrataLeveeWinter", "StrataPalmForest", "StrataLegumeThicket",
              "StrataWillwoodSwamp", "StrataPolecatBench", "StrataLakeForest", "StrataWhiteRiver",
              "StrataGrassland"]


@scenario
def grass_battles(g, args):
    """Encounter grass of each era: the overlay around the player's legs, the wild battle's
    entry wall and background, then run. Before grasslands it is ferns, palms, herbs."""
    names = [n for n in GRASS_MAPS if not args.map or n in args.map]
    for name in names:
        mi = world.MapInfo(name)
        grass = set(t for t in mi.reachable if mi.behavior[t] in ("TALL_GRASS", "LONG_GRASS", "ASHGRASS")
                    and t not in mi.trigger_tiles and t not in mi.blocked_by_objects)
        pair = next((t for t in sorted(grass) if (t[0] + 1, t[1]) in grass), None)
        if pair is None:
            raise TestFailure(f"{name}: no pair of encounter tiles")
        g.log(f"=== {name}")
        quickstart_act(g, mi, pair[0], pair[1], level=50, encounters=True)
        g.walk("right", 1)
        g.wait(8)
        g.screenshot(f"{name}_in_grass")
        steps = 0
        while not g.st["inBattle"] and g.cb2() == "CB2_Overworld":
            g.walk("left" if steps % 2 == 0 else "right", 1)
            steps += 1
            if steps > 400:
                raise TestFailure(f"{name}: no wild encounter in 400 steps")
        g.wait(150)                     # the entry wall of plants slides past about now
        g.screenshot(f"{name}_battle_intro")
        outcome = g.battle("run", max_actions=10)
        g.check(outcome in (1, 4), f"{name}: wild battle after {steps} steps ended (outcome {outcome})")


# ---------------------------------------------------------------------------
@scenario
def peer_review_smoke(g, args):
    """Camp after Hell Creek: the ornithologist is unlocked, a peer review pays its prize, and
    Dr. Halvorsen pays the survey stipend for the Codex entries."""
    story = world.story_for_act(1) + 1   # STORY_ACT_DONE(1) = 3
    party = [(world.STARTERS[0], 100), (world.STARTERS[1], 100), (world.STARTERS[2], 100)]
    g.quickstart("MAP_STRATA_FIELD_CAMP", 22, 10, story=story, era=1, party=party,
                 items=[("ITEM_POKE_BALL", 5)], flags=["FLAG_STRATA_DIG_DONE"])
    settle(g)
    g.screenshot("start")
    # Story gating: act 1's researcher is out, act 3's is still hidden (FLAG_TEMP_N hides researcher N).
    g.check(not g.flag("FLAG_TEMP_1"), "the act 1 researcher (Arlo) is visible once act 1 is done")
    g.check(g.flag("FLAG_TEMP_3"), "the act 3 researcher (Tomas) is still hidden")
    g.check(not g.trainer_defeated("TRAINER_STRATA_REVIEW_ACT1"), "Arlo is not beaten yet")

    # Peer review: Arlo stands at (22, 8).
    money0 = g.money()
    g.walk("up", 1)
    g.check(g.pos() == (22, 9), f"stands below Arlo ({g.pos()})")
    g.press("A")
    g.wait(20)
    g.screenshot("intro")
    r = g.talk(stop_at_menu=False)
    g.check(r == "battle", f"Arlo's intro leads to a battle ({r})")
    outcome = g.battle("fight", max_actions=40)
    g.check(outcome == 1, f"the peer review was won (outcome {outcome})")
    g.talk(stop_at_menu=False)
    g.screenshot("end")
    g.check(g.trainer_defeated("TRAINER_STRATA_REVIEW_ACT1"), "Arlo's defeat flag is set")
    prize = g.money() - money0
    g.check(prize == 4 * 9 * 12, f"the prize is 4 x Lv 9 x 12 = 432 (got {prize})")
    # Talking again does not start another battle.
    g.press("A")
    r = g.talk(stop_at_menu=False)
    g.check(r == "done" and not g.st["inBattle"], f"a second talk is just talk ({r})")

    # The survey stipend: Halvorsen pays 175 (150 + 25 for the act done) per new Codex entry. The
    # three starters count as entries (nothing has been paid yet) and so do two new catches.
    g.give_mon("SPECIES_ANZU", 20)
    g.give_mon("SPECIES_MESODMA", 20)
    g.warp("MAP_STRATA_FIELD_STATION", 6, 6)
    g.face("up")
    money1 = g.money()
    g.press("A")
    shots = 0
    for _ in range(400):
        if g.text_waiting():
            if shots < 14:
                g.screenshot(f"stipend_{shots}")
                shots += 1
            g.press("A", 2, 4)
            continue
        if not g.st["scriptActive"] and not g.st["fieldLocked"] and not g.text_active() and g.cb2() == "CB2_Overworld":
            break
        g.step(2, 0)
    paid = g.money() - money1
    g.check(paid == 5 * 175, f"the stipend pays 5 entries x 175 = 875 (got {paid})")
    g.expect_flag("FLAG_STRATA_HUB_STIPEND_TOLD")
    g.expect_var("VAR_STRATA_STIPEND_COUNT", 5)
    # Nothing new: a second visit pays nothing.
    g.press("A")
    g.talk(stop_at_menu=False)
    g.check(g.money() - money1 == paid, "a second visit pays nothing")
    g.screenshot("after_stipend")


# ---------------------------------------------------------------------------
@scenario
def act_tour(g, args):
    """Every Strata map: arrival, each creature object up close, every edge and warp."""
    names = world.strata_maps()
    if args.map:
        names = [n for n in names if n in args.map]
    infos = [world.MapInfo(n) for n in names]
    if args.act:
        infos = [m for m in infos if m.act in args.act]
    infos.sort(key=lambda m: (m.act, m.name))
    problems = []
    for mi in infos:
        start = mi.start_tile()
        if start is None:
            problems.append(f"{mi.name}: no free start tile")
            continue
        g.log(f"=== {mi.name} (act {mi.act})")
        quickstart_act(g, mi, *start, flags=TOUR_FLAGS)
        settle(g)
        g.screenshot(f"{mi.name}_arrival")
        for o in mi.species_objects():
            t = mi.near((o["x"], o["y"]), 2, 5)
            if not t:
                g.log(f"{mi.name}: no free tile near {o['species']} at ({o['x']}, {o['y']})")
                continue
            g.warp(mi.id, *t)
            settle(g)
            g.screenshot(f"{mi.name}_{o['species']}")
        for c in mi.connections:
            try:
                tour_edge(g, mi, c)
            except TestFailure as e:
                problems.append(f"{mi.name} {c['direction']} edge: {e}")
                g.log(f"PROBLEM {problems[-1]}")
        for w in mi.warps:
            try:
                tour_warp(g, mi, w)
            except TestFailure as e:
                problems.append(f"{mi.name} warp ({w['x']}, {w['y']}): {e}")
                g.log(f"PROBLEM {problems[-1]}")
    g.check(not problems, f"tour transitions ({len(problems)} problems: {'; '.join(problems)})")


def tour_edge(g, mi, c):
    d = c["direction"]
    dx, dy = world.DIR_STEP[d]
    walk = mi.walk_set()
    pairs = world.edge_pairs(mi, c)
    if not pairs:
        raise TestFailure(f"no edge tile is walkable on both sides of the seam to {c['map']} "
                          f"(offset {c.get('offset', 0)})")
    tile = pairs[len(pairs) // 2][0]
    inner = (tile[0] - dx * 2, tile[1] - dy * 2)
    for back in range(2, 6):
        inner = (tile[0] - dx * back, tile[1] - dy * back)
        if inner in walk and all((tile[0] - dx * k, tile[1] - dy * k) in walk for k in range(back)):
            break
    else:
        inner = tile
    g.warp(mi.id, *inner)
    settle(g)
    want = g.const(c["map"])
    for _ in range(3):
        g.walk(d, 8)
        settle(g)
        if g.map_id() == want:
            break
    g.wait_overworld()
    g.wait(20)
    g.screenshot(f"{mi.name}_{d}_to_{c['map'].removeprefix('MAP_STRATA_').lower()}")
    if g.map_id() != want:
        raise TestFailure(f"walking {d} from {inner} ended on {g._map_name()} at {g.pos()}, not {c['map']}")


def tour_warp(g, mi, w):
    target = (w["x"], w["y"])
    walk = mi.walk_set() | {target}
    best = None
    for d, (dx, dy) in world.DIR_STEP.items():
        n = (target[0] - dx, target[1] - dy)
        if n in walk and n != target and mi.free(n):
            # Doors are entered walking up; mats are left walking down.
            pref = {"up": 0, "down": 1}.get(d, 2)
            if best is None or pref < best[0]:
                best = (pref, n, d)
    if not best:
        raise TestFailure("no tile next to the warp")
    _, n, d = best
    g.warp(mi.id, *n)
    settle(g)
    want = g.const(w["dest_map"])
    g.walk(d, 1)
    if g.map_id() != want:
        g.walk(d, 1)  # arrow warps (mats) fire on the next step
    g.wait_until(lambda: g.map_id() == want or g.in_overworld(), 600, "the warp")
    g.wait_overworld()
    settle(g)
    g.screenshot(f"{mi.name}_warp_{w['dest_map'].removeprefix('MAP_STRATA_').lower()}")
    if g.map_id() != want:
        raise TestFailure(f"stepping {d} onto ({w['x']}, {w['y']}) did not warp to {w['dest_map']}")


# ---------------------------------------------------------------------------
@scenario
def watchdog_selftest(g, args):
    """Harness self-test: a forced freeze and a forced bad jump must both be caught."""
    from harness import GameCrash
    mi = world.MapInfo("StrataLevee")
    quickstart_act(g, mi, *mi.start_tile())
    state = g.out + "/selftest.ss"
    g.save_state(state)
    # 1. Freeze: point the main callback at a Thumb `b .` written into spare EWRAM.
    loop = g.cmd_addr + 4
    g.runner.cmd(f"w16 {loop:x} e7fe")
    g.runner.cmd(f"w32 {g.sym['gMain'] + 4:x} {loop | 1:x}")
    try:
        g.wait(1200)
        raise TestFailure("the freeze was not detected")
    except GameCrash as e:
        g.check("freeze" in str(e) and "pc=" in g.crash_info["where"], f"freeze caught: {g.crash_info['where']}")
    # 2. Crash: jump into unmapped memory.
    g.load_state(state)
    g.runner.cmd(f"w32 {g.sym['gMain'] + 4:x} 0e000001")
    try:
        g.wait(600)
        raise TestFailure("the bad jump was not detected")
    except GameCrash as e:
        g.check("invalid address" in str(e) or "freeze" in str(e), f"bad jump caught: {e}")
    g.crash_info = None


# ---------------------------------------------------------------------------
BOSS_LEVEL = 100  # no level-ups (and so no move-learning prompts) during the fight


def boss(g, args, act):
    """Quick-start next to act N's boss line, walk onto it, fight the boss, check the act ends."""
    candidates = []
    for mi in world.maps_by_act().get(act, []):
        for (script, value), tiles in mi.story_triggers().items():
            if value == world.story_for_act(act):
                candidates.append((mi, script, tiles))
    if not candidates:
        raise TestFailure(f"act {act}: no VAR_STRATA_STORY trigger found")
    mi, script, tiles = candidates[0]
    g.log(f"act {act} boss: {script} on {mi.name}, {len(tiles)} trigger tiles")
    best = None
    for t in sorted(tiles):
        for d, (dx, dy) in world.DIR_STEP.items():
            n = (t[0] - dx, t[1] - dy)
            if mi.free(n):
                score = abs(n[0] - (mi.arrival or n)[0]) + abs(n[1] - (mi.arrival or n)[1])
                if best is None or score < best[0]:
                    best = (score, n, d, t)
    if not best:
        raise TestFailure("no free tile next to the boss line")
    _, n, d, t = best
    party = [(world.STARTERS[0], BOSS_LEVEL), (world.STARTERS[1], BOSS_LEVEL), (world.STARTERS[2], BOSS_LEVEL)]
    quickstart_act(g, mi, *n, party=party)
    settle(g)
    g.screenshot("before_boss_line")
    g.walk(d, 1)
    g.wait(10)
    g.check(g.st["scriptActive"] or g.st["fieldLocked"] or g.st["inBattle"], f"stepping onto {t} starts {script}")
    shots = 0
    battles = 0
    t0 = g.frame
    # Text, menus and every battle the script starts (act 2's gauntlet has three), until it ends.
    while True:
        if g.frame - t0 > 60 * 60 * 5:
            raise TestFailure(f"boss script still running after 5 game minutes (native={g.script_native()}, "
                              f"tasks={g.tasks()}, printers={g.printers()})")
        if g.st["inBattle"]:
            outcome = g.battle("fight", max_actions=60, shots=True)
            battles += 1
            g.check(outcome in (1, 7), f"boss battle {battles} was won (outcome {outcome})")
            continue
        if g.text_waiting():
            if shots < 8:
                g.screenshot(f"boss_script_{shots}")
                shots += 1
            g.press("A", 2, 4)
            continue
        if not g.st["scriptActive"] and not g.st["fieldLocked"] and g.cb2() == "CB2_Overworld" \
                and not g.st["fadeActive"] and not g.text_active():
            break
        if g.menu_open() and not g.text_active():
            g.screenshot("boss_menu")
            g.press("A", 4, 20)
            continue
        g.step(2, 0)
    g.check(battles >= 1, f"the boss script started a battle ({battles})")
    g.screenshot("after_boss")
    g.expect_var("VAR_STRATA_STORY", 2 * act + 1)


# ---------------------------------------------------------------------------
# Rig forecast (F1) and pressure chart (F2): src/strata_forecast.c

# A White River TEAM (act 6 done) of mixed fates for the Ashfall load, with counters set so
# every kind of line shows: default descent with a branch close, a branch taken, a heat
# branch out of reach, an extinction, stasis, and the rhino's open-country branch.
FORECAST_TEAM = [("SPECIES_HESPEROCYON", 35), ("SPECIES_MESOHIPPUS", 33), ("SPECIES_PROTOCHELYD", 34),
                 ("SPECIES_ISCHYROMYS", 32), ("SPECIES_GALLINULOID", 34), ("SPECIES_SUBHYRACODON", 30)]
FORECAST_PRESSURES = [(0, "PRESSURE_MEAT_DIET", 41), (1, "PRESSURE_FOREST", 70), (2, "PRESSURE_HEAT", 100),
                      (4, "PRESSURE_OPEN", 50), (5, "PRESSURE_OPEN", 64)]
FORECAST_PC = [("SPECIES_HYAENODON", 33), ("SPECIES_PALAEOLAGUS", 31), ("SPECIES_POEBROTHERE", 32),
               ("SPECIES_LEPISOSTEUS", 30)]
RIG_STAND = (10, 8)  # below the rig console (signs at (10, 7) and (11, 7), facing north)


def forecast_quickstart(g, act=6):
    g.quickstart("MAP_STRATA_FIELD_STATION", *RIG_STAND, story=2 * act + 1, era=act, party=FORECAST_TEAM)
    for slot, pressure, amount in FORECAST_PRESSURES:
        g.add_pressure(slot, pressure, amount)
    for species, level in FORECAST_PC:
        g.give_mon(species, level)  # the TEAM is full: these go to the PC


def read_forecast(g):
    """The TEAM gStrataRigForecast expects after the load: [(species, level)]."""
    c = g.const
    base = g.sym["gStrataRigForecast"]
    n = g.read(base, 1, c("offsetof(struct RigForecast, expectedCount)"))
    sp = c("offsetof(struct RigForecast, expectedSpecies)")
    lv = c("offsetof(struct RigForecast, expectedLevel)")
    return [(g.read(base, 2, sp + 2 * i), g.read(base, 1, lv + i)) for i in range(n)]


@scenario
def forecast_smoke(g, args):
    """Field station rig after act 6: the forecast window (every row), then YES; the TEAM
    after the load must be what the forecast said."""
    forecast_quickstart(g)
    g.screenshot("at_rig")
    g.face("up")
    g.press("A")
    r = g.talk()
    # Building the window takes the game a few frames.
    g.wait_until(lambda: "Task_RigForecast" in g.tasks(), 120, "the forecast window")
    g.check(r == "menu" and "Task_RigForecast" in g.tasks(), f"the forecast window opened (talk={r}, tasks={g.tasks()})")
    g.wait(10)
    expected = read_forecast(g)
    g.log(f"forecast expects TEAM {expected}")
    g.screenshot("forecast_first")
    rows = len(FORECAST_TEAM) + 1
    for i in range(1, rows):
        g.press("DOWN", 4, 8)
        g.screenshot(f"forecast_row_{i + 1}")
    g.press("DOWN", 4, 8)  # stays on the PC row
    for i in range(rows):
        g.press("UP", 4, 4)
    g.screenshot("forecast_back_to_top")
    g.press("A", 4, 10)
    g.check("Task_RigForecast" not in g.tasks(), "A closed the forecast")
    r = g.talk()
    g.check(r == "menu" and any("YesNo" in t for t in g.tasks()), f"the load YES/NO follows (tasks={g.tasks()})")
    g.screenshot("load_yes_no")
    g.press("A", 4, 10)  # YES
    r = g.talk(stop_at_menu=False, timeout=12000)
    g.wait_overworld()
    g.screenshot("after_load")
    g.expect_var("VAR_STRATA_ERA", 7)
    party = [(m["species"], m["level"]) for m in g.party()]
    g.log(f"TEAM after the load {party}")
    g.check(party == expected, f"the TEAM after the load is the forecast ({party} vs {expected})")
    want = {"SPECIES_LEPTOCYON", "SPECIES_HYPOHIPPUS", "SPECIES_CHELYDRA", "SPECIES_GALLINULOID", "SPECIES_APHELOPS"}
    g.check(sorted(s for s, _ in party) == sorted(g.const(s) for s in want),
            "Leptocyon, Hypohippus, Chelydra, Gallinuloid and Aphelops; Ischyromys lost")


def open_team_menu(g):
    """START -> TEAM; returns once the party menu takes input."""
    g.wait_overworld()
    g.press("START", 4, 20)
    n = g.read("sNumStartMenuActions", 1)
    actions = [g.read("sCurrentStartMenuActions", 1, i) for i in range(n)]
    team = actions.index(1)  # MENU_ACTION_POKEMON (src/start_menu.c)
    g.screenshot("start_menu")
    for _ in range(team):
        g.press("DOWN", 4, 4)
    g.press("A", 4, 10)
    g.wait_until(lambda: "Task_HandleChooseMonInput" in g.tasks(), 600, "the TEAM menu")


@scenario
def pressure_chart_smoke(g, args):
    """TEAM menu -> LINEAGE on a steered animal: the pressure chart, paging through the TEAM, and back."""
    forecast_quickstart(g)
    open_team_menu(g)
    g.wait_until(lambda: not g.st["fadeActive"], 300, "the TEAM menu fade")
    g.screenshot("team_menu")
    # The TEAM menu takes a moment after its fade before it reads A: retry.
    def options_open():
        return "Task_HandleSelectionMenuInput" in g.tasks()
    for _ in range(5):
        g.press("A", 4, 4)
        for _ in range(20):
            if options_open():
                break
            g.wait(2)
        if options_open():
            break
    g.wait_until(lambda: "Task_HandleSelectionMenuInput" in g.tasks(), 300, "the animal's options")
    g.screenshot("team_options")
    g.press("DOWN", 4, 4)  # SUMMARY, LINEAGE, ...
    g.press("A", 4, 4)
    g.wait_until(lambda: g.cb2() == "CB2_PressureChart" and not g.st["fadeActive"], 600, "the pressure chart")
    g.screenshot("chart_hesperocyon")
    for name in ["mesohippus", "protochelyd", "ischyromys", "gallinuloid", "subhyracodon"]:
        g.press("DOWN", 4, 8)
        g.screenshot(f"chart_{name}")
    g.press("DOWN", 4, 8)
    g.screenshot("chart_wraps_to_first")
    g.press("UP", 4, 8)
    g.check(g.read("sChart", 4) != 0, "the chart is still up")
    g.press("B", 4, 10)
    g.wait_until(lambda: "Task_HandleSelectionMenuInput" in g.tasks() and not g.st["fadeActive"], 900,
                 "the TEAM menu again")
    g.screenshot("back_in_team_menu")
    g.check(g.read("gLastViewedMonIndex", 1) == 5, "the TEAM menu returns on the last animal viewed")
    g.check(g.read("sChart", 4) == 0, "the chart freed its memory")
    g.press("B", 4, 20)
    g.screenshot("team_menu_cursor")


def fossil_slot(species):
    """Fossil slot of a species: its row in src/data/strata_fossils.h (append-only)."""
    import os
    text = open(os.path.join(world.ROOT, "src/data/strata_fossils.h")).read()
    rows = re.findall(r"\{ (SPECIES_\w+),", text)
    return rows.index(species)


def play_script(g, prefix, max_shots=40):
    """Press through a script's text and menus (A: default answers), a screenshot per box,
    until the field is free again (after any warp)."""
    shots, t0 = 0, g.frame
    while True:
        if g.frame - t0 > 60 * 60 * 3:
            raise TestFailure(f"{prefix}: script still running after 3 game minutes (tasks={g.tasks()})")
        if g.text_waiting():
            if shots < max_shots:
                g.screenshot(f"{prefix}_{shots:02d}")
                shots += 1
            g.press("A", 2, 4)
            continue
        if g.menu_open() and not g.text_active():
            g.screenshot(f"{prefix}_menu_{shots:02d}")
            shots += 1
            g.press("A", 4, 20)
            continue
        if not g.st["scriptActive"] and not g.st["fieldLocked"] and g.cb2() == "CB2_Overworld" \
                and not g.st["fadeActive"] and not g.text_active():
            return shots
        g.step(2, 0)


@scenario
def extinction_smoke(g, args):
    """Act 1 done with doomed dinosaurs in the team and PC: load the impact winter at the rig,
    read the loss list, then open the Fossil Case from the bag."""
    party = [("SPECIES_CIMOLESTES", 14), ("SPECIES_TYRANNOSAUR", 14), ("SPECIES_TRICERATOPS", 13),
             ("SPECIES_ANZU", 12), ("SPECIES_AVISAURUS", 12), ("SPECIES_EMARGINACHEL", 12)]
    # Story 3 = STORY_ACT_DONE(1): the rig offers the next layer (RIG_NEXT).
    g.quickstart("MAP_STRATA_FIELD_STATION", 10, 8, story=3, era="ERA_HELL_CREEK", party=party,
                 items=[("ITEM_POKE_BALL", 5)])
    # The team is full, so these two go to the PC.
    g.give_mon("SPECIES_EDMONTOSAUR", 12)
    g.give_mon("SPECIES_EDMONTOSAUR", 11)
    g.face("up")
    g.screenshot("at_rig")
    g.press("A")
    play_script(g, "rig")
    g.expect_map("MAP_STRATA_LEVEE_WINTER")
    g.expect_var("VAR_STRATA_STORY", 4)
    party_after = g.party()
    g.log(f"party after {party_after}")
    g.check(len(party_after) == 2, f"two survivors left in the team ({len(party_after)})")
    base = g.const("FLAG_STRATA_FOSSIL_BASE")
    for sp in ("SPECIES_TYRANNOSAUR", "SPECIES_TRICERATOPS", "SPECIES_ANZU", "SPECIES_AVISAURUS",
               "SPECIES_EDMONTOSAUR"):
        g.check(g.flag(base + fossil_slot(sp)), f"fossil flag for {sp}")
    g.check(not g.flag(base + fossil_slot("SPECIES_ANKYLOSAURUS")), "no fossil for a lineage never carried")
    g.check(g.item_count("ITEM_FOSSIL_CASE") == 1, "the Fossil Case was given")

    # START -> BAG -> KEY ITEMS -> Fossil Case -> USE.
    g.press("START", 4, 30)
    actions = [g.read("sCurrentStartMenuActions", 1, i) for i in range(g.read("sNumStartMenuActions", 1))]
    bag = 2  # MENU_ACTION_BAG: a private enum in src/start_menu.c (POKEDEX, POKEMON, BAG, ...)
    g.check(bag in actions, f"the start menu has the bag ({actions})")
    for _ in range(actions.index(bag) - g.read("sStartMenuCursorPos", 1)):
        g.press("DOWN", 4, 8)
    g.screenshot("start_menu")
    g.press("A", 4, 10)
    g.wait_until(lambda: "Bag" in g.cb2() or "BagMenu" in g.cb2(), 600, "the bag", keys=0)
    g.wait(60)
    key_pocket = g.const("POCKET_KEY_ITEMS")
    for _ in range(8):
        if g.read("gBagPosition", 1, 5) == key_pocket:
            break
        g.press("RIGHT", 4, 30)
    g.wait(30)
    g.screenshot("bag_key_items")
    g.check(g.read("gBagPosition", 1, 5) == key_pocket, "the bag is on the KEY ITEMS pocket")
    g.press("A", 4, 20)
    g.screenshot("bag_item_menu")
    g.press("A", 4, 20)  # USE
    g.wait_until(lambda: g.cb2() == "CB2_Overworld" and g.st["scriptActive"], 1200, "the Fossil Case script")
    g.wait_until(lambda: g.menu_open(), 600, "the fossil list")
    g.wait(30)
    g.screenshot("fossil_case_list")
    g.press("DOWN", 4, 20)
    g.screenshot("fossil_case_list_2")
    g.press("A", 4, 10)
    g.wait_until(g.text_waiting, 600, "a fossil label")
    g.screenshot("fossil_label")
    g.press("A", 2, 4)
    g.wait_until(g.text_waiting, 600, "the fossil label's reason")
    g.screenshot("fossil_label_reason")
    # The label runs over a few boxes; A through them back to the list.
    t0 = g.frame
    while not (g.menu_open() and not g.text_active()):
        if g.frame - t0 > 1200:
            raise TestFailure("the fossil list did not come back after the label")
        if g.text_waiting():
            g.press("A", 2, 4)
        else:
            g.step(2, 0)
    g.wait(10)
    g.press("B", 4, 20)
    g.wait_until(lambda: not g.st["scriptActive"] and not g.st["fieldLocked"], 600, "the case to close")
    g.screenshot("after_case")


# ---------------------------------------------------------------------------
# S3: the Colby gate, the ending and the credits up the column.

def read_messages(g, prefix, until, max_shots=30, timeout=60 * 60 * 3):
    """Press A through text boxes and menus (default answers), with a screenshot of each, until
    until() holds. Returns every message the field box showed (gStringVar4, decoded)."""
    shots, seen, t0 = 0, [], g.frame
    while not until():
        if g.frame - t0 > timeout:
            raise TestFailure(f"{prefix}: still waiting after {timeout} frames (cb2={g.cb2()}, tasks={g.tasks()})")
        if g.text_waiting():
            msg = g.read_text("gStringVar4")
            if not seen or seen[-1] != msg:
                seen.append(msg)
            if shots < max_shots:
                g.screenshot(f"{prefix}_{shots:02d}")
                shots += 1
            g.press("A", 2, 4)
            continue
        # The stock save dialog runs its own YES/NO inside SaveGameTask.
        if (g.menu_open() or "SaveGameTask" in g.tasks()) and not g.text_active():
            msg = g.read_text("gStringVar4")
            if not seen or seen[-1] != msg:
                seen.append(msg)
            if shots < max_shots:
                g.screenshot(f"{prefix}_menu_{shots:02d}")
                shots += 1
            g.press("A", 4, 20)
            continue
        g.step(2, 0)
    return seen


def trainer_battle(g, rounds=8):
    """g.battle('fight'), but when the lead faints and the game waits for the next animal
    (WaitForMonSelection: the TEAM menu of a forced switch), pick the next one and go on."""
    for n in range(rounds):
        try:
            return g.battle("fight", max_actions=80, timeout=9000, shots=(n == 0))
        except TestFailure:
            if "WaitForMonSelection" not in g.controllers():
                raise
        g.log(f"forced switch: cb2={g.cb2()} tasks={g.tasks()}")
        g.screenshot(f"switch_{n}")
        g.wait(30)
        g.press("DOWN", 4, 10)
        g.press("A", 4, 30)
        g.press("A", 4, 60)
    raise TestFailure("the battle needed more switches than the TEAM has")


def field_free(g):
    return not g.st["scriptActive"] and not g.st["fieldLocked"] and g.cb2() == "CB2_Overworld" \
        and not g.st["fadeActive"] and not g.text_active()


@scenario
def colby_gate(g, args):
    """Story 17 (Ice Age done) at the rig: with the Colby coda unseen the rig holds today back and
    only re-enters the Ice Age; then the real coda (sub-layer marker, Clovis point, anchor) and the
    rig loads today, with the end-Pleistocene filter."""
    party = [("SPECIES_CANIS", 50), ("SPECIES_CHELYDRA", 50), ("SPECIES_MAMMUTHUS", 49)]
    g.quickstart("MAP_STRATA_FIELD_STATION", 10, 8, story=17, era="ERA_TRAP_CAVE", party=party,
                 items=[("ITEM_POKE_BALL", 5)])
    g.check(not g.flag("FLAG_STRATA_COLBY_SEEN"), "the Colby coda is not seen yet")

    # Unseen: the rig says why, and offers the Ice Age layer again (YES re-enters it).
    g.face("up")
    g.screenshot("rig_unseen")
    g.press("A")
    msgs = read_messages(g, "rig_unseen", lambda: g.map_id() == g.const("MAP_STRATA_STEPPE") and field_free(g))
    g.log(f"rig said: {msgs}")
    g.check(any("load yet. Each layer is chained" in m for m in msgs), "the rig explains the gate")
    g.check(any("Colby sub-layer" in m for m in msgs), "the rig names the Colby sub-layer")
    g.check(any("Trap Cave, 20,000 yrs ago" in m and "Enter the reconstruction?" in m for m in msgs),
            "the rig offers to re-enter the Ice Age layer")
    g.expect_map("MAP_STRATA_STEPPE")
    g.expect_var("VAR_STRATA_STORY", 17)
    g.expect_var("VAR_STRATA_ERA", g.const("ERA_TRAP_CAVE"))
    g.check(len(g.party()) == 3, "no filter ran: the mammoth is still in the TEAM")

    # The sub-layer marker beside the anchor (55, 8): stand below it and read it.
    g.walk("left", 1)
    g.face("up")
    g.press("A")
    read_messages(g, "marker", lambda: g.map_id() == g.const("MAP_STRATA_COLBY") and field_free(g))
    g.expect_map("MAP_STRATA_COLBY")
    g.screenshot("colby_arrival")
    # East along row 8: the intro trigger at x 10, then up to the bone pile.
    g.walk("right", 6)
    read_messages(g, "colby_intro", lambda: field_free(g))
    g.walk("right", 13 - g.pos()[0])
    g.check(g.pos() == (13, 8), f"beside the point ({g.pos()})")
    g.face("right")
    g.screenshot("colby_point")
    g.press("A")
    msgs = read_messages(g, "colby_point", lambda: field_free(g))
    g.check(any("Someone made this." in m for m in msgs), "the point: someone made this")
    g.expect_flag("FLAG_STRATA_COLBY_SEEN")
    # The bone pile's note hedges the meat-cache reading.
    g.face("up")
    g.press("A")
    msgs = read_messages(g, "colby_bones", lambda: field_free(g))
    g.check(any("debated" in m for m in msgs), "the bone pile says the cache reading is debated")

    # Back by the anchor sign (5, 7), then the rig.
    g.walk("left", g.pos()[0] - 5)
    g.check(g.pos() == (5, 8), f"below the anchor ({g.pos()})")
    g.face("up")
    g.press("A")
    read_messages(g, "anchor", lambda: g.map_id() == g.const("MAP_STRATA_FIELD_STATION") and field_free(g))
    g.expect_map("MAP_STRATA_FIELD_STATION")
    g.face("up")
    g.screenshot("rig_seen")
    g.press("A")
    msgs = read_messages(g, "rig_seen", lambda: g.var("VAR_STRATA_STORY") == 18 and field_free(g), max_shots=40)
    g.log(f"rig said: {msgs}")
    g.check(not any("load yet. Each layer is chained" in m for m in msgs), "no gate once Colby is seen")
    g.expect_var("VAR_STRATA_STORY", 18)
    g.expect_var("VAR_STRATA_ERA", g.const("ERA_EPILOGUE"))
    g.check(g.flag(f"FLAG_STRATA_FOSSIL_BASE + {fossil_slot('SPECIES_MAMMUTHUS')}"), "the mammoth is a fossil now")
    g.screenshot("today")


@scenario
def ending_smoke(g, args):
    """Epilogue: the Interpretive Center with a few fossils and a mixed TEAM and PC. Beat
    Halvorsen's final peer review, read her ending lines, save, then the credits climb the column
    band by band to THE END (left there: a key would soft-reset to the title)."""
    # q2_battle (the Q2 policy): the best-damage move each turn and the next animal after a faint.
    # g.battle('fight') always used move 1, the bison's Stomp, and lost to the Uintatherium (Q2).
    party = [("SPECIES_BISON", 100), ("SPECIES_CHELYDRA", 100), ("SPECIES_MELEAGRIS", 100),
             ("SPECIES_EQUUS", 100), ("SPECIES_CENTROCERCUS", 100), ("SPECIES_CANIS", 100)]
    lost =["SPECIES_TYRANNOSAUR", "SPECIES_TRICERATOPS", "SPECIES_TAENIOLABIS", "SPECIES_HYOPSODUS",
            "SPECIES_HYAENODON", "SPECIES_EPICYON", "SPECIES_MAMMUTHUS", "SPECIES_ARCTODUS"]
    flags = [f"FLAG_STRATA_FOSSIL_BASE + {fossil_slot(sp)}" for sp in lost] + ["FLAG_STRATA_COLBY_SEEN"]
    # VAR_STRATA_SUBPLOT (0x40DC, story lane S1) at its final value: Bea chose the consortium.
    g.quickstart("MAP_STRATA_INTERPRETIVE_1F", 15, 8, story=18, era="ERA_EPILOGUE", party=party,
                 items=[("ITEM_POKE_BALL", 5)], flags=flags, vars=[("0x40DC", 10)])
    g.give_mon("SPECIES_ANTILOCAPRA", 50)  # the TEAM is full: these go to the PC
    g.give_mon("SPECIES_MUSTELA", 50)
    g.give_mon("SPECIES_CANIS", 48)
    g.screenshot("center")

    # Halvorsen (14, 8) faces right, at the Pair.
    g.face("left")
    g.press("A")
    r = g.talk(stop_at_menu=True)
    g.check(r == "menu", f"Halvorsen asks first ({r})")
    g.screenshot("review_question")
    # YES (the cursor's default). The menu ignores A for a few frames after it opens: retry.
    for _ in range(10):
        g.wait(10)
        g.press("A", 4, 10)
        if "Task_HandleYesNoInput" not in g.tasks():
            break
    r = g.talk(stop_at_menu=False)
    g.check(r == "battle", f"the final peer review starts ({r})")
    res = q2_battle(g)
    g.check(res["outcome"] == 1, f"the final peer review was won (outcome {res['outcome']})")
    lead = g.party()[0]
    g.log(f"Halvorsen review: {res['turns']} turns, the Lv 100 bison ends at {lead['hp']}/{lead['maxHP']} HP")
    g.check(g.trainer_defeated("TRAINER_STRATA_HALVORSEN"), "Halvorsen's defeat flag is set")

    # Her ending lines, the save prompt, then the credits.
    msgs = read_messages(g, "ending", lambda: g.cb2() == "CB2_Credits", max_shots=40)
    g.log(f"ending said: {msgs}")
    text = " ".join(msgs)
    g.check("written in the rock before you got" in text and "happening now isn" in text, "the theme line")
    for animal in ("Bison", "black-footed ferret", "Swift foxes"):
        g.check(animal in text, f"the ending names the {animal}")
    g.check(any("would you like to save" in m.lower() for m in msgs), "the stock save prompt was shown")
    g.check(g.flag("FLAG_STRATA_EPI_PEER_REVIEW_DONE"), "the peer review flag is set")
    g.check(g.flag("FLAG_STRATA_ENDING_SEEN"), "the ending flag is set")
    g.check(g.read("gSpecialVar_Result", 2) == 1, "the save succeeded (SAVE_SUCCESS)")

    # The roll: a screenshot every few seconds until THE END.
    state = lambda: g.read("gStrataCreditsState", 2)
    g.check(state() == 1, "the credits roll started")
    g.wait(90)
    shots, t0 = 0, g.frame
    while state() != 2:
        if g.frame - t0 > 60 * 60 * 3:
            raise TestFailure("the credits did not reach THE END in 3 minutes")
        g.screenshot(f"credits_{shots:02d}")
        shots += 1
        g.wait(200)
    g.log(f"credits: {shots} screenshots, {g.frame - t0} frames")
    g.check(shots >= 8, f"the roll lasted long enough for several bands ({shots} shots)")
    g.wait(150)
    g.screenshot("the_end")
    g.check(g.cb2() == "CB2_Credits", "still on the credits (no reset)")


# The present-day subplot (S1): src/strata_story.c, the hub map scripts

STORY_TEAM = [("SPECIES_CIMOLESTES", 30)]
STATION_RIG = (10, 8)     # arrival from the rig; the interlude row is y 10
CAMP_WEST = (2, 9)        # on the ranch road, a few steps from the ranch
RANCH_WEST = (2, 8)       # on the road, a few steps from Jordan


def story_start(g, map_name, pos, story, subplot, flags=()):
    g.quickstart(map_name, *pos, story=story, era=min(story // 2, 9), party=STORY_TEAM,
                 vars=[("VAR_STRATA_SUBPLOT", subplot)], flags=["FLAG_STRATA_DIG_DONE"] + list(flags))
    settle(g)


def field_log(g, name):
    """START: the field log's objective beside the menu, then close it again."""
    g.wait_overworld()
    g.press("START", 4, 30)
    g.wait(10)
    g.screenshot(f"fieldlog_{name}")
    g.check(g.read("sLogShown", 1) == 1, f"{name}: the field log window is up with the start menu")
    g.press("B", 4, 20)
    g.wait_until(lambda: not g.st["fieldLocked"], 300, "the start menu to close")
    g.check(g.read("sLogShown", 1) == 0, f"{name}: closing the menu removes the field log")


def interlude(g, name, subplot):
    """Play the interlude that just started (a screenshot per box) and check the subplot moved on."""
    g.wait_until(lambda: g.st["scriptActive"] or g.st["fieldLocked"], 300, f"the {name} interlude to start")
    shots = play_script(g, name)
    g.check(shots >= 2, f"{name}: the interlude showed its text ({shots} boxes)")
    g.expect_var("VAR_STRATA_SUBPLOT", subplot)
    g.screenshot(f"{name}_after")


def station_interlude(g, name, story, subplot, after):
    story_start(g, "MAP_STRATA_FIELD_STATION", STATION_RIG, story, subplot, ["FLAG_STRATA_BLM_PERMIT"])
    g.check(g.var("VAR_TEMP_3") == 1, f"{name}: a station beat is due ({g.var('VAR_TEMP_2')})")
    field_log(g, f"{name}_due")
    g.walk("down", 2)
    interlude(g, name, after)
    g.check(g.var("VAR_TEMP_3") == 0, f"{name}: no second beat waits in the station")


def walk_into(g, direction, want_map, tiles=6):
    g.walk(direction, tiles)
    g.check(g.map_id() == g.const(want_map), f"walked into {want_map} ({g._map_name()})")


@scenario
def story_interludes(g, args):
    """Every present-day interlude after acts 1-8 (S1): quick-start where the player arrives with
    the right story and subplot, play each scene through (a shot per box) and check
    VAR_STRATA_SUBPLOT moved on; the field log in the start menu at a few of the states."""
    # Act 1 done (story 3): Kessler's offer, in the field station.
    station_interlude(g, "kessler_offer", 3, "SUBPLOT_NONE", "SUBPLOT_KESSLER_OFFER")
    field_log(g, "after_kessler")

    # Act 2 done (story 5): the fern spike at the ranch, then the permit in Jordan.
    story_start(g, "MAP_STRATA_FIELD_CAMP", CAMP_WEST, 5, "SUBPLOT_KESSLER_OFFER")
    walk_into(g, "left", "MAP_STRATA_LINDQVIST_RANCH")
    interlude(g, "fern_spike", "SUBPLOT_FERN_SPIKE")
    field_log(g, "after_fern_spike")
    g.warp("MAP_STRATA_BLM_OFFICE", 5, 5)
    g.face("up")
    g.press("A")
    interlude(g, "permit", "SUBPLOT_BLM_PERMIT")
    g.expect_flag("FLAG_STRATA_BLM_PERMIT")

    # Act 3 done (story 7): Josie's pit, then a look at it in Sand Arroyo.
    station_interlude(g, "josie_pit", 7, "SUBPLOT_BLM_PERMIT", "SUBPLOT_JOSIE_PIT")
    field_log(g, "see_the_pit")
    g.warp("MAP_STRATA_SAND_ARROYO", 29, 14)
    g.face("up")
    g.press("A")
    play_script(g, "arroyo_pit")
    g.expect_flag("FLAG_STRATA_STORY_SAW_PIT")

    # Act 4 done (story 9): Kessler's funding deal; Halvorsen refuses, Theo keeps the card.
    station_interlude(g, "refusal", 9, "SUBPLOT_JOSIE_PIT", "SUBPLOT_HALVORSEN_REFUSAL")

    # Act 5 done (story 11): documenting the pit with Ranger Ortiz.
    story_start(g, "MAP_STRATA_SAND_ARROYO", (26, 14), 11, "SUBPLOT_HALVORSEN_REFUSAL", ["FLAG_STRATA_BLM_PERMIT"])
    g.check(not g.flag("FLAG_TEMP_9"), "Ortiz is at the pit")
    g.screenshot("ortiz_at_pit")
    g.face("left")
    g.press("A")
    play_script(g, "ortiz_brief")
    g.expect_flag("FLAG_STRATA_STORY_EVIDENCE_STARTED")
    field_log(g, "evidence_0")
    for name, pos, facing, flag in [("pit", (29, 14), "up", "PIT"), ("jacket", (27, 14), "down", "JACKET"),
                                    ("tracks", (31, 14), "down", "TRACKS")]:
        g.warp("MAP_STRATA_SAND_ARROYO", *pos)
        g.face(facing)
        g.press("A")
        play_script(g, f"log_{name}")
        g.expect_flag(f"FLAG_STRATA_STORY_EVIDENCE_{flag}")
    field_log(g, "evidence_3")
    g.warp("MAP_STRATA_SAND_ARROYO", 26, 14)
    g.face("left")
    g.press("A")
    interlude(g, "ortiz_report", "SUBPLOT_PIT_DOCUMENTED")

    # Act 6 done (story 13): Bea has set an auction date; Josie argues.
    story_start(g, "MAP_STRATA_FIELD_CAMP", CAMP_WEST, 13, "SUBPLOT_PIT_DOCUMENTED")
    g.check(g.flag("FLAG_TEMP_9"), "Josie is not at camp while the ranch scene waits")
    walk_into(g, "left", "MAP_STRATA_LINDQVIST_RANCH")
    interlude(g, "auction_date", "SUBPLOT_AUCTION_DATE")

    # Act 7 done (story 15): Ortiz cites Kessler's crew in Jordan; Halvorsen's consortium.
    story_start(g, "MAP_STRATA_LINDQVIST_RANCH", RANCH_WEST, 15, "SUBPLOT_AUCTION_DATE")
    walk_into(g, "left", "MAP_STRATA_JORDAN")
    interlude(g, "citation", "SUBPLOT_CITATION")
    station_interlude(g, "consortium", 15, "SUBPLOT_CITATION", "SUBPLOT_CONSORTIUM")
    # The same beat from a talk with Halvorsen (she plays it instead of her usual lines).
    story_start(g, "MAP_STRATA_FIELD_STATION", (6, 6), 15, "SUBPLOT_CITATION")
    g.face("up")
    g.press("A")
    interlude(g, "consortium_talk", "SUBPLOT_CONSORTIUM")

    # Act 8 done (story 17): auction day at the ranch. Bea picks the consortium.
    story_start(g, "MAP_STRATA_FIELD_CAMP", CAMP_WEST, 17, "SUBPLOT_CONSORTIUM")
    walk_into(g, "left", "MAP_STRATA_LINDQVIST_RANCH")
    interlude(g, "auction_day", "SUBPLOT_AUCTION_DAY")
    field_log(g, "after_auction")

    # Halvorsen afterwards: science, then what she makes of the auction.
    g.warp("MAP_STRATA_FIELD_STATION", 6, 6)
    g.face("up")
    g.press("A")
    play_script(g, "halvorsen_after")
    g.expect_var("VAR_STRATA_SUBPLOT", "SUBPLOT_AUCTION_DAY")


# ---------------------------------------------------------------------------
# Q2 balance pass (docs/strata_outline.md §6 M5): headless starter playthroughs.
#
# starter_run_mammal / _bird / _turtle walk one starter's lineage through every boss, set
# piece and peer review in story order. Each fight is its own quick-start: the TEAM is the
# starter's default-path descendant for that act (lead) plus the same typical catches for every
# starter, all at the level a normal player has there (balance.exp_model: 20 wild knockouts per
# act with the Exp. Share, carried from act to act, raised to the era floor on arrival), with
# stats set to IV 15 and a neutral nature so the three runs differ only by the starter.
# The policy is simple: always FIGHT with the move that does the most expected damage (power,
# STAB, type chart, attack/defence and stages, accuracy), never switch or use items, send in
# the next animal when one faints. Each run writes fights.csv and fights.md to its output folder;
# tools/strata/balance.py --playtest <out> merges them into the balance report.
# About 2 minutes each, so they are not in `all`:
#   python3 tools/strata/playtest/run.py starter_runs --out /mnt/c/Projects/pokemon-custom/build/harness_balance
# Environment: STRATA_Q2_REPEAT=<n> plays every fight n times (wild IVs, crits and damage rolls
# vary; default 1); STRATA_Q2_KOS=<n> wild knockouts per act in the EXP model (default 20);
# STRATA_Q2_ONLY=arlo,gauntlet runs only those fights.

import csv  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import struct  # noqa: E402

import harness  # noqa: E402

Q2_REPEAT = int(os.environ.get("STRATA_Q2_REPEAT", "1"))
Q2_KOS = int(os.environ.get("STRATA_Q2_KOS", "0")) or None
Q2_ONLY = [f for f in os.environ.get("STRATA_Q2_ONLY", "").split(",") if f]
Q2_ANIM = os.environ.get("STRATA_Q2_ANIM", "0") == "1"   # battle animations on (slower)
Q2_FINAL_LEVEL = 52     # Halvorsen's final review: an epilogue TEAM at about Lv 50-55 (§3.1)
Q2_LINES = {"mammal": 0, "bird": 1, "turtle": 2}   # VAR_STARTER_MON
# Typical catches, the same for every starter (wild in that act or carried from the last one,
# never a starter line, mid-table BST). The TEAM size per act is balance.TEAM_SIZE (3 animals
# in acts 1-2, 4 in 3-5, 5 in 6-8, 6 in the epilogue).
Q2_CATCHES = {
    0: [],
    1: ["CHAMPSOSAUR", "DIDELPHODON"],
    2: ["CHAMPSOSAUR", "MESODMA"],
    3: ["CHAMPSOSAUR", "LOXOLOPHUS", "CARSIOPTYCH"],
    4: ["SIFRHIPPUS", "DIACODEXIS", "BOREALOSUCH"],
    5: ["EOHIPPUS", "HYRACHYUS", "PRESBYORNIS"],
    6: ["MESOHIPPUS", "POEBROTHERE", "MERYCOIDODON", "STYLEMYS"],
    7: ["PROTOHIPPUS", "PROCAMELUS", "COSORYX", "HYPOHIPPUS"],
    8: ["EQUUS", "OVIS", "ANTILOCAPRA", "CAMELOPS"],
    9: ["BISON", "EQUUS", "OVIS", "ANTILOCAPRA", "CENTROCERCUS"],
}
THEO0 = ["TRAINER_STRATA_THEO_ACT0_BIRD", "TRAINER_STRATA_THEO_ACT0_TURTLE", "TRAINER_STRATA_THEO_ACT0_MAMMAL"]
# Story order: (act, id, kind, map folder, how, script). kind: setpiece | boss | survival (the
# tyrannosaur: running is the point) | encounter (the ferret: a catch, not a fight to win) |
# review | final. how: "trigger" (step onto a coord trigger of that script) or "talk" (A on the
# object running it). Reviews happen at STORY_ACT_DONE(act).
Q2_FIGHTS = [
    (0, "theo_0", "review", "StrataFieldCamp", "talk", "StrataFieldCamp_EventScript_Theo"),
    (1, "acheroraptors", "setpiece", "StrataFernGlade", "trigger", "StrataFernGlade_EventScript_RaptorAmbush"),
    (1, "tyrannosaur", "survival", "StrataRiver", "trigger", "StrataRiver_EventScript_Tyrannosaur"),
    (1, "arlo", "review", "StrataFieldCamp", "talk", "StrataFieldCamp_EventScript_Arlo"),
    (2, "gauntlet", "boss", "StrataBackswampWinter", "trigger", "StrataBackswampWinter_EventScript_Gauntlet"),
    (2, "priya", "review", "StrataLindqvistRanch", "talk", "StrataLindqvistRanch_EventScript_Priya"),
    (3, "taeniolabis", "setpiece", "StrataConcretionBluffs", "talk", "StrataConcretionBluffs_EventScript_Taeniolabis"),
    (3, "eoconodon", "boss", "StrataLegumeThicket", "trigger", "StrataLegumeThicket_EventScript_Eoconodon"),
    (3, "tomas", "review", "StrataFieldCamp", "talk", "StrataFieldCamp_EventScript_Tomas"),
    (3, "theo_3", "review", "StrataFieldCamp", "talk", "StrataFieldCamp_EventScript_Theo"),
    (4, "oxyaena", "setpiece", "StrataClarksFork", "talk", "StrataClarksFork_EventScript_Oxyaena"),
    (4, "coryphodon", "boss", "StrataRedBeds", "trigger", "StrataRedBeds_EventScript_Coryphodon"),
    (4, "ingrid", "review", "StrataFieldStation", "talk", "StrataFieldStation_EventScript_Ingrid"),
    (5, "patriofelis", "setpiece", "StrataOilShale", "talk", "StrataOilShale_EventScript_Patriofelis"),
    (5, "uintatherium", "boss", "StrataLakeForest", "trigger", "StrataLakeForest_EventScript_Uintatherium"),
    (5, "keola", "review", "StrataLindqvistRanch", "talk", "StrataLindqvistRanch_EventScript_Keola"),
    (6, "hyaenodon", "setpiece", "StrataToadstool", "trigger", "StrataToadstool_EventScript_Hyaenodon"),
    (6, "archaeotherium", "boss", "StrataWhiteRiver", "trigger", "StrataWhiteRiver_EventScript_Archaeotherium"),
    (6, "oskar", "review", "StrataJordan", "talk", "StrataJordan_EventScript_Oskar"),
    (6, "theo_6", "review", "StrataFieldCamp", "talk", "StrataFieldCamp_EventScript_Theo"),
    (7, "epicyon", "setpiece", "StrataSavanna", "talk", "StrataSavanna_EventScript_Epicyon"),
    (7, "teleoceras", "boss", "StrataWaterhole", "trigger", "StrataWaterhole_EventScript_Teleoceras"),
    (7, "hollis", "review", "StrataJordan", "talk", "StrataJordan_EventScript_Hollis"),
    (8, "panthera", "setpiece", "StrataSteppe", "trigger", "StrataSteppe_EventScript_Lions"),
    (8, "arctodus", "boss", "StrataTrapCave", "trigger", "StrataTrapCave_EventScript_Arctodus"),
    (8, "asha", "review", "StrataLindqvistRanch", "talk", "StrataLindqvistRanch_EventScript_Asha"),
    (8, "theo_8", "review", "StrataFieldCamp", "talk", "StrataFieldCamp_EventScript_Theo"),
    (9, "mustela", "encounter", "StrataPrairie", "talk", "StrataPrairie_EventScript_Ferret"),
    (9, "halvorsen", "final", "StrataInterpretive1F", "talk", "StrataInterpretive1F_EventScript_Halvorsen"),
]
# Theo offers the earliest review not had yet: the earlier ones must be marked as done.
Q2_THEO_DONE = {"theo_3": THEO0, "theo_6": THEO0 + ["TRAINER_STRATA_THEO_ACT3"],
                "theo_8": THEO0 + ["TRAINER_STRATA_THEO_ACT3", "TRAINER_STRATA_THEO_ACT6"]}
Q2_OUTCOMES = {1: "won", 2: "lost", 3: "drew", 4: "ran", 7: "caught", 9: "forfeited"}


def q2_data():
    """The starter lines' default paths and the EXP model's levels, from balance.py (lineages.h,
    the roster, the map modules and the boss scripts), so a change to a floor, a wild table or a
    boss moves the TEAM levels too."""
    import balance
    descents, extinct, _floors = balance.read_lineages()
    lines = balance.starter_lines(descents, extinct)
    model = balance.exp_model(Q2_KOS or balance.WILD_KOS_PER_ACT)
    return balance, lines, model


def q2_level(act, kind, model):
    """The TEAM level for a fight (balance.exp_model); Halvorsen's final review at Q2_FINAL_LEVEL."""
    if kind == "final":
        return Q2_FINAL_LEVEL
    kind = {"survival": "boss", "encounter": "setpiece"}.get(kind, kind)
    return model[act][kind]


def q2_team(line, act, level, lines, starters, size):
    """[(SPECIES_X, level)]: the line's animal for this act first, then the act's catches."""
    start = starters[line]
    lead = lines[start][act] if act else start
    return [(f"SPECIES_{sp}", level) for sp in ([lead] + Q2_CATCHES[act])[:size]]


def q2_ivs(line, act, lines, starters, size):
    """IVs per TEAM slot: the starter line has been carried since act 1, so it has the lineage
    resilience of every load since (balance.resilience_iv, from include/lineage.h); the catches
    are fresh (15, a wild catch's average)."""
    import balance
    return [balance.resilience_iv(lines[starters[line]], act)] + [balance.IV] * (size - 1)


def q2_layout(g):
    """Battle struct offsets, move data and the type chart (read once per run)."""
    if getattr(g, "_q2", None):
        return g._q2
    for h in ("pokemon.h", "move.h", "battle_main.h"):
        if h not in harness.Constants.HEADERS:
            harness.Constants.HEADERS.append(h)
    c = g.const
    lay = dict(bm=c("sizeof(struct BattlePokemon)"), mi=c("sizeof(struct MoveInfo)"),
               mon=c("sizeof(struct Pokemon)"), mon_hp=c("offsetof(struct Pokemon, hp)"),
               mon_level=c("offsetof(struct Pokemon, level)"),
               moves=c("offsetof(struct BattlePokemon, moves)"), stages=c("offsetof(struct BattlePokemon, statStages)"),
               types=c("offsetof(struct BattlePokemon, types)"), pp=c("offsetof(struct BattlePokemon, pp)"),
               hp=c("offsetof(struct BattlePokemon, hp)"), level=c("offsetof(struct BattlePokemon, level)"),
               maxhp=c("offsetof(struct BattlePokemon, maxHP)"), ability=c("offsetof(struct BattlePokemon, ability)"),
               ntypes=c("NUMBER_OF_MON_TYPES"), eff_size=c("sizeof(uq4_12_t)"),
               no_types=(c("TYPE_NONE"), c("TYPE_MYSTERY")),
               phys=c("DAMAGE_CATEGORY_PHYSICAL"), special=c("DAMAGE_CATEGORY_SPECIAL"),
               stat=dict(atk=c("STAT_ATK"), defn=c("STAT_DEF"), spa=c("STAT_SPATK"), spd=c("STAT_SPDEF")),
               party=g.sym["gParties"] + c("B_TRAINER_PLAYER") * c("PARTY_SIZE") * c("sizeof(struct Pokemon)"))
    n, es = lay["ntypes"], lay["eff_size"]
    raw = bytes.fromhex(g.runner.cmd(f"rd {g.sym['gTypeEffectivenessTable']:x} {n * n * es}"))
    lay["eff"] = struct.unpack(f"<{n * n}{'I' if es == 4 else 'H'}", raw)
    lay["move_cache"] = {}
    g._q2 = lay
    return lay


def q2_move(g, lay, move):
    """(type, category, power, accuracy) of a move, from gMovesInfo (bit-fields of word 2)."""
    if move not in lay["move_cache"]:
        raw = bytes.fromhex(g.runner.cmd(f"rd {g.sym['gMovesInfo'] + move * lay['mi'] + 8:x} 8"))
        w0, acc = struct.unpack_from("<IH", raw)
        lay["move_cache"][move] = ((w0 >> 16) & 31, (w0 >> 21) & 3, w0 >> 23, acc & 127)
    return lay["move_cache"][move]


def q2_battler(g, lay, b):
    bm = lay["bm"]
    raw = bytes.fromhex(g.runner.cmd(f"rd {g.sym['gBattleMons'] + b * bm:x} {bm}"))
    sp, atk, dfn, spe, spa, spd = struct.unpack_from("<6H", raw, 0)
    return dict(species=sp, atk=atk, defn=dfn, spa=spa, spd=spd,
                moves=struct.unpack_from("<4H", raw, lay["moves"]),
                stages=struct.unpack_from("<8b", raw, lay["stages"]),
                types=[t for t in raw[lay["types"]:lay["types"] + 3]],
                pp=list(raw[lay["pp"]:lay["pp"] + 4]),
                hp=struct.unpack_from("<H", raw, lay["hp"])[0], maxhp=struct.unpack_from("<H", raw, lay["maxhp"])[0],
                level=raw[lay["level"]], ability=struct.unpack_from("<H", raw, lay["ability"])[0])


def q2_stage(s):
    return (2 + s - 6) / 2 if s >= 6 else 2 / (2 + 6 - s)


def q2_damage(g, lay, move, atk, dfn):
    """Expected damage as a share of the target's HP (capped at 1: a KO)."""
    mtype, cat, power, acc = q2_move(g, lay, move)
    if power == 0 or cat not in (lay["phys"], lay["special"]) or dfn["hp"] == 0:
        return 0.0
    power = 60 if power == 1 else power      # variable-power moves
    st = lay["stat"]
    if cat == lay["phys"]:
        a = atk["atk"] * q2_stage(atk["stages"][st["atk"]])
        d = dfn["defn"] * q2_stage(dfn["stages"][st["defn"]])
    else:
        a = atk["spa"] * q2_stage(atk["stages"][st["spa"]])
        d = dfn["spd"] * q2_stage(dfn["stages"][st["spd"]])
    dmg = (2 * atk["level"] / 5 + 2) * power * a / max(d, 1) / 50 + 2
    if mtype in atk["types"]:
        dmg *= 1.5
    for t in set(dfn["types"]) - set(lay["no_types"]):
        dmg *= lay["eff"][mtype * lay["ntypes"] + t] / 4096
    dmg *= (acc or 100) / 100
    return min(1.0, dmg / dfn["hp"])


def q2_best_slot(g, lay, battler, foes):
    me = q2_battler(g, lay, battler)
    targets = [q2_battler(g, lay, f) for f in foes]
    targets = [t for t in targets if t["hp"] > 0 and t["species"]] or targets[:1]
    best, slot = -1.0, 0
    for i, mv in enumerate(me["moves"]):
        if not mv or not me["pp"][i]:
            continue
        score = max((q2_damage(g, lay, mv, me, t) for t in targets), default=0.0)
        if score > best:
            best, slot = score, i
    return slot


def q2_normalize_team(g, team, ivs):
    """The given IVs, no EVs, neutral nature, full HP: overwrite the TEAM's calculated stats (the
    plain, unencrypted part of struct Pokemon). Battles copy these; only a level-up recalculates them."""
    import balance
    lay = q2_layout(g)
    for i, (species, _lv) in enumerate(team):
        base = lay["party"] + i * lay["mon"]
        level = g.read(base + lay["mon_level"], 1)
        s, _ = balance.stats_at(species.removeprefix("SPECIES_"), level, ivs[i])
        data = struct.pack("<7H", s["hp"], s["hp"], s["atk"], s["defn"], s["spe"], s["spa"], s["spd"])
        g.runner.cmd(f"wd {base + lay['mon_hp']:x} {data.hex()}")
    g.step(2)


def q2_assert_screen(g):
    """The freeze watchdog fired on the game's assert screen (AssertfCrashScreen: 'PRESS START TO
    CONTINUE', a recoverable debug-build assert): press START and carry on. FALSE for a real crash."""
    info = getattr(g, "crash_info", None) or {}
    if "CrashScreen" not in info.get("where", ""):
        return False
    g.log(f"Q2 ASSERT screen ({info.get('where')}): START to continue")
    g.crash_info = None
    g.stalled = 0
    g.press("START", 4, 30)
    g.stalled = 0
    return True


def q2_ko_counter(g):
    """(address, bit) of gBattleStruct->battlerKOAnimsRunning (a 3-bit field, so no offsetof): from
    the playtest ELF's DWARF once, then cached with the harness constants."""
    key = "__q2_battlerKOAnimsRunning_bit"
    if key not in g.const.values:
        import subprocess
        out = subprocess.run(["arm-none-eabi-readelf", "--debug-dump=info", g.elf], capture_output=True,
                             text=True).stdout
        m = re.search(r"DW_AT_name\s*:.*: battlerKOAnimsRunning\n(?:.*\n){0,6}?.*DW_AT_data_bit_offset:\s*(\d+)", out)
        g.const.values[key] = int(m.group(1)) if m else -1
        try:
            json.dump(g.const.values, open(g.const.cache_path, "w"), indent=0, sort_keys=True)
        except OSError:
            pass
    bit = g.const.values[key]
    if bit < 0:
        return None
    return g.read("gBattleStruct", 4) + bit // 8, bit % 8


def q2_softlock(g):
    """The KO-animation soft-lock (see q2_battle): TRUE if battlerKOAnimsRunning was stuck and has been
    cleared so the battle goes on."""
    where = q2_ko_counter(g)
    if not where:
        return False
    addr, bit = where
    byte = g.read(addr, 1)
    count = (byte >> bit) & 7
    if not count:
        return False
    g.log(f"Q2 SOFTLOCK: battlerKOAnimsRunning stuck at {count} (controllers={g.controllers()}); clearing it")
    g.screenshot("softlock")
    g.runner.cmd(f"wd {addr:x} {byte & ~(7 << bit) & 0xFF:02x}")
    return True


def q2_battle(g, timeout=60 * 60 * 8, max_turns=150):
    """Play one battle with the best-damage policy. Returns dict(outcome, turns, foe_hp, msgs, asserts,
    softlocks). Two engine bugs in the KO animations (B_ANIMATE_MON_AFTER_KO, launched twice per
    faint by BtlController_HandleFaintAnimation) are worked around and counted, not hidden: the
    debug-build assert screen ("disabled species", START continues) and a soft-lock where
    battlerKOAnimsRunning never returns to 0 and Cmd_waitanimation waits for ever."""
    lay = q2_layout(g)
    s = dict(start=g.frame, turns=0, idle=0, last_msg="", foe_hp=None, msgs=[], tries=0, asserts=0, softlocks=0)
    g.wait_battle()
    g.wait(2)
    double = bool(g.st["battleTypeFlags"] & g.const("BATTLE_TYPE_DOUBLE"))
    foes = [1, 3] if double else [1]
    while g.st["inBattle"] or "Battle" in g.cb2():
        if g.frame - s["start"] > timeout:
            raise TestFailure(f"battle still running after {timeout} frames (controllers={g.controllers()})")
        if not g.st["inBattle"] and g.cb2() == "CB2_Overworld":
            break
        try:
            q2_battle_step(g, lay, foes, s, max_turns)
        except harness.GameCrash:
            if not q2_assert_screen(g):
                raise
            s["asserts"] += 1
        if s["idle"] >= 600 and q2_softlock(g):   # 1200 frames with nothing to press
            s["softlocks"] += 1
            s["idle"] = 0
    outcome = g.st["battleOutcome"]
    g.log(f"battle over: outcome {outcome} after {s['turns']} turns, {g.frame - s['start']} frames")
    return dict(outcome=outcome, turns=s["turns"], foe_hp=s["foe_hp"] or [], msgs=s["msgs"], asserts=s["asserts"],
                softlocks=s["softlocks"])


def q2_foe_party_hp(g, lay):
    """[(hp, maxHP)] of the whole opposing party (gParties[B_TRAINER_OPPONENT_A], the plain part of
    struct Pokemon), so a loss to a trainer counts the animals not sent out yet too."""
    base = g.sym["gParties"] + g.const("B_TRAINER_OPPONENT_A") * 6 * lay["mon"]
    raw = bytes.fromhex(g.runner.cmd(f"rd {base:x} {6 * lay['mon']}"))
    out = []
    for i in range(6):
        hp, mx = struct.unpack_from("<HH", raw, i * lay["mon"] + lay["mon_hp"])
        if mx:
            out.append((hp, mx))
    return out


def q2_battle_step(g, lay, foes, s, max_turns):
    """One input decision of q2_battle (s: its state)."""
    cb2 = g.cb2()
    ctrl = g.controllers() if g.st["inBattle"] else []
    who = next((i for i, f in enumerate(ctrl) if f in ("HandleInputChooseAction", "HandleInputChooseMove")), None)
    if who is not None and ctrl[who] == "HandleInputChooseAction":
        if who == 0:
            s["turns"] += 1
            s["foe_hp"] = q2_foe_party_hp(g, lay)
            if s["turns"] > max_turns:
                raise TestFailure(f"battle: more than {max_turns} turns")
        g.press("LEFT", 2, 2); g.press("UP", 2, 2); g.press("A", 2, 10)
        s["idle"] = s["tries"] = 0
        return
    if who is not None:   # HandleInputChooseMove
        s["tries"] += 1
        slot = q2_best_slot(g, lay, who, foes) if s["tries"] < 4 else 0
        g.press("LEFT", 2, 2); g.press("UP", 2, 2)
        if slot & 1:
            g.press("RIGHT", 2, 4)
        if slot & 2:
            g.press("DOWN", 2, 4)
        g.press("A", 2, 10)
        return
    if "HandleInputChooseTarget" in ctrl:
        g.press("A", 2, 10)
        return
    msg = g.battle_text() if g.st["inBattle"] else ""
    if msg and msg != s["last_msg"] and " " in msg.strip():
        line = msg.replace("\n", " ").strip()
        g.log(f"battle: {line}")
        s["msgs"].append(line)
        s["last_msg"] = msg
    if "PartyMenu" in cb2 or "WaitForMonSelection" in ctrl:
        # A faint: 'use next?' YES opened the TEAM, or a trainer battle's forced switch.
        # Driven by the party menu's own tasks: list -> next slot, A; submenu -> SEND OUT;
        # "no energy left" / "already in battle" -> dismiss, back to the list, next slot.
        tasks = g.tasks()
        if "Task_HandleSelectionMenuInput" in tasks:
            g.press("A", 4, 20)
        elif "Task_PrintAndWaitForText" in tasks or "Task_ReturnToChooseMonAfterText" in tasks:
            g.press("A", 4, 20)
        elif "Task_HandleChooseMonInput" in tasks:
            g.press("DOWN", 4, 10)
            g.press("A", 4, 20)
        else:
            g.step(2, 0)
        return
    if "give up on having" in msg and not g.text_active():
        g.press("A", 2, 20)   # a level-up move prompt: YES, keep the old moves
        s["last_msg"] = ""
        return
    if "Use next" in msg and not g.text_active():
        g.press("A", 2, 20)
        s["last_msg"] = ""
        return
    if g.text_waiting():
        g.press("B", 2, 2)
        s["idle"] = 0
        return
    s["idle"] += 1
    if s["idle"] % 30 == 0:
        g.press("B", 2, 2)
    g.step(2, 0)


def q2_start_tile(mi, how, script):
    """(tile, direction): where to quick-start and which way to step or face. Grass is fine
    (encounters are off), triggers and objects are not."""
    def ok(t):
        return t in mi.reachable and t not in mi.blocked_by_objects and t not in mi.trigger_tiles

    if how == "talk":
        obj = next(o for o in mi.objects if o["script"] == script)
        ox, oy = obj["x"], obj["y"]
        for d in ("up", "right", "left", "down"):
            dx, dy = world.DIR_STEP[d]
            n = (ox - dx, oy - dy)
            if ok(n):
                return n, d
        raise TestFailure(f"no free tile next to {script}'s object at {(ox, oy)}")
    tiles = [t for t, e in mi.trigger_tiles.items() if e["script"] == script]
    best = None
    for t in sorted(tiles):
        for d, (dx, dy) in world.DIR_STEP.items():
            n = (t[0] - dx, t[1] - dy)
            if ok(n):
                score = abs(n[0] - (mi.arrival or n)[0]) + abs(n[1] - (mi.arrival or n)[1])
                if best is None or score < best[0]:
                    best = (score, n, d)
    if not best:
        raise TestFailure(f"no free tile next to a {script} trigger")
    return best[1], best[2]


def q2_fight(g, line, fight, team, rows, ivs=None):
    act, fid, kind, map_name, how, script = fight
    ivs = ivs or [15] * len(team)
    mi = world.map_info(map_name)
    story = 1 if act == 0 else 18 if act == 9 else 2 * act + (1 if kind == "review" else 0)
    tile, d = q2_start_tile(mi, how, script)
    flags = ["FLAG_STRATA_DIG_DONE", "FLAG_STRATA_BLM_PERMIT"] + (["FLAG_STRATA_COLBY_SEEN"] if act == 9 else []) \
        + [f"(TRAINER_FLAGS_START + {t})" for t in Q2_THEO_DONE.get(fid, [])]
    # Subplot at its last value: no present-day interlude starts on the hub maps.
    vars_ = [("VAR_STARTER_MON", Q2_LINES[line]), ("VAR_STRATA_SUBPLOT", "SUBPLOT_COUNT - 1")]
    g.quickstart(mi.id, *tile, story=story, era=act, party=team, items=[("ITEM_POKE_BALL", 5)],
                 flags=flags, vars=vars_, battle_anim=Q2_ANIM)
    q2_normalize_team(g, team, ivs)
    g.log(f"Q2 {line} {fid}: TEAM {team}, IVs {ivs}")
    if how == "talk":
        g.face(d)
        g.press("A")
    else:
        g.walk(d, 1)
    g.wait(10)
    battles, t0 = 0, g.frame
    while True:
        if g.frame - t0 > 60 * 60 * 15:
            raise TestFailure(f"{fid}: still running after 15 game minutes (tasks={g.tasks()})")
        if g.st["inBattle"]:
            battles += 1
            r = q2_battle(g)
            g.wait_until(lambda: not g.st["inBattle"], 3000, "the end of the battle")
            party = g.party()
            won = r["outcome"] in (1, 7)
            hp = sum(m["hp"] for m in party) if won else 0
            mx = sum(m["maxHP"] for m in party) or 1
            foe = sum(h for h, _ in r["foe_hp"]) / (sum(m for _, m in r["foe_hp"]) or 1)
            rows.append(dict(starter=line, act=act, fight=fid + (f"_{battles}" if fid == "gauntlet" else ""),
                             kind=kind, lead=team[0][0].removeprefix("SPECIES_"), level=team[0][1],
                             team="/".join(s.removeprefix("SPECIES_").title() for s, _ in team),
                             outcome=Q2_OUTCOMES.get(r["outcome"], str(r["outcome"])), turns=r["turns"],
                             team_hp=round(100 * hp / mx),
                             lead_hp=round(100 * party[0]["hp"] / max(1, party[0]["maxHP"])) if won else 0,
                             fainted=sum(1 for m in party if m["hp"] == 0) if won else len(team),
                             foe_hp_left=0 if won else round(100 * foe), engine=r["asserts"] + r["softlocks"]))
            g.log(f"Q2 result: {rows[-1]}")
            if kind == "final" or not won:
                return   # the ending (credits, then a soft reset) or a whiteout: done here
            continue
        if g.text_waiting():
            g.press("A", 2, 4)
            continue
        if field_free(g) and g.frame - t0 > 30:
            break
        if (g.menu_open() or "SaveGameTask" in g.tasks()) and not g.text_active():
            g.press("A", 4, 20)
            continue
        g.step(2, 0)
    if not battles:
        raise TestFailure(f"{fid}: the script started no battle")


Q2_FIELDS = ["starter", "act", "fight", "kind", "lead", "level", "team", "outcome", "turns", "team_hp", "lead_hp",
             "fainted", "foe_hp_left", "engine"]


def q2_recover(g, tries=3000):
    """After a failed fight: B through whatever is open (a battle is run from or lost) until the
    overworld takes input again, so the next quick-start is accepted."""
    for i in range(tries):
        if field_free(g) and not g.st["inBattle"]:
            return
        if g.st["inBattle"] and "HandleInputChooseAction" in g.controllers():
            g.press("RIGHT", 2, 2); g.press("DOWN", 2, 2); g.press("A", 2, 10)   # RUN
            continue
        if g.st["inBattle"] and i % 100 == 99:
            q2_softlock(g)
        g.press("B" if i % 3 else "A", 2, 6)
    raise TestFailure("could not get back to the overworld after a failed fight")


def starter_run(g, args, line):
    balance, lines, model = q2_data()
    starters = {name: world.STARTERS[i].removeprefix("SPECIES_") for name, i in Q2_LINES.items()}
    g.max_frames = 40_000_000 * Q2_REPEAT
    rows = []
    try:
        q2_fights(g, line, balance, lines, model, starters, rows)
    finally:
        q2_write(g, line, rows)
    lost = sorted({r["fight"] for r in rows if r["outcome"] not in ("won", "caught") and r["kind"] != "survival"})
    g.check(not lost, f"{line}: every boss, set piece and review won ({', '.join(lost) or 'all won'})")


def q2_fights(g, line, balance, lines, model, starters, rows):
    for fight in Q2_FIGHTS:
        act, fid, kind = fight[:3]
        if Q2_ONLY and fid not in Q2_ONLY:
            continue
        team = q2_team(line, act, q2_level(act, kind, model), lines, starters, balance.TEAM_SIZE[act])
        ivs = q2_ivs(line, act, lines, starters, len(team))
        for attempt in range(Q2_REPEAT):
            n = len(rows)
            try:
                q2_fight(g, line, fight, team, rows, ivs)
            except harness.GameCrash:
                raise
            except TestFailure as e:
                g.log(f"Q2 {fid} error: {e}")
                g.screenshot(f"error_{fid}")
                q2_recover(g)
                rows.append(dict(starter=line, act=act, fight=fid, kind=kind,
                                 lead=team[0][0].removeprefix("SPECIES_"), level=team[0][1], team="",
                                 outcome="error", turns=0, team_hp=0, lead_hp=0, fainted=0, foe_hp_left=0,
                                 engine=0))
            for r in rows[n:]:
                r["attempt"] = attempt + 1


def q2_write(g, line, rows):
    """fights.csv and fights.md in the scenario's output folder."""
    fields = Q2_FIELDS + ["attempt"]
    with open(os.path.join(g.out, "fights.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fields, restval="")
        w.writeheader()
        w.writerows(rows)
    md = [f"# Starter run: {line} (TEAM levels from balance.exp_model, {Q2_REPEAT} attempt(s) per fight)\n",
          "| " + " | ".join(fields) + " |", "|" + "---|" * len(fields)]
    md += ["| " + " | ".join(str(r.get(k, "")) for k in fields) + " |" for r in rows]
    open(os.path.join(g.out, "fights.md"), "w").write("\n".join(md) + "\n")


@scenario
def starter_run_mammal(g, args):
    """Q2: the mammal line (Cimolestes) through every boss, set piece and peer review (fights.csv)."""
    starter_run(g, args, "mammal")


@scenario
def starter_run_bird(g, args):
    """Q2: the bird line (Asteriornis) through every boss, set piece and peer review (fights.csv)."""
    starter_run(g, args, "bird")


@scenario
def starter_run_turtle(g, args):
    """Q2: the turtle line (Emarginachel) through every boss, set piece and peer review (fights.csv)."""
    starter_run(g, args, "turtle")
