#!/bin/bash

set -ex

unset DISPLAY # otherwise dropbox tries to use X

cd ~

mkdir ~/bin/ || :

rm -f ~/bin/dropbox || :

rm -rf ~/.dropbox/ ~/.dropbox-dist/ ~/.dropbox-master/ || :

wget -O ~/bin/dropbox "https://www.dropbox.com/download?dl=packages/dropbox.py"
chmod a+x ~/bin/dropbox

dropbox start -i # to install it

echo "Manual steps follow; exiting until they're automated"
exit 0

# MANUAL: wait for it to install

~/bin/dropbox stop

~/.dropbox-dist/dropboxd
# MANUAL: <visit link>

# MANUAL: kill it
~/bin/dropbox start

~/bin/dropbox status
# MANUAL: wait until done syncing

dropbox lansync n # apparently makes it use less network bandwidth
