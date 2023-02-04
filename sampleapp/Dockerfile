FROM ubuntu:focal
ARG jobs=1
WORKDIR /home/sdk-folder
ENV HOME=/home
RUN mkdir sdk-build sdk-source sdk-install db
RUN apt-get update && apt-get upgrade -y
RUN cd $HOME
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install -y \
git gcc cmake sox build-essential nghttp2 libsqlite3-dev libcurl4-openssl-dev libgtest-dev libssl-dev openssl \
libnghttp2-dev libasound2-dev doxygen pulseaudio portaudio19-dev libgstreamer1.0-0 libgstreamer-plugins-base1.0-dev \
gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
gstreamer1.0-libav gstreamer1.0-tools clang-format libgcrypt20-dev libarchive-dev
RUN echo $HOME && cd $HOME/sdk-folder/sdk-source && git clone --single-branch https://github.com/alexa/avs-device-sdk.git
RUN echo "export PORTAUDIO_LIB_PATH=$(find -P /usr/lib -name libportaudio.so)" >> /envfile
RUN . /envfile; echo $PORTAUDIO_LIB_PATH
RUN . /envfile && cd $HOME/sdk-folder/sdk-build && cmake $HOME/sdk-folder/sdk-source/avs-device-sdk \
    -DGSTREAMER_MEDIA_PLAYER=ON \
    -DPORTAUDIO=ON \
    -DPKCS11=OFF \
    -DPORTAUDIO_LIB_PATH=$PORTAUDIO_LIB_PATH \
    -DPORTAUDIO_INCLUDE_DIR=/usr/include \
    -DCMAKE_BUILD_TYPE=DEBUG && make SampleApp -j$jobs
COPY ./config.json /home/sdk-folder/sdk-folder/sdk-source/avs-device-sdk/tools/Install/
RUN . /envfile && cd $HOME/sdk-folder/sdk-source/avs-device-sdk/tools/Install && bash genConfig.sh \
    config.json \
    12345 \
    $HOME/sdk-folder/db \
    $HOME/sdk-folder/sdk-source/avs-device-sdk \
    $HOME/sdk-folder/sdk-build/Integration/AlexaClientSDKConfig.json \
    -DSDK_CONFIG_MANUFACTURER_NAME="Ubuntu" \
    -DSDK_CONFIG_DEVICE_DESCRIPTION="Ubuntu"
RUN . /envfile && cd $HOME/sdk-folder/sdk-build/ && ./SampleApplications/ConsoleSampleApplication/src/SampleApp ./Integration/AlexaClientSDKConfig.json 
