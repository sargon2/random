#!/usr/bin/env python

import sys
import os

infile = sys.argv[3]
outfile = sys.argv[2]

print "Bootstrap compiling '{}' to '{}' ".format(infile, outfile)

with open(infile) as f:
    contents = f.read()

with open(outfile, "w") as f:
    f.write("")

os.chmod(outfile, 0755)
