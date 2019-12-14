import intcode


def get_input_str():
    return open("day13.in").readlines()[0]


def get_inputs(input_str):
    return list(map(int, input_str.split(',')))


def print_board():
    global tiles, w, h, score
    t_lookup = [' ', 'W', 'B', 'H', 'O']
    for yy in range(h):
        for xx in range(w):
            t = tiles[yy*w+xx]
            print(t_lookup[t], end='')
        print()
    print("score:", score, "paddle:", paddle_pos_x, paddle_pos_y, "ball:", ball_pos[0], ball_pos[1], "ball v:", ball_vel[0], ball_vel[1])
    print()


def part1():
    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 10000)
    comp = intcode.Intcode()
    w = 64
    tiles = [0] * (w * h)
    while 1:
        out = comp.run(inputs, False, False, 3)
        if comp.is_halted:
            break
        x = out
        y = comp.outputs.pop(0)
        type = comp.outputs.pop(0)
        tiles[y*w+x] = type

    # print_board(tiles, w)

    block_count = tiles.count(2)
    return block_count


out_idx = 0
x = 0
y = 0
w = 42
h = 25
tiles = [0] * (w * h)
score = 0
ball_pos = (0, 0)
ball_vel = (0, 0)
paddle_pos_x = 0
paddle_pos_y = 0


def sub(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1])


def part2():
    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 10000)
    comp = intcode.Intcode()

    def on_output(val):
        global out_idx, x, y, tiles, score, ball_pos, ball_vel, paddle_pos_x, paddle_pos_y

        if out_idx == 0:
            x = val
        elif out_idx == 1:
            y = val
        elif out_idx == 2:
            if x == -1 and y == 0:
                score = val
            else:
                tiles[y * w + x] = val
                if val == 4:
                    ball_vel = sub(ball_pos, (x, y))
                    ball_pos = (x, y)
                elif val == 3:
                    paddle_pos_x = x
                    paddle_pos_y = y

                if (val == 4) and paddle_pos_x != 0:
                    pass
                    # print_board()

        out_idx = (out_idx + 1) % 3

    def get_input():
        global paddle_pos_y
        b_next_pos = (ball_pos[0] + ball_vel[0] * (paddle_pos_y - ball_pos[1] - 1))
        input = 1 if (b_next_pos > paddle_pos_x) else -1 if (b_next_pos < paddle_pos_x) else 0
        return input

    while 1:
        inputs[0] = 2
        comp.run(inputs, False, False, -1, get_input, on_output)
        if comp.is_halted:
            break

    # print_board()

    return score