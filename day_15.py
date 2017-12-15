
f = open("day_15_input.txt")
fileStr = f.read()

# A: 16807
# B: 48271

# % 2147483647

a_start = int(fileStr.splitlines()[0].split()[-1])
b_start = int(fileStr.splitlines()[1].split()[-1])

# a_start = 65
# b_start = 8921

a = a_start
b = b_start

match_count = 0

part_1 = False
pair_eval_count = 40000000 if part_1 else 5000000
for i in range(pair_eval_count):
    a = (a * 16807) % 2147483647
    while a % 4 != 0:
        a = (a * 16807) % 2147483647
    b = (b * 48271) % 2147483647
    while b % 8 != 0:
        b = (b * 48271) % 2147483647
    # print(a, b)

    if (a & 0xFFFF) == (b & 0xFFFF):
        print(a, b, i)
        match_count += 1

print(match_count)
