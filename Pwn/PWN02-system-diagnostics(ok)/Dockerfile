FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/chall chall
WORKDIR /home/chall

COPY chall.py .
COPY flag.txt /home/chall/flag.txt
RUN chown chall:chall /home/chall/flag.txt && chmod 400 /home/chall/flag.txt

USER chall
EXPOSE 9002
CMD ["socat", "-T30", "TCP-LISTEN:9002,reuseaddr,fork", "EXEC:python3 /home/chall/chall.py,pty,stderr"]
