
serial_num = 1309


def power_level(x, y):
    result = ((x + 10) * y + serial_num) * (x + 10)
    if result < 100:
        result = 0
    else:
        result = int(str(result)[-3])
    result -= 5
    return result


# print(power_level(122, 79))
# print(power_level(217, 196))
# print(power_level(101, 153))

grid = [0] * (300 * 300)
for yy in range(1, 301 - 2):
    for xx in range(1, 301 - 2):
        grid[yy * 300 + xx] = power_level(xx, yy)

best_tl = [0, 0, 0]
highest_level = 0

for yy in range(1, 301 - 2):
    for xx in range(1, 301 - 2):
        for i in range(3, min(100, 301-max(xx, yy))):  # Part 2
        # for i in range(3, min(4, 301-max(xx, yy))):  # Part 1
            p = 0
            for yy2 in range(i):
                for xx2 in range(i):
                    p += grid[(yy + yy2) * 300 + xx + xx2]

            if p > highest_level:
                print(p, xx, yy, i)
                highest_level = p
                best_tl[0] = xx
                best_tl[1] = yy
                best_tl[2] = i
            elif p < -100:
                break
    print("{0:.2f}%".format(yy/301*100))

for yy in range(best_tl[1] - 1, best_tl[1] + 4):
    for xx in range(best_tl[0] - 1, best_tl[0] + 4):
        print(power_level(xx, yy), '\t', end='')
    print()

print(best_tl, highest_level)
