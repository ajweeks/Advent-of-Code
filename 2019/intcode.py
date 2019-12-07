
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


class Intcode:
    def __init__(self):
        self.signals = []
        self.outputs = []
        self.inst_ptr = 0
        self.complete = False

    def receive_signal(self, signal):
        self.signals.append(signal)

    def is_complete(self):
        return self.complete

    def run(self, inputs, print_halt_codes=True, return_halt_codes=False):
        while self.inst_ptr < len(inputs):
            opcode, modes = decode_input(inputs[self.inst_ptr])
            # print("opcode, modes:  ", opcode, ", ", modes, sep='')

            if opcode == 1:  # Add
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2)
                inputs[inputs[self.inst_ptr + 3]] = in0 + in1
                self.inst_ptr += 4
            elif opcode == 2:  # Multiply
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2)
                inputs[inputs[self.inst_ptr + 3]] = in0 * in1
                self.inst_ptr += 4
            elif opcode == 3:  # Load
                if len(self.signals) > 0:
                    inputs[inputs[self.inst_ptr + 1]] = self.signals.pop(0)
                    assert (modes[0] == modes[1] == 0)
                    self.inst_ptr += 2
                else:
                    assert len(self.outputs) > 0
                    return self.outputs.pop()  # Waiting on a signal
            elif opcode == 4:  # Store
                [in0] = retrieve(modes, inputs, self.inst_ptr + 1, 1)
                self.outputs.append(in0)
                self.inst_ptr += 2
            elif opcode == 5:  # jump if true
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2)
                if in0:
                    self.inst_ptr = in1
                    if self.inst_ptr > len(inputs):
                        print("jumped out of program! (", self.inst_ptr, ")")
                else:
                    self.inst_ptr += 3
            elif opcode == 6:  # jump if false
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2)
                if not in0:
                    self.inst_ptr = in1
                    if self.inst_ptr > len(inputs):
                        print("jumped out of program! (", self.inst_ptr, ")")
                else:
                    self.inst_ptr += 3
            elif opcode == 7:  # less than
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2)
                inputs[inputs[self.inst_ptr + 3]] = 1 if (in0 < in1) else 0
                self.inst_ptr += 4
            elif opcode == 8:  # equals
                [in0, in1] = retrieve(modes, inputs, self.inst_ptr + 1, 2)
                inputs[inputs[self.inst_ptr + 3]] = 1 if (in0 == in1) else 0
                self.inst_ptr += 4
            else:
                if inputs[self.inst_ptr] == 99:
                    if print_halt_codes:
                        print(self.outputs)
                else:
                    print("Unhandled opcode: ", opcode)
                break
        self.complete = True
        return self.outputs[-1] if return_halt_codes else inputs[0]
