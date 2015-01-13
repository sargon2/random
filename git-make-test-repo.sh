#!/bin/bash

set -e

if [[ -z "$1" ]]; then
    NAME=repo
else
    NAME=$1
fi

git init --bare ${NAME}.git
git clone ${NAME}.git ${NAME}
cd ${NAME}
echo "file" > file.txt
git add file.txt
git commit -m "Add file.txt"
git push origin master

