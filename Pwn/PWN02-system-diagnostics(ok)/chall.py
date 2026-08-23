#!/usr/bin/env python3
"""
PWN02 - System Diagnostics
Category: Binary & Exploitation (Python) - Command Injection
Difficulty: Easy

Story: A "network diagnostics" tool that lets you ping a host. It builds
a shell command by string-concatenating your input, so anything you type
after the hostname runs too.

Intended solution:
    Enter host: 127.0.0.1; cat flag.txt
    Enter host: 127.0.0.1 && cat flag.txt
    Enter host: $(cat flag.txt)
    ...any of the classic shell-injection separators work.

The flag itself is never in this source file - it lives in flag.txt on
the challenge host, which the injected command reveals.
"""

import os
import sys


BANNER = r"""
=== SYSTEM DIAGNOSTICS TERMINAL ===
Authorized use only. All commands are logged (not really).
"""


def run_ping(host: str) -> None:
    # Deliberately vulnerable: naive string concatenation into a shell
    # command instead of using subprocess with a list + shell=False.
    command = "ping -c 1 -W 1 " + host
    print(f"[*] Running: {command}")
    os.system(command)


def main() -> None:
    print(BANNER)
    try:
        host = input("Enter host to ping: ").strip()
    except EOFError:
        sys.exit(0)

    if not host:
        print("No host provided.")
        return

    run_ping(host)


if __name__ == "__main__":
    main()
