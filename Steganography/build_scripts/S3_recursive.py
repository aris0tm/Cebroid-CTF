import os, base64, random, subprocess, zipfile
from PIL import Image, PngImagePlugin

random.seed(7)
FLAG = "cebroid{l4y3rs_upon_l4y3rs}"
B64 = base64.b64encode(FLAG.encode()).decode()
PASSWORD = "d33p3r"

# ---------- Layer 3/4: second.png with LSB-encoded base64 string ----------
W, H = 200, 200
img2 = Image.new("RGB", (W, H))
px2 = img2.load()
for y in range(H):
    for x in range(W):
        px2[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

payload = B64.encode() + b"\x00"  # null-terminated
bits = "".join(f"{b:08b}" for b in payload)
assert len(bits) <= W * H, "image too small for payload"

idx = 0
for y in range(H):
    for x in range(W):
        if idx >= len(bits):
            break
        r, g, b = px2[x, y]
        r = (r & ~1) | int(bits[idx])
        px2[x, y] = (r, g, b)
        idx += 1
    if idx >= len(bits):
        break

second_path = "/home/claude/build/_rec_second.png"
img2.save(second_path)

# ---------- Layer 2: zip up second.png (password protected) ----------
inner_zip = "/home/claude/build/_rec_inner.zip"
if os.path.exists(inner_zip):
    os.remove(inner_zip)
subprocess.run(
    ["zip", "-j", "-P", PASSWORD, inner_zip, second_path],
    check=True, cwd="/home/claude/build", capture_output=True
)

# ---------- Layer 1: outer PNG with metadata clue + appended zip ----------
outer_img = Image.new("RGB", (500, 350), (30, 30, 30))
opx = outer_img.load()
for y in range(350):
    for x in range(500):
        opx[x, y] = (x % 256, y % 256, (x + y) % 256)

meta = PngImagePlugin.PngInfo()
meta.add_text("Comment", "look_deeper")
meta.add_text("Author", PASSWORD)

outer_path = "/home/claude/build/_rec_outer.png"
outer_img.save(outer_path, pnginfo=meta)

with open(outer_path, "rb") as f:
    outer_bytes = f.read()
with open(inner_zip, "rb") as f:
    zip_bytes = f.read()

final_path = "/home/claude/challenges/recursive.png"
with open(final_path, "wb") as f:
    f.write(outer_bytes)
    f.write(bytes(random.randint(0, 255) for _ in range(64)))
    f.write(zip_bytes)

Image.open(final_path).verify()
print("recursive.png written:", os.path.getsize(final_path))
print("password:", PASSWORD)
print("base64 in second.png:", B64)
