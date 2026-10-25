#!/usr/bin/env python3
"""Generate original creature cries. Thin CLI over tools/strata/cries/.

Usage (from the repo root):
    python3 tools/strata/gen_cry.py [<folder> ...]   those species (default: every species)
    python3 tools/strata/gen_cry.py --check          re-render everything in memory and compare
                                                     with the wavs on disk (exit 1 if any differ)
    python3 tools/strata/gen_cry.py --report DIR     listening proxies: one spectrogram PNG per
                                                     artist lane, cries_summary.txt (duration, f0,
                                                     peak, clipping, DC, loudness, DPCM SNR, size),
                                                     the closest-sounding pairs, stock loudness for
                                                     calibration, and a byte check against wav2agb

Writes sound/direct_sound_samples/cries/strata_<folder>.wav (8-bit mono 13379 Hz,
the mixer rate) and the marker list strata_cries.txt that tells gen_species.py
not to copy the `borrow=` stock cry. Run gen_species.py afterwards, then make.
Docs: docs/strata_art.md, "Cries".
"""

import glob
import math
import os
import subprocess
import sys
import tempfile
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cries import analysis, build, dsp, manifest  # noqa: E402
from cries.specs import CRIES  # noqa: E402
from sprites.taxonomy import LANES, SPECIES_PLAN  # noqa: E402
import sprites  # noqa: E402


def roster():
    return sprites.roster()


def render_all(names, roster_by):
    root_of = build.lineages()
    out = {}
    for f in names:
        sp = roster_by[f]
        levels, voice = build.render(f, sp["mass"], SPECIES_PLAN[f], root_of(f))
        out[f] = (levels, voice, build.wav_bytes(levels))
    return out


def cmd_generate(names, ros):
    by = {sp["folder"]: sp for sp in ros}
    bad = [n for n in names if n not in by]
    if bad:
        sys.exit(f"gen_cry: not roster species: {', '.join(bad)}")
    missing = [sp["folder"] for sp in ros if sp["folder"] not in CRIES]
    extra = [f for f in CRIES if f not in by]
    if missing or extra:
        sys.exit(f"gen_cry: specs.py out of step with the roster: missing {missing}, extra {extra}")
    entries = manifest.read()
    for f, (levels, _, data) in render_all(names, by).items():
        path = manifest.wav_path(f)
        with open(path, "wb") as fh:
            fh.write(data)
        entries[f] = (manifest.sha1(path), SPECIES_PLAN[f], len(levels) / dsp.SR)
        print(f"{f:<13} {len(levels) / dsp.SR:.2f} s  {SPECIES_PLAN[f]}")
    manifest.write(entries, [sp["folder"] for sp in ros])
    own, borrowed, _ = manifest.status([sp["folder"] for sp in ros])
    print(f"original cries: {len(own)}/{len(ros)}, borrowed stock cries: {len(borrowed)}")


def cmd_check(ros):
    by = {sp["folder"]: sp for sp in ros}
    diff = []
    for f, (_, _, data) in render_all([sp["folder"] for sp in ros], by).items():
        path = manifest.wav_path(f)
        if not os.path.exists(path) or open(path, "rb").read() != data:
            diff.append(f)
    print(f"gen_cry --check: {len(ros) - len(diff)}/{len(ros)} byte-identical" +
          (f"; differ: {', '.join(diff)}" if diff else ""))
    return 1 if diff else 0


def decode_bin(path):
    """Decodes following wav2agb's write order exactly: per 64-sample block one raw
    byte, one byte holding sample 1 in its low nibble, then high/low nibble pairs."""
    data = open(path, "rb").read()
    n = int.from_bytes(data[12:16], "little")
    p, out = 16, []
    tab = analysis.DPCM_TABLE
    while len(out) < n and p < len(data):
        blk = min(64, n - len(out))
        s = data[p] - 256 if data[p] > 127 else data[p]
        p += 1
        out.append(s)
        if blk > 1:
            s += tab[data[p] & 0xF]
            out.append(s)
            p += 1
        k = 2
        while k < blk:
            b = data[p] if p < len(data) else 0
            s += tab[b >> 4]
            out.append(s)
            k += 1
            if k < blk:
                s += tab[b & 0xF]
                out.append(s)
                k += 1
                p += 1
            else:
                break
    return len(data), out[:n]


