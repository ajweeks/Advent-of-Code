import intcode


def get_input_str():
    return open("day11.in").readlines()[0]


def get_inputs(input_str):
    return list(map(int, input_str.split(',')))


def print_board(panels, w, pos, facing):
    comp = ['^', '>', 'v', '<'][facing]
    for i in range(len(panels)//w):
        for j in range(w):
            print(comp if (j, i) == pos else '#' if panels[i * w + j] else '.', end='')
        print()
    print()


def do_paint(starting_paint_colour, print_final_board=False):
    comp = intcode.Intcode()
    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 10000)

    facing = 0  # 0 = up, 1 = right, 1 = down, 3 = left
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    panel_dim = 256
    comp_pos = (panel_dim // 2, panel_dim // 2)
    panels = [0] * (panel_dim * panel_dim)
    panels[comp_pos[1] * panel_dim + comp_pos[0]] = starting_paint_colour
    painted = [True if x == 1 else False for x in panels]

    painted_panel_count = 0
    while 1:
        pos_idx = comp_pos[1] * panel_dim + comp_pos[0]
        comp.receive_signal(panels[pos_idx])
        paint = comp.run(inputs, False, False, 2)

        if comp.is_halted:
            break

        if not painted[pos_idx]:
            painted_panel_count += 1
            painted[pos_idx] = True

        panels[pos_idx] = paint
        turn = comp.outputs.pop(0)
        assert(len(comp.outputs) == 0)
        if turn == 0:
            facing = (facing - 1) % 4
        else:
            facing = (facing + 1) % 4
        comp_pos = (comp_pos[0] + moves[facing][0], comp_pos[1] + moves[facing][1])

        # print_board(panels, panel_dim, comp_pos, facing)
        comp.signals = []

    if print_final_board:
        print_board(panels, panel_dim, comp_pos, facing)

    return painted_panel_count


def part1():
    painted_panel_count = do_paint(0)
    return painted_panel_count


def part2():
    painted_panel_count = do_paint(1, False)
    return "PCKRLPUK"
