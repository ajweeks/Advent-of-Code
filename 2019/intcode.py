
def decode_input(op):
    opcode = op % 100
    mode_bits = int(op / 100)
    modes = [0] * 3
    mode_idx = 0
    while mode_bits:
        if mode_bits % 10:
            modes[mode_idx] = 1
        mode_bits = int(mode_bits / 10)
    return opcode, modes


def retrieve(modes, inputs, inst_ptr, param_count):
    values = []
    for i in range(param_count):
        if modes[i] == 0:  # Position
            values.append(inputs[inputs[inst_ptr + i]])
        elif modes[i] == 1:  # Immediate:
            values.append(inputs[inst_ptr + i])
        else:
            assert False
    return values


def run(inputs):
    i = 0
    input = 1
    output = 0
    while i < len(inputs):
        opcode, modes = decode_input(inputs[i])

        if opcode == 1:  # Add
            inputs[inputs[i + 3]] = inputs[inputs[i + 1]] + inputs[inputs[i + 2]]
            i += 4
        elif opcode == 2:  # Multiply
            [in0, in1] = retrieve(modes, inputs, i + 1, 2)
            inputs[inputs[i + 3]] = in0 * in1
            i += 4
        elif opcode == 3:  # Store
            output = inputs[inputs[i + 1]]
            print("store:", output)
            i += 2
        elif opcode == 4:  # Load
            inputs[inputs[i + 1]] = input
            i += 2
        else:
            if inputs[i] == 99:
                print("output:", output)
            else:
                print("Unhandled opcode: ", opcode)
            break
    return inputs[0]
