I want to understand RSA encryption better.

So, I'm going to work through this: http://www.muppetlabs.com/~breadbox/txt/rsa.html

In my own words,
A trapdoor function is a function that is hard to find the inverse of.
27 = 3 (mod 12) is the same as 27 % 12 = 3.
a = b (mod c), d = e (mod c), then (a + d) = (b + e) (mod c)

Two numbers are relatively prime if they have no common prime factors. e.g. 21,10. 21 = 3 * 7 and 10 = 2 * 5, no overlap.

phi(n) = the number of numbers that are relatively prime to n, less than n and >= 1.

phi(n) = n-1 if n is prime.

phi(p*q) = (p-1)*(q-1) if p and q are prime.

If T and R are relatively prime (T < R), then T^(phi(R)) = 1 (mod R). T^(phi(R)) % R = 1.

R=6.  phi(R) = 2.
T=5.

5^(2) % 6 = 1.
25 % 6 = 1. Yep.  Another way to write that is 25 = 1 (mod 6).

T^(N * phi(R)) = (N * 1) (mod R).
T^(N * phi(R)) % R = 1.
Let's call N * phi(R) S.  Another way to say that is S % phi(R) = 0, or S = 0 (mod phi(R)).

So, T^S % R = 1.  T^S = 1 (mod R).
T^S * T = 1 * T (mod R).
T^(S + 1) = T (mod R).
T^(S + 2) = T^2 (mod R).
T^E = T^F (mod R) if E = F (mod phi(R)).

Backing up, T^(S+1) % R = T.  Only if T<R, T and R are relatively prime, and S is divisible by phi(R).

Choose P,Q,S such that P*Q = S+1.
P*Q = 1 (mod phi(R)).

T^(P*Q) = T (mod R)
(T^P)^Q = T (mod R).

(T^P) % R = X
(X^Q) % R = T.

T is the plaintext.  X is the ciphertext.  P and R are the public key, and Q and R and the private key.

If you advance a clock by N hours at a time, it will repeat if N is not relatively prime with 12.  If it is, you will visit each number once.

factor(12) = 2 * 2 * 3.  So, we need a number that's not divisible by 2 or 3, but is less than 12.

1 visits each number once.
2, 3 repeat.
4%2=0
5 works.  12, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7, 12.  That's cool.
6%2=0
7 works (that's their example)
9%3=0
11 works -- it just advances backwards.

He says that means it's important that both P and Q be relatively prime to phi(R).  That means there is only one X for each T.

If it was T^P = X and X^Q = T, it wouldn't work, because P would be public knowledge (it would be the public key).  Adding in R makes it secure.

He says if the codebreaker knows T, P, and X, they still can't deduce Q.  Why is that?  In the example below they know R too.  They don't know phi(R) though.  X^? % R = T, and we know X, R, and T.  Is that hard?  Maybe that's hard.  There are lots of possible values for Q, so it's hard to know which is the correct one?

Making a pair of keys:

We choose R to be the product of two primes, U * V.  Why can't R be prime?  So phi(R) isn't just R-1.  The attacker knows R but not phi(R).

We want R to be hard to factor.  Why is that?  To make it hard to find phi(R).

phi(R) = (U-1) * (V-1).  We can discard U and V after calculating R.

Choose P and Q such that P*Q=1 (mod phi(R)).

Example:

U = 5, V = 11.  R = 55.

phi(55) = 4 * 10 = 40.

factor(40) = 2 * 20 = 2 * 2 * 10 = 2 * 2 * 2 * 5.

Now we want to find P and Q.  P*Q = 1 (mod 40).

We want P and Q to be relatively prime.

Let P = 7.  Then 7 * Q = 1 (mod 40).  7 * Q = K * 40 + 1, for any K.

He says let Q = 23.  We just brute-force search for that I guess?

7 * 23 = 161 = 4 * 40 + 1.

So, P=7 and Q=23.

T = 31.  31^7 (mod 55) = 27512614111 (mod 55) = 26.

T = 31, P = 7, Q = 23, X = 26, R = 55.

Back to the not knowing Q thing.  26^Q % 55 = 31.  There are lots of valid values for Q.


