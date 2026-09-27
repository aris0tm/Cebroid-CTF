# Illustrative only — shows how encrypted.bmp was produced (AES-128-ECB on raw pixel data)
from Crypto.Cipher import AES
key = b"<REDACTED - not needed to solve>"
with open("original.bmp","rb") as f:
    data = f.read()
header, pixels = data[:54], data[54:]
cipher = AES.new(key, AES.MODE_ECB)
enc = cipher.encrypt(pixels)
with open("encrypted.bmp","wb") as f:
    f.write(header + enc)
