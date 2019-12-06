
import day01, day02, day03, day04, day05, day06

funcs = [
    (day01.part1, day01.part2),
    (day02.part1, day02.part2),
    (day03.part1, day03.part2),
    (day04.part1, day04.part2),
    (day05.part1, day05.part2),
    (day06.part1, day06.part2),
]


def print_latest():
    print_pair(len(funcs) - 1, funcs[-1])


def print_all():
    for idx, func_pair in enumerate(funcs):
        print_pair(idx, func_pair)


def print_pair(idx, pair):
    print("--== Day ", str(idx + 1).zfill(2), " ==--", sep='')
    pair[0]()
    pair[1]()


# print_all()
print_latest()
