#!/bin/bash -e

function test_should_fail {
    assertEquals true false
}

function test_should_pass {
    assertEquals true true
}

. ./run_tests.sh
