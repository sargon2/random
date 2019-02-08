import sys

if sys.version_info[0] != 3:
    print("This requires Python 3")
    exit()

import math

def is_prime(val):
    if val % 2 == 0:
        return False
    i = 3
    while i * i <= val:
        if val % i == 0:
            return False
        i += 2
    return True

def mersenne():
    i = 2
    while True:
        val = (2 ** i) - 1
        if is_prime(val):
            yield val
        i += 1

for i in mersenne():
    print((i * (i+1)) // 2)
