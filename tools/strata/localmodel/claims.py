"""A fact-check worklist from the game's science text.

Two passes over the Codex entries (tools/strata/roster) and the field notes and
dialogue (data/maps/Strata*/scripts.inc):

1. Mechanical, no model: superlatives and proof words ("the first", "largest") in a sentence
   with no hedge. These are the claims a specialist disputes first (outline section 5).
2. Model: split each text into single checkable claims with a kind, whether the text
   hedges it, and how likely a specialist would dispute it.

The output is a reading order for the fact-check, nothing more. A local model does not
know the literature: "risk" is its guess at what to check first, and a claim it ranks
low is not thereby confirmed. Verification needs a primary source (PBDB, the paper).
"""

import glob
import os
import re

from roster import SPECIES

from .client import ROOT, run_batch

# Superlatives and proof words. Plain quantifiers ("every", "always") are left out: in
# dialogue they are almost never a claim about the record.
ABSOLUTE = re.compile(
    r"\b(the (first|oldest|earliest|largest|biggest|smallest|fastest|only|youngest|heaviest|tallest|best)"
    r"|the last (of|known|surviving)|no other|proves?|proved|certainly|definitely|undoubtedly)\b", re.I)
HEDGE = re.compile(
    r"\b(may|might|could|probably|perhaps|possibly|likely|suggests?|appears?|seems?|thought to|"
    r"among the|one of the|about|around|roughly|approximately|estimated?|debated|uncertain|inferred|"
    r"known|so far|yet found|on record|hypothes[ie]s|interpret\w*|stand-in|model)\b", re.I)

SCHEMA = {
    "type": "object",
    "properties": {"claims": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "claim": {"type": "string", "description": "one checkable statement, in the text's own words"},
            "kind": {"type": "string", "enum": ["age", "locality", "size", "anatomy", "behaviour", "ecology",
                                                "taxonomy", "event", "law", "other"]},
            "hedged": {"type": "boolean"},
            "risk": {"type": "string", "enum": ["low", "medium", "high"]},
        },
        "required": ["claim", "kind", "hedged", "risk"]}}},
    "required": ["claims"],
}

PROMPT = (
    "Below is text from a science-grounded game about real fossil animals of the North American "
    "West. Split it into its separate checkable factual claims: statements a paleontologist could "
    "confirm or refute from the literature (ages, places, sizes, anatomy, behaviour, ecology, "
    "relationships, events, law). Skip game instructions, greetings and opinions.\n"
    "For each claim give:\n"
    "- claim: the statement, in the text's own words, with the animal's name filled in\n"
    "- kind: one of the listed kinds\n"
    "- hedged: true if the text itself marks it as uncertain (may, probably, suggests, about)\n"
    "- risk: high if specialists commonly dispute this kind of statement or it is a superlative, "
    "an exact number, or a behaviour inferred from bones; low if it is textbook-level\n"
    "Do not correct the text and do not add facts of your own.\n\nTEXT ({source}):\n{text}")


# --- Sources -------------------------------------------------------------------------

def codex_texts():
    """(source id, text) for every roster species."""
    for sp in SPECIES:
        facts = f"{sp['genus']}. Site: {sp['site']}. Age: {sp['age']}. Mass: {sp['mass']} kg" + (
            " (our estimate)" if sp.get("mass_est") else "") + f". Length: {sp['length']} m."
        text = " ".join(filter(None, [facts, sp.get("dex"), sp.get("notes")]))
        yield f"codex:{sp['name']}", text


_STRING = re.compile(r'^\s*\.string\s+"(.*)"\s*$')
_LABEL = re.compile(r"^(\w+):+\s*$")
_CONTROL = re.compile(r"\\[nlp]|\$|\{[A-Z_0-9 ]+\}")


def map_texts(pattern="data/maps/Strata*/scripts.inc"):
    """(source id, text) for every text label in the Strata map scripts."""
    for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
        label, parts = None, []
        for line in open(path, encoding="utf-8"):
            m = _STRING.match(line)
            if m and label:
                parts.append(m.group(1))
                continue
            if parts:
                yield f"map:{label}", clean(" ".join(parts))
                parts = []
            m = _LABEL.match(line)
            if m:
                label = m.group(1)
        if parts:
            yield f"map:{label}", clean(" ".join(parts))


def clean(text):
    return re.sub(r"\s+", " ", _CONTROL.sub(" ", text)).strip()


def texts(which):
    out = []
    if which in ("codex", "all"):
        out += list(codex_texts())
    if which in ("maps", "all"):
        out += [t for t in map_texts() if len(t[1].split()) >= 6]
    return out


# --- Pass 1: mechanical --------------------------------------------------------------

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def absolutes(text):
    """Sentences with an absolute word and no hedge: [(sentence, word)]."""
    found = []
    for s in sentences(text):
        m = ABSOLUTE.search(s)
        if m and not HEDGE.search(s):
            found.append((s, m.group(0)))
    return found


# --- Pass 2: model -------------------------------------------------------------------

def extract(client, items, quiet=False):
    def one(item):
        source, text = item
        answer = client.ask_json(PROMPT.format(source=source, text=text), SCHEMA, max_tokens=1500)
        return {"claims": answer["claims"]}

    results = run_batch(items, one, label=lambda item: item[0], quiet=quiet)
    return [dict(r, source=source, text=text) for (source, text), r in zip(items, results)]


def report(items, extracted, model):
    lines = ["# Fact-check worklist", "",
             "A reading order, not a verdict. Verify each line against a primary source before "
             "changing game text; record the outcome in `docs/strata_outline.md` section 5.", "",
             "## Absolute wording with no hedge (mechanical)", ""]
    flagged = [(source, s, w) for source, text in items for s, w in absolutes(text)]
    lines += [f"- `{source}`: \"{s}\" (**{w}**)" for source, s, w in flagged] or ["None."]
    if extracted is not None:
        rank = {"high": 0, "medium": 1, "low": 2}
        claims = [dict(c, source=e["source"]) for e in extracted for c in e.get("claims", [])]
        claims.sort(key=lambda c: (c["hedged"], rank[c["risk"]]))
        errors = [e for e in extracted if "error" in e]
        lines += ["", f"## Claims by review order (model `{model}`)", "",
                  f"{len(claims)} claims from {len(extracted)} texts. Unhedged before hedged, then the "
                  "model's guess at risk.", "",
                  "| Risk | Hedged | Kind | Claim | Source |", "|---|---|---|---|---|"]
        lines += [f"| {c['risk']} | {'yes' if c['hedged'] else 'NO'} | {c['kind']} | "
                  f"{c['claim'].replace('|', '/')} | `{c['source']}` |" for c in claims]
        if errors:
            lines += ["", "## Texts the model failed on", ""] + [f"- `{e['source']}`: {e['error']}" for e in errors]
    return "\n".join(lines) + "\n"
