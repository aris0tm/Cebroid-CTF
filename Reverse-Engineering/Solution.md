# CTF Reverse Engineering Solution Guide

This document provides a comprehensive solution writeup and reverse engineering methodology for all 5 CTF challenges in the suite.

---

## 1. Challenge 1: Obfuscated JavaScript

* **Target Output:** `cebroid{7h3_m461c_0f_08fuc1c4710n}`
* **Format:** Raw JavaScript Snippet

### Analysis & Reversing

The obfuscated code relies on two main techniques:

1. **Property Lookup Obfuscation:** String property `fromCharCode` is accessed via Unicode escape sequence (`'\u0066\u0072\u006F\u006D\u0043\u0068\u0061\u0072\u0043\u006F\u0064\u0065'`).
2. **Bitwise XOR Encoding:** Character ASCII values are hidden behind XOR operations between paired integer values (e.g., `460449 ^ 460514`).

### Solution Methods

* **Method A (Dynamic Execution):** Execute the expression inside any JavaScript console (Node.js or Browser V8) wrapped in a `console.log()` statement.
* **Method B (Static Evaluation):** Evaluate each XOR pair statically:
* $460449 \oplus 460514 = 67 \rightarrow \text{'C'}$
* $552002 \oplus 551995 = 121 \rightarrow \text{'y'}$
* $373704 \oplus 373674 = 98 \rightarrow \text{'b'}$



### Python Solver

```python
pairs = [
    (460449, 460514), (552002, 551995), (373704, 373674), (253808, 253698),
    (384062, 384081), (683421, 683508), (675825, 675733), (363310, 363349),
    (763002, 762957), (428437, 428541), (352372, 352327), (215279, 215216),
    (964674, 964655), (535875, 535927), (881799, 881841), (699222, 699239),
    (422935, 423028), (762875, 762788), (721573, 721557), (624140, 624234),
    (211428, 211387), (591705, 591721), (628458, 628434), (858579, 858549),
    (611580, 611465), (928464, 928435), (849834, 849819), (970818, 970785),
    (903110, 903154), (372742, 372785), (274292, 274245), (655445, 655461),
    (344546, 344460), (837892, 838009)
]

flag = "".join(chr(a ^ b) for a, b in pairs)
print("[+] JS Flag:", flag)

```

---

## 2. Challenge 2: Relocatable C Object File

* **Flag:** `cebroid{607_fr0m_C}`
* **Format:** Relocatable Object File (`challenge.o`)

### Analysis & Reversing

Opening `challenge.o` in Ghidra reveals the decompiled `decode_payload` routine:

```c
void decode_payload(long input_ptr, long output_ptr, ulong len) {
  ulong i = 0;
  while (i < len) {
    *(byte *)(output_ptr + i) = *(byte *)(input_ptr + i) ^ (byte)i + 0x60;
    i = i + 1;
  }
}

```

The ciphertext array in `.rodata` is 19 bytes long:
`0x23, 0x18, 0x01, 0x11, 0x09, 0x01, 0x03, 0x1C, 0x5E, 0x56, 0x50, 0x36, 0x4E, 0x5B, 0x1A, 0x44, 0x35, 0x69, 0x6A`

### Transformation Formula

$$\text{Output}[i] = \text{Cipher}[i] \oplus ((i + 0\text{x}60) \pmod{256})$$

### Python Solver

```python
cipher = [
    0x23, 0x18, 0x01, 0x11, 0x09, 0x01, 0x03, 0x1C, 
    0x5E, 0x56, 0x50, 0x36, 0x4E, 0x5B, 0x1A, 0x44, 
    0x35, 0x69, 0x6A
]

flag = "".join(chr(b ^ ((i + 0x60) & 0xFF)) for i, b in enumerate(cipher))
print("[+] C Object Flag:", flag)

```

---

## 3. Challenge 3: Java Compiled Bytecode

* **Flag:** `cebroid{r3v3r51n6_j4v44}`
* **Format:** Java Compiled Class (`JavaChallenge.class`)

### Analysis & Reversing

Decompiling `JavaChallenge.class` using `cfr` or `jd-gui` reveals the validation logic:

```java
private static boolean validateKey(String inputKey) {
    if (inputKey.length() != 4) return false;
    int check = 0;
    for (int i = 0; i < inputKey.length(); i++) {
        check += (inputKey.charAt(i) ^ (i * 0x07));
    }
    return check == 263;
}

```

1. **Passcode Derivation:** Solving the checksum constraint for a 4-character string yields `inputKey = "J4V4"`.
2. **Key Offset:** The decryption loop uses `baseKey = args[0].charAt(0)`, which corresponds to `'J'` (`0x4A`).
3. **Decryption Expression:**

$$\text{Flag}[i] = \text{ENCRYPTED\_FLAG}[i] \oplus \text{0x4A} \oplus (i \pmod{16})$$



### Python Solver

```python
encrypted = [
    0x01, 0x3B, 0x30, 0x30, 0x2D, 0x2B, 0x26, 0x39, 0x31, 
    0x71, 0x3B, 0x73, 0x31, 0x30, 0x77, 0x74, 0x3C, 0x2C, 0x32, 0x30, 0x3C
]

base_key = ord('J')  # 0x4A
flag = "".join(chr(b ^ base_key ^ (i & 0x0F)) for i, b in enumerate(encrypted))
print("[+] Java Flag:", flag)

```

---

## 4. Challenge 4: Python Bytecode

* **Flag:** `cebroid{py7h0n_h45_08jc0d3??}`
* **Format:** Python Bytecode (`py_challenge.pyc`)

### Analysis & Reversing

