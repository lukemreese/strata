"""Repo paths and the shared PNG/palette readers from tools/strata/maprender.py."""

import os
import sys

STRATA_TOOLS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ROOT = os.path.abspath(os.path.join(STRATA_TOOLS, "..", ".."))
if STRATA_TOOLS not in sys.path:
    sys.path.insert(0, STRATA_TOOLS)

from maprender import read_pal, read_png, write_png, draw_text  # noqa: E402,F401

ART_DIR = os.path.join(ROOT, "graphics/pokemon/strata")


def species_dir(folder):
    return os.path.join(ART_DIR, folder)
