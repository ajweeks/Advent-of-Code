
f = open("day_05_input.txt")
fileStr = f.read()

# fileStr = "0\n3\n0\n1\n-3"  # Test input


def execute_instructions(part2):
    steps = 0
    index = 0
    p_index = index

    instructions = [int(numeric_string) for numeric_string in fileStr.splitlines()]

    while True:
        if index >= len(instructions) or index < 0:
            return steps

        offset = instructions[index]
        index += offset
        if part2 and offset >= 3:
            instructions[p_index] -= 1
        else:
            instructions[p_index] += 1
        # print(instructions)
        p_index = index
        steps += 1


part_2 = True
print(execute_instructions(part_2))
