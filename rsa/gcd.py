import fractions
import random

R = 8876044532898802067

# phi(R) = 7416037547
# The chance of finding one of these is 7416037547/8876044532898802067 = .0000000008 or 1 in 1.2 billion.

done = False
i = 0
while not done:
    n = random.randint(1, R)
    gcd = fractions.gcd(R, n)
    if gcd != 1:
        print "For %d, got gcd of %d" % (n, gcd)
        done = True
    i += 1
    if i % 100000 == 0:
        print "i is %d" % i

