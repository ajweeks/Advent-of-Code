import sys

f = open("day_06_input.txt")
fileStr = f.read()

banks = [int(i) for i in fileStr.split()]

# banks = [0, 2, 7, 0]  # Test input


def fullest_bank():
    fullest = -1
    max_value = -sys.maxsize
    for i in range(len(banks)):
        if banks[i] > max_value:
            max_value = banks[i]
            fullest = i
    return fullest


def detect_infinite_loop(part2):
    seen_states = [banks.copy()]
    cycles = 0
    while True:
        cycles += 1
        fullest_index = fullest_bank()
        distribute = banks[fullest_index]
        banks[fullest_index] = 0
        i = (fullest_index + 1) % len(banks)
        while distribute > 0:
            banks[i] += 1
            distribute -= 1
            i = (i + 1) % len(banks)

        # print(seen_states)
        if banks in seen_states:
            if part2:
                for i in range(len(seen_states)):
                    if seen_states[i] == banks:
                        return cycles - i
            else:
                break

        seen_states.append(banks.copy())
    return cycles


part_2 = True
print(detect_infinite_loop(part_2))
