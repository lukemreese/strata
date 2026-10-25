"""Call types: the vocal models, built from the dsp primitives.

A `Voice` holds what a species' anatomy implies: fundamental frequency from
mass (F0 ~ M^-0.4 across mammals, Fletcher 2004; compressed per plan so the
whole roster stays inside the GBA's audible band), vocal-tract length ~ M^(1/3)
times a plan factor (long faces, trunks and tracheas resonate lower), the
uniform-tube formants F_n = (2n-1) c / 4L that follow from it, and two seeded
random streams: the lineage motif (shared by every species of a lineage in
src/data/lineages.h: rhythm, contour skew, vibrato rate, brightness) and the
species' own (small pitch/timing offsets), so relatives sound related and no
two species are identical.

Each call function takes the Voice and options and returns a dsp.Track. The
roster's calls are chosen in specs.py.
"""

import math

from . import dsp
from .dsp import Track, curve

C_SOUND = 350.0  # m/s, warm humid air

# Per-plan vocal constants: f0 at 1 kg (Hz), mass exponent, vocal-tract factor.
PLAN_VOICE = {
    "small_mammal":      (1800, 0.30, 1.0),
    "rodent_lagomorph":  (2000, 0.30, 1.0),
    "primate":           (1600, 0.30, 1.0),
    "bat":               (3000, 0.20, 1.0),
    "canid":             (1300, 0.30, 1.2),
    "carnivoran":        (800, 0.35, 1.1),
    "equid":             (1500, 0.30, 1.8),
    "ungulate":          (1200, 0.30, 1.4),
    "hoofed_giant":      (900, 0.30, 1.2),
    "rhino_brontothere": (900, 0.30, 1.2),
    "proboscidean":      (900, 0.30, 2.2),
    "bird_ground":       (1400, 0.30, 1.5),
    "bird_flying":       (2600, 0.20, 1.0),
    "crane_raptor":      (900, 0.25, 3.0),
    "theropod":          (300, 0.12, 1.0),
    "ornithischian":     (300, 0.12, 1.0),
    "croc_champsosaur":  (250, 0.20, 1.0),
    "turtle":            (400, 0.25, 0.8),
    "fish":              (800, 0.20, 1.0),
    "ray":               (800, 0.20, 1.0),
}
F0_LO, F0_HI = 55.0, 3800.0


class Voice:
    def __init__(self, folder, plan, mass, lineage, pitch=1.0):
        self.folder, self.plan, self.mass = folder, plan, mass
        self.rng = dsp.rng_of("cry", folder)
        lr = dsp.rng_of("lineage", lineage)
        self.motif = dict(rhythm=lr.uniform(0.88, 1.12), skew=lr.uniform(0.35, 0.6),
                          vib=lr.uniform(0.85, 1.15), bright=lr.uniform(-4, 4),
                          pitch=lr.uniform(0.94, 1.06))
        self.own_pitch = self.rng.uniform(0.95, 1.05) * pitch
        f1, self.exp, self.tract_k = PLAN_VOICE[plan]
        self.f1 = f1
        self.f0log = []

    # ---- anatomy
    def f0(self, k=1.0):
        f = self.f1 * self.mass ** -self.exp * self.motif["pitch"] * self.own_pitch * k
        return min(F0_HI, max(F0_LO, f))

    def tract(self, k=1.0):
        return min(1.6, max(0.012, self.tract_k * k * 0.045 * self.mass ** (1 / 3)))

    def tube(self, L=None, mult=(1.0, 1.0, 1.0, 1.0), bw=1.0, gains=(1.0, 0.7, 0.45, 0.3), n=4):
        """Uniform-tube formants for tract length L; mult: per-formant multiplier
        (constant or contour) for articulation (mouth opening, rounding)."""
        L = L or self.tract()
        out = []
        for i in range(n):
            base = (2 * i + 1) * C_SOUND / (4 * L)
            m = dsp.fn(mult[i] if i < len(mult) else 1.0)
            f = (lambda t, b=base, m=m: b * m(t))
            b = 40 + 0.08 * base * bw
            out.append((f, b, gains[i] if i < len(gains) else 0.2))
        return out

    def dscale(self, k=1.0):
        """Calls of big animals last longer."""
        return k * min(1.35, max(0.7, 1.0 + 0.09 * math.log10(self.mass)))

    def gap(self, sec):
        return sec * self.motif["rhythm"] * self.rng.uniform(0.92, 1.08)

    def skew(self):
        return self.motif["skew"]

    # ---- primitives with this voice's streams
    def voiced(self, dur, f0, form=(), **kw):
        kw.setdefault("bright", 34)
        kw["bright"] += self.motif["bright"]
        if "vib" in kw:
            kw["vib"] = (kw["vib"][0] * self.motif["vib"], kw["vib"][1])
        return dsp.voiced(dur, f0, form, rng=self.rng, log=self.f0log, **kw)

    def tone(self, dur, f, harmonics=(1.0,), **kw):
        if "vib" in kw:
            kw["vib"] = (kw["vib"][0] * self.motif["vib"], kw["vib"][1])
        return dsp.tone(dur, f, harmonics, rng=self.rng, log=self.f0log, **kw)

    def noise(self, dur, bands, **kw):
        return dsp.noise(dur, bands, rng=self.rng, **kw)

    def click(self, freq, decay, **kw):
        return dsp.click(freq, decay, rng=self.rng, **kw)

    def u(self, a, b):
        return self.rng.uniform(a, b)


