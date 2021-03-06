
import day01, day02, day03, day04, day05, day06, day07, day08, day09, day10, day11, day12, day13, day14, day15, day16
import day17, day18, day19, day20
import logging

pairs = [
    (day01.part1, day01.part2, 3336985, 5002611),
    (day02.part1, day02.part2, 5434663, 4559),
    (day03.part1, day03.part2, 403, 4158),
    (day04.part1, day04.part2, 945, 617),
    (day05.part1, day05.part2, 16574641, 15163975),
    (day06.part1, day06.part2, 144909, 259),
    (day07.part1, day07.part2, 17790, 19384820),
    (day08.part1, day08.part2, 2032, "CFCUG"),
    (day09.part1, day09.part2, 3906448201, 59785),
    (day10.part1, day10.part2, 329, 512),
    (day11.part1, day11.part2, 2373, "PCKRLPUK"),
    (day12.part1, day12.part2, 7687, 334945516288044),
    (day13.part1, day13.part2, 427, 21426),
    (day14.part1, day14.part2, 337862, 3687786),
    (day15.part1, day15.part2, 236, 368),
    (day16.part1, day16.part2, 32002835, 69732268),
    (day17.part1, day17.part2, 3192, 684691),
    (day18.part1, day18.part2),
    (day19.part1, day19.part2),
    (day20.part1, day20.part2),
]


def run_latest():
    run_pair(len(pairs) - 1, pairs[-1])


def run_all():
    regression = False
    for idx, func_pair in enumerate(pairs):
        if not run_pair(idx, func_pair):
            regression = True
    if not regression:
        print("\nAll successful!")


def run_pair(idx, pair):
    print("--== Day ", str(idx + 1).zfill(2), " ==--", sep='')
    success = True
    r0 = pair[0]()
    if len(pair) > 2 and r0 != pair[2]:
        logging.error(" Regression! Expected " + pair[2] + ", Got: " + r0)
        success = False
    else:
        print(r0)

    r1 = pair[1]()
    if len(pair) > 2 and r1 != pair[3]:
        logging.error(" Regression! Expected " + pair[3] + ", Got: " + r1)
        success = False
    else:
        print(r1)

    return success


# run_all()
run_latest()
