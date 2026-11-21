# Cebroid-CTF

## Overview

Welcome to **Cebroid-CTF**, a Capture The Flag (CTF) repository containing security challenges, source files, deployment setups, and/or writeups designed to test and sharpen cybersecurity skills.

* **Date:** 10/10/2026
* **Repository:** [aris0tm/Cebroid-CTF](https://github.com/aris0tm/Cebroid-CTF)
* **Authors:**
  * [@aris0tm](https://github.com/aris0tm)
  * [@Zeus0tm](https://github.com/Zeus0tm)
  * [@sarathi377](https://github.com/sarathi377)

## Challenge Categories

This repository covers challenges across multiple cybersecurity domains:

| Category | Description |
| :--- | :--- |
| **Web** | Web application vulnerabilities |
| **Crypto** | Classical and modern cryptography puzzles |
| **Reverse Engineering** | Binary analysis, decompilation, and malware-style puzzles |
| **Pwn / Binary** | Memory corruption, buffer overflows, and exploitation |
| **Forensics** | Packet captures, memory dumps, steganography, and file analysis |
| **OSINT** | Open-source intelligence and investigative challenges |
| **Misc** | Scripting, logic puzzles, and hybrid tasks |

*(Edit or remove categories above to match the actual challenges in your repository.)*

## Repository Structure

```text
Cebroid-CTF/
├── web/                # Web exploitation challenges
├── crypto/             # Cryptography challenges
├── rev/                # Reverse engineering challenges
├── pwn/                # Binary exploitation challenges
├── forensics/          # Digital forensics challenges
├── misc/               # Miscellaneous challenges
├── writeups/           # Official solutions & walkthroughs
└── README.md
```

## Getting Started

### Prerequisites

Ensure you have the required tools installed depending on the challenges you want to run or solve:

* `git`
* `docker` & `docker-compose` *(if deploying containerized challenges)*
* `python3` *(for scripts and exploits)*

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/aris0tm/Cebroid-CTF.git
cd Cebroid-CTF
```

If challenges use Docker, navigate to a specific challenge directory and start it:

```bash
cd <category>/<challenge-name>
docker compose up -d
```

## Flag Format

Unless specified otherwise in a challenge description, all flags follow this standard format:

```text
CEBROID{example_flag_here}
```

## Rules & Ethics

* Do not attack any infrastructure outside the designated CTF scope.
* Do not share flags publicly while an event is active.
* Use all techniques and tools responsibly and strictly for educational purposes.

## Contributing

Contributions, bug fixes, and community writeups are welcome!

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-challenge`).
3. Commit your changes (`git commit -m "Add new challenge"`).
4. Push to the branch (`git push origin feature/new-challenge`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

*Last updated: 10/10/2026*
