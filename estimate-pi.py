#!/usr/bin/python

from __future__ import division

import math

numerator = 1
denominator = 1
best_error = 9999

while(True):
    result = numerator / denominator
    error = abs(math.pi - result)
    if error < best_error:
        best_error = error
        print str(numerator) + " / " + str(denominator) + " = " + str(result) + ", error = " + str(error)
    if result < math.pi :
        numerator = numerator + 1
    elif result > math.pi :
        denominator = denominator + 1
    elif result == math.pi:
        system.exit(0)
