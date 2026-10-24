---
name: strata-species-art
description: Adding or changing Strata species and their art — roster rules, stat formula, lineages and extinctions, script-generated sprites, and the no-stock-Pokémon rule. Use for any species, lineage, sprite or terminology work.
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

## Art pipeline

- `tools/strata/gen_sprite.py` draws original pixel art from parametric body plans and writes the
  exact formats in `graphics/pokemon/strata/<name>/` (2-frame front, back, normal + variant
  palettes with index 0 transparent, icon in one of the 6 shared icon palettes, footprint) plus a
  `CUSTOM` marker. `gen_species.py` keeps CUSTOM folders and reads their measured sizes/offsets.
  Docs: `docs/strata_art.md`.
- Species without CUSTOM art still use the `borrow=` stock placeholder. That must reach zero.
- Creature map objects use `OBJ_EVENT_GFX_SPECIES(<species>)`; until a species has overworld
  sprite data they render as the substitute placeholder.
- Era battle-background and grass-overlay palettes come from `gen_tilesets.py` transforms, selected
  by the current map's era in `src/strata_art.c`.
- Always look at the output (`Read` the PNG at 1× and 3×) before committing art.
