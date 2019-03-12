FROM schachr/raspbian-stretch
#
# FogLAMP on Raspberry PI 
#

# Install packages required for FogLAMP
RUN apt-get update && apt-get upgrade -y  && apt-get install -y --no-install-recommends\
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
    vim \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /foglamp
WORKDIR /foglamp

# Clone the FogLAMP git repository, select the 1.4.2 version, build, and install
RUN git clone https://github.com/foglamp/FogLAMP.git /foglamp \
&& git checkout v1.5.0 \
&& make \
&& make install

ENV FOGLAMP_ROOT=/usr/local/foglamp

# Install HTTP north plugin
RUN mkdir -p /usr/local/foglamp/python/foglamp/plugins/north/http_north
COPY http_north /usr/local/foglamp/python/foglamp/plugins/north/http_north

# Install the random south plugin
RUN mkdir -p /usr/local/foglamp/plugins/south/Random
COPY random_south /usr/local/foglamp/plugins/south/Random

# Install the B100 Modbus plugin
RUN mkdir -p /usr/local/foglamp/plugins/south/b100
COPY b100_south /usr/local/foglamp/python/foglamp/plugins/south/b100

RUN pip3 install -r /usr/local/foglamp/python/foglamp/plugins/south/b100/requirements.txt

# Copy the foglamp startup script and set owner and permissions
WORKDIR /usr/local/foglamp
COPY foglamp.sh foglamp.sh
RUN chown root.staff /usr/local/foglamp/foglamp.sh
RUN chmod 777 /usr/local/foglamp/foglamp.sh

# Create foglamp data volume. This contains the configuration and needs to be preserved between restarts
VOLUME /usr/local/foglamp/data

# FogLAMP API port
EXPOSE 8081

# start rsyslog, FogLAMP, and tail syslog
CMD ["bash", "usr/bin/foglamp/foglamp.sh"]

LABEL maintainer="rob@raesemann.com" \
      author="Raesemann" \
      target="Raspberry PI" \
      version="1.5.0" \