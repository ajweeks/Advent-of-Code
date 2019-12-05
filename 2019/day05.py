
import intcode


def get_inputs():
    return [int(y) for y in open("day05.in").readlines()[0].split(',')]


def part1():
    # inputs = list(map(lambda x: int(x), "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")))
    # intcode.run(inputs, 1000)
    intcode.run(get_inputs(), 1)


def part2():
    intcode.run(get_inputs(), 5)
