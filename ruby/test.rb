#!/usr/local/bin/ruby

def comb(n, r)
	if(r > 0)
		return n * comb(n-1, r-1) / r
	else
		return 1
	end
end
def factorial(n)
	if n == 1
		n
	else
		n * factorial(n-1)
	end
end

# Have to subtract the hands with more than one straight flush in them
straightflush = 4 * 10 * comb(52-5, 2) - (4 * 9 * (52-6))
print "Straight flush: ", straightflush, "\n"

fourofakind = 13 * comb(52-4, 3)
print "Four of a kind: ", fourofakind, "\n"

# AAABBBC, 13 choose 2 ranks, 4 choose 3 suits for each, minus 4-of-a-kinds
fullhouse = comb(13, 2) * comb(4, 3) * comb(4, 3) * (52-6-2)
# AAABBCC
fullhouse += 13 * comb(12, 2) * comb(4, 3) * comb(4, 2)**2
# AAABBCD
fullhouse += 13 * 12 * comb(11, 2) * comb(4, 3) * comb(4, 2) * 4 * 4
print "Full house: ", fullhouse, "\n"

# all 7 cards the same suit
flush = comb(13, 7) * 4
# 6 cards the same, one different
flush += comb(13, 6) * 4 * 3 * 13
# 5 cards the same, 2 anything
flush += comb(13, 5) * 4 * comb(13*3, 2)
# But not straight flushes
flush -= straightflush
print "Flush: ", flush, "\n"

# http://www.math.sfu.ca/~alspach/comp20/
