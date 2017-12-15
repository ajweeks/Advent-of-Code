
import knot_hash

f = open("day_10_input.txt")
fileStr = f.read()

fileStr = ""

part_1 = False
if part_1:
    instructions = [int(x) for x in fileStr.split(',')]
else:
    instructions = fileStr

print(instructions)


def main():
    pos = 0
    skip = 0

    nums = list(range(256))
    if part_1:
        nums = knot_hash.knot_hash(instructions, pos, skip, nums, False)[2]
        print(nums[0] * nums[1])
    else:
        for i in range(64):
            pos, skip, nums, = knot_hash.knot_hash(instructions, pos, skip, nums, True)

        # nums = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]
        # nums *= 16

        hash_str = knot_hash.knot_hash_to_hex_str(nums)
        print(hash_str)


main()
