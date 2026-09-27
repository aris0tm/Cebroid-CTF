#!/usr/bin/env python3
"""
Run this locally to check whether a (message, token) pair is valid,
i.e. whether token == SHA256(secret + message) for the server's secret.
It will NOT reveal the secret. If it prints "ACCESS GRANTED" for a
message containing "admin=true", you've won.

Usage: python3 verify.py <message_hex> <token_hex>
"""
import hashlib, sys

SECRET = bytes.fromhex("9a3c75d3ba2d7186c455ddd53c71514a")  # only used locally to check, never printed

def check(message: bytes, token_hex: str) -> bool:
    return hashlib.sha256(SECRET + message).hexdigest() == token_hex

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 verify.py <message_hex> <token_hex>")
        sys.exit(1)
    message = bytes.fromhex(sys.argv[1])
    token_hex = sys.argv[2]
    if check(message, token_hex):
        if b"admin=true" in message:
            print("ACCESS GRANTED - admin token accepted")
            print("cebroid{hash_me_outside}")
        else:
            print("Token valid, but no admin privileges requested.")
    else:
        print("Invalid token.")
