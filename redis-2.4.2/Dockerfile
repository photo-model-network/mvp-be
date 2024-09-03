FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
    build-essential \
    tcl \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget http://download.redis.io/releases/redis-2.4.2.tar.gz && \
    tar xzf redis-2.4.2.tar.gz && \
    cd redis-2.4.2 && \
    make && \
    make install

CMD ["redis-server"]
