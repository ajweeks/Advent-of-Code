
from timeit import default_timer as timer

# TODO:
# [x] Input parsing
# [x] Turn ordering
# [x] Find potential targets
# [x] Find distances to targets
# [x] Move to closest target if not in range
# [x] Kill weakest target in range
# [x] Remove dead targets from list

initial_map = [a.strip() for a in open("day15.in").readlines()]

# Part 1 tests:
# # 27730
# initial_map = """#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######""".splitlines()
#
# # 36334
# initial_map = """#######
# #G..#E#
# #E#E.E#
# #G.##.#
# #...#E#
# #...E.#
# #######""".splitlines()
#
# # 39514
# initial_map = """#######
# #E..EG#
# #.#G.E#
# #E.##E#
# #G..#.#
# #..E#.#
# #######""".splitlines()
#
# # 28944
# initial_map = """#######
# #E.G#.#
# #.#G..#
# #G.#.G#
# #G..#.#
# #...E.#
# #######""".splitlines()
#
# # 27755
# initial_map = """#######
# #.E...#
# #.#..G#
# #.###.#
# #E#G#G#
# #...#G#
# #######""".splitlines()

# Part 2 tests:
# # 4988, 15 dmg
# initial_map = """#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######""".splitlines()
# # 31284, 4 dmg
# initial_map = """#######
# #E..EG#
# #.#G.E#
# #E.##E#
# #G..#.#
# #..E#.#
# #######""".splitlines()
# # 3478, 15 dmg
# initial_map = """#######
# #E.G#.#
# #.#G..#
# #G.#.G#
# #G..#.#
# #...E.#
# #######""".splitlines()

part1 = True

cells = []
units = []

w, h, = len(initial_map[0]), len(initial_map)


def init():
    global cells
    global units

    cells = []
    units = []
    for yy in range(len(initial_map)):
        line = initial_map[yy]
        for xx in range(len(line)):
            c = line[xx]
            if c == '.':
                cells.append(0)
            elif c == '#':
                cells.append(1)
            elif c == 'E' or c == 'G':
                cells.append(0)
                units.append([0 if c == 'E' else 1, xx, yy, 200])


def print_board():
    for y in range(h):
        units_in_row = []
        for x in range(w):
            unit_test = unit_at(x, y)
            if unit_test:
                print('E' if unit_test[0] == 0 else 'G', end='')
                units_in_row.append(unit_test)
            else:
                cell = cells[y * w + x]
                print('.' if cell == 0 else '#', end='')
        print("  ", end='')
        for unit_in_row in units_in_row:
            print(('E' if unit_in_row[0] == 0 else 'G') + f'({unit_in_row[3]}), ', end='')
        print()
    print()


def print_dist_map(d_map):
    for y in range(h):
        for x in range(w):
            if d_map[y * w + x] == 0:
                print('T', end='')
            elif d_map[y * w + x] == -1:
                print('#', end='')
            else:
                print(d_map[y * w + x]%10, end='')
        print()
    print()


def available_spaces(unit):
    ux = unit[1]
    uy = unit[2]
    a = []
    if cells[(uy - 1) * w + ux] == 0:  # Top
        a.append((uy - 1) * w + ux)
    if cells[uy * w + ux - 1] == 0:    # Left
        a.append(uy * w + ux - 1)
    if cells[uy * w + ux + 1] == 0:    # Right
        a.append(uy * w + ux + 1)
    if cells[(uy + 1) * w + ux] == 0:  # Bottom
        a.append((uy + 1) * w + ux)
    return a


def unit_at(x, y):
    for unit in units:
        if unit[1] == x and unit[2] == y:
            return unit
    return None


def dist_map_recursive(d_map, target_x, target_y, xx, yy, i, shortest_path_dist):
    if xx == target_x and yy == target_y:
        d_map[yy * w + xx] = i + 1
        shortest_path_dist = i + 1
        return shortest_path_dist
    if cells[yy * w + xx] != 0 or (d_map[yy * w + xx] != -1 and d_map[yy * w + xx] <= i):
        return shortest_path_dist
    if i != 0 and unit_at(xx, yy):
        return shortest_path_dist
    d_map[yy * w + xx] = i
    i += 1
    if shortest_path_dist != -1 and i >= shortest_path_dist:
        return shortest_path_dist

    shortest_path_dist = dist_map_recursive(d_map, target_x, target_y, xx + 1, yy, i, shortest_path_dist)
    shortest_path_dist = dist_map_recursive(d_map, target_x, target_y, xx - 1, yy, i, shortest_path_dist)
    shortest_path_dist = dist_map_recursive(d_map, target_x, target_y, xx, yy + 1, i, shortest_path_dist)
    shortest_path_dist = dist_map_recursive(d_map, target_x, target_y, xx, yy - 1, i, shortest_path_dist)

    return shortest_path_dist


