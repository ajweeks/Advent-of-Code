lines = open("day16.in").readlines()

tests = []
tests_rough = ''.join(lines).split('Before:')[1:]
test_programs_rough = [x for x in tests_rough[-1][tests_rough[-1].rfind(']')+1:].splitlines() if len(x) > 0]
tests_rough[-1] = tests_rough[-1][0:tests_rough[-1].rfind(']')] + ']'
for t in tests_rough:
    reg_bef = [int(x) for x in t.split(']')[0][2:].split(',')]
    inst = [int(x) for x in t.split(']')[1].split('A')[0].split(' ')]
    reg_aft = [int(x) for x in t.split('After:')[1][3:].split(']')[0].split(',')]
    tests.append([reg_bef, inst, reg_aft])

test_programs = []
for line in test_programs_rough:
    test_programs.append([int(x) for x in line.split(' ')])

# tests = [[[3, 2, 1, 1], [9, 2, 1, 2], [3, 2, 2, 1]]]


def code_to_idx(code_str):
    if 'add' in code_str:
        if code_str[3] == 'r':
            return 0  # addr
        else:
            return 1  # addi
    if 'mul' in code_str:
        if code_str[3] == 'r':
            return 2  # mulr
        else:
            return 3  # muli
    if 'ban' in code_str:
        if code_str[3] == 'r':
            return 4  # banr
        else:
            return 5  # bani
    if 'bor' in code_str:
        if code_str[3] == 'r':
            return 6  # borr
        else:
            return 7  # bori
    if 'set' in code_str:
        if code_str[3] == 'r':
            return 8  # setr
        else:
            return 9  # seti
    if 'gt' in code_str:
        if code_str[3:] == 'ir':
            return 10  # gtir
        elif code_str[3:] == 'ri':
            return 11  # gtri
        else:
            return 12  # gtrr
    if 'eq' in code_str:
        if code_str[3:] == 'ir':
            return 13  # eqir
        elif code_str[3:] == 'ri':
            return 14  # eqri
        else:
            return 15  # eqrr
    return -1


def apply_op(op_idx, in_0, in_1, out_0, registers):
    if op_idx == 0:  # addr
        registers[out_0] = registers[in_0] + registers[in_1]
    elif op_idx == 1:  # addi
        registers[out_0] = registers[in_0] + in_1
    elif op_idx == 2:  # mulr
        registers[out_0] = registers[in_0] * registers[in_1]
    elif op_idx == 3:  # muli
        registers[out_0] = registers[in_0] * in_1
    elif op_idx == 4:  # banr
        registers[out_0] = registers[in_0] & registers[in_1]
    elif op_idx == 5:  # bani
        registers[out_0] = registers[in_0] & in_1
    elif op_idx == 6:  # borr
        registers[out_0] = registers[in_0] | registers[in_1]
    elif op_idx == 7:  # bori
        registers[out_0] = registers[in_0] | in_1
    elif op_idx == 8:  # setr
        registers[out_0] = registers[in_0]
    elif op_idx == 9:  # seti
        registers[out_0] = in_0
    elif op_idx == 10:  # gtir
        registers[out_0] = 1 if in_0 > registers[in_1] else 0
    elif op_idx == 11:  # gtri
        registers[out_0] = 1 if registers[in_0] > in_1 else 0
    elif op_idx == 12:  # gtrr
        registers[out_0] = 1 if registers[in_0] > registers[in_1] else 0
    elif op_idx == 13:  # eqir
        registers[out_0] = 1 if in_0 == registers[in_1] else 0
    elif op_idx == 14:  # eqri
        registers[out_0] = 1 if registers[in_0] == in_1 else 0
    elif op_idx == 15:  # eqrr
        registers[out_0] = 1 if registers[in_0] == registers[in_1] else 0


op_idx_mapping = dict()

num_ops_trip_ambig = 0
added_mapping = True
for t in tests:
    op_idx = t[1][0]
    possible_op_count = 0
    possible_unmapped_op_count = 0
    possible_op_idcs = []
    for i in range(16):
        registers = t[0].copy()
        apply_op(i, t[1][1], t[1][2], t[1][3], registers)
        if registers == t[2]:
            possible_op_count += 1

        if registers == t[2] and i not in op_idx_mapping.values():
            possible_unmapped_op_count += 1
            possible_op_idcs.append(i)
    if possible_op_count >= 3:
        num_ops_trip_ambig += 1
    if possible_unmapped_op_count == 1:
        op_idx_mapping[op_idx] = possible_op_idcs[0]

print(f"{num_ops_trip_ambig}/{len(tests)}")
# print(len(op_idx_mapping), op_idx_mapping)

registers = [0] * 4
for t in test_programs:
    apply_op(op_idx_mapping[t[0]], t[1], t[2], t[3], registers)

print(registers[0], registers)
