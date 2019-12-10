
start = 145852
end = 616942

tot = 0
for i in range(start, end+1):
    nums = [int(d) for d in str(i)]
    valid = True
    has_adjacent = False
    for i in range(0, 5):
        if nums[i] > nums[i+1]:
            valid = False
        if i == 0 and nums[0] == nums[1] and nums[1] != nums[2]:
            has_adjacent = True
        elif i == 4 and nums[4] == nums[5] and nums[4] != nums[3]:
            has_adjacent = True
        elif i > 0 and i < 4 and nums[i] == nums[i+1] and nums[i] != nums[i-1] and nums[i+1] != nums[i+2]:
            has_adjacent = True
    if not has_adjacent:
        valid = False
    if valid:
        tot += 1

print(tot)
