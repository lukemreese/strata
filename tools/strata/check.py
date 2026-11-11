#!/usr/bin/env python3
"""Every Strata check that needs no ROM build, in one command. CI runs it; run it before a commit.

    python3 tools/strata/check.py            all checks (about 2 minutes)
    python3 tools/strata/check.py --fast     skip `drift` (about 10 seconds)
    python3 tools/strata/check.py maps art   only the named checks

Checks:
    tests   unit tests of the Python tooling (tools/strata/tests)
    art     every species has its own sprite and cry (gen_sprite.py --strict)
    maps    every trigger, sign, forage spot and map edge is reachable (mapcheck.py)
    drift   rerun every generator; the working tree must not change. A change means a
            source (roster, sprite spec, cry spec, map module) was edited and its
            output was not regenerated and committed. Fix: commit what it wrote.

Exit code 0 only if every check passed. `drift` rewrites generated files: never run it
while `make` or `make check` is running in the same worktree.

This does not replace the ROM checks: `make -j8` and `make check -j8` (strata-build-test skill).
"""

import hashlib
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PY = sys.executable

# The generator order matters: sprites and cries before species (strata-build-test skill).
GENERATORS = [
    ["tools/strata/gen_sprite.py", "--all"],
    ["tools/strata/gen_cry.py"],
    ["tools/strata/gen_species.py"],
    ["tools/strata/gen_tilesets.py"],
    ["tools/strata/gen_maps.py"],
]


def run(cmd, quiet=True):
    """Runs a tool from the repo root. Returns (ok, last lines of output)."""
    p = subprocess.run([PY] + cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    tail = "\n".join(p.stdout.strip().splitlines()[-12:])
    return p.returncode == 0, tail


def tree_state():
    """(fingerprint, status lines) of the working tree against HEAD."""
    def git(*args):
        return subprocess.run(["git"] + list(args), cwd=ROOT, stdout=subprocess.PIPE, check=True).stdout
    status = git("status", "--porcelain").decode().splitlines()
    return hashlib.sha256(git("diff", "HEAD") + "\n".join(status).encode()).hexdigest(), status


def check_tests():
    return run(["-m", "unittest", "discover", "-s", "tools/strata/tests"])


def check_art():
    return run(["tools/strata/gen_sprite.py", "--strict"])


def check_maps():
    ok, tail = run(["tools/strata/mapcheck.py"])
    return ok, tail if not ok else ""


def check_drift():
    before, status_before = tree_state()
    for cmd in GENERATORS:
        ok, tail = run(cmd)
        if not ok:
            return False, f"{' '.join(cmd)} failed:\n{tail}"
    after, status_after = tree_state()
    if after == before:
        return True, ""
    changed = [s for s in status_after if s not in status_before] or status_after
    return False, ("the generators changed these files (sources were edited without regenerating):\n"
                   + "\n".join(changed[:40])
                   + "\nfix: review `git diff --stat`, then commit the regenerated files")


CHECKS = {"tests": check_tests, "art": check_art, "maps": check_maps, "drift": check_drift}


def main(argv):
    fast = "--fast" in argv
    names = [a for a in argv if not a.startswith("--")]
    unknown = [n for n in names if n not in CHECKS] + [a for a in argv if a.startswith("--") and a != "--fast"]
    if unknown:
        sys.exit(f"check: unknown {unknown[0]} (checks: {', '.join(CHECKS)}; option: --fast)")
    names = names or [n for n in CHECKS if not (fast and n == "drift")]
    failed = []
    for name in names:
        t = time.time()
        ok, detail = CHECKS[name]()
        print(f"{'PASS' if ok else 'FAIL'}  {name:<6} {time.time() - t:5.1f} s", flush=True)
        if not ok:
            failed.append(name)
            print("    " + detail.replace("\n", "\n    "), flush=True)
    print("check:", "all passed" if not failed else f"FAILED: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
