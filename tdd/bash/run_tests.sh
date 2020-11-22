#!/bin/bash -e

# set -x; PS4='+ ${LINENO}: '

function equals {
    if [ "$1" == "$2" ]; then
        return 0
    fi
    return 1
}

function assertEquals {
    local MSG="$3"
    if [ -z "$3" ]; then
        MSG="expected '$1' to equal '$2'"
    fi
    assertFailsMsg assertNotEquals "$1" "$2" "$MSG"
}

function assertNotEquals {
    if equals "$1" "$2"; then
        if [ -n "$3" ]; then
            echo "$3"
        else
            echo "expected '$1' to not equal '$2'"
        fi
        return 1
    fi
}


# We have no way to know if a message was provided,
# so we have to use the function name to tell.
function assertFails {
    assertFailsMsg "$@" "expected '$*' to fail"
}

function assertFailsMsg {
    local RET=0
    # https://stackoverflow.com/a/11092989 (workaround for -e)
    # https://stackoverflow.com/a/1215592 (strip last arg)
    set +e ; ( set -e; "${@:1:$#-1}" >/dev/null ) ; RET=$?
    set -e

    MSG="${@: -1}"
    assertNotEquals $RET 0 "$MSG"
}

function assertFileNotExists {
    if [ -f "$1" ]; then
        if [ -n "$2" ]; then
            echo "$2"
        else
            echo "expected '$1' to not exist"
        fi
        return 1
    fi
}

function assertFileExists {
    MSG=$2
    if [ -z "$2" ]; then
        MSG="expected '$1' to exist"
    fi
    assertFailsMsg assertFileNotExists "$1" "$MSG"
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

    assertNotEquals "asdf jkl" "asdf asdf"
    assertEquals "asdf jkl" "asdf jkl"

    assertFails assertFileExists "del me.txt"
    assertFileNotExists "del me.txt"

    touch "del me.txt"
    trap "rm -f \"del me.txt\"" EXIT RETURN
    assertFileExists "del me.txt"
    assertFails assertFileNotExists "del me.txt"
}

function assertFailureMessage {
    expected_msg="${@: -1}"
    set +e ; actual_msg=$( ( set -e; "${@:1:$#-1}" ) ) ;
    set -e

    assertEquals "$expected_msg" "$actual_msg"
}

function assertCustomFailureMessage {
    assertFailureMessage "$@" "blah msg" "blah msg"
}

function assertBothFailureMessages {
    assertFailureMessage "$@"
    assertCustomFailureMessage "${@:1:$#-1}"
}

function internal_test_failure_messages {
    assertBothFailureMessages assertNotEquals "a" "a" "expected 'a' to not equal 'a'"
    assertBothFailureMessages assertEquals "a" "b" "expected 'a' to equal 'b'"

    assertFailureMessage assertFails assertEquals "a" "a" "expected 'assertEquals a a' to fail"
    assertCustomFailureMessage assertFailsMsg assertEquals "a" "a"

    assertBothFailureMessages assertFileExists "del me.txt" "expected 'del me.txt' to exist"
    touch "del me.txt"
    trap "rm -f \"del me.txt\"" EXIT RETURN
    assertBothFailureMessages assertFileNotExists "del me.txt" "expected 'del me.txt' to not exist"
}

functions=$(declare -F | cut -d" " -f3-)

overall_passed=true
for func in $functions; do
    if [[ $func = internal_test_* ]]; then
        set +e ; MSG=$( ( set -e; $func ) ) ; RET=$?
        set -e

        if [ "$RET" -ne "0" ]; then
            echo "internal test $func FAIL: $MSG"
            exit 1
        fi
    fi
    if [[ $func = test_* ]]; then
        set +e ; MSG=$( ( set -e; $func ) ) ; RET=$?
        set -e

        if [ "$RET" -eq "0" ]; then
            echo $func "PASS"
        else
            echo "$func FAIL: $MSG"
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
