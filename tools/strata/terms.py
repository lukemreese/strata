#!/usr/bin/env python3
"""Strata vocabulary pass: take the Pokemon branding out of player-visible stock text.

Strata never calls the creatures "Pokemon" (see docs/strata_design.md, "Vocabulary"). This is
the script that did the bulk of the rewrite of the shared stock strings. It is idempotent
(after a run nothing matches any more) and kept so that stock text pulled in later, for
example from a newer pokeemerald-expansion, can be put through the same rules.

    python3 tools/strata/terms.py [--write] FILE...

Without --write it prints a unified diff. The script only touches text inside string
literals, joins adjacent literals of one string (COMPOUND_STRING, consecutive .string lines)
so it can see the whole sentence, and then decides:

  * number: "a Pokemon" -> "an animal", "wild Pokemon" -> "wild animals", "the Pokemon was" ->
    "the animal was" (a bare noun is read as a plural, "the X" as singular unless a plural verb
    follows). Anything that does not read well is fixed by hand afterwards: read the diff.
  * case: ALL CAPS stays ALL CAPS, sentence starts are capitalised.
  * phrases: POKeMON CENTER -> FIELD STATION, POKe BALL -> CAPSULE, POKeDEX -> CODEX, ...

Always run the tests after: shared battle strings are asserted by MESSAGE() in test/battle.
"""
import difflib
import re
import sys

# --- vocabulary -------------------------------------------------------------------------------

ANIMAL = ("animal", "animals")

# Phrases first. (regex over the joined string, replacement, flags) - word gaps are \s or \n or \l.
GAP = r"(?:\s|\\[nl])+"


def phrase(words):
    return GAP.join(re.escape(w) for w in words.split(" "))


PHRASES = [
    # places
    ("POKéMON CENTER", "FIELD STATION"),
    ("Pokémon Center", "Field Station"),
    ("POKéMON MART", "CAMP STORE"),
    ("POKé MART", "CAMP STORE"),
    ("Poké Mart", "Camp Store"),
    # the codex
    ("POKéDEX", "CODEX"),
    ("Pokédex", "Codex"),
    # capsules (prose; item names are done by hand in items.h)
    ("PREMIER BALLS", "PREMIER CAPSULES"),
    ("PREMIER BALL", "PREMIER CAPSULE"),
    ("POKé BALLS", "CAPSULES"),
    ("POKé BALL", "CAPSULE"),
    ("Poké Balls", "capsules"),
    ("Poké Ball", "capsule"),
    ("POKé FLUTE", "BONE FLUTE"),
    ("Poké Flute", "Bone Flute"),
]

TOKEN = re.compile(r"POKéMON|Pokémon|POKeMON|Pokemon(?![A-Za-z_])|\{PKMN\}")

SING_DET = {"a", "an", "one", "each", "every", "single", "another", "this", "any", "neither", "either"}
# singular when directly in front of the noun ("that POKeMON"), but "that" can also be a relative
# pronoun two words back ("a glass flute that snaps Pokemon"), so these are not in SING_DET
SING_DEM = {"this", "that", "which", "what", "next", "last", "only", "first", "second", "third",
            "same", "chosen", "fainted"}
PLUR_PREV = {"all", "other", "both", "many", "some", "these", "those", "two", "three", "four",
             "more", "most", "few", "no", "several", "other's"}
DEF_DET = {"its", "the", "your", "my", "our", "their", "his", "her", "opposing", "party"}
PLUR_VERBS = {"are", "were", "have", "get", "can", "evolve", "do", "lose", "faint"}

QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*|\{[A-Za-z_0-9 ]+\}|[.!?:,;]")


def normalise(j):
    """Same-length copy of a joined literal with escapes turned into plain spaces/stops."""
    n = re.sub(r"\\[nl]", "  ", j)
    n = re.sub(r"\\p", ". ", n)
    return n.replace("$", " ")


def is_mixed_case(j):
    """True if the string has lower case letters outside {placeholders}: then it is prose."""
    return re.search(r"[a-z]", re.sub(r"\{[^}]*\}|\\[nlp]", "", j)) is not None


def decide(n, s, e):
    prev = [w.lower() for w in WORD.findall(n[:s])][-3:]
    nxt = [w.lower() for w in WORD.findall(n[e:e + 40])][:3]
    p1 = prev[-1] if prev else ""
    if re.match(r"'s", n[e:e + 2]) or n[e:e + 2] == "’s":
        return "P" if p1 in PLUR_PREV else "S"
    if p1.startswith("{") and p1.endswith("}"):
        return "S" if p1.startswith("{b_") and "team" not in p1 else "P"
    if p1 in SING_DET or p1 in SING_DEM:
        return "S"
    if p1 in PLUR_PREV:
        return "P"
    if len(prev) >= 2 and prev[-2] in SING_DET:
        return "S"
    # used as an adjective in front of a capitalised noun: ANIMAL INFO, animal Eggs
    if re.match(r" +[A-Z][A-Za-z]+", n[e:e + 30]) and not re.match(r" +(I|I'll|I'm)", n[e:e + 30]):
        return "S"
    if p1 in DEF_DET:
        return "P" if nxt and nxt[0] in PLUR_VERBS else "S"
    return "P"


