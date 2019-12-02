
def get_inputs():
    return [int(x) for x in open("day2.in").readlines()[0].split(',')]


def part1():
    inputs = get_inputs()
    inputs[1] = 12
    inputs[2] = 2
    i = 0
    while i < len(inputs):
        if inputs[i] == 1:  # Add
            inputs[inputs[i + 3]] = inputs[inputs[i + 1]] + inputs[inputs[i + 2]]
        elif inputs[i] == 2:  # Mult
            inputs[inputs[i + 3]] = inputs[inputs[i + 1]] * inputs[inputs[i + 2]]
        else:
            if inputs[i] != 99:
                print("Unhandled opcode: ", inputs[i])
            break
        i += 4
    print(inputs[0])


def part2():
    # inputs = [1,9,10,3,2,3,11,0,99,30,40,50]
    result = -1
    initial_inputs = get_inputs()
    for n in range(100):
        for v in range(100):
            i = 0
            inputs = initial_inputs.copy()
            inputs[1] = n
            inputs[2] = v
            while i < len(inputs):
                if inputs[i] == 1:  # Add
                    inputs[inputs[i + 3]] = inputs[inputs[i + 1]] + inputs[inputs[i + 2]]
                elif inputs[i] == 2:  # Mult
                    inputs[inputs[i + 3]] = inputs[inputs[i + 1]] * inputs[inputs[i + 2]]
                else:
                    if inputs[i] != 99:
                        print("Unhandled opcode: ", inputs[i])

                    # print("Halted on: ", inputs[0], inputs)

                    if inputs[0] == 19690720:
                        result = 100 * n + v
                        print(result)

                    break
                i += 4

            if result != -1:
                break
        if result != -1:
            break
