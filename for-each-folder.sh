#!/bin/bash -eu

for FOLDER in *; do
    if [ ! -d "$FOLDER" ]; then
        continue
    fi
    if [ "$FOLDER" = "." ]; then
        continue
    fi
    if [ "$FOLDER" = ".." ]; then
        continue
    fi
    echo $FOLDER:
    pushd $FOLDER >/dev/null
        "$@"
    popd >/dev/null
    echo
done
