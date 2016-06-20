#!/bin/bash -e

FAILED=()

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
        ret=0
        "$@" || ret=$?
        if [ $ret -ne 0 ]; then
            FAILED+=("$FOLDER")
        fi
    popd >/dev/null
    echo
done

if [ -n "$FAILED" ]; then
    echo "FAILED: ${FAILED[@]}"
fi
