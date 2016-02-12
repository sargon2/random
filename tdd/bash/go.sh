#!/bin/bash -e

t=true
f=false

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

assertEquals t t
assertEquals f f

assertFails assertEquals t f
assertFails assertEquals f t

assertFails assertFails assertEquals t t
assertFails assertFails assertEquals f f

assertFails assertFails assertFails assertEquals t f
assertFails assertFails assertFails assertEquals f t

assertNotEquals t f
assertNotEquals f t

assertFails assertNotEquals t t
assertFails assertNotEquals f f


assertEquals "a" "a"
assertFails assertEquals "a" "b"
assertFails assertEquals "a" 1
assertEquals "asdf" "asdf"
assertEquals "1" "1"
assertEquals "3" "3"

echo "passed"
