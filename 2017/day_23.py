
f = open("day_23_input.txt")
instStr = f.read()


def reg_to_ind(c):
    return ord(c) - ord('a')


instructions = []
for instLine in instStr.split('\n'):
    instParts = instLine.split(' ')

    regIdx = 0 if instParts[0] == 'set' else 1 if instParts[0] == 'sub' else 2 if instParts[0] == 'mul' else 3
    p1Reg = not instParts[1].lstrip('-').isdigit()
    p1RegOrVal = 0
    if p1Reg:
        p1RegOrVal = reg_to_ind(instParts[1])
    else:
        p1RegOrVal = int(instParts[1])

    p2Reg = not instParts[2].lstrip('-').isdigit()
    p2RegOrVal = 0
    if p2Reg:
        p2RegOrVal = reg_to_ind(instParts[2])
    else:
        p2RegOrVal = int(instParts[2])

    instructions.append([regIdx, p1Reg, p1RegOrVal, p2Reg, p2RegOrVal])

registers = [0] * 8

part2 = True

if part2:
    b = 105700
    c = 122700


    def prime(num):
        i = 2
        while i * i <= num:
            if num % i == 0:
                return False
            i += 1
        return True


    result = 0
    for b in range(105700, c + 1, 17):
        if not prime(b):
            result += 1
    print(result)
else:
    mulCount = 0
    curInst = 0
    while 0 <= curInst < len(instructions):
        print(curInst, registers)

        inst = instructions[curInst]

        if inst[0] == 0:                    # set
            if inst[3]:
                registers[inst[2]] = registers[inst[4]]
            else:
                registers[inst[2]] = inst[4]
        elif inst[0] == 1:                  # sub
            if inst[3]:
                registers[inst[2]] -= registers[inst[4]]
            else:
                registers[inst[2]] -= inst[4]
        elif inst[0] == 2:                  # mul
            if inst[3]:
                registers[inst[2]] *= registers[inst[4]]
            else:
                registers[inst[2]] *= inst[4]
            mulCount += 1
        else:                               #jnz
            if inst[1]:
                if registers[inst[2]] != 0:
                    curInst += inst[4]
                    continue
            else:
                if inst[2] != 0:
                    curInst += inst[4]
                    continue

        curInst += 1

    print(f"Mul called {mulCount} times")
