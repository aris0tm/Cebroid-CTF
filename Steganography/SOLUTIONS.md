# Cybroid 2K26 — Steganography Track: Solutions

All flags use the prefix `cebroid{...}`.

---

## 1. Scattered — `scattered.png`
**Flag:** `cebroid{sc4tter3d_l3tt3rs}`

512×512 white PNG with 26 non-white pixels scattered at random `(x, y)`.
Each non-white pixel's RGB value equals the ASCII code of one flag
character, repeated across R/G/B (e.g. `c` = 99 → `(99,99,99)`).
Reading order is encoded by ascending **X coordinate**.

**Solve:**
```python
from PIL import Image
img = Image.open("scattered.png")
px = img.load()
hits = []
for y in range(img.height):
    for x in range(img.width):
        r, g, b = px[x, y][:3]
        if (r, g, b) != (255, 255, 255):
            hits.append((x, chr(r)))
hits.sort()
print("".join(c for _, c in hits))
```

---

## 2. Dead Space — `deadspace.png`
**Flag:** `cebroid{tr41l1ng_byt3s}`

A normal, valid PNG (gradient image), followed by 128 random padding
bytes, followed by a ZIP archive (`note.txt` containing the flag)
appended directly after the file's real PNG data. The PNG itself
displays and validates fine — the payload lives in the "dead space"
after `IEND`.

**Solve:**
```bash
binwalk deadspace.png            # or: strings/xxd to find the PK\x03\x04 signature
dd if=deadspace.png bs=1 skip=<zip_offset> of=payload.zip
unzip payload.zip && cat note.txt
```

---

## 3. Recursive — `recursive.png`
**Flag:** `cebroid{l4y3rs_upon_l4y3rs}`

Four layers:
1. `exiftool recursive.png` → PNG text chunks `Comment: look_deeper`,
   `Author: d33p3r` (the password).
2. A ZIP is appended after the PNG data (same trick as Dead Space) —
   extract it with `binwalk -e` or by locating the `PK\x03\x04` header.
   It's password-protected with `d33p3r` and contains `second.png`.
3. `second.png` hides a null-terminated Base64 string in the LSB of
   the red channel, read row-major from `(0,0)`.
4. Base64-decode the extracted string → flag.

**Solve:**
```bash
exiftool recursive.png                       # get password: d33p3r
python3 -c "
data = open('recursive.png','rb').read()
open('inner.zip','wb').write(data[data.find(b'PK\x03\x04'):])
"
unzip -P d33p3r inner.zip                    # -> second.png
```
```python
from PIL import Image
import base64
img = Image.open("second.png"); px = img.load()
bits = bytearray(); byte = ""
for y in range(img.height):
    for x in range(img.width):
        byte += str(px[x, y][0] & 1)
        if len(byte) == 8:
            v = int(byte, 2); byte = ""
            if v == 0: raise SystemExit(base64.b64decode(bytes(bits)).decode())
            bits.append(v)
```

---

## 4. Frequency — `frequency.wav`
**Flag:** `cebroid{s33_th3_sound}`

~9s WAV that sounds like static. The flag text is rendered as a
bitmap and used as the STFT magnitude spectrogram (0–5000 Hz band),
with random phase reconstructed via inverse STFT, then mixed with
background noise at 60/40 to keep the waveform itself unremarkable.

**Solve:** Open in Audacity or Sonic Visualiser → switch to
Spectrogram view → read the text directly (visible roughly in the
1–4 kHz band).

```python
# quick check via scipy
import numpy as np, matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft
fs, data = wavfile.read("frequency.wav")
f, t, Z = stft(data.astype(float), fs=fs, nperseg=256, noverlap=128)
plt.pcolormesh(t, f, np.abs(Z), cmap="inferno"); plt.ylim(0, 5000); plt.show()
```

---

## 5. Missing Piece — `missingpiece.png`
**Flag:** `cebroid{crop_h1des_d4t4}`

400×300 crop cut from a larger 1600×1600 "photo" (blurred noise
texture, so it plausibly looks like a scan/screenshot). The flag was
LSB-embedded (red channel) only within the region that ended up
inside the crop, so the surviving PNG carries the full payload
starting at pixel `(0,0)`.

**Solve:** same LSB routine as Recursive's Layer 3 — read the R
channel LSB row-major from the top-left corner until the null
terminator.

---

## Build notes
All five files were generated programmatically (Pillow / NumPy /
SciPy) — see the accompanying `build/` scripts if you want to
regenerate with different flags or difficulty tuning (e.g. bump the
`Frequency` noise ratio, or add more layers to `Recursive`).
