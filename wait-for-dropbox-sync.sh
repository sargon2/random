#!/bin/bash

set -e

unset DISPLAY # otherwise dropbox tries to use X

if [ -x /bin/dropbox-cli ]; then
  DROPBOX=/bin/dropbox-cli # arch
else
  DROPBOX="$HOME/bin/dropbox"
fi

$DROPBOX lansync n # apparently makes it use less network bandwidth
$DROPBOX start

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
