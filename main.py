#!/usr/bin/env python3
"""news-image-20261127 entry: place the front page in the output dir.

The image (entry.png, drawn by draw.py at build time) sums up the
world news of Friday 27 November 2026 as one newspaper front page.
This program only copies it into the output directory, so both
grading runs write identical bytes. Standard library only; no
network, no clock, no files outside this repository.

The gate allows at most 1 MiB and 1024 by 1024 pixels: the program
refuses to write an image that breaks either limit, and verifies the
copy with a sha256 self-check before reporting success.
"""
import hashlib
import os
import shutil
import sys

IMAGE = "entry.png"
MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_png_size(path):
    """Return (width, height) from a PNG header, or None if not a PNG."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, IMAGE)

    if not os.path.isfile(source):
        print(f"missing {IMAGE} beside main.py", file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print(f"{IMAGE} is over the 1 MiB gate limit", file=sys.stderr)
        return 1
    size = read_png_size(source)
    if size is None:
        print(f"{IMAGE} is not a PNG file", file=sys.stderr)
        return 1
    if size[0] > MAX_DIM or size[1] > MAX_DIM:
        print(f"{IMAGE} is {size[0]}x{size[1]}, over the 1024x1024 limit",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)
    if sha256_of(source) != sha256_of(target):
        print("copy self-check failed", file=sys.stderr)
        return 1
    print(f"wrote {target} sha256={sha256_of(target)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
