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
5. Menu text that must stay a fixed width uses `{CLEAR_TO n}` (battle menu `Battle Bag Team Run`);
   keep those offsets.

## Species category

`CopyMonCategoryText` (`src/international_string_util.c`) prints the category alone
("Cimolestid"); no suffix. Categories come from `tools/strata/roster`, max 12 chars.

## Left on purpose (unreachable in Strata)

Stock content nothing links to: contests, Battle Frontier, link/trade/union room, TV, Match
Call, Pokéblock and berry blender, day care, safari zone, Mauville and Lilycove NPC text,
tutors, every stock `data/maps/*` (Hoenn and Kanto) script, `src/debug.c`, credits
(`src/data/credits.h`, `src/credits_frlg.c`: needs a Strata credits pass), `shared_dex_text.h`
(stock species). Text baked into images (not redrawn): `graphics/pokedex/hgss/tileset_menu_search*.png`
("POKéDEX" title), `graphics/pokedex/menu.png`, `graphics/pokedex/search_menu.png`,
`graphics/credits/the_end_copyright.png`, FRLG intro/title/credits art, `graphics/pokenav/*`.
If one becomes reachable, redraw it and add the file to this list's "done" side in the commit.
