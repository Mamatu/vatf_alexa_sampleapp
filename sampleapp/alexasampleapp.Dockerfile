FROM ubuntu:focal
ARG jobs=4
WORKDIR /home
COPY bin/ /home/bin
RUN mkdir -p sdk-folder && cd sdk-folder && mkdir -p sdk-build sdk-source sdk-install db \
&& cd /home \
&& apt-get update && apt-get upgrade -y && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata apt-utils git \
&& cd /home && git clone -b master_v1.0 https://github.com/Mamatu/vatf.git \
&& cd /home/vatf \
#&& git submodule update --init --remote --force \
&& cd /home \
&& apt-get update && apt-get upgrade -y \
&& DEBIAN_FRONTEND=noninteractive apt-get install -y keyboard-configuration \
&& apt-get install -y \
  git gcc cmake sox build-essential nghttp2 alsa-base alsa-utils libsqlite3-dev libcurl4-openssl-dev libgtest-dev libssl-dev openssl \
  libnghttp2-dev libasound2-dev doxygen alsa pulseaudio pulseaudio-utils portaudio19-dev libgstreamer1.0-0 libgstreamer-plugins-base1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
  gstreamer1.0-libav gstreamer1.0-tools clang-format libgcrypt20-dev libarchive-dev python python3 python3-pip libpulse0 moreutils mplayer \
&& pip install --upgrade pip && pip install pytest psutil jsonschema \
&& echo /home && cd /home/sdk-folder/sdk-source && git clone --single-branch https://github.com/alexa/avs-device-sdk.git \
&& echo "export PORTAUDIO_LIB_PATH=$(find -P /usr/lib -name libportaudio.so)" >> /envfile \
&& . /envfile; echo $PORTAUDIO_LIB_PATH \
&& . /envfile && cd /home/sdk-folder/sdk-build && cmake /home/sdk-folder/sdk-source/avs-device-sdk \
    -DGSTREAMER_MEDIA_PLAYER=ON \
    -DPORTAUDIO=ON \
    -DPKCS11=OFF \
    -DPORTAUDIO_LIB_PATH=$PORTAUDIO_LIB_PATH \
    -DPORTAUDIO_INCLUDE_DIR=/usr/include \
    -DCMAKE_BUILD_TYPE=DEBUG && make SampleApp -j8
COPY config.json /home/sdk-folder/sdk-source/avs-device-sdk/tools/Install/config.json
COPY tests /home/tests
COPY assets /home/assets
# +from https://github.com/TheBiggerGuy/docker-pulseaudio-example/blob/master/Dockerfile
ENV UNAME pacat
RUN export UNAME=$UNAME UID=1000 GID=1000 && \
    mkdir -p "/home/${UNAME}" && \
    echo "${UNAME}:x:${UID}:${GID}:${UNAME} User,,,:/home/${UNAME}:/bin/bash" >> /etc/passwd && \
    echo "${UNAME}:x:${UID}:" >> /etc/group && \
    mkdir -p /etc/sudoers.d && \
    echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${UNAME} && \
    chmod 0440 /etc/sudoers.d/${UNAME} && \
    chown ${UID}:${GID} -R /home/${UNAME} && \
    gpasswd -a ${UNAME} audio
COPY pulse-client.conf /etc/pulse/client.conf
# -from https://github.com/TheBiggerGuy/docker-pulseaudio-example/blob/master/Dockerfile
RUN . /envfile && ls /home/sdk-folder/sdk-source/avs-device-sdk/tools/Install && cd /home/sdk-folder/sdk-source/avs-device-sdk/tools/Install && bash genConfig.sh \
    config.json \
    12345 \
    /home/sdk-folder/db \
    /home/sdk-folder/sdk-source/avs-device-sdk \
    /home/sdk-folder/sdk-build/Integration/AlexaClientSDKConfig.json \
    -DSDK_CONFIG_MANUFACTURER_NAME="Ubuntu" \
    -DSDK_CONFIG_DEVICE_DESCRIPTION="Ubuntu" \
    && cd /home/sdk-folder/sdk-build/ \
#&& ./SampleApplications/ConsoleSampleApplication/src/SampleApp ./Integration/AlexaClientSDKConfig.json 
