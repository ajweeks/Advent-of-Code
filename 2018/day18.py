lines = [l.strip() for l in open("day18.in").readlines()]

# lines = """.#.#...|#.
# .....#|##|
# .|..|...#.
# ..|#.....#
# #.#|||#|#|
# ...#.||...
# .|....|...
# ||...#|.#|
# |.||||..|.
# ...#.|..|.""".splitlines()

w, h = len(lines[0]), len(lines)
acres = []
for line in lines:
    for l in line:
        acres.append(0 if l == '.' else 1 if l == '|' else 2)


def print_board():
    for yy in range(h):
        for xx in range(w):
            a = acres[yy * w + xx]
            print('.' if a == 0 else '|' if a == 1 else '#', end='')
        print()
    print()


r = 1000000000
acres_hist = []
i = 0
skipped = False
part1 = 0
while i < r - 1:
    new_acres = acres.copy()
    for yy in range(h):
        for xx in range(w):
            tree_neighbors = 0
            lumberyard_neighbors = 0
            open_neighbors = 0

            for yo in range(-1, 1+1):
                for xo in range(-1, 1+1):
                    if xo == 0 and yo == 0:
                        continue
                    if 0 <= (yy + yo) < h and 0 <= (xx + xo) < w:
                        n = acres[(yy + yo) * w + (xx + xo)]
                        if n == 0:
                            open_neighbors += 1
                        if n == 1:
                            tree_neighbors += 1
                        if n == 2:
                            lumberyard_neighbors += 1

            a = acres[yy * w + xx]
            if a == 0 and tree_neighbors >= 3:
                new_acres[yy * w + xx] = 1
            elif a == 1 and lumberyard_neighbors >= 3:
                new_acres[yy * w + xx] = 2
            elif a == 2 and (lumberyard_neighbors < 1 or tree_neighbors < 1):
                new_acres[yy * w + xx] = 0

    acres = new_acres
    if not skipped and acres in acres_hist:
        skipped = True
        cycle_len = (i - acres_hist.index(acres))
        print(f"repeat on i: {i}, cycle_len: {cycle_len}")
        delta_i = cycle_len * ((r-i) // cycle_len)
        print(f"adding {delta_i} to i")
        i += delta_i
    else:
        i += 1

    if i == 10:
        part1 = sum([1 for t in acres if t == 1]) * sum([1 for l in acres if l == 2])

    acres_hist.append(acres)
    print(f"{i}, {sum([1 for t in acres if t == 0])}, {sum([1 for t in acres if t == 1])}, {sum([1 for l in acres if l == 2])}")


print(f"part1: {part1}")
final_tree_count = sum([1 for t in acres if t == 1])
final_lumberyard_count = sum([1 for l in acres if l == 2])
print(f"part2: {final_tree_count * final_lumberyard_count} \
({final_tree_count} * {final_lumberyard_count})")
