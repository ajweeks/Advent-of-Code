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
    inputs = get_inputs(get_input_str())
    # inputs = 80871224585914546619083218645595

    num = inputs
    digit_count = len(decompose(num))
    digits = decompose(num, digit_count)

    for phase_idx in range(100):
        for digit_idx in range(len(digits)):
            pattern = [0] * (digit_idx+1) + [1] * (digit_idx+1) + [0] * (digit_idx+1) + [-1] * (digit_idx+1)
            new_digit = 0
            pattern_index = 1
            for digit in digits:
                new_digit += digit * pattern[pattern_index % len(pattern)]
                pattern_index += 1
            digits[digit_idx] = (abs(new_digit) % 10)

    num = recompose_top_n_digits(digits, 0, 8)
    return num


def FFT_slow(digits):
    N = len(digits)
    nlist = range(N)
    M = [math.exp(-2j * math.pi * k * n / N) for k in nlist]
    math.dot(M, x)

def part2():
    inputs = get_inputs(get_input_str())
    inputs = 3036732577212944063491565474664

    num = inputs
    digit_count = len(decompose(num))                             + 1
    digits = decompose(num, digit_count)
    digits = digits * 10000
    digit_count *= 10000

    msg_offset = recompose_top_n_digits(digits, 0, 7)

    for phase_idx in range(100):
        for digit_idx in range(len(digits)):
            pattern = [0] * (digit_idx + 1) + [1] * (digit_idx + 1) + [0] * (digit_idx + 1) + [-1] * (digit_idx + 1)
            new_digit = 0
            pattern_index = 1
            for digit in digits:
                new_digit += digit * pattern[pattern_index % len(pattern)]
                pattern_index += 1
            digits[digit_idx] = (abs(new_digit) % 10)

    num = recompose_top_n_digits(digits, msg_offset, 8)
    return num
