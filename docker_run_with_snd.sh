#!/bin/bash
docker run --env HOME=/home -it --device /dev/snd/ $1
