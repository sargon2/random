#!/bin/bash

set -e

BRANCHES=`git branch | cut -b 3-`

while read i; do
    echo
    echo "$i"
    git branch -d $i || :
done <<< "$BRANCHES"
