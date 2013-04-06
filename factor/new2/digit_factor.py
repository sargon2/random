#!/usr/bin/python

import sys
import functools
#import statprof

# i and j must be the same length for this to work

# taken from http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# note that this decorator ignores **kwargs
def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


def get_digits(number, digits):
    return (("0"*digits) + str(number))[-digits:]

def strlen(number):
    return len(str(number))

@memoize
def factor(num_to_factor, i_so_far="", j_so_far=""):
    #print "factor(" + str(i_so_far) + ", " + str(j_so_far) + ")"
    digits_to_match = strlen(i_so_far) + 1
    right_side = get_digits(num_to_factor, digits_to_match)
    for i in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
        for j in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            new_i_so_far = i + i_so_far
            new_j_so_far = j + j_so_far
            result = int(new_i_so_far) * int(new_j_so_far)
            #print "new i is", new_i_so_far, ", new j is", new_j_so_far, "result is", result
            if result == num_to_factor:
                if int(new_j_so_far) != 1 and int(new_i_so_far) != 1:
                    #print "RETURNING 1: ", (new_i_so_far, new_j_so_far)
                    return (int(new_i_so_far), int(new_j_so_far))
            if result < num_to_factor:
                right_of_result = get_digits(result, digits_to_match)
                if right_of_result == right_side:
                    if new_i_so_far <= new_j_so_far:
                        result = factor(num_to_factor, new_i_so_far, new_j_so_far)
                    else:
                        result = factor(num_to_factor, new_j_so_far, new_i_so_far)
                    if result:
                        #print "RETURNING 2: ", result
                        return result
    #print "ENDED"

if __name__ == "__main__":
    #statprof.start()
    print factor(int(sys.argv[1]))
    #statprof.stop()
    #statprof.display()
