#!/bin/bash

set -e

unset DISPLAY # otherwise dropbox tries to use X

DROPBOX=/bin/dropbox-cli # arch
# DROPBOX=~/bin/dropbox

$DROPBOX lansync n # apparently makes it use less network bandwidth

# wait until done syncing
# TODO: dup'd with reinstall-dropbox.sh
while ! $DROPBOX status 2>&1 | grep -q "Up to date"; do
    sleep 5
done

