#!/bin/bash

set -e

git init --bare repo.git
git clone repo.git repo
cd repo
echo "file" > file.txt
git add file.txt
git commit -m "Add file.txt"
git push origin master

