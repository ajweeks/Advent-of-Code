import intcode


def get_input_str():
    return open("day19.in").readlines()[0]


def get_inputs(input_str):
    return [int(x) for x in input_str.split(',')]


x = 5
y = 5
w = 50
h = 50
points = [-1] * (w * h)
input_idx = 0
comp = intcode.Intcode()


def print_points():
    for yy in range(h):
        for xx in range(w):
            print('# ' if points[yy * w + xx] == 1 else '. ', end='')
        print()
    print()


def point_lit(xx, yy):
    global comp

    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 100000)

    comp = intcode.Intcode()

    comp.receive_signal(xx)
    comp.receive_signal(yy)
    return comp.run(inputs.copy(), False, True)


def part1():
    global comp

    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 100000)

    for yy in range(h):
        for xx in range(w):
            points[yy * w + xx] = point_lit(xx,yy)

    # print_points()

    lit_points = sum(points)
    return lit_points


def part2():
    if points[-1] == -1:
        part1()  # Initialize points

    xx = yy = 0
    while point_lit(xx + 99, yy) == 0:
        yy += 1
        if point_lit(xx, yy + 99) == 0:
            xx += 1

    return xx * 10000 + yy
