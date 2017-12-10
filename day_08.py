
import sys

f = open("day_08_input.txt")
fileStr = f.read()

# fileStr = "b inc 5 if a > 1\n\
# a inc 1 if b < 5\n\
# c dec -10 if a >= 1\n\
# c inc -20 if c == 10"

highest_val = -sys.maxsize

registers = []

for line in fileStr.splitlines():
    if line.split()[0] not in [r[0] for r in registers]:
        registers.append([line.split()[0], 0])

print(registers)


def register_index(name):
    for i in range(len(registers)):
        if registers[i][0] == name:
            return i


for line in fileStr.splitlines():
    line_parts = line.split()
    reg_index = register_index(line_parts[0])
    inc = 1 if line_parts[1] == 'inc' else -1
    amount = int(line_parts[2])
    cond_reg_index = register_index(line_parts[4])
    cond_e = line_parts[5]
    cond_rval = int(line_parts[6])

    passed = False

    if cond_e == '==':
        passed = registers[cond_reg_index][1] == cond_rval
    elif cond_e == '!=':
        passed = registers[cond_reg_index][1] != cond_rval
    elif cond_e == '<':
        passed = registers[cond_reg_index][1] < cond_rval
    elif cond_e == '<=':
        passed = registers[cond_reg_index][1] <= cond_rval
    elif cond_e == '>':
        passed = registers[cond_reg_index][1] > cond_rval
    elif cond_e == '>=':
        passed = registers[cond_reg_index][1] >= cond_rval
    else:
        print("!!!Unhandled condition:", cond_e, "!!!")

    if passed:
        registers[reg_index][1] = registers[reg_index][1] + inc * amount
        highest_val = max(highest_val, registers[reg_index][1])

    # print('inc' if inc else 'dec', "reg", reg_index, "by", amount, "if", cond_reg_index, cond_e, cond_rval, passed)
    print(registers)

print(max([i[1] for i in registers]))
print(highest_val)