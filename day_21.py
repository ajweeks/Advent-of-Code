
import re

f = open("day_21_input.txt")
rulesStr = f.read()

# rulesStr = """../.# => ##./#../...
# .#./..#/### => #..#/..../..../#..#"""

rules = []
for r in rulesStr.split('\n'):
    n = r.split(" => ")
    n[0] = re.sub('/', '', n[0])
    n[1] = re.sub('/', '', n[1])
    rules.append(n)


def print_block(block):
    if len(block) == 9:
        print(block[:3])
        print(block[3:6])
        print(block[6:])
        print()
    else:
        print(block[:2])
        print(block[2:])
        print()


# 0 1 2
# 3 4 5
# 6 7 8

# 0 1
# 2 3

# block and rule should be solid string of chars (e.g., "##..", "#.#." for a 2x2 block)
def match_rule(block, rule):
    if len(block) != len(rule):
        return False

    rots3 = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],  # identity
        [6, 3, 0, 7, 4, 1, 8, 5, 2],  # rotate cw 90
        [8, 7, 6, 5, 4, 3, 2, 1, 0],  # rotate 180
        [2, 5, 8, 1, 4, 7, 0, 3, 6],  # rotate ccw 90
    ]

    flips3 = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],  # identity
        [2, 1, 0, 5, 4, 3, 8, 7, 6],  # h flip
        [6, 7, 8, 3, 4, 5, 0, 1, 2],  # v flip
    ]

    rots2 = [
        [0, 1, 2, 3],  # identity
        [2, 0, 3, 1],  # rotate cw 90
        [3, 2, 1, 0],  # rotate 180
        [1, 3, 0, 2],  # rotate ccw 90
    ]

    flips2 = [
        [0, 1, 2, 3],  # identity
        [1, 0, 3, 2],  # h flip
        [2, 3, 0, 1],  # v flip
    ]

    if len(block) == 9:
        for r in rots3:
            for f in flips3:
                if block[f[r[0]]] == rule[0] and \
                        block[f[r[1]]] == rule[1] and \
                        block[f[r[2]]] == rule[2] and \
                        block[f[r[3]]] == rule[3] and \
                        block[f[r[4]]] == rule[4] and \
                        block[f[r[5]]] == rule[5] and \
                        block[f[r[6]]] == rule[6] and \
                        block[f[r[7]]] == rule[7] and \
                        block[f[r[8]]] == rule[8]:
                    # print("match 3")
                    # print_block(rule)
                    return True
    else:
        for r in rots2:
            for f in flips2:
                if block[f[r[0]]] == rule[0] and \
                        block[f[r[1]]] == rule[1] and \
                        block[f[r[2]]] == rule[2] and \
                        block[f[r[3]]] == rule[3]:
                    # print("match 2")
                    # print_block(rule)
                    return True
    return False


image = """.#...####"""
size = 3  # side-length count


#
# 9 1      0 2 1
# 2 3  =>  2 2 3
#          2 3 3
#
# 0 2 1      2 2 3 1
# 2 2 3  =>  2 1 7 9
# 2 3 3      4 5 6 6
#            8 9 5 4
#
# 2 3 1 6      2 3 1 | 0 1 2
# 5 2 1 4      2 4 5 | 0 8 4
# 5 1 3 6      4 8 9 | 0 9 6
# 4 5 6 6  =>  -------------
#              2 3 1 | 0 1 2
#              2 4 5 | 0 8 4
#              4 8 9 | 0 9 6
#

print(size)
print_block(image)

