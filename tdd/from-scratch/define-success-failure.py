#!/usr/bin/python

# I started with defining success as 'success' and failure as 'failure', and made succeed() and fail() methods
# and TDD'd from there.  I removed lots of duplication, etc.
# What did I discover?  If we use return code to indicate test success or failure,
# we eliminate try/catch blocks, and we actually obviate the need for assertEquals().
# assertEquals(a, b) is the same as return a == b.
# The down side of using return code is you can't have multiple asserts per method.
# Is that really a down side?

def equals(a, b):
    return a == b

# todo: this shouldn't be so exposed
tests = []

def Test(fn):
    tests.append(fn)
    return fn

@Test
def testAssertEqualsSucceed():
    return equals(True, True)

@Test
def testAssertEqualsFail():
    return not equals(True, False)

# todo: this should be a console runner etc.
for test in tests:
    print test.__name__ + ":",
    if test():
        print "pass"
    else:
        print "fail"
