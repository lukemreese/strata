---
name: strata-text
description: Strata's game vocabulary (no "Pokémon" anywhere the player can see) and how to change a stock string safely - the terms.py first pass, test expectations, width tests, and what is deliberately left. Use for any player-visible text, item/move/menu strings, or when pulling in new stock text.
---

# Strata text and vocabulary

The creatures are never "Pokémon". The table is in `docs/strata_design.md` section 0; the short
version: creature = **animal** (labels: `ANIMAL`), party = **TEAM**, Poké Ball = **Specimen
Capsule** (prose: capsule; pocket `CAPSULES`), POKéMON CENTER = **FIELD STATION**, POKé MART =
**CAMP STORE**, POKéDEX = **CODEX**, opponent class = **RESEARCHER**, POKéNAV = **FIELD LOG**,
species category has **no** " POKéMON" suffix. ALL CAPS only for labels and the proper nouns
the stock text already capitalised; prose is lower case ("an animal", "wild animals").
Because `ANIMAL` means the creature, don't reuse it for anything else: the meat-diet pressure
(`PRESSURE_MEAT_DIET`) is labelled **MEAT**, next to PLANT.

## Changing stock text

1. Run `python3 tools/strata/terms.py [--sentences] FILE...` (diff, or whole-sentence before/after;
   `--write` to apply). It joins `COMPOUND_STRING` pieces and `.string` runs, picks a/an and
   singular/plural from context, keeps case. It is a first pass: **read every sentence**
   (menu labels, "the X" and possessives are where it guesses wrong), then fix by hand.
2. Tools that mangle this work: the Bash tool halves backslashes in heredocs, so write Python
   or C that contains `\n`, `\p` or regexes with the Write tool, not a heredoc.
3. `make check` fails for any battle string a test asserts. `MESSAGE("...")` in `test/battle/**`
   compares the rendered text exactly, so change both in the same commit: update the test
   expectations with the same wording (a mechanical replace on lines containing `MESSAGE(` is
   fine; item names come from `gItemsInfo`, so "You used Poké Ball!" becomes "You used Specimen
   Capsule!"). Strings no test asserts need nothing. Test-owned text such as
   `test/battle/trainer_slides.h` is not player text and stays.
4. Widths are tested, not guessed: `test/text.c` checks item names (88 px bag list, 84 px shop),
   item and move descriptions, and every battle string against the message window. Run
   `make check TESTS='Item names'` and `TESTS='Battle strings'` after touching them. `animal`
   is shorter than `Pokémon`, so rewrites only get narrower; a longer name such as "Specimen
   Capsule" is what to measure.
5. Text built at runtime (rig forecast, pressure chart: `src/strata_forecast.c`) switches to
   `FONT_NARROW` when a line is too wide (`Forecast_FitFont`), and `test/strata_forecast.c`
   formats every species x era x pressure case and checks the widths. Follow that pattern for new
   generated text. `{COLOR RED}` is palette index 4 (shadow 5): a custom palette must keep those
   slots red (the chart's does) or the colour code shows the wrong colour.
6. Map script text has no width test of its own. For new dialogue you want checked, make its
   labels global (`Label::`), declare them `extern const u8 Label[];` in a test, expand the
   placeholders at their widest (7-char `W` name, `888` for a number) and measure each line
   (≤ 208 px, at most one `\n` per `\p` page): `test/strata_story.c` does this for the S1
   interludes, Halvorsen's lines (every story × subplot) and the 152 px field-log box.
7. Menu text that must stay a fixed width uses `{CLEAR_TO n}` (battle menu `Battle Bag Team Run`);
   keep those offsets.

## Species category

`CopyMonCategoryText` (`src/international_string_util.c`) prints the category alone
("Cimolestid"); no suffix. Categories come from `tools/strata/roster`, max 12 chars.

## Left on purpose (unreachable in Strata)

Stock content nothing links to: contests, Battle Frontier, link/trade/union room, TV, Match
Call, Pokéblock and berry blender, day care, safari zone, Mauville and Lilycove NPC text,
tutors, every stock `data/maps/*` (Hoenn and Kanto) script, `src/debug.c`, the stock credits
data (`src/data/credits.h`, no longer included) and `src/credits_frlg.c` (FRLG build only),
`shared_dex_text.h` (stock species), the Hall of Fame screen (league text, never entered).
Text baked into images (not redrawn): `graphics/pokedex/hgss/tileset_menu_search*.png`
("POKéDEX" title), `graphics/pokedex/menu.png`, `graphics/pokedex/search_menu.png`,
FRLG intro/title/credits art, `graphics/pokenav/*`.
If one becomes reachable, redraw it and add the file to this list's "done" side in the commit.
Done: the truck interior (`data/maps/InsideOfTruck`, reachable since the new game starts there:
its stock logo-box text is now a field-gear crate; the three box sprites and the tileset
carry no logo; width-tested in `test/strata_truck.c`, which also scans for "POK").
Done: the credits (`src/credits.c` is Strata's roll up the column, S3: printed text only, so
`graphics/credits/the_end_copyright.png` and the bike-scene art are no longer drawn).

## The credits roll (S3)

`src/credits.c` draws, `src/strata_ending.c` holds the words: band names and ages, loss phrases
per filter ("lost at the K-Pg boundary"), the credits proper (`gEndingCreditsLines`) and the
fixed lines (`gText_Ending*`). Rows are two columns (x 8 and x 92, end 232) or centred; every
string goes through `Ending_FitFont` (narrow when too wide), and `test/strata_ending.c` checks
every band, every species as lost or living, and every fixed line, so a new line must be added
to that test. Credit people as "the Strata team" and the science in general; no stock names.
