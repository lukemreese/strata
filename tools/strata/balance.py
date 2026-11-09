#!/usr/bin/env python3
"""Balance report for Strata, one section per act, printed as markdown.

Usage (from the repo root):  python3 tools/strata/balance.py [--strict] [--playtest DIR]

--playtest DIR adds the headless starter playthroughs (Q2): every fights.csv that
`tools/strata/playtest/run.py starter_runs --out DIR` left under DIR, as a fight x starter
table with its own flags (PLAYTEST LOSS, REVIEW HARD, TOO EASY, SURVIVAL WON EASILY,
STARTER GAP). The "EXP model" section is always printed: the level a normal player has at
each fight (exp_model()), which is also the level the starter runs use; LEVEL GAP flags a
boss far above it.

Reads, and never writes:
  tools/strata/roster/          species, masses, stat weights, focal flag
  tools/strata/gen_species.py   the BST formula (base_stats), so the report always
                                matches the generated data
  tools/strata/maps/            wild encounter tables and each map's era
  data/maps/Strata*/scripts.inc boss battles (setwildbattle species, level[s])
  src/data/trainers_strata.party peer-review trainers (REVIEW OVERTUNED / REVIEW WEAK flags)
  src/data/lineages.h           era level floors (sEraLevelFloor), descents and
                                extinctions, to follow the three starter lines

Stats "at level" use the game's stat formula with IV 15, no EVs and a neutral
nature, summed over the six stats ("stat total at level", STL). The expected
party is the three starter lines on their default (no-pressure) path, at the
EXP model's level at the boss (exp_model(): what a normal player reaches with
the act's wild battles; the era floor on arrival), with the IVs lineage
resilience (include/lineage.h, F7) has given them by then.

Flags (see docs/strata_outline.md §3.1):
  NO VIABLE CATCH  no land wild species reaches CATCH_VIABLE of the boss's STL
  FAR BELOW BOSS   a land wild species, at its highest level, is under WILD_FLOOR
                   of the boss's STL
  OVERTUNED WILD   a wild's STL exceeds the expected party median by over 35%
  PARTY GAP        the expected party median is under PARTY_FLOOR of the boss's STL
  FLOOR            the era floor is above the act's lowest wild level, or more
                   than FLOOR_GAP levels below it
  WATER ONLY       species only in water/fishing tables (no surf or rod yet, A4)
Water and fishing tables are listed but not counted as catches.

--strict exits 1 if any flag is raised, for CI-style checks.
"""

import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import maps  # noqa: E402
from gen_species import STAT_KEYS, base_stats, const_name  # noqa: E402
from roster import SPECIES  # noqa: E402

IV = 15
CATCH_VIABLE = 0.75
WILD_FLOOR = 0.60
PARTY_FLOOR = 0.70
OVERTUNED = 1.35
FLOOR_GAP = 5
REVIEW_MAX = 1.15  # a peer-review animal's STL over this share of the party median is flagged
REVIEW_MAX_FINAL = 1.25  # Dr. Halvorsen's final exam may peak a little higher (the Tyrannosaur ace)
REVIEW_MIN = 0.70
STARTERS = ["CIMOLESTES", "ASTERIORNIS", "EMARGINACHEL"]
STARTER_LEVEL = 5
ACT_NAMES = ["Present dig", "Hell Creek", "Impact winter", "Corral Bluffs", "Bighorn Basin (PETM)",
             "Green River / Bridger", "White River", "Ashfall", "Ice Age (Trap Cave)", "Epilogue"]

BY_CONST = {const_name(sp): sp for sp in SPECIES}


def stats_at(species, level, iv=IV):
    base, bst = base_stats(BY_CONST[species])
    out = {}
    for k in STAT_KEYS:
        core = (2 * base[k] + iv) * level // 100
        out[k] = core + level + 10 if k == "hp" else core + 5
    return out, bst


def stl(species, level, iv=IV):
    return sum(stats_at(species, level, iv)[0].values())


def read_resilience():
    """(per era, stasis bonus) from include/lineage.h (RESILIENCE_IV_PER_ERA, _STASIS_BONUS)."""
    text = open(os.path.join(ROOT, "include/lineage.h")).read()
    get = lambda name: int(re.search(rf"#define {name}\s+(\d+)", text).group(1)) if name in text else 0
    return get("RESILIENCE_IV_PER_ERA"), get("RESILIENCE_STASIS_BONUS")


