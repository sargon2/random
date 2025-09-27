#!/usr/bin/env python3

results = {}
MAX_DEPTH = 5
TARGET_NUMBER="5"

def is_whole(n):
    return n == int(n)

def num_fives(s):
    return s.count(TARGET_NUMBER)

def doit(string_so_far, num_parens=0, depth=0):
    if num_parens < 0:
        return
    elif num_parens == 0:
        try:
            result = eval(string_so_far)
        except:
            return
        if result > 0 and is_whole(result):
            result = int(result)
            if not result in results or num_fives(string_so_far) < num_fives(results[result]):
                results[result] = string_so_far
    if depth > MAX_DEPTH:
        return
    doit(string_so_far + "*" + TARGET_NUMBER, num_parens, depth+1)
    doit(string_so_far + "+" + TARGET_NUMBER, num_parens, depth+1)
    doit(string_so_far + "-" + TARGET_NUMBER, num_parens, depth+1)
    doit(string_so_far + "/" + TARGET_NUMBER, num_parens, depth+1)

    doit(string_so_far + ")*" + TARGET_NUMBER, num_parens-1, depth+1)
    doit(string_so_far + ")+" + TARGET_NUMBER, num_parens-1, depth+1)
    doit(string_so_far + ")-" + TARGET_NUMBER, num_parens-1, depth+1)
    doit(string_so_far + ")/" + TARGET_NUMBER, num_parens-1, depth+1)

    doit(string_so_far + "*(" + TARGET_NUMBER, num_parens+1, depth+1)
    doit(string_so_far + "+(" + TARGET_NUMBER, num_parens+1, depth+1)
    doit(string_so_far + "-(" + TARGET_NUMBER, num_parens+1, depth+1)
    doit(string_so_far + "/(" + TARGET_NUMBER, num_parens+1, depth+1)

    doit(string_so_far + ")*(" + TARGET_NUMBER, num_parens, depth+1)
    doit(string_so_far + ")+(" + TARGET_NUMBER, num_parens, depth+1)
    doit(string_so_far + ")-(" + TARGET_NUMBER, num_parens, depth+1)
    doit(string_so_far + ")/(" + TARGET_NUMBER, num_parens, depth+1)

    doit(string_so_far + ")", num_parens-1, depth+1)

doit(TARGET_NUMBER)
doit("(" + TARGET_NUMBER, 1)

kc = 1
for k in sorted(results):
    if k != kc:
        print("BREAK!!!")
        kc = k
    kc = kc + 1
    print(k, results[k])
