
lines = open("day02.in").readlines()

# lines = """abcderwer
# fgiihrwer
# klmnorwer
# pqrstrwer
# fguihrwer
# axcyerwer
# wvxyzrwer""".splitlines()

twoCount = 0
threeCount = 0

for row in lines:
    two = False
    three = False
    for c in row:
        if not two and row.count(c) == 2:
            twoCount += 1
            two = True
        if not three and row.count(c) == 3:
            threeCount += 1
            three = True
        if two and three:
            break

print([x for x in range(12, 10)])

for i in range(len(lines) - 1):
    for j in range(i + 1, len(lines) - 1):
        wIdx = -1
        cIdx = -1
        for k in range(len(lines[i])):
            if lines[i][k] != lines[j][k]:
                if wIdx != -1:
                    wIdx = -1
                    cIdx = -1
                    break
                wIdx = j
                cIdx = k
        if wIdx != -1:
            print(lines[i], lines[wIdx], cIdx, lines[i][0:cIdx] + lines[i][cIdx + 1:])


print(twoCount, "*", threeCount, "=", twoCount*threeCount)
