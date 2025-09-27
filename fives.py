#!/usr/bin/env python3

results = {}

def is_whole(n):
    return n == int(n)

def num_fives(s):
    return s.count("5")

def doit(string_so_far, num_parens=0):
    if num_parens < 0:
        return
    if num_parens == 0:
        try:
            result = eval(string_so_far)
        except:
            return
        if result > 0 and is_whole(result):
            result = int(result)
            if not result in results or num_fives(string_so_far) < num_fives(results[result]):
                results[result] = string_so_far
    if len(string_so_far) > 15:
        return
    doit(string_so_far + "*5", num_parens)
    doit(string_so_far + "+5", num_parens)
    doit(string_so_far + "-5", num_parens)
    doit(string_so_far + "/5", num_parens)

    doit(string_so_far + ")*5", num_parens-1)
    doit(string_so_far + ")+5", num_parens-1)
    doit(string_so_far + ")-5", num_parens-1)
    doit(string_so_far + ")/5", num_parens-1)

    doit(string_so_far + "*(5", num_parens+1)
    doit(string_so_far + "+(5", num_parens+1)
    doit(string_so_far + "-(5", num_parens+1)
    doit(string_so_far + "/(5", num_parens+1)

doit("5")

kc = 1
for k in sorted(results):
    if k != kc:
        print("BREAK!!!")
    kc = kc + 1
    print(k, results[k])
