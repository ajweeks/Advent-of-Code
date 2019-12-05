
def decode_input(op):
    opcode = op % 100
    mode_bits = int(op / 100)
    modes = [0] * 3
    mode_idx = 0
    while mode_bits:
        if mode_bits % 10:
            modes[mode_idx] = 1
        mode_bits = int(mode_bits / 10)
        mode_idx += 1
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


def run(inputs, register0_start, print_halt_codes=True):
    inst_ptr = 0
    register0 = register0_start
    while inst_ptr < len(inputs):
        opcode, modes = decode_input(inputs[inst_ptr])
        # print("opcode, modes:  ", opcode, ", ", modes, sep='')

        if opcode == 1:  # Add
            [in0, in1] = retrieve(modes, inputs, inst_ptr + 1, 2)
            inputs[inputs[inst_ptr + 3]] = in0 + in1
            inst_ptr += 4
        elif opcode == 2:  # Multiply
            [in0, in1] = retrieve(modes, inputs, inst_ptr + 1, 2)
            inputs[inputs[inst_ptr + 3]] = in0 * in1
            inst_ptr += 4
        elif opcode == 3:  # Load
            inputs[inputs[inst_ptr + 1]] = register0
            assert (modes[0] == modes[1] == 0)
            # print("load:", register0)
            inst_ptr += 2
        elif opcode == 4:  # Store
            [in0] = retrieve(modes, inputs, inst_ptr + 1, 1)
            register0 = in0
            # print("store:", register0)
            inst_ptr += 2
        elif opcode == 5:  # jump if true
            [in0, in1] = retrieve(modes, inputs, inst_ptr + 1, 2)
            if in0:
                inst_ptr = in1
                if inst_ptr > len(inputs):
                    print("jumped out of program! (", inst_ptr, ")")
            else:
                inst_ptr += 3
        elif opcode == 6:  # jump if false
            [in0, in1] = retrieve(modes, inputs, inst_ptr + 1, 2)
            if not in0:
                inst_ptr = in1
                if inst_ptr > len(inputs):
                    print("jumped out of program! (", inst_ptr, ")")
            else:
                inst_ptr += 3
        elif opcode == 7:  # less than
            [in0, in1] = retrieve(modes, inputs, inst_ptr + 1, 2)
            inputs[inputs[inst_ptr + 3]] = 1 if (in0 < in1) else 0
            inst_ptr += 4
        elif opcode == 8:  # equals
            [in0, in1] = retrieve(modes, inputs, inst_ptr + 1, 2)
            inputs[inputs[inst_ptr + 3]] = 1 if (in0 == in1) else 0
            inst_ptr += 4
        else:
            if inputs[inst_ptr] == 99:
                if print_halt_codes:
                    print(register0)
            else:
                print("Unhandled opcode: ", opcode)
            break
    return inputs[0]