def rise_fall(lo, hi, end, skew, log=True):
    return curve((0.0, lo), (skew, hi), (1.0, end), log=log)


# ================================================================ mammals

def squeak(v, n=3, k=1.0, dur=0.07, gap=0.05, sweep=(0.8, 1.2, 0.85), noise=0.08, h2=0.25):
    """Short tonal FM chirps: shrews, mice, multituberculates, small rodents."""
    t = Track(1.0)
    at = 0.0
    f = v.f0(k)
    for i in range(n):
        fi = f * v.u(0.92, 1.08) * (1 - 0.04 * i)
        d = dur * v.u(0.85, 1.15)
        c = rise_fall(fi * sweep[0], fi * sweep[1], fi * sweep[2], v.skew())
        t.add(at, v.tone(d, c, (1.0, h2, h2 * 0.3), attack=0.006, release=0.02,
                         env=curve((0, 0.6), (0.3, 1), (1, 0.5))), 1 - 0.1 * i)
        if noise:
            t.add(at, v.noise(d * 0.6, [(min(5500, fi * 1.5), 1500, 1.0)], release=0.02), noise)
        at += d + v.gap(gap)
    return t.trim()


def chitter(v, n=9, k=1.0, rate=16.0, dur=0.028):
    """Rapid irregular squeak/click train: chattering rodents, primates, ferrets."""
    t = Track(1.0)
    f = v.f0(k)
    at = 0.0
    for i in range(n):
        fi = f * v.u(0.8, 1.2)
        c = curve((0, fi * 1.1), (1, fi * 0.8), log=True)
        t.add(at, v.tone(dur * v.u(0.8, 1.3), c, (1.0, 0.3), attack=0.003, release=0.01), v.u(0.6, 1.0))
        t.add(at, v.click(min(5200, fi * 1.7), 0.002, noise_amt=0.8), 0.25)
        at += v.gap(1 / rate) * v.u(0.75, 1.3)
    return t.trim()


def twitter(v, n=7, k=1.0, rate=13.0, dur=0.055, drop=0.25):
    """Descending trill of whistled FM notes: tiny primates (tarsier/marmoset-like)."""
    t = Track(1.2)
    f = v.f0(k)
    at = 0.0
    for i in range(n):
        fi = f * (1 - drop * i / max(1, n - 1)) * v.u(0.96, 1.04)
        c = curve((0, fi * 0.85), (0.35, fi * 1.15), (1, fi * 0.9), log=True)
        t.add(at, v.tone(dur, c, (1.0, 0.2, 0.05), attack=0.005, release=0.02), 1 - 0.05 * i)
        at += v.gap(1 / rate)
    return t.trim()


def wail(v, k=1.0, dur=0.6, L=1.0):
    """Tonal rise-fall with harmonics and vibrato: lemur-like adapiform call."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = rise_fall(f * 0.75, f * 1.15, f * 0.6, v.skew())
    form = v.tube(v.tract(L), mult=(curve((0, 0.6), (0.4, 1.2), (1, 0.8)), 1.0, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=30, vib=(6.0, 0.35), jitter=0.01, breath=0.04,
                      env=curve((0, 0.5), (0.3, 1), (1, 0.6)), direct=0.25))
    return t.trim()


def yip(v, n=3, k=1.6, dur=0.09, gap=0.09, L=1.0):
    """Short rising-falling voiced yelps: small canids, the coyote's opening."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.93, 1.07) * (1 + 0.05 * i)
        c = rise_fall(f * 0.8, f * 1.25, f * 0.85, v.skew())
        form = v.tube(v.tract(L), mult=(1.15, 1.25, 1.0))
        t.add(at, v.voiced(dur * v.u(0.85, 1.15), c, form, bright=30, breath=0.06, jitter=0.015,
                           attack=0.008, release=0.03, direct=0.2), 1 - 0.08 * i)
        at += dur + v.gap(gap)
    return t.trim()


