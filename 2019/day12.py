
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


def part2():
    positions = get_inputs(get_input_str())
    positions = get_inputs("""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".splitlines())
    velocities = [(0, 0, 0)] * len(positions)

    for i, p in enumerate(positions):
        print(p, velocities[i])
    print()

    history = []

    iter_count = 0
    while 1:
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

        iter_count += 1
        if iter_count % 1000 == 0:
            print(iter_count)

        if h in history:
            print("history repeated itself after", iter_count, "iterations")

            for i, p in enumerate(positions):
                print(p, velocities[i])
            print()

            print(history)

            break
        else:
            history.append(h)
            # history.append((positions.copy(), velocities.copy()))

    energy = sum([kinetic_energy(velocities[i]) * potential_energy(positions[i]) for i in range(len(positions))])

    return energy