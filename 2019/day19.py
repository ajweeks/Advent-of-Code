import intcode


def get_input_str():
    return open("day19.in").readlines()[0]


def get_inputs(input_str):
    return [int(x) for x in input_str.split(',')]


x = 5
y = 5
w = 10
h = 10
points = [-1] * (w * h)
input_idx = 0
comp = intcode.Intcode()


def print_points():
    for yy in range(h):
        for xx in range(w):
            print('# ' if points[yy * w + xx] == 1 else '. ', end='')
        print()
    print()


def get_input():
    global input_idx, x, y, w, h, comp

    val = x if input_idx == 0 else y
    input_idx = (input_idx + 1) % 2

    return val


def on_output(val):
    global x, y, w, h, points
    points[y * w + x] = val

    x = (x + 1) % w
    if x == 0:
        y = (y + 1) % h
        if y == 0:
            comp.is_halted = True

    print_points()


def part1():
    global comp

    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 100000)

    while 1:
        comp.run(inputs, False, False, -1, get_input, on_output)
        comp = intcode.Intcode()


    lit_points = sum(points)

    return lit_points


def part2():
    pass
