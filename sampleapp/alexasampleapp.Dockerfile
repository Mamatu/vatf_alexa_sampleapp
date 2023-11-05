FROM ubuntu:focal
ARG jobs=1
WORKDIR /home
COPY bin/ /home/bin
RUN mkdir -p sdk-folder && cd sdk-folder && mkdir -p sdk-build sdk-source sdk-install db \
&& cd /home \
&& apt-get update && apt-get upgrade -y && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata apt-utils \
&& apt-get update && apt-get upgrade -y && apt-get install -y \
  git gcc cmake sox build-essential nghttp2 libsqlite3-dev libcurl4-openssl-dev libgtest-dev libssl-dev openssl \
  libnghttp2-dev libasound2-dev doxygen alsa pulseaudio portaudio19-dev libgstreamer1.0-0 libgstreamer-plugins-base1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
  gstreamer1.0-libav gstreamer1.0-tools clang-format libgcrypt20-dev libarchive-dev python libpulse0 moreutils \
&& echo /home && cd /home/sdk-folder/sdk-source && git clone --single-branch https://github.com/alexa/avs-device-sdk.git \
&& echo "export PORTAUDIO_LIB_PATH=$(find -P /usr/lib -name libportaudio.so)" >> /envfile \
&& . /envfile; echo $PORTAUDIO_LIB_PATH \
&& . /envfile && cd /home/sdk-folder/sdk-build && cmake /home/sdk-folder/sdk-source/avs-device-sdk \
    -DGSTREAMER_MEDIA_PLAYER=ON \
    -DPORTAUDIO=ON \
    -DPKCS11=OFF \
    -DPORTAUDIO_LIB_PATH=$PORTAUDIO_LIB_PATH \
    -DPORTAUDIO_INCLUDE_DIR=/usr/include \
    -DCMAKE_BUILD_TYPE=DEBUG && make SampleApp -j$jobs
COPY config.json /home/sdk-folder/sdk-source/avs-device-sdk/tools/Install/config.json
RUN . /envfile && ls /home/sdk-folder/sdk-source/avs-device-sdk/tools/Install && cd /home/sdk-folder/sdk-source/avs-device-sdk/tools/Install && bash genConfig.sh \
    config.json \
    12345 \
    /home/sdk-folder/db \
    /home/sdk-folder/sdk-source/avs-device-sdk \
    /home/sdk-folder/sdk-build/Integration/AlexaClientSDKConfig.json \
    -DSDK_CONFIG_MANUFACTURER_NAME="Ubuntu" \
    -DSDK_CONFIG_DEVICE_DESCRIPTION="Ubuntu" \
    . /envfile && cd /home/sdk-folder/sdk-build/ && ./SampleApplications/ConsoleSampleApplication/src/SampleApp ./Integration/AlexaClientSDKConfig.json 
