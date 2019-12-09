import intcode


def get_input_str():
    return open("day09.in").readlines()[0]


def get_inputs(input_str):
    return [int(x) for x in input_str.split(',')]


def part1():
    inputs = get_inputs(get_input_str())
    # inputs = get_inputs("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    inputs.extend([0] * 1000)
    comp = intcode.Intcode()
    comp.receive_signal(1)
    return comp.run(inputs, False, True)


def part2():
    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 1000)
    comp = intcode.Intcode()
    comp.receive_signal(2)
    return comp.run(inputs, False, True)
