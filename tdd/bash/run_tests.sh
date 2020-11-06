#!/bin/bash -e

. ./asserts.sh

functions=$(declare -F | cut -d" " -f3-)

overall_passed=true
for func in $functions; do
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
