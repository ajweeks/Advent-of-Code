
f = open("day_13_input.txt")
fileStr = f.read()

# fileStr = "\
# 0: 3\n\
# 1: 2\n\
# 4: 4\n\
# 6: 4"

cols = fileStr.splitlines()
layers = []

max_d = 0

for r in cols:
    ind = int(r.split(':')[0])
    dep = int(r.split(':')[1])
    if dep > max_d:
        max_d = dep
    while ind > len(layers):
        layers.append(-1)
    layers.append(dep)

print(layers)


def draw_area(packet_index):
    print(packet_index, ':', sep='')
    caught = False
    for col in range(len(layers)):
        print(' ', col, ' ', end='', sep='')
    print()

    for d in range(max_d):
        for col in range(len(layers)):
            depth = layers[col]
            if depth == -1 or d >= depth:
                if d == 0 and packet_index == col:
                    print('(.)', end='')
                else:
                    print('...', end='')
            else:
                s = False
                scanner_index = packet_index % (depth * 2 - 2)
                if scanner_index >= depth:
                    s = (depth * 2 - 2) - scanner_index == d
                    print((depth * 2 - 2) - scanner_index, d)
                elif scanner_index == d:
                    s = True

                if d == 0 and packet_index == col:
                    print('(', 'S' if s else ' ', ')', end='', sep='')
                    if s:
                        caught = True
                else:
                    print('[', 'S' if s else ' ', ']', end='', sep='')

        print()
    print('(caught)' if caught else '')
    return caught


def calc_min_delay(packet_index, offset):
    depth = layers[packet_index]
    if depth == -1:
        return False
    else:
        caught = False
        length = (depth * 2 - 2)
        scanner_index = (packet_index + offset) % length
        if scanner_index == 0:
            caught = True
        elif scanner_index >= depth:
            caught = length - scanner_index == 0

        return caught


def main():
    part_1 = False
    if part_1:
        severity = 0
        for layer_index in range(len(layers)):
            if draw_area(layer_index):
                severity += layer_index * layers[layer_index]

        print("severity:", severity)
    else:
        min_delay = -1
        caught = True
        while caught:
            caught = False
            severity = 0
            min_delay += 1
            for layer_index in range(len(layers)):
                if calc_min_delay(layer_index, min_delay):
                    severity += layer_index * layers[layer_index]
                    caught = True
                    break
        print("min delay:", min_delay)

main()
