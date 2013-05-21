#!/usr/bin/python

import sys

def usage():
    print "Usage: " + sys.argv[0] + " <sentences> <ok-list>"
    print "Both files must be sorted."

if len(sys.argv) != 3:
    usage()
    sys.exit(-1)

def read_line(f):
    sline = f.readline()
    if sline == "":
        sys.exit(0)
    sline = sline.split("\t")
    return sline

with open(sys.argv[1], 'r') as sentences:
    with open(sys.argv[2], 'r') as ok:

        sline = read_line(sentences)
        oline = read_line(ok)

        while True:
            snum = sline[0]
            onum = oline[0]
            if snum == onum:
                print '\t'.join(sline),
                sline = read_line(sentences)
                oline = read_line(ok)
            elif snum < onum:
                sline = read_line(sentences)
            else: # snum > onum
                oline = read_line(ok)

