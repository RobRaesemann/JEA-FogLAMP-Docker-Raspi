FROM schachr/raspbian-stretch
#
# FogLAMP on Raspberry PI 
# TODO: Find an official Raspian Stretch image or build from scratch


# Install packages required for FogLAMP
RUN apt-get update && apt-get install -y \
    apt-utils \
    autoconf \ 
    automake \
    avahi-daemon \
    build-essential \
    cmake \
    curl \
    g++ \
    git \
    libboost-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libpq-dev \
    libsqlite3-dev \
    libssl-dev \
    libtool \
    libz-dev \
    make \
    postgresql \
    python3-dev \
    python3-pip \
    python3-dbus \
    python3-setuptools \
    rsyslog \
    sqlite3 \
    uuid-dev \
&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/foglamp/FogLAMP.git /foglamp

WORKDIR /foglamp
RUN make
RUN make install

RUN mkdir -p /usr/local/foglamp/python/foglamp/plugins/north/http_north
COPY http_north /usr/local/foglamp/python/foglamp/plugins/north/http_north

RUN mkdir -p /usr/local/foglamp/plugins/south/Random
COPY Random /usr/local/foglamp/plugins/south/Random

WORKDIR /usr/local/foglamp
COPY foglamp.sh foglamp.sh

VOLUME /usr/local/foglamp/data

# FogLAMP API port
EXPOSE 8081

# start rsyslog, FogLAMP, and tail syslog
CMD ["bash", "./foglamp.sh"]

LABEL maintainer="rob@raesemann.com" \
      author="Raesemann" \
      target="Raspberry PI" \
      version="0.1-beta" \