#!/usr/bin/env python

import sys
import os
import struct

if len(sys.argv) == 1:
    print "Usage:", sys.argv[0], " <outfile> <infiles...>"

outfile = sys.argv[1]
infiles = sys.argv[2:]

fds = []
for infile in infiles:
    fds.append(open(infile, "rb"))
    # TODO: close fds

with open(outfile, "wb") as o:
    # Read size
    str_size = ""
    for i in xrange(0, 4):
        current_size_byte = 0
        for fd in fds:
            current_file_size_byte = fd.read(1)
            current_size_byte ^= ord(current_file_size_byte)
        str_size += chr(current_size_byte)

    # Read and decrypt data
    size = struct.unpack("I", str_size)[0]
    for i in xrange(0, size):
        byte = 0
        for fd in fds:
            byte ^= ord(fd.read(1))
        o.write(chr(byte))