def howl(v, k=1.0, dur=0.9, L=1.0):
    """Long tonal howl: rise, plateau with vibrato, fall; rounded 'oo' mouth."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = curve((0, f * 0.62), (0.25, f), (0.6, f * 1.1), (1, f * 0.58), log=True)
    form = v.tube(v.tract(L), mult=(curve((0, 0.55), (0.5, 0.85), (1, 0.6)), 0.75, 0.9))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=40, vib=(5.0, 0.45), jitter=0.006, breath=0.05,
                      attack=0.08, release=0.18, env=curve((0, 0.6), (0.3, 1), (0.8, 0.9), (1, 0.5)),
                      direct=0.3))
    return t.trim()


def bark(v, n=2, k=0.8, dur=0.13, gap=0.12, L=1.0, rough=0.3):
    """Short harsh voiced bursts with a fast pitch drop."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.94, 1.06)
        c = curve((0, f * 1.2), (0.25, f), (1, f * 0.7), log=True)
        form = v.tube(v.tract(L), mult=(curve((0, 0.8), (0.3, 1.35), (1, 1.0)), 1.1, 1.0))
        t.add(at, v.voiced(dur * v.u(0.9, 1.1), c, form, bright=26, sub=rough, jitter=0.04, breath=0.18,
                           attack=0.004, release=0.05, env=curve((0, 1), (1, 0.4)), direct=0.15), 1 - 0.12 * i)
        at += dur + v.gap(gap)
    return t.trim()


def whoop(v, k=0.9, dur=0.7, L=1.0):
    """Rising whoop (spotted-hyena-like), used for the hyena-like borophagine."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = curve((0, f * 0.55), (0.75, f * 1.35), (1, f * 1.2), log=True)
    form = v.tube(v.tract(L), mult=(0.65, 0.75, 0.9))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=36, vib=(4.0, 0.2), jitter=0.01, breath=0.06,
                      attack=0.05, release=0.12, env=curve((0, 0.5), (0.6, 1), (1, 0.7)), direct=0.25))
    return t.trim()


def growl(v, k=0.6, dur=0.7, L=1.0, pulse=28.0, hiss_amt=0.0, opening=1.0):
    """Low rough growl: period doubling, pulsing amplitude, breath."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = rise_fall(f * 0.9, f * 1.1, f * 0.85, v.skew())
    form = v.tube(v.tract(L), mult=(curve((0, 0.7), (0.5, 0.95 * opening), (1, 0.8)), 1.0, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=28, sub=0.6, am=(pulse, 0.55), jitter=0.06, shimmer=0.2,
                      breath=0.2, attack=0.06, release=0.12, env=curve((0, 0.5), (0.5, 1), (1, 0.7)),
                      direct=0.15))
    if hiss_amt:
        t.add(0.05, hiss(v, dur=d * 0.8).x, hiss_amt)
    return t.trim()


def roar(v, k=1.0, dur=0.95, L=1.3, grunts=2):
    """Big-cat roar: crescendo, falling pitch, wide-open mouth, then grunts."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = curve((0, f * 0.8), (0.25, f), (1, f * 0.55), log=True)
    form = v.tube(v.tract(L), mult=(curve((0, 0.6), (0.35, 1.3), (1, 0.9)), 1.1, 1.0, 1.0))
    t = Track(d + 0.6)
    end = t.add(0, v.voiced(d, c, form, bright=24, sub=0.35, jitter=0.05, shimmer=0.1, breath=0.16,
                            attack=0.07, release=0.2, env=curve((0, 0.35), (0.3, 1), (1, 0.45)), direct=0.12))
    for i in range(grunts):
        g = grunt(v, n=1, k=k * 0.7, dur=0.16, L=L).x
        end = t.add(end + v.gap(0.06), g, 0.6 - 0.15 * i)
    return t.trim()


def grunt(v, n=3, k=0.7, dur=0.15, gap=0.12, L=1.0, decay=0.15):
    """Short low voiced grunts with a falling pitch (pigs, bears, oreodonts, tortoises)."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.92, 1.08)
        c = curve((0, f * 1.1), (1, f * 0.8), log=True)
        form = v.tube(v.tract(L), mult=(0.85, 0.95, 1.0))
        t.add(at, v.voiced(dur * v.u(0.85, 1.15), c, form, bright=28, sub=0.4, jitter=0.05, breath=0.25,
                           attack=0.01, release=0.06, env=curve((0, 1), (1, 0.45)), direct=0.15),
              1 - decay * i)
        at += dur + v.gap(gap) * v.u(0.8, 1.25)
    return t.trim()


