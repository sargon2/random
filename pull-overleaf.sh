#!/bin/bash -ex

if [ -z "$1" ]
then
        echo "Pull .tex files from overleaf"
        echo
        echo "Usage: $0 <overleaf git URI>"
        exit 1
fi

git remote add overleaf $1
git fetch overleaf
git checkout remotes/overleaf/master '*'
git remote rm overleaf
