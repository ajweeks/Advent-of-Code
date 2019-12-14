import math


def get_input_str():
    return open("day12.in").readlines()


def get_inputs(input_str):
    return [(int(l.split('=')[1].split(',')[0]), int(l.split('=')[2].split(',')[0]), int(l.split('=')[3][0:-1])) for l in [t.strip() for t in input_str]]


def sub(p1, p2):
    return (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])


def add(p1, p2):
    return (p2[0]+p1[0], p2[1]+p1[1], p2[2]+p1[2])


def potential_energy(moon_pos):
    return abs(moon_pos[0]) + abs(moon_pos[1]) + abs(moon_pos[2])


def kinetic_energy(moon_vel):
    return abs(moon_vel[0]) + abs(moon_vel[1]) + abs(moon_vel[2])


def part1():
    positions = get_inputs(get_input_str())
    velocities = [(0, 0, 0)] * len(positions)

    for step in range(1000):
        for i in range(0, len(velocities)):
            for j in range(i + 1, len(velocities)):
                delta = sub(positions[i], positions[j])
                velocities[i] = add(velocities[i],
                                    (1 if delta[0] > 0 else -1 if delta[0] < 0 else 0,
                                     1 if delta[1] > 0 else -1 if delta[1] < 0 else 0,
                                     1 if delta[2] > 0 else -1 if delta[2] < 0 else 0))
                velocities[j] = add(velocities[j],
                                    (-1 if delta[0] > 0 else 1 if delta[0] < 0 else 0,
                                     -1 if delta[1] > 0 else 1 if delta[1] < 0 else 0,
                                     -1 if delta[2] > 0 else 1 if delta[2] < 0 else 0))

        for i in range(len(positions)):
            positions[i] = add(positions[i], velocities[i])

    energy = sum([kinetic_energy(velocities[i]) * potential_energy(positions[i]) for i in range(len(positions))])

    return energy


def sim(positions, velocities):
    step_count = 0

    starting_positions = positions.copy()
    starting_velocities = velocities.copy()

    while step_count == 0 or positions != starting_positions and velocities != starting_velocities:
        for i in range(len(positions)):
            velocities[i] += sum(1 if positions[i] < p else -1 if positions[i] > p else 0 for p in positions if p != positions[i])
        for i in range(len(positions)):
            positions[i] += velocities[i]
        step_count += 1

    return step_count


def part2():
    positions = get_inputs(get_input_str())
    positions2 = get_inputs("""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""".splitlines())

    xx = sim([x for x, _, _ in positions], [0] * len(positions))
    yy = sim([y for _, y, _ in positions], [0] * len(positions))
    zz = sim([z for _, _, z in positions], [0] * len(positions))

    def _lcm(a, b):
        return a * b // math.gcd(a, b)

    steps = _lcm(xx, _lcm(yy, zz))

    return steps * 2