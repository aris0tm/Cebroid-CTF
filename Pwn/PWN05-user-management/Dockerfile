FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/chall chall
WORKDIR /home/chall

COPY chall.c .
RUN gcc -o chall chall.c -no-pie -w \
    && rm chall.c

COPY flag.txt /home/chall/flag.txt
RUN chown chall:chall /home/chall/flag.txt && chmod 400 /home/chall/flag.txt

USER chall
EXPOSE 9005
CMD ["socat", "-T60", "TCP-LISTEN:9005,reuseaddr,fork", "EXEC:/home/chall/chall,pty,stderr"]