def move_in_dir(x, y, dir):
    if dir == 0:
        return x, (y - 1)
    if dir == 1:
        return x - 1, y
    if dir == 2:
        return x + 1, y
    if dir == 3:
        return x, (y + 1)
    assert False


init()

start = timer()

elf_damage = 3 if part1 else 22
elf_died = True
while elf_died:
    elf_died = False
    full_rounds = 0
    targets_remain = True
    action = False
    while targets_remain:
        action = False
        print(f"rounds complete: {full_rounds}, units remaining: {len(units)}, elf damage: {elf_damage}")
        print_board()
        units = sorted(units, key=lambda x: x[2] * w + x[1])

        ui = 0
        while ui < len(units):
            u = units[ui]
            potential_targets = []
            for u2 in units:
                if u2[0] != u[0]:
                    potential_targets.append(u2)

            if len(potential_targets) == 0:
                print("no targets remain!")
                targets_remain = False
                break

            targets_in_range = []
            for i in [[0, -1], [-1, 0], [1, 0], [0, 1]]:
                unit = unit_at(u[1] + i[0], u[2] + i[1])
                if unit and unit[0] != u[0]:
                    targets_in_range.append(unit)

            if len(targets_in_range) == 0:  # If no targets are in range, find closest target to move towards
                dist_map_pairs = []
                for t in potential_targets:
                    dist_map = [-1] * (w * h)
                    shortest_path_dist = dist_map_recursive(dist_map, u[1], u[2], t[1], t[2], 0, -1)
                    # print_dist_map(dist_map)

                    dist_map_pairs.append([t, dist_map])

                closest_dist_pair = []
                closest_dist = 9999
                for dist_map_pair in dist_map_pairs:
                    dist = dist_map_pair[1][u[2] * w + u[1]]
                    if dist != -1 and dist < closest_dist:
                        closest_dist = dist
                        closest_dist_pair = dist_map_pair

                if closest_dist != 9999:
                    dir_to_move = -1
                    smallest_d = closest_dist_pair[1][u[2] * w + u[1]]
                    direc = 0
                    for i in [[0, -1], [-1, 0], [1, 0], [0, 1]]:
                        d = closest_dist_pair[1][(u[2] + i[1]) * w + (u[1] + i[0])]
                        if d != -1 and d < smallest_d:
                            smallest_d = d
                            dir_to_move = direc
                        direc += 1

                    assert dir_to_move != -1

                    u[1], u[2] = move_in_dir(u[1], u[2], dir_to_move)
                    action = True

                    for i in [[0, -1], [-1, 0], [1, 0], [0, 1]]:
                        unit = unit_at(u[1] + i[0], u[2] + i[1])
                        if unit and unit[0] != u[0]:
                            targets_in_range.append(unit)

            unit_killed = -1
            if len(targets_in_range) != 0:
                # Attack!
                weakest_hp = 9999
                weakest_u = []
                for t in targets_in_range:
                    if t[3] < weakest_hp:
                        weakest_hp = t[3]
                        weakest_u = t

                assert weakest_hp != 9999

                weakest_u[3] -= elf_damage if u[0] == 0 else 3
                action = True

                if weakest_u[3] <= 0:
                    # Die!
                    if not part1:
                        if weakest_u[0] == 0:
                            elf_died = True
                            print(f"Elf died! Moving onto next highest attack value: {elf_damage + 1}")
                    unit_killed = units.index(weakest_u)
                    units.remove(weakest_u)

                if not part1 and elf_died:
                    break

            if unit_killed == -1 or unit_killed > ui:
                ui += 1

        if targets_remain:
            full_rounds += 1

        if not part1 and elf_died:
            break

        if not action:
            print("nothing happened this round!")
    if part1:
        break
    else:
        if elf_died:
            init()
            elf_damage += 1

end = timer()

print_board()

summed_hp = sum([u[3] for u in units])
outcome = full_rounds * summed_hp
print(f"outcome: {outcome}, full rounds: {full_rounds}, summed_hp: {summed_hp}, elf dmg: {elf_damage}, remaining units: {units}")
print(f"took {end-start:.2f}s")
