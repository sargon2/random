#!/bin/bash -e

date

MINECRAFT_USER=minecraft
CLOUD_USER=besen
DST_PATH="/home/besen/Google Drive/backups/minecraft/metal/"
FILENAME=minecraft.tar.gz
TMP_DIR=$(mktemp -d)
CLOUD_WAITER="/home/besen/github/sargon2/random/bin/wait-rclone-vfs.sh"

if (( $EUID != 0 )); then
    echo "Error: Please run this script as root." >&2
    exit 1
fi

sudo -u $CLOUD_USER mkdir -p "$DST_PATH"

pushd /srv
tar cvf - minecraft/ | gzip -9 > $TMP_DIR/$FILENAME
popd
sudo chown -R $CLOUD_USER:$CLOUD_USER $TMP_DIR
sudo -u $CLOUD_USER mv -f $TMP_DIR/$FILENAME "$DST_PATH"

rm -rf $TMP_DIR

sudo -u $CLOUD_USER "$CLOUD_WAITER"
