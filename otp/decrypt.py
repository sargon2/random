#!/usr/bin/env python

import sys
import os
import struct

infile1 = sys.argv[1]
infile2 = sys.argv[2]
outfile = sys.argv[3]

with open(infile1, "rb") as f1:
    with open(infile2, "rb") as f2:
        with open(outfile, "wb") as o:
            # Read size
            size = ""
            for i in range(0, 4):
                size1 = f1.read(1)
                size2 = f2.read(1)
                size += chr(ord(size1) ^ ord(size2))

            # Read and decrypt data
            size = struct.unpack("I", size)[0]
            for i in range(0, size):
                byte = f1.read(1)
                byte2 = f2.read(1)
                r = ord(byte) ^ ord(byte2)
                o.write(chr(r))
