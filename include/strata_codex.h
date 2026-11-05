#ifndef GUARD_STRATA_CODEX_H
#define GUARD_STRATA_CODEX_H

#include "constants/strata.h"

// Strata's Codex (docs/strata_design.md 7.8). The info screen's bar leads to three pages:
// EVIDENCE (what the reconstruction rests on), LINEAGE (ancestors and descendants from the
// descent table) and CRY. This file has the data and text behind them; src/pokedex.c draws them.

// ---------------------------------------------------------------------------------------------
// Measurements. The species_info `weight` (hectograms, u16, max 6553.5 kg) and `height`
// (decimeters) cannot show a 30 g animal or a 9 t one, so the Codex reads exact values from
// src/data/strata_codex.h (generated from the roster) and shows them metric. Stock species fall
// back to their species_info fields.

// Largest length shown exactly; anything above prints as "999.9+ m". Masses need no cap: the
// largest u32 gram value prints as "4,295 t".
#define CODEX_MAX_LENGTH_DM 9999

// A buffer big enough for any string the writers below produce ("999.9+ m" + EOS).
#define CODEX_MEASURE_STR_LEN 16

// Body mass in grams / body length in centimeters.
u32 Strata_GetSpeciesMassGrams(enum Species species);
u32 Strata_GetSpeciesLengthCm(enum Species species);

// Write the display string for a mass / length at `dst` (EOS-terminated) and return a pointer
// to the EOS:
//   mass    "50 g" (below 1 kg), "2.2 kg" (below 100 kg), "450 kg" (below 1 t),
//           "6.8 t" (below 100 t), "120 t", "4,295 t"
//   length  "15 cm" (below 1 m), "1.5 m", "12.3 m", "999.9+ m" (cap)
u8 *Strata_WriteMass(u8 *dst, u32 grams);
u8 *Strata_WriteLength(u8 *dst, u32 centimeters);

// ---------------------------------------------------------------------------------------------
// EVIDENCE page: generated from tools/strata/roster/evidence.py (src/data/strata_evidence.h).

#define CODEX_EVIDENCE_MAX_LINES 4
#define CODEX_EVIDENCE_TODAY_LINES 2

struct StrataEvidence
{
    const u8 *genus;   // full scientific name
    const u8 *site;    // the fossil occurrence the game uses
    const u8 *age;
    const u8 *record;  // confidence tag: "well known", "teeth and jaws", ...
    const u8 *lines[CODEX_EVIDENCE_MAX_LINES]; // the material, "Inferred: ...", "Stand-in: ..."
    const u8 *today[CODEX_EVIDENCE_TODAY_LINES]; // LINEAGE page note for a living end, or NULL
    u8 lineCount;
    u8 firstEra;       // enum StrataEra: the roster's `first_era`
    bool8 massEstimate;
};

const struct StrataEvidence *Codex_GetEvidence(enum Species species); // NULL for stock species

// The page's text rows, top to bottom (each EOS-terminated, CODEX_LINE_SIZE bytes).
#define CODEX_LINE_SIZE 64
#define CODEX_EVIDENCE_ROWS (4 + CODEX_EVIDENCE_MAX_LINES)
// Fills `rows` (genus, site, age, record, then the evidence lines); returns the row count.
u32 Codex_FormatEvidence(enum Species species, u8 rows[][CODEX_LINE_SIZE]);

// ---------------------------------------------------------------------------------------------
// LINEAGE page: the ancestor chain back to the root of the descent table (src/data/lineages.h),
// the species itself, then its descendants depth first (the default descent before branches).

enum CodexLineageKind
{
    CODEX_LINEAGE_ROOT,    // nothing descends into it
    CODEX_LINEAGE_DEFAULT, // the default descent of its parent (PRESSURE_NONE)
    CODEX_LINEAGE_BRANCH,  // a branch of its parent, steered by `pressure`
};

enum CodexLineageFate
{
    CODEX_FATE_DESCENDS, // it has descendants of its own
    CODEX_FATE_LIVING,   // an end that is alive today
    CODEX_FATE_LOST,     // an end the record ends at a filter (src/data/strata_fossils.h)
};

struct CodexLineageRow
{
    u16 species;
    u16 parent;   // SPECIES_NONE for the root
    u8 depth;     // generations below the root
    u8 era;       // enum StrataEra: the era load it descends at (the root: its first era)
    u8 pressure;  // enum SelectionPressure; PRESSURE_NONE for the root and default descents
    u8 kind;      // enum CodexLineageKind
    u8 fate;      // enum CodexLineageFate
    u8 lostEra;   // the filter that ends it (CODEX_FATE_LOST), else ERA_COUNT
    bool8 seen;   // seen in the Codex; unseen rows show "?"
    bool8 isSelf; // the species whose page this is
};

#define CODEX_LINEAGE_MAX_ROWS 16
#define CODEX_LINEAGE_DETAIL_LINES 4

// Builds the rows for `species`' page; returns the count (at least 1, the species itself).
u32 Codex_BuildLineage(enum Species species, struct CodexLineageRow *rows, u32 max);
// The row's columns: name ("?" when unseen), tag ("default", "MEAT"...), fate ("living", "lost").
void Codex_FormatLineageRow(const struct CodexLineageRow *row, u8 *name, u8 *tag, u8 *fate);
// The detail box under the list for row `index`: how it arises, its fate, and why (the fossil
// reason for a lost end, the evidence `today` note for a living one). Returns the line count.
u32 Codex_FormatLineageDetail(const struct CodexLineageRow *rows, u32 count, u32 index,
                              u8 lines[][CODEX_LINE_SIZE]);
const u8 *Codex_GetEraName(enum StrataEra era);
const u8 *Codex_GetPressureLabel(u32 pressure);

// FONT_NORMAL when `str` fits `width` pixels, else FONT_NARROW (the tests check every Codex
// line fits one of them).
u32 Codex_FitFont(const u8 *str, u32 width);

// Labels of the info screen's bar (EVIDENCE, LINEAGE, CRY), in slot order.
#define CODEX_BAR_SLOTS 3
#define CODEX_BAR_LABEL_FONT FONT_SMALL_NARROW
#define CODEX_BAR_LABEL_WIDTH 40 // the slot's interior: 5 tiles between its end caps
extern const u8 *const gCodexBarLabels[CODEX_BAR_SLOTS];

// Page geometry (pixels in the full-screen info window), shared with the tests.
#define CODEX_PAGE_LEFT  8
#define CODEX_PAGE_WIDTH 224
// LINEAGE rows: the name (indented per generation), the tag and the fate columns.
#define CODEX_LINEAGE_NAME_X  14
#define CODEX_LINEAGE_INDENT  6
#define CODEX_LINEAGE_TAG_X   132
#define CODEX_LINEAGE_FATE_X  188
#define CODEX_LINEAGE_NAME_WIDTH(depth) (CODEX_LINEAGE_TAG_X - 4 - CODEX_LINEAGE_NAME_X - CODEX_LINEAGE_INDENT * (depth))
#define CODEX_LINEAGE_TAG_WIDTH  (CODEX_LINEAGE_FATE_X - CODEX_LINEAGE_TAG_X - 4)
#define CODEX_LINEAGE_FATE_WIDTH (CODEX_PAGE_LEFT + CODEX_PAGE_WIDTH - CODEX_LINEAGE_FATE_X)

#endif // GUARD_STRATA_CODEX_H
