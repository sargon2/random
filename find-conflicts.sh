#!/bin/bash

! grep -I -r --exclude-dir=.git "^<<<<<<< " .
