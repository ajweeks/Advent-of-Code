
f = open("day_18_input.txt")
instructionsStr = f.read()

# instructionsStr = """snd 1
# snd 2
# snd p
# rcv a
# rcv b
# rcv c
# rcv d"""

instructions = instructionsStr.split('\n')

registers = [[0] * 26, [0] * 26]

# Program IDs
registers[0][ord('p') - ord('a')] = 0
registers[1][ord('p') - ord('a')] = 1

rcvQueues = [[], []]

curProgramIdx = 0
instIdxs = [0, 0]
programStalled = [False, False]

p1SndCount = 0

while True:
    while 0 <= instIdxs[curProgramIdx] < len(instructions):
        parts = instructions[instIdxs[curProgramIdx]].split(' ')

        if parts[0] == 'jgz':
            cond = 0
            if parts[1].strip('-').isdigit():
                cond = int(parts[1])
            else:
                cond = registers[curProgramIdx][ord(parts[1]) - ord('a')]

            val = 0
            if len(parts) > 2 and parts[2].strip('-').isdigit():
                val = int(parts[2])
            else:
                val = registers[curProgramIdx][ord(parts[2]) - ord('a')]

            if cond > 0:
                instIdxs[curProgramIdx] += val
            else:
                instIdxs[curProgramIdx] += 1
        else:
            reg1Idx = ord(parts[1]) - ord('a')

            if parts[0] == 'rcv':
                if len(rcvQueues[curProgramIdx]) == 0:
                    programStalled[curProgramIdx] = True
                    break
                else:
                    val = rcvQueues[curProgramIdx].pop(0)

                    print(f"recovered sound {val} for reg {parts[1]} in program {curProgramIdx}")
                    registers[curProgramIdx][ord(parts[1]) - ord('a')] = val
                    # exit()
            else:
                val = 0
                if len(parts) > 2:
                    if parts[2].strip('-').isdigit():
                        val = int(parts[2])
                    else:
                        val = registers[curProgramIdx][ord(parts[2]) - ord('a')]
                else:
                    if parts[1].strip('-').isdigit():
                        val = int(parts[1])
                    else:
                        val = registers[curProgramIdx][ord(parts[1]) - ord('a')]

                if parts[0] == 'snd':
                    rcvQueues[1-curProgramIdx].append(val)
                    programStalled[1-curProgramIdx] = False

                    if curProgramIdx == 1:
                        p1SndCount += 1
                elif parts[0] == 'set':
                    registers[curProgramIdx][reg1Idx] = val
                elif parts[0] == 'add':
                    registers[curProgramIdx][reg1Idx] += val
                elif parts[0] == 'mul':
                    registers[curProgramIdx][reg1Idx] *= val
                elif parts[0] == 'mod':
                    registers[curProgramIdx][reg1Idx] %= val
            instIdxs[curProgramIdx] += 1

        print(curProgramIdx, registers[curProgramIdx], parts, instIdxs[curProgramIdx], rcvQueues)

    if programStalled[0] and programStalled[1]:
        print("Deadlock")
        break

    curProgramIdx = 1 - curProgramIdx


print(f"p1 send count: {p1SndCount}")
