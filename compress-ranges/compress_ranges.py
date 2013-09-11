#!/usr/bin/python

import sys

class IndividualRange(object):
    def __init__(self, begin, end=None):
        if end is None:
            end = begin
        if "-" in str(begin):
            parts = begin.split("-")
            self.begin = int(parts[0])
            self.end = int(parts[1])
        else:
            self.begin = int(begin)
            self.end = int(end)

        if self.end < self.begin:
            self.end, self.begin = self.begin, self.end

    def __str__(self):
        if self.begin == self.end:
            return str(self.begin)
        return "%s-%s" % (self.begin, self.end)

    def is_overlapping(self, range):
        begin_minus_one = self.begin-1
        end_plus_one = self.end+1
        if range.begin >= begin_minus_one and range.begin <= end_plus_one:
            return True
        if range.end >= begin_minus_one and range.end <= end_plus_one:
            return True

    def merge(self, range):
        self.begin = min(self.begin, range.begin)
        self.end = max(self.end, range.end)

class Ranges(object):

    def __init__(self, input):
        self.ranges = []
        if input is None:
            return

        ranges = [IndividualRange(item) for item in input]
        ranges.sort(key=lambda s:s.begin)

        last_range = None
        for range in ranges:
            if last_range is None:
                last_range = range
            else:
                if last_range.is_overlapping(range):
                    last_range.merge(range)
                else:
                    self.ranges.append(last_range)
                    last_range = range
        if last_range is not None:
            self.ranges.append(last_range)

    def __str__(self):
        return ", ".join([str(range) for range in self.ranges])

# this main is untested...
if __name__ == "__main__":
    print str(Ranges([item for item in sys.argv[1:]]))
