Yep. If I were designing **Cybroid specifically for your audience**, I'd make the 30 stock + 8 hard like this.

## 30 Stock Challenges

### Web — 7

1. **Source Code** — hidden HTML comment → flag
2. **Robots** — `robots.txt` → hidden endpoint → flag
3. **Cookie Monster** — modify a cookie → access page
4. **IDOR** — change an ID → another user's document
5. **SQL Injection** — login bypass → flag
6. **Path Traversal** — read an unintended file → clue/flag
7. **Upload** — restricted file upload → retrieve flag

### Forensics — 6

8. **Where Am I?** — EXIF GPS → identify location
9. **Wrong Coordinates** — manipulated GPS vs visual evidence
10. **JPEG Layers** — crop → Base64 → decode
11. **Nested Evidence** — crop → Base64 password → ZIP → nested files
12. **The Evidence Drive** — disk image → application package → follow clues
13. **Packet Trail** — PCAP → determine what the victim accessed

### Steganography — 5

14. **Not an Image** — renamed file → inspect actual format
15. **Reversed Signal** — audio → spectrogram/reversal → message
16. **Silent Pixels** — LSB image stego
17. **Attachment** — image → appended ZIP → extract
18. **Layers** — image → archive → encoded text → flag

### Crypto — 5

19. **Caesar's Mistake** — Caesar cipher
20. **Encoded** — Base64/Hex/ROT chain
21. **XOR Me** — single-byte XOR
22. **Repeating Key** — repeating-key XOR
23. **Weak Hash** — identify/crack a weak password hash

### OSINT — 4

24. **Digital Footprint** — username → profile → clue
25. **Where Was This?** — photograph → landmark/location
26. **The Missing Post** — reconstruct information from multiple public sources
27. **Timeline** — several posts/articles → determine the correct event/person/place

### Reverse Engineering — 3

28. **Strings Attached** — strings/inspection → flag
29. **Bytecode** — Python/Java bytecode → reverse → flag
30. **Broken Program** — debug simple program → understand flag generation

---

# 8 Hard Challenges

Here I'd deliberately make the **chain** difficult rather than introducing insane techniques.

### 31. The Rabbit Hole — Web

```text
Recon
 ↓
Hidden endpoint
 ↓
SQLi
 ↓
Credentials
 ↓
Admin panel
 ↓
File upload
 ↓
Shell
 ↓
Flag
```

### 32. Dead Packet — Network/Forensics

```text
PCAP
 ↓
Identify compromised host
 ↓
Follow TCP stream
 ↓
Extract encoded payload
 ↓
Decode
 ↓
Find C2
 ↓
Correlate server logs
 ↓
Flag
```

### 33. The Forgotten Drive — Forensics

```text
Disk image
 ↓
Deleted file
 ↓
Application database
 ↓
Extract artifact
 ↓
Password-protected archive
 ↓
Password hidden elsewhere
 ↓
Flag
```

### 34. Echo — Stego/Audio

```text
Audio
 ↓
Spectrogram
 ↓
Hidden message
 ↓
Decode
 ↓
Second audio artifact
 ↓
Reverse/transform
 ↓
Flag
```

### 35. Broken Cipher — Crypto

```text
Encoded message
 ↓
Identify encoding
 ↓
XOR
 ↓
Recover key
 ↓
Second encrypted artifact
 ↓
Weak crypto implementation
 ↓
Flag
```

### 36. The Machine — Reverse

```text
ELF
 ↓
Strings give false clue
 ↓
Debugger
 ↓
Trace comparison
 ↓
Recover algorithm
 ↓
Reconstruct flag
```

### 37. Ghost Account — OSINT

```text
Username
 ↓
Social profile
 ↓
Image
 ↓
Metadata/location
 ↓
Another account
 ↓
Timeline reconstruction
 ↓
Identify final location/person
 ↓
Flag
```

### 38. CYBROID — Final Boss

This would combine **multiple categories**:

```text
OSINT
   ↓
Find target information
   ↓
Web application
   ↓
Authentication weakness
   ↓
Obtain artifact
   ↓
Forensics
   ↓
Decode evidence
   ↓
Reverse engineering
   ↓
Recover final flag
```

I'd make this one **team-solving oriented**, where different members can work on different branches.

---

## Difficulty distribution

I'd actually make the 30 stock challenges:

```text
Easy       ████████████████  16
Medium     ██████████████    14

Hard       ████████           8
```

So a beginner can immediately solve *something*, while experienced participants have enough depth to separate themselves.

And I'd add **hints with diminishing point penalties**, rather than making hints free:

```text
Challenge: 100 pts

Hint 1 → -10
Hint 2 → -20
Hint 3 → -30
```

That encourages beginners to keep moving instead of abandoning a challenge.

**One design choice I'd strongly make:** don't label the challenges *Easy / Medium / Hard* in the UI. Let the point values and challenge descriptions communicate difficulty. That makes discovery more interesting and prevents people from avoiding something simply because it says "Hard."
