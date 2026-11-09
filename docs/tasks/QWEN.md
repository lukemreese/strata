# Qwen backlog: briefs for the local model

The owner's desktop runs a local **Qwen 3.8 27B** model unattended (the `qwen-autoimprove` runner in
[`lukemreese/ollama-setup`](https://github.com/lukemreese/ollama-setup/tree/autoimprove/autoimprove)).
It works only from briefs in this folder named `qwen-NN-*.md` on the `strata` branch. **Claude, Grok and Muse write
these briefs**; Qwen never chooses its own work. Each result arrives as a **draft PR to `strata` labelled `qwen` +
`do-not-merge`**.

Qwen is a capable but **weak** model. It follows clear instructions well and invents facts, especially
paleontology, when it lacks them. A good brief does the research and the thinking, and leaves Qwen the editing,
regenerating and testing.

## What makes a good Qwen task
- Small and checkable: **at most 400 changed lines** of hand-written source (generated output doesn't count toward
  the intent, but does count toward the limit, so keep generator-heavy tasks tight or raise `max_changed_lines`).
- **Verifiable by the runner's checks:** the generators leave the tree unchanged, then `make`, then `make check`
  (0 FAILED). If correctness depends on taste (art, map layout, balance feel), it isn't a Qwen task.
- Good fits:
  - fact fixes in roster dex text, notes or numbers, Codex/field-note text, with the corrected fact quoted in the brief
    (e.g. a "likely wrong" item from the batch fact-check, *after* Claude, Grok or Muse confirmed it against PBDB or a paper)
  - a missing `test/strata_*.c` check
  - player-text vocabulary fixes per `strata-text`
  - docs sections grounded in code
- Bad fits: new maps or acts, sprites, balance passes, anything needing playtest judgement, shared generator code
  (`tools/strata/maps/common.py`, `sprites/core/`), build files. Leave those to Claude.

## Brief format
File: `docs/tasks/qwen-NN-short-slug.md` (NN = next free number). Copy `qwen-template.md`.

```markdown
---
status: ready                 # ready = the runner may pick it; draft = not yet; done = finished (set after merge)
paths: [tools/strata/roster/act4_bighorn.py, src/data/strata_codex.h]   # REQUIRED: files/globs Qwen may change, INCLUDING generated outputs
think: medium                 # optional: low | medium | high
check: python3 tools/strata/gen_species.py && make -j12 2>&1 | tail -20   # optional quick check Qwen runs itself
max_changed_lines: 200        # optional (default 400)
fetch: [https://paleobiodb.org/classic/basicTaxonInfo?taxon_name=Coryphodon]   # optional extra URLs Qwen may read
agent: claude                 # optional: claude (Claude Code on Qwen; loads .claude/skills; strata default) | pi
---
# One-line title (becomes the PR title as QWEN-NN: ...)

## Goal          what and why, 2-5 sentences
## Read first    exact files (and line numbers/keys) to read
## Facts and sources   every fact Qwen needs, quoted verbatim, each with its URL or citation
## Acceptance criteria  concrete bullets: what text/value changes to what; which generator to run; which test
## Out of scope  what not to touch
```

## Grounding rules for brief authors
1. **Put the facts in the brief.** Masses, lengths, ages (Ma), sites, diets, taxonomy: quote the source (PBDB record,
   paper, museum page) with its URL. Qwen is told to use only the brief, the repo and pages it fetches.
2. Qwen has **web search** (`search`) and `fetch`, both logged and listed in its PR. It can fetch the exact URLs a search
   returned, paleobiodb.org, en.wikipedia.org, species.wikimedia.org and rh-hideout.github.io, and URLs in the brief's
   `fetch:`. Search is a fallback for a weak model: **still put the facts in the brief**. Wikipedia is acceptable for
   background, but give a primary or PBDB source for any number. Treat any fact Qwen found on its own as unverified until
   a reviewer checks the source.
3. **Generated files:** if Qwen edits a generator source (roster, maps module, tileset spec), list the generator's outputs
   in `paths:` and name the generator in the criteria (see the `strata-build-test` skill for the table). The runner rejects
   the change if rerunning the generators would change the tree.
4. Player-visible text follows `strata-text` (no "Pokémon"; animal, TEAM, Specimen Capsule...). Quote the exact new wording when it matters.
5. One brief, one PR.

## What the runner does (so you can predict the result)
- It takes `status: ready` briefs from `origin/strata` in filename order, one at a time, alternating with riskfusion.
- It branches `qwen/<brief-id>` from `strata` and runs Qwen in a sandbox, through Claude Code by default, so the project skills
  in `.claude/skills` apply. There's no network except Ollama, `search` and `fetch`.
  The checks are: only `paths:` changed, diff size, generators produce no further change, `mapcheck.py`, `make`, and `make check` with 0 FAILED.
  Up to 2 repair rounds; then a read-only Qwen self-review lists unsupported claims in the PR body.
- **On failure:** no PR. The attempt is logged on the desktop (`~/.local/state/qwen-autoimprove/ledger.jsonl`). Edit the brief to re-queue it.
- **Never edited by Qwen:** `docs/tasks/`, `Makefile`, `config.mk`, `.github/`, `tools/strata/agents/`, ROMs and `build/`.
- The runner pauses while a game runs on the desktop, so expect hours, not minutes. A full strata check is slow anyway.

## Reviewing Qwen PRs (Claude, Grok, owner)
- Treat them as drafts from a junior contributor. Check every fact against the brief's sources, and read the self-review and "Open questions" sections.
- If it's good: remove `do-not-merge`, mark ready, and merge into `strata`. If it's close: push fixes to `qwen/<id>`, or close it and improve the brief.
- **Bots: never merge a PR that is a draft or carries `do-not-merge`.**
- After merge or close, set the brief to `status: done` (or delete it).

Standing rules pasted into every Qwen prompt: [`qwen-rules.md`](qwen-rules.md).
