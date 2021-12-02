#!/usr/bin/env python3

import random
import time

total_votes = 0
ary = []
while True:
    r = random.randint(0, total_votes + 30)
    ary = ary + [" "] * (r - len(ary) + 1)
    if ary[r] == " ":
        total_votes += 1
        if bool(random.getrandbits(1)):
            ary[r] = "A"
        else:
            ary[r] = "B"
        print("".join(ary))
        time.sleep(0.1)
