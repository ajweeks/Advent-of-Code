import math

lines = open("day23.in").readlines()

# lines = """pos=<0,0,0>, r=4
# pos=<1,0,0>, r=1
# pos=<4,0,0>, r=3
# pos=<0,2,0>, r=1
# pos=<0,5,0>, r=3
# pos=<0,0,3>, r=1
# pos=<1,1,1>, r=1
# pos=<1,1,2>, r=1
# pos=<1,3,1>, r=1""".splitlines()

lines = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".splitlines()


def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])


min_x, min_y, min_z = math.inf, math.inf, math.inf
max_x, max_y, max_z = -math.inf, -math.inf, -math.inf
bots = []
for line in lines:
    x, y, z = map(int, line.split('<')[1].split('>')[0].split(','))
    r = int(line.split('r=')[1])
    bots.append([x, y, z, r])

    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

print(min_x, min_y, min_z, max_x, max_y, max_z)

strongest = [-1, -1, -1, -1]
for b in bots:
    if b[3] > strongest[3]:
        strongest = b

in_range = []
for b in bots:
    if dist(strongest, b) <= strongest[3]:
        in_range.append(b)

print(f"p1: {len(in_range)}")


def in_box(bot, xr, yr, zr):
    x, y, z = bot[0], bot[1], bot[2]
    r = bot[3]
    return x-r >= xr[0] and x+r <= xr[1] and \
           y-r >= yr[0] and y+r <= yr[1] and \
           z-r >= zr[0] and z+r <= zr[1]


# -1629600, -1366100, -285300
# (-285400, -1366200, -1629700, 1000) => 3281600
most_in_range = (-1, -1, -1, -1)
best_dist = 556513799
# min_x, min_y, min_z = -1613185-1000, -1367592-1000, -300436-1000
# max_x, max_y, max_z = min_x + 1000, min_y + 10000, min_z + 100000
x, y, z = min_x, min_y, min_z
while (max_x - min_x) > 1:
    quadrants = [0] * 8
    for z in [0, 1]:
        for y in [0, 1]:
            for x in [0, 1]:
                hx = (max_x - min_x) // 2
                xr = (min_x + x * hx, min_x + (x + 1) * hx)
                hy = (max_y - min_y) // 2
                yr = (min_y + y * hy, min_y + (y + 1) * hy)
                hz = (max_z - min_z) // 2
                zr = (min_z + z * hz, min_z + (z + 1) * hz)
                for b in bots:
                    if in_box(b, xr, yr, zr):
                        quadrants[z*4+y*2+x] += 1

    most_q = (-1, -1, -1)
    most_in_q = -1
    for z in [0, 1]:
        for y in [0, 1]:
            for x in [0, 1]:
                if quadrants[z*4+y*2+x] >= most_in_q:
                    if quadrants[z*4+y*2+x] == most_in_q:
                        hx = (max_x - min_x) // 2
                        n_x, x_x = (min_x + x * hx, min_x + (x + 1) * hx + (max_x - min_x) % 2)
                        hy = (max_y - min_y) // 2
                        n_y, x_y = (min_y + y * hy, min_y + (y + 1) * hy + (max_y - min_y) % 2)
                        hz = (max_z - min_z) // 2
                        n_z, x_z = (min_z + z * hz, min_z + (z + 1) * hz + (max_z - min_z) % 2)
                        if dist((min(n_x, x_x), min(n_y, x_y), min(n_z, x_z)), (0, 0, 0)) > \
                           dist((min(min_x, max_x), min(min_y, max_y), min(min_z, max_z)), (0, 0, 0)):
                            continue
                    most_in_q = quadrants[z*4+y*2+x]
                    most_q = (x, y, z)

    assert most_q != (-1, -1, -1)

    hx = (max_x - min_x) // 2
    min_x, max_x = (min_x + most_q[0] * hx, min_x + (most_q[0] + 1) * hx + (max_x - min_x) % 2)
    hy = (max_y - min_y) // 2
    min_y, max_y = (min_y + most_q[1] * hy, min_y + (most_q[1] + 1) * hy + (max_y - min_y) % 2)
    hz = (max_z - min_z) // 2
    min_z, max_z = (min_z + most_q[2] * hz, min_z + (most_q[2] + 1) * hz + (max_z - min_z) % 2)

    # print(x, y, z, in_range, best_dist)

print()
print((min_x, min_y, min_z), (max_x, max_y, max_z))
print(dist((min_x, min_y, min_z), (0, 0, 0)))
print(dist((max_x, max_y, max_z), (0, 0, 0)))

# 117923168 -> x
# 117922958 -> x
# 117922848 -> x
# 3282050 -> x
# 3281542 -> x
# 3274726-> x
# 556513799 -> x
# 556513796 -> ?