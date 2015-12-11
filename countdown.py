#!/usr/bin/env python

import parsedatetime
import datetime
import time
import sys
import math

t = time.mktime(parsedatetime.Calendar().parse(sys.argv[1])[0])

last = 0
while True:
    now = time.time()
    diff = t - now
    diff = int(math.ceil(diff))
    if diff != last:
        sys.stdout.write('\r' + str(datetime.timedelta(seconds=diff)))
        sys.stdout.flush()
        last = diff
    time.sleep(.01)
