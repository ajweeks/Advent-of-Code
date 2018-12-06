
lines = open("day06.in").read().split('\n')

# lines = """1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9""".split('\n')


def manhattan(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)


coords = []
for line in lines:
    parts = line.split(", ")
    coords.append([int(parts[0]), int(parts[1])])

max_x = max_y = 0

for coord in coords:
    max_x = max(coord[0] + 1, max_x)
    max_y = max(coord[1] + 1, max_y)

print(max_x, max_y)

possibleIdces = [x for x in coords]

for coord in coords:
    if coord[0] == 0 or coord[0] == max_x or \
       coord[1] == 0 or coord[1] == max_y:
        possibleIdces.remove(coord)

print(coords)
print(possibleIdces)

grid = [999] * (max_x * max_y)
for yy in range(max_y):
    for xx in range(max_x):
        shortest = 999
        shortestIdx = -1
        equi = False
        for c in range(len(coords)):
            dist = manhattan(coords[c][0], coords[c][1], xx, yy)
            if dist < shortest:
                shortest = dist
                shortestIdx = c
                equi = False
            elif dist == shortest:
                equi = True
        if equi:
            grid[yy * max_x + xx] = -1
        elif shortestIdx != -1:
            grid[yy * max_x + xx] = shortestIdx

for yy in range(max_y):
    for xx in range(max_x):
        c = False
        for j in range(len(coords)):
            if coords[j][0] == xx and coords[j][1] == yy:
                c = True
                break
        if c:
            print("$", end='')
        else:
            print(chr(ord('A') + grid[yy * max_x + xx]), end='')
    print()

largestFiniteSize = 0
largestFiniteIdx = 0
coverage = []
for i in range(len(coords)):
    coverage.append([0, i])

for yy in range(max_y):
    for xx in range(max_x):
        coverage[grid[yy * max_x + xx]][0] += 1

coverage = sorted(coverage, reverse=True)

# print(coverage, "largestFiniteSize:", largestFiniteSize, "largestFiniteIdx:", largestFiniteIdx)

print(coverage[0][0], chr(ord('A') + coverage[0][1]), coverage)

for i in range(len(coverage)):
    onEdge = False
    for yy in range(max_y):
        for xx in range(max_x):
            if grid[yy * max_x + xx] == coverage[i][1]:
                if xx <= 0 or xx > max_x - 1 or \
                   yy <= 0 or yy > max_y - 1:
                    onEdge = True
                    break
        if onEdge:
            break
    if not onEdge:
        print(chr(ord('A') + coverage[i][1]), coverage[i])

