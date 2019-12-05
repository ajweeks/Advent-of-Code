
import intcode


def get_inputs():
    return [int(x) for x in open("day02.in").readlines()[0].split(',')]


def part1():
    inputs = get_inputs()
    inputs[1] = 12
    inputs[2] = 2
    print(intcode.run(inputs))


def part2():
    result = -1
    initial_inputs = get_inputs()
    for n in range(100):
        for v in range(100):
            inputs = initial_inputs.copy()
            inputs[1] = n
            inputs[2] = v
            if intcode.run(inputs) == 19690720:
                result = 100 * n + v
                print(result)
                break

            if result != -1:
                break
        if result != -1:
            break
