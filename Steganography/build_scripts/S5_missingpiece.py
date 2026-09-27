import os, random
import numpy as np
from PIL import Image, ImageFilter

random.seed(2026)
FLAG = "cebroid{crop_h1des_d4t4}"

# 1. build a large "photograph-like" texture (smooth noise, believable as a scan)
BIG_W, BIG_H = 1600, 1600
noise = np.random.default_rng(5).integers(0, 256, (BIG_H, BIG_W, 3), dtype=np.uint8)
big = Image.fromarray(noise, "RGB").filter(ImageFilter.GaussianBlur(radius=6))
big = big.convert("RGB")

# 2. choose the crop region (this is what "survives" the crop)
CROP_X, CROP_Y, CROP_W, CROP_H = 640, 480, 400, 300
crop_box = (CROP_X, CROP_Y, CROP_X + CROP_W, CROP_Y + CROP_H)

# 3. embed the flag via LSB, but ONLY within the pixels that fall inside the crop box
payload = FLAG.encode() + b"\x00"
bits = "".join(f"{b:08b}" for b in payload)
assert len(bits) <= CROP_W * CROP_H

px = big.load()
idx = 0
for y in range(CROP_Y, CROP_Y + CROP_H):
    for x in range(CROP_X, CROP_X + CROP_W):
        if idx >= len(bits):
            break
        r, g, b = px[x, y]
        r = (r & ~1) | int(bits[idx])
        px[x, y] = (r, g, b)
        idx += 1
    if idx >= len(bits):
        break

# 4. crop and save — this is the only file players receive
cropped = big.crop(crop_box)
out_path = "/home/claude/challenges/missingpiece.png"
cropped.save(out_path)
print("missingpiece.png written:", cropped.size, os.path.getsize(out_path))
