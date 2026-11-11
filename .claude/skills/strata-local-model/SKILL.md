---
name: strata-local-model
description: Using the local model on the desktop GPU (RTX 4090) for Strata — server setup and model choice, the doctor check, blind sprite identification, the fact-check worklist, playtest screenshot triage, one-off questions, and what may and may not be handed to a weaker model or a local coding agent. Use when reviewing many sprites, screenshots or texts, or when delegating work to a local model.
---

# Local model (tools/strata/local_model.py)

A 24 GB card runs a ~30B multimodal model for free. That is far below a frontier model at
judgement and far above it at price, so it gets the jobs that are wide and shallow: look at 87
sprites, read 300 texts, scan 200 screenshots, and say which few deserve a careful look.

**The rule: it sorts and flags; it never decides.** Nothing it writes ships. Nothing it says about
the fossil record is evidence. Every report it makes is a reading order.

## Setup (once)

Any OpenAI-compatible server works: Ollama (`:11434/v1`, the default), llama.cpp `llama-server`
(`:8080/v1`), LM Studio (`:1234/v1`), vLLM (`:8000/v1`).

```bash
export STRATA_LLM_URL=http://localhost:11434/v1   # default
export STRATA_LLM_MODEL=<text model name>          # unset = the server's only model
export STRATA_VLM_MODEL=<vision model name>        # unset = STRATA_LLM_MODEL
python3 tools/strata/local_model.py doctor         # must print two "ok" lines
```

- **Model.** One multimodal model for both jobs keeps it loaded and avoids swaps. On 24 GB pick the
  largest vision-capable model whose 4-bit quant leaves ~3 GB free for context (a Qwen3-VL-class
  30B or the current Qwen ~27B multimodal; Gemma's ~27B is the usual alternative). Model names
  change every few months: check the hub, pull one, and let `doctor` be the judge. If `doctor`
  fails the image line, the model or its server build has no vision.
- **Repo in WSL, server on Windows.** `localhost` reaches Windows from WSL only with mirrored
  networking (`[wsl2] networkingMode=mirrored` in `%UserProfile%\.wslconfig`, then `wsl --shutdown`).
  Otherwise bind the server to all interfaces (Ollama: `OLLAMA_HOST=0.0.0.0`) and use the host
  address: `export STRATA_LLM_URL=http://$(ip route show default | awk '{print $3}'):11434/v1`.
- **Context.** Ollama's default context window is small. For `ask --file` on long files raise it
  (`OLLAMA_CONTEXT_LENGTH=16384`, or a Modelfile `PARAMETER num_ctx`), or the file is silently cut.
- A cloud session can't reach the desktop. Run these on the desktop and commit or paste the report.

## Commands

All write to `build/local_model/` (`--out` to change). Answers are cached on disk by request
(`.cache/strata-local`), so a rerun asks only about what changed. Changing the model or a prompt
invalidates the cache by itself.

| Command | Does | Read the result as |
|---|---|---|
| `doctor` | Server up, models served, JSON and image probes | Go / no-go |
| `sprites [species...] [--plan P]` | Shows each front sprite, unnamed, and asks "what animal is this?"; grades the guesses against keywords per body plan (`top1`, `top3`, `miss`) | The order to look at sprites. `sprites.md` lists misses first |
| `claims [--source codex\|maps\|all] [--no-model] [--only X]` | Mechanical pass: superlatives with no hedge. Model pass: every text split into single claims with kind, hedged or not, guessed risk | The order to fact-check. `--no-model` needs no server |
| `shots DIR` | Describes each playtest screenshot and flags cut-off text, garbled tiles, wrong colours, placeholders | Which screenshots to open |
| `ask "q" [--image PNG] [--file F]` | One free-form answer | A cheap first read, never a source |

Typical runs:

```bash
python3 tools/strata/local_model.py sprites --plan equid          # after changing the horse template
python3 tools/strata/local_model.py claims --only Hypohippus      # after editing one Codex entry
python3 tools/strata/playtest/run.py all --quiet --out build/harness
python3 tools/strata/local_model.py shots build/harness
```

## Reading the reports

- **Sprites.** A `miss` is one of three things: the sprite doesn't read; the model doesn't know the
  animal; the keyword list is too narrow. Open `build/local_model/sprites/<folder>.png` (exactly
  what the model saw) and decide. Widen `SPECIES_ACCEPT` in `tools/strata/localmodel/sprites.py`
  only for a name a lay viewer could fairly give; never to make a number go up. Track the count
  per plan over time: a template change that turns three `top1` into `miss` is a regression signal
  even when each sprite looks fine alone. Guesses within a plan that are all the same word
  ("deer" for every ungulate) mean the species are not distinct at 1x.
- **Claims.** The model's `risk` is a guess. Verify against PBDB or the paper, then record the
  outcome in `docs/strata_outline.md` section 5 as before. A claim marked low risk is unverified,
  not confirmed.
- **Shots.** The harness (`result.json`) owns crashes and state; this owns what a still image
  shows. Vision models misread small pixel fonts: confirm a `text_cut_off` flag by opening the PNG.

## Making a weak model reliable (how these tools are built; do the same in new ones)

1. One narrow question per call, about one item. No multi-step instructions.
2. The answer is JSON with a schema; enums instead of free text wherever a grade is needed.
   `Client.ask_json` validates and re-asks with the error; an item that still fails is marked
   `error` in the report, never guessed.
3. Grade with code, not with the model: the model says what it sees, a keyword table decides.
4. Blind where possible: don't tell it the expected answer and then ask if it agrees.
5. Say what normal looks like ("a dark or grey scene is normal"), or everything gets flagged.
6. Temperature 0, cached, so two runs agree and a diff of two reports means something.
7. Every report states what it can't tell you.

Add a new batch job as `tools/strata/localmodel/<job>.py` (prompt, schema, `review`, `report`), a
subcommand in `local_model.py`, and a test with the fake server in `tools/strata/tests/`.

## A local model as a coding agent

Possible with any agent CLI that speaks the OpenAI API, but hold it to task cards. It works from
`AGENTS.md` (written for it), in its own worktree (strata-parallel-agents skill), and the lead
reviews the diff before any merge.

| Hand it | Why it is safe |
|---|---|
| Proportion and colour tweaks in one `sprites/specs/<plan>.py` | One file, instant render, `sprites` regrades it |
| New `.txt` playtest scenarios in the DSL | Runs or it doesn't; the harness reports |
| Widening keyword tables, test data, doc tables | Mechanical, covered by unit tests |
| First drafts of *questions* for the fact-check | Questions can't be wrong the way answers can |

Never hand it: C code, `lineages.h`, roster order or stats, Codex or field-note wording, merges,
or anything where "it compiles" is the only check. A task card states the one file it may edit,
the exact command that proves it worked, and the stop conditions from `AGENTS.md`.
