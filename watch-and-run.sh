#!/bin/bash

function usage() {
    echo "Usage: $0 <file/folder to watch> <command to run>"
    exit 1
}

if [ -z "$2" ]; then
    usage
fi

if [ ! -e "$1" ]; then
    usage
fi

TO_WATCH=$1
shift 1

# TODO: make the clears optional
clear
"$@"
while inotifywait -r -e modify -e attrib -e move -e create -e delete --exclude '\.git' --exclude '\.ropeproject' "$TO_WATCH"; do
    clear
    "$@"
done
