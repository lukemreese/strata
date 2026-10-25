"""Scripted Strata playtests: a headless mGBA core driven frame by frame.

The runner (runner/strata-runner, mGBA 0.10.5's GBA core) runs unthrottled and
answers one command per line. This module wraps it in `Game`, a small DSL:

    g.quickstart("MAP_STRATA_LEVEE", 10, 20, story=2, era=1, party=[("SPECIES_X", 12)])
    g.walk("up", 3)
    g.press("A"); g.talk()
    g.screenshot("levee_north")
    g.expect_map("MAP_STRATA_LEVEE"); g.expect_var("VAR_STRATA_STORY", 2)

Game state comes from symbols in the playtest ELF (`make playtest`): the game
mirrors its state into gStrataPlaytestStatus every frame and takes commands
from gStrataPlaytestCommand (src/strata_playtest.c). Every run gets a folder
with numbered PNGs, log.txt and result.json. See .claude/skills/strata-autotest.
"""

import json
import os
import re
import struct
import subprocess
import sys
import time
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RUNNER = os.path.join(HERE, "runner", "strata-runner")

KEYS = {"A": 1, "B": 2, "SELECT": 4, "START": 8, "RIGHT": 16, "LEFT": 32, "UP": 64, "DOWN": 128,
        "R": 256, "L": 512}
DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
DIR_KEYS = {"up": "UP", "down": "DOWN", "left": "LEFT", "right": "RIGHT"}

# struct StrataPlaytestStatus (include/strata_playtest.h)
STATUS_FMT = "<IIIIHHHHhhHHBBBBIBBBB" + "HBBHH" * 6 + "BBBBBBBBBBHI"
STATUS_SIZE = struct.calcsize(STATUS_FMT)
STATUS_FIELDS = ["magic", "frames", "callback1", "callback2", "doneSeq", "result", "mapGroup", "mapNum",
                 "x", "y", "story", "era", "facing", "moving", "inBattle", "battleOutcome",
                 "battleTypeFlags", "scriptActive", "fieldLocked", "fadeActive", "partyCount"]
LAYOUT_FIELDS = ["printerNext", "printerState", "printerActiveByte", "printerActiveMask",
                 "printerWindowId", "sizeofTask", "renderStateWait", "renderStateWaitSE",
                 "scriptNative", "scriptMode", "padding"]
MAGIC = 0x54505453

CMD = {"QUICKSTART": 1, "SET_VAR": 2, "SET_FLAG": 3, "WARP": 4, "RUN_SCRIPT": 5, "GIVE_MON": 6,
       "GIVE_ITEM": 7, "HEAL": 8, "READ_PARTY": 9, "GET_VAR": 10, "GET_FLAG": 11, "COUNT_ITEM": 12}
OPT = {"no_encounters": 1, "no_collision": 2, "instant_text": 4, "no_battle_anim": 8, "female": 16}
PT_MAX_ITEMS, PT_MAX_VARS, PT_MAX_FLAGS = 16, 24, 48

# Lines in mGBA's log that every boot produces (register clears, flash probes).
BOOT_NOISE = re.compile(r"Write to read-only I/O register|Invalid DMA source address: 0x00000000|"
                        r"Invalid video register|Bad flash write|Bad BIOS Load")


class TestFailure(Exception):
    pass


class GameCrash(TestFailure):
    pass


class Symbols:
    """Name <-> address from `arm-none-eabi-nm` on the playtest ELF."""

    def __init__(self, elf):
        out = subprocess.run(["arm-none-eabi-nm", "-S", "--defined-only", elf], check=True,
                             capture_output=True, text=True).stdout
        self.addr, self.size, funcs = {}, {}, []
        for line in out.splitlines():
            parts = line.split()
            if len(parts) == 4:
                a, size, kind, name = parts
            elif len(parts) == 3:
                a, kind, name = parts
                size = "0"
            else:
                continue
            a = int(a, 16)
            if name not in self.addr or kind.isupper():
                self.addr[name] = a
                self.size[name] = int(size, 16)
            if kind in "tT" and 0x08000000 <= a < 0x0A000000:
                funcs.append((a & ~1, name))
        funcs.sort()
        self._funcs = funcs
        self._func_by_addr = {a: n for a, n in funcs}

    def __getitem__(self, name):
        return self.addr[name]

    def func_name(self, address):
        """Exact function name for a code pointer (e.g. a callback), else hex."""
        if address == 0:
            return "NULL"
        return self._func_by_addr.get(address & ~1, f"0x{address:08X}")

    def nearest(self, address):
        """Function containing a PC value, as name+offset."""
        import bisect
        a = address & ~1
        i = bisect.bisect_right(self._funcs, (a, "￿")) - 1
        if i < 0 or not 0x08000000 <= a < 0x0A000000:
            return f"0x{address:08X}"
        base, name = self._funcs[i]
        return f"{name}+0x{a - base:X}"


