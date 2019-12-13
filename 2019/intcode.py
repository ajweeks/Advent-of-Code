
def decode_input(op):
    opcode = op % 100
    mode_bits = int(op / 100)
    modes = [0] * 8
    mode_idx = 0
    while mode_bits:
        if mode_bits % 10:
            modes[mode_idx] = mode_bits % 10
        mode_bits = int(mode_bits / 10)
        mode_idx += 1
    return opcode, modes


def retrieve(modes, inputs, inst_ptr, param_count, relative_base):
    values = []
    for i in range(param_count):
        if modes[i] == 0:  # Position
            values.append(inputs[inputs[inst_ptr + i]])
        elif modes[i] == 1:  # Immediate
            values.append(inputs[inst_ptr + i])
        elif modes[i] == 2:  # Relative
            values.append(inputs[relative_base + inputs[inst_ptr + i]])
        else:
            assert False
    return values


def retrieve_address(modes, inputs, inst_ptr, param_count, relative_base):
    values = []
    for i in range(param_count):
        if modes[i] == 0:  # Position
            values.append(inputs[inst_ptr + i])
        elif modes[i] == 1:  # Immediate
            values.append(inst_ptr + i)
        elif modes[i] == 2:  # Relative
            values.append(relative_base + inputs[inst_ptr + i])
        else:
            assert False
    return values


class Intcode:
    def __init__(self):
        self.signals = []
        self.outputs = []
        self.inst_ptr = 0
        self.complete = False
        self.relative_base = 0
        self.is_halted = False

    def receive_signal(self, signal):
        self.signals.append(signal)

    def run(self, inputs, print_halt_codes=True, return_halt_codes=False, yield_on_output_count=-1, get_input=None, on_output=None):
        while self.inst_ptr < len(inputs):
            opcode, modes = decode_input(inputs[self.inst_ptr])
            # print("opcode, modes:  ", opcode, ", ", modes, sep='')

            if opcode == 1:  # Add
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2, self.relative_base)
                [in2] = retrieve_address(modes[2:], inputs, self.inst_ptr + 3, 1, self.relative_base)
                inputs[in2] = in0 + in1
                self.inst_ptr += 4
            elif opcode == 2:  # Multiply
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2, self.relative_base)
                [in2] = retrieve_address(modes[2:], inputs, self.inst_ptr + 3, 1, self.relative_base)
                inputs[in2] = in0 * in1
                self.inst_ptr += 4
            elif opcode == 3:  # Load
                [in0] = retrieve_address(modes, inputs, self.inst_ptr + 1, 1, self.relative_base)
                if get_input is not None:
                    inputs[in0] = get_input()
                    self.inst_ptr += 2
                elif len(self.signals) > 0:
                    inputs[in0] = self.signals.pop(0)
                    self.inst_ptr += 2
                else:
                    assert len(self.outputs) > 0
                    return self.outputs.pop()  # Waiting on a signal
            elif opcode == 4:  # Store
                [in0] = retrieve(modes, inputs, self.inst_ptr + 1, 1, self.relative_base)
                if on_output is not None:
                    on_output(in0)
                    self.inst_ptr += 2
                else:
                    self.outputs.append(in0)
                    self.inst_ptr += 2
                    if len(self.outputs) == yield_on_output_count:
                        return self.outputs.pop(0)
            elif opcode == 5:  # jump if true
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2, self.relative_base)
                if in0:
                    self.inst_ptr = in1
                    if self.inst_ptr > len(inputs):
                        print("jumped out of program! (", self.inst_ptr, ")")
                else:
                    self.inst_ptr += 3
            elif opcode == 6:  # jump if false
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2, self.relative_base)
                if not in0:
                    self.inst_ptr = in1
                    if self.inst_ptr > len(inputs):
                        print("jumped out of program! (", self.inst_ptr, ")")
                else:
                    self.inst_ptr += 3
            elif opcode == 7:  # less than
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2, self.relative_base)
                [in2] = retrieve_address(modes[2:], inputs, self.inst_ptr + 3, 1, self.relative_base)
                inputs[in2] = 1 if (in0 < in1) else 0
                self.inst_ptr += 4
            elif opcode == 8:  # equals
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2, self.relative_base)
                [in2] = retrieve_address(modes[2:], inputs, self.inst_ptr + 3, 1, self.relative_base)
                inputs[in2] = 1 if (in0 == in1) else 0
                self.inst_ptr += 4
            elif opcode == 9:  # adjust relative base
                [in0] = retrieve(modes, inputs, self.inst_ptr + 1, 1, self.relative_base)
                self.relative_base += in0
                self.inst_ptr += 2
            else:
                if inputs[self.inst_ptr] == 99:
                    self.is_halted = True
                    if print_halt_codes:
                        print(self.outputs)
                else:
                    print("Unhandled opcode: ", opcode)
                break
        self.complete = True
        return self.outputs[-1] if return_halt_codes else inputs[0]
