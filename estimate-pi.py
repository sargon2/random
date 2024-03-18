#!/usr/bin/env python3

import math
import sys

target = math.pi
# target = (1 + math.sqrt(5)) / 2 # phi (the golden ratio)

def go():

    numerator = 1
    denominator = 1
    best_error = 9999
    result = 0

    while(True):
        prev_result = result
        result = numerator / denominator
        if prev_result == result:
            sys.exit(0)
        error = abs(target - result)
        if error < best_error:
            best_error = error
            print(str(numerator) + " / " + str(denominator) + " = " + str(result) + ", error = " + str(error))
        if result < target:
            numerator = numerator + 1
        elif result > target:
            denominator = denominator + 1

if __name__ == "__main__":
    go()
