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
    if name == "all":
        return ["watchdog_selftest", "new_game_smoke", "battle_smoke", "forecast_smoke", "pressure_chart_smoke",
                "peer_review_smoke", "act_tour", "extinction_smoke", "story_interludes"] + [f"boss_{a}" for a in range(1, 9)]
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