def resilience_iv(path, act, start_iv=IV):
    """IV of a lineage caught (or chosen) in act 1 and carried to `act` along `path` (one species per
    era index, as starter_lines gives): every load from act 2 on adds the resilience raise, more if
    the species stayed the same (src/lineage.c, Lineage_ResilientIV)."""
    per_era, stasis = read_resilience()
    iv = start_iv
    for k in range(2, act + 1):
        if path[k] is None:
            break
        iv = min(31, iv + per_era + (stasis if path[k] == path[k - 1] else 0))
    return iv


def bst(species):
    return base_stats(BY_CONST[species])[1]


def strip(s):
    return s[len("SPECIES_"):] if s.startswith("SPECIES_") else s


# --------------------------------------------------------------------------
# src/data/lineages.h
# --------------------------------------------------------------------------
def read_lineages():
    with open(os.path.join(ROOT, "src/data/lineages.h")) as f:
        text = f.read()
    # The default descendant is the DESCENT_DEFAULT entry of each option list.
    defaults = {m.group(1): m.group(2) for m in re.finditer(
        r"struct DescentOption (sDescent_\w+)\[\]\s*=\s*\{[^}]*?DESCENT_DEFAULT\(SPECIES_(\w+)\)", text)}
    descents = {}
    for m in re.finditer(r"\{\s*SPECIES_(\w+),\s*(ERA_\w+),\s*(sDescent_\w+)\s*\}", text):
        if m.group(3) in defaults:  # a branch-only table has no default: the lineage stays
            descents[(m.group(1), m.group(2))] = defaults[m.group(3)]
    lists = {m.group(1): re.findall(r"SPECIES_(\w+)", m.group(2)) for m in re.finditer(
        r"u16 (sExtinctions_\w+)\[\]\s*=\s*\{(.*?)\};", text, re.S)}
    extinct = {}
    block = re.search(r"sEraExtinctions\[ERA_COUNT\]\s*=\s*\{(.*?)\};", text, re.S).group(1)
    for era, name in re.findall(r"\[(ERA_\w+)\]\s*=\s*(\w+)", block):
        extinct[era] = [s for s in lists[name] if s != "NONE"]
    block = re.search(r"sEraLevelFloor\[ERA_COUNT\]\s*=\s*\{(.*?)\};", text, re.S).group(1)
    floors = {era: int(lv) for era, lv in re.findall(r"\[(ERA_\w+)\]\s*=\s*(\d+)", block)}
    return descents, extinct, floors


def starter_lines(descents, extinct):
    """Default-path species of each starter line, per era index (None once lost)."""
    lines = {}
    for start in STARTERS:
        cur, path = start, []
        for era in maps.ERAS:
            if cur is not None:
                cur = descents.get((cur, era), cur)
                if cur in extinct.get(era, []):
                    cur = None
            path.append(cur)
        lines[start] = path
    return lines


# --------------------------------------------------------------------------
# EXP model: the level a normal player has at each fight (Q2)
# --------------------------------------------------------------------------
# The game's EXP rules (include/config/battle.h, item.h; battle_script_commands.c): Gen 9
# scaled EXP, yield x foe level / 5 x ((2F+10)/(F+M+10))^2.5 + 1; the animal sent out gets it
# all, every other TEAM animal half (FLAG_STRATA_EXP_SHARE, the Gen 6 Exp. Share). A normal
# player knocks out WILD_KOS_PER_ACT wild animals per act (about five per map), the act's land
# table in turn, leading with each TEAM animal in turn, and carries its level from act to act;
# the rig raises it to the era floor on arrival. The set piece comes half-way through the act,
# the boss at the end, the peer review after the boss.
WILD_KOS_PER_ACT = 20
TEAM_SIZE = [1, 3, 3, 4, 4, 4, 5, 5, 5, 6]   # by act: the starter alone at the dig, 6 in the epilogue
GROWTH = {const_name(sp): sp["growth"] for sp in SPECIES}


