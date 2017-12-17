
f = open("day_16_input.txt")
fileStr = f.read()

instructions_str = fileStr.split(',')

# instructions_str = ["s1", "x3/4", "pe/b"]


def main():
    part_1 = False
    dance_count = 1 if part_1 else 1000000000

    programs = []
    for i in range(16):
        programs.append(chr(ord('a') + i))
    print(''.join(programs))

    instructions = []
    for inst in instructions_str:
        inst_type = 0 if inst[0] == 's' else 1 if inst[0] == 'x' else 2
        one = 0
        if inst_type == 0:
            one = int(inst[1:])
        if inst_type == 1:
            one = int(inst.split('/')[0][1:])
        else:
            one = inst.split('/')[0][1:].lower()

        two = 0
        if inst_type == 0:
            two = 0
        elif inst_type == 1:
            two = int(inst.split('/')[1])
        else:
            two = inst.split('/')[1].lower()

        instructions.append([inst_type, one, two])

    seen_states = []
    for dance in range(dance_count):
        s = ''.join(programs)
        if s in seen_states:
            print(seen_states[dance_count % dance], dance)
            return
        seen_states.append(s)

        for inst in instructions:
            if inst[0] == 0:
                count = int(inst[1])
                programs = list(programs[-count:]) + list(programs[0:len(programs) - count])
            elif inst[0] == 1:
                first = int(inst[1])
                second = int(inst[2])
                programs[first], programs[second] = programs[second], programs[first]
            elif inst[0] == 2:
                first = programs.index(inst[1])
                second = programs.index(inst[2])
                programs[first], programs[second] = programs[second], programs[first]

    print(''.join(programs))


main()
