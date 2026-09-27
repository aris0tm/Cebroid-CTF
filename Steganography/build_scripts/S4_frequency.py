import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import istft
from scipy.io import wavfile

FLAG = "cebroid{s33_th3_sound}"
FS = 10000          # sample rate
NPERSEG = 256        # -> 129 freq bins, 0..5000 Hz
NFREQ = NPERSEG // 2 + 1

# ---- render flag text to a bitmap: rows=freq bins, cols=time frames ----
NTIME = 700
txt_img = Image.new("L", (NTIME, NFREQ), 0)
draw = ImageDraw.Draw(txt_img)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 34)
except Exception:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), FLAG, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(((NTIME - tw) / 2 - bbox[0], (NFREQ - th) / 2 - bbox[1]), FLAG, fill=255, font=font)

# flip vertically: image row 0 (top) should map to HIGH frequency bin
arr = np.array(txt_img, dtype=np.float64) / 255.0
arr = arr[::-1, :]   # now row 0 = low freq, matches STFT bin ordering

# keep text out of very low/high bins so it's not trivially visible in raw waveform
mag = arr * 40.0     # magnitude scale

# random phase, symmetric enough for istft to produce real-valued audio
rng = np.random.default_rng(99)
phase = rng.uniform(-np.pi, np.pi, size=mag.shape)
Zxx = mag * np.exp(1j * phase)

_, audio = istft(Zxx, fs=FS, nperseg=NPERSEG, noverlap=NPERSEG // 2)

# normalize and add background noise/static so it "sounds like nothing"
audio = audio / (np.max(np.abs(audio)) + 1e-9)
noise = rng.normal(0, 0.08, size=audio.shape)
final = audio * 0.6 + noise
final = final / (np.max(np.abs(final)) + 1e-9) * 0.9

pcm = np.int16(final * 32767)
wavfile.write("/home/claude/challenges/frequency.wav", FS, pcm)
print("frequency.wav written, duration:", len(pcm) / FS, "s")
