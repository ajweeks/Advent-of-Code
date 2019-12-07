
import intcode


def get_inputs():
    return [int(y) for y in open("day05.in").readlines()[0].split(',')]


def part1():
    inputs = get_inputs()
    # inputs = list(map(lambda x: int(x), "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")))
    comp = intcode.Intcode()
    comp.receive_signal(1)
    return comp.run(inputs, False, True)


def part2():
    inputs = get_inputs()
    comp = intcode.Intcode()
    comp.receive_signal(5)
    return comp.run(inputs, False, True)
