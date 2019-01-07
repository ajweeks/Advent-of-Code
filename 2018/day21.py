lines = open("day21.in").readlines()

r = [0, 0, 0, 0, 0, 0]


def op_to_idx(op_str):
    if 'add' in op_str:
        if op_str[3] == 'r':
            return 0  # addr
        else:
            return 1  # addi
    if 'mul' in op_str:
        if op_str[3] == 'r':
            return 2  # mulr
        else:
            return 3  # muli
    if 'ban' in op_str:
        if op_str[3] == 'r':
            return 4  # banr
        else:
            return 5  # bani
    if 'bor' in op_str:
        if op_str[3] == 'r':
            return 6  # borr
        else:
            return 7  # bori
    if 'set' in op_str:
        if op_str[3] == 'r':
            return 8  # setr
        else:
            return 9  # seti
    if 'gt' in op_str:
        if op_str[2:] == 'ir':
            return 10  # gtir
        elif op_str[2:] == 'ri':
            return 11  # gtri
        else:
            return 12  # gtrr
    if 'eq' in op_str:
        if op_str[2:] == 'ir':
            return 13  # eqir
        elif op_str[2:] == 'ri':
            return 14  # eqri
        else:
            return 15  # eqrr
    return -1


def apply_op(op_idx, in_0, in_1, out_0):
    if op_idx == 0:  # addr
        r[out_0] = r[in_0] + r[in_1]
    elif op_idx == 1:  # addi
        r[out_0] = r[in_0] + in_1
    elif op_idx == 2:  # mulr
        r[out_0] = r[in_0] * r[in_1]
    elif op_idx == 3:  # muli
        r[out_0] = r[in_0] * in_1
    elif op_idx == 4:  # banr
        r[out_0] = r[in_0] & r[in_1]
    elif op_idx == 5:  # bani
        r[out_0] = r[in_0] & in_1
    elif op_idx == 6:  # borr
        r[out_0] = r[in_0] | r[in_1]
    elif op_idx == 7:  # bori
        r[out_0] = r[in_0] | in_1
    elif op_idx == 8:  # setr
        r[out_0] = r[in_0]
    elif op_idx == 9:  # seti
        r[out_0] = in_0
    elif op_idx == 10:  # gtir
        r[out_0] = 1 if (in_0 > r[in_1]) else 0
    elif op_idx == 11:  # gtri
        r[out_0] = 1 if (r[in_0] > in_1) else 0
    elif op_idx == 12:  # gtrr
        r[out_0] = 1 if (r[in_0] > r[in_1]) else 0
    elif op_idx == 13:  # eqir
        r[out_0] = 1 if (in_0 == r[in_1]) else 0
    elif op_idx == 14:  # eqri
        r[out_0] = 1 if (r[in_0] == in_1) else 0
    elif op_idx == 15:  # eqrr
        r[out_0] = 1 if (r[in_0] == r[in_1]) else 0


instructions = []
for line in range(1, len(lines)):
    op = op_to_idx(lines[line].split(' ')[0])
    a, b, c = lines[line].split(' ')[1:]
    instructions.append([op, int(a), int(b), int(c)])

ip_reg_idx = int(lines[0].split(' ')[1])

# s = set([])
# ip = 0
# i = 0
# while ip < len(instructions):
#     inst = instructions[ip]
#     r[ip_reg_idx] = ip
#     apply_op(inst[0], inst[1], inst[2], inst[3])
#     ip = r[ip_reg_idx]
#     ip += 1
#     if ip == 28:
#         s.add(r[2])
#         print(f"s: {s}")
#     i += 1
#     # print(i, r)


s = set([])
smallest_i = 99999999
p1 = -1
p2 = -1
last_r2 = -1
while True:
    r = [0] * 6
    while True:
        # 6-7
        r[5] = r[2] | 65536
        r[2] = 4843319
        while True:
            # 8-12
            r[2] += r[5] & 255
            r[2] &= 16777215
            r[2] = r[2] * 65899
            r[2] &= 16777215

            if len(s) > 0 and r[2] in s:
                p2 = last_r2  # Because python doesn't let you index into sets...
                break

            # 13-15
            if r[5] < 256:
                break  # GOTO 28

            # 18-27
            r[5] = int(r[5] / 256)
            # GOTO 8

        if p2 != -1:
            break

        # 28
        # if r[2] == r[0]:

        if len(s) == 0:
            p1 = r[2]
        last_r2 = r[2]
        s.add(r[2])

        # GOTO 6

    if p2 != -1:
        break

print(f"p1: {p1}, p2: {p2}")
