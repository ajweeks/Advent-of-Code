
f = open("day_03_input.txt")
fileStr = f.read()

cell = int(fileStr)
# cell = 23


def sign(x):
    return x and (1, -1)[x < 0]


def part1(num):
    x = 0
    y = 0

    xx = 1
    yy = 1

    b = True

    for i in range(num - 1):
        if b:
            x += sign(xx)
            if x == xx:
                if xx < 0:
                    xx = (-xx) + 1
                else:
                    xx = -xx
                b = not b
        else:
            y += sign(yy)

            if y == yy:
                if yy < 0:
                    yy = (-yy) + 1
                else:
                    yy = -yy
                b = not b

    print(abs(x) + abs(y))


def get_value_at_coord(target_x, target_y):
    x = 0
    y = 0

    xx = 1
    yy = 1

    b = True

    count = 0

    while True:
        count += 1

        if x == target_x and y == target_y:
            break

        if b:
            x += sign(xx)
            if x == xx:
                if xx < 0:
                    xx = (-xx) + 1
                else:
                    xx = -xx
                b = not b
        else:
            y += sign(yy)

            if y == yy:
                if yy < 0:
                    yy = (-yy) + 1
                else:
                    yy = -yy
                b = not b

    return count


def part2(num):
    nums = []

    x = 0
    y = 0

    xx = 1
    yy = 1

    b = True

    nums.append(1)
    i = 0
    while True:
        neighbor_sum = 0
        if i > 0:  # first value is always 1
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if j == 0 and k == 0:
                        continue

                    index = get_value_at_coord(x + j, y + k)
                    if (index - 1) < len(nums):
                        neighbor_sum += nums[index - 1]

            nums.append(neighbor_sum)

        if b:
            x += sign(xx)
            if x == xx:
                if xx < 0:
                    xx = (-xx) + 1
                else:
                    xx = -xx
                b = not b
        else:
            y += sign(yy)

            if y == yy:
                if yy < 0:
                    yy = (-yy) + 1
                else:
                    yy = -yy
                b = not b

        if neighbor_sum > num:
            print(neighbor_sum)
            break

        i += 1


part1(cell)
part2(cell)
