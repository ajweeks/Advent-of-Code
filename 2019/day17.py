import intcode


def get_input_str():
    return open("day17.in").readlines()[0]


def get_inputs(input_str):
    return [int(x) for x in input_str.split(',')]


SCAFFOLD = 35
EMPTY = 46
NEW_LINE = 10

w = 38
h = 32
scaffolding = [0] * (w * h)
intersections = []
output_idx = 0
alignment_params = 0
comp = intcode.Intcode()


def print_scaffolding():
    for yy in range(h):
        for xx in range(w):
            val = scaffolding[idx(xx, yy)]
            if (xx, yy) in intersections:
                val = ord('O')
            print(' ', chr(val), sep='', end='')
    print()
    print("|" * 38)
    print()


def idx(x, y):
    global w, h
    return y * w + x


def count_alignment_params():
    sum = 0
    for i in intersections:
        sum += (i[0] * i[1])
    return sum


def count_intersections():
    global scaffolding, w, h, intersections
    for yy in range(1, h - 1):
        for xx in range(1, w - 1):
            if scaffolding[idx(xx, yy)] == SCAFFOLD:
                if scaffolding[idx(xx + 1, yy)] == SCAFFOLD and \
                        scaffolding[idx(xx - 1, yy)] == SCAFFOLD and \
                        scaffolding[idx(xx, yy + 1)] == SCAFFOLD and \
                        scaffolding[idx(xx, yy - 1)] == SCAFFOLD:
                    intersections.append((xx, yy))
    return intersections


def get_input1():
    return 0


def on_output1(val):
    global output_idx, scaffolding, alignment_params, comp

    scaffolding[output_idx] = val
    output_idx += 1

    if output_idx == (w * h):
        count_intersections()
        output_idx = 0
        # print_scaffolding()
        alignment_params = count_alignment_params()
        comp.is_halted = True


def part1():
    instr = get_inputs(get_input_str())
    instr.extend([0] * 10000)
    comp.run(instr, True, False, True, get_input1, on_output1)
    return alignment_params


def get_input2():
    return 0


def on_output2(val):
    global output_idx, scaffolding, alignment_params, comp

    scaffolding[output_idx] = val
    output_idx += 1

    if output_idx == (w * h):
        count_intersections()
        output_idx = 0
        # print_scaffolding()
        alignment_params = count_alignment_params()
        comp.is_halted = True


def part2():
    global comp

    instr = get_inputs(get_input_str())
    instr.extend([0] * 10000)
    instr[0] = 2
    comp = intcode.Intcode()
    comp.run(instr, True, False, True, get_input2, on_output2)
    return 99
