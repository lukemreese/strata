# Strata

> A science-grounded GBA game set in the North American West, running from the last days of
> the dinosaurs to the present. Every creature is a real, fossil-documented animal. You are a
> field paleontologist climbing a stratigraphic column: each act is a rock layer you reconstruct
> before entering it.

Strata is complete and playable: nine acts from Hell Creek (66 Ma) to the Montana prairie
today, 87 animals with original generated sprites and cries, lineages that descend or die out
at each layer according to the pressures you put them under, and a present-day story about a
fossil that might be sold out of the ground.

| | |
|---|---|
| [Game design](docs/strata_design.md) | pillars, vocabulary, acts, systems |
| [Master outline](docs/strata_outline.md) | the plan, what is done, the fact-check list |
| [Art pipeline](docs/strata_art.md) | how the creatures, tiles and cries are generated |
| [Agent rules](AGENTS.md) | the rules and the edit, generate, check loop |

## Play

Grab the `strata` artifact (`pokeemerald-release.gba`) from a green CI run on the `strata`
branch, or build it. Any GBA emulator runs it; mGBA is the one it is tested on.

## Build

Toolchain: `gcc-arm-none-eabi`, `binutils-arm-none-eabi`, `libnewlib-arm-none-eabi`,
`libpng-dev`, `python3` (details per platform in [INSTALL.md](INSTALL.md)).

```bash
make -j$(nproc)            # pokeemerald.gba
make -j$(nproc) check      # the test suite: 0 FAILED required
make -j$(nproc) release    # pokeemerald-release.gba, asserts off
```

## Work on it

Species, sprites, cries, maps and tilesets are generated from Python sources in
`tools/strata/`; the outputs are committed and never edited by hand. The loop and the table of
sources are in [AGENTS.md](AGENTS.md).

```bash
python3 tools/strata/check.py                      # tooling tests, art, maps, generator drift
make -j8 playtest && python3 tools/strata/playtest/run.py all --quiet   # scripted headless playtests
python3 tools/strata/local_model.py doctor         # optional: batch review on a local GPU model
```

How to do each kind of work is written down as skills in [`.claude/skills/`](.claude/skills/README.md).

## Credits

Strata is built on RHH's [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)
1.17.1, which is built on pret's [pokeemerald](https://github.com/pret/pokeemerald). The engine's
features are listed in [FEATURES.md](FEATURES.md), its contributors in [CREDITS.md](CREDITS.md)
and its documentation at the
[pokeemerald-expansion documentation page](https://rh-hideout.github.io/pokeemerald-expansion/).

```
Based off RHH's pokeemerald-expansion 1.17.1 https://github.com/rh-hideout/pokeemerald-expansion/
```
