#!/usr/bin/env python

import sys
import os
import struct
import math

infile = sys.argv[1]

size = os.stat(infile).st_size

def readit(filename):
    with open(filename, "rb") as f:
        byte = f.read(1)
        while byte != "":
            yield byte
            byte = f.read(1)

def writeit(outfile1, outfile2, generator):
    with open(outfile1, "ab") as k1:
        with open(outfile2, "ab") as k2:
            for byte in generator:
                r = ord(os.urandom(1))
                a = ord(byte) ^ r
                k1.write(chr(r))
                k2.write(chr(a))

def pad(num):
    for i in xrange(0, num):
        yield chr(0)

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


outfile1 = infile + ".k1"
outfile2 = infile + ".k2"

if(os.path.exists(outfile1)):
    print outfile1 + " exists"
    sys.exit(1)

if(os.path.exists(outfile2)):
    print outfile2 + " exists"
    sys.exit(1)

size_bytes = struct.pack("I", size)

writeit(outfile1, outfile2, size_bytes)
writeit(outfile1, outfile2, readit(infile))
writeit(outfile1, outfile2, pad(get_padding_size(size+4)))
