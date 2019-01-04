lines = [a.strip() for a in open("day19.in").readlines()]


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
        if op_str[3:] == 'ir':
            return 10  # gtir
        elif op_str[3:] == 'ri':
            return 11  # gtri
        else:
            return 12  # gtrr
    if 'eq' in op_str:
        if op_str[3:] == 'ir':
            return 13  # eqir
        elif op_str[3:] == 'ri':
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
        r[out_0] = 1 if in_0 > r[in_1] else 0
    elif op_idx == 11:  # gtri
        r[out_0] = 1 if r[in_0] > in_1 else 0
    elif op_idx == 12:  # gtrr
        r[out_0] = 1 if r[in_0] > r[in_1] else 0
    elif op_idx == 13:  # eqir
        r[out_0] = 1 if in_0 == r[in_1] else 0
    elif op_idx == 14:  # eqri
        r[out_0] = 1 if r[in_0] == in_1 else 0
    elif op_idx == 15:  # eqrr
        r[out_0] = 1 if r[in_0] == r[in_1] else 0


ip_reg_idx = int(lines[0].split(' ')[1])

instructions = []
for line in range(1, len(lines)):
    op = op_to_idx(lines[line].split(' ')[0])
    a, b, c = lines[line].split(' ')[1:]
    instructions.append([op, int(a), int(b), int(c)])

# ip = 0
# i = 0
# while ip < len(instructions):
#     inst = instructions[ip]
#     r[ip_reg_idx] = ip
#     apply_op(inst[0], inst[1], inst[2], inst[3])
#     ip = r[ip_reg_idx]
#     ip += 1
#     i += 1
#     if i % 1000000 == 0:
#         print(i, r)


for p in range(0, 2):
    r = [p, 0, 0, 0, 0, 0]

    halted = False
    while not halted:
        while not halted:
            # 17-20
            r[2] = 209 * (r[2] + 2) * (r[2] + 2)
            # 21-23
            r[1] = 17 + 22 * (r[1] + 3)
            # 24
            r[2] += r[1]
            # if r[0] == 0:
            #     break

            if p == 1:
                # 27-32
                r[1] = 10550400
                # 33
                r[2] += r[1]
                # 34
                r[0] = 0

            # 1
            r[4] = 1
            # loop 1 (3-11)
            # Store sum of factors of r[2] in r[0]
            for i in range(1, r[2]+1):
                if r[2] % i == 0:
                    r[0] += i

            r[4] = r[2]
            # 16
            print(f"p{p}: {r[0]}")
            halted = True
