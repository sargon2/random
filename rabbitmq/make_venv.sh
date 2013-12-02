#!/bin/bash

set -e

virtualenv .venv
source .venv/bin/activate
pip install -r test-requires
pip install -r pip-requires
