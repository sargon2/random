import unittest2

# The idea here is we list the N largest items in the given folder.
# e.g.:
# <size> Files in . except those listed below
# <size> ./folder1 except those listed below
# <size> ./folder1/folder2
# <size> ./folder3 # has many folder in it, but they're small individually, so we don't list them here

# Maybe ./folder1/<etc> or something is better wording.

# First, get an overall size.
# Then, recurse, and at each level, either return the current folder, or split it and recurse further.
# We can only "split" one item off -- no "<size> folder1 and folder2" or anything like that.

# Maybe I should have a split() function that takes in a folder, finds the largest unsplit item, and splits it.
# Then I could just call it N times.

class TestDu(unittest2.TestCase):
    def test_things(self):
        pass
