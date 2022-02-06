#!/bin/bash
kill -9 $(cat /tmp/sleep_infinity.pid)
rm /tmp/alexa_input.pipe
