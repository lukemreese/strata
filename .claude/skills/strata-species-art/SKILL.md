---
name: strata-species-art
description: Adding or changing Strata species, their art and cries — roster rules, stat formula, lineages and extinctions, script-generated sprites, procedural cries, and the no-stock-Pokémon rule. Use for any species, lineage, sprite, cry or terminology work.
---

# Strata species and art

## Hard rules from the user

- **No stock Pokémon anywhere**: no borrowed stock sprites, cries or overworld sprites in the
  shipped game, and the creatures are never called "Pokémon" (in game text, docs or replies).
  Strata's words: animals, specimens, lineages, reconstructions, Codex. Treat any remaining
  "POKéMON"/"Poké Ball"/stock sprite as a bug. The vocabulary table and the safe way to change
  stock strings are in the strata-text skill.
- Science first: real genera, sites and dates; flag uncertainty in dex text and field notes.

## Roster

- `tools/strata/roster/` per act; aggregator `__init__.py` documents every field. **Order rule:**
  new species are always appended (`part3.py` or a new `partN.py` at the end of `PARTS`). Never
  insert or reorder: species IDs, dex numbers and saves depend on order.
- Names ≤ 12 chars (genus, else informal form, else a morpheme cut). Category ≤ 12 chars. Dex text
  wraps at 38 chars, 4 lines (the generator enforces it).
- Stats: `BST = 340 + 50·log10(kg)`, clamped 250–600, +40 for `focal=True` (every species a starter
  line can become; a test checks this).
- `first_era` required, `last_era` for stand-ins, `diet` (carnivore/omnivore/herbivore) generates
  `src/data/strata_diets.h`.
- Lineages and extinctions: `src/data/lineages.h` (`DESCENT_DEFAULT`, `DESCENT_BRANCH(sp, pressure,
  minScore)`, `DESCENT_END`; per-era extinction lists; `sEraLevelFloor`). Branch thresholds must stay
  above the knockout cap (24).

## Art pipeline (`tools/strata/sprites/`, CLI `gen_sprite.py`)

Read `docs/strata_art.md` first: package layout, taxonomy table, formats and the **style guide**
(the quality bar: profile + 3/4 cues for fronts, ramps, outlines, 1×/3× judging, science of colour).

- `sprites/core/` is the plan-independent machinery (rasteriser, palettes, writers, previews);
  `sprites/taxonomy.py` is the one species → body-plan table (20 plans, checked against the roster
  on every run); `sprites/plans/<plan>.py` is a parametric template and `sprites/specs/<plan>.py`
  holds its species data. Working templates: `fish` (Knightia), `small_mammal` (Mesodma); the other
  18 are stubs whose docstrings list species and anatomy. **An artist agent owns its plans' two
  files only**; changes to `core/` or `taxonomy.py` go through the lead.
- Commands (repo root):
  `gen_sprite.py <folder ...> | --plan NAME | --all [--preview DIR]`,
  `--contact OUT.png` (every species' front + overworld on one sheet, borrowed ones framed red),
  `--borrowed [--strict]` (art and cry status; strict exits 1 while any stock sprite or cry remains),
  `--plans` (taxonomy and suggested lanes). Then `gen_species.py`, then `make`.
- Each species gets battle front/back, palettes, icon, footprint, `overworld.png` (6 frames:
  south, south step, north, north step, west, west step; 32×32, 64×64 over 1 t) and `CUSTOM`
  (presentation fields + `@overworld` line). `gen_species.py` turns that into `overworldData`,
  so `OBJ_EVENT_GFX_SPECIES(<species>)` map objects show the creature; species without own art
  still show the substitute placeholder.
- Species without CUSTOM art would get the `borrow=` stock sprites; `ART_STRICT = True` in
  `gen_species.py` makes that an `#error` (build fails). Same for cries with `CRY_STRICT`.

## Cries (`tools/strata/cries/`, CLI `gen_cry.py`; doc: strata_art.md "Cries")

- Every species has an original procedural cry: `cries/specs.py` gives each a basis note
  (living / relative / speculative / silent) and a call program from `voices.CALLS` (squeak,
  yip, howl, growl, roar, whinny, bleat, hum, bellow, trumpet, gobble, boom, honk, hiss, ticks,
  ...). Pitch and formants come from mass and body plan; a lineage motif keeps relatives related.
- A new species needs a `specs.py` entry (gen_cry fails otherwise), then `gen_cry.py <folder>`,
  `gen_species.py`, `make`. Commit the wav with `strata_cries.txt` (the hash marker
  gen_species checks); a hand-edited or stale wav counts as borrowed and breaks the build.
- Output: 8-bit mono 13379 Hz wav, 0.35-1.6 s, signature sound in the first 0.3 s (doubles
  cut cries there). wav2agb DPCM-compresses it: loud highs and noise overload the deltas.
- You can't listen: run `gen_cry.py --report DIR` (Windows temp) and `Read` the lane
  spectrogram sheets and `cries_summary.txt` (loudness -11 ± 1 K-weighted, no clipping, DC
  ~0, not in the closest-pairs list, byte-identical, wav2agb cross-check). `--check` verifies
  the wavs on disk are reproducible.
- Loudness is K-weighted on purpose: A-weighting made booms saturate into buzzes.
- Dinosaur calls are speculative closed-mouth booms, hisses and honks (not roars); say so.
- Refactors of the core must keep existing art byte-identical (`cmp` the PNG/pal files against a
  copy taken before) unless the change is a deliberate improvement you looked at.
- Era battle-background and grass-overlay palettes come from `gen_tilesets.py` transforms, selected
  by the current map's era in `src/strata_art.c`.
- Always look at the output (`Read` the `_sheet`, `_battle` and `_ow` previews; 1× and 3×) before
  committing art, and compare with plan-mates on the contact sheet.
