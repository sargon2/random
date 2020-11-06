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
    local RET=0
    "$@" || RET=$?
    assertNotEquals $RET 0
}

function internal_test_asserts {

    assertEquals true true
    assertEquals false false

    assertFails assertEquals true false
    assertFails assertEquals false true

    assertFails assertFails assertEquals true true
    assertFails assertFails assertEquals false false

    assertFails assertFails assertFails assertEquals true false
    assertFails assertFails assertFails assertEquals false true

    assertNotEquals true false
    assertNotEquals false true

    assertFails assertNotEquals true true
    assertFails assertNotEquals false false


    assertEquals "a" "a"
    assertNotEquals "a" "b"
    assertNotEquals "a" 1
    assertEquals "asdf" "asdf"
    assertEquals "1" "1"
    assertEquals "3" "3"
}

functions=$(declare -F | cut -d" " -f3-)

overall_passed=true
for func in $functions; do
    if [[ $func = internal_test_* ]]; then
        # Silently run internal tests
        # If we do $func || RET=$? here, it causes the tests to false negative.
        # That's super annoying and needs a fix, so we can output a reasonable
        # message on internal failure.
        $func
    fi
    if [[ $func = test_* ]]; then
        RET=0
        $func || RET=$?
        if [ "$RET" -eq "0" ]; then
            echo $func "PASS"
        else
            echo $func "FAIL"
            overall_passed=false
        fi
    fi
done
if $overall_passed; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi
