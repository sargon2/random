#!/bin/bash -ex

export DISPLAY=
unset DISPLAY

dropbox start
sleep 1
~/bitbucket/random/wait-for-dropbox-sync.sh
find ~/Dropbox | grep -i conflicted