def hiss(v, dur=0.4, centre=3600.0, bw=3200.0, attack=0.02, low=0.35):
    """Breath forced through a constriction: filtered noise."""
    t = Track(dur)
    t.add(0, v.noise(dur, [(centre, bw, 1.0), (centre * 0.45, bw * 0.35, low)], attack=attack,
                     release=dur * 0.5, env=curve((0, 1), (0.4, 0.85), (1, 0.3))))
    return t.trim()


def chirp(v, n=2, k=2.2, dur=0.11, gap=0.09):
    """Cheetah/puma-style chirp: a bird-like voiced upward sweep."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.95, 1.05)
        c = curve((0, f * 0.7), (0.6, f * 1.2), (1, f * 0.95), log=True)
        t.add(at, v.tone(dur, c, (1.0, 0.45, 0.2, 0.08), attack=0.008, release=0.03,
                         env=curve((0, 0.7), (0.5, 1), (1, 0.6))), 1 - 0.1 * i)
        at += dur + v.gap(gap)
    return t.trim()


def dook(v, n=7, k=1.0, rate=9.0, dur=0.045):
    """Ferret 'dooking': a soft rapid cluck series."""
    t = Track(1.2)
    at = 0.0
    f = v.f0(k)
    for i in range(n):
        fi = f * v.u(0.9, 1.1)
        form = v.tube(mult=(1.0, 1.0))
        t.add(at, v.voiced(dur, curve((0, fi * 1.1), (1, fi * 0.85), log=True), form, bright=26,
                           breath=0.1, attack=0.004, release=0.02, direct=0.3), v.u(0.7, 1.0))
        at += v.gap(1 / rate) * v.u(0.85, 1.2)
    return t.trim()


def huff(v, n=2, dur=0.18, gap=0.1, centre=650.0):
    """Explosive exhalations through the nose: bears, rhinos."""
    t = Track(1.0)
    at = 0.0
    c = centre * (v.mass / 500) ** -0.12
    for i in range(n):
        t.add(at, v.noise(dur, [(c, c * 0.9, 1.0), (c * 2.6, c * 1.5, 0.5)], attack=0.008,
                          release=dur * 0.7, env=curve((0, 1), (1, 0.2)), am=(32, 0.35)), 1 - 0.15 * i)
        at += dur + v.gap(gap)
    return t.trim()


def jaw_pop(v, n=2, freq=420.0, gap=0.12):
    """Jaw or tooth clacks (bears, snapping turtles, crocodylians)."""
    t = Track(0.5)
    at = 0.0
    for i in range(n):
        t.add(at, v.click(freq * v.u(0.9, 1.1), 0.012, noise_amt=0.9, dur=0.06), 1 - 0.2 * i)
        at += v.gap(gap)
    return t.trim()


def whinny(v, k=1.0, dur=1.0, L=1.0, tremolo=11.0):
    """Horse whinny: biphonation (Briefer et al. 2015): a high fundamental (F0)
    with fast tremolo over a lower, independent one (G0), the whole call falling."""
    d = v.dscale(dur)
    g0 = v.f0(k)
    f0 = g0 * 2.7
    sk = v.skew() * 0.4
    hi = curve((0, f0 * 0.8), (sk, f0 * 1.15), (0.6, f0 * 0.82), (1, f0 * 0.5), log=True)
    lo = curve((0, g0 * 0.9), (sk + 0.1, g0 * 1.05), (1, g0 * 0.75), log=True)
    form = v.tube(v.tract(L), mult=(1.3, 1.2, 1.0, 1.0))
    t = Track(d)
    env = curve((0, 0.6), (sk + 0.05, 1), (0.7, 0.8), (1, 0.4))
    t.add(0, v.voiced(d, hi, form, bright=34, vib=(tremolo, 1.2), am=(tremolo, 0.35), jitter=0.01,
                      attack=0.03, release=0.15, env=env, direct=0.35), 0.8)
    t.add(0.02, v.voiced(d * 0.95, lo, form, bright=30, jitter=0.02, breath=0.12, attack=0.04,
                         release=0.2, env=env, direct=0.2), 0.55)
    return t.trim()


def nicker(v, k=0.55, dur=0.45, pulses=9.0, L=1.0):
    """Low pulsed nicker, mouth closed."""
    d = v.dscale(dur)
    f = v.f0(k)
    form = v.tube(v.tract(L), mult=(0.6, 0.8, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, curve((0, f * 1.05), (1, f * 0.85), log=True), form, bright=34, am=(pulses, 0.9),
                      breath=0.15, jitter=0.03, attack=0.03, release=0.1, direct=0.2))
    return t.trim()


def snort(v, dur=0.28, centre=700.0, flutter=30.0):
    """Air blown through the nostrils, flapping: equids, bovids, rhinos."""
    c = centre * (v.mass / 300) ** -0.12
    t = Track(dur)
    t.add(0, v.noise(dur, [(c, c * 0.8, 1.0), (c * 2.8, c * 1.6, 0.5), (4200, 2500, 0.15)], attack=0.01,
                     release=dur * 0.6, env=curve((0, 1), (0.3, 0.8), (1, 0.15)), am=(flutter, 0.6)))
    return t.trim()


def bleat(v, k=1.0, dur=0.65, L=1.0, trem=7.5, depth=0.5):
    """'Baa': the mouth opens, then a tremulous (vibrato + tremolo) falling note."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = curve((0, f * 0.95), (0.2, f * 1.08), (1, f * 0.82), log=True)
    form = v.tube(v.tract(L), mult=(curve((0, 0.45), (0.15, 1.2), (1, 1.0)), 1.05, 1.0, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=30, vib=(trem, 0.6), am=(trem, depth), jitter=0.03, breath=0.1,
                      attack=0.02, release=0.12, env=curve((0, 0.7), (0.15, 1), (1, 0.6)), direct=0.2))
    return t.trim()


