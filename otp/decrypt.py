#!/usr/bin/env python3

import sys
import os
import struct

if len(sys.argv) == 1:
    print("Usage:", sys.argv[0], " <outfile> <infiles...>")
    sys.exit(1)

outfile = sys.argv[1]
infiles = sys.argv[2:]

fds = []
for infile in infiles:
    fds.append(open(infile, "rb"))

with open(outfile, "wb") as o:
    # Read size
    bytes_size = bytearray()
    for i in range(0, 4):
        current_size_byte = 0
        for fd in fds:
            current_file_size_byte = fd.read(1)[0]
            current_size_byte ^= current_file_size_byte
        bytes_size.append(current_size_byte)

    # Read and decrypt data
    size = struct.unpack("I", bytes(bytes_size))[0]
    for i in range(0, size):
        byte = 0
        for fd in fds:
            byte ^= fd.read(1)[0]
        o.write(bytes([byte]))
