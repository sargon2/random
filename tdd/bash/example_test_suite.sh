#!/bin/bash -e

function setUpTest {
    echo "set up"
}

function tearDownTest {
    echo "tear down"
}

function test_should_fail {
    assertEquals true false
}

function test_should_pass {
    assertEquals true true
}

. ./run_tests.sh
