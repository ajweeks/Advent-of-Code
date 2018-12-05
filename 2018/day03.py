
lines = open("day03.in").readlines()

# lines = """#1 @ 1,3: 4x4
# #2 @ 3,1: 4x4
# #3 @ 5,5: 2x2""".splitlines()

patches = []

for line in lines:
    parts = line.split(' ')
    claim = int(parts[0][1:])
    x = int(parts[2].split(',')[0])
    y = int((parts[2].split(',')[1])[0:-1])
    w = int(parts[3].split('x')[0])
    h = int(parts[3].split('x')[1])
    patches.append([x, y, w, h, claim])
    print(x, y, w, h, claim)

cloth_w = 0
cloth_h = 0
for p in patches:
    cloth_w = max(cloth_w, p[0] + p[2])
    cloth_h = max(cloth_h, p[1] + p[3])
print(f"cloth w, h: {cloth_w}, {cloth_h}")

cloth = [0] * (cloth_w * cloth_h)


for p in patches:
    for yy in range(p[1], p[1] + p[3]):
        for xx in range(p[0], p[0] + p[2]):
            cloth[yy * cloth_w + xx] += 1

for yy in range(cloth_h):
    for xx in range(cloth_w):
        print(f"{cloth[yy * cloth_w + xx]},", end='')
    print()

for p in patches:
    good = True
    for yy in range(p[1], p[1] + p[3]):
        for xx in range(p[0], p[0] + p[2]):
            if cloth[yy * cloth_w + xx] > 1:
                good = False
                break
    if good:
        print(f"good patch: {p[4]}")


numOverlapping = 0
for i in range(cloth_h):
    # print(cloth[i*cloth_w:(i+1)*cloth_w])
    for j in range(cloth_w):
        if cloth[i * cloth_w + j] > 1:
            numOverlapping += 1

print(f"numOverlapping: {numOverlapping}")

