# Strata skills

Claude Code skills capturing how to work on Strata. They're canonical here, in the repo. The
Windows workspace (`C:\Projects\pokemon-custom`) mirrors them in `.claude/skills/` so they load in
sessions started there. After editing, sync with:

```bash
rsync -a --delete ~/projects/strata/.claude/skills/ /mnt/c/Projects/pokemon-custom/.claude/skills/
```

When a task teaches something non-obvious (a trap, a working recipe, a check that would have
caught a bug), add it to the matching skill or create a new one. Keep each skill short and
actionable.

| Skill | Use for |
|---|---|
| `strata-shell` | Running commands in the WSL repo from Windows; pushing |
| `strata-build-test` | Generators, build, tests and their pitfalls, debug ROM |
| `strata-maps` | Maps, scripts, act content, flags, object graphics |
| `strata-species-art` | Roster, lineages, sprites, no-stock-Pokémon rule |
| `strata-playtest` | mGBA testing, debug menu, crash hunting |
| `strata-parallel-agents` | Splitting work across subagents and merging it |
