import sys

f = open("day_02_input.txt")
fileStr = f.read()

# fileStr = "5 1 9 5\n7 5 3\n2 4 6 8"
# fileStr = "5 9 2 8\n9 4 7 3\n3 8 6 5"
rows = fileStr.splitlines()


def part1():
    row_sum = 0
    for i in range(len(rows)):
        row_min = sys.maxsize
        row_max = -sys.maxsize
        chars = rows[i].split()
        for j in range(len(chars)):
            val = int(chars[j])
            if val > row_max:
                row_max = val
            if val < row_min:
                row_min = val
        row_sum += row_max - row_min

    print(row_sum)


def part2():
    row_sum = 0
    for i in range(len(rows)):
        quotient = 0
        chars = rows[i].split()
        for j in range(len(chars)):
            val1 = int(chars[j])
            for k in range(len(chars)):
                if j != k:
                    val2 = int(chars[k])
                    if val1 % val2 == 0:
                        quotient = int(val1 / val2)
                        row_sum += quotient

    print(row_sum)


part1()
part2()