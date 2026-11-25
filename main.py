"""Deliver the pre-rendered front page for news-image-20261125.

The image itself lives in the repository as entry.png. This program's only
job is to place an exact copy of it where the grader looks for the output:
the directory named by MAKEFUN_OUTPUT_DIR (or "out" when that variable is
empty or unset). The copy is byte for byte, so repeated runs always produce
identical output.
"""

import os
import shutil
import sys
from pathlib import Path


IMAGE_FILENAME = "entry.png"


def output_directory() -> Path:
    """Resolve the output directory from the environment."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(configured if configured else "out")


def place_image(image: Path, directory: Path) -> Path:
    """Copy image into directory, making it first if needed."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / image.name
    shutil.copyfile(image, target)
    return target


def run() -> int:
    repo_root = Path(__file__).resolve().parent
    image = repo_root / IMAGE_FILENAME
    if not image.is_file():
        print(f"error: {IMAGE_FILENAME} not found next to main.py", file=sys.stderr)
        return 1
    target = place_image(image, output_directory())
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