def hum(v, k=1.0, dur=0.7, L=1.0, rise=1.12):
    """Closed-mouth hum (llamas and alpacas hum): low first formant, near-pure tone."""
    d = v.dscale(dur)
    f = v.f0(k)
    form = v.tube(v.tract(L), mult=(0.45, 0.6, 0.9), gains=(1.0, 0.4, 0.15))
    t = Track(d)
    t.add(0, v.voiced(d, curve((0, f), (0.6, f * rise), (1, f * rise * 0.95), log=True), form, bright=44,
                      am=(3.0, 0.2), breath=0.03, jitter=0.008, attack=0.06, release=0.15, direct=0.35))
    return t.trim()


def groan(v, k=0.55, dur=0.9, L=1.0, gurgle=12):
    """Camel groan: low, rough, with gurgling bubbles from the throat."""
    d = v.dscale(dur)
    f = v.f0(k)
    form = v.tube(v.tract(L), mult=(curve((0, 0.6), (0.5, 1.1), (1, 0.7)), 1.0, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, rise_fall(f * 0.9, f * 1.1, f * 0.8, v.skew()), form, bright=28, sub=0.5,
                      am=(8.0, 0.4), jitter=0.08, shimmer=0.25, breath=0.2, attack=0.05, release=0.15,
                      env=curve((0, 0.6), (0.4, 1), (1, 0.6)), direct=0.12))
    for _ in range(gurgle):
        t.add(v.u(0.05, d - 0.08), v.click(v.u(220, 520), 0.01, noise_amt=0.3, chirp=0.6), 0.35)
    return t.trim()


