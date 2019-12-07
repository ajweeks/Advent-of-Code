
import intcode


def get_inputs():
    return [int(x) for x in open("day02.in").readlines()[0].split(',')]


def part1():
    inputs = get_inputs()
    inputs[1] = 12
    inputs[2] = 2
    comp = intcode.Intcode()
    comp.receive_signal(1)
    result = comp.run(inputs, False, False)
    return result


def part2():
    result = -1
    initial_inputs = get_inputs()
    for n in range(100):
        for v in range(100):
            inputs = initial_inputs.copy()
            inputs[1] = n
            inputs[2] = v
            comp = intcode.Intcode()
            comp.receive_signal(1)
            if comp.run(inputs, False, False) == 19690720:
                result = 100 * n + v
                break

            if result != -1:
                break
        if result != -1:
            break
    return result
