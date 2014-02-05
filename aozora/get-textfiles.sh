#!/bin/bash

set -e

shopt -s globstar

TARGET_DIR=~/bitbucket/random/aozora/textfiles

mkdir $TARGET_DIR

cd ~/github/aozorabunko

for i in `ls **/*ruby*.zip`; do
    mkdir -p $TARGET_DIR/$i
    unzip $i '*.txt' -d $TARGET_DIR/$i || :
done