def features(dec):
    x = [v / 128 for v in dec]
    frames = analysis.stft(x, 512, 128)
    en = [sum(m * m for m in fr) for fr in frames]
    top = max(en) or 1
    act = [fr for fr, e in zip(frames, en) if e > top * 0.01] or frames
    edges = [60 * (6600 / 60) ** (i / 20) for i in range(21)]
    bands = []
    for lo, hi in zip(edges, edges[1:]):
        k0, k1 = int(lo * 512 / dsp.SR), max(int(lo * 512 / dsp.SR) + 1, int(hi * 512 / dsp.SR))
        p = sum(sum(fr[k] ** 2 for k in range(k0, min(k1, 257))) for fr in act) / len(act)
        bands.append(10 * math.log10(p + 1e-12))
    mx = max(bands)
    bands = [max(-40.0, b - mx) / 10 for b in bands]
    seg = [math.sqrt(sum(e for e in en[int(i * len(en) / 10):int((i + 1) * len(en) / 10)] or [0]) / top)
           for i in range(10)]
    return bands + [s * 2 for s in seg] + [len(dec) / dsp.SR * 3]


def stock_loudness(limit=80):
    files = sorted(f for f in glob.glob(os.path.join(manifest.CRY_DIR, "*.wav"))
                   if not os.path.basename(f).startswith(("strata_", "uncomp_")))
    vals = []
    for path in files[::max(1, len(files) // limit)]:
        try:
            w = wave.open(path)
            if w.getsampwidth() != 1 or w.getnchannels() != 1:
                continue
            raw = w.readframes(w.getnframes())
            rate = w.getframerate()
        except (wave.Error, EOFError):
            continue
        x = [(b - 128) / 128 for b in raw]
        if rate != dsp.SR:  # nearest-neighbour resample is fine for a level estimate
            x = [x[min(len(x) - 1, int(i * rate / dsp.SR))] for i in range(int(len(x) * dsp.SR / rate))]
        vals.append(analysis.loudness(x))
    vals.sort()
    return vals


def cmd_report(outdir, ros):
    os.makedirs(outdir, exist_ok=True)
    by = {sp["folder"]: sp for sp in ros}
    names = [sp["folder"] for sp in ros]
    rendered = render_all(names, by)
    root_of = build.lineages()
    wav2agb = os.path.join(build.ROOT, "tools/wav2agb/wav2agb")
    rows, feats, decs = [], {}, {}
    mismatch = []
    total_new = 0
    for f in names:
        levels, voice, data = rendered[f]
        on_disk = os.path.exists(manifest.wav_path(f)) and open(manifest.wav_path(f), "rb").read() == data
        size, dec = analysis.dpcm_roundtrip(levels)
        if os.path.exists(wav2agb):
            with tempfile.TemporaryDirectory() as td:
                wp, bp = os.path.join(td, "c.wav"), os.path.join(td, "c.bin")
                open(wp, "wb").write(data)
                subprocess.run([wav2agb, "-b", "-c", "-l", "1", "--no-pad", wp, bp], check=True,
                               stdout=subprocess.DEVNULL)
                real_size, real = decode_bin(bp)
            if real != dec[:len(real)] or real_size != size:
                mismatch.append(f"{f} (size {real_size} vs {size})")
            size = real_size
        total_new += size
        decs[f] = dec
        x = [v / 128 for v in dec]
        f0s = voice.f0log
        f0lo = min(a for a, _ in f0s) if f0s else 0
        f0hi = max(b for _, b in f0s) if f0s else 0
        dlo, dhi = analysis.dominant_range(x)
        rows.append(dict(
            folder=f, plan=SPECIES_PLAN[f], secs=len(dec) / dsp.SR, f0=(f0lo, f0hi), dom=(dlo, dhi),
            peak=max(abs(v) for v in dec), clip=sum(1 for v in dec if v >= 127 or v <= -128),
            dc=sum(dec) / len(dec) / 128, loud=analysis.loudness(x), snr=analysis.snr_db(levels, dec),
            size=size, same=on_disk, basis=CRIES[f][0].split(":")[0], calls="+".join(c for c, _ in CRIES[f][1]),
            lineage=root_of(f)))
        feats[f] = features(dec)

    # ---- spectrogram sheets, one per lane
    for li, lane in enumerate(LANES):
        members = [r for r in rows if r["plan"] in lane]
        cols = 2
        cw, rh = 380, 12 + analysis.WAVE_H + 2 + analysis.SPEC_H + 10
        img = analysis.Image(cols * cw + 10, 26 + rh * ((len(members) + cols - 1) // cols))
        img.text(6, 6, f"lane {li + 1}: {' + '.join(lane)}   (log freq 50 hz - 6.7 khz, ticks 100/1k/5k)", scale=2)
        for i, r in enumerate(members):
            x0, y0 = 12 + (i % cols) * cw, 26 + (i // cols) * rh
            img.text(x0, y0, f"{r['folder']} {r['calls']} {r['loud']:.1f}db", scale=2)
            analysis.draw_cry(img, x0, y0 + 12, [v / 128 for v in decs[r['folder']]])
        path = os.path.join(outdir, f"cries_lane{li + 1}_{'_'.join(lane)}.png")
        img.save(path)
        print("wrote", path)

    # ---- closest pairs
    def dist(a, b):
        return math.sqrt(sum((p - q) ** 2 for p, q in zip(feats[a], feats[b])))
    pairs = sorted((dist(a, b), a, b) for i, a in enumerate(names) for b in names[i + 1:])
    same_lin = [d for d, a, b in pairs if rows[names.index(a)]["lineage"] == rows[names.index(b)]["lineage"]]
    all_d = [d for d, _, _ in pairs]

    stock = stock_loudness()
    lines = []
    lines.append(f"{'species':<13} {'plan':<17} {'basis':<11} {'sec':>4} {'f0 design Hz':>13} "
                 f"{'peak Hz':>11} {'pk':>4} {'clip':>4} {'dc%':>5} {'loud':>6} {'snr':>5} {'bytes':>6} same  calls")
    for r in rows:
        lines.append(f"{r['folder']:<13} {r['plan']:<17} {r['basis']:<11} {r['secs']:4.2f} "
                     f"{r['f0'][0]:6.0f}-{r['f0'][1]:<6.0f} {r['dom'][0]:5.0f}-{r['dom'][1]:<5.0f} "
                     f"{r['peak']:4d} {r['clip']:4d} {r['dc'] * 100:5.2f} {r['loud']:6.1f} {r['snr']:5.1f} "
                     f"{r['size']:6d} {'yes' if r['same'] else 'NO':<4}  {r['calls']}")
    louds = sorted(r["loud"] for r in rows)
    lines.append("")
    lines.append(f"species: {len(rows)}; total {sum(r['secs'] for r in rows):.1f} s; "
                 f"{min(r['secs'] for r in rows):.2f}-{max(r['secs'] for r in rows):.2f} s each")
    lines.append(f"loudness (K-weighted, gated, after DPCM): {louds[0]:.1f} .. {louds[-1]:.1f} dB, "
                 f"median {louds[len(louds) // 2]:.1f} (target {build.TARGET_LOUDNESS})")
    if stock:
        lines.append(f"stock cries, same measure ({len(stock)} sampled): {stock[0]:.1f} .. {stock[-1]:.1f}, "
                     f"median {stock[len(stock) // 2]:.1f}")
    lines.append(f"peak max {max(r['peak'] for r in rows)} / 127; clipped samples total "
                 f"{sum(r['clip'] for r in rows)}; |DC| max {max(abs(r['dc']) for r in rows) * 100:.2f}%")
    lines.append(f"DPCM SNR {min(r['snr'] for r in rows):.1f} .. {max(r['snr'] for r in rows):.1f} dB")
    lines.append(f"ROM: {total_new} bytes of cry samples ({total_new / 1024:.1f} KiB)")
    lines.append("wav2agb cross-check: " + ("not run (tools/wav2agb not built)" if not os.path.exists(wav2agb)
                 else ("all decoded samples and sizes match the simulation" if not mismatch
                       else "MISMATCH " + ", ".join(mismatch))))
    lines.append(f"byte-identical to the wavs on disk: {sum(r['same'] for r in rows)}/{len(rows)}")
    lines.append(f"feature distance: mean {sum(all_d) / len(all_d):.2f}, same lineage mean "
                 f"{sum(same_lin) / max(1, len(same_lin)):.2f} ({len(same_lin)} pairs)")
    lines.append("closest pairs: " + ", ".join(f"{a}/{b} {d:.2f}" for d, a, b in pairs[:8]))
    text = "\n".join(lines)
    with open(os.path.join(outdir, "cries_summary.txt"), "w") as fh:
        fh.write(text + "\n")
    print(text)


def main():
    args = sys.argv[1:]
    ros = roster()
    if "--check" in args:
        sys.exit(cmd_check(ros))
    if "--report" in args:
        i = args.index("--report")
        if i + 1 >= len(args):
            sys.exit("gen_cry: --report needs a directory")
        cmd_report(args[i + 1], ros)
        return
    unknown = [a for a in args if a.startswith("--") and a != "--all"]
    if unknown:
        sys.exit(f"gen_cry: unknown option {unknown[0]} (see the docstring)")
    names = [a for a in args if not a.startswith("--")] or [sp["folder"] for sp in ros]
    cmd_generate(names, ros)


if __name__ == "__main__":
    main()
