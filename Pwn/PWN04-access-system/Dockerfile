FROM rust:1.75-slim AS build
WORKDIR /build
COPY Cargo.toml .
COPY src ./src
RUN cargo build --release

FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/chall chall
WORKDIR /home/chall

COPY --from=build /build/target/release/chall /home/chall/chall
COPY flag.txt /home/chall/flag.txt
RUN chown chall:chall /home/chall/flag.txt /home/chall/chall && chmod 400 /home/chall/flag.txt

USER chall
EXPOSE 9004
CMD ["socat", "-T60", "TCP-LISTEN:9004,reuseaddr,fork", "EXEC:/home/chall/chall,pty,stderr"]
