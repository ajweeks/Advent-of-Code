
stepCount = int(open("day_17_input.txt").read())
# stepCount = 3

# Only used in part 1
buffer = [0]

part_1 = False
index = 0
last_val_after_zero = 0
count = 2018 if part_1 else 50000001
for i in range(1, count):
    index = (index + stepCount) % i + 1
    if part_1:
        buffer.insert(index, i)
    elif index == 1:
        print(i)
        last_val_after_zero = i

if part_1:
    print("part 1:", buffer[buffer.index(2017) + 1])
else:
    print("part 2:", last_val_after_zero)
