#!/bin/env python3

# Clever way to count tanks: https://www.youtube.com/watch?v=WLCwMRJBhuI

import random

# Choose a random total number of items
num_items = random.randint(1, 10000) # TODO nonlinear distribution

num_samples = 10

sampled = []
for i in range(1, num_samples+1):
    rand_num = random.randint(1, num_items)
    while rand_num in sampled:
        rand_num = random.randint(1, num_items)
    sampled.append(rand_num)

print("Samples:", sampled)
m = max(sampled)
print("Guess:", m + ((m-num_samples)/num_samples))
print("Answer:", num_items)
