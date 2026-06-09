#!/bin/bash -e

date

MINECRAFT_USER=minecraft
DROPBOX_USER=besen
SRC_PATH=/srv/minecraft
DST_PATH=/home/besen/Dropbox/minecraft/metal/
FILENAME=minecraft.tar.gz
TMP_DIR=$(mktemp -d)
DROPBOX_WAITER=/home/besen/github/sargon2/random/bin/wait-for-dropbox-sync

if (( $EUID != 0 )); then
    echo "Error: Please run this script as root." >&2
    exit 1
fi

sudo -u $DROPBOX_USER mkdir -p $DST_PATH

pushd /srv
tar cvf - minecraft/ | gzip -9 > $TMP_DIR/$FILENAME
popd
sudo chown $DROPBOX_USER:$DROPBOX_USER $TMP_DIR/$FILENAME
mv -f $TMP_DIR/$FILENAME $DST_PATH

rm -rf $TMP_DIR

sudo -u $DROPBOX_USER $DROPBOX_WAITER
