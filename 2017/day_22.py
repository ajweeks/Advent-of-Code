
import re
import sys

f = open("day_22_input.txt")
nodesStr = f.read()

# nodesStr = """..#
# #..
# ..."""

minPos = int(-len(nodesStr.split('\n')[0]) / 2)
maxPos = -minPos

nodesStr = re.sub('\n', '', nodesStr)

nodes = [0] * (pow(maxPos - minPos + 1, 2))
i = 0
for c in nodesStr:
    nodes[i] = 2 if (c == '#') else 0
    i = i + 1

cur_node_x = 0
cur_node_y = 0
cur_dir = 0 # 0, 1, 2, 3  =>  N, E, S, W

#  0 = clean, 1 = weak, 2 = infected, 3 = flagged


def print_board():
    for y in range(maxPos - minPos + 1):
        for x in range(maxPos - minPos + 1):
            printIdx = x + y * (maxPos - minPos + 1)
            if (cur_node_x - minPos) == x and (cur_node_y - minPos) == y:
                sys.stdout.write('[.]' if nodes[printIdx] == 0 else '[W]' if nodes[printIdx] == 1 else '[#]' if nodes[printIdx] == 2 else '[F]')
            else:
                sys.stdout.write(' . ' if nodes[printIdx] == 0 else ' W ' if nodes[printIdx] == 1 else ' # ' if nodes[printIdx] == 2 else ' F ')
        sys.stdout.write('\n')
    sys.stdout.write('\n')


def turn_left():
    global cur_dir
    cur_dir -= 1
    if cur_dir < 0:
        cur_dir = 3


def turn_right():
    global cur_dir
    cur_dir += 1
    if cur_dir == 4:
        cur_dir = 0


def turn_around():
    global cur_dir
    cur_dir += 2
    if cur_dir >= 4:
        cur_dir -= 4


burstCount = 10000000
infectionCount = 0
for burstIdx in range(burstCount):
    if burstIdx % 10000 == 0:
        print(burstIdx)

    curIdx = (cur_node_x - minPos) + (cur_node_y - minPos) * (maxPos - minPos + 1)
    if nodes[curIdx] == 0:  # clean
        turn_left()
        nodes[curIdx] = 1
    elif nodes[curIdx] == 1:  # weakened
        infectionCount += 1
        nodes[curIdx] = 2
    elif nodes[curIdx] == 2:  # infected
        turn_right()
        nodes[curIdx] = 3
    elif nodes[curIdx] == 3:  # flagged
        turn_around()
        nodes[curIdx] = 0

    if cur_dir == 0:
        cur_node_y -= 1
    elif cur_dir == 1:
        cur_node_x += 1
    elif cur_dir == 2:
        cur_node_y += 1
    elif cur_dir == 3:
        cur_node_x -= 1

    newMinPos = min(minPos, min(cur_node_x, cur_node_y))
    newMaxPos = max(maxPos, max(cur_node_x, cur_node_y))

    if newMinPos != minPos or newMaxPos != maxPos:
        pMinPos = minPos
        pMaxPos = maxPos
        minPos = minPos * 2
        maxPos = maxPos * 2

        dDimHalf = int(((maxPos-minPos+1) - (pMaxPos-pMinPos+1)) / 2)

        newNodesDim = (maxPos - minPos + 1)
        newNodes = [0] * (newNodesDim * newNodesDim)

        for y in range(maxPos - minPos + 1):
            for x in range(maxPos - minPos + 1):
                idx = x + y * (maxPos - minPos + 1)
                mappedX = (x - dDimHalf)
                mappedY = (y - dDimHalf)
                oldIdx = mappedX + mappedY * (pMaxPos - pMinPos + 1)
                if 0 <= mappedX < int((pMaxPos-pMinPos+1)) and 0 <= mappedY < int((pMaxPos-pMinPos+1)):
                    newNodes[idx] = nodes[oldIdx]

        nodes = newNodes

    # print_board()

print(f"After {burstCount} bursts, {infectionCount} caused an infection")