def bellow(v, k=0.8, dur=1.05, L=1.0, rough=0.45):
    """Bull bellow: low rough voice, mouth opening, crescendo then fade."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = curve((0, f * 0.85), (0.3, f * 1.05), (0.8, f * 0.95), (1, f * 0.7), log=True)
    form = v.tube(v.tract(L), mult=(curve((0, 0.6), (0.35, 1.15), (1, 0.75)), 1.05, 1.0, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=27, sub=rough, jitter=0.05, shimmer=0.12, breath=0.2,
                      attack=0.06, release=0.2, env=curve((0, 0.4), (0.35, 1), (1, 0.5)), direct=0.12))
    return t.trim()


def trumpet(v, k=1.0, dur=0.75, L=1.0):
    """Elephant trumpet: forced through the trunk; brassy, noisy, fluttering."""
    d = v.dscale(dur) * 0.75
    f = 420 * v.motif["pitch"] * v.own_pitch * k
    c = curve((0, f * 0.8), (0.1, f), (0.8, f * 1.06), (1, f * 0.85), log=True)
    form = v.tube(v.tract(L) * 0.35, mult=(1.0, 1.0, 1.0, 1.0), gains=(1.0, 0.9, 0.7, 0.5))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=16, sub=0.25, am=(38, 0.25), jitter=0.04, breath=0.3,
                      breath_band=(1800, 2400), attack=0.02, release=0.12, direct=0.25))
    return t.trim()


def rumble(v, k=1.0, dur=0.6, L=1.0, f=None):
    """Low rumble. Real proboscidean rumbles are largely infrasonic; this keeps the
    fundamental at the audible floor (55 Hz+) and lets formants carry the size."""
    d = v.dscale(dur)
    f = f or max(58.0, v.f0(k))
    form = v.tube(v.tract(L), mult=(1.0, 1.0, 1.0, 1.0), gains=(1.0, 0.8, 0.6, 0.4))
    t = Track(d)
    t.add(0, v.voiced(d, curve((0, f * 0.95), (0.5, f * 1.05), (1, f * 0.9), log=True), form, bright=34,
                      sub=0.3, am=(4.0, 0.3), jitter=0.03, breath=0.1, breath_band=(400, 500),
                      attack=0.12, release=0.2, direct=0.3))
    return t.trim()


def echo(v, n=7, f_hi=4300.0, f_lo=1700.0, sweep=0.014, start_gap=0.09, end_gap=0.025):
    """Bat FM sweeps, slowed ~10x into the audible band, speeding up like a
    feeding buzz. (Whether Onychonycteris echolocated is debated; see specs.)"""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        u = i / max(1, n - 1)
        c = curve((0, f_hi), (1, f_lo), log=True)
        t.add(at, v.tone(sweep * (1.2 - 0.4 * u), c, (1.0, 0.15), attack=0.002, release=0.006), 0.7 + 0.3 * u)
        at += start_gap + (end_gap - start_gap) * u
    return t.trim()


# ================================================================ birds

def peep(v, n=3, k=1.4, dur=0.09, gap=0.07, drop=0.75):
    """Chick peeps: pure descending whistles."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.95, 1.05)
        c = curve((0, f * 1.12), (0.3, f * 1.05), (1, f * drop), log=True)
        t.add(at, v.tone(dur * v.u(0.9, 1.1), c, (1.0, 0.12), attack=0.006, release=0.025,
                         env=curve((0, 0.8), (0.3, 1), (1, 0.6))), 1 - 0.08 * i)
        at += dur + v.gap(gap)
    return t.trim()


