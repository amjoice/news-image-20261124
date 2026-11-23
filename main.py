#!/usr/bin/env python3
"""The World Today — sum up 24 November 2026's world news in one image.

The front page is pre-rendered as entry.png (see render.py, the build-time
script that drew it with Pillow). This program uses only the Python standard
library: it copies the pre-rendered image to /output/entry.png, byte for
byte, so the output is deterministic on every run, including in a sandbox
with no third-party packages installed.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
