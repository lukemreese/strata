---
name: strata-species-art
description: Adding or changing Strata species and their art and cries — roster rules, stat formula, lineages and extinctions, script-generated sprites, procedural cries, item (capsule) art, and the no-stock-Pokémon rule. Use for any species, lineage, sprite, cry, item-art or terminology work.
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
- **Codex numbers are derived** (`codex_order()` in `gen_species.py`): sorted by `first_era`,
  then roster position, written into `pokedex.h` (`FOREACH_STRATA_CODEX_ORDER`,
  `HOENN_DEX_COUNT`). The player only sees these (001-087); the National number is just the
  save-flag index, so appending keeps saves valid while a new species shifts later Codex
  numbers. A species needs a correct `first_era`, `mass` (kg) and `length` (m): the Codex
  shows mass and length exactly and metric (`50 g`, `2.2 kg`, `9,000 kg`, `10 cm`, `1.5 m`)
  from `src/data/strata_codex.h`, not from the u16 `weight`/`height` fields. Details in
  `docs/strata_design.md` 7.8.
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

## Item art: the specimen capsule (`tools/strata/sprites/items/`, CLI `gen_item_art.py`)

Every place the game draws a Poké Ball draws a capsule (a canister with a bail handle, latch and
status light): battle balls + `balls/open.png`, bag icons, the map item, team row and caught mark,
party menu, bag spinner and pocket badge, Codex caught mark, heal machine, both battle
transitions, starter choice (capsules + an open field case instead of Birch's bag).
`docs/strata_art.md` "Item art" has the file table and what is left on purpose.

- Regenerate: `python3 tools/strata/gen_item_art.py` (all; idempotent), or groups
  (`--list`); then `make`. Colours/markings per capsule: `tiers.py`; shapes: `capsule.py`;
  per-file layout: `targets.py`. Review: `gen_item_art.py --review OUT.png` (stock from git
  vs new) and `Read` it.
- Drawings are role grids (`o`, `b0..b3`, `l0..l2`, `m0/m1`, `s0/s1`, `led`, `in`, `glow`);
  shared palettes get a fixed role -> index map instead of new colours. Before redrawing a
  stock file, find who else uses its palette (healthbox elements use the healthbox palette;
  the status row's palette is the health bar's; party small icon uses the big icon's).
- All tier palettes must keep one role -> index layout: `LoadBallGfx()` pastes the shared
  `balls/open.png` over frame 2 of nine ball sheets.
- A new capsule item: add a `TIERS` entry keyed by the stock ball name, run the generator.
- New stock art with a ball in it: add a writer to `targets.TARGETS` and a row to
  `review.assets()`.
