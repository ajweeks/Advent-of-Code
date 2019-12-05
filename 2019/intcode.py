
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
    register0 = 1
    while i < len(inputs):
        opcode, modes = decode_input(inputs[i])

        if opcode == 1:  # Add
            [in0, in1] = retrieve(modes, inputs, i + 1, 2)
            inputs[inputs[i + 3]] = in0 + in1
            i += 4
        elif opcode == 2:  # Multiply
            [in0, in1] = retrieve(modes, inputs, i + 1, 2)
            inputs[inputs[i + 3]] = in0 * in1
            i += 4
        elif opcode == 3:  # Load
            inputs[inputs[i + 1]] = register0
            print("load:", register0)
            i += 2
        elif opcode == 4:  # Store
            register0 = inputs[inputs[i + 1]]
            print("store:", register0)
            i += 2
        else:
            if inputs[i] == 99:
                print("halted with output:", register0)
            else:
                print("Unhandled opcode: ", opcode)
            break
    return inputs[0]
