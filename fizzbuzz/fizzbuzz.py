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

# Modified solution from http://c2.com/cgi/wiki?FizzBuzz
for i in range(1, 100):
    data = [(3, "fizz"), (5, "buzz")]
    line = ""
    for num, word in data:
        if i % num == 0:
            line += word
    if line:
        print line
    else:
        print i

# This is the least duplication I can come up with:

#for i in range(1, 100):
#    printed = False
#    if i % 3 == 0:
#        sys.stdout.write("fizz")
#        printed = True
#    if i % 5 == 0:
#        sys.stdout.write("buzz")
#        printed =  True
#    if not printed:
#        sys.stdout.write(str(i))
#    sys.stdout.write("\n")

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

# Another interesting solution 12/15/2014:
#def none(*args):
#    for arg in args:
#        if arg: return False
#    return True
#
#for i in range(1, 100):
#    fizz = i % 3 == 0
#    buzz = i % 5 == 0
#    if fizz:
#        sys.stdout.write("fizz")
#    if buzz:
#        sys.stdout.write("buzz")
#    if none(fizz, buzz):
#        sys.stdout.write(str(i))
#    sys.stdout.write("\n")

