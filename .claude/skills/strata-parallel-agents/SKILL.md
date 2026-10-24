---
name: strata-parallel-agents
description: Running several Strata subagents in parallel without collisions — worktrees, briefs, file ownership, reserved flags, merging branches with the repo's merge helper, and recovering from usage limits. Use when splitting Strata work across agents.
---

# Parallel agents on Strata

## Setup per agent

- Each agent gets its own worktree and branch:
  `git worktree add -b strata-<lane> ~/projects/strata-<lane> strata`. If the git lock is busy
  because another agent is doing the same, wait and retry. Agents never touch the main checkout,
  never push or merge, and never remove their worktree.
- Give each agent a unique temp-script name (`<lane>_x.sh`, see the strata-shell skill) and
  `make -j6`..`-j8`.
- Per-act content: reuse `tools/strata/agents/act_brief.md` (placeholders `{ACT_TITLE}`, `{ERA}`,
  `{MODULE}`, `{TASK}`, `{SECTION}`, `{BRANCH}`, `{TAG}`, `{STORY_IN}`/`{STORY_DONE}`,
  `{MAPS_HINT}`). The prompt says "read the brief at … and follow it with these substitutions".
- Give agents the context they lack: what's built, file paths, which files other agents own. A
  fresh agent knows nothing of this session.

## File ownership (prevents conflicts)

- One act module per agent (`tools/strata/maps/actN_*.py`) plus its map scripts and its section
  of `include/constants/strata_act_flags.h`. Shared helpers (`common.py`, `gen_maps.py`,
  `__init__.py`), roster files, `lineages.h` and shared C each belong to one agent per round.
- Never hand-merge generated files. `tools/strata/agents/merge_branch.sh <branch>` takes either
  side for them and regenerates, auto-resolves markdown table conflicts by row key
  (`resolve_tables.py`, keeps the longer row), stops on any other conflict, then runs mapcheck,
  build and the full tests. After fixing a manual conflict and `git add`, run
  `merge_branch.sh --continue`.
- Merge one branch at a time and check the test result before the next; remove the worktree after
  merging.
- Hand-kept lists in tests are conflict magnets: iterate generated tables (`sStrataMapInfo`) instead.

## Usage limits

Four or more agents at once tend to hit the session usage limit. Agents stop mid-task, but their
work is saved. After the reset, resume each with SendMessage ("check `git status` in your
worktree, then finish per the brief"), not a new agent. Waves of about four keep progress steady.

## Model choice that worked

Design or outline work: Opus, high effort. Systems C work: Opus, medium to high. Content and maps:
Sonnet, high. Ask each agent for an exact reply format (what changed, deviations, test counts,
commit hash) so the lead can merge without rereading everything.
