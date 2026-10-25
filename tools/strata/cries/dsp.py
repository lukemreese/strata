"""DSP building blocks for the cry synthesiser: stdlib only and deterministic.

Signals are plain lists of floats at SR (full scale = 1.0). Everything random
draws from a random.Random seeded by zlib.crc32 of a name (never hash(), which
is salted per process), so a re-run is byte-identical.

Primitives (each returns a list of samples, `n = ns(seconds)` long):
  voiced    source-filter voice: band-limited glottal pulse train (closed-form
            geometric harmonic series, so nothing aliases), jitter, shimmer,
            subharmonics, amplitude modulation, breath noise, parallel formants
  noise     filtered noise bands (hiss, snort, huff, splash, breath)
  tone      a few sine harmonics on an FM contour (whistles, squeaks, bat sweeps)
  click     damped sinusoid plus a noise tick (claps, pops, ticks, knocks)
Contours are functions of normalised time t in [0, 1] (see `curve`).
"""

import math
import random
import zlib

SR = 13379          # the m4a mixer rate (src/m4a.c), and the rate most stock cries use
NYQ = SR / 2
TAU = 2 * math.pi
BLOCK = 16          # samples between filter-coefficient updates
BRIGHT_REF = 3000.0  # Hz, where voiced()'s `bright` roll-off is measured (see there)


def seed_of(*parts):
    return zlib.crc32("|".join(str(p) for p in parts).encode())


def rng_of(*parts):
    return random.Random(seed_of(*parts))


def ns(sec):
    return max(1, int(round(sec * SR)))


def fn(x):
    """A constant or a contour, as a contour."""
    return x if callable(x) else (lambda t, v=x: v)


def curve(*pts, log=False):
    """Piecewise-linear contour through (t, value) points, t in [0, 1].
    log=True interpolates in log space (use it for frequencies)."""
    pts = sorted(pts)
    if log:
        pts = [(t, math.log(v)) for t, v in pts]

    def f(t):
        if t <= pts[0][0]:
            v = pts[0][1]
        elif t >= pts[-1][0]:
            v = pts[-1][1]
        else:
            v = pts[-1][1]
            for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
                if t <= t1:
                    v = v0 + (v1 - v0) * ((t - t0) / (t1 - t0) if t1 > t0 else 1.0)
                    break
        return math.exp(v) if log else v
    return f


def scaled(c, k):
    c = fn(c)
    return lambda t: c(t) * k


def sample(c, n):
    c = fn(c)
    if n == 1:
        return [c(0.0)]
    return [c(i / (n - 1)) for i in range(n)]


def envelope(n, attack=0.01, release=0.05, shape=None, power=1.0):
    """Amplitude envelope: `shape` contour (default flat) times a raised-cosine
    attack and release (seconds)."""
    shape = fn(shape if shape is not None else 1.0)
    a, r = max(1, ns(attack)), max(1, ns(release))
    out = []
    for i in range(n):
        v = shape(i / max(1, n - 1))
        if i < a:
            v *= 0.5 - 0.5 * math.cos(math.pi * i / a)
        if n - 1 - i < r:
            v *= 0.5 - 0.5 * math.cos(math.pi * (n - 1 - i) / r)
        out.append(max(0.0, v) ** power if power != 1.0 else max(0.0, v))
    return out


