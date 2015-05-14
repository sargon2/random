#!/usr/bin/env python

import sys
import os

infile = sys.argv[3]
outfile = sys.argv[2]

with open(infile) as f:
    contents = f.read()

# Note that contents is always the same.  So we could just hardcode the output if we wished.

with open(outfile, "w") as f:
    f.write(contents)

os.chmod(outfile, 0755)
