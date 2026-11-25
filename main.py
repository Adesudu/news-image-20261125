#!/usr/bin/env python3
"""Place the finished front-page image where the harness expects it.

The newspaper front page itself is drawn ahead of time by render.py and
stored in this repository as entry.png. This entrypoint does no drawing:
it only copies that ready-made image into the output directory the
harness names, so the graded file lands at <output>/entry.png.

Deterministic by construction: a plain byte copy, so two runs always
produce identical output.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT = "out"


def pick_output_dir() -> str:
    """Return the output directory from the environment, or the default."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return chosen or DEFAULT_OUTPUT


def repo_root() -> Path:
    """Return the directory this script lives in (the repository root)."""
    return Path(__file__).resolve().parent


def copy_front_page() -> Path:
    """Copy entry.png into the output directory and return its path."""
    source = repo_root() / SOURCE_NAME
    if not source.is_file():
        raise FileNotFoundError(f"expected image not found: {source}")

    out_dir = Path(pick_output_dir())
    out_dir.mkdir(parents=True, exist_ok=True)

    destination = out_dir / SOURCE_NAME
    shutil.copyfile(source, destination)
    return destination


def main() -> int:
    placed = copy_front_page()
    print(f"wrote {placed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