def cluck(v, n=3, k=0.7, dur=0.07, gap=0.11, L=1.0):
    """Galliform cluck: abrupt bright voiced 'bok' with a click onset."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.93, 1.07)
        form = v.tube(v.tract(L), mult=(curve((0, 1.4), (1, 0.9)), 1.1, 1.0))
        t.add(at, v.voiced(dur * v.u(0.85, 1.2), curve((0, f * 1.15), (1, f * 0.85), log=True), form,
                           bright=24, breath=0.08, attack=0.003, release=0.03, env=curve((0, 1), (1, 0.35)),
                           direct=0.25), 1 - 0.1 * i)
        t.add(at, v.click(min(3000, f * 3), 0.003, noise_amt=0.6), 0.25)
        at += dur + v.gap(gap) * v.u(0.85, 1.2)
    return t.trim()


def gobble(v, k=0.6, dur=0.75, rate=32.0, L=1.0):
    """Turkey gobble: a fast amplitude-fluttered descending call."""
    d = v.dscale(dur)
    f = v.f0(k)
    c = curve((0, f * 1.25), (0.15, f * 1.3), (1, f * 0.7), log=True)
    form = v.tube(v.tract(L), mult=(1.2, 1.1, 1.0))
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=26, am=(rate, 0.85), vib=(rate, 0.8), jitter=0.04, breath=0.1,
                      attack=0.01, release=0.15, env=curve((0, 1), (0.6, 0.85), (1, 0.4)), direct=0.25))
    return t.trim()


def strut(v, k=1.0):
    """Sage-grouse strut: two soft coos, a wing swish, then the air-sac
    pop - whistle - pop."""
    t = Track(1.4)
    f = v.f0(0.28 * k)
    at = 0.0
    for i in range(2):
        at = t.add(at, v.tone(0.11, curve((0, f), (1, f * 0.9), log=True), (1.0, 0.3, 0.1), attack=0.02,
                              release=0.04), 0.5) + v.gap(0.05)
    at = t.add(at, v.noise(0.12, [(2600, 3000, 1.0)], attack=0.03, release=0.06), 0.35) + v.gap(0.04)
    t.add(at, v.click(330, 0.018, noise_amt=0.5, dur=0.09), 1.0)
    t.add(at + 0.07, v.tone(0.16, curve((0, 1500 * k), (0.5, 2100 * k), (1, 1700 * k), log=True), (1.0, 0.1),
                            attack=0.01, release=0.05), 0.45)
    t.add(at + 0.25, v.click(300, 0.02, noise_amt=0.5, dur=0.1), 1.0)
    return t.trim()


def boom(v, n=1, k=1.0, dur=0.55, gap=0.15, L=1.0, f=None, depth=0.25):
    """Closed-mouth boom (crocodylians, ostriches, cassowaries, pigeons; the
    cautious reconstruction for non-avian dinosaurs, Riede et al. 2016): a
    near-sinusoidal low voice resonating in an inflated throat or air sac."""
    t = Track(2.0)
    at = 0.0
    for i in range(n):
        fi = (f or v.f0(k)) * v.u(0.96, 1.04) * (1 - 0.05 * i)
        d = v.dscale(dur) * v.u(0.9, 1.1)
        c = curve((0, fi * 0.92), (0.3, fi * 1.03), (1, fi * 0.88), log=True)
        sac = [(fi * 2.0, fi * 0.8, 1.0), (fi * 3.1, fi * 1.2, 0.7), (fi * 5.0, fi * 2.0, 0.4), (fi * 7.5, fi * 3.0, 0.2)]
        t.add(at, v.voiced(d, c, sac, bright=46, am=(3.5, depth), jitter=0.015, attack=0.09, release=0.18,
                           env=curve((0, 0.6), (0.35, 1), (1, 0.6)), direct=0.5), 1 - 0.15 * i)
        at += d + v.gap(gap)
    return t.trim()


def quack(v, n=2, k=1.0, dur=0.17, gap=0.08):
    """Duck quack: nasal, buzzy, sharply decaying."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * v.u(0.95, 1.05)
        form = [(950, 160, 1.0), (1700, 220, 0.8), (2700, 300, 0.4)]
        t.add(at, v.voiced(dur * v.u(0.9, 1.1), curve((0, f * 1.05), (1, f * 0.85), log=True), form,
                           bright=16, sub=0.2, jitter=0.03, breath=0.05, attack=0.006, release=0.05,
                           env=curve((0, 1), (1, 0.3)), direct=0.1), 1 - 0.12 * i)
        at += dur + v.gap(gap)
    return t.trim()


def bugle(v, k=1.0, L=1.0):
    """Crane bugle 'ga-roo': a short low note jumping to a long high one, rich
    in closely spaced formants from the long coiled trachea."""
    f = v.f0(k)
    form = v.tube(v.tract(L), n=4, gains=(1.0, 0.9, 0.8, 0.6))
    t = Track(1.2)
    a = t.add(0, v.voiced(0.13, curve((0, f * 0.9), (1, f), log=True), form, bright=24, sub=0.35,
                          jitter=0.03, attack=0.01, release=0.03, direct=0.3), 0.8)
    t.add(a + 0.01, v.voiced(v.dscale(0.42), curve((0, f * 1.45), (0.3, f * 1.6), (1, f * 1.3), log=True),
                             form, bright=24, vib=(9, 0.25), jitter=0.02, attack=0.015, release=0.1,
                             env=curve((0, 1), (1, 0.6)), direct=0.3))
    return t.trim()


def trill(v, n=9, k=1.0, rate=17.0, dur=0.04, voices=2):
    """Songbird-like syrinx trill: FM notes from two independent voices."""
    t = Track(1.2)
    f = v.f0(k)
    at = 0.0
    for i in range(n):
        fi = f * (1 + 0.15 * math.sin(i * 1.3)) * v.u(0.97, 1.03)
        c = curve((0, fi * 1.2), (1, fi * 0.8), log=True)
        t.add(at, v.tone(dur, c, (1.0, 0.1), attack=0.004, release=0.012), 0.8)
        if voices > 1:
            c2 = curve((0, fi * 0.7), (1, fi * 0.78), log=True)
            t.add(at, v.tone(dur, c2, (1.0,), attack=0.004, release=0.012), 0.35)
        at += v.gap(1 / rate)
    return t.trim()


def whistle(v, k=1.0, dur=0.3, shape=(0.9, 1.1, 0.95)):
    t = Track(dur)
    f = v.f0(k)
    t.add(0, v.tone(dur, rise_fall(f * shape[0], f * shape[1], f * shape[2], v.skew()), (1.0, 0.1),
                    attack=0.01, release=0.05, vib=(20, 0.15)))
    return t.trim()


