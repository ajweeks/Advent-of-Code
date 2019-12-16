import math


def get_input_str():
    return open("day16.in").readlines()[0]


def get_inputs(input_str):
    return int(input_str)


def decompose(num, length=-1):
    res = []
    i = 0
    while num != 0:
        res.append(num % 10)
        num //= 10
        i += 1
    res = list(reversed(res))
    if length != -1 and i < length:
        res.insert(0, 0)
    return res


def recompose(digits):
    num = 0
    for i, d in enumerate(reversed(digits)):
        num += d * 10 ** i
    return num


def recompose_top_n_digits(digits, s, n):
    num = 0
    i = 0
    for di in range(s, s + n):
        num += digits[di] * 10 ** (n - i - 1)
        i += 1
    return num


def part1():
    signal = get_inputs(get_input_str())
    # signal = 80871224585914546619083218645595

    num = signal
    digit_count = len(decompose(num))
    digits = decompose(num, digit_count)

    for phase_idx in range(100):
        for digit_idx in range(len(digits)):
            pattern_len = (digit_idx + 1) * 4
            new_digit = 0
            pattern_index = 1
            for digit in digits:
                p = int((pattern_index / pattern_len) * 4)
                new_digit += digit * [0, 1, 0, -1][p]
                pattern_index = (pattern_index + 1) % pattern_len
            digits[digit_idx] = (abs(new_digit) % 10)

    num = recompose_top_n_digits(digits, 0, 8)
    return num


def part2():
    signal = get_inputs(get_input_str())
    # signal = 2935109699940807407585447034323

    num = signal
    digit_count = len(decompose(num))
    digits = decompose(num, digit_count)
    msg_offset = recompose_top_n_digits(digits, 0, 7)
    required_len = (digit_count * 10000) - msg_offset
    num_copies = math.ceil(required_len / digit_count)
    digits = digits * num_copies

    digits = digits[-required_len:]

    for phase_idx in range(100):
        new_digit = 0
        for i in range(len(digits) - 1, -1, -1):
            new_digit += digits[i]
            digits[i] = (abs(new_digit) % 10)

    num = recompose_top_n_digits(digits, 0, 8)
    return num
