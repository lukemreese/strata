---
status: draft
paths: [tools/strata/roster/actN_x.py, src/data/strata_codex.h]
think: medium
max_changed_lines: 200
fetch: []
---
# Short imperative title

## Goal
What to change and why, in 2-5 sentences.

## Read first
- `tools/strata/roster/actN_x.py`, the `SPECIES_NAME` entry
- the `strata-build-test` skill's generator table, for which outputs the generator writes

## Facts and sources
- "Exact quote with the fact." (https://paleobiodb.org/... or the paper citation + URL)

## Acceptance criteria
- `field` of `SPECIES_NAME` changes from `old` to `new`.
- Run `python3 tools/strata/gen_species.py`; commit its output (listed in `paths:`).
- `make -j12` and `make check -j12` (0 FAILED) pass.

## Out of scope
Everything else, in particular other species and balance.
