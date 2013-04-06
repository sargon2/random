#!/usr/bin/python

num_to_factor = 289

for digits_to_match in range(1, strlen(num_to_factor)):
    right_side = get_digits(num_to_factor, digits_to_match)
    for i in range(0,10):
        for j in range(0,10):
            result = i * j
            if result == num_to_factor:
                sys.exit("i is " + i, "j is " + j)
            if result < num_to_factor:
                right_of_result = get_digits(result, digits_to_match)
                if right_of_result == right_side:
                    recurse(...)
