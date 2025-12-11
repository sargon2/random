#!/bin/bash

set -e

unset DISPLAY # otherwise dropbox tries to use X

DROPBOX=/bin/dropbox-cli # arch
# DROPBOX=~/bin/dropbox

$DROPBOX lansync n # apparently makes it use less network bandwidth

# wait until done syncing
# TODO: dup'd with reinstall-dropbox.sh
while true; do
    status="$($DROPBOX status 2>&1)"
    echo "$status"
    if echo "$status" | grep -q "Up to date"; then
        break
    fi
    sleep 5
done