def exp_for_level(growth, n):
    """Total EXP at the start of level n (src/data/pokemon/experience_tables.h)."""
    if growth == "MEDIUM_FAST":
        return n ** 3
    if growth == "FAST":
        return 4 * n ** 3 // 5
    if growth == "SLOW":
        return 5 * n ** 3 // 4
    if growth == "MEDIUM_SLOW":
        return 6 * n ** 3 // 5 - 15 * n * n + 100 * n - 140
    raise ValueError(f"growth rate {growth} not modelled")


def level_for_exp(growth, exp):
    n = 1
    while n < 100 and exp_for_level(growth, n + 1) <= exp:
        n += 1
    return n


def exp_gain(species, foe_level, level, sent_out):
    """EXP for one knockout of `species` at foe_level, for a TEAM animal at `level`."""
    base = round(bst(species) * 0.3) * foe_level // 5   # expYield = 0.3 x BST (gen_species.py)
    if not sent_out:
        base //= 2
    return int(base * ((2 * foe_level + 10) / (foe_level + level + 10)) ** 2.5) + 1


def exp_model(kos=WILD_KOS_PER_ACT):
    """{act: {"arrive", "setpiece", "boss", "review"}: level} for the starter lines (median of
    the three; they share growth rates, so they agree), from Lv 5 at the dig."""
    descents, extinct, floors = read_lineages()
    lines = starter_lines(descents, extinct)
    acts = act_encounters()
    bosses = read_bosses()
    out = {0: dict(arrive=STARTER_LEVEL, setpiece=STARTER_LEVEL, boss=STARTER_LEVEL, review=STARTER_LEVEL)}
    per_line = {s: (STARTER_LEVEL, exp_for_level(GROWTH[s], STARTER_LEVEL)) for s in STARTERS}
    for idx, era in enumerate(maps.ERAS):
        if idx == 0 or era not in acts:
            continue
        land = sorted(acts[era]["land"].items())
        wild = [(sp, (lo + hi) // 2) for sp, (lo, hi) in land]
        fights = [f for _, fs in bosses.get(era, []) for f in fs]
        boss = max(fights, key=lambda f: f[1]) if fights else None
        setpiece = min(fights, key=lambda f: f[1]) if fights else None
        n = TEAM_SIZE[idx]
        res = {k: [] for k in ("arrive", "setpiece", "boss", "review")}
        for s in STARTERS:
            sp = lines[s][idx] or lines[s][idx - 1] or s
            growth = GROWTH.get(sp, "MEDIUM_FAST")
            level, _ = per_line[s]
            level = max(level, floors.get(era, 0))
            exp = exp_for_level(growth, level)
            res["arrive"].append(level)
            for k in range(kos):
                foe, foe_lv = wild[k % len(wild)]
                exp += exp_gain(foe, foe_lv, level, k % n == 0)
                level = level_for_exp(growth, exp)
                if k == kos // 2 - 1:
                    res["setpiece"].append(level)
                    if setpiece:
                        exp += exp_gain(setpiece[0], setpiece[1], level, False)
                        level = level_for_exp(growth, exp)
            res["boss"].append(level)
            if boss:
                exp += exp_gain(boss[0], boss[1], level, False)
                level = level_for_exp(growth, exp)
            res["review"].append(level)
            per_line[s] = (level, exp)
        out[idx] = {k: int(statistics.median(v)) for k, v in res.items()}
    return out


# --------------------------------------------------------------------------
# Maps and bosses
# --------------------------------------------------------------------------
def read_bosses():
    bosses = {}
    pat = re.compile(r"^\s*setwildbattle\s+SPECIES_(\w+),\s*(\d+)(?:,\s*\w+,\s*SPECIES_(\w+),\s*(\d+))?", re.M)
    for m in maps.MAPS:
        path = os.path.join(ROOT, "data/maps", m["name"], "scripts.inc")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for b in pat.finditer(f.read()):
                fights = [(b.group(1), int(b.group(2)))]
                if b.group(3):
                    fights.append((b.group(3), int(b.group(4))))
                bosses.setdefault(m["era"], []).append((m["name"], fights))
    return bosses


def act_encounters():
    """era -> {"land": {species: (min, max)}, "water": {...}, "maps": [names]}"""
    acts = {}
    for m in maps.MAPS:
        enc = m.get("encounters")
        if not enc:
            continue
        a = acts.setdefault(m["era"], {"land": {}, "water": {}, "maps": []})
        a["maps"].append(m["name"])
        for table, kind in (("land_mons", "land"), ("water_mons", "water"), ("fishing_mons", "water")):
            for slot in enc.get(table, []):
                sp = strip(slot["species"])
                lo, hi = a[kind].get(sp, (999, 0))
                a[kind][sp] = (min(lo, slot["min_level"]), max(hi, slot["max_level"]))
    return acts


# --------------------------------------------------------------------------
# Peer-review trainers (src/data/trainers_strata.party)
# --------------------------------------------------------------------------
def read_trainers():
    """[(id, name, [(species, level)])] from the Strata party file."""
    path = os.path.join(ROOT, "src/data/trainers_strata.party")
    trainers = []
    for block in re.split(r"^=== ", open(path, encoding="utf-8").read(), flags=re.M)[1:]:
        tid = block.split(" ===")[0]
        name = re.search(r"^Name: (.*)$", block, re.M).group(1)
        mons = re.findall(r"^SPECIES_(\w+)\nLevel: (\d+)", block, re.M)
        trainers.append((tid, name, [(sp, int(lv)) for sp, lv in mons]))
    return trainers


def trainer_act(tid):
    """The act a peer-review trainer belongs to (its expected party), 9 for the epilogue."""
    m = re.search(r"_ACT(\d)", tid)
    if m:
        return max(int(m.group(1)), 1)  # Theo's first review (act 0) is on the starter, at Lv 5
    return 9


def peer_review_report(party_by_act, lines):
    """Markdown for the peer-review trainers: each animal's STL against the expected party's
    median at the act's boss level. REVIEW OVERTUNED when an animal is over REVIEW_MAX of it
    (a party that finished the act should win), REVIEW WEAK when the team is under REVIEW_MIN."""
    out = ["## Peer review\n",
           "Visiting researchers, Theo and Dr. Halvorsen (`src/data/trainers_strata.party`). STL as above; "
           f"each animal is compared with the expected party median at the act's boss level "
           f"(flag over {REVIEW_MAX:.0%}, {REVIEW_MAX_FINAL:.0%} for Dr. Halvorsen; a team median under "
           f"{REVIEW_MIN:.0%} is flagged weak).\n",
           "| Trainer | Act | Team (Lv, STL) | Last Lv | Team median vs party | Strongest vs party |",
           "|---|---|---|---|---|---|"]
    flags = []
    for tid, name, mons in read_trainers():
        act = trainer_act(tid)
        if tid.endswith("ACT0_BIRD") or "ACT0" in tid:
            med = statistics.median(stl(s, STARTER_LEVEL) for s in STARTERS)
        else:
            med = party_by_act.get(act, (0, 0))[0]
        stls = [stl(sp, lv) for sp, lv in mons]
        team_med = statistics.median(stls)
        top = max(stls)
        ratio_med, ratio_top = team_med / med if med else 0, top / med if med else 0
        notes = []
        if med and ratio_top > (REVIEW_MAX_FINAL if act == 9 else REVIEW_MAX):
            notes.append("REVIEW OVERTUNED")
        if med and ratio_med < REVIEW_MIN:
            notes.append("REVIEW WEAK")
        flags += [(act, f"{n}: {name} ({tid})") for n in notes]
        out.append(f"| {name} ({tid.removeprefix('TRAINER_STRATA_')}) | {act if act < 9 else 'E'} | "
                   + ", ".join(f"{sp.title()} {lv} ({s})" for (sp, lv), s in zip(mons, stls))
                   + f" | {mons[-1][1]} | {ratio_med:.0%} | {ratio_top:.0%}"
                   + (f" **{', '.join(notes)}**" if notes else "") + " |")
    out.append("")
    return out, flags


# --------------------------------------------------------------------------
# EXP model table and the headless playtests (Q2)
# --------------------------------------------------------------------------
LEVEL_GAP = 6        # a boss more than this many levels above the EXP model's TEAM is flagged
EASY_HP = 80         # a boss or set piece won with more TEAM HP left than this (%) is flagged
STARTER_HP_GAP = 20  # a starter whose mean TEAM HP left differs this much from another's is flagged
REVIEW_MIN_WINS = 0.5


def exp_model_report(model):
    """Markdown: the EXP model's TEAM level per act against the act's fights."""
    _, _, floors = read_lineages()
    bosses = read_bosses()
    out = ["## EXP model\n",
           f"The level a normal player has at each fight: {WILD_KOS_PER_ACT} wild knockouts per act "
           "(the act's land table in turn, the TEAM sharing EXP), carried from act to act and raised "
           "to the era floor on arrival (`exp_model()`). The starter runs use these levels.\n",
           "| Act | Floor | Arrive | Set piece | Boss | Review | Boss fights (Lv) | Boss Lv - TEAM Lv |",
           "|---|---|---|---|---|---|---|---|"]
    flags = []
    for idx, era in enumerate(maps.ERAS):
        if idx not in model or idx == 0:
            continue
        m = model[idx]
        fights = [f for _, fs in bosses.get(era, []) for f in fs]
        top = max((lv for _, lv in fights), default=0)
        gap = top - m["boss"] if top else 0
        note = ""
        if top and gap > LEVEL_GAP and idx != 1:   # act 1's tyrannosaur is a survival set piece
            note = " **LEVEL GAP**"
            flags.append((idx, f"LEVEL GAP: the boss (Lv {top}) is {gap} levels above the EXP model's TEAM (Lv {m['boss']})"))
        out.append(f"| {idx} | {floors.get(era, 0)} | {m['arrive']} | {m['setpiece']} | {m['boss']} | {m['review']} | "
                   + ", ".join(f"{s.title()} {lv}" for s, lv in fights) + f" | {gap:+d}{note} |")
    out.append("")
    return out, flags


def read_playtests(path):
    """Rows of every fights.csv under `path` (the starter_run_* output folders)."""
    import csv
    rows = []
    for dirpath, _dirs, files in os.walk(path):
        if "fights.csv" in files and os.path.basename(dirpath).startswith("starter_run_"):
            with open(os.path.join(dirpath, "fights.csv"), newline="") as f:
                rows += list(csv.DictReader(f))
    return rows


def playtest_report(rows):
    """Markdown: fight x starter (wins/attempts, mean TEAM HP left on a win, mean turns), with flags:
    PLAYTEST LOSS (a boss or set piece lost), REVIEW HARD (a review won under half the time),
    TOO EASY (a boss won with the TEAM barely hurt), SURVIVAL WON EASILY (the tyrannosaur),
    STARTER GAP (one starter's TEAM ends fights much healthier than another's)."""
    starters = [s for s in ("mammal", "bird", "turtle") if any(r["starter"] == s for r in rows)]
    order, cells = [], {}
    for r in rows:
        key = (int(r["act"]), r["fight"], r["kind"])
        if key not in order:
            order.append(key)
        cells.setdefault((key, r["starter"]), []).append(r)
    out = ["## Starter playthroughs (headless)\n",
           "`tools/strata/playtest/run.py starter_runs`: every boss, set piece and peer review in story order, "
           "a TEAM of the starter's line plus the act's typical catches at the EXP model's level, best-damage "
           "moves, no items or switching. Cell: wins/attempts, mean TEAM HP left after a win, mean turns "
           "(L: foe HP left when lost).\n",
           "| Act | Fight | Kind | Lv | " + " | ".join(s.title() for s in starters) + " |",
           "|---|---|---|---|" + "---|" * len(starters)]
    flags = []
    hp_by_starter = {s: [] for s in starters}
    for key in order:
        act, fight, kind = key
        line, lv = [], ""
        for s in starters:
            rs = cells.get((key, s), [])
            if not rs:
                line.append("-")
                continue
            lv = rs[0]["level"]
            wins = [r for r in rs if r["outcome"] in ("won", "caught")]
            losses = [r for r in rs if r not in wins]
            hp = statistics.mean(int(r["team_hp"]) for r in wins) if wins else 0
            turns = statistics.mean(int(r["turns"]) for r in rs)
            cell = f"{len(wins)}/{len(rs)}, {hp:.0f}%, {turns:.0f} t"
            if losses:
                foe = statistics.mean(int(r["foe_hp_left"]) for r in losses)
                cell += f" (L: {foe:.0f}%)"
            if kind in ("boss", "setpiece"):
                hp_by_starter[s].append(hp)
                if losses:
                    flags.append((act, f"PLAYTEST LOSS: {fight} ({s}, {len(losses)}/{len(rs)} lost)"))
                elif hp > EASY_HP:
                    flags.append((act, f"TOO EASY: {fight} ({s}, {hp:.0f}% TEAM HP left)"))
            elif kind == "encounter" and losses:
                flags.append((act, f"PLAYTEST LOSS: {fight} ({s}, {len(losses)}/{len(rs)} lost)"))
            elif kind in ("review", "final") and len(wins) < REVIEW_MIN_WINS * len(rs):
                flags.append((act, f"REVIEW HARD: {fight} ({s}, {len(wins)}/{len(rs)} won)"))
            elif kind == "survival" and wins and hp > 50:
                flags.append((act, f"SURVIVAL WON EASILY: {fight} ({s}, {hp:.0f}% TEAM HP left)"))
            engine = sum(int(r.get("engine") or 0) for r in rs)
            if engine:
                cell += f" ({engine} engine)"
                flags.append((act, f"ENGINE BUG: {fight} ({s}, {engine} KO-animation assert screen(s) or soft-lock(s))"))
            line.append(cell)
        out.append(f"| {act if act < 9 else 'E'} | {fight} | {kind} | {lv} | " + " | ".join(line) + " |")
    out.append("")
    means = {s: statistics.mean(v) for s, v in hp_by_starter.items() if v}
    if means:
        out.append("Mean TEAM HP left after the bosses and set pieces: "
                   + ", ".join(f"{s} {m:.0f}%" for s, m in means.items()) + ".\n")
        if max(means.values()) - min(means.values()) > STARTER_HP_GAP:
            flags.append((9, "STARTER GAP: " + ", ".join(f"{s} {m:.0f}%" for s, m in means.items())))
    return out, flags


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
def main():
    strict = "--strict" in sys.argv[1:]
    playtest = None
    if "--playtest" in sys.argv[1:]:
        playtest = sys.argv[sys.argv.index("--playtest") + 1]
    descents, extinct, floors = read_lineages()
    lines = starter_lines(descents, extinct)
    bosses = read_bosses()
    acts = act_encounters()
    model = exp_model()
    out, all_flags = [], []

    out.append("# Strata balance report\n")
    out.append(f"STL = stat total at level (IV {IV}, no EVs, neutral nature). Party = the three "
               "starter lines on their default path, at the EXP model's level at the boss, with the "
               "IVs lineage resilience has given them by then. Generated by `tools/strata/balance.py`.\n")

    party_by_act = {}
    summary = ["| Act | Floor | Wild land Lv | Wild BST | Boss (Lv, BST) | Boss STL | Best catch STL | "
               "Party median STL (Lv) | Flags |",
               "|---|---|---|---|---|---|---|---|---|"]
    sections = []

    for idx, era in enumerate(maps.ERAS):
        enc = acts.get(era)
        fights = [f for _, fs in bosses.get(era, []) for f in fs]
        if not enc and not fights:
            continue
        flags = []
        land = enc["land"] if enc else {}
        water = enc["water"] if enc else {}
        floor = floors.get(era, 0)
        wild_lo = min((lo for lo, _ in land.values()), default=0)
        wild_hi = max((hi for _, hi in land.values()), default=0)
        party_lv = model[idx]["boss"] if idx in model else max(floor, STARTER_LEVEL)
        arrive_lv = model[idx]["arrive"] if idx in model else max(floor, STARTER_LEVEL)

        party = [lines[s][idx] for s in STARTERS if lines[s][idx] is not None]
        party_iv = {lines[s][idx]: resilience_iv(lines[s], idx) for s in STARTERS if lines[s][idx] is not None}
        party_stl = {p: stl(p, party_lv, party_iv[p]) for p in party}
        party_med = statistics.median(party_stl.values()) if party_stl else 0

        # The hardest single fight of the act is the reference boss.
        boss = max(fights, key=lambda f: stl(*f)) if fights else None
        boss_stl = stl(*boss) if boss else 0

        sec = [f"## Act {idx}: {ACT_NAMES[idx]} (`{era}`)\n"]
        if enc:
            sec.append(f"Maps: {', '.join(enc['maps'])}. Era floor {floor}; land wilds Lv {wild_lo}-{wild_hi}; "
                       f"expected party Lv {arrive_lv} on arrival, {party_lv} at the boss.\n")
        if fights:
            sec.append("Boss fights: " + "; ".join(
                f"{name}: " + " + ".join(f"{s.title()} Lv {lv} (BST {bst(s)}, STL {stl(s, lv)})" for s, lv in fs)
                for name, fs in bosses[era]) + "\n")
        if party:
            sec.append("Expected party: " + ", ".join(
                f"{p.title()} (BST {bst(p)}, IV {party_iv[p]}, STL {party_stl[p]} @ Lv {party_lv})" for p in party) + "\n")

        if land:
            sec.append("| Species | Lv | BST | STL @ max Lv | vs boss | vs party median |")
            sec.append("|---|---|---|---|---|---|")
            best = 0
            for sp, (lo, hi) in sorted(land.items(), key=lambda kv: -bst(kv[0])):
                s = stl(sp, hi)
                best = max(best, s)
                vb = s / boss_stl if boss_stl else 0
                vp = s / party_med if party_med else 0
                note = []
                if boss_stl and vb < WILD_FLOOR:
                    note.append("FAR BELOW BOSS")
                if party_med and vp > OVERTUNED:
                    note.append("OVERTUNED WILD")
                flags += [f"{n}: {sp.title()}" for n in note]
                sec.append(f"| {sp.title()} | {lo}-{hi} | {bst(sp)} | {s} | "
                           f"{f'{vb:.0%}' if boss_stl else '-'} | {f'{vp:.0%}' if party_med else '-'} "
                           f"{' **' + ', '.join(note) + '**' if note else ''}|")
            sec.append("")
            if boss_stl and best < CATCH_VIABLE * boss_stl:
                flags.append(f"NO VIABLE CATCH: best land catch STL {best} < {CATCH_VIABLE:.0%} of boss {boss_stl}")
        else:
            best = 0
        only_water = sorted(set(water) - set(land))
        if only_water:
            flags.append("WATER ONLY: " + ", ".join(s.title() for s in only_water))
        if party_med and boss_stl and party_med < PARTY_FLOOR * boss_stl:
            flags.append(f"PARTY GAP: party median {party_med:.0f} < {PARTY_FLOOR:.0%} of boss {boss_stl}")
        if land and floor:
            if floor > wild_lo:
                flags.append(f"FLOOR: era floor {floor} is above the lowest wild level {wild_lo}")
            elif wild_lo - floor > FLOOR_GAP:
                flags.append(f"FLOOR: era floor {floor} is {wild_lo - floor} levels below the wilds")
        for s in STARTERS:
            if lines[s][idx] is None and (idx == 0 or lines[s][idx - 1] is not None):
                flags.append(f"STARTER LOST: the {s.title()} line goes extinct on the default path")

        sec.append("Flags: none\n" if not flags else "Flags:\n")
        sec += [f"- {f}" for f in flags]
        sec.append("")
        sections += sec
        party_by_act[idx] = (party_med, party_lv)
        all_flags += [(idx, f) for f in flags]

        boss_txt = " + ".join(f"{s.title()} {lv} ({bst(s)})" for s, lv in fights) if fights else "-"
        wild_bst = (f"{min(bst(s) for s in land)}-{max(bst(s) for s in land)}" if land else "-")
        kinds = sorted({f.split(":")[0] for f in flags})
        summary.append(f"| {idx} | {floor} | {f'{wild_lo}-{wild_hi}' if land else '-'} | {wild_bst} | {boss_txt} | "
                       f"{boss_stl or '-'} | {best or '-'} | {f'{party_med:.0f} ({party_lv})' if party else '-'} | "
                       f"{', '.join(kinds) or 'ok'} |")

    review_lines, review_flags = peer_review_report(party_by_act, lines)
    all_flags += [(a, f) for a, f in review_flags]
    model_lines, model_flags = exp_model_report(model)
    all_flags += model_flags
    play_lines = []
    if playtest:
        rows = read_playtests(playtest)
        if not rows:
            sys.exit(f"balance.py: no starter_run_*/fights.csv under {playtest}")
        play_lines, play_flags = playtest_report(rows)
        all_flags += play_flags
        play_lines += ["Flags:\n"] + [f"- {f}" for _, f in play_flags] + [""] if play_flags else ["Flags: none\n"]

    out.append("## Summary\n")
    out += summary
    out.append("")
    out += model_lines
    out += play_lines
    out += review_lines
    out += sections
    print("\n".join(out))
    if strict and all_flags:
        sys.exit(1)


if __name__ == "__main__":
    main()
