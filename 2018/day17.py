
lines = open("day17.in").readlines()

# lines = """x=495, y=2..7
# y=7, x=495..501
# x=501, y=3..7
# x=498, y=2..4
# x=506, y=1..2
# x=498, y=10..13
# x=504, y=10..13
# y=13, x=498..504""".splitlines()


def draw_ground():
    for yy in range(h):
        print(f"{yy:2} ", end='')
        for xx in range(min_x, max_x+1):
            if yy == 0 and xx == 500:
                print('+', end='')
            else:
                c = cells[yy * w + (xx-min_x)]
                print('|' if c[1] == 1 else '~' if c[1] == 2 else '.' if c[0] == 0 else '#', end='')
        print()
    print()


def sideways_flood_fill(x, y):
    assert cells[y * w + (x-min_x)][0] == 0
    left, right = x, x
    changed = False
    while cells[y * w + (left-min_x)][0] == 0 and \
            (cells[(y+1) * w + (left-min_x)][0] == 1 or
             cells[(y+1) * w + (left-min_x)][1] == 2):
        if cells[y * w + (left-min_x)][1] != 1:
            cells[y * w + (left-min_x)][1] = 1
            changed = True
        left -= 1
    while cells[y * w + (right-min_x)][0] == 0 and \
            (cells[(y+1) * w + (right-min_x)][0] == 1 or
             cells[(y+1) * w + (right-min_x)][1] == 2):
        if cells[y * w + (right-min_x)][1] != 1:
            cells[y * w + (right-min_x)][1] = 1
            changed = True
        right += 1

    bounded_left = cells[y * w + (left-min_x)][0] == 1
    bounded_right = cells[y * w + (right-min_x)][0] == 1

    # print(x, y, left, right, bounded_left, bounded_right)

    if bounded_left and bounded_right:
        for xx in range(left+1, right):
            if cells[y * w + (xx-min_x)][1] != 2:
                cells[y * w + (xx-min_x)][1] = 2
                changed = True
        # draw_ground()
    else:
        for xx in range(left+1, right):
            cells[y * w + (xx-min_x)][1] = 1
        if not bounded_left:
            if drop_vertically(left, y):
                changed = True
        if not bounded_right:
            if drop_vertically(right, y):
                changed = True
    return changed


def drop_vertically(x, y):
    c = cells[y * w + (x-min_x)]
    assert c[0] == 0
    c[1] = 1
    c_d = cells[(y+1) * w + (x-min_x)]
    changed = False
    while y < h and c_d[0] == 0 and (c_d[1] == 0 or c_d[1] == 1):
        if c_d[1] != 1:
            c_d[1] = 1
            changed = True
        y += 1
        if y + 1 < h:
            c_d = cells[(y+1) * w + (x-min_x)]

    if y >= h:
        return changed

    assert c_d[0] == 1 or c_d[1] == 2  # Either on clay or water surface

    if sideways_flood_fill(x, y):
        changed = True

    # draw_ground()

    return changed


ranges = []
min_x = 9999
max_x = -9999
min_y = 9999
max_y = -9999
for line in lines:
    const_num = int(line.split(', ')[0].split('=')[1])
    range_min = int(line.split(', ')[1].split('=')[1].split('.')[0])
    range_max = int(line.split(', ')[1].split('=')[1].split('.')[2])

    ranges.append([0 if line[0] == 'x' else 1, const_num, range_min, range_max])

for r in ranges:
    if r[0] == 0:
        min_x = min(min_x, r[1])
        max_x = max(max_x, r[1])
        min_y = min(min_y, r[2])
        max_y = max(max_y, r[3])
    else:
        min_y = min(min_y, r[1])
        max_y = max(max_y, r[1])
        min_x = min(min_x, r[2])
        max_x = max(max_x, r[3])

min_x -= 1
max_x += 1
w = (max_x - min_x + 2)
max_y += 1
h = (max_y + 1)

cells = []
for i in range(w * h):
    # [(0=sand, 1=clay), (0=no water, 1=water touched, 2=water present)]
    cells.append([0, 0])

for r in ranges:
    for i in range(r[2], r[3]+1):
        if r[0] == 0:  # x
            cells[i * w + (r[1]-min_x)][0] = 1
        else:  # y
            cells[r[1] * w + (i-min_x)][0] = 1


while drop_vertically(500, 0):
    pass

draw_ground()

touched_cells = sum([1 for ci in range(len(cells)) if (w * min_y <= ci < (w*max_y) and (cells[ci][1] == 1 or cells[ci][1] == 2))])
filled_cells = sum([1 for ci in range(len(cells)) if (w * min_y <= ci < (w*max_y) and cells[ci][1] == 2)])
print(touched_cells, filled_cells)
