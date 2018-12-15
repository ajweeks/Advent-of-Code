
lines = open("day13.in").readlines()

# lines = """/->-\\
# |   |  /----\\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/""".splitlines()

# lines = """/>-<\
# |   |
# | /<+-\\
# | | | v
# \>+</ |
#   |   ^
#   \<->/""".splitlines()

w = 0
for line in lines:
    w = max(w, len(line))
h = len(lines)
tracks = []
carts = []
for yy in range(h):
    line = lines[yy]
    for xx in range(w):
        c = line[xx] if xx < len(line) else ' '
        tracks.append(0 if c == ' '
                      else 1 if c == '|' or c == '^' or c == 'v'
                      else 2 if c == '-' or c == '>' or c == '<'
                      else 3 if c == '/'
                      else 4 if c == '\\'
                      else 5 if c == '+'
                      else 0)
        if c == '^':
            carts.append([xx, yy, 0, 0])
        elif c == '>':
            carts.append([xx, yy, 1, 0])
        elif c == 'v':
            carts.append([xx, yy, 2, 0])
        elif c == '<':
            carts.append([xx, yy, 3, 0])

first_collision = [-1, -1]


def print_board():
    for y in range(h):
        for x in range(w):
            if x == first_collision[0] and y == first_collision[1]:
                print('X', end='')
            else:
                cart = -1
                for cc in carts:
                    if cc[0] == x and cc[1] == y:
                        cart = cc[2]
                        break
                if cart != -1:
                    print('^' if cart == 0 else '>' if cart == 1 else 'v' if cart == 2 else '<', end='')
                else:
                    v = tracks[y * w + x]
                    print(' ' if v == 0 else '|' if v == 1 else '-' if v == 2 else '/' if v == 3 else '\\' if v == 4 else '+', end='')
        print()


def tile_in_dir(x, y, d):
    new_x = x
    new_y = y
    # TODO: Handle edges!(?)
    if d == 0:
        new_y = y - 1
    elif d == 1:
        new_x = x + 1
    elif d == 2:
        new_y = y + 1
    else:
        new_x = x - 1
    return new_x, new_y, tracks[new_y * w + new_x]


def collisions_occurred():
    for c1i in range(len(carts)):
        for c2i in range(c1i + 1, len(carts)):
            if carts[c1i][0] == carts[c2i][0] and carts[c1i][1] == carts[c2i][1]:
                return True, c1i, c2i
    return False, None, None


def rel_to_world_dir(rel, facing):
    if rel == 1:
        return facing
    else:
        return (facing + (rel - 1)) % 4


print_board()

last_cart = [-1, -1]

steps = 0
while True:
    collision = False
    carts = sorted(carts, key=lambda x: x[1] * w + x[0])
    i = 0
    while i < len(carts):
        c = carts[i]
        next_x, next_y, next_track = tile_in_dir(c[0], c[1], c[2])
        c[0] = next_x
        c[1] = next_y
        if next_track == 1 or next_track == 2:  # | or -
            pass
        elif next_track == 3:  # /
            c[2] = 1 if c[2] == 0 else 0 if c[2] == 1 else 3 if c[2] == 2 else 2
        elif next_track == 4:  # \
            c[2] = 3 if c[2] == 0 else 2 if c[2] == 1 else 1 if c[2] == 2 else 0
        elif next_track == 5:  # +
            rel_dir = (c[3] % 3)
            c[2] = rel_to_world_dir(rel_dir, c[2])
            c[3] += 1
        else:
            assert False

        collisionOccurred, c1, c2 = collisions_occurred()
        if collisionOccurred:
            collision = True
            if first_collision[0] == -1:
                first_collision = [next_x, next_y]

            carts.remove(carts[max(c1, c2)])
            carts.remove(carts[min(c1, c2)])
            if min(c2, c1) < i:
                i -= 1

            print(f"Collision at {next_x},{next_y}! carts left: {len(carts)} steps: {steps}")
        else:
            i += 1

    if len(carts) == 1:
        last_cart = carts[0]
        print(f"final remaining cart: {carts[0]}, steps: {steps}")
        break

    steps += 1

    # print_board()

# print_board()

print(f"\nfirst collision: {first_collision}")
print(f"last cart: {last_cart}")
