"""Entrypoint: copy the front page image to the output directory.

The grader runs `python3 -P -s /bot/main.py` with standard library only
(RULES.txt: nothing is installed before the program runs), so this file
imports nothing beyond the standard library. The image itself is
entry.png beside this file -- draw.py (Pillow) drew it on this machine
and is kept in the repository as its source, but the grader never runs
it. Copying the file byte for byte is deterministic: two runs write
identical bytes.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    main()
