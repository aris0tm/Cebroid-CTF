# Cybroid — Binary & Exploitation Track

Five challenges, deliberately mixed languages so beginners see the same
class of bug ("the program trusts input it shouldn't") show up in very
different-looking code.

Category name note: three of these (PWN01, PWN03, PWN05) are classic
compiled-binary memory-corruption pwn. PWN02 is a scripting-language
command injection, and PWN04 is a pure logic/arithmetic flaw with no
memory corruption at all. Experienced players will reasonably push back
on calling #2 and #4 "Pwn." Recommend renaming the section **"Binary &
Exploitation"** rather than strictly "Pwn" — that's what's used below
and in each challenge header.

| ID | Name | Language | Vulnerability | Difficulty |
|----|------|----------|----------------|------------|
| PWN01 | Percentage Panic | C | Stack overflow (overwrite adjacent flag) | Easy |
| PWN02 | System Diagnostics | Python | OS command injection | Easy |
| PWN03 | Message Terminal | C++ | Format string (memory disclosure) | Easy |
| PWN04 | Access System | Rust | Integer wraparound / logic flaw | Medium |
| PWN05 | User Management | C | Controlled use-after-free → function pointer hijack | Medium |

## Layout

Each challenge directory is self-contained and CTFd-Whale-friendly:

```
PWNxx-name/
  chall.{c,cpp,py}  or  src/main.rs + Cargo.toml   <- source, flag NOT hardcoded
  Dockerfile                                        <- builds + serves on one port
  flag.txt                                          <- REPLACE before deploying
```

Every `flag.txt` currently contains an obvious placeholder like:

```
CYBROID{REPLACE_ME_<challenge>_placeholder}
```

Swap those for the real flags before you build images. Do not commit
real flags to the same repo/zip you hand to players — keep a private
`flag.txt` overlay and inject it at build time (CI secret, `.gitignore`,
or CTFd-Whale's per-instance flag templating if you want unique flags
per team).

## Build & run everything locally

```bash
docker compose build
docker compose up -d
```

Ports: PWN01→9001, PWN02→9002, PWN03→9003, PWN04→9004, PWN05→9005.
All are served over `socat` with a PTY so `nc host port` works directly
for players.

## Per-challenge notes for your writers/testers

**PWN01 — Percentage Panic (C, stack overflow)**
- Compiled with `-fno-stack-protector -no-pie` on purpose — no canary,
  fixed load address, so overflowing `name[32]` to flip the adjacent
  `is_admin` int is a clean, deterministic win. No ASLR-defeat needed.
- Verified locally: 32 filler bytes + 4 bytes of `\x01\x00\x00\x00`
  flips the flag and prints the flag file.
- If you want it harder, switch the win condition to overwriting the
  saved return address to jump to `print_flag()` instead of just
  flipping a bool — same binary, one difficulty knob.

**PWN02 — System Diagnostics (Python, command injection)**
- `os.system("ping -c 1 -W 1 " + host)` — any shell metacharacter in
  `host` works: `; cat flag.txt`, `&& cat flag.txt`, `$(cat flag.txt)`,
  backticks, etc. Deliberately no allowlist/regex validation.
- Flag lives in `flag.txt` next to the script, not in source — so
  reading the source (if leaked) doesn't spoil the challenge.

**PWN03 — Message Terminal (C++, format string)**
- Bug is exactly `printf(msg.c_str())` instead of `printf("%s", ...)`.
- Verified locally that `%x` chains leak raw stack words back to the
  player immediately.
- The flag is loaded into a stack-local `std::string` specifically so
  it's in the leakable region; if you want a `%n`-write-based variant
  instead of a `%s`/`%x`-read leak, that's a natural "hard" follow-up
  challenge later in the season.

**PWN04 — Access System (Rust, integer wraparound)**
- The whole bug is Rust's *actual default*: `cargo build --release`
  disables overflow checks. `credits: u8` starting at 3, spend it down
  to 0, one more spend wraps to 255, which is the admin-unlock value.
- Verified locally end-to-end: swipe 4 times from a start of 3 credits
  reaches 255 and unlocks the flag.
- No unsafe blocks, no pointers, nothing "un-Rust-like" — that's the
  point of putting this under Binary & Exploitation rather than Misc:
  it's still a released, compiled binary with a real exploitable state
  transition, just not a memory-safety bug.

**PWN05 — User Management (C, controlled UAF)**
- Built as a *controlled* UAF per your note: `struct User` and
  `struct Note` are the same size, so freeing the user and then
  allocating a note reliably reclaims the same tcache chunk
  (single-threaded, small object, no other allocations racing it).
- The note's raw bytes alias the user struct's `print_profile`
  function pointer, and the menu lets the player supply that value
  directly as a decimal number — no shellcode, no ROP, just "put a
  known address where a function pointer used to be."
- Ships with `LEAK_WIN_ADDR` on (menu option 5 prints `win()`'s
  address) so it's solvable purely as a UAF/hijack concept without
  also requiring a separate infoleak. Flip that macro to 0 later in
  the season and players instead pull the address from `objdump -d`
  since the binary is `-no-pie`.
- Verified locally end-to-end with a scripted exploit: create → delete
  → leak → note with fake pointer → view profile → `win()` fires and
  prints the flag.

## Suggested playtesting order before CTFd import

1. `docker compose build` — confirms every Dockerfile still builds
   clean on a fresh machine (don't trust your dev box's cached layers).
2. `nc localhost <port>` each challenge manually once, blind, as if
   you were a player who's never seen the source.
3. Swap placeholder flags for real ones, rebuild, re-test the intended
   solve path one more time against the rebuilt images specifically —
   this catches the classic "flag file didn't get copied into the new
   image" mistake.
4. Only then zip up the distributable (source + Dockerfile, no
   `flag.txt`) for CTFd-Whale.
