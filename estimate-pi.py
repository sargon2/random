#!/usr/bin/python

from __future__ import division

import math
import sys

numerator = 1
denominator = 1
best_error = 9999

while(True):
    result = numerator / denominator
    error = abs(math.pi - result)
    if error < best_error:
        best_error = error
        print str(numerator) + " / " + str(denominator) + " = " + str(result) + ", error = " + str(error)
    if str(result) == str(math.pi):
        sys.exit(0)
    if result < math.pi :
        numerator = numerator + 1
    elif result > math.pi :
        denominator = denominator + 1
