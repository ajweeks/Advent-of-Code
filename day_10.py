
f = open("day_10_input.txt")
fileStr = f.read()

# fileStr = ""

part_1 = False
if part_1:
    instructions = [int(x) for x in fileStr.split(',')]
else:
    instructions = [ord(c) for c in fileStr]
    for i in [17, 31, 73, 47, 23]:
        instructions.append(i)

# print(instructions)


def knot_hash(current_pos, skip_size, nums):
    for length in instructions:
        print(length, current_pos, skip_size)

        # Reverse section
        for i in range(int(length / 2)):
            i1 = (i + current_pos) % len(nums)
            i2 = (length - i - 1 + current_pos) % len(nums)
            nums[i1], nums[i2] = nums[i2], nums[i1]

        current_pos = (current_pos + length + skip_size) % len(nums)
        skip_size += 1

    return nums[0] * nums[1], current_pos, skip_size, nums


def to_hex(num):
    res = hex(num)[2:]
    if len(res) == 1:
        res = '0' + res
    return res


def main():
    pos = 0
    skip = 0

    if part_1:
        print(knot_hash(pos, skip, nums)[0])
    else:
        nums = list(range(256))

        for i in range(64):
            n, pos, skip, nums, = knot_hash(pos, skip, nums)
            # print(n, pos, skip)
        # print(nums)

        # nums = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]
        # nums *= 16

        dense = []
        for i in range(16):
            dense.append(nums[i * 16])
            for j in range(1, 16):
                dense[i] ^= nums[i * 16 + j]
        print(dense)

        hash_str = ""
        for d in dense:
            hash_str += to_hex(d)
        print(hash_str)


main()