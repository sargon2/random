#!/bin/bash -ex

# Vim doesn't detect when this ran, not sure why.
# autopep8 -i --max-line-length 120 --experimental -a -a -a -a even_further.py
python3 -m unittest even_further.py
