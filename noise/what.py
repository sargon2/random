#!/usr/bin/env python3

# The idea here is Perlin noise uses a weird interpolation function,
# and Simplex noise is amazingly complex and patented,
# and OpenSimplex is amazingly complex.
#
# So, what happens if we just sum corners of octaves?  What does it look like?  that would be much simpler.
#
# ANSWER: It looks like a QR code.  We get huge cliffs aligned with the axes, making square shapes.

from PIL import Image
import random
import opensimplex

def get_rand_for(n):
    n = n * 1000;
    random.seed(n)
    return random.random()

def get_rand_for_tuple(t):
    return get_rand_for(t[0] * 500 + t[1])

def generate_noise_basic(x, y):
    result = 0
    octaves = (100, 50, 10, 5, 1)
    for octave in octaves:
        x_val = x // octave
        y_val = y // octave
        result += get_rand_for_tuple((x_val, y_val))
    return result / len(octaves)

def generate_noise(x, y):
    return (opensimplex.noise2(x/100, y/100) + 1) / 2

def generate_noise_with_octaves(x, y, octaves=4, persistence=0.5):
    total = 0
    frequency = 1
    amplitude = 1
    max_value = 0  # This will store the sum of all amplitudes to normalize the result at the end

    for i in range(octaves):
        total += opensimplex.noise2(x / 100 * frequency, y / 100 * frequency) * amplitude

        max_value += amplitude
        amplitude *= persistence
        frequency *= 2

    return (total / max_value + 1) / 2


# I tried to do a linear interpolation, but it turned out that was hard to do on a square.

opensimplex.seed(1234)

img = Image.new('RGB', [500,500], 255)
data = img.load()

for x in range(img.size[0]):
    for y in range(img.size[1]):
        value = generate_noise_with_octaves(x, y)
        value *= 255;
        value = int(value)
        data[x,y] = (value, value, value)

img.save('image.png')
