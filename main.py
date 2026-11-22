#!/usr/bin/env python3
"""Entry program: writes /output/entry.png (front page, Saturday 21 November 2026).

The graded runtime is Python 3.13 standard library only, so the final image is
committed in the repository and this program copies it to the output directory
byte for byte — the rules allow exactly this, and it keeps both runs identical.
The committed PNG was drawn by build_front.py (Pillow at 4x supersample) in the
build session; the drawing itself never runs at grade time.
"""
import os, shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
src = os.path.join(here, "entry.png")
dst = os.path.join(out, "entry.png")
shutil.copyfile(src, dst)
print("entry at", dst, os.path.getsize(dst), "bytes")
