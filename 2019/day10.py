
import math


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
            ratio = reduce(x-pos[0], y-pos[1])
            dist = manhattan(x-pos[0], y-pos[1])
            if ratio in seen.keys():
                if dist < seen[ratio][0]:
                    seen[ratio] = (dist, (x, y))
            else:
                seen[ratio] = (dist, (x, y))
            # print(ratio)

    if print_asteroids:
        for key, value in seen:
            print(key, value)

    return seen


def part1():
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
                a_count = len(get_visible_asteroids((x, y), field))
                if a_count > best_asteroid_count:
                    best_asteroid_count = a_count
                    best_asteroid = (x, y)

    print(best_asteroid, best_asteroid_count)
    # count_line_of_sight(best_asteroid, field, True)

    return best_asteroid_count


def next_asteroid(laser_angle, visible_asteroids, laser_pos, quadrant):
    max_angle = laser_angle - math.pi
    if max_angle < -2 * math.pi:
        max_angle += 4 * math.pi

    next_roid = None
    for asteroid in visible_asteroids.values():
        angle = math.atan2(asteroid[1][1] - laser_pos[1], asteroid[1][0] - laser_pos[0])
        if ((quadrant == 0 or quadrant == 1) and (max_angle < angle <= laser_angle)) or\
           ((quadrant == 3 or quadrant == 2) and (max_angle < angle <= laser_angle)):
            if next_roid is None or asteroid[0] < next_roid[0]:
                max_angle = angle
                next_roid = asteroid

    return next_roid, max_angle - 0.0001


def part2():
    inputs = get_inputs(get_input_str())
    inputs = get_inputs(""".#..##.###...#######
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

    # best_asteroid = ()

    # print(best_asteroid, best_asteroid_count)
    visible_asteroids = get_visible_asteroids(best_asteroid, field)

    exploded_asteroid_count = 0
    asteroid_200 = None
    quadrant = 0
    laser_angle = math.pi
    while 1:
        asteroid, laser_angle = next_asteroid(laser_angle, visible_asteroids, best_asteroid, quadrant)
        if asteroid is None:
            if sum([sum(x) for x in field]) == 0:
                break
            # quadrant -= 1
            # if quadrant < 0:
            #     quadrant = 3
        else:
            asteroid_pos = asteroid[1]
            field[asteroid_pos[1]][asteroid_pos[0]] = 0  # Boom!
            exploded_asteroid_count += 1
            print("exploded ", asteroid_pos, "laser angle", laser_angle)

            if exploded_asteroid_count == 200:
                asteroid_200 = asteroid
                print("200!", asteroid)
                break

        if quadrant == 0 and laser_angle <= 0.0:
            quadrant = 3
            print("quadrant", quadrant, "vis: ", len(visible_asteroids))
        elif quadrant == 3 and laser_angle <= -math.pi:
            quadrant = 2
            print("quadrant", quadrant, "vis: ", len(visible_asteroids))
        elif quadrant == 2 and laser_angle >= 0.0:
            quadrant = 1
            print("quadrant", quadrant, "vis: ", len(visible_asteroids))
        elif quadrant == 1 and laser_angle <= math.pi:
            quadrant = 0
            print("quadrant", quadrant, "vis: ", len(visible_asteroids))

        visible_asteroids = get_visible_asteroids(best_asteroid, field)
        if len(visible_asteroids) == 0:
            break

    return asteroid_200[1][0] * 100 + asteroid_200[1][1]
