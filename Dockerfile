FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    strace \
    tcpdump \
    iproute2 \
    iputils-ping \
    net-tools \
    procps \
 && rm -rf /var/lib/apt/lists/*


COPY . .

CMD ["bash"]