def smooth_noise(n, rng, rate):
    """Band-limited random wobble in [-1, 1] (values at `rate` Hz, cosine-interpolated)."""
    step = max(1, int(SR / max(0.1, rate)))
    pts = [rng.uniform(-1, 1) for _ in range(n // step + 3)]
    out = []
    for i in range(n):
        k, u = divmod(i, step)
        u = 0.5 - 0.5 * math.cos(math.pi * u / step)
        out.append(pts[k] + (pts[k + 1] - pts[k]) * u)
    return out


# ---------------------------------------------------------------- filters

class Bandpass:
    """RBJ constant-0-dB-peak band-pass biquad with time-varying centre/bandwidth."""

    def __init__(self):
        self.x1 = self.x2 = self.y1 = self.y2 = 0.0
        self.set(1000.0, 100.0)

    def set(self, f, bw):
        f = min(max(f, 20.0), NYQ * 0.94)
        q = max(0.3, f / max(bw, 5.0))
        w = TAU * f / SR
        alpha = math.sin(w) / (2 * q)
        a0 = 1 + alpha
        self.b0 = alpha / a0
        self.a1 = -2 * math.cos(w) / a0
        self.a2 = (1 - alpha) / a0

    def run(self, x):
        y = self.b0 * (x - self.x2) - self.a1 * self.y1 - self.a2 * self.y2
        self.x2, self.x1 = self.x1, x
        self.y2, self.y1 = self.y1, y
        return y


def formants(x, bank, direct=0.0):
    """Parallel formant filter. bank: [(freq contour, bandwidth contour, gain)];
    formants at or above ~Nyquist are dropped. `direct` mixes in the unfiltered
    source (keeps tiny animals, whose vocal tracts resonate above Nyquist, audible)."""
    n = len(x)
    y = [v * direct for v in x]
    for f, bw, g in bank:
        f, bw = fn(f), fn(bw)
        if f(0.0) >= NYQ * 0.94 and f(1.0) >= NYQ * 0.94 and f(0.5) >= NYQ * 0.94:
            continue
        bp = Bandpass()
        for i in range(n):
            if i % BLOCK == 0:
                t = i / max(1, n - 1)
                fc = f(t)
                bp.set(fc, bw(t))
                fade = 1.0 if fc < NYQ * 0.85 else max(0.0, (NYQ * 0.94 - fc) / (NYQ * 0.09))
                gg = g * fade
            y[i] += gg * bp.run(x[i])
    return y


def lowpass(x, cutoff, q=0.707):
    """RBJ low-pass biquad, fixed cutoff."""
    w = TAU * min(cutoff, NYQ * 0.95) / SR
    alpha = math.sin(w) / (2 * q)
    a0 = 1 + alpha
    b0 = (1 - math.cos(w)) / 2 / a0
    b1 = (1 - math.cos(w)) / a0
    a1, a2 = -2 * math.cos(w) / a0, (1 - alpha) / a0
    x1 = x2 = y1 = y2 = 0.0
    out = []
    for v in x:
        y = b0 * v + b1 * x1 + b0 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, v, y1, y
        out.append(y)
    return out


def highpass(x, cutoff, q=0.707):
    """RBJ high-pass biquad, fixed cutoff (DC and sub-bass removal)."""
    w = TAU * cutoff / SR
    alpha = math.sin(w) / (2 * q)
    a0 = 1 + alpha
    b0 = (1 + math.cos(w)) / 2 / a0
    b1 = -(1 + math.cos(w)) / a0
    a1, a2 = -2 * math.cos(w) / a0, (1 - alpha) / a0
    x1 = x2 = y1 = y2 = 0.0
    out = []
    for v in x:
        y = b0 * v + b1 * x1 + b0 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, v, y1, y
        out.append(y)
    return out


# ---------------------------------------------------------------- sources

def voiced(dur, f0, form=(), *, rng, bright=36.0, direct=0.15, env=None, attack=0.015,
           release=0.06, vib=(0.0, 0.0), jitter=0.0, shimmer=0.0, sub=0.0, am=(0.0, 0.0),
           breath=0.0, breath_band=(2500.0, 3000.0), log=None):
    """Source-filter voice.
    f0       Hz contour.  bright: harmonic roll-off (geometric), dB down at
             max(BRIGHT_REF, 4 f0) (higher = darker)
    form     formant bank, see `formants`
    vib      (rate Hz, depth semitones) sinusoidal vibrato; jitter: random f0 wobble
             (fraction); shimmer: random amplitude wobble (fraction)
    sub      0..1 period-doubling (a subharmonic at f0/2: growl, roughness)
    am       (rate Hz, depth 0..1) amplitude modulation (trill, gobble, purr)
    breath   noise mixed into the source, coloured by breath_band (centre, bandwidth)
    log      list that receives (min f0, max f0), for the report"""
    n = ns(dur)
    f0 = sample(f0, n)
    vr, vd = vib
    jit = smooth_noise(n, rng, 28.0) if jitter else None
    shim = smooth_noise(n, rng, 40.0) if shimmer else None
    ar, ad = am
    src = []
    ph = ph2 = 0.0
    r = 0.5
    norm = 1.0
    fmin, fmax = 1e9, 0.0
    for i in range(n):
        tsec = i / SR
        f = f0[i]
        if vd:
            f *= 2 ** (vd * math.sin(TAU * vr * tsec) / 12)
        if jit:
            f *= 1 + jitter * jit[i]
        f = min(max(f, 20.0), NYQ * 0.9)
        fmin, fmax = min(fmin, f), max(fmax, f)
        if i % BLOCK == 0:
            # roll-off reference: `bright` dB down at max(BRIGHT_REF, 4 f0), never past
            # Nyquist, so low voices are not buzzes and nothing loud aliases
            harmonics = min(max(BRIGHT_REF / f, 4.0), NYQ / f)
            r = 10 ** (-bright / 20 / harmonics)
            r = min(r, 0.995)
            norm = math.sqrt(2 * (1 - r * r)) / r
        ph += TAU * f / SR
        ph2 += math.pi * f / SR
        if ph > TAU:
            ph -= TAU
        if ph2 > TAU:
            ph2 -= TAU
        c = math.cos(ph)
        v = (r * c - r * r) / (1 - 2 * r * c + r * r) * norm
        if sub:
            v *= 1 - sub * (0.5 + 0.5 * math.cos(ph2))
        if ad:
            v *= 1 - ad * (0.5 + 0.5 * math.cos(TAU * ar * tsec))
        if shim:
            v *= 1 + shimmer * shim[i]
        src.append(v)
    if log is not None:
        log.append((fmin, fmax))
    if breath:
        nz = noise_raw(n, rng)
        nz = formants(nz, [(breath_band[0], breath_band[1], 1.0)])
        src = [s + breath * 3.0 * z for s, z in zip(src, nz)]
    y = formants(src, form, direct) if form else src
    e = envelope(n, attack, release, env)
    return [a * b for a, b in zip(y, e)]


def noise_raw(n, rng):
    u = rng.uniform
    return [u(-1.0, 1.0) for _ in range(n)]


def noise(dur, bands, *, rng, env=None, attack=0.005, release=0.05, am=(0.0, 0.0), direct=0.0):
    """Filtered noise: bands = [(centre contour, bandwidth contour, gain)]."""
    n = ns(dur)
    x = noise_raw(n, rng)
    y = formants(x, bands, direct)
    ar, ad = am
    if ad:
        y = [v * (1 - ad * (0.5 + 0.5 * math.cos(TAU * ar * i / SR))) for i, v in enumerate(y)]
    e = envelope(n, attack, release, env)
    return [a * b for a, b in zip(y, e)]


def tone(dur, freq, harmonics=(1.0,), *, env=None, attack=0.005, release=0.03, vib=(0.0, 0.0),
         am=(0.0, 0.0), rng=None, jitter=0.0, log=None):
    """Sine harmonics on an FM contour (harmonics above Nyquist are dropped)."""
    n = ns(dur)
    fr = sample(freq, n)
    vr, vd = vib
    ar, ad = am
    jit = smooth_noise(n, rng, 30.0) if jitter and rng else None
    ph = 0.0
    out = []
    fmin, fmax = 1e9, 0.0
    for i in range(n):
        tsec = i / SR
        f = fr[i]
        if vd:
            f *= 2 ** (vd * math.sin(TAU * vr * tsec) / 12)
        if jit:
            f *= 1 + jitter * jit[i]
        fmin, fmax = min(fmin, f), max(fmax, f)
        ph += TAU * f / SR
        if ph > TAU * 64:
            ph -= TAU * 64
        v = 0.0
        for k, a in enumerate(harmonics, 1):
            if a and f * k < NYQ * 0.92:
                v += a * math.sin(k * ph)
        if ad:
            v *= 1 - ad * (0.5 + 0.5 * math.cos(TAU * ar * tsec))
        out.append(v)
    if log is not None:
        log.append((fmin, fmax))
    e = envelope(n, attack, release, env)
    return [a * b for a, b in zip(out, e)]


def click(freq, decay, *, rng, noise_amt=0.4, dur=None, chirp=0.0):
    """Damped sinusoid at `freq` Hz decaying by 1/e every `decay` seconds, plus a
    noise tick. chirp: fractional frequency rise over the click (bubbles rise)."""
    dur = dur or decay * 6
    n = ns(dur)
    out = []
    ph = 0.0
    for i in range(n):
        tsec = i / SR
        f = freq * (1 + chirp * min(1.0, tsec / dur))
        ph += TAU * min(f, NYQ * 0.9) / SR
        e = math.exp(-tsec / decay)
        out.append(e * math.sin(ph) + noise_amt * e * e * rng.uniform(-1, 1))
    att = min(n, 8)
    for i in range(att):
        out[i] *= i / att
    return out


# ---------------------------------------------------------------- mixing

class Track:
    def __init__(self, sec):
        self.x = [0.0] * ns(sec)

    def add(self, at, sig, gain=1.0):
        i0 = ns(at) if at > 0 else 0
        need = i0 + len(sig)
        if need > len(self.x):
            self.x.extend([0.0] * (need - len(self.x)))
        x = self.x
        for i, v in enumerate(sig):
            x[i0 + i] += gain * v
        return at + len(sig) / SR

    def trim(self, floor=1e-4):
        """Drops trailing near-silence (keeps 20 ms)."""
        peak = max((abs(v) for v in self.x), default=0.0) or 1.0
        last = max((i for i, v in enumerate(self.x) if abs(v) > floor * peak), default=0)
        self.x = self.x[:min(len(self.x), last + ns(0.02))]
        return self


def rms(x):
    return math.sqrt(sum(v * v for v in x) / max(1, len(x)))


def peak_norm(x, to=1.0):
    p = max((abs(v) for v in x), default=0.0)
    return [v * to / p for v in x] if p else x
