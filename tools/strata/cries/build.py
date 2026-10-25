"""Render a species' cry: program -> mix -> master -> 8-bit wav bytes.

Mastering (in order): 45 Hz high-pass (no DC, no inaudible sub-bass eating
DPCM headroom), a 5.6 kHz low-pass (content near Nyquist only adds DPCM
slope-overload error), 3 ms fade-in / 12 ms fade-out, then loudness normalisation to
TARGET_LOUDNESS (analysis.loudness, K-weighted and gated) with a look-ahead
peak limiter at CEILING, repeated until the level settles. Finally the 8-bit
quantisation and DPCM round trip are simulated and the loudness is corrected
once more on the decoded signal, so what the hardware plays is on target.
"""

import io
import math
import os
import re
import wave

from . import analysis, dsp
from .specs import CRIES
from .voices import CALLS, Voice

TARGET_LOUDNESS = -11.0   # dB, analysis.loudness; stock cries: median -8, p25 -10 (see --report)
CEILING = 0.9             # peak, full scale 1.0 (=114 of 127): no rail clipping after DPCM
MIN_SEC, MAX_SEC = 0.35, 1.6
DEFAULT_GAP = 0.06

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def lineages():
    """folder -> lineage root folder, from the DESCENT_* lists in src/data/lineages.h
    (species not in any lineage are their own root)."""
    with open(os.path.join(ROOT, "src/data/lineages.h")) as f:
        text = f.read()
    parent = {}

    def root(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x

    for m in re.finditer(r"sDescent_(\w+)\[\]\s*=\s*\{(.*?)\};", text, re.S):
        src = m.group(1).lower()
        for d in re.findall(r"DESCENT_(?:DEFAULT|BRANCH)\(SPECIES_(\w+)", m.group(2)):
            a, b = root(src), root(d.lower())
            if a != b:
                parent[b] = a
    return lambda folder: root(folder)


def limiter(x, ceiling=CEILING, look=0.003, release=0.06):
    n = len(x)
    w = max(1, dsp.ns(look))
    need = [min(1.0, ceiling / abs(v)) if abs(v) > ceiling else 1.0 for v in x]
    if min(need) >= 1.0:
        return x
    gm = [min(need[i:i + w + 1]) for i in range(n)]       # gain dips w samples before a peak
    avg, acc = [], float(w + 1)                             # moving mean over [i-w, i]: stays
    for i in range(n):                                      # below the need at every peak
        acc += gm[i] - (gm[i - w - 1] if i - w - 1 >= 0 else 1.0)
        avg.append(min(gm[i], acc / (w + 1)))
    rel = 1 - math.exp(-1 / (release * dsp.SR))
    out, g = [], 1.0
    for i in range(n):
        g = min(avg[i], g + (1 - g) * rel)
        out.append(x[i] * g)
    return out


def quantise(x):
    return [max(-128, min(127, int(round(v * 128)))) for v in x]


def master(x):
    x = dsp.lowpass(dsp.highpass(x, 45.0), 5600.0)
    fi, fo = dsp.ns(0.003), dsp.ns(0.012)
    for i in range(min(fi, len(x))):
        x[i] *= i / fi
    for i in range(min(fo, len(x))):
        x[-1 - i] *= i / fo
    x = dsp.peak_norm(x, 0.5)
    for _ in range(5):
        g = 10 ** ((TARGET_LOUDNESS - analysis.loudness(x)) / 20)
        x = limiter([v * g for v in x])
    # Low, pulse-like voices (booms, bellows) have a high crest factor and hit the
    # ceiling before the target. Gentle tanh saturation lowers the crest factor and
    # adds the upper harmonics a small speaker can reproduce (a rough voice anyway).
    for drive in (1.5, 2.0):
        if analysis.loudness(x) > TARGET_LOUDNESS - 0.8:
            break
        x = [math.tanh(drive * v) for v in dsp.peak_norm(x)]
        x = dsp.peak_norm(dsp.highpass(x, 30.0), CEILING)  # tanh of an asymmetric wave adds DC
        for _ in range(3):
            g = 10 ** ((TARGET_LOUDNESS - analysis.loudness(x)) / 20)
            x = limiter([v * g for v in x])
    for _ in range(2):
        levels = quantise(x)
        _, dec = analysis.dpcm_roundtrip(levels)
        err = TARGET_LOUDNESS - analysis.loudness([v / 128 for v in dec])
        if abs(err) < 0.25:
            break
        x = limiter([v * 10 ** (err / 20) for v in x])
    return quantise(x)


def render(folder, mass, plan, lineage_root):
    """Returns (levels -128..127, Voice) for one species."""
    if folder not in CRIES:
        raise SystemExit(f"gen_cry: no cry program for {folder} in tools/strata/cries/specs.py")
    _, program = CRIES[folder]
    v = Voice(folder, plan, mass, lineage_root)
    t = dsp.Track(0.05)
    end = None
    for call, opts in program:
        opts = dict(opts)
        gap = opts.pop("gap", DEFAULT_GAP)
        gain = opts.pop("gain", 1.0)
        if call not in CALLS:
            raise SystemExit(f"gen_cry: {folder}: unknown call {call}")
        piece = dsp.peak_norm(CALLS[call](v, **opts).x)
        end = t.add(0.0 if end is None else max(0.0, end + gap), piece, gain)
    x = t.trim().x
    secs = len(x) / dsp.SR
    if not MIN_SEC <= secs <= MAX_SEC:
        raise SystemExit(f"gen_cry: {folder} is {secs:.2f} s (keep cries {MIN_SEC}-{MAX_SEC} s)")
    return master(x), v


def wav_bytes(levels):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(dsp.SR)
        w.writeframes(bytes(v + 128 for v in levels))
    return buf.getvalue()
