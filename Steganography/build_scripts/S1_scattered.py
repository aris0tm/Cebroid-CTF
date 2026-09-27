import random
from PIL import Image

FLAG = "cebroid{sc4tter3d_l3tt3rs}"
random.seed(1337)

W, H = 512, 512
img = Image.new("RGB", (W, H), (255, 255, 255))
px = img.load()

# choose ascending x-coordinates so left-to-right reading order == flag order
xs = sorted(random.sample(range(10, W - 10), len(FLAG)))
for ch, x in zip(FLAG, xs):
    y = random.randint(10, H - 10)
    v = ord(ch)
    px[x, y] = (v, v, v)

img.save("/home/claude/challenges/scattered.png")
print("scattered.png written, chars:", len(FLAG))
