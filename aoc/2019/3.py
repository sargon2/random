#!/usr/bin/env python3

import unittest

# TODO for part 2, if a line intersects with itself, it changes the number of steps for remaining movements.
# So can I be clever and get away with not straight-up simulating it?

class TestThings(unittest.TestCase):
    def test_single_segment_intersects(self):
        self.assertTrue(single_segment_intersects(((0,0),(3,0)),((1,-1),(1,1))))

def segments_intersect(horizontal_list, vertical_list):
    ret = []

    first = True
    for h in horizontal_list:
        for v in vertical_list:
            if not first: # Ignore the first one since they always start at 0,0
                result = single_segment_intersects(h, v)
                if result is not None:
                    ret.append(result)
            first = False
    return ret

def single_segment_intersects(horizontal, vertical):
    # Assumes segments are left-to-right and bottom-to-top
    if horizontal[0][0] > vertical[0][0]:
        return None
    if horizontal[1][0] < vertical[0][0]:
        return None
    if vertical[0][1] > horizontal[0][1]:
        return None
    if vertical[1][1] < horizontal[1][1]:
        return None
    return (vertical[0][0], horizontal[0][1])

def get_segments(in_string):
    horizontal = []
    vertical = []
    curr_pos = (0, 0)
    items = in_string.split(",")
    for item in items:
        direction = item[0]
        distance = int(item[1:])
        if direction == "R":
            new_pos = (curr_pos[0]+distance, curr_pos[1])
            horizontal.append((curr_pos, new_pos))
        elif direction == "L":
            new_pos = (curr_pos[0]-distance, curr_pos[1])
            horizontal.append((new_pos, curr_pos))
        elif direction == "U":
            new_pos = (curr_pos[0], curr_pos[1]+distance)
            vertical.append((curr_pos, new_pos))
        elif direction == "D":
            new_pos = (curr_pos[0], curr_pos[1]-distance)
            vertical.append((new_pos, curr_pos))
        curr_pos = new_pos
    return (horizontal, vertical)

def calc_distance(point, in_string):
    # TODO we're reparsing input_str, we should only parse it once
    curr_pos = (0, 0)
    items = in_string.split(",")
    tot_dist = 0
    for item in items:
        direction = item[0]
        distance = int(item[1:])
        if direction == "R":
            new_pos = (curr_pos[0]+distance, curr_pos[1])
            if point[1] == curr_pos[1] and curr_pos[0] <= point[0] and point[0] <= new_pos[0]:
                return tot_dist + (point[0] - curr_pos[0])
        elif direction == "L":
            new_pos = (curr_pos[0]-distance, curr_pos[1])
            if point[1] == curr_pos[1] and curr_pos[0] >= point[0] and point[0] >= new_pos[0]:
                return tot_dist + (curr_pos[0] - point[0])
        elif direction == "U":
            new_pos = (curr_pos[0], curr_pos[1]+distance)
            if point[0] == curr_pos[0] and curr_pos[1] <= point[1] and point[1] <= new_pos[1]:
                return tot_dist + (point[1] - curr_pos[1])
        elif direction == "D":
            new_pos = (curr_pos[0], curr_pos[1]-distance)
            if point[0] == curr_pos[0] and curr_pos[1] >= point[1] and point[1] >= new_pos[1]:
                return tot_dist + (curr_pos[1] - point[1])
        tot_dist += distance
        curr_pos = new_pos


def find_closest(point_list, input1, input2):
    closest = None
    closest_val = None
    for point in point_list:
        #val = abs(point[0]) + abs(point[1])
        val1 = calc_distance(point, input1)
        val2 = calc_distance(point, input2)
        val = val1 + val2
        if closest is None or val < closest_val:
            closest = point
            closest_val = val
    return closest, closest_val

