#!/bin/bash

COLUMNS=$(tput cols)
git log --stat=$COLUMNS,$(($COLUMNS-32)) "$@"
