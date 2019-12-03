
import day1, day2, day3

funcs = [
    (day1.part1, day1.part2),
    (day2.part1, day2.part2),
    (day3.part1, day3.part2),
]


def print_latest():
    print_pair(len(funcs) - 1, funcs[-1])


def print_all():
    for idx, func_pair in enumerate(funcs):
        print_pair(idx, func_pair)


def print_pair(idx, pair):
    print("Day ", idx + 1, ":\n\t", sep='', end='')
    pair[0]()
    print("\t", end='')
    pair[1]()


# print_all()
print_latest()
