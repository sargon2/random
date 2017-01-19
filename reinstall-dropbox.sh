#!/bin/bash

set -e

unset DISPLAY # otherwise dropbox tries to use X

cd ~

mkdir ~/bin/ || :

rm -f ~/bin/dropbox || :

rm -rf ~/.dropbox/ ~/.dropbox-dist/ ~/.dropbox-master/ || :

wget -O ~/bin/dropbox "https://www.dropbox.com/download?dl=packages/dropbox.py"
chmod a+x ~/bin/dropbox

echo "No need to type anything"
echo y | ~/bin/dropbox start -i # to install it

~/bin/dropbox stop

~/.dropbox-dist/dropboxd &

echo "Manually visit the link!!"
# MANUAL: <visit link, authenticate>

# wait until done syncing
# TODO: we're doing extra status calls here...
# TODO: dup'd with wait-for-dropbox-sync.sh
while ! ~/bin/dropbox status 2>&1 | grep -q "Up to date"; do sleep 5; ~/bin/dropbox status; sleep 5; done

# Restart it so it's running via the python script instead of in this shell
~/bin/dropbox stop
~/bin/dropbox start

~/bin/dropbox lansync n # apparently makes it use less network bandwidth