def sentence_start(n, s):
    before = n[:s].rstrip(" “\"(")
    return before == "" or before[-1] in ".!?:…"


def group_literals(lines):
    """Yield groups of (line_index, start, end) for the contents of consecutive literals."""
    groups, cur = [], []
    last_line, last_tail_blank, last_content_end = None, True, ""
    for i, line in enumerate(lines):
        code = line
        if "//" in code:
            # only strip // comments that are outside quotes: cheap check
            head = code.split("//")[0]
            if head.count('"') % 2 == 0:
                code = head
        if '"' not in code or code.lstrip().startswith("#include"):
            continue
        for m in QUOTED.finditer(code):
            s, e = m.start(1), m.end(1)
            before = code[:m.start()].strip()
            joins = False
            if cur:
                li, ls, le = cur[-1]
                prev_line = lines[li]
                tail = prev_line[le + 1:].strip()
                if li == i:
                    joins = code[le + 1:m.start()].strip() == ""
                elif li == i - 1 or (li < i and all(not l.strip() for l in lines[li + 1:i])):
                    joins = tail == "" and (before == "" or before in (".string", ".ascii")) \
                        and not prev_line[ls:le].endswith("$")
            if not joins and cur:
                groups.append(cur)
                cur = []
            cur.append((i, s, e))
        # nothing: continue
    if cur:
        groups.append(cur)
    return groups


def convert_group(lines, group):
    pieces = [lines[i][s:e] for i, s, e in group]
    offs, total = [], 0
    for p in pieces:
        offs.append(total)
        total += len(p)
    j = "".join(pieces)
    n = normalise(j)
    mixed = is_mixed_case(j)
    edits = []  # (start, end, text)

    # phrases
    for old, new in PHRASES:
        for m in re.finditer(phrase(old), j):
            s, e = m.span()
            if any(a < e and s < b for a, b, _ in edits):
                continue  # already covered by a longer phrase
            t = new
            if old[0].islower() is False and new[0].islower() and sentence_start(n, s):
                t = new[0].upper() + new[1:]
            edits.append((s, e, t))

    # tokens
    for m in TOKEN.finditer(j):
        s, e = m.span()
        if any(a <= s < b for a, b, _ in edits):
            continue
        tok = m.group(0)
        upper = tok in ("POKéMON", "POKeMON", "{PKMN}") and not mixed
        number = decide(n, s, e)
        word = ANIMAL[1 if number == "P" else 0]
        if upper:
            word = word.upper()
        elif sentence_start(n, s):
            word = word[0].upper() + word[1:]
        if n[e:e + 2] in ("'s", "’s"):
            # possessive: animal's / animals' (the s of 's stays lower case in ALL CAPS text)
            word += "'" if number == "P" else "'s"
            e += 2
        # a/an before it
        am = re.search(r"(?<![A-Za-z])([Aa]n?)(\s+)$", n[:s])
        if number == "S" and am:
            art = am.group(1)
            if art in ("a", "A"):
                edits.append((am.start(1), am.end(1), art + "n"))
        edits.append((s, e, word))

    if not edits:
        return None
    edits.sort()
    # check that every edit stays within one piece
    cuts = offs + [total]
    out = list(pieces)
    for s, e, t in sorted(edits, reverse=True):
        k = max(x for x in range(len(pieces)) if offs[x] <= s or x == 0)
        if not (offs[k] <= s and e <= offs[k] + len(pieces[k])):
            sys.stderr.write("edit spans pieces, do by hand: %r\n" % j[s:e])
            continue
        ls, le = s - offs[k], e - offs[k]
        if t is not None:
            out[k] = out[k][:ls] + t + out[k][le:]
    return pieces, out


SENTENCES = False


def process(path):
    src = open(path, encoding="utf-8").read()
    lines = src.split("\n")
    groups = group_literals(lines)
    # apply from the bottom up so earlier offsets stay valid: collect replacements per line
    repl = {}
    for g in groups:
        r = convert_group(lines, g)
        if not r:
            continue
        pieces, out = r
        for (i, s, e), old, new in zip(g, pieces, out):
            if old != new:
                repl.setdefault(i, []).append((s, e, new))
        if SENTENCES:
            old_s = "".join(pieces).replace(chr(92) + "n", "/")
            new_s = "".join(out).replace(chr(92) + "n", "/")
            print("%s:%d: %s" % (path, g[0][0] + 1, old_s))
            print("    -> %s" % new_s)
    for i, items in repl.items():
        line = lines[i]
        for s, e, new in sorted(items, reverse=True):
            line = line[:s] + new + line[e:]
        lines[i] = line
    return src, "\n".join(lines)


def main(argv):
    global SENTENCES
    SENTENCES = "--sentences" in argv
    write = "--write" in argv
    files = [a for a in argv if not a.startswith("--")]
    for path in files:
        old, new = process(path)
        if old == new or SENTENCES:
            continue
        if write:
            open(path, "w", encoding="utf-8", newline="").write(new)
            print("changed", path)
        else:
            sys.stdout.writelines(difflib.unified_diff(
                old.splitlines(True), new.splitlines(True), path, path, n=0))


if __name__ == "__main__":
    main(sys.argv[1:])