class Constants:
    """Values of C constants (MAP_*, SPECIES_*, ITEM_*, FLAG_*, VAR_*, enums) via the
    ARM compiler, cached per ELF so enums and expressions are always right."""

    HEADERS = ["global.h", "constants/map_groups.h", "constants/species.h", "constants/items.h",
               "constants/flags.h", "constants/vars.h", "constants/strata.h", "constants/event_objects.h",
               "constants/battle.h"]

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.values = {}
        if os.path.exists(cache_path):
            try:
                self.values = json.load(open(cache_path))
            except ValueError:
                self.values = {}

    def resolve(self, names):
        missing = [n for n in names if isinstance(n, str) and n not in self.values]
        if missing:
            src = "".join(f'#include "{h}"\n' for h in self.HEADERS)
            src += "const int sPlaytestProbe[] = {\n" + "".join(f"  (int)({n}),\n" for n in missing) + "};\n"
            cmd = ["arm-none-eabi-gcc", "-S", "-o", "-", "-x", "c", "-", "-iquote", "include",
                   "-DMODERN=1", "-DTESTING=0", "-DEMERALD", "-std=gnu17", "-mthumb", "-O1",
                   "-w", "-mabi=apcs-gnu"]
            res = subprocess.run(cmd, input=src, capture_output=True, text=True, cwd=ROOT)
            if res.returncode != 0:
                bad = [l for l in res.stderr.splitlines() if "error" in l][:5]
                raise TestFailure("unknown constant(s) " + ", ".join(missing) + ": " + " | ".join(bad))
            words = [int(m) for m in re.findall(r"\.word\s+(-?\d+)", res.stdout)]
            words += [0] * (len(missing) - len(words))  # all-zero arrays go to .bss/.space
            if ".space" in res.stdout and not words[:1]:
                words = [0] * len(missing)
            for n, v in zip(missing, words):
                self.values[n] = v
            try:
                json.dump(self.values, open(self.cache_path, "w"), indent=0, sort_keys=True)
            except OSError:
                pass
        return [self.values[n] if isinstance(n, str) else n for n in names]

    def __call__(self, name):
        if isinstance(name, int):
            return name
        if re.fullmatch(r"-?(0x[0-9a-fA-F]+|\d+)", name):
            return int(name, 0)
        return self.resolve([name])[0]


_CHARMAP = None


