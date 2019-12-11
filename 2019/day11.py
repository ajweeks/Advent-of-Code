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


def part1():
    comp = intcode.Intcode()
    inputs = get_inputs(get_input_str())

    facing = 0  # 0 = up, 1 = right, 1 = down, 3 = left
    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    panel_dim = 10000
    comp_pos = (panel_dim // 2, panel_dim // 2)
    panels = [0] * (panel_dim * panel_dim)

    # print_board(panels, panel_dim, comp_pos, facing)

    painted_panel_count = 0
    while 1:
        print(comp_pos[1] * panel_dim + comp_pos[0])
        comp.receive_signal(panels[comp_pos[1] * panel_dim + comp_pos[0]])
        out = comp.run(inputs, True, False, True)
        assert(len(comp.signals) == 0)

        if comp.is_halted:
            break
        painted_panel_count += 1
        panels[comp_pos[1] * panel_dim + comp_pos[0]] = out
        turn = comp.outputs.pop(0)
        assert(len(comp.outputs) == 0)
        if turn == 0:
            facing = (facing - 1) % 4
        else:
            facing = (facing + 1) % 4
        comp_pos = (comp_pos[0] + moves[facing][0], comp_pos[1] + moves[facing][1])

        # print_board(panels, panel_dim, comp_pos, facing)
        comp.signals = []

    return painted_panel_count


def part2():
    inputs = get_inputs(get_input_str())
    pass