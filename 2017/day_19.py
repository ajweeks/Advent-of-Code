
import sys

f = open("day_19_input.txt")
maze_u = f.read()

# maze = """     |
#      |  +--+
#      A  |  C
#  F---|----E|--+
#      |  |  |  D
#      +B-+  +--+
#                 """

maze_w = 0
for line in maze_u.split('\n'):
    if len(line) > maze_w:
        maze_w = len(line)
maze_h = len(maze_u.split('\n'))
print(maze_w, "x", maze_h)

sys.stdout.write('  ')
for s in range(maze_w):
    sys.stdout.write(str(s % 10))
sys.stdout.write('\n')

for idx, line in enumerate(maze_u.split('\n')):
    print(idx, line)
print()

maze = ""

for line in maze_u.split('\n'):
    maze += ''.join([c for c in line if c != '\n'])
    maze += " " * (maze_w - len(line))

curx, cury = 0, 0
dx = 0
dy = 1
steps = 0

for x in range(maze_w):
    if not maze[x].isspace():
        curx = x
        break

letters = ""

print("starting at:", curx, cury)

while 1:
    nxtx = curx + dx
    nxty = cury + dy
    steps += abs(dx) + abs(dy)
    nxt = maze[nxtx + nxty * maze_w]
    #print("next:", nxtx, nxty, nxt)
    curx = nxtx
    cury = nxty

    if nxt == ' ':
        print("found end of the line at: ", curx, cury)
        break
    elif nxt == '|':
        continue
    elif nxt == '-':
        continue
    elif nxt == '+':
        acrossx = curx + dx
        acrossy = cury + dy
        across = maze[acrossx + acrossy * maze_w]

        can_go_straight = across != ' ' or (dx != 0 and across == '-') or (dy != 0 and across == '|')
        if can_go_straight:
            curx += dx
            cury += dy
            continue
        else: # can't go across
            if dx == 0: # moving vertically
                rx = curx + 1
                i = rx + cury * maze_w
                r = maze[i] if (0 <= i < len(maze)) else '!'
                lx = curx - 1
                i = lx + cury * maze_w
                l = maze[i] if (0 <= i < len(maze)) else '!'

                if r != ' ':
                    dx = 1
                    dy = 0
                    #curx = rx
                    continue
                elif l != ' ':
                    dx = -1
                    dy = 0
                    #curx = lx
                    continue
            else: # moving horizontally
                uy = cury - 1
                i = curx + uy * maze_w
                u = maze[i] if (0 <= i < len(maze)) else '!'
                dy = cury + 1
                i = curx + dy * maze_w
                d = maze[i] if (0 <= i < len(maze)) else '!'

                if u != ' ':
                    dx = 0
                    dy = -1
                    #curx = uy
                    continue
                elif d != ' ':
                    dx = 0
                    dy = 1
                    #cury = dy
                    continue
    else:
        # should be a letter
        letters += nxt


print("letters:", letters)
print("steps:", steps)
