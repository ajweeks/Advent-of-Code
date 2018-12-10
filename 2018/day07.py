
lines = open("day07.in").read().split('\n')

# lines = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.""".split('\n')

test = False

#     Letter idx (A=0), available, traversed, requirements
orig_instructions = []
for i in range(6 if test else 26):
    orig_instructions.append([i, True, False, []])

i = 0
for line in lines:
    parts = line.split(' ')
    i = ord(parts[7]) - ord('A')
    orig_instructions[i][1] = False
    orig_instructions[i][3].append(ord(parts[1]) - ord('A'))

orig_instructions = sorted(orig_instructions)
print(orig_instructions)

instructions1 = [c.copy() for c in orig_instructions]
instructions2 = [c.copy() for c in orig_instructions]

order = []
completedIdx = 0
reordered = True
while reordered:
    reordered = False
    available = []
    for inst in instructions1:
        if inst[0] not in order:
            if inst[1]:
                available.append(inst)
    available = sorted(available)
    print(available)
    if len(available) > 0:
        available[0][2] = True
        order.append(available[0][0])
        for i in range(len(instructions1)):
            if available[0][0] in instructions1[i][3]:
                other_parents_traversed = True
                for par_idx in instructions1[i][3]:
                    if available[0][0] != par_idx and not instructions1[par_idx][2]:
                        other_parents_traversed = False
                        break
                if other_parents_traversed:
                    instructions1[i][1] = True
        reordered = True

orderStr = ""
for o in order:
    orderStr = orderStr + chr((ord('A') + o))

print(orderStr, order)

workers = []
for i in range(2 if test else 5):
    # Step index, seconds remaining
    workers.append([0, 0])

print("S 1 2 3 4 5 ORDER")

order_in_prog = []
order = []
seconds = 0
inst_left = True
while inst_left:
    inst_left = False
    workers_available = []
    for w in range(len(workers)):
        if workers[w][1] == 0:
            workers_available.append(w)
    steps_available = []
    for inst in instructions2:
        if inst[0] not in order_in_prog:
            if inst[1]:
                steps_available.append(inst)
    steps_available = sorted(steps_available)
    while len(workers_available) > 0 and len(steps_available) > 0:
        inst_left = True
        order_in_prog.append(steps_available[0][0])
        workers[workers_available[0]][0] = steps_available[0][0]
        workers[workers_available[0]][1] = (steps_available[0][0] + 1 + 60)
        workers_available.pop(0)
        steps_available.pop(0)

    print(str(seconds) + ' ', end='')
    for w in range(len(workers)):
        if workers[w][1] > 0:
            print(chr(ord('A') + workers[w][0]) + ' ', end='')
        else:
            print('. ', end='')
    for o in order:
        print(chr(ord('A') + o), end='')
    print()

    for w in range(len(workers)):
        if workers[w][1] > 0:
            inst_left = True
            workers[w][1] -= 1
            if workers[w][1] == 0:
                instructions2[workers[w][0]][2] = True
                order.append(workers[w][0])
                for i in range(len(instructions2)):
                    if instructions2[workers[w][0]][0] in instructions2[i][3]:
                        other_parents_traversed = True
                        for par_idx in instructions2[i][3]:
                            if instructions2[workers[w][0]][0] != par_idx and not instructions2[par_idx][2]:
                                other_parents_traversed = False
                                break
                        if other_parents_traversed:
                            instructions2[i][1] = True
                workers[w][0] = -1

    seconds += 1

for o in order:
    if o not in [x[0] for x in workers]:
        print(chr(ord('A') + o), end='')
print()
print(seconds - 1)
