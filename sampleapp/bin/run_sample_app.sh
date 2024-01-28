#!/bin/bash
trap "bash cleanup_sample_app.sh" err exit

BUILD_DIR=$HOME/sdk-folder/sdk-build
mkfifo /tmp/alexa_input.pipe

sleep infinity > /tmp/alexa_input.pipe &
echo $! > /tmp/sleep_infinity.pid

cat /tmp/alexa_input.pipe | $BUILD_DIR/SampleApplications/ConsoleSampleApplication/src/SampleApp $BUILD_DIR/Integration/AlexaClientSDKConfig.json DEBUG1 | ts '%Y-%m-%d %H:%M:%.S ' | tee /tmp/alexa_sampleapp.log
