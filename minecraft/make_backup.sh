#!/bin/bash -ex

TMP_DIR=$(mktemp -d)
DESTINATION=$HOME/Dropbox/minecraft/metal/

mkdir -p $DESTINATION

pushd /srv
sudo tar cvfz $TMP_DIR/minecraft.tar.gz minecraft/
popd
sudo chown $USER:$USER $TMP_DIR/minecraft.tar.gz
mv -f $TMP_DIR/minecraft.tar.gz $DESTINATION

rm -rf $TMP_DIR

wait-for-dropbox-sync
