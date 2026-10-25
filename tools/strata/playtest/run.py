#!/usr/bin/env python3
"""Run Strata playtest scenarios headless and unthrottled.

    python3 tools/strata/playtest/run.py new_game_smoke battle_smoke boss_3
    python3 tools/strata/playtest/run.py act_tour --act 5
    python3 tools/strata/playtest/run.py my_test.txt          # a line-DSL file
    python3 tools/strata/playtest/run.py --list

Needs the playtest ROM (`make playtest` -> pokeemerald-playtest.gba/.elf) and the
runner (tools/strata/playtest/runner/build_runner.sh). Each scenario writes
<out>/<scenario>/ with numbered PNGs, log.txt and result.json, and <out>/summary.json
lists them all. Default out: /mnt/c/Projects/pokemon-custom/build/harness
(Windows: C:\\Projects\\pokemon-custom\\build\\harness).
"""

import argparse
import glob
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness  # noqa: E402
import scenarios  # noqa: E402

DEFAULT_OUT = "/mnt/c/Projects/pokemon-custom/build/harness"


def run_one(name, args):
    out = os.path.join(args.out, os.path.splitext(os.path.basename(name))[0])
    if os.path.isdir(out):
        for f in glob.glob(os.path.join(out, "*")):
            if f.endswith((".png", ".txt", ".json", ".ss")):
                os.remove(f)
    g = harness.Game(args.rom, args.elf, out, name=name, quiet=args.quiet)
    status, error = "pass", None
    try:
        if name.endswith(".txt"):
            g.boot()
            harness.run_dsl(g, open(name).read())
        else:
            scenarios.get(name)(g, args)
    except harness.GameCrash as e:
        status, error = "crash", str(e)
    except harness.TestFailure as e:
        status, error = "fail", str(e)
        try:
            g.screenshot("failure")
        except Exception:
            pass
    except Exception as e:  # a bug in the scenario or harness
        status, error = "error", f"{type(e).__name__}: {e}"
        g.log(traceback.format_exc())
        try:
            g.screenshot("failure")
        except Exception:
            pass
    res = g.close(status, error)
    res["out"] = out
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenarios", nargs="*")
    ap.add_argument("--rom", default=os.path.join(harness.ROOT, "pokeemerald-playtest.gba"))
    ap.add_argument("--elf", default=None)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--act", type=int, action="append", help="act_tour: only these acts (repeatable)")
    ap.add_argument("--map", action="append", help="act_tour: only these maps (e.g. StrataLevee)")
    ap.add_argument("--quiet", action="store_true", help="only print the summary")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or not args.scenarios:
        for n, f in scenarios.REGISTRY.items():
            print(f"{n:18s} {(f.__doc__ or '').strip().splitlines()[0]}")
        return 0
    args.elf = args.elf or os.path.splitext(args.rom)[0] + ".elf"
    if not os.path.exists(harness.RUNNER):
        sys.exit("runner missing: bash tools/strata/playtest/runner/build_runner.sh")
    if not os.path.exists(args.rom):
        sys.exit(f"{args.rom} missing: make -j8 playtest")
    os.makedirs(args.out, exist_ok=True)
    names = []
    for n in args.scenarios:
        names += scenarios.expand(n)
    results = []
    t0 = time.time()
    for n in names:
        r = run_one(n, args)
        results.append(r)
        print(f"{r['status'].upper():5s} {n:18s} {r['seconds']:7.1f} s {r['frames']:8d} frames "
              f"{len(r['screenshots']):3d} shots  {r['out']}" + (f"  -- {r['error']}" if r["error"] else ""),
              flush=True)
    summary = dict(seconds=round(time.time() - t0, 1), results=[
        {k: r[k] for k in ("scenario", "status", "error", "seconds", "frames", "out")} for r in results])
    json.dump(summary, open(os.path.join(args.out, "summary.json"), "w"), indent=1)
    bad = [r for r in results if r["status"] != "pass"]
    print(f"{len(results) - len(bad)}/{len(results)} passed in {summary['seconds']} s")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
