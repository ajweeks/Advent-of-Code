import intcode
import itertools


def get_input_str():
    return open("day17.in").readlines()[0]


def get_inputs(input_str):
    return [int(x) for x in input_str.split(',')]


SCAFFOLD = 35
EMPTY = 46
NEW_LINE = 10

w = 38
h = 33
scaffolding = [0] * (w * h)
intersections = []
output_idx = 0
alignment_params = 0
comp = intcode.Intcode()
robo_pos = (-1, -1)
robo_dir = -1
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
movements = [(0, -1), (1, 0), (0, 1), (-1, 0)]
end = (-1, -1)
total_dist_traveled = 0
last_output = 0


def print_scaffolding():
    for yy in range(h):
        for xx in range(w):
            val = scaffolding[idx(xx, yy)]
            if (xx, yy) in intersections:
                val = ord('O')
            elif (xx, yy) == robo_pos:
                val = ord(['^', '>', 'v', '<'][robo_dir])
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
    global output_idx, scaffolding, alignment_params, comp, robo_pos, robo_dir

    scaffolding[output_idx] = val

    if val == ord('^'):
        robo_pos = (output_idx % w, output_idx // w)
        robo_dir = NORTH
        scaffolding[output_idx] = ord('#')

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
    global part2_inputs, part2_input_index

    result = part2_inputs[part2_input_index]
    part2_input_index += 1
    return result


def on_output2(val):
    global output_idx, scaffolding, alignment_params, comp, last_output

    scaffolding[output_idx] = val
    output_idx += 1

    if output_idx == (w * h):
        count_intersections()
        output_idx = 0
        # print_scaffolding()

    last_output = val


def find_end_point(pos, dir):
    global scaffolding

    while 0 <= pos[0] < w and 0 <= pos[1] < h and scaffolding[idx(pos[0], pos[1])] == ord('#'):
        pos = (pos[0] + movements[dir][0], pos[1] + movements[dir][1])

    pos = (pos[0] - movements[dir][0], pos[1] - movements[dir][1])  # undo last step
    return pos


def get_dist(pos1, pos2):
    return abs(pos2[0] - pos1[0] + pos2[1] - pos1[1])


def rotate_to(cur_dir, target_dir):
    diff = target_dir - cur_dir
    if abs(diff) == 1 or abs(diff) == 3:
        if diff == 1 or diff == -3:
            return 'R'
        else:
            return 'L'
    else:
        return 'X'


def rotate(facing, rotation):
    return (facing + (1 if rotation == 'R' else -1)) % 4


def valid_seq(seq, pos, dir):
    start_pos = pos
    start_dir = dir
    combo_parts = seq[0].split(',')
    dist_traveled = 0
    for combo in combo_parts:
        if combo == '':
            continue
        dir = rotate(dir, combo[0])
        for _ in range(int(combo[1:])):
            pos = (pos[0] + movements[dir][0], pos[1] + movements[dir][1])
            if pos[0] < 0 or pos[0] >= w or pos[1] < 0 or pos[1] >= h or scaffolding[idx(pos[0], pos[1])] != ord('#'):
                return start_pos, start_dir, dist_traveled, False
        dist_traveled += int(combo[1:])
    return pos, dir, dist_traveled, True


def eval_seq_combo(seq_combo):
    global total_dist_traveled
    cur_dir = robo_dir
    cur_pos = robo_pos
    seq_indices = []

    local_total_dist_traveled = 0
    while 1:
        valid_seq_found = False
        for seq_idx, seq in enumerate(seq_combo):
            cur_pos, cur_dir, dist_traveled, success = valid_seq(seq, cur_pos, cur_dir)
            if success:
                valid_seq_found = True
                local_total_dist_traveled += dist_traveled
                seq_indices.append(seq_idx)
                break
        if not valid_seq_found:
            total_dist_traveled = max(local_total_dist_traveled, total_dist_traveled)
            return seq_indices, False
        if cur_pos == end:
            total_dist_traveled = max(local_total_dist_traveled, total_dist_traveled)
            return seq_indices, True


part2_inputs = []
part2_input_index = 0


def part2():
    global comp, end, part2_inputs, part2_input_index

    if len(scaffolding) == 0:
        part1()  # Discover scaffolding

    # print_scaffolding()

    path = []
    dir = -1
    cur_pos = robo_pos
    cur_dir = robo_dir

    total_dist = 0
    while 1:
        pdir = dir
        if cur_pos[0] > 0 and scaffolding[idx(cur_pos[0] - 1, cur_pos[1])] == ord('#') and dir != EAST:
            dir = WEST
        elif cur_pos[0] < (w - 1) and scaffolding[idx(cur_pos[0] + 1, cur_pos[1])] == ord('#') and dir != WEST:
            dir = EAST
        elif cur_pos[1] > 0 and scaffolding[idx(cur_pos[0], cur_pos[1] - 1)] == ord('#') and dir != NORTH:
            dir = NORTH
        elif cur_pos[1] < h - 1 and scaffolding[idx(cur_pos[0], cur_pos[1] + 1)] == ord('#') and dir != NORTH:
            dir = SOUTH

        if dir == pdir:
            end = cur_pos
            break  # Reached end

        last_pos = cur_pos
        last_dir = cur_dir
        cur_pos = find_end_point(cur_pos, dir)
        dist = get_dist(last_pos, cur_pos)
        cur_dir = dir
        path.append(rotate_to(last_dir, cur_dir))
        path.append(dist)
        total_dist += dist

    path_str = ''.join([x if type(x) == str else (str(x) + ',') for x in path])

    sequence_counts = []
    path_parts = path_str.split(',')
    for i, p in enumerate(path_parts):
        if p == ',':
            continue
        for ii in range(i + 3, i + 10):
            seq = ''.join([x + (',' if (j+i) < ii-1 else '') for j, x in enumerate(path_parts[i:ii])])
            c = path_str.count(seq)
            if len(seq) > 2 and c > 0 and (seq, c) not in sequence_counts:
                sequence_counts.append((seq, c))

    sequence_counts = sorted(sequence_counts, key=lambda x: x[1], reverse=True)

    winning_combo = None
    for seq_combo in itertools.combinations(sequence_counts, 3):
        seq_indices, result = eval_seq_combo(seq_combo)
        if result:
            winning_combo  = (seq_indices, seq_combo)
            break

    # print(winning_combo)

    for index in winning_combo[0]:
        part2_inputs.append(ord('A') + index)
        part2_inputs.append(ord(','))
    part2_inputs[-1] = NEW_LINE

    for combo in winning_combo[1]:
        combo_parts = combo[0].split(',')
        for c in combo_parts:
            part2_inputs.append(ord(c[0]))  # L or R
            part2_inputs.append(ord(','))
            part2_inputs.extend([ord(x) for x in c[1:]])
            part2_inputs.append(ord(','))
        part2_inputs[-1] = NEW_LINE

    part2_inputs.append(ord('n'))
    part2_inputs.append(NEW_LINE)

    # print(part2_inputs)

    instr = get_inputs(get_input_str())
    instr.extend([0] * 100000)
    instr[0] = 2
    comp = intcode.Intcode()
    comp.run(instr, False, False, True, get_input2, on_output2)

    return last_output
