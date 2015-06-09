#!/bin/bash -ex

rm -f compile || :
./make_compiler.sh ./compile
nosetests bootstrap.py
./compile -o asserts asserts.newlang
./asserts
rm -f asserts ./compile
echo "Passed"
