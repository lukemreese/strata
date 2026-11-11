"""Triage of playtest screenshots by a local vision model.

A scenario run (tools/strata/playtest) leaves dozens of 240x160 PNGs. Reading each one
with a strong model is the expensive part of a playtest. This sorts them: the model
describes each screen and flags the faults a still image can show, so only the flagged
ones need a careful look. Crashes, freezes and wrong state are the harness's job
(result.json), not this tool's.
"""

import glob
import os

from .client import read_bytes, run_batch

FAULTS = ["text_cut_off", "text_outside_box", "garbled_graphics", "wrong_colours",
          "placeholder_or_debug", "sprite_missing"]

SCHEMA = {
    "type": "object",
    "properties": {
        "screen": {"type": "string", "description": "one sentence: what this screen shows"},
        "text": {"type": "string", "description": "the text on screen, exactly as shown, or empty"},
        "faults": {"type": "array", "items": {"type": "string", "enum": FAULTS}},
        "note": {"type": "string", "description": "where the fault is, or empty"},
    },
    "required": ["screen", "text", "faults", "note"],
}

PROMPT = (
    "This is a 240x160 screenshot from a Game Boy Advance role-playing game (pixel art, a top-down "
    "map or a battle or a menu; text appears in bordered boxes).\n"
    "Describe the screen in one sentence, copy any text exactly, and list only the faults you can "
    "actually see:\n"
    "- text_cut_off: a word or line ends mid-way at the edge of its box\n"
    "- text_outside_box: letters drawn over the box border or outside it\n"
    "- garbled_graphics: blocks of random or scrambled tiles, torn sprites\n"
    "- wrong_colours: an object in clearly wrong colours (a magenta or rainbow patch)\n"
    "- placeholder_or_debug: debug text, '???', a question-mark sprite, an error screen\n"
    "- sprite_missing: an empty space where a character or creature should clearly be\n"
    "A dark, grey or plain scene is normal. If nothing is wrong, faults is an empty list.")


def find(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(os.path.join(p, "**", "*.png"), recursive=True)) if os.path.isdir(p) else [p]
    return files


def review(client, files, quiet=False):
    def one(path):
        return client.ask_json(PROMPT, SCHEMA, images=[read_bytes(path)], max_tokens=500)

    results = run_batch(files, one, label=os.path.basename, quiet=quiet)
    return [dict(r, file=f) for f, r in zip(files, results)]


def report(rows, model, base):
    flagged = [r for r in rows if r.get("faults") or "error" in r]
    lines = ["# Screenshot triage", "",
             f"Model: `{model}`. {len(rows)} screenshots, **{len(flagged)} to look at**. A flag is a "
             "reason to open the image, not a confirmed bug; an unflagged image was not proven clean.", ""]
    if flagged:
        lines += ["| File | Faults | Note | Screen |", "|---|---|---|---|"]
        lines += [f"| `{os.path.relpath(r['file'], base)}` | {', '.join(r.get('faults', [])) or 'error'} | "
                  f"{r.get('note') or r.get('error', '')} | {r.get('screen', '')} |" for r in flagged]
    lines += ["", "## All screens", ""]
    lines += [f"- `{os.path.relpath(r['file'], base)}`: {r.get('screen', r.get('error', ''))}"
              + (f" Text: \"{r['text']}\"" if r.get("text") else "") for r in rows]
    return "\n".join(lines) + "\n"
