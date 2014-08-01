#!/bin/bash

set -ex

unset DISPLAY # otherwise dropbox tries to use X

cd ~

mkdir ~/bin/ || :

rm -f ~/bin/dropbox || :

rm -rf ~/.dropbox/ ~/.dropbox-dist/ ~/.dropbox-master/ || :

wget -O ~/bin/dropbox "https://www.dropbox.com/download?dl=packages/dropbox.py"
chmod a+x ~/bin/dropbox

yes | ~/bin/dropbox start -i # to install it

echo "Manual steps follow; exiting until they're automated"
exit 1

# MANUAL: wait for it to install, kill it when finished

~/.dropbox-dist/dropboxd
# MANUAL: <visit link, authenticate>

# MANUAL: kill it
~/bin/dropbox start

# wait until done syncing
while ! ~/bin/dropbox status 2>&1 | grep -q "Up to date"; do sleep 1; done

~/bin/dropbox lansync n # apparently makes it use less network bandwidth
