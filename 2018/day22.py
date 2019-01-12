import heapq

f = open("day22.in").readlines()

depth = int(f[0].split(':')[1])
tx, ty = map(int, f[1].split(':')[1].split(','))

# depth = 510
# tx, ty = (10, 10)

dp = [[None for _ in range(ty + 50)] for _ in range(tx + 1000)]


def el(x, y):
    if dp[x][y] is not None:
        return dp[x][y]
    gi = None
    if (x, y) == (tx, ty):
        gi = 0
    elif y == 0:
        gi = x * 16807
    elif x == 0:
        gi = y * 48271
    else:
        gi = el(x - 1, y) * el(x, y - 1)

    dp[x][y] = (gi + depth) % 20183
    return int(dp[x][y])


def risk(x, y):
    return el(x, y) % 3


print(f"p1: {sum(el(x, y) % 3 for x in range(tx + 1) for y in range(ty + 1))}")

# # Region =>            Rocky,   wet,    narrow
# # Tool not allowed => Neither, torch, climbing gear

queue = [(0, 0, 0, 1)]  # Dist, x, y, tool not allowed
best = dict()  # (x, y, tool not allowed): dist
target = (tx, ty, 1)
while queue:
    dist, x, y, toolNotAllowed = heapq.heappop(queue)
    bkey = (x, y, toolNotAllowed)
    if bkey in best and best[bkey] <= dist:
        continue
    best[bkey] = dist
    if bkey == target:
        print(f"p2: {dist}")
        break
    for i in range(3):
        if i != toolNotAllowed and i != risk(x, y):
            heapq.heappush(queue, (dist + 7, x, y, i))

    for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        nx = x + dx
        ny = y + dy
        if nx < 0 or ny < 0 or risk(nx, ny) == toolNotAllowed:
            continue
        heapq.heappush(queue, (dist + 1, nx, ny, toolNotAllowed))
