#!/usr/bin/env python3
"""Balance report for Strata, one section per act, printed as markdown.

Usage (from the repo root):  python3 tools/strata/balance.py [--strict]

Reads, and never writes:
  tools/strata/roster/          species, masses, stat weights, focal flag
  tools/strata/gen_species.py   the BST formula (base_stats), so the report always
                                matches the generated data
  tools/strata/maps/            wild encounter tables and each map's era
  data/maps/Strata*/scripts.inc boss battles (setwildbattle species, level[s])
  src/data/lineages.h           era level floors (sEraLevelFloor), descents and
                                extinctions, to follow the three starter lines

Stats "at level" use the game's stat formula with IV 15, no EVs and a neutral
nature, summed over the six stats ("stat total at level", STL). The expected
party is the three starter lines on their default (no-pressure) path, at the
level the outline expects at the boss (docs/strata_outline.md §3.1: the act's
highest land wild level; the era floor on arrival).

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
STARTERS = ["CIMOLESTES", "ASTERIORNIS", "EMARGINACHEL"]
STARTER_LEVEL = 5
ACT_NAMES = ["Present dig", "Hell Creek", "Impact winter", "Corral Bluffs", "Bighorn Basin (PETM)",
             "Green River / Bridger", "White River", "Ashfall", "Ice Age (Trap Cave)", "Epilogue"]

BY_CONST = {const_name(sp): sp for sp in SPECIES}


def stats_at(species, level):
    base, bst = base_stats(BY_CONST[species])
    out = {}
    for k in STAT_KEYS:
        core = (2 * base[k] + IV) * level // 100
        out[k] = core + level + 10 if k == "hp" else core + 5
    return out, bst


def stl(species, level):
    return sum(stats_at(species, level)[0].values())


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
# Report
# --------------------------------------------------------------------------
def main():
    strict = "--strict" in sys.argv[1:]
    descents, extinct, floors = read_lineages()
    lines = starter_lines(descents, extinct)
    bosses = read_bosses()
    acts = act_encounters()
    out, all_flags = [], []

    out.append("# Strata balance report\n")
    out.append(f"STL = stat total at level (IV {IV}, no EVs, neutral nature). Party = the three "
               "starter lines on their default path. Generated by `tools/strata/balance.py`.\n")

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
        party_lv = wild_hi or max((lv for _, lv in fights), default=STARTER_LEVEL)
        arrive_lv = max(floor, STARTER_LEVEL)

        party = [lines[s][idx] for s in STARTERS if lines[s][idx] is not None]
        party_stl = {p: stl(p, party_lv) for p in party}
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
                f"{p.title()} (BST {bst(p)}, STL {party_stl[p]} @ Lv {party_lv})" for p in party) + "\n")

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
        all_flags += [(idx, f) for f in flags]

        boss_txt = " + ".join(f"{s.title()} {lv} ({bst(s)})" for s, lv in fights) if fights else "-"
        wild_bst = (f"{min(bst(s) for s in land)}-{max(bst(s) for s in land)}" if land else "-")
        kinds = sorted({f.split(":")[0] for f in flags})
        summary.append(f"| {idx} | {floor} | {f'{wild_lo}-{wild_hi}' if land else '-'} | {wild_bst} | {boss_txt} | "
                       f"{boss_stl or '-'} | {best or '-'} | {f'{party_med:.0f} ({party_lv})' if party else '-'} | "
                       f"{', '.join(kinds) or 'ok'} |")

    out.append("## Summary\n")
    out += summary
    out.append("")
    out += sections
    print("\n".join(out))
    if strict and all_flags:
        sys.exit(1)


if __name__ == "__main__":
    main()
