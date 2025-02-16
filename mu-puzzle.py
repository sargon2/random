#!/usr/bin/env python3

# From Godel, Escher, Bach.  The MU puzzle.

import sys

# Rules:
# If it ends in I - add U on end
# Mx -> Mxx
# III -> U
# drop UU

start_state = "MI"
end_state = "MU"

def children(s):
    if s[-1] == "I":
        yield s + "U"
    tail = s[1:]
    yield s + tail
    for i in range(0, len(s)):
        if s[i:i+3] == "III":
            yield s[0:i] + "U" + s[i+3:]
    for i in range(0, len(s)):
        if s[i:i+2] == "UU":
            yield s[0:i] + s[i+2:]

def sfs(): # shortest-first search
    state = start_state
    unexplored = [state]
    explored = []

    i = 0
    while(True):
        explored.append(state)
        if(i % 1000) == 0:
            print("i is", i, "state is", state)
        i += 1
        unexplored.extend(children(state))
        unexplored = list(set(unexplored) - set(explored))
        unexplored.sort(key = len)

        state = unexplored.pop(0)
        if state == end_state:
            print("Win")
            sys.exit(0)

sfs()


#def dfs(max_depth, state = None):
#    if state == None:
#        state = start_state
#
#    if state == end_state:
#        print(state)
#        return "Win"
#
#    if max_depth == 0:
#        return
#
#    for child in children(state):
#        result = dfs(max_depth-1, child)
#        if result == "Win":
#            print(state)
#            return "Win"
#
## Iterative deepening search
#max_depth = 1
#while True:
#    max_depth += 1
#    print("Depth", max_depth)
#    result = dfs(max_depth)
#    if result == "Win":
#        sys.exit()
