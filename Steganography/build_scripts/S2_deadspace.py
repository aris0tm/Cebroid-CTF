import os, random, subprocess, zipfile
from PIL import Image

FLAG = "cebroid{tr41l1ng_byt3s}"
random.seed(42)

# 1. innocent-looking base PNG
base_path = "/home/claude/build/_ds_base.png"
img = Image.new("RGB", (600, 400))
px = img.load()
for y in range(400):
    for x in range(600):
        px[x, y] = (int(255 * x / 600), int(255 * y / 400), 128)
img.save(base_path)

# 2. note.txt with the flag, zipped
note_path = "/home/claude/build/_ds_note.txt"
with open(note_path, "w") as f:
    f.write(FLAG + "\n")

zip_path = "/home/claude/build/_ds_payload.zip"
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, "w") as zf:
    zf.write(note_path, arcname="note.txt")

# 3. random padding
padding = bytes(random.randint(0, 255) for _ in range(128))

# 4. concatenate: legit png + padding + zip, after the PNG's IEND chunk
out_path = "/home/claude/challenges/deadspace.png"
with open(base_path, "rb") as f:
    png_bytes = f.read()
with open(zip_path, "rb") as f:
    zip_bytes = f.read()

with open(out_path, "wb") as f:
    f.write(png_bytes)
    f.write(padding)
    f.write(zip_bytes)

print("deadspace.png written, total size:", os.path.getsize(out_path))

# sanity: image still opens fine
Image.open(out_path).verify()
print("PNG still valid")
