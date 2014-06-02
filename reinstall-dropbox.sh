#!/bin/bash

set -ex

cd ~

rm -f ~/bin/dropbox

rm -rf ~/.dropbox/ ~/.dropbox-dist/ ~/.dropbox-master/

cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -

wget -O ~/bin/dropbox "https://www.dropbox.com/download?dl=packages/dropbox.py" && chmod +x ~/bin/dropbox

# dropbox start -i

echo "Be sure to run dropbox lansync n after it's up and running"


~/.dropbox-dist/dropboxd # will ask for authentication

# dropbox lansync n # apparently makes it use less network bandwidth
