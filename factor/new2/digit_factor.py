#!/usr/bin/python

import sys

# i and j must be the same length for this to work


def get_digits(number, digits):
    return str(number)[-digits:]

def strlen(number):
    return len(str(number))

def factor(num_to_factor, i_so_far="", j_so_far=""):
    #print "factor(" + str(i_so_far) + ", " + str(j_so_far) + ")"
    digits_to_match = strlen(i_so_far) + 1
    right_side = get_digits(num_to_factor, digits_to_match)
    for i in range(0,10):
        for j in range(0,10):
            new_i_so_far = str(i) + str(i_so_far)
            new_j_so_far = str(j) + str(j_so_far)
            result = int(new_i_so_far) * int(new_j_so_far)
            #print "new i is", new_i_so_far, ", new j is", new_j_so_far, "result is", result
            if result == num_to_factor:
                if int(new_j_so_far) != 1 and int(new_i_so_far) != 1:
                    #print "RETURNING 1: ", (new_i_so_far, new_j_so_far)
                    return (int(new_i_so_far), int(new_j_so_far))
            if result < num_to_factor:
                right_of_result = get_digits(result, digits_to_match)
                if right_of_result == right_side:
                    result = factor(num_to_factor, new_i_so_far, new_j_so_far)
                    if result:
                        #print "RETURNING 2: ", result
                        return result
    #print "ENDED"

if __name__ == "__main__":
    print factor(int(sys.argv[1]))
