# judge-house-letter-01 entry: hands in the image beside this file as
# /output/entry.png. The image is the whole entry, so the program does
# nothing to it: it reads entry.png and writes those exact bytes out again.
# A pure byte copy is deterministic by construction, so the grader's two
# runs match. Pure stdlib only (the grader runs stock python:3.13-slim
# with no Pillow installed).
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(HERE, "entry.png"), "rb") as src:
    with open(os.path.join(OUT_DIR, "entry.png"), "wb") as dst:
        shutil.copyfileobj(src, dst)
size = os.path.getsize(os.path.join(OUT_DIR, "entry.png"))
print(f"entry.png written to {OUT_DIR} ({size} bytes)")
