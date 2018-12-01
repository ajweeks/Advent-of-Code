
f = open("day_11_input.txt")
fileStr = f.read()

print(fileStr)


def dist(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])) / 2


def move(dirs):
    res = [0, 0, 0]
    max_dist = 0
    for dir in dirs.split(','):
        if dir == 'ne':
            res[0] += 1
            res[2] -= 1
        if dir == 'nw':
            res[0] -= 1
            res[1] += 1
        if dir == 'n':
            res[1] += 1
            res[2] -= 1
        if dir == 'se':
            res[0] += 1
            res[1] -= 1
        if dir == 'sw':
            res[0] -= 1
            res[2] += 1
        if dir == 's':
            res[1] -= 1
            res[2] += 1

        d = dist([0, 0, 0], res)
        max_dist = max(d, max_dist)
    return res, max_dist


end, max_d = move(fileStr)
print(dist([0, 0, 0], end), max_d)
