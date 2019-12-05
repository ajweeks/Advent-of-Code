
import intcode


def get_inputs():
    return [int(y) for y in open("day05.in").readlines()[0].split(',')]


def part1():
    intcode.run(get_inputs())


def part2():
    pass
