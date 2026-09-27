#!/usr/bin/env python3
"""
Paddington Bear - local padding oracle.
Run this script; it will decrypt whatever ciphertext you send it (via stdin/args)
and tell you ONLY whether the PKCS#7 padding was valid. Nothing else.

Usage:
    python3 oracle.py <hex_iv_plus_ciphertext>

This never prints the plaintext. It only ever prints "Padding OK" or "Invalid padding".
The key is fixed and NOT included in this file.
"""
import sys
from Crypto.Cipher import AES

KEY = bytes.fromhex("92a846ab6bca2307622d87082239118a")

def check_padding(data: bytes) -> bool:
    if len(data) < 32 or len(data) % 16 != 0:
        return False
    iv, ct = data[:16], data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    pad_len = pt[-1]
    if pad_len == 0 or pad_len > 16:
        return False
    return pt[-pad_len:] == bytes([pad_len]) * pad_len

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 oracle.py <hex_iv_plus_ciphertext>")
        sys.exit(1)
    data = bytes.fromhex(sys.argv[1])
    print("Padding OK" if check_padding(data) else "Invalid padding")
