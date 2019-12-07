
def get_inputs():
    return [int(y) for y in open("day04.in").readlines()[0].split('-')]


def meets_criteria(num, p2):
    digits = [ord(x) for x in str(num)]
    for idx, d in enumerate(digits):
        for i in range(0, idx):
            if d < digits[i]:
                return False
    has_double = False
    i = 0
    while i < len(digits) - 1:
        if digits[i] == digits[i + 1]:
            if p2 and has_double:
                return False
            has_double = True
            if p2:
                if i + 2 < len(digits):
                    if digits[i] == digits[i + 2]:
                        has_double = False  # Triple or more
                        count = 2 if (i + 1) == (len(digits) - 1) else len(digits) - i
                        for j in range(i, len(digits)):
                            if digits[j] != digits[i]:
                                count = j - i
                                break
                        i += count
                        continue
                    else:
                        break
                else:
                    break  # End of the num with 2
            if not p2:
                break
        i += 1
    if not has_double:
        return False
    # print(num)
    return True


def get_count(p2):
    inputs = get_inputs()
    count = 0
    for i in range(inputs[0], inputs[1]+1):
        if meets_criteria(i, p2):
            count += 1
    return count


def part1():
    return get_count(False)


def part2():
    return get_count(True)
