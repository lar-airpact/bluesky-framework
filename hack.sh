#!/bin/bash

# Example of using this script:
# 
#   > hack.sh
#
# NOTE: this script DOESN'T INCLUDE all necessary steps to replicate the Docker
# image at https://hub.docker.com/repository/docker/larairpact/bluesky-framework
# since that image was "committed" while being run as a container
#

# hack
rm /bluesky/dist/bluesky/base/lib/MapScript-5.6.3-py2.7-linux-x86_64.egg/mapscript*
cp /usr/lib/python2.7/dist-packages/mapscript* /bluesky/dist/bluesky/base/lib/MapScript-5.6.3-py2.7-linux-x86_64.egg/

# to get Joe's scripting to work without Aeolus
# TODO > in the future, somebody should redesign this without circular dependencies
touch ~/AIRHOME/run_ap5_day1/set_AIRPACT_fire_season.csh 
mkdir -p ~/AIRHOME/run_ap5_day1/emis/fire_orl/transfer