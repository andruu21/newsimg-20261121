#!/usr/bin/env python3
"""Entry program: regenerates /output/entry.png deterministically (front page, Sat 21 Nov 2026).

Runs gen.py, which draws the whole newspaper page with the Python standard library
only (no fonts, no network, no randomness that is not seeded) and writes the PNG.
"""
import os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
subprocess.run([sys.executable, os.path.join(here, "gen.py"),
                os.path.join(out, "entry.png")], check=True)
