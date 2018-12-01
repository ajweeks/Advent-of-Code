
f = open("day_19_input.txt")

elfCount = int(f.read())
elfCount = 5

elves = []


def next_index(index):
    result_index = (index + 1) % elfCount
    while elves[result_index][0] == 0:
        result_index += 1
        result_index %= elfCount
        if result_index == index:
            return -1
    return result_index


def next_index2(index, elfCount1):
    if elfCount1 == 0:
        return -1

    result_index = int(index + elfCount1 / 2 + 1) % elfCount1
    return result_index


def part_1():
    for i in range(elfCount):
        elves.append({1, i})

    index = 0
    while True:
        n_index = next_index(index)
        if n_index == -1:
            return index
        else:
            elves[index][0] += elves[n_index]
            elves[n_index][0] = 0
            n_index = next_index(n_index)
            if n_index == -1:
                return index
            else:
                index = n_index


def part_2():
    elfCount1 = elfCount
    for i in range(elfCount1):
        elves.append([1, i + 1])

    index = 0
    n_index = next_index2(index, elfCount1)
    while True:
        print(n_index)
        if n_index == -1:
            return index
        else:
            elves[index][0] += elves[n_index][0]
            elves.remove(elves[n_index])
            elfCount1 -= 1
            n_index = next_index2(n_index, elfCount1)
            if n_index == -1:
                return elves[index][1]
            else:
                index = n_index


# print("Last elf standing: ", part_1() + 1)
print("Last elf standing: ", part_2() + 1)

