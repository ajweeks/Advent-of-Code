
lines = open("day10.in").readlines()

# lines = """position=< 9,  1> velocity=< 0,  2>
# position=< 7,  0> velocity=<-1,  0>
# position=< 3, -2> velocity=<-1,  1>
# position=< 6, 10> velocity=<-2, -1>
# position=< 2, -4> velocity=< 2,  2>
# position=<-6, 10> velocity=< 2, -2>
# position=< 1,  8> velocity=< 1, -1>
# position=< 1,  7> velocity=< 1,  0>
# position=<-3, 11> velocity=< 1, -2>
# position=< 7,  6> velocity=<-1, -1>
# position=<-2,  3> velocity=< 1,  0>
# position=<-4,  3> velocity=< 2,  0>
# position=<10, -3> velocity=<-1,  1>
# position=< 5, 11> velocity=< 1, -2>
# position=< 4,  7> velocity=< 0, -1>
# position=< 8, -2> velocity=< 0,  1>
# position=<15,  0> velocity=<-2,  0>
# position=< 1,  6> velocity=< 1,  0>
# position=< 8,  9> velocity=< 0, -1>
# position=< 3,  3> velocity=<-1,  1>
# position=< 0,  5> velocity=< 0, -1>
# position=<-2,  2> velocity=< 2,  0>
# position=< 5, -2> velocity=< 1,  2>
# position=< 1,  4> velocity=< 2,  1>
# position=<-2,  7> velocity=< 2, -2>
# position=< 3,  6> velocity=<-1, -1>
# position=< 5,  0> velocity=< 1,  0>
# position=<-6,  0> velocity=< 2,  0>
# position=< 5,  9> velocity=< 1, -2>
# position=<14,  7> velocity=<-2,  0>
# position=<-3,  6> velocity=< 2, -1>""".splitlines()

stars = []
for line in lines:
    parts = line.split('>')
    pos_x = int(parts[0].split(',')[0].split('<')[1])
    pos_y = int(parts[0].split(',')[1])
    vel_x = int(parts[1].split(',')[0].split('<')[1])
    vel_y = int(parts[1].split(',')[1])
    stars.append([pos_x, pos_y, vel_x, vel_y])

print(stars)

steps = 0
while True:
    draw = False

    t = 300
    t2 = int(t/2)
    n = 0
    for s in stars:
        if -t < s[0] < t and -t < s[1] < t:
            for s2 in stars:
                if s != s2 and abs(s2[0] - s[0]) < 2 and abs(s2[1] - s[1]) < 2:
                    n += 1
                    if n > 30:
                        draw = True
                        break
        if draw:
            break
    if draw:
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for s in stars:
            min_x = min(min_x, s[0])
            min_y = min(min_y, s[1])
            max_x = max(max_x, s[0])
            max_y = max(max_y, s[1])

        for yy in range(min_y, max_y + 5):
            for xx in range(min_x, max_x + 5):
                star_here = False
                for s in stars:
                    if s[0] == xx and s[1] == yy:
                        star_here = True
                        break
                if star_here:
                    print('#', end='')
                else:
                    print('.', end='')

            print()
        print(steps)

        for s in stars:
            s[0] += s[2]
            s[1] += s[3]
        steps += 1
    else:
        step_count = max(1, abs(int(stars[0][0] / stars[0][2])))
        steps += step_count
        for s in stars:
            s[0] += s[2] * step_count
            s[1] += s[3] * step_count
