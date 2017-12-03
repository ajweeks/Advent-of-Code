
f = open("day_01_input.txt")

str = f.read()

#str = "1212"

strlen = len(str)
halfstrlen = int(strlen/2)

sum = 0

for i in range(strlen):
    if str[i] == str[(i + halfstrlen) % strlen]:
        sum += int(str[i])

print(sum)