iterations = 5
for i in range(iterations):
    print("iteration:", i, "size:", size)

    replacementBlockSize = 0
    newBlockSize = 0
    blockCount = 0  # side-length count
    pSize = size
    if size % 2 == 0:
        replacementBlockSize = 2
        newBlockSize = 3
        blockCount = int(size / replacementBlockSize)
        size = (blockCount * 3)
        new_image = ["!"] * (size * size)
    else:
        replacementBlockSize = 3
        newBlockSize = 4
        blockCount = int(size / replacementBlockSize)
        size = (blockCount * 4)
        new_image = ["!"] * (size * size)

    for blockIndex in range(blockCount * blockCount):
        oldImgIdx = (blockIndex * replacementBlockSize) % pSize + int((blockIndex * replacementBlockSize) / pSize) * pSize * replacementBlockSize
        imgIdx = (blockIndex * newBlockSize) % size + int((blockIndex * newBlockSize) / size) * size * newBlockSize
        matched = False

        pBlock = ["!"] * (replacementBlockSize * replacementBlockSize)
        if replacementBlockSize == 3:
            pBlock[0] = image[oldImgIdx + 0 + pSize * 0]
            pBlock[1] = image[oldImgIdx + 1 + pSize * 0]
            pBlock[2] = image[oldImgIdx + 2 + pSize * 0]
            pBlock[3] = image[oldImgIdx + 0 + pSize * 1]
            pBlock[4] = image[oldImgIdx + 1 + pSize * 1]
            pBlock[5] = image[oldImgIdx + 2 + pSize * 1]
            pBlock[6] = image[oldImgIdx + 0 + pSize * 2]
            pBlock[7] = image[oldImgIdx + 1 + pSize * 2]
            pBlock[8] = image[oldImgIdx + 2 + pSize * 2]
        else:
            pBlock[0] = image[oldImgIdx + 0 + pSize * 0]
            pBlock[1] = image[oldImgIdx + 1 + pSize * 0]
            pBlock[2] = image[oldImgIdx + 0 + pSize * 1]
            pBlock[3] = image[oldImgIdx + 1 + pSize * 1]

        for r in rules:
            if match_rule(pBlock, r[0]):
                matched = True
                replacement = r[1]
                if replacementBlockSize == 3:
                    new_image[imgIdx + 0 + size * 0] = replacement[0]
                    new_image[imgIdx + 1 + size * 0] = replacement[1]
                    new_image[imgIdx + 2 + size * 0] = replacement[2]
                    new_image[imgIdx + 3 + size * 0] = replacement[3]
                    new_image[imgIdx + 0 + size * 1] = replacement[4]
                    new_image[imgIdx + 1 + size * 1] = replacement[5]
                    new_image[imgIdx + 2 + size * 1] = replacement[6]
                    new_image[imgIdx + 3 + size * 1] = replacement[7]
                    new_image[imgIdx + 0 + size * 2] = replacement[8]
                    new_image[imgIdx + 1 + size * 2] = replacement[9]
                    new_image[imgIdx + 2 + size * 2] = replacement[10]
                    new_image[imgIdx + 3 + size * 2] = replacement[11]
                    new_image[imgIdx + 0 + size * 3] = replacement[12]
                    new_image[imgIdx + 1 + size * 3] = replacement[13]
                    new_image[imgIdx + 2 + size * 3] = replacement[14]
                    new_image[imgIdx + 3 + size * 3] = replacement[15]
                else:
                    new_image[imgIdx + 0 + size * 0] = replacement[0]
                    new_image[imgIdx + 1 + size * 0] = replacement[1]
                    new_image[imgIdx + 2 + size * 0] = replacement[2]
                    new_image[imgIdx + 0 + size * 1] = replacement[3]
                    new_image[imgIdx + 1 + size * 1] = replacement[4]
                    new_image[imgIdx + 2 + size * 1] = replacement[5]
                    new_image[imgIdx + 0 + size * 2] = replacement[6]
                    new_image[imgIdx + 1 + size * 2] = replacement[7]
                    new_image[imgIdx + 2 + size * 2] = replacement[8]

                break

        if not matched:
            print("Failed to match!")

    image = new_image


pixels_on = image.count("#")

print(f"after {iterations} iterations, {pixels_on} pixels were on")
