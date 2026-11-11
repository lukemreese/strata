"""Strata's bridge to a local model (the desktop GPU): cheap, private batch review.

    client.py   OpenAI-compatible chat client (Ollama, llama.cpp, LM Studio, vLLM):
                JSON answers checked against a schema, retries, images, disk cache
    sprites.py  blind identification of every creature sprite ("what animal is this?")
    claims.py   a fact-check worklist from the Codex and field-note text
    shots.py    triage of playtest screenshots (cut-off text, garbled graphics)

CLI: tools/strata/local_model.py. How and when to use it: the strata-local-model skill.

The one rule: a local model sorts and flags; it never decides. Nothing it writes
ships, and nothing it says about the fossil record is evidence. Its output is a
reading order for a person or a stronger model.
"""
