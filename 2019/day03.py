def get_inputs():
    return [y.split(',') for y in [x for x in open("day03.in").readlines()]]


def is_horiz(seg):
    return seg[0][0] != seg[1][0]


def intersect(seg1, seg2):
    seg1Horiz = is_horiz(seg1)
    seg2Horiz = is_horiz(seg2)
    if seg1Horiz == seg2Horiz:
        # Lines are parallel
        return None
    if seg1Horiz:
        if seg1[0][0] > seg2[0][0] or seg1[1][0] < seg2[0][0]:
            return None
        elif not(seg2[0][1] < seg1[0][1] < seg2[1][1]):
            return None
    else: # seg2 is horizontal
        if seg2[0][0] > seg1[0][0] or seg2[1][0] < seg1[0][0]:
            return None
        elif not(seg1[0][1] < seg2[0][1] < seg1[1][1]):
            return None

    if seg1Horiz:
        return (seg2[0][0], seg1[0][1])
    else:
        return (seg1[0][0], seg2[0][1])


def manhattan(point):
    return abs(point[0]) + abs(point[1])


def get_segs():
    inputs = get_inputs()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # inputs = [['R8', 'U5', 'L5', 'D3'], ['U7', 'R6', 'D4', 'L4']]
    # inputs = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
    #           ['U62','R66','U55','R34','D71','R55','D58','R83']]
    # inputs = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
    #           ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]
    all_line_segs = []
    for line in inputs:
        # print(line)
        last_pos = (0, 0)
        line_segs = []
        steps = 0
        for inst in line:
            heading = 0 if inst[0] == 'U' else 1 if inst[0] == 'R' else 2 if inst[0] == 'D' else 3
            dist = int(inst[1:])
            steps += dist
            new_pos = (last_pos[0] + dirs[heading][0] * dist, last_pos[1] + dirs[heading][1] * dist)
            # first point is always bottom-left-most
            line_segs.append((((min(last_pos[0], new_pos[0]), min(last_pos[1], new_pos[1])), (max(last_pos[0], new_pos[0]), max(last_pos[1], new_pos[1]))), steps))
            last_pos = new_pos

        all_line_segs.append(line_segs)
    return all_line_segs


def part1():
    all_line_segs = get_segs()
    closest_crossing = ((99999, 99999), 99999)  # (x, y), steps

    for wire_index in range(len(all_line_segs)):
        for seg in all_line_segs[wire_index]:
            for wire_index2 in range(wire_index + 1, len(all_line_segs)):
                for seg2 in all_line_segs[wire_index2]:
                    cross = intersect(seg[0], seg2[0])
                    if cross is not None:
                        dist = manhattan(cross)
                        if dist < manhattan(closest_crossing[0]):
                            closest_crossing = (cross, 0)

    print(closest_crossing[0], manhattan(closest_crossing[0]))


def additional_steps(p_seg, n_seg, crossing):
    if is_horiz(n_seg):
        if n_seg[0] == p_seg[0] or n_seg[0] == p_seg[1]:
            # Going right
            dist = n_seg[1][0] - crossing[0]
            return dist
        elif n_seg[1] == p_seg[0] or n_seg[1] == p_seg[1]:
            # Going left
            dist = crossing[0] - n_seg[0][0]
            return dist
        else:
            assert False
    else:
        if n_seg[0] == p_seg[0] or n_seg[0] == p_seg[1]:
            # Going up
            dist = n_seg[1][1] - crossing[1]
            return dist
        elif n_seg[1] == p_seg[0] or n_seg[1] == p_seg[1]:
            # Going down
            dist = crossing[1] - n_seg[0][1]
            return dist
        else:
            assert False

def dist_to_point(segs, point):
    dist = 0
    for seg_i in range(len(segs)):
        seg = segs[seg_i][0]
        dist += seg[1][0] - seg[0][0] + seg[1][1] - seg[0][1]

        if point[0] == seg[0][0] and point[0] == seg[1][0]:
            if seg[0][1] <= point[1] <= seg[1][1]:
                dist -= additional_steps(((0,0),(0,0)) if seg_i == 0 else segs[seg_i-1][0], segs[seg_i][0], point)
                return dist
        elif point[1] == seg[0][1] and point[1] == seg[1][1]:
            if seg[0][0] <= point[0] <= seg[1][0]:
                dist -= additional_steps(((0,0),(0,0)) if seg_i == 0 else segs[seg_i-1][0], segs[seg_i][0], point)
                return dist
    return -1


def part2():
    all_line_segs = get_segs()
    closest_crossing = ((99999, 99999), 99999)  # (x, y), steps

    for wire_index in range(len(all_line_segs)):
        for seg_i in range(len(all_line_segs[wire_index])):
            seg = all_line_segs[wire_index][seg_i]
            for wire_index2 in range(wire_index + 1, len(all_line_segs)):
                for seg2_i in range(len(all_line_segs[wire_index2])):
                    seg2 = all_line_segs[wire_index2][seg2_i]
                    cross = intersect(seg[0], seg2[0])
                    if cross is not None:
                        total_dist = dist_to_point(all_line_segs[wire_index], cross)
                        total_dist += dist_to_point(all_line_segs[wire_index2], cross)
                        if total_dist < closest_crossing[1]:
                            closest_crossing = (cross, total_dist)

    print(closest_crossing[0], closest_crossing[1])
