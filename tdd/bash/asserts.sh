#!/bin/bash -e

function equals {
    if [ "$1" == "$2" ]; then
        return 0
    fi
    return 1
}

function assertEquals {
    assertFails assertNotEquals $1 $2
}

function assertNotEquals {
    if equals $1 $2; then
        return 1
    fi
}

function assertFails {
    RET=0
    $@ > /dev/null || RET=$?
    assertNotEquals $RET 0
}
