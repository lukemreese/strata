"""Listening proxies: what the GBA will play, and how to look at it.

  dpcm_roundtrip  the exact DPCM the build applies (tools/wav2agb, `-c -l 1 --no-pad`:
                  64-sample blocks, a raw first sample, then 4-bit deltas from
                  {0,1,4,9,16,25,36,49,-64,-49,...,-1} chosen greedily). Returns the
                  encoded .bin payload size and the decoded samples, so loudness,
                  clipping and spectrograms are measured on what the hardware plays.
  loudness        K-weighted (ITU-R BS.1770, the LUFS curve), gated: the mean weighted
                  power of the frames within 15 dB of the loudest, in dB re a full-scale
                  square wave. The gate ignores pauses; the curve's high shelf counts a
                  3 kHz whistle as louder than a 100 Hz boom of the same RMS. (A-weighting
                  was tried first: it penalises bass so hard that booms had to be
                  saturated into buzzes to reach the target.)
  spectrogram     log-frequency (50 Hz..Nyquist) STFT image with a waveform strip.
"""

import cmath
import math
import struct
import zlib

from .dsp import SR, NYQ

DPCM_TABLE = [0, 1, 4, 9, 16, 25, 36, 49, -64, -49, -36, -25, -16, -9, -4, -1]
DPCM_BLOCK = 64


def dpcm_roundtrip(levels):
    """levels: ints -128..127 (the wav's u8 - 128). Returns (payload bytes, decoded)."""
    out = []
    size = 0
    for b in range(0, len(levels), DPCM_BLOCK):
        blk = levels[b:b + DPCM_BLOCK]
        s = blk[0]
        out.append(s)
        size += 1
        for x in blk[1:]:
            best, best_err = 0, None
            for d in DPCM_TABLE:
                lv = s + d
                if lv > 127 or lv < -128:
                    continue
                e = (x - lv) * (x - lv)
                if best_err is None or e < best_err:
                    best, best_err = lv, e
            s = best
            out.append(s)
        size += len(blk) // 2  # first nibble shares the byte after the raw sample
    return size + 16, out      # + the 16-byte wave header


def snr_db(ref, dec):
    sig = sum(v * v for v in ref) or 1
    err = sum((a - b) ** 2 for a, b in zip(ref, dec)) or 1e-9
    return 10 * math.log10(sig / err)


# ---------------------------------------------------------------- FFT

_TW = {}


