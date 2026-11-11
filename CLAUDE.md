# Strata

@AGENTS.md

## For Claude sessions

- Skills are in `.claude/skills/` (index: `.claude/skills/README.md`). Load the one for the task
  before starting; when a task teaches a trap or a recipe, add it to the matching skill.
- Where the session runs decides the shell rules. In WSL or a cloud session, run commands
  directly from the repo root. Only a Windows-side session driving WSL needs the strata-shell
  skill.
- A cloud session needs `apt-get install -y gcc-arm-none-eabi binutils-arm-none-eabi
  libnewlib-arm-none-eabi libpng-dev` before `make` (after `apt-get update`). A full build is
  about 15 minutes on 4 cores, `make check` longer.
- The default branch is `strata`. CI builds the ROM, runs the tests and runs
  `tools/strata/check.py` on every push to it and on every pull request.
- Token economy: reading sprites and screenshots one by one is the expensive part of art and
  playtest work. Use `tools/strata/local_model.py sprites` / `shots` (the strata-local-model
  skill) to sort them first, and read only what it flags plus a sample of what it passes.