# ================================================================ reptiles, archosaurs

def honk(v, k=1.0, dur=0.7, L=1.0, nasal=1.0):
    """Hadrosaur honk: low voice through long nasal passages (a resonating
    tube read off the skull; Weishampel 1981 for crested relatives)."""
    d = v.dscale(dur)
    f = v.f0(k)
    Ln = min(1.6, 0.9 * nasal)
    form = v.tube(Ln, n=4, gains=(1.0, 0.9, 0.7, 0.5), bw=0.6)
    c = curve((0, f * 0.9), (0.15, f * 1.05), (1, f * 0.85), log=True)
    t = Track(d)
    t.add(0, v.voiced(d, c, form, bright=30, jitter=0.02, breath=0.05, breath_band=(600, 600),
                      attack=0.05, release=0.18, env=curve((0, 0.7), (0.2, 1), (1, 0.6)), direct=0.25))
    return t.trim()


def hoot(v, n=2, k=1.0, dur=0.22, gap=0.12):
    """Closed-mouth coo/hoot (doves, tinamous): soft, near-pure."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        f = v.f0(k) * (1 - 0.06 * i)
        t.add(at, v.tone(dur, curve((0, f * 0.95), (0.4, f * 1.05), (1, f * 0.9), log=True), (1.0, 0.35, 0.12),
                         attack=0.04, release=0.08), 1 - 0.15 * i)
        at += dur + v.gap(gap)
    return t.trim()


def knock(v, n=2, freq=900.0, gap=0.1):
    """Hard clack (skull-dome knock: a non-vocal sound)."""
    t = Track(0.5)
    at = 0.0
    for i in range(n):
        t.add(at, v.click(freq * v.u(0.92, 1.08), 0.008, noise_amt=1.0, dur=0.05), 1 - 0.25 * i)
        t.add(at, v.click(freq * 0.37, 0.02, noise_amt=0.0, dur=0.08), 0.5)
        at += v.gap(gap)
    return t.trim()


# ================================================================ fish

def ticks(v, n=22, f=2400.0, r0=28.0, r1=70.0):
    """Herring 'FRT' (fast repetitive tick): bursts of ticks from air released
    by the swim bladder through the anal duct (Wilson et al. 2004)."""
    t = Track(1.0)
    at = 0.0
    for i in range(n):
        u = i / max(1, n - 1)
        t.add(at, v.click(f * v.u(0.8, 1.2), 0.002, noise_amt=0.7, dur=0.01), v.u(0.5, 1.0))
        at += 1 / (r0 + (r1 - r0) * u) * v.u(0.85, 1.15)
    t.add(at + 0.03, bubble(v, 900).x, 0.5)
    return t.trim()


def bubble(v, f=800.0):
    t = Track(0.06)
    t.add(0, v.click(f * v.u(0.85, 1.15), 0.012, noise_amt=0.1, chirp=0.35, dur=0.05))
    return t


def gulp(v, bubbles=4):
    """Gar air gulp at the surface: a low thump, then rising bubbles."""
    t = Track(0.8)
    t.add(0, v.click(130, 0.035, noise_amt=0.3, dur=0.16), 1.0)
    t.add(0.0, v.noise(0.12, [(500, 600, 1.0)], attack=0.005, release=0.08), 0.4)
    at = 0.12
    for _ in range(bubbles):
        t.add(at, bubble(v, v.u(450, 1100)).x, v.u(0.5, 0.8))
        at += v.gap(0.07) * v.u(0.7, 1.4)
    return t.trim()


def splash(v, bubbles=5):
    """Surfacing splash and bubbles (rays make no vocal sound)."""
    t = Track(0.9)
    t.add(0, v.noise(0.3, [(1800, 3000, 1.0), (500, 500, 0.5)], attack=0.004, release=0.2,
                     env=curve((0, 1), (0.2, 0.5), (1, 0.1))), 0.8)
    at = 0.18
    for _ in range(bubbles):
        t.add(at, bubble(v, v.u(600, 1600)).x, v.u(0.4, 0.7))
        at += v.gap(0.06) * v.u(0.6, 1.5)
    return t.trim()


CALLS = {f.__name__: f for f in [
    squeak, chitter, twitter, wail, yip, howl, bark, whoop, growl, roar, grunt, hiss, chirp, dook, huff,
    jaw_pop, whinny, nicker, snort, bleat, hum, groan, bellow, trumpet, rumble, echo, peep, cluck, gobble,
    strut, boom, quack, bugle, trill, whistle, honk, hoot, knock, ticks, gulp, splash,
]}