def decode_text(raw):
    """Game text (charmap.txt encoding) to a str: FE newline, FA/FB prompts, FF end."""
    global _CHARMAP
    if _CHARMAP is None:
        _CHARMAP = {}
        for line in open(os.path.join(ROOT, "charmap.txt"), encoding="utf-8"):
            m = re.match(r"'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
            if m and int(m.group(2), 16) not in _CHARMAP:
                _CHARMAP[int(m.group(2), 16)] = m.group(1)
    out, i = [], 0
    while i < len(raw):
        b = raw[i]
        if b == 0xFF:
            break
        if b == 0xFE:
            out.append("\n")
        elif b in (0xFA, 0xFB):
            out.append(" ")
        elif b == 0xFD:
            out.append("{}")
            i += 1
        elif b == 0xFC:
            i += 2  # control code and (usually) one argument
            continue
        else:
            out.append(_CHARMAP.get(b, "?"))
        i += 1
    return "".join(out)


class Runner:
    def __init__(self, rom, rtc=None, sav=None):
        args = [RUNNER, rom]
        if rtc is not None:
            args += ["--rtc", str(int(rtc))]
        if sav:
            args += ["--sav", sav]
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def cmd(self, line):
        self.p.stdin.write(line + "\n")
        self.p.stdin.flush()
        reply = self.p.stdout.readline()
        if not reply:
            raise GameCrash(f"runner exited during '{line}'")
        reply = reply.rstrip("\n")
        if reply.startswith("err"):
            raise TestFailure(f"runner: {reply} ({line})")
        return reply[3:]

    def close(self):
        try:
            self.cmd("quit")
        except Exception:
            pass
        self.p.wait(timeout=5)


class Game:
    def __init__(self, rom, elf, out_dir, name="run", rtc=12 * 3600 + 1_700_000_000 // 86400 * 86400,
                 freeze_frames=600, sav=None, quiet=False, max_frames=1_500_000):
        self.rom, self.elf, self.out, self.name = rom, elf, out_dir, name
        os.makedirs(out_dir, exist_ok=True)
        self.sym = Symbols(elf)
        self.const = Constants(os.path.splitext(elf)[0] + ".playtest_constants.json")
        if self.sym.size.get("gStrataPlaytestStatus", STATUS_SIZE) != STATUS_SIZE:
            raise TestFailure(f"gStrataPlaytestStatus is {self.sym.size['gStrataPlaytestStatus']} bytes, "
                              f"harness expects {STATUS_SIZE}: update STATUS_FMT")
        self.status_addr = self.sym["gStrataPlaytestStatus"]
        self.cmd_addr = self.sym["gStrataPlaytestCommand"]
        self.runner = Runner(rom, rtc=rtc, sav=sav)
        self.quiet = quiet
        self.freeze_frames = freeze_frames
        self.max_frames = max_frames  # a hard budget so a scenario bug can't spin forever
        self.shots, self.events, self.checks, self.errors = [], [], [], []
        self.keys = 0
        self.frame = 0
        self.st = {}
        self.layout = None
        self.seq = 0
        self.resets_seen = 0
        self.last_game_frames = 0
        self.stalled = 0
        self.screen_frames = 600
        self._same_screen = 0
        self._last_hash = None
        self.warnings = []
        self.t0 = time.time()
        self.logf = open(os.path.join(out_dir, "log.txt"), "w")
        self.log(f"rom {rom}")
        self._refresh(self.runner.cmd(f"step 0 0 {self.status_addr:x} {STATUS_SIZE}"))

    # ---------------------------------------------------------------- logging
    def log(self, msg):
        line = f"[{self.frame:7d}] {msg}"
        self.logf.write(line + "\n")
        self.logf.flush()
        self.events.append(line)
        if not self.quiet:
            print(line, flush=True)

    # ------------------------------------------------------------ frame core
    def _refresh(self, reply):
        parts = reply.split()
        self.frame = int(parts[0])
        if len(parts) > 1:
            raw = bytes.fromhex(parts[1])
            vals = struct.unpack(STATUS_FMT, raw)
            st = dict(zip(STATUS_FIELDS, vals[:len(STATUS_FIELDS)]))
            pv = vals[len(STATUS_FIELDS):len(STATUS_FIELDS) + 30]
            st["party"] = [dict(species=pv[i * 5], level=pv[i * 5 + 1], isEgg=pv[i * 5 + 2], hp=pv[i * 5 + 3],
                                maxHP=pv[i * 5 + 4]) for i in range(6)]
            st["value"] = vals[-1]
            if st["magic"] == MAGIC and self.layout is None:
                self.layout = dict(zip(LAYOUT_FIELDS, vals[-12:-1]))
            self.st = st

    def step(self, frames=1, keys=None):
        """Run `frames` frames holding `keys` (default: the keys held now), with the watchdog."""
        if keys is not None:
            self.keys = keys
        remaining = frames
        while True:
            chunk = min(remaining, 30)
            self._refresh(self.runner.cmd(f"step {chunk} {self.keys:x} {self.status_addr:x} {STATUS_SIZE}"))
            self._watchdog(chunk)
            remaining -= chunk
            if self.frame > self.max_frames:
                raise TestFailure(f"over the frame budget ({self.max_frames} frames): cb2={self.cb2()} "
                                  f"tasks={self.tasks()}")
            if remaining <= 0:
                break

    def _watchdog(self, frames):
        if self.st.get("magic") == MAGIC:
            if self.st["frames"] == self.last_game_frames:
                self.stalled += frames
                if self.stalled >= self.freeze_frames:
                    self.crash(f"freeze: the main loop made no progress for {self.stalled} frames")
            else:
                self.stalled = 0
            self.last_game_frames = self.st["frames"]
        if frames and self.frame % 60 < frames:
            # Screen watchdog: input held but the picture hasn't changed for screen_frames.
            # Not fatal (walking into a wall looks the same), so warn once with a screenshot.
            if self.keys:
                h = self.screen_hash()
                if h == self._last_hash:
                    self._same_screen += 60
                    if self._same_screen == self.screen_frames:
                        self.log(f"WARN screen unchanged for {self.screen_frames} frames with keys {self.keys:#x} "
                                 f"held (cb2={self.cb2()})")
                        self.warnings.append(f"frozen screen at frame {self.frame} (cb2={self.cb2()})")
                        self.screenshot("frozen_screen", advance=False)
                else:
                    self._same_screen = 0
                self._last_hash = h
            else:
                self._same_screen = 0
        if frames and self.frame % 120 < frames:
            stats = dict(kv.split("=") for kv in self.runner.cmd("stats").split())
            if int(stats["resets"]) > self.resets_seen:
                self.resets_seen = int(stats["resets"])
                if not getattr(self, "_expect_reset", False):
                    self.crash("reset: the game called SoftReset")
            self._drain_log()

    def _drain_log(self):
        lines = json.loads(self.runner.cmd("log"))
        for l in lines:
            if BOOT_NOISE.search(l):
                continue
            l = re.sub(r"pc=([0-9A-F]{8})", lambda m: f"pc={m.group(1)} ({self.sym.nearest(int(m.group(1), 16))})", l)
            kind = l.split("|", 1)[0]
            if kind == "error" or kind == "reset":
                self.errors.append(l)
                self.log(f"EMU {l}")
                if "Jumped to invalid address" in l:
                    self.crash("crash: " + l)
            else:
                self.log(f"GAME {l}")

    def crash(self, why):
        self.log(f"CRASH {why}")
        try:
            regs = self.runner.cmd("regs").split()
            pc, lr = int(regs[15], 16), int(regs[14], 16)
            where = f"pc={pc:08X} ({self.sym.nearest(pc)}) lr={lr:08X} ({self.sym.nearest(lr)})"
            self.log(f"CRASH at {where}; callback2={self.cb2()}")
            self.crash_info = dict(reason=why, pc=f"{pc:08X}", lr=f"{lr:08X}", where=where, callback2=self.cb2())
        except Exception as e:  # runner gone
            self.crash_info = dict(reason=why, error=str(e))
        try:
            self.screenshot("crash_last", advance=False)
        except Exception:
            pass
        raise GameCrash(why)

    def cb2(self):
        return self.sym.func_name(self.st.get("callback2", 0))

    def cb1(self):
        return self.sym.func_name(self.st.get("callback1", 0))

    # ----------------------------------------------------------------- input
    def key_mask(self, buttons):
        if isinstance(buttons, int):
            return buttons
        mask = 0
        for b in re.split(r"[+ ,]+", buttons.strip()):
            if b:
                mask |= KEYS[b.upper()]
        return mask

    def hold(self, buttons, frames):
        self.step(frames, self.key_mask(buttons))
        self.step(1, 0)

    def press(self, buttons="A", frames=4, after=4):
        """Tap buttons: hold `frames` frames, release, then wait `after` frames."""
        self.step(frames, self.key_mask(buttons))
        self.step(after, 0)

    def wait(self, frames):
        self.step(frames, 0)

    def wait_until(self, pred, timeout=1200, what="condition", keys=0, every=1):
        start = self.frame
        while not pred():
            if self.frame - start >= timeout:
                raise TestFailure(f"timeout after {timeout} frames waiting for {what}"
                                  f" (cb2={self.cb2()}, map={self.st.get('mapGroup')}.{self.st.get('mapNum')})")
            self.step(every, keys)
        return self.frame - start

    def seconds(self, s):
        self.wait(int(s * 60))

    # ------------------------------------------------------------ text/menus
    def printers(self):
        """Active text printers as (windowId, state)."""
        if not self.layout:
            return []
        L = self.layout
        out = []
        ptr = int(self.runner.cmd(f"r32 {self.sym['sFirstTextPrinter']:x}"), 16)
        for _ in range(40):
            if not 0x02000000 <= ptr < 0x02040000:
                break
            raw = bytes.fromhex(self.runner.cmd(f"rd {ptr:x} {L['printerNext'] + 4}"))
            if raw[L["printerActiveByte"]] & L["printerActiveMask"]:
                out.append((raw[L["printerWindowId"]], raw[L["printerState"]]))
            ptr = struct.unpack_from("<I", raw, L["printerNext"])[0]
        return out

    def text_active(self):
        return bool(self.printers())

    def script_native(self):
        """Name of the native function the overworld script is waiting in (e.g.
        WaitForAorBPress, IsFieldMessageBoxHidden), or None."""
        if not self.layout or not self.st.get("scriptActive"):
            return None
        a = self.sym["sGlobalScriptContext"]
        raw = bytes.fromhex(self.runner.cmd(f"rd {a:x} {self.layout['scriptNative'] + 4}"))
        if raw[self.layout["scriptMode"]] != 2:  # SCRIPT_MODE_NATIVE
            return None
        return self.sym.func_name(struct.unpack_from("<I", raw, self.layout["scriptNative"])[0])

    def text_waiting(self):
        """Text waits for a button: a printer shows the arrow mid-message, or the script
        sits in waitbuttonpress after a message."""
        L = self.layout or {}
        # RENDER_STATE_WAIT, _CLEAR and _SCROLL_START (consecutive in text.h) wait for A with the arrow.
        w = L.get("renderStateWait", -9)
        if any(s in (w, w + 1, w + 2) for _, s in self.printers()):
            return True
        return self.script_native() == "WaitForAorBPress" and not self.st["fadeActive"]

    def tasks(self):
        """Names of the active tasks' functions (menus show up here, e.g. Task_HandleYesNoInput)."""
        size = self.layout["sizeofTask"] if self.layout else 40
        raw = bytes.fromhex(self.runner.cmd(f"rd {self.sym['gTasks']:x} {size * 16}"))
        names = []
        for i in range(16):
            func, active = struct.unpack_from("<IB", raw, i * size)
            if active:
                names.append(self.sym.func_name(func))
        return names

    def menu_open(self):
        return any(re.search(r"YesNo|Multichoice|ListMenu|Menu_Process|HandleInput|MenuInput|Naming", t) for t in self.tasks())

    def wait_text(self, timeout=1800):
        """Wait until text waits for a button, or no text is printing any more."""
        return self.wait_until(lambda: self.text_waiting() or not self.text_active(), timeout, "text")

    def advance(self, boxes=1, timeout=1800):
        """Wait for `boxes` text boxes to finish and press A on each."""
        for _ in range(boxes):
            self.wait_until(self.text_waiting, timeout, "a text box waiting for A")
            self.press("A", 2, 2)

    def talk(self, max_boxes=60, timeout=6000, stop_at_menu=True):
        """Press A through a script's text until the script ends (field unlocked) or a
        menu (YES/NO, multichoice) needs an answer. Returns 'done', 'menu' or 'battle'."""
        start = self.frame
        boxes = 0
        while self.frame - start < timeout:
            if self.st.get("inBattle"):
                return "battle"
            if self.text_waiting():
                self.press("A", 2, 2)
                boxes += 1
                if boxes > max_boxes:
                    raise TestFailure(f"more than {max_boxes} text boxes")
                continue
            if stop_at_menu and self.menu_open() and not self.text_active():
                return "menu"
            if not self.st["scriptActive"] and not self.st["fieldLocked"] and not self.text_active() \
                    and self.cb2() == "CB2_Overworld":
                return "done"
            self.step(2, 0)
        raise TestFailure(f"talk: script still running after {timeout} frames (cb2={self.cb2()}, tasks={self.tasks()})")

    # ------------------------------------------------------------- overworld
    def in_overworld(self):
        return self.cb2() == "CB2_Overworld" and not self.st["fadeActive"]

    def wait_overworld(self, timeout=1200):
        """Wait until the player can move (map loaded, faded in, no script)."""
        return self.wait_until(lambda: self.in_overworld() and not self.st["fieldLocked"]
                               and not self.st["scriptActive"], timeout, "free overworld")

    def pos(self):
        return (self.st["x"], self.st["y"])

    def map_id(self):
        return self.st["mapNum"] | (self.st["mapGroup"] << 8)

    def map_name(self):
        return self._map_name()

    def _map_name(self):
        names = getattr(self, "_map_names", None)
        if names is None:
            names = {}
            text = open(os.path.join(ROOT, "include/constants/map_groups.h")).read()
            for m in re.finditer(r"(MAP_\w+)\s*=\s*\((\d+) \| \((\d+) << 8\)\)", text):
                names[int(m.group(2)) | (int(m.group(3)) << 8)] = m.group(1)
            self._map_names = names
        return names.get(self.map_id(), f"map {self.st['mapGroup']}.{self.st['mapNum']}")

    def walk(self, direction, tiles=1, run=False, timeout_per_tile=60):
        """Walk `tiles` tiles. Counts position changes; a map change (edge or warp) ends the walk.
        Returns the number of tiles moved (fewer when blocked)."""
        direction = direction.lower()
        mask = self.key_mask(DIR_KEYS[direction]) | (KEYS["B"] if run else 0)
        moved = 0
        start_map = self.map_id()
        last = self.pos()
        idle = 0
        self.keys = mask
        while moved < tiles:
            self.step(1, mask)
            if self.map_id() != start_map:
                moved += 1
                break
            if self.cb2() != "CB2_Overworld":  # a battle or another screen took over
                break
            if self.pos() != last:
                moved += 1
                last = self.pos()
                idle = 0
            else:
                idle += 1
                if idle > timeout_per_tile:
                    break
            if self.st["scriptActive"] or self.st["inBattle"]:
                break
        self.step(1, 0)
        self.wait_until(lambda: self.st["moving"] == 0 or self.cb2() != "CB2_Overworld", 120, "the step to end")
        if moved < tiles and self.map_id() == start_map:
            self.log(f"walk {direction} {tiles}: moved {moved} (blocked or interrupted) at {self.pos()}")
        return moved

    def face(self, direction):
        self.press(DIR_KEYS[direction.lower()], 2, 6)

    def path_to(self, x, y, walkable):
        """Shortest walk from the player to (x, y) over `walkable` tiles (a set)."""
        from collections import deque
        start = self.pos()
        prev = {start: None}
        q = deque([start])
        while q:
            cur = q.popleft()
            if cur == (x, y):
                break
            for d, (dx, dy) in DIRS.items():
                n = (cur[0] + dx, cur[1] + dy)
                if n in walkable and n not in prev:
                    prev[n] = (cur, d)
                    q.append(n)
        if (x, y) not in prev:
            return None
        steps = []
        cur = (x, y)
        while prev[cur]:
            cur, d = prev[cur]
            steps.append(d)
        steps.reverse()
        runs = []
        for d in steps:
            if runs and runs[-1][0] == d:
                runs[-1][1] += 1
            else:
                runs.append([d, 1])
        return runs

    def walk_to(self, x, y, walkable):
        runs = self.path_to(x, y, walkable)
        if runs is None:
            raise TestFailure(f"no path from {self.pos()} to {(x, y)}")
        for d, n in runs:
            if self.walk(d, n) < n:
                break
        return self.pos() == (x, y)

    # -------------------------------------------------------------- commands
    def _command(self, name, args=(), scenario=b"", timeout=600):
        self.seq = (self.st.get("doneSeq", 0) + 1) & 0xFFFF or 1
        args = list(args) + [0] * (4 - len(args))
        data = struct.pack("<HH4H", 0, CMD[name], *[a & 0xFFFF for a in args]) + scenario
        self.runner.cmd(f"wd {self.cmd_addr:x} {data.hex()}")
        self.runner.cmd(f"w16 {self.cmd_addr:x} {self.seq:x}")
        self.wait_until(lambda: self.st.get("doneSeq") == self.seq, timeout, f"command {name}")
        if self.st["result"] != 1:
            raise TestFailure(f"command {name}{tuple(args)} refused in state cb2={self.cb2()} "
                              f"script={self.st['scriptActive']} locked={self.st['fieldLocked']} "
                              f"fade={self.st['fadeActive']}")

    def boot(self, timeout=3000):
        """Reset and run to the title screen."""
        self.log("boot")
        self.wait_until(lambda: self.st.get("magic") == MAGIC and "Task_TitleScreenPhase3" in self.tasks(),
                        timeout, "the title screen", every=10)
        self.wait(30)

    def quickstart(self, map_name, x, y, story=1, era=0, party=(), items=(), vars=(), flags=(),
                   encounters=False, collision=True, instant_text=True, battle_anim=False, female=False):
        """New game straight into a state: map/x/y, story and era vars, party [(species, level)],
        items [(item, count)], vars [(var, value)], flags [flag]. From any non-battle screen."""
        if self.st.get("magic") != MAGIC or self.cb2() in ("NULL", "CB2_InitCopyrightScreenAfterBootup"):
            self.boot()
        c = self.const
        mid = c(map_name)
        opts = (0 if encounters else OPT["no_encounters"]) | (0 if collision else OPT["no_collision"]) \
            | (OPT["instant_text"] if instant_text else 0) | (0 if battle_anim else OPT["no_battle_anim"]) \
            | (OPT["female"] if female else 0)
        party = [(c(s), int(l)) for s, l in party]
        items = [(c(i), int(n)) for i, n in items]
        vars_ = [(c(v), c(val)) for v, val in vars]
        flags = [c(f) for f in flags]
        assert len(party) <= 6 and len(items) <= PT_MAX_ITEMS and len(vars_) <= PT_MAX_VARS and len(flags) <= PT_MAX_FLAGS
        sc = struct.pack("<HHhhHHHH", mid >> 8, mid & 0xFF, x, y, c(story), c(era), opts, len(party))
        sc += b"".join(struct.pack("<HH", *p) for p in party + [(0, 0)] * (6 - len(party)))
        sc += b"".join(struct.pack("<HH", *p) for p in items + [(0, 0)] * (PT_MAX_ITEMS - len(items)))
        sc += b"".join(struct.pack("<HH", *p) for p in vars_ + [(0, 0)] * (PT_MAX_VARS - len(vars_)))
        sc += struct.pack(f"<{PT_MAX_FLAGS}H", *(flags + [0] * (PT_MAX_FLAGS - len(flags))))
        self.log(f"quickstart {map_name} ({x}, {y}) story={story} era={era} party={party}")
        self._command("QUICKSTART", scenario=sc)
        self.wait_until(lambda: self.map_id() == mid and self.in_overworld() and not self.st["fieldLocked"],
                        1800, f"arrival on {map_name}")
        self.wait_until(lambda: not self.st["scriptActive"], 600, "map scripts to finish")
        self.log(f"arrived {self._map_name()} at {self.pos()}")

    def set_var(self, var, value):
        self._command("SET_VAR", [self.const(var), self.const(value)])

    def set_flag(self, flag, on=True):
        self._command("SET_FLAG", [self.const(flag), int(bool(on))])

    def warp(self, map_name, x, y):
        mid = self.const(map_name)
        self.wait_overworld()
        self._command("WARP", [mid >> 8, mid & 0xFF, x & 0xFFFF, y & 0xFFFF])
        self.wait_until(lambda: self.map_id() == mid and self.in_overworld() and not self.st["fieldLocked"],
                        1800, f"warp to {map_name}")
        self.log(f"warped to {map_name} {self.pos()}")

    def run_script(self, symbol):
        a = self.sym[symbol]
        self.wait_overworld()
        self._command("RUN_SCRIPT", [a & 0xFFFF, a >> 16])
        self.log(f"run script {symbol}")

    def give_mon(self, species, level):
        self._command("GIVE_MON", [self.const(species), int(level)])

    def give_item(self, item, count=1):
        self._command("GIVE_ITEM", [self.const(item), int(count)])

    def heal(self):
        self._command("HEAL")

    def party(self):
        self._command("READ_PARTY")
        return [m for m in self.st["party"][:self.st["partyCount"]]]

    def read_text(self, symbol_or_addr, maxlen=400):
        a = self.sym[symbol_or_addr] if isinstance(symbol_or_addr, str) else symbol_or_addr
        return decode_text(bytes.fromhex(self.runner.cmd(f"rd {a:x} {maxlen}")))

    def battle_text(self):
        """The battle message on screen (gDisplayedStringBattle)."""
        return self.read_text("gDisplayedStringBattle")

    # ---------------------------------------------------------------- battle
    def controllers(self):
        """Names of gBattlerControllerFuncs[0..3] (e.g. HandleInputChooseAction for battler 0)."""
        raw = bytes.fromhex(self.runner.cmd(f"rd {self.sym['gBattlerControllerFuncs']:x} 16"))
        return [self.sym.func_name(v) for v in struct.unpack("<4I", raw)]

    def wait_battle(self, timeout=1800):
        self.wait_until(lambda: self.st["inBattle"], timeout, "a battle")

    def battle(self, action="fight", max_actions=80, timeout=60000, shots=True):
        """Play a battle to its end. action: 'fight' (first move every turn), 'run', or
        'catch' (throw the last used capsule with R every turn). Text is advanced with B, so
        YES/NO prompts (nickname, 'use next?') get NO. Screenshots: battle_start, throw_N,
        codex (the registration page), battle_end. Returns gBattleOutcome
        (1 won, 2 lost, 4 ran, 7 caught; see include/constants/battle.h)."""
        start = self.frame
        actions = 0
        seen_dex = False
        idle = 0
        last_msg = ""
        self.wait_battle()
        while self.st["inBattle"] or "Battle" in self.cb2():
            if self.frame - start > timeout:
                raise TestFailure(f"battle still running after {timeout} frames (controllers={self.controllers()})")
            if not self.st["inBattle"] and self.cb2() in ("CB2_Overworld",):
                break
            cb2 = self.cb2()
            if not seen_dex and re.search(r"Dex|Codex", cb2 + " ".join(self.tasks())):
                seen_dex = True
                self.wait(30)
                if shots:
                    self.screenshot("codex")
            ctrl = self.controllers() if self.st["inBattle"] else []
            if "HandleInputChooseAction" in ctrl:
                if actions == 0 and shots:
                    self.screenshot("battle_start")
                actions += 1
                if actions > max_actions:
                    raise TestFailure(f"battle: more than {max_actions} turns")
                if action == "run":
                    self.press("RIGHT", 2, 2); self.press("DOWN", 2, 2); self.press("A", 2, 10)
                elif action == "catch":
                    self.press("R", 2, 40)
                    if shots:
                        self.screenshot(f"throw_{actions}")
                else:
                    self.press("LEFT", 2, 2); self.press("UP", 2, 2); self.press("A", 2, 10)
                idle = 0
                continue
            if "HandleInputChooseMove" in ctrl:
                self.press("LEFT", 2, 2); self.press("UP", 2, 2); self.press("A", 2, 10)
                continue
            if "HandleInputChooseTarget" in ctrl:
                self.press("A", 2, 10)
                continue
            msg = self.battle_text() if self.st["inBattle"] else ""
            if msg and msg != last_msg and " " in msg.strip():
                self.log(f"battle: {msg.replace(chr(10), ' ').strip()}")
                last_msg = msg
            if "PartyMenu" in cb2 and action != "run":
                # 'Use next?' -> YES opened the party: send out the next healthy one.
                self.wait(20)
                self.press("DOWN", 2, 6); self.press("A", 2, 20); self.press("A", 2, 30)
                continue
            if action != "run" and "Use next" in msg and not self.text_active():
                self.press("A", 2, 20)
                last_msg = ""
                continue
            if self.text_waiting():
                self.press("B", 2, 2)
                idle = 0
                continue
            idle += 1
            if idle % 30 == 0:
                self.press("B", 2, 2)  # pages and prompts that aren't text printers
            self.step(2, 0)
        outcome = self.st["battleOutcome"]
        self.log(f"battle over: outcome {outcome} after {actions} actions, {self.frame - start} frames")
        self.wait_until(lambda: self.cb2() == "CB2_Overworld" and not self.st["fadeActive"], 3000,
                        "the overworld after the battle")
        if shots:
            self.screenshot("battle_end")
        return outcome

    # ------------------------------------------------------------- memory
    def read(self, symbol_or_addr, size=4, offset=0):
        a = (self.sym[symbol_or_addr] if isinstance(symbol_or_addr, str) else symbol_or_addr) + offset
        return int.from_bytes(bytes.fromhex(self.runner.cmd(f"rd {a:x} {size}")), "little")

    def var(self, name):
        """A var's value (save vars 0x4000+, special vars 0x8000+), via the game's VarGet."""
        self._command("GET_VAR", [self.const(name)])
        return self.st["value"]

    def flag(self, name):
        self._command("GET_FLAG", [self.const(name)])
        return bool(self.st["value"])

    def item_count(self, item):
        self._command("COUNT_ITEM", [self.const(item)])
        return self.st["value"]

    # -------------------------------------------------------------- outputs
    def screenshot(self, name, advance=True):
        if advance:
            self.step(1)  # one more frame so the picture matches the state just read
        n = len(self.shots) + 1
        fname = f"{n:03d}_{re.sub(r'[^A-Za-z0-9_.-]', '_', name)}.png"
        path = os.path.join(self.out, fname)
        self.runner.cmd(f"shot {path}")
        self.shots.append(dict(file=fname, name=name, frame=self.frame, map=self._map_name(), pos=self.pos()))
        self.log(f"screenshot {fname} on {self._map_name()} at {self.pos()}")
        return path

    def screen_hash(self):
        return self.runner.cmd("hash")

    def save_state(self, path):
        self.runner.cmd(f"ss {path}")

    def load_state(self, path):
        self.runner.cmd(f"ls {path}")
        self.stalled, self.last_game_frames, self._same_screen = 0, 0, 0
        self.step(1)

    # ------------------------------------------------------------- checks
    def check(self, ok, what):
        self.checks.append(dict(ok=bool(ok), what=what, frame=self.frame))
        self.log(("PASS " if ok else "FAIL ") + what)
        if not ok:
            raise TestFailure(what)

    def expect_map(self, map_name):
        self.check(self.map_id() == self.const(map_name), f"on {map_name} (now {self._map_name()})")

    def expect_var(self, var, value):
        got = self.var(var)
        self.check(got == self.const(value), f"{var} == {value} (got {got})")

    def expect_flag(self, flag, on=True):
        got = self.flag(flag)
        self.check(got == on, f"{flag} is {'set' if on else 'clear'} (got {got})")

    def expect_pos(self, x, y):
        self.check(self.pos() == (x, y), f"player at {(x, y)} (got {self.pos()})")

    def expect_battle(self, on=True):
        self.check(bool(self.st["inBattle"]) == on, f"in battle == {on}")

    def close(self, status="pass", error=None):
        try:
            self._drain_log()
        except Exception:
            pass
        result = dict(scenario=self.name, status=status, error=error, frames=self.frame,
                      seconds=round(time.time() - self.t0, 2), screenshots=self.shots, checks=self.checks,
                      emulator_errors=self.errors, warnings=self.warnings, crash=getattr(self, "crash_info", None), rom=self.rom)
        json.dump(result, open(os.path.join(self.out, "result.json"), "w"), indent=1)
        self.log(f"{status.upper()} {self.name}: {self.frame} frames in {result['seconds']} s"
                 + (f" ({error})" if error else ""))
        self.logf.close()
        self.runner.close()
        return result


# ------------------------------------------------------------------ text DSL
def run_dsl(g, text):
    """Run a line-based scenario: one Game method per line, e.g.
    `press A`, `walk up 3`, `wait_text`, `talk`, `screenshot levee`, `expect_map MAP_STRATA_LEVEE`,
    `expect_var VAR_STRATA_STORY 2`, `quickstart MAP_STRATA_LEVEE 10 20 story=2 era=1 party=SPECIES_X:12`.
    Lines starting with # are comments."""
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        words = line.split()
        fn = getattr(g, words[0], None)
        if fn is None or words[0].startswith("_"):
            raise TestFailure(f"line {lineno}: unknown command {words[0]}")
        args, kwargs = [], {}
        for w in words[1:]:
            if "=" in w:
                k, v = w.split("=", 1)
                if k in ("party", "items", "vars"):
                    kwargs[k] = [tuple(p.split(":")) for p in v.split(",")]
                elif k == "flags":
                    kwargs[k] = v.split(",")
                else:
                    kwargs[k] = _num(v)
            else:
                args.append(_num(w))
        result = fn(*args, **kwargs)
        if words[0] in ("party", "tasks", "printers", "pos"):
            g.log(f"{words[0]}: {result}")


def _num(s):
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if s in ("True", "False"):
        return s == "True"
    return s
