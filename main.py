"""Entrypoint: render the front page and write it to the output directory.

The grader runs `python3 -P -s /bot/main.py` with no network, so this file
adds its own directory to sys.path first (the -P flag stops Python doing
that on its own), imports the drawing code from draw.py beside it, and
writes entry.png into $MAKEFUN_OUTPUT_DIR (or /output when unset).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import render


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    image = render()
    path = os.path.join(out_dir, "entry.png")
    image.save(path, format="PNG")
    size = os.path.getsize(path)
    print(f"wrote {path} ({image.width}x{image.height}, {size} bytes)")


if __name__ == "__main__":
    main()
