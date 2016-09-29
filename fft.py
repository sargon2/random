# FFT.

# https://www.youtube.com/watch?v=iTMn0Kt18tg

# Polynomial/frequency domain -> samples

# We have an array of numbers.

# A(x) = a[0] + a[1]*x + a[2]*x^2 + ...

# Divide into evens and odds.

# Aeven(x) = a[0] + a[2]*x + a[4]*x^2 + ...
# Aodd(x) = a[1] + a[3]*x + a[5]*x^2 + ...

# Now, we want to convert a single number.

# Aeven(x) = a[0].  That's easy.

# Combine.

# A(x) = Aeven(x^2) + x * Aodd(x^2)

import math

def fft(in_ary, out_size=None):
    if out_size is None:
        out_size = len(in_ary)
    if len(in_ary) == 1:
        return [in_ary[0]] * out_size
    evens = in_ary[::2]
    odds = in_ary[1::2]
    even_result = fft(evens, out_size)
    odd_result = fft(odds, out_size)
    result = []
    for x in xrange(out_size): # assumes x sub k = k
        val = even_result[x] + math.sqrt(x) * odd_result[x]
        result.append(val)
    return result

# TODO: we want all the x's to be nth roots of unity instead of k

print fft([1, 2, 3, 4])