Disassembling `py_challenge.pyc` using Python's `dis` module reveals the key check and array mapping:

```python
if len(passkey) != 3 or sum(ord(c) for c in passkey) != 248:
    return "Access Denied"

```

1. **Passcode Derivation:** The passkey requires 3 ASCII characters summing to `248`, resolving to `"PY3"`.
2. **Salt Offset:** `salt = ord(passkey[0])` uses `'P'` (`0x50`).
3. **Transformation Formula:**

$$\text{Flag}[i] = \text{ENCRYPTED\_FLAG}[i] \oplus \text{0x50} \oplus ((i \times 3) \pmod{256})$$



### Python Solver

```python
encrypted = [
    0x23, 0x18, 0x00, 0x10, 0x0c, 0x0a, 0x07, 0x1e,
    0x15, 0x1d, 0x50, 0x30, 0x08, 0x21, 0x5a, 0x31,
    0x53, 0x56, 0x30, 0x22, 0x3d, 0x38, 0x30, 0x32,
    0x20, 0x38, 0x76, 0x7a
]

salt = ord('P')  # 0x50
flag = "".join(chr(b ^ salt ^ ((i * 3) & 0xFF)) for i, b in enumerate(encrypted))
print("[+] Python Flag:", flag)

```

---

## 5. Challenge 5: Native Executable Binary

* **Flag:** `cebroid{F146_Fr0m_81n4ry}`
* **Format:** Executable Binary File (`challenge.bin`)

### Analysis & Reversing

Disassembling `challenge.bin` in GDB, IDA, or Ghidra shows a single-byte XOR loop inside `print_decoded_flag`:

```c
for (int i = 0; i < 25; i++) {
    flag_buffer[i] = BINARY_PAYLOAD[i] ^ 0x40;
}

```

* **XOR Mask:** `0x40` ($64_{10}$)
* **Payload Offset:** Extracted directly from `.rodata` section.

### Python Solver

```python
payload = [
    0x03, 0x39, 0x22, 0x32, 0x2F, 0x29, 0x24, 0x3B,
    0x06, 0x71, 0x74, 0x76, 0x1F, 0x06, 0x32, 0x70,
    0x2D, 0x1F, 0x78, 0x71, 0x2E, 0x74, 0x32, 0x39,
    0x3D
]

flag = "".join(chr(b ^ 0x40) for b in payload)
print("[+] Binary Flag:", flag)

```

---

## Unified Master Solver Script (`solve_all.py`)

Run this single Python script to verify all 5 decoded flags at once:

```python
#!/usr/bin/env python3

def solve_js():
    pairs = [
        (460449, 460514), (552002, 551995), (373704, 373674), (253808, 253698),
        (384062, 384081), (683421, 683508), (675825, 675733), (363310, 363349),
        (763002, 762957), (428437, 428541), (352372, 352327), (215279, 215216),
        (964674, 964655), (535875, 535927), (881799, 881841), (699222, 699239),
        (422935, 423028), (762875, 762788), (721573, 721557), (624140, 624234),
        (211428, 211387), (591705, 591721), (628458, 628434), (858579, 858549),
        (611580, 611465), (928464, 928435), (849834, 849819), (970818, 970785),
        (903110, 903154), (372742, 372785), (274292, 274245), (655445, 655461),
        (344546, 344460), (837892, 838009)
    ]
    return "".join(chr(a ^ b) for a, b in pairs)

def solve_c_obj():
    cipher = [
        0x23, 0x18, 0x01, 0x11, 0x09, 0x01, 0x03, 0x1C, 
        0x5E, 0x56, 0x50, 0x36, 0x4E, 0x5B, 0x1A, 0x44, 
        0x35, 0x69, 0x6A
    ]
    return "".join(chr(b ^ ((i + 0x60) & 0xFF)) for i, b in enumerate(cipher))

def solve_java():
    encrypted = [
        0x01, 0x3B, 0x30, 0x30, 0x2D, 0x2B, 0x26, 0x39, 0x31, 
        0x71, 0x3B, 0x73, 0x31, 0x30, 0x77, 0x74, 0x3C, 0x2C, 0x32, 0x30, 0x3C
    ]
    return "".join(chr(b ^ ord('J') ^ (i & 0x0F)) for i, b in enumerate(encrypted))

def solve_python():
    encrypted = [
        0x23, 0x18, 0x00, 0x10, 0x0c, 0x0a, 0x07, 0x1e,
        0x15, 0x1d, 0x50, 0x30, 0x08, 0x21, 0x5a, 0x31,
        0x53, 0x56, 0x30, 0x22, 0x3d, 0x38, 0x30, 0x32,
        0x20, 0x38, 0x76, 0x7a
    ]
    return "".join(chr(b ^ ord('P') ^ ((i * 3) & 0xFF)) for i, b in enumerate(encrypted))

def solve_binary():
    payload = [
        0x03, 0x39, 0x22, 0x32, 0x2F, 0x29, 0x24, 0x3B,
        0x06, 0x71, 0x74, 0x76, 0x1F, 0x06, 0x32, 0x70,
        0x2D, 0x1F, 0x78, 0x71, 0x2E, 0x74, 0x32, 0x39,
        0x3D
    ]
    return "".join(chr(b ^ 0x40) for b in payload)

if __name__ == "__main__":
    print("=== CTF Master Solution Suite ===")
    print(f"[1] JavaScript Flag : {solve_js()}")
    print(f"[2] C Object Flag   : {solve_c_obj()}")
    print(f"[3] Java Class Flag : {solve_java()}")
    print(f"[4] Python PYC Flag : {solve_python()}")
    print(f"[5] Binary .bin Flag: {solve_binary()}")

```