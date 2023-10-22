#!/usr/bin/env python3

import sys
import os
import struct
import math

if len(sys.argv) == 1:
    print("Usage:", sys.argv[0], "<file to encrypt> [number of output files (default 2)]")
    sys.exit(1)

infile = sys.argv[1]
num_files = 2
if len(sys.argv) > 2:
    num_files = int(sys.argv[2])

size = os.stat(infile).st_size

def readit(filename):
    with open(filename, "rb") as f:
        byte = f.read(1)
        while byte:
            yield byte[0]
            byte = f.read(1)

def writeit(outfiles, generator):
    fds = []
    for outfile in outfiles:
        fds.append(open(outfile, "ab"))
    for byte in generator:
        first = byte
        for i in range(1, num_files):
            r = os.urandom(1)[0]
            fds[i].write(bytes([r]))
            first = first ^ r
        fds[0].write(bytes([first]))

def pad(num):
    for i in range(0, num):
        yield 0

# http://stackoverflow.com/a/19164783
def next_power_of_2(n):
    """
    Return next power of 2 greater than or equal to n
    """
    n -= 1 # greater than OR EQUAL TO n
    shift = 1
    while (n+1) & n: # n+1 is not a power of 2 yet
        n |= n >> shift
        shift <<= 1
    return n + 1

def get_padding_size(num):
    # Return number of bytes to add to make the size a power of two.  Can be zero.
    s = next_power_of_2(num)
    return s - num


outfiles = []
for i in range(0, num_files):
    outfiles.append(infile + ".k" + str(i))

for outfile in outfiles:
    if(os.path.exists(outfile)):
        print(outfile + " exists")
        sys.exit(1)

size_bytes = struct.pack("I", size)

writeit(outfiles, size_bytes)
writeit(outfiles, readit(infile))
writeit(outfiles, pad(get_padding_size(size+4)))
