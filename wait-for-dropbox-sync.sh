#!/bin/bash

set -e

unset DISPLAY # otherwise dropbox tries to use X

~/bin/dropbox lansync n # apparently makes it use less network bandwidth

# wait until done syncing
# TODO: we're doing extra status calls here...
# TODO: dup'd with reinstall-dropbox.sh
while ! ~/bin/dropbox status 2>&1 | grep -q "Up to date"; do sleep 5; ~/bin/dropbox status; sleep 5; done

