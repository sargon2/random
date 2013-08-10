#!/usr/bin/python

import sys

# (Aug. 10, 2013)

# References:
# http://imranontech.com/2007/01/24/using-fizzbuzz-to-find-developers-who-grok-coding/
# http://c2.com/cgi/wiki?FizzBuzzTest

# I admit it.  I think FizzBuzz is a hard problem.
# It's easy to do, but hard to do *well*.  It's hard to do without duplication.
# Printing "fizz" and printing "fizzbuzz" both duplicate printing "fizz".
# Checking for i%3 and i%15 duplicates the check for i%3.

# This is the least duplication I can come up with:

for i in range(1, 100):
    printed = False
    if i % 3 == 0:
        sys.stdout.write("fizz")
        printed = True
    if i % 5 == 0:
        sys.stdout.write("buzz")
        printed =  True
    if not printed:
        sys.stdout.write(str(i))
    sys.stdout.write("\n")

# Full duplication looks like this:

#for i in range(1, 100):
#    if i % 3 == 0:
#        if i % 5 == 0:
#            print "fizzbuzz"
#        else:
#            print "fizz"
#    else:
#        if i % 5 == 0:
#            print "buzz"
#        else:
#            print i
