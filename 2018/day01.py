
lines = open("day01.in").readlines()
rows = []

for row in lines:
    rows.append(int(row))

freqH = set()

freq = 0
freqH.add(freq)
dup = False

part1 = sum(x for x in rows)
part2 = 0

while not dup:
    for row in rows:
        freq += row
        if freq in freqH:
            part2 = freq
            dup = True
            break
        freqH.add(freq)

print(f"part1: {part1}")
print(f"part2: {part2}")
