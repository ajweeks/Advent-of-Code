from collections import defaultdict

line = open("day20.in").read()

# line = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"

x, y = 0, 0
positions = []
branches_deep = 0
distances = defaultdict(int)
px, py = x, y
for d in line[1:-1]:
    if d == '(':
        positions.append((x, y))
    elif d == '|':
        x, y = positions[-1]
    elif d == ')':
        x, y = positions.pop()
    else:
        if d == 'N':
            y -= 1
        elif d == 'E':
            x += 1
        elif d == 'S':
            y += 1
        elif d == 'W':
            x -= 1

        if distances[(x, y)] == 0:
            distances[(x, y)] = distances[(px, py)] + 1
        else:
            distances[(x, y)] = min(distances[(x, y)], distances[(px, py)])
    px, py = x, y

print(max(distances.values()))
print(len([x for x in distances.values() if x >= 1000]))
