#!/usr/bin/env python3
"""Entry program: regenerates /output/entry.png deterministically (front page, Sat 21 Nov 2026).

Runs build_front.py, which draws the whole newspaper page with Pillow at 4x
supersample (no network, no randomness, no wall clock) and writes the PNG.
"""
import os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)

# build_front.py writes entry.png next to itself; copy it into the output dir.
subprocess.run([sys.executable, os.path.join(here, "build_front.py")], check=True)
src = os.path.join(here, "entry.png")
dst = os.path.join(out, "entry.png")
if os.path.abspath(src) != os.path.abspath(dst):
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
print("entry at", dst, os.path.getsize(dst), "bytes")
