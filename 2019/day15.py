import intcode


def get_input_str():
    return open("day15.in").readlines()[0]


def get_inputs(input_str):
    return [int(x) for x in input_str.split(',')]


area_size = 42
area = [(-1, -1)] * (area_size * area_size)  # (type = -1=unknown, 0=empty, 1=wall, 2=oxygen system, 3=oxygenated empty, distance from start)
starting_pos = (area_size // 2, area_size // 2)
pos = starting_pos
move_request = 0  # 1=N, 2=S, 3=W, 4=E
oxygen_dist = -1
oxygen_pos = (-1, -1)
movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]
trail = []
comp = intcode.Intcode()


def print_area(print_distances=False):
    global area, area_size, pos

    for y in range(area_size):
        if sum(area[y * area_size:(y+1) * area_size][0]) == -area_size:
            print()
        else:
            for x in range(area_size):
                typ = area[idx((x, y))][0]
                dst = area[idx((x, y))][1]
                if print_distances:
                    print('D' if (x, y) == pos else 'X' if (x, y) == starting_pos else ' ' if dst == -1 else dst % 10, end='')
                else:
                    print('D' if (x, y) == pos else 'X' if (x, y) == starting_pos else ' ' if typ == -1 else '.' if typ == 0 else '#' if typ == 1 else 'O', end='')
            print()
    print('#' * area_size)


def add(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1])


def sub(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1])


def idx(pos):
    return pos[1] * area_size + pos[0]


def dist(pos):
    return abs(pos[0]) + abs(pos[1])


def reverse(dir):
    return [2, 1, 4, 3][dir - 1]


def get_input():
    global area, pos, movements, move_request, trail
    neighbors = [area[idx(add(pos, movements[i]))][0] for i in range(4)]
    for i, n in enumerate(neighbors):
        if n == -1:
            move_request = i + 1
            return move_request

    if len(trail) > 0:
        move_request = reverse(trail.pop()[1])
        return move_request

    assert False


def on_output(val):
    global area, area_size, pos, oxygen_dist, oxygen_pos, trail, comp

    moved = (val == 1 or val == 2)

    if moved:
        pos = add(pos, movements[move_request - 1])

    dist = area[idx(pos)][1]
    neighbors = [area[idx(add(pos, movements[i]))] for i in range(4)]
    l = [n[1] for n in neighbors if n[0] != -1 and n[0] != 1]
    closest_neighbor_dist = min(l or [-1])
    if moved:
        if closest_neighbor_dist != -1:
            dist = closest_neighbor_dist + 1
        else:
            dist = area[idx(pos)][1] + 1

    if val == 0:  # wall
        wall_pos = add(pos, movements[move_request - 1])
        area[idx(wall_pos)] = (1, -1)
    elif val == 1:  # moved
        area[idx(pos)] = (0, dist)
        if len(trail) == 0 and pos == starting_pos:
            comp.is_halted = True
    elif val == 2:  # oxygen system
        oxygen_pos = pos
        area[idx(oxygen_pos)] = (2, dist)
        oxygen_dist = dist
    else:
        assert False

    if moved:
        if len(trail) == 0 or pos != trail[-1][0]:
            trail.append((pos, move_request))

    # print_area(True)


def floodfill():
    area[idx(pos)] = (3, area[idx(pos)][1])

    iter_count = 0
    positions_remaining = [add(oxygen_pos, movements[i]) for i in range(4)]
    positions_remaining = [p for p in positions_remaining if area[idx(p)][0] == 0]

    while len(positions_remaining) > 0:
        new_positions_remaining = []
        for p in positions_remaining:
            area[idx(p)] = (3, area[idx(p)][1])
            for i, n in enumerate([area[idx(add(p, movements[i]))] for i in range(4)]):
                if n[0] == 0:
                    new_positions_remaining.append(add(p, movements[i]))
        positions_remaining = new_positions_remaining.copy()
        iter_count += 1

    return iter_count


def part1():
    global oxygen_dist

    inputs = get_inputs(get_input_str())
    inputs.extend([0] * 10000)
    area[idx(starting_pos)] = (0, 0)

    comp.run(inputs, True, False, -1, get_input, on_output)

    # print_area()

    return oxygen_dist


def part2():
    iter_count = floodfill()
    return iter_count
