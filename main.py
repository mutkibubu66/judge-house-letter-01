# judge-house-letter-01 entry: hands in the image beside this file as
# /output/entry.png. The image is the whole entry, so the program does
# nothing to it: it reads entry.png and writes those exact bytes out again.
# A pure byte copy is deterministic by construction, so the grader's two
# runs match. Pure stdlib only (the grader runs stock python:3.13-slim
# with no Pillow installed).
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
import struct

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

src_path = os.path.join(HERE, "entry.png")
dst_path = os.path.join(OUT_DIR, "entry.png")

with open(src_path, "rb") as f:
    data = f.read()

# Validate: entry.png must be a real PNG, not just any file with that name.
if data[:8] != PNG_SIGNATURE:
    raise SystemExit("entry.png is not a PNG: bad 8-byte signature")
if len(data) < 33 or data[12:16] != b"IHDR":
    raise SystemExit("entry.png is not a PNG: missing IHDR chunk")
width, height = struct.unpack(">II", data[16:24])
if width == 0 or height == 0:
    raise SystemExit("entry.png is not a PNG: zero IHDR dimension")

os.makedirs(OUT_DIR, exist_ok=True)
with open(src_path, "rb") as src:
    with open(dst_path, "wb") as dst:
        shutil.copyfileobj(src, dst)

# Verify: the copied output must be byte-identical to the source.
src_hash = hashlib.sha256(data).hexdigest()
with open(dst_path, "rb") as f:
    dst_hash = hashlib.sha256(f.read()).hexdigest()
if src_hash != dst_hash:
    raise SystemExit(
        f"output mismatch: {dst_path} differs from {src_path} "
        f"(sha256 {dst_hash} != {src_hash})"
    )
size = os.path.getsize(dst_path)
print(f"entry.png: {width}x{height}, {size} bytes, written to {dst_path}")
print(f"verified byte-identical copy (sha256 {src_hash[:16]}...)")
