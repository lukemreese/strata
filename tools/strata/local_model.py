#!/usr/bin/env python3
"""Batch review with a local model (the desktop GPU). Thin CLI over tools/strata/localmodel/.

Usage (from the repo root; the server must be OpenAI-compatible):
    python3 tools/strata/local_model.py doctor
        Is the server up, which models does it serve, can the chosen ones return JSON
        and read an image? Run this first.
    python3 tools/strata/local_model.py sprites [species ...] [--plan NAME]
        Blind identification of creature sprites: "what animal is this?" graded per body plan.
    python3 tools/strata/local_model.py claims [--source codex|maps|all] [--no-model] [--only TEXT]
        Fact-check worklist from Codex entries and field notes. --no-model runs only the
        mechanical pass (absolute wording with no hedge) and needs no server.
    python3 tools/strata/local_model.py shots DIR_OR_PNG [...]
        Triage playtest screenshots (cut-off text, garbled graphics).
    python3 tools/strata/local_model.py ask "question" [--image PNG] [--file PATH] [--max-tokens N]
        One free-form question. For delegating a cheap read; the answer is not evidence.

Common options: --out DIR (default build/local_model), --quiet.
Environment: STRATA_LLM_URL, STRATA_LLM_MODEL, STRATA_VLM_MODEL, STRATA_LLM_KEY,
STRATA_LLM_CACHE (see tools/strata/localmodel/client.py). Answers are cached on disk by
request, so a rerun after changing three sprites asks three questions.

Reports are a reading order for a person or a stronger model. Nothing here edits the game.
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from localmodel.client import Client, LocalModelError, ROOT, read_bytes  # noqa: E402


def write(out, name, text):
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def finish(client, *paths):
    print(f"{client.calls} model calls, {client.cache_hits} cached, "
          f"{client.usage['completion_tokens']} tokens out")
    for p in paths:
        print("wrote", os.path.relpath(p))


def probe_image():
    """96x96 PNG, left half red, right half blue."""
    from maprender import write_png
    path = os.path.join(ROOT, ".cache", "strata-local", "probe.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_png(path, 96, 96, [[(220, 30, 30)] * 48 + [(30, 30, 220)] * 48 for _ in range(96)])
    return read_bytes(path)


def cmd_doctor(client, args):
    client.cache_dir = None
    print("server:", client.url)
    served = client.models()
    print("serves:", ", ".join(served) or "(nothing)")
    ok = True
    for vision in (False, True):
        name = client.model(vision)
        what = "image" if vision else "text "
        if name not in served:
            print(f"FAIL {what} model {name!r} is not served")
            ok = False
            continue
        schema = {"type": "object", "required": ["left", "right"],
                  "properties": {"left": {"type": "string"}, "right": {"type": "string"}}}
        try:
            t = time.time()
            if vision:
                a = client.ask_json("What colour is the left half of this image, and the right half? "
                                    "One word each.", schema, images=[probe_image()], max_tokens=200)
                good = "red" in a["left"].lower() and "blue" in a["right"].lower()
            else:
                a = client.ask_json("In the word pair (red, blue), which word is on the left and which is "
                                    "on the right?", schema, max_tokens=200)
                good = a["left"].lower().strip() == "red" and a["right"].lower().strip() == "blue"
            print(f"{'ok  ' if good else 'FAIL'} {what} {name}: {json.dumps(a)} "
                  f"({time.time() - t:.1f} s, format {client.formats[0] or 'plain'})")
            ok &= good
        except LocalModelError as e:
            print(f"FAIL {what} {name}: {e}")
            ok = False
    if not ok:
        print("fix: see .claude/skills/strata-local-model/SKILL.md (Setup)")
    return 0 if ok else 1


def cmd_sprites(client, args):
    from localmodel import sprites
    import sprites as art
    folders = list(args.species)
    if args.plan:
        if args.plan not in art.TAXONOMY:
            sys.exit(f"no body plan {args.plan} (have: {', '.join(art.TAXONOMY)})")
        folders += art.TAXONOMY[args.plan][1]
    rows = sprites.review(client, args.out, folders or None, args.quiet)
    model = client.model(vision=True)
    finish(client, write(args.out, "sprites.md", sprites.report(rows, model)),
           write(args.out, "sprites.json", json.dumps({"model": model, "rows": rows}, indent=1)))
    count = {g: sum(r["grade"] == g for r in rows) for g in ("top1", "top3", "miss", "error")}
    print(" ".join(f"{g}={n}" for g, n in count.items()))
    return 0


def cmd_claims(client, args):
    from localmodel import claims
    items = [t for t in claims.texts(args.source) if not args.only or args.only.lower() in t[0].lower()]
    extracted = None if args.no_model else claims.extract(client, items, args.quiet)
    model = None if args.no_model else client.model()
    paths = [write(args.out, "claims.md", claims.report(items, extracted, model))]
    if extracted is not None:
        paths.append(write(args.out, "claims.json", json.dumps({"model": model, "texts": extracted}, indent=1)))
    finish(client, *paths)
    return 0


def cmd_shots(client, args):
    from localmodel import shots
    files = shots.find(args.paths)
    if not files:
        sys.exit("no PNGs found")
    rows = shots.review(client, files, args.quiet)
    model = client.model(vision=True)
    base = os.path.commonpath([os.path.abspath(f) for f in files] + [os.path.abspath(args.paths[0])])
    base = base if os.path.isdir(base) else os.path.dirname(base)
    rows = [dict(r, file=os.path.abspath(r["file"])) for r in rows]
    finish(client, write(args.out, "shots.md", shots.report(rows, model, base)),
           write(args.out, "shots.json", json.dumps({"model": model, "rows": rows}, indent=1)))
    print(f"{sum(bool(r.get('faults')) for r in rows)} of {len(rows)} flagged")
    return 0


def cmd_ask(client, args):
    prompt = args.question
    for path in args.file or []:
        prompt += f"\n\n--- {path} ---\n" + open(path, encoding="utf-8", errors="replace").read()
    images = [read_bytes(p) for p in args.image or []]
    print(client.chat(prompt, images=images, max_tokens=args.max_tokens))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.join(ROOT, "build", "local_model"))
    ap.add_argument("--quiet", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    p = sub.add_parser("sprites")
    p.add_argument("species", nargs="*")
    p.add_argument("--plan")
    p = sub.add_parser("claims")
    p.add_argument("--source", choices=["codex", "maps", "all"], default="codex")
    p.add_argument("--no-model", action="store_true")
    p.add_argument("--only", help="only sources whose id contains this text")
    p = sub.add_parser("shots")
    p.add_argument("paths", nargs="+")
    p = sub.add_parser("ask")
    p.add_argument("question")
    p.add_argument("--image", action="append")
    p.add_argument("--file", action="append")
    p.add_argument("--max-tokens", type=int, default=1024)
    args = ap.parse_args()
    client = Client()
    try:
        return globals()["cmd_" + args.cmd](client, args)
    except LocalModelError as e:
        sys.exit(f"local_model: {e}")


if __name__ == "__main__":
    sys.exit(main())
