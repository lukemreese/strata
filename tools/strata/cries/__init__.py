"""Strata cry synthesiser: original procedural cries for every roster species.

    dsp.py       sources, filters, envelopes, mixing (stdlib, seeded)
    voices.py    Voice (anatomy from mass and body plan, lineage motif) and the call library
    specs.py     CRIES: each species' basis note and call program
    build.py     render + master (loudness, limiter, DPCM-aware) + wav bytes
    analysis.py  DPCM simulation, loudness, FFT, spectrogram PNGs
    manifest.py  strata_cries.txt, the original-cry marker gen_species.py reads

CLI: tools/strata/gen_cry.py. Docs: docs/strata_art.md, "Cries".
"""
