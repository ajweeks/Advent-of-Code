import intcode


def get_input_str():
    return open("day18.in").readlines()


def get_inputs(input_str):
    return [1 if x == '#' else 2 if x == '@' else 0 if x == '.' else x for line in input_str for x in line.strip()]


movements = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def idx(x, y, w):
    return y * w + x


def print_board(w, h, board):
    for yy in range(h):
        for xx in range(w):
            v = board[yy * w + xx]
            print(".#@"[v] if type(v) == int else v, end='')
        print()
    print()


def find_visible_keys(pos, w, h, board):
    keys = []
    for move in movements:
        p = (pos[0] + move[0], pos[1] + move[1])
        if 0 <= p[0] < w and 0 <= p[1] < h:
            v = board[idx(p[0], p[1], w)]
            if v == 0:
                keys.extend(find_visible_keys(p, w, h, board))
            elif type(v) == str:
                if ord('a') <= ord(v) <= ord('z'):  # Key
                    keys.extend((p, v))
                    # TODO
                    # keys.extend(find_visible_keys(p, w, h, board))
                else:  # Door
                    pass
    return keys


def move_to(cur_pos, new_pos, w, h, board):
    steps = 0

    return steps, new_pos


def part1():
    input_str = get_input_str()
    input_str = """#########
#b.A.@.a#
#########""".splitlines()
    w = len(input_str[0].strip())
    h = len(input_str)
    inputs = get_inputs(input_str)
    pos = (inputs.index(2) % w, inputs.index(2) // w)

    print_board(w, h, inputs)

    visible_keys = find_visible_keys(pos, w, h, inputs)
    print(visible_keys)

    steps = 0
    while len(visible_keys) > 0:
        new_steps, pos = move_to(pos, visible_keys[0][0], w, h, inputs)
        steps += new_steps
        inputs = [0 if x == visible_keys[1] else x for x in inputs]  # Pick up the key
        inputs = [0 if x == visible_keys[1].upper() else x for x in inputs]  # Open the door
        visible_keys.remove(visible_keys[0])

        print_board(w, h, inputs)

    return 0


def part2():
    pass
