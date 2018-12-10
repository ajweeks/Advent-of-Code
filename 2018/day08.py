
lines = [int(x) for x in open("day08.in").read().split(' ')]
# lines = [int(x) for x in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(' ')]


def parse(idx):
    # Child count, metadata count, children, metadata entries
    node = [lines[idx], lines[idx + 1], [], []]

    new_idx = idx + 2
    for i in range(lines[idx]):  # Add each child
        new_node, new_idx = parse(new_idx)
        node[2].append(new_node)

    for i in range(lines[idx + 1]):  # Add each metadata entry
        node[3].append(lines[new_idx])
        new_idx += 1

    return node, new_idx


def count_meta(node):
    count = 0

    for i in range(node[0]):
        count += count_meta(node[2][i])

    for i in range(node[1]):
        count += node[3][i]

    return count


def value(node):
    result = 0

    if node[0] > 0:
        indices = [node[3][i] - 1 for i in range(node[1])]
        for i in indices:
            if i == -1 or i >= node[0]:
                continue
            result += value(node[2][i])

    else:
        for i in range(node[1]):
            result += node[3][i]

    return result


root_node, final_idx = parse(0)
print(root_node, count_meta(root_node), value(root_node))


