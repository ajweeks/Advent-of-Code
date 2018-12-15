
lines = open("day12.in").readlines()

# lines = """initial state: #..#.#..##......###...###
#
# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #""".splitlines()

initial_state = [1 if x == '#' else 0 for x in lines[0].split(':')[1][1:]]

rules = []
for i in range(2, len(lines)):
    pattern = [1 if x == '#' else 0 for x in lines[i].split(' => ')[0]]
    end_state = 1 if lines[i].split(' => ')[1][0] == '#' else 0
    rules.append([pattern, end_state])


def get_alive(sample):
    for r in rules:
        if r[0] == sample:
            return r[1]
    return 0


pots = [0] * len(initial_state) * 3
zero_idx = int(len(pots) / 2)
for i in range(len(initial_state)):
    pots[zero_idx + i] = initial_state[i]

print(' ', end='')
for p in range(0, len(pots), 5):
    print(str(abs(p - zero_idx)) + '   ', end='')
print()

r = 20
for i in range(r):
    print(str(i) + ': ', end='')
    for p in pots:
        print('#' if p == 1 else '.', end='')
    print()

    new_pots = pots.copy()

    for p in range(2, len(pots) - 2):
        new_pots[p] = get_alive(pots[p-2:p+3])
        if new_pots[p] and (p < 10 or p > len(pots) - 10):
            print(f"ruh roh, p={p}")

    pots = new_pots
    print(sum([x - zero_idx if pots[x] == 1 else 0 for x in range(len(pots))]))

print(str(r) + ': ', end='')
for p in pots:
    print('#' if p == 1 else '.', end='')
print()

pot_sum = sum([x - zero_idx if pots[x] == 1 else 0 for x in range(len(pots))])
print(f"p1: {pot_sum}")

x = 50000000000
print(f"p2: {67000 + (x - 1000) * 67}")
