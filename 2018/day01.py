
lines = open("day01.in").readlines()
rows = []

for row in lines:
    rows.append(int(row))

freqH = []

freq = 0
freqH.append(freq)
dup = False

while not dup:
    for row in rows:
        freq += row
        if freq in freqH:
            print(f"dup: {freq}")
            dup = True
            break
        freqH.append(freq)
    print(freq)

print(f"{freq}")
