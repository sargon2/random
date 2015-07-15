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
echo "line 2" >> file.txt
git add file.txt
git commit -m "Add line 2"
echo "line 3" >> file.txt
git add file.txt
git commit -m "Add line 3"
git push origin master

