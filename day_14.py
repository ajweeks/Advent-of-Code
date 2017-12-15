
import knot_hash

f = open("day_14_input.txt")
fileStr = f.read()

# fileStr = "flqrgnkx"


def hex_to_binary(hex_num):
    return ''.join(bin(int(h, 16))[2:].zfill(4) for h in hex_num)


def flood(x, y, grid):
    if x < 0 or y < 0 or x > 127 or y > 127 or grid[x + y * 128] == 0:
        return grid

    grid[x + y * 128] = 0
    grid = flood(x - 1, y, grid)
    grid = flood(x + 1, y, grid)
    grid = flood(x, y - 1, grid)
    grid = flood(x, y + 1, grid)

    return grid


def defrag(p1):
    square_count = 0

    grid = []

    for row in range(128):
        instructions = fileStr + '-' + str(row)
        pos = 0
        skip = 0
        nums = list(range(256))
        for i in range(64):
            pos, skip, nums = knot_hash.knot_hash(instructions, pos, skip, nums, True)

        hash_str = knot_hash.knot_hash_to_hex_str(nums)
        binary_str = hex_to_binary(hash_str)

        for c in binary_str:
            if c == '1':
                square_count += 1

        for x in binary_str:
            grid.append(int(x))

    if p1:
        print(square_count)
    else:
        print(grid, len(grid))
        island_count = 0
        for x in range(128):
            for y in range(128):
                if grid[x + y * 128] == 1:
                    island_count += 1
                    grid = flood(x, y, grid)

        print("island count:", island_count)


part_1 = True
defrag(part_1)
