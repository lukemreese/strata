#ifndef GUARD_STRATA_CODEX_H
#define GUARD_STRATA_CODEX_H

// Strata's Codex measurements. The species_info `weight` (hectograms, u16, max 6553.5 kg) and
// `height` (decimeters) cannot show a 30 g animal or a 9 t one, so the Codex reads exact values
// from src/data/strata_codex.h (generated from the roster) and shows them metric.
// Stock species fall back to their species_info fields.

// Largest value shown exactly; anything above prints as "99,999+ kg" / "999.9+ m".
#define CODEX_MAX_MASS_KG   99999
#define CODEX_MAX_LENGTH_DM 9999

// A buffer big enough for any string the writers below produce ("99,999+ kg" + EOS).
#define CODEX_MEASURE_STR_LEN 16

// Body mass in grams / body length in centimeters.
u32 Strata_GetSpeciesMassGrams(enum Species species);
u32 Strata_GetSpeciesLengthCm(enum Species species);

// Write the display string for a mass / length at `dst` (EOS-terminated) and return a pointer
// to the EOS:
//   mass    "50 g" (below 1 kg), "2.2 kg" (below 100 kg), "300 kg", "9,000 kg", "99,999+ kg" (cap)
//   length  "15 cm" (below 1 m), "1.5 m", "12.3 m", "999.9+ m" (cap)
u8 *Strata_WriteMass(u8 *dst, u32 grams);
u8 *Strata_WriteLength(u8 *dst, u32 centimeters);

#endif // GUARD_STRATA_CODEX_H
