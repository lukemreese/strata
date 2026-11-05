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
  shows mass and length exactly and metric (`50 g`, `2.2 kg`, `450 kg`, `9.0 t`, `10 cm`, `1.5 m`)
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

## Codex: evidence and lineage pages (C14; design doc 7.8)

Every species needs an EVIDENCE entry, or `gen_species.py` stops ("roster/evidence.py: missing").

- Add it to `tools/strata/roster/evidence.py` (not the roster modules: other lanes edit those),
  keyed by the species constant (`const_name`: the in-game name upper-cased, e.g. `"DOUGLASSCIUR"`):
  `record` (confidence tag: "well known", "partial skeletons", "teeth and jaws", "living
  species"), `bones` (what the reconstruction rests on, ≤ 2 wrapped lines), `inferred` (one line,
  R-e: "colour, calls, habits"; living species: "little, it lives today"), optional `standin`
  (every grade or stand-in descent: shown as "Stand-in: ..."), `note` (a caveat line written in
  full: "Debated: ...", "Unverified: ..."), `today` (a living end's status for the LINEAGE page,
  ≤ 2 lines split by `\n`, e.g. "lost from Montana, alive elsewhere").
- The page also shows the roster's `genus`, `site`, `age` and `mass_est`; don't repeat them. The
  body must wrap to 2-4 lines of ≤ 38 characters. No `~` (the game font has no glyph; ages get
  "about" automatically). Say less rather than guess: no specimen numbers, counts or years you
  can't source; hedge debated points; list species you were unsure of in the commit message.
- Then `gen_species.py`, `make`, `make check TESTS='Every'` (coverage, `Inferred:`, widths in
  pixels) and add the species to the stand-in list in `test/strata_codex.c` if it is a grade.
- LINEAGE needs nothing per species: it reads `src/data/lineages.h` (and `sStrataFossils` for
  the loss reason). A new descent shows up by itself; `test/strata_codex.c` checks every
  species' rows fit their columns, so a long name deep in a line may need FONT_NARROW (it falls
  back automatically) or a shorter `name`.
- Look at it: `python3 tools/strata/playtest/run.py codex_pages` (edit `CODEX_CAUGHT` in
  `scenarios.py` to screenshot another species' pages).

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
  by the current map's era in `src/strata_art.c`. Acts 1-5 also have their own ground-cover art
  (`gen_era_tiles.py`: tileset tiles, grass overlay frames, grass battle backgrounds and entry
  walls), drawn in palette roles from code. Tile-art lessons: judge at 1x (thin vertical
  strokes read as grass; arcs with leaflets read as ferns, radiating rays with dark folds as
  palm fans, wide blades as herbs); recolour shared colours exactly (the lawn ramp plus the
  tree-shadow teal) in every palette instead of redrawing every edge tile; keep 8x8 tiles
  that other metatiles reuse (flipped) self-contained; a battle entry-anim tile 0 must stay
  empty (the tilemap uses it for blank space); wrap entry walls horizontally only.
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
- Other Strata key-item icons (not capsules): letter grids with their own palette in
  `key_items.py`, target group `key_items` (the Fossil Case: `graphics/items/icons/fossil_case.png`
  + `icon_palettes/fossil_case.pal`, `INCGFX` lines at the end of `src/data/graphics/items.h`).
- New stock art with a ball in it: add a writer to `targets.TARGETS` and a row to
  `review.assets()`.
