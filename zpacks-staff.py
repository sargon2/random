
# Problem: given a 4-section pole, what section lengths are ideal?
# - They should sum to 59.5
# - They should be in round half-inch sizes
# - The length of the longest pole should be minimized
# - No two combinations of pole lengths should be the same total length

def what():
    for i in range(0, 595, 5):
        for j in range(0, i, 5):
            for k in range(0, j, 5):
                l = 595 - (i+j+k)
                if l < 0:
                    continue
                sizeset = set()
                sizeset.add(0)
                sizeset.add(i)
                sizeset.add(j)
                sizeset.add(k)
                sizeset.add(l)
                sizeset.add(i+j)
                sizeset.add(i+k)
                sizeset.add(i+l)
                sizeset.add(j+k)
                sizeset.add(j+l)
                sizeset.add(k+l)
                sizeset.add(i+j+k)
                sizeset.add(i+j+l)
                sizeset.add(i+k+l)
                sizeset.add(j+k+l)
                sizeset.add(i+j+k+l)
                #if len(sizeset) <= 12:
                #    continue
                #if 380 not in sizeset:
                #    continue
                if 480 not in sizeset and 485 not in sizeset and 475 not in sizeset:
                    continue
                if 520 not in sizeset and 525 not in sizeset and 515 not in sizeset:
                    continue
                # The two smallest plus 2.5 should equal the middle + 2.5 should equal the largest.
                sizes = sorted([i, j, k, l])
                for m in range(20, 35, 5):
                    if abs(sizes[2] + m - sizes[3]) > 5:
                        continue
                    if abs(sizes[0] + sizes[1] + m - sizes[3]) > 5:
                        continue

                    print(m, sizes)


if __name__ == "__main__":
    what()
