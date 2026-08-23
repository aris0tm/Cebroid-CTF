FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/chall chall
WORKDIR /home/chall

COPY chall.c .
# Beginner-friendly binary: no stack canary, no PIE, so a plain
# overflow onto is_admin is enough. Keep NX on if you don't want
# shellcode-on-stack to also be viable; turn it off if you do.
RUN gcc -o chall chall.c -fno-stack-protector -no-pie -w \
    && rm chall.c

# Real flag goes here at deploy time - NEVER bake the real flag into
# the image you hand out for local testing/CI.
COPY flag.txt /home/chall/flag.txt
RUN chown chall:chall /home/chall/flag.txt && chmod 400 /home/chall/flag.txt

USER chall
EXPOSE 9001
CMD ["socat", "-T30", "TCP-LISTEN:9001,reuseaddr,fork", "EXEC:/home/chall/chall,pty,stderr"]
