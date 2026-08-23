FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/chall chall
WORKDIR /home/chall

COPY chall.cpp .
RUN g++ -o chall chall.cpp -fno-stack-protector -no-pie -w \
    && rm chall.cpp

COPY flag.txt /home/chall/flag.txt
RUN chown chall:chall /home/chall/flag.txt && chmod 400 /home/chall/flag.txt

USER chall
EXPOSE 9003
CMD ["socat", "-T30", "TCP-LISTEN:9003,reuseaddr,fork", "EXEC:/home/chall/chall,pty,stderr"]