def fft(x):
    n = len(x)
    if n not in _TW:
        bits = n.bit_length() - 1
        rev = [int(format(i, f"0{bits}b")[::-1], 2) for i in range(n)]
        tw = [cmath.exp(-2j * math.pi * k / n) for k in range(n // 2)]
        _TW[n] = (rev, tw)
    rev, tw = _TW[n]
    a = [complex(x[r]) for r in rev]
    size = 2
    while size <= n:
        half, step = size // 2, n // size
        for start in range(0, n, size):
            for k in range(half):
                w = tw[k * step]
                u, v = a[start + k], a[start + k + half] * w
                a[start + k], a[start + k + half] = u + v, u - v
        size *= 2
    return a


def hann(n):
    return [0.5 - 0.5 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]


def stft(x, size=512, hop=64):
    win = hann(size)
    wsum = sum(win)
    frames = []
    pad = [0.0] * (size // 2)
    xx = pad + list(x) + pad
    for s in range(0, max(1, len(xx) - size + 1), hop):
        seg = xx[s:s + size]
        if len(seg) < size:
            seg = seg + [0.0] * (size - len(seg))
        spec = fft([a * w for a, w in zip(seg, win)])
        frames.append([abs(c) * 2 / wsum for c in spec[:size // 2 + 1]])
    return frames


def k_weight(f):
    """|H(f)| of the ITU-R BS.1770 K-weighting (the LUFS curve): a +4 dB high
    shelf around 1.7 kHz and a 38 Hz high-pass, evaluated on their analogue
    prototypes so it holds at any sample rate."""
    if f <= 0:
        return 0.0
    f0, q = 38.1, 0.5
    hp = f * f / math.sqrt((f0 * f0 - f * f) ** 2 + (f * f0 / q) ** 2)
    a = 10 ** (4.0 / 40)
    s = 1j * f / 1681.0
    sq = math.sqrt(a) / 0.7071
    shelf = a * (a * s * s + sq * s + 1) / (s * s + sq * s + a)
    return hp * abs(shelf)


_KW = {}


def loudness(x, size=512, hop=256):
    """K-weighted gated loudness in dB (x: floats, full scale 1.0)."""
    frames = stft(x, size, hop)
    if size not in _KW:
        _KW[size] = [k_weight(k * SR / size) ** 2 for k in range(size // 2 + 1)]
    wts = _KW[size]
    pw = [sum(m * m * w for m, w in zip(fr, wts)) / 2 for fr in frames]
    top = max(pw) if pw else 0
    if top <= 0:
        return -120.0
    gated = [p for p in pw if p >= top * 10 ** (-15 / 10)]
    return 10 * math.log10(sum(gated) / len(gated))


def dominant_range(x, size=512, hop=128, floor_db=-25):
    """(low, high) of the per-frame spectral peak (Hz) over frames within
    floor_db of the loudest: a measured stand-in for the pitch range."""
    frames = stft(x, size, hop)
    en = [sum(m * m for m in fr) for fr in frames]
    top = max(en) if en else 0
    peaks = []
    for fr, e in zip(frames, en):
        if top and e >= top * 10 ** (floor_db / 10):
            k = max(range(2, len(fr)), key=lambda i: fr[i])
            peaks.append(k * SR / size)
    if not peaks:
        return (0.0, 0.0)
    peaks.sort()
    return peaks[len(peaks) // 20], peaks[-1 - len(peaks) // 20]


# ---------------------------------------------------------------- images

# 3x5 font, rows top to bottom, 3 bits each (MSB = left column).
FONT = {
    "A": "25755", "B": "65656", "C": "34443", "D": "65556", "E": "74647", "F": "74644",
    "G": "34553", "H": "55755", "I": "72227", "J": "11152", "K": "55655", "L": "44447",
    "M": "57755", "N": "65555", "O": "25552", "P": "65644", "Q": "25563", "R": "65655",
    "S": "34216", "T": "72222", "U": "55557", "V": "55552", "W": "55775", "X": "55255",
    "Y": "55222", "Z": "71247", "0": "75557", "1": "26227", "2": "61247", "3": "61216",
    "4": "55711", "5": "74616", "6": "34652", "7": "71122", "8": "25252", "9": "25316",
    " ": "00000", "-": "00700", ".": "00002", ":": "02020", "/": "11244", "_": "00007",
    "(": "12221", ")": "42224", "%": "51245", "+": "02720", "=": "07070", ",": "00024",
    "<": "12421", ">": "42124", "~": "00630", "'": "22000",
}


class Image:
    def __init__(self, w, h, bg=(16, 16, 20)):
        self.w, self.h = w, h
        self.px = [list(bg) * w for _ in range(h)]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            row = self.px[y]
            row[3 * x:3 * x + 3] = c

    def text(self, x, y, s, c=(230, 230, 230), scale=2):
        for ch in s.upper():
            g = FONT.get(ch, FONT[" "])
            for ry, bits in enumerate(g):
                b = int(bits)
                for rx in range(3):
                    if b & (4 >> rx):
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(x + rx * scale + dx, y + ry * scale + dy, c)
            x += 4 * scale
        return x

    def save(self, path):
        raw = b"".join(b"\x00" + bytes(row) for row in self.px)

        def chunk(t, d):
            return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)))
            f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
            f.write(chunk(b"IEND", b""))


STOPS = [(0.0, (0, 0, 4)), (0.25, (60, 10, 100)), (0.5, (180, 40, 90)),
         (0.75, (250, 140, 30)), (1.0, (252, 255, 164))]


def colormap(v):
    v = min(1.0, max(0.0, v))
    for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
        if v <= t1:
            u = (v - t0) / (t1 - t0)
            return tuple(int(a + (b - a) * u) for a, b in zip(c0, c1))
    return STOPS[-1][1]


SPEC_H, WAVE_H, FMIN = 120, 28, 50.0


def draw_cry(img, x0, y0, x, px_per_frame=1, size=512, hop=64, rng_db=66):
    """Draws waveform strip + log-frequency spectrogram of x at (x0, y0).
    Returns the width used."""
    frames = stft(x, size, hop)
    top = max((max(fr) for fr in frames), default=1e-9) or 1e-9
    w = len(frames) * px_per_frame
    # waveform: min/max per column
    per = max(1, len(x) // max(1, w))
    mid = y0 + WAVE_H // 2
    for cx in range(w):
        seg = x[cx * per:(cx + 1) * per] or [0.0]
        lo, hi = min(seg), max(seg)
        for yy in range(int(mid - hi * WAVE_H / 2), int(mid - lo * WAVE_H / 2) + 1):
            img.set(x0 + cx, yy, (120, 200, 160) if max(hi, -lo) < 0.99 else (255, 60, 60))
    ys = y0 + WAVE_H + 2
    lmin, lmax = math.log(FMIN), math.log(NYQ)
    nb = len(frames[0]) if frames else 1
    for row in range(SPEC_H):
        f = math.exp(lmax - (lmax - lmin) * row / (SPEC_H - 1))
        kf = f * size / SR
        k0 = min(nb - 2, int(kf))
        u = kf - k0
        for fi, fr in enumerate(frames):
            m = fr[k0] * (1 - u) + fr[k0 + 1] * u
            db = 20 * math.log10(max(m, 1e-12) / top)
            c = colormap(1 + db / rng_db)
            for dx in range(px_per_frame):
                img.set(x0 + fi * px_per_frame + dx, ys + row, c)
    # guide lines at 100 Hz, 1 kHz, 5 kHz
    for gf in (100, 1000, 5000):
        row = int((lmax - math.log(gf)) / (lmax - lmin) * (SPEC_H - 1))
        for cx in range(-4, 0):
            img.set(x0 + cx, ys + row, (200, 200, 200))
    return w
