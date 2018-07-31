
import sys

f = open("day_25_input.txt")
instructionsStr = f.read()

# instructionsStr = """Begin in state A.
# Perform a diagnostic checksum after 6 steps.
#
# In state A:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state B.
#   If the current value is 1:
#     - Write the value 0.
#     - Move one slot to the left.
#     - Continue with state B.
#
# In state B:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the left.
#     - Continue with state A.
#   If the current value is 1:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state A."""


def resize_tape(new_size):
    global tape
    global cursor

    d_size = new_size - len(tape)
    assert(d_size % 2 == 0)

    new_tape = [0] * new_size

    for i in range(len(tape)):
        new_tape[i + int(d_size / 2)] = tape[i]

    tape = new_tape


def print_board():
    halfLen = int(len(tape) / 2)

    sys.stdout.write(chr(ord('A') + curStateIdx) + ' ')

    for c in range(len(tape)):
        if c == cursor + halfLen:
            sys.stdout.write(f'[{tape[c]}]')
        elif c == halfLen:
            sys.stdout.write(f'({tape[c]})')
        else:
            sys.stdout.write(f' {tape[c]} ')
    sys.stdout.write('\n')


startState = ord(instructionsStr.split('\n')[0][-2]) - ord('A')
stepsBeforeChecksum = int(instructionsStr.split('\n')[1].split(' ')[-2])
curStateIdx = startState

stateStrs = instructionsStr.split("In state")

states = []
sI = 1
while sI < len(stateStrs):
    lines = stateStrs[sI].split('\n')
    writeIf0 = int(lines[2][-2])
    moveIf0 = 1 if lines[3].split(' ')[-1] == "right." else -1
    nextStateIf0 = ord(lines[4][-2]) - ord('A')
    writeIf1 = int(lines[6][-2])
    moveIf1 = 1 if lines[7].split(' ')[-1] == "right." else -1
    nextStateIf1 = ord(lines[8][-2]) - ord('A')
    states.append([writeIf0, moveIf0, nextStateIf0, writeIf1, moveIf1, nextStateIf1])

    sI += 1

tape = [0, 0, 0, 0, 0, 0, 0, 0]
cursor = 0
for step in range(stepsBeforeChecksum):
    halfLen = int(len(tape) / 2)
    if cursor >= halfLen or cursor <= -halfLen:
        resize_tape(halfLen * 4)
    halfLen = int(len(tape) / 2)

    if step % 100000 == 0:
        print("{:.1f}%".format(step/stepsBeforeChecksum*100.0))
        # print_board()

    if tape[cursor + halfLen] == 0:
        tape[cursor + halfLen] = states[curStateIdx][0]
        cursor += states[curStateIdx][1]
        curStateIdx = states[curStateIdx][2]
    else:
        tape[cursor + halfLen] = states[curStateIdx][3]
        cursor += states[curStateIdx][4]
        curStateIdx = states[curStateIdx][5]

print_board()

print(sum(tape))

