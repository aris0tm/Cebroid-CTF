# cebroid — Binary & Exploitation Track

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
cebroid{REPLACE_ME_<challenge>_placeholder}
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

