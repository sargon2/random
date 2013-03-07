#!/bin/bash

set -e

if [ -z "$1" ]
then
        echo "Delete a file from the history of a git repository."
        echo "The script found here may be useful for identifying which to remove:"
        echo "http://stubbisms.wordpress.com/2009/07/10/git-script-to-show-largest-pack-objects-and-trim-your-waist-line/"
        echo
        echo "Usage: $0 <files or directories>"
        exit 1
fi


git filter-branch --index-filter "git rm -r --cached --ignore-unmatch $*" --prune-empty --tag-name-filter cat -- --all
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now
git gc --aggressive --prune=now

echo
echo 'Now, you may want to run: git push origin --all --force'
echo
echo 'WARNING: This command counts as an upstream rebase. That means everyone who has the repository checked out will have to delete their copies and re-check it out (or run git reset --hard HEAD) before they can push.'
