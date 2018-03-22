# https://www.reddit.com/r/personalfinance/comments/86bx1n/fair_way_to_split_rent_advice_needed/

from itertools import permutations

# My idea for dividing up the house and assigning costs based on users' preferences...

def print_results(preferences, total_cost):

    # Normalize preferences
    normalized = []
    for pref_vector in preferences:
        for pref in pref_vector:
            if pref  < 0:
                raise Exception("No negative values allowed.")
        s = sum(pref_vector)
        normalized.append([i / s for i in pref_vector])

    num_people = len(preferences)

    for perm in permutations(range(num_people)):
        print("For permutation", perm, ":")
        # Sum utility values
        tot = 0
        for i in range(num_people):
            tot += normalized[i][perm[i]]
        if tot == 0:
            print("skip, total utility 0")
            continue
        # Print permutation and amounts
        for i in range(num_people):
            value = normalized[i][perm[i]] / tot
            print("Person", i, "gets item", perm[i], "; value", value, "cost", total_cost * value)


#                item 0  item 1
preferences = [[      3,      2], # person 0
               [      5,      4]] # person 1

total_cost = 1000

print_results(preferences, total_cost)

