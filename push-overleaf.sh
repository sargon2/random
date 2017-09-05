#!/bin/bash -ex

if [ -z "$1" ]
then
        echo "Push .tex files to overleaf"
        echo
        echo "Usage: $0 <overleaf git URI>"
        exit 1
fi

git remote add overleaf $1
git fetch overleaf master
git checkout -b overleaf/master overleaf/master
git rm -r '*'
git checkout master '*.tex'
git add -A
git commit -m "Update .tex files"
git push overleaf HEAD:master
git checkout master
git branch -D overleaf/master
git remote rm overleaf
