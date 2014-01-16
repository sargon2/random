import sys
import math

# This method is very fast, but only works on a small subset of semiprimes.

def find_smallest_square_greater_than(n):
    i = int(math.sqrt(n)) + 1
    return (i*i, i)

n = int(sys.argv[1])

(r, i) = find_smallest_square_greater_than(n)
d = r - n
s = int(math.sqrt(d))
a = i+s
b = i-s
if a*b == n:
    print a, "*", b
else:
    print "nope"
