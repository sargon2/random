#!/usr/bin/env python3

results = {}

def is_whole(n):
    return n == int(n)

def doit(string_so_far):
    result = eval(string_so_far)
    if result > 0 and is_whole(result):
        result = int(result)
        if not result in results or len(string_so_far) < len(results[result]):
            results[result] = string_so_far
    if len(string_so_far) > 17:
        return
    doit(string_so_far + "*5")
    doit(string_so_far + "+5")
    doit(string_so_far + "-5")
    doit(string_so_far + "/5")

doit("5")

kc = 1
for k in sorted(results):
    if k != kc:
        print("BREAK!!!")
    kc = kc + 1
    print(k, results[k])
