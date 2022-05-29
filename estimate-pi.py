#!/usr/bin/env python3

import math
import sys

def go():

    numerator = 1
    denominator = 1
    best_error = 9999

    while(True):
        result = numerator / denominator
        error = abs(math.pi - result)
        if error < best_error:
            best_error = error
            print(str(numerator) + " / " + str(denominator) + " = " + str(result) + ", error = " + str(error))
        if error < .00000000001:
            sys.exit(0)
        if result < math.pi :
            numerator = numerator + 1
        elif result > math.pi :
            denominator = denominator + 1

if __name__ == "__main__":
    go()
