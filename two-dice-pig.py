#!/usr/bin/env python3 -u

# Monte carlo simulation of two-dice pig to tell what is a good score.

from collections import defaultdict
import random
import operator

num_trials = 1000

def do_run(stop_at, overall_score):
    # For now, quit on any 1
    score = overall_score
    must_reroll = False
    while True:
        if must_reroll is False:
            if score >= 100:
                return 100
            if score >= stop_at:
                return score
        must_reroll = False
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        if d1 + d2 == 2:
            return 0
        if d1 == d2:
            must_reroll = True
        score += d1 + d2
        if d1 == 1:
            return overall_score
        if d2 == 1:
            return overall_score


def main():
    # There's a turn score, and an overall score.
    results = defaultdict(lambda: {})
    print("overall_score stop_at diff result")
    for overall_score in range(1, 100):
        for stop_at in range(overall_score, min(overall_score+30, 101)):
            scores = []
            for i in range(num_trials):
                score = do_run(stop_at, overall_score)
                scores.append(score)
            results[stop_at] = sum(scores) / len(scores)
        highest_key = max(results.items(), key=operator.itemgetter(1))[0]
        print(overall_score, highest_key, highest_key - overall_score, results[highest_key])


if __name__ == "__main__":
    main()

""" 6/25/2020 num_trials=100000
overall_score stop_at diff result
1 18 17 8.94356
2 21 19 9.84181
3 19 16 10.82104
4 21 17 11.77585
5 21 16 12.68038
6 25 19 13.64345
7 24 17 14.58576
8 24 16 15.57434
9 27 18 16.4777
10 27 17 17.42977
11 27 16 18.36705
12 28 16 19.28377
13 27 14 20.24758
14 32 18 21.24589
15 30 15 22.12174
16 32 16 23.06842
17 33 16 24.03039
18 33 15 24.96935
19 35 16 25.90449
20 35 15 26.87769
21 38 17 27.86992
22 37 15 28.7618
23 39 16 29.71245
24 38 14 30.68022
25 39 14 31.58175
26 43 17 32.5331
27 40 13 33.46175
28 42 14 34.40249
29 44 15 35.37634
30 45 15 36.31585
31 46 15 37.24803
32 46 14 38.2219
33 46 13 39.16274
34 49 15 40.14481
35 47 12 41.07838
36 49 13 42.03736
37 52 15 42.97946
38 52 14 43.92907
39 51 12 44.85341
40 52 12 45.82128
41 55 14 46.75131
42 54 12 47.77759
43 56 13 48.68799
44 59 15 49.56849
45 57 12 50.55427
46 59 13 51.47857
47 62 15 52.4313
48 62 14 53.37788
49 62 13 54.32911
50 66 16 55.30534
51 62 11 56.26507
52 64 12 57.20829
53 67 14 58.12526
54 68 14 59.07325
55 68 13 60.07827
56 68 12 60.97981
57 70 13 61.95524
58 71 13 62.90881
59 70 11 63.92788
60 70 10 64.75773
61 72 11 65.73814
62 74 12 66.65273
63 76 13 67.60036
64 74 10 68.55507
65 76 11 69.55639
66 78 12 70.51022
67 78 11 71.40073
68 80 12 72.49496
69 80 11 73.32526
70 83 13 74.33403
71 82 11 75.232
72 82 10 76.25348
73 83 10 77.1931
74 86 12 78.07745
75 87 12 79.07622
76 87 11 80.08543
77 88 11 80.95378
78 88 10 82.07035
79 89 10 82.8238
80 90 10 83.85028
81 94 13 84.73483
82 95 13 85.74029
83 96 13 86.68577
84 95 11 87.68018
85 97 12 88.5424
86 97 11 89.55691
87 99 12 90.50314
88 98 10 91.49809
89 98 9 92.40189
90 98 8 93.33993
91 100 9 94.25463
92 98 6 95.25989
93 100 7 96.18492
94 100 6 97.06668
95 96 1 97.96437
96 99 3 98.89906
97 98 1 99.97453
98 99 1 100.819
99 100 1 101.94798
"""