if __name__ == "__main__":

    #input1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    #input2 = "U62,R66,U55,R34,D71,R55,D58,R83"

    #input1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    #input2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

    input1 = "R1001,D890,R317,U322,L481,D597,L997,U390,L78,D287,L401,U638,R493,D493,R237,U29,R333,D466,L189,D634,R976,U934,R597,U62,L800,U229,R625,D927,L629,D334,L727,U4,R716,U20,L284,U655,R486,U883,R194,U49,L845,D960,R304,D811,L38,U114,R477,D318,L308,U445,L26,D44,R750,D12,R85,D146,R353,U715,R294,D595,L954,U267,L927,U383,L392,D866,L195,U487,L959,U630,R528,D482,R932,D541,L658,D171,L964,U687,R118,U53,L81,D381,R592,U238,L391,U399,R444,U921,R706,U925,R204,D220,L595,U489,R621,D15,R104,D567,L664,D54,R683,U654,R441,D748,L212,D147,L699,U296,L842,U230,L684,D470,R247,D421,R38,D757,L985,U791,R112,U494,R929,D726,L522,U381,R184,D492,L517,D819,R487,D620,R292,D206,R254,D175,L16,U924,R838,D423,R756,D720,L555,U449,L952,D610,L427,U391,R520,D957,R349,D670,L678,U467,R804,U757,L342,U808,R261,D597,L949,U162,R3,D712,L799,U531,R879,D355,R325,D173,L303,U679,L432,D421,R613,U431,L207,D669,R828,D685,R808,U494,R821,U195,L538,U16,L835,D442,L77,U309,L490,U918,L6,D200,L412,D272,L416,U774,L75,D23,L193,D574,R807,D382,L314,D885,R212,D806,L183,U345,L932,U58,L37,U471,R345,U678,R283,U644,L559,U892,L26,D358,L652,D606,L251,U791,L980,D718,L14,D367,R997,D812,R504,D474,L531,U708,R660,U253,L86,D491,R971,U608,L166,U659,R167,U92,L600,U20,R28,U852,R972,D409,L719,D634,R787,D796,L546,D857,L987,U111,L916,D108,R537,U931,R308,U385,L258,D171,R797,U641,R798,D723,R600,D710,R436,U587,R16,D564,L14,D651,R709,D587,R626,U270,R802,U937,R31,U518,L187,D738,R562,D238,R272,D403,R788,D859,L704,D621,L547,D737,L958,U311,L927"
    input2 = "L1007,U199,L531,D379,L313,U768,L87,U879,R659,U307,L551,D964,L725,D393,R239,D454,R664,U402,R100,D62,R53,D503,R918,U998,L843,D142,R561,U461,R723,D915,L217,D126,L673,U171,R131,U518,R298,U99,L852,D799,L159,U161,R569,D802,L391,D553,L839,U954,R502,U351,R851,D11,L243,D774,L642,U613,R376,U867,L357,D887,L184,D298,R406,U912,R900,D348,L779,U494,R240,D712,R849,D684,R475,D449,L94,U630,L770,D426,L304,D869,R740,D377,R435,D719,L815,D211,R391,U484,R350,U599,R57,U210,R95,U500,L947,D649,R615,D404,L953,D468,R380,U215,R82,D872,R150,D347,L700,D450,L90,U803,L593,U296,R408,U667,R407,U725,R197,U269,R115,D758,R558,U62,L519,U308,R259,U869,L846,U3,R592,D357,R633,D909,L826,U165,L190,D821,L525,U404,R63,D214,R265,U74,L715,U461,L840,D647,R782,D655,R72,D601,L435,U549,L108,U687,R836,D975,L972,U813,R258,U703,R90,D438,R434,D818,R184,D886,R271,U31,L506,U395,L274,U455,R699,U889,L162,U771,R752,U317,R267,D959,R473,U58,R552,U51,R637,D726,R713,D530,L209,D824,R275,D207,R357,D373,L169,U880,L636,U409,R67,D740,R225,D272,R114,U970,R51,U230,R859,U820,L979,D153,R16,D883,L542,U806,L523,D752,L712,U55,L739,U746,R910,D873,R108,D558,L54,D619,L444,U941,R613,U478,L839,D910,R426,D614,L622,U928,L65,D644,L208,U971,L939,U874,R827,U672,L620,U140,L493,D637,L767,U831,R874,U468,R648,U714,R294,D606,L375,D962,L105,D919,L486,D771,L827,D196,L408,U217,L960,D633,L850,U805,L188,U566,L884,D212,L677,D204,R257,D409,R309,D783,L773,D588,L302,U129,L550,U919,L482,U563,R290,U690,R586,D460,L771,D63,R451,D591,L861,D598,L432,U818,L182"

    (h1, v1) = get_segments(input1)
    (h2, v2) = get_segments(input2)

    intersections_1 = segments_intersect(h1, v2)
    intersections_2 = segments_intersect(h2, v1)

    intersections_1.extend(intersections_2)

    print(find_closest(intersections_1, input1, input2))
