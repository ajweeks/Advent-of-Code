import math

# ========= ⚠ WARNING: GROSS CODE LIES AHEAD: BE WARNED ⚠ ========= #


def get_input_str():
    return open("day10.in").readlines()


def get_inputs(input_str):
    return [x.strip() for x in input_str]


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def reduce(a, b):
    if a == 0:
        return (0, 1 if b > 0 else -1)
    elif b == 0:
        return (1 if a > 0 else -1, 0)

    orig_ratio = a / b
    common_divisor = gcd(abs(a), abs(b))
    a //= common_divisor
    b //= common_divisor

    return (a, b)


def manhattan(x, y):
    return abs(x) + abs(y)


def get_visible_asteroids(pos, field, print_asteroids=False):
    seen = dict()
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell == 0 or (x, y) == pos:
                continue
            ratio = reduce(x - pos[0], y - pos[1])
            dist = manhattan(x - pos[0], y - pos[1])
            if ratio in seen.keys():
                if dist < seen[ratio][0]:
                    seen[ratio] = (dist, (x, y))
            else:
                seen[ratio] = (dist, (x, y))

    if print_asteroids:
        for key, value in seen:
            print(key, value)

    return seen


def part1():
    inputs = get_inputs(get_input_str())
    field = []
    for line in inputs:
        field.append([1 if x == '#' else 0 for x in line])

    best_asteroid = (0, 0)
    best_asteroid_count = 0

    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell == 1:  # asteroid
                a_count = len(get_visible_asteroids((x, y), field))
                if a_count > best_asteroid_count:
                    best_asteroid_count = a_count
                    best_asteroid = (x, y)

    # print(best_asteroid, best_asteroid_count)
    # count_line_of_sight(best_asteroid, field, True)

    return best_asteroid_count


# Find the closest asteroid that is at or in front of (clockwise from) the current laser angle
def next_asteroid(laser_angle, visible_asteroids, laser_pos, quadrant):
    max_angle = laser_angle - math.pi / 2.0
    if quadrant == 2:
        max_angle = -math.pi

    next_roid = None
    for asteroid in visible_asteroids.values():
        angle = math.atan2(-(asteroid[1][1] - laser_pos[1]), asteroid[1][0] - laser_pos[0])

        if max_angle <= angle <= laser_angle:
            if next_roid is None or (max_angle != angle or (max_angle == angle and asteroid[0] < next_roid[0])):
                max_angle = angle
                next_roid = asteroid

    if quadrant == 2 and next_roid is None:  # Yikeroonies
        quadrant = 1
        return next_asteroid(math.pi, visible_asteroids, laser_pos, quadrant)

    return next_roid, max_angle - 0.000001


def part2():
    inputs = get_inputs(get_input_str())
    inputs2 = get_inputs(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split('\n'))
    field = []
    for line in inputs:
        field.append([1 if x == '#' else 0 for x in line])

    best_asteroid = (0, 0)
    best_asteroid_count = 0

    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell == 1:  # asteroid
                visible_asteroids = get_visible_asteroids((x, y), field)
                if len(visible_asteroids) > best_asteroid_count:
                    best_asteroid_count = len(visible_asteroids)
                    best_asteroid = (x, y)

    visible_asteroids = get_visible_asteroids(best_asteroid, field)

    exploded_asteroid_count = 0
    asteroid_200 = None
    quadrant = 0
    laser_angle = math.pi / 2.0
    while 1:
        asteroid, laser_angle = next_asteroid(laser_angle, visible_asteroids, best_asteroid, quadrant)
        if asteroid is None:
            print("UH OH!")
            break
        else:
            asteroid_pos = asteroid[1]
            field[asteroid_pos[1]][asteroid_pos[0]] = 0  # Boom!
            exploded_asteroid_count += 1
            # print("explosion", exploded_asteroid_count, "at", asteroid_pos, "- laser angle:", laser_angle, "- quadrant:", quadrant)

            if exploded_asteroid_count == 200:
                asteroid_200 = asteroid
                # print("200!", asteroid)
                break

        if quadrant == 0 and laser_angle <= 0.0:
            quadrant = 3
            # print("quadrant", quadrant, "vis: ", len(visible_asteroids))
        elif quadrant == 3 and laser_angle <= -math.pi / 2.0:
            quadrant = 2
            # print("quadrant", quadrant, "vis: ", len(visible_asteroids))
        elif quadrant == 2 and laser_angle >= 0.0:
            quadrant = 1
            # print("quadrant", quadrant, "vis: ", len(visible_asteroids))
        elif quadrant == 1 and laser_angle <= math.pi / 2.0:
            quadrant = 0
            # print("quadrant", quadrant, "vis: ", len(visible_asteroids))

        visible_asteroids = get_visible_asteroids(best_asteroid, field)
        if len(visible_asteroids) == 0:
            break

    return asteroid_200[1][0] * 100 + asteroid_200[1][1]
