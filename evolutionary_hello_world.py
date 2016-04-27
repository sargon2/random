#!/usr/bin/env python

from random import randint

target = "Hello, World!"

def string_distance(string1, string2):
    distance = 0
    # Adding a character increases distance
    if len(string1) > len(string2):
        string1, string2 = string2, string1

    diff = len(string2) - len(string1)
    distance += diff
    string1 += " " * diff

    for i in range(0, len(string1)):
        char1 = string1[i]
        char2 = string2[i]
        diff += abs(ord(char1) - ord(char2))
    return diff

def mutate(string):
    what_to_do = randint(0, 9)
    if len(string) == 0:
        what_to_do = 1
    if what_to_do == 1:
        return string + chr(randint(1, 255))
    if what_to_do == 2:
        return string[0:len(string)-1]
    which_char = randint(0, len(string)-1)
    l = list(string)
    if randint(1, 2) == 1:
        l[which_char] = chr(ord(l[which_char])+1)
    else:
        l[which_char] = chr(ord(l[which_char])-1)
    return "".join(l)



curr = ""
generation_number = 0
while curr != target:
    curr_child = mutate(curr)
    generation_number += 1
    dist1 = string_distance(curr, target)
    dist2 = string_distance(curr_child, target)
    if dist2 < dist1:
        curr = curr_child
        print "curr is", curr, "/ gen #", generation_number, "/ fitness is", dist2
