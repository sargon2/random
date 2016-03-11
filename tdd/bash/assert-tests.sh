#!/bin/bash -e

. ./asserts.sh

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

echo "passed"
