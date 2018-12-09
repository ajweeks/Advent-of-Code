
from collections import deque, defaultdict
import time

inputstr = open("day09.in").read()

# inputstr = "9 players; last marble is worth 25 points"
# inputstr = "10 players; last marble is worth 1618 points"
# inputstr = "13 players; last marble is worth 7999 points"
# inputstr = "17 players; last marble is worth 1104 points"
# inputstr = "21 players; last marble is worth 6111 points"
# inputstr = "30 players; last marble is worth 5807 points"

player_count = int(inputstr.split(' ')[0])
final_marble_value = int(inputstr.split(' ')[6])

part2 = True
if part2:
    final_marble_value *= 100


marbles = deque([0])
player_scores = defaultdict(int)
global_start = time.time()
start = time.time()
for i in range(1, final_marble_value + 1):
    if i % 23 == 0:
        marbles.rotate(7)
        player_scores[i % player_count] += i + marbles.pop()
        marbles.rotate(-1)
    else:
        marbles.rotate(-1)
        marbles.append(i)
    if i % 100000 == 0:
        end = time.time()
        prcnt = format(i / final_marble_value * 100, ".2f")
        print(f"{prcnt}% {format(end-start, '.2f')}s, marble count: {len(marbles)}")
        start = end

global_end = time.time()
print(f"{player_count}, {final_marble_value}, {max(player_scores.values())}, {format(global_end-global_start, '.2f')}s")  # '\n', player_scores, '\n', marbles)
