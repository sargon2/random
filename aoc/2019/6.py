#!/usr/bin/env python3

data = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""

def make_parents(input_data):
    parents = {}
    for item in input_data.splitlines():
        (parent, child) = item.split(")")
        parents[child] = parent

    return parents

def depth(parents, a):
    count = 0
    while a != "COM":
        count += 1
        a = parents[a]
    return count

def count_dist(parents, a, b):
    tot = 0
    a_depth = depth(parents, a)
    b_depth = depth(parents, b)
    if a_depth > b_depth:
        return count_dist(parents, b, a) # inefficient but easy
    # now a_depth <= b_depth
    diff = b_depth - a_depth
    tot += diff
    for i in range(0, diff):
        b = parents[b]

    # Now they're at the same depth, so look for a common ancester.
    while a != b:
        a = parents[a]
        b = parents[b]
        tot += 2
    return tot


def count_orbits(parents):
    orbits = 0
    for k, v in parents.items():
        orbits += 1
        while v != "COM":
            orbits += 1
            v = parents[v]
    return orbits

with open("6.data") as f:
    data = f.read()

parents = make_parents(data)
print(count_dist(parents, parents["YOU"], parents["SAN"]))
